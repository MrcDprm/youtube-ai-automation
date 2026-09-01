"""Daily queue: topic picking, inbox priority, once-per-day guard, lock, catch-up."""

from __future__ import annotations

import os
from datetime import date, timedelta
from pathlib import Path

import pytest

from modules.queue import (
    DailyLock,
    ScenarioQueue,
    SchedulerState,
    Topic,
    decide_daily_action,
    default_scene_count,
    load_state,
    load_topics,
    next_unused_topic,
    save_state,
)
from utils.exceptions import ConfigurationError
from utils.fs import write_json

TODAY = date(2026, 8, 20)


def _queue(tmp_path: Path) -> ScenarioQueue:
    """Build a queue rooted in the test temp directory."""
    queue = ScenarioQueue(tmp_path / "scenarios")
    queue.ensure()
    return queue


def _topics_file(tmp_path: Path, payload: object) -> Path:
    """Write a topics.json and return its path."""
    path = tmp_path / "topics.json"
    write_json(path, payload)
    return path


# --------------------------------------------------------------------------------------
# Topic loading
# --------------------------------------------------------------------------------------


def test_load_topics_accepts_a_bare_array(tmp_path: Path) -> None:
    """A top-level array is the simplest valid shape."""
    path = _topics_file(tmp_path, ["Kahve", "Mars"])

    topics = load_topics(path)

    assert [item.topic for item in topics] == ["Kahve", "Mars"]


def test_load_topics_accepts_objects_with_overrides(tmp_path: Path) -> None:
    """Object entries carry scene count, guidance and language."""
    path = _topics_file(
        tmp_path,
        {
            "topics": [
                {
                    "topic": "Yapay zeka",
                    "scenes": 12,
                    "guidance": "abartısız",
                    "language": "tr",
                }
            ]
        },
    )

    topic = load_topics(path)[0]

    assert topic.topic == "Yapay zeka"
    assert topic.scenes == 12
    assert topic.guidance == "abartısız"
    assert topic.language == "tr"


def test_load_topics_skips_blank_strings(tmp_path: Path) -> None:
    """Empty strings are ignored rather than becoming unusable topics."""
    path = _topics_file(tmp_path, ["  ", "Kahve", ""])

    assert [item.topic for item in load_topics(path)] == ["Kahve"]


def test_missing_topics_file_is_a_configuration_error(tmp_path: Path) -> None:
    """A missing file has a hint pointing at the example."""
    with pytest.raises(ConfigurationError, match="not found"):
        load_topics(tmp_path / "nope.json")


def test_malformed_topic_entry_is_rejected(tmp_path: Path) -> None:
    """A number where a string or object belongs is a schema error, not a skip."""
    path = _topics_file(tmp_path, [42])

    with pytest.raises(ConfigurationError, match="string or an object"):
        load_topics(path)


def test_object_without_topic_field_is_rejected(tmp_path: Path) -> None:
    """An object that forgot the only required key fails loudly."""
    path = _topics_file(tmp_path, {"topics": [{"scenes": 3}]})

    with pytest.raises(ConfigurationError, match="missing a non-empty"):
        load_topics(path)


# --------------------------------------------------------------------------------------
# Unused-topic picking
# --------------------------------------------------------------------------------------


def test_next_unused_topic_is_case_insensitive() -> None:
    """Regenerating the same wording in a different case must not count as new."""
    topics = [Topic("Kahve"), Topic("Mars")]
    picked = next_unused_topic(topics, ["KAHVE"])
    assert picked is not None
    assert picked.topic == "Mars"


def test_next_unused_topic_returns_none_when_exhausted() -> None:
    """An exhausted list is idle, not an error inside the picker."""
    assert next_unused_topic([Topic("Kahve")], ["kahve"]) is None


def test_default_scene_count_falls_back() -> None:
    """A string topic uses the daily default; an object can override it."""
    assert default_scene_count(Topic("Kahve"), fallback=8) == 8
    assert default_scene_count(Topic("Kahve", scenes=12), fallback=8) == 12


# --------------------------------------------------------------------------------------
# Daily decision
# --------------------------------------------------------------------------------------


def test_inbox_wins_over_the_topic_list(tmp_path: Path) -> None:
    """A dropped scenario is how a human overrides the model for a day."""
    queue = _queue(tmp_path)
    (queue.inbox / "hand.json").write_text("{}", encoding="utf-8")

    action = decide_daily_action(
        queue=queue,
        topics=[Topic("Kahve")],
        state=SchedulerState(),
        today=TODAY,
    )

    assert action.kind == "inbox"
    assert action.inbox_path == queue.inbox / "hand.json"


def test_already_ran_today_is_a_skip(tmp_path: Path) -> None:
    """The once-per-day guard is the YouTube-quota safety net."""
    queue = _queue(tmp_path)
    state = SchedulerState(last_success_date=TODAY.isoformat())

    action = decide_daily_action(queue=queue, topics=[Topic("Kahve")], state=state, today=TODAY)

    assert action.kind == "skip"


def test_force_overrides_the_once_per_day_guard(tmp_path: Path) -> None:
    """--force is how you redo a day on purpose."""
    queue = _queue(tmp_path)
    state = SchedulerState(last_success_date=TODAY.isoformat())

    action = decide_daily_action(
        queue=queue, topics=[Topic("Kahve")], state=state, today=TODAY, force=True
    )

    assert action.kind == "generate"
    assert action.topic is not None
    assert action.topic.topic == "Kahve"


def test_missed_days_still_produce_only_one_video(tmp_path: Path) -> None:
    """Catch-up is one video, never a burst equal to the number of days missed."""
    queue = _queue(tmp_path)
    state = SchedulerState(last_success_date=(TODAY - timedelta(days=4)).isoformat())

    action = decide_daily_action(
        queue=queue, topics=[Topic("Kahve"), Topic("Mars")], state=state, today=TODAY
    )

    assert action.kind == "generate"
    assert action.topic is not None
    assert action.topic.topic == "Kahve"
    assert "one video" in action.reason
    assert "4 day" in action.reason


def test_empty_topics_and_empty_inbox_is_idle(tmp_path: Path) -> None:
    """Nothing to do is a clean exit, not a crash."""
    queue = _queue(tmp_path)

    action = decide_daily_action(queue=queue, topics=[], state=SchedulerState(), today=TODAY)

    assert action.kind == "idle"


def test_exhausted_topics_is_idle(tmp_path: Path) -> None:
    """When every topic has been used the operator has to add more."""
    queue = _queue(tmp_path)
    state = SchedulerState(used_topics=["Kahve"])

    action = decide_daily_action(queue=queue, topics=[Topic("Kahve")], state=state, today=TODAY)

    assert action.kind == "idle"
    assert "already been used" in action.reason


# --------------------------------------------------------------------------------------
# Queue moves
# --------------------------------------------------------------------------------------


def test_claim_moves_inbox_to_processing(tmp_path: Path) -> None:
    """Claiming is a rename, so a crash cannot process the same inbox file twice."""
    queue = _queue(tmp_path)
    source = queue.inbox / "job.json"
    source.write_text("{}", encoding="utf-8")

    claimed = queue.claim(source)

    assert claimed.parent == queue.processing
    assert not source.exists()
    assert claimed.exists()


def test_complete_success_moves_to_done(tmp_path: Path) -> None:
    """A successful render leaves the scenario in done/."""
    queue = _queue(tmp_path)
    processing = queue.processing / "job.json"
    processing.write_text("{}", encoding="utf-8")

    resting = queue.complete(processing, ok=True)

    assert resting.parent == queue.done
    assert not processing.exists()


def test_complete_failure_does_not_consume_the_filename(tmp_path: Path) -> None:
    """A failed render is kept for inspection, under a unique name if done/failed collide."""
    queue = _queue(tmp_path)
    (queue.failed / "job.json").write_text("old", encoding="utf-8")
    processing = queue.processing / "job.json"
    processing.write_text("new", encoding="utf-8")

    resting = queue.complete(processing, ok=False)

    assert resting.name == "job-2.json"
    assert resting.read_text(encoding="utf-8") == "new"


# --------------------------------------------------------------------------------------
# State persistence
# --------------------------------------------------------------------------------------


def test_success_records_the_date_and_the_topic(tmp_path: Path) -> None:
    """The next invocation uses last_success_date for the once-per-day guard."""
    path = tmp_path / "state.json"
    state = SchedulerState()
    state.record(status="success", today=TODAY, topic="Kahve", project_id="kahve-20260820")
    save_state(path, state)

    loaded = load_state(path)

    assert loaded.already_ran_on(TODAY)
    assert loaded.used_topics == ["Kahve"]
    assert loaded.last_project_id == "kahve-20260820"


def test_failed_run_does_not_consume_the_topic(tmp_path: Path) -> None:
    """A failed generation must be retried tomorrow with the same topic."""
    state = SchedulerState()
    state.record(status="failed", today=TODAY, topic="Kahve")

    assert state.used_topics == []
    assert state.last_success_date is None


def test_missing_state_file_is_empty(tmp_path: Path) -> None:
    """First run has no history."""
    state = load_state(tmp_path / "missing.json")

    assert state.last_success_date is None
    assert state.used_topics == []


def test_corrupt_state_file_is_treated_as_empty(tmp_path: Path) -> None:
    """A truncated state file must not crash the daily command."""
    path = tmp_path / "state.json"
    path.write_text("{not json", encoding="utf-8")

    assert load_state(path).used_topics == []


# --------------------------------------------------------------------------------------
# Lock
# --------------------------------------------------------------------------------------


def test_lock_refuses_a_second_acquirer(tmp_path: Path) -> None:
    """Two overlapping daily runs cannot both produce a video."""
    directory = tmp_path / "scheduler"
    with (
        DailyLock(directory),
        pytest.raises(ConfigurationError, match="already in progress"),
        DailyLock(directory),
    ):
        pass


def test_stale_lock_is_stolen(tmp_path: Path) -> None:
    """A crash leftover must not block the next morning's run forever."""
    directory = tmp_path / "scheduler"
    directory.mkdir()
    lock_path = directory / "daily.lock"
    lock_path.write_text("1", encoding="utf-8")
    os.utime(lock_path, (0, 0))

    with DailyLock(directory):
        assert lock_path.exists()

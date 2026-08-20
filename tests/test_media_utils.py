"""Geometry math, filesystem helpers and secret redaction."""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from utils.exceptions import FontNotFoundError
from utils.fs import (
    atomic_write_bytes,
    format_bytes,
    hash_payload,
    human_duration,
    resolve_font,
    safe_filename,
)
from utils.logger import SecretRedactingFilter
from utils.media import (
    aspect_ratio,
    classify_orientation,
    distribute_duration,
    make_even,
    matches_orientation,
    plan_scale_and_crop,
    resolution_for_orientation,
    zoom_scale_at,
)

# --------------------------------------------------------------------------------------
# Scale and crop
# --------------------------------------------------------------------------------------


def test_landscape_source_to_portrait_target_exact_math() -> None:
    """A 1920x1080 source becomes exactly 1080x1920 with the expected crop offsets.

    Cover scale is max(1080/1920, 1920/1080) = 1.7778, so the source becomes 3413x1920 and
    1166 pixels are trimmed from the width, 1166 // 2 = 583 from the left.
    """
    plan = plan_scale_and_crop(1920, 1080, 1080, 1920)

    assert plan.scale == pytest.approx(1920 / 1080)
    assert plan.scaled_height == 1920
    assert plan.scaled_width == 3414  # 3413.33 rounds to 3413, then up to the next even number
    assert plan.target_size == (1080, 1920)
    assert plan.crop_x == (3414 - 1080) // 2
    assert plan.crop_y == 0
    assert plan.crop_center == (plan.crop_x + 540, 960)


def test_portrait_source_to_portrait_target_is_a_pure_upscale() -> None:
    """A source already at the target aspect ratio is scaled with no crop."""
    plan = plan_scale_and_crop(540, 960, 1080, 1920)

    assert plan.scaled_size == (1080, 1920)
    assert plan.crop_x == 0
    assert plan.crop_y == 0


def test_exact_match_is_a_no_op() -> None:
    """A source at the exact target size needs neither scaling nor cropping."""
    plan = plan_scale_and_crop(1080, 1920, 1080, 1920)

    assert plan.scale == pytest.approx(1.0)
    assert plan.scaled_size == (1080, 1920)
    assert plan.crop_x == 0
    assert plan.crop_y == 0


def test_portrait_source_to_landscape_target_crops_vertically() -> None:
    """The crop happens on the height when the source is too tall."""
    plan = plan_scale_and_crop(1080, 1920, 1920, 1080)

    assert plan.scaled_width == 1920
    assert plan.scaled_height > 1080
    assert plan.crop_x == 0
    assert plan.crop_y > 0


def test_crop_window_always_fits_inside_the_scaled_frame() -> None:
    """Rounding to even numbers never makes the crop exceed the scaled image."""
    for source in [(1920, 1080), (1280, 720), (3840, 2160), (640, 480), (1001, 999)]:
        for target in [(1080, 1920), (1920, 1080), (1080, 1080)]:
            plan = plan_scale_and_crop(*source, *target)
            assert plan.crop_x >= 0
            assert plan.crop_y >= 0
            assert plan.crop_x + plan.target_width <= plan.scaled_width
            assert plan.crop_y + plan.target_height <= plan.scaled_height


def test_scaled_dimensions_are_always_even() -> None:
    """Odd dimensions would break yuv420p encoding."""
    plan = plan_scale_and_crop(1001, 999, 1080, 1920)
    assert plan.scaled_width % 2 == 0
    assert plan.scaled_height % 2 == 0


def test_non_positive_dimensions_are_rejected() -> None:
    """A zero dimension is a programming error, not a degenerate case to absorb."""
    with pytest.raises(ValueError, match="positive"):
        plan_scale_and_crop(0, 1080, 1080, 1920)


# --------------------------------------------------------------------------------------
# Orientation helpers
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("width", "height", "expected"),
    [
        (1080, 1920, "portrait"),
        (1920, 1080, "landscape"),
        (1080, 1080, "square"),
        (720, 1280, "portrait"),
        (3840, 2160, "landscape"),
    ],
)
def test_classify_orientation(width: int, height: int, expected: str) -> None:
    """Resolutions bucket into the expected orientation."""
    assert classify_orientation(width, height) == expected


def test_matches_orientation_and_canonical_resolutions() -> None:
    """The orientation helpers agree with the canonical resolution table."""
    assert matches_orientation(1080, 1920, "portrait")
    assert not matches_orientation(1080, 1920, "landscape")
    assert resolution_for_orientation("landscape") == (1920, 1080)

    with pytest.raises(ValueError, match="Unknown orientation"):
        matches_orientation(1080, 1920, "diagonal")
    with pytest.raises(ValueError, match="Unknown orientation"):
        resolution_for_orientation("diagonal")


def test_aspect_ratio_rejects_zero_height() -> None:
    """A zero height would divide by zero."""
    with pytest.raises(ValueError, match="positive"):
        aspect_ratio(100, 0)


def test_make_even_rounds_up() -> None:
    """Odd values round up, and the floor is 2."""
    assert make_even(1080) == 1080
    assert make_even(1081) == 1082
    assert make_even(0) == 2
    assert make_even(-5) == 2


# --------------------------------------------------------------------------------------
# Timing helpers
# --------------------------------------------------------------------------------------


def test_zoom_is_clamped_at_both_ends() -> None:
    """Frames requested outside the segment never over- or under-zoom."""
    assert zoom_scale_at(0.0, 4.0, 1.0, 1.06) == pytest.approx(1.0)
    assert zoom_scale_at(2.0, 4.0, 1.0, 1.06) == pytest.approx(1.03)
    assert zoom_scale_at(4.0, 4.0, 1.0, 1.06) == pytest.approx(1.06)
    assert zoom_scale_at(9.0, 4.0, 1.0, 1.06) == pytest.approx(1.06)
    assert zoom_scale_at(-1.0, 4.0, 1.0, 1.06) == pytest.approx(1.0)
    assert zoom_scale_at(1.0, 0.0, 1.0, 1.06) == pytest.approx(1.0)


def test_distribute_duration_sums_exactly() -> None:
    """Slices always sum to the requested total despite floating-point division."""
    slices = distribute_duration(10.0, 3)
    assert len(slices) == 3
    assert sum(slices) == pytest.approx(10.0)


def test_distribute_duration_avoids_sub_minimum_slices() -> None:
    """Rather than emit flashes, fewer and longer slices are returned."""
    slices = distribute_duration(1.0, 4, minimum=0.5)
    assert len(slices) == 2
    assert sum(slices) == pytest.approx(1.0)


def test_distribute_duration_rejects_bad_input() -> None:
    """Non-positive inputs are programming errors."""
    with pytest.raises(ValueError, match="parts"):
        distribute_duration(10.0, 0)
    with pytest.raises(ValueError, match="total"):
        distribute_duration(0.0, 2)


# --------------------------------------------------------------------------------------
# Filesystem helpers
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("Yapay Zekanin Kisa Tarihi", "Yapay-Zekanin-Kisa-Tarihi"),
        ("a/b\\c:d*e?f", "a-b-c-d-e-f"),
        ("  ...  ", "untitled"),
        ("", "untitled"),
    ],
)
def test_safe_filename(raw: str, expected: str) -> None:
    """Arbitrary text becomes a portable filename component."""
    assert safe_filename(raw) == expected


def test_safe_filename_folds_accents() -> None:
    """Turkish characters fold to ASCII rather than being dropped wholesale."""
    assert safe_filename("Gunes Isigi") == "Gunes-Isigi"
    assert "u" in safe_filename("Türkçe")


def test_hash_payload_is_stable_and_order_independent() -> None:
    """Cache keys must not depend on dictionary insertion order."""
    first = hash_payload("text", {"a": 1, "b": 2})
    second = hash_payload("text", {"b": 2, "a": 1})

    assert first == second
    assert len(first) == 64
    assert first != hash_payload("other", {"a": 1, "b": 2})


def test_atomic_write_leaves_no_part_file(tmp_path: Path) -> None:
    """A completed write removes its temporary sibling."""
    target = tmp_path / "nested" / "file.bin"
    atomic_write_bytes(target, b"payload")

    assert target.read_bytes() == b"payload"
    assert not list(tmp_path.rglob("*.part"))


def test_format_bytes_and_duration() -> None:
    """Human-readable formatting matches the documented shapes."""
    assert format_bytes(512) == "512 B"
    assert format_bytes(1536) == "1.5 KB"
    assert format_bytes(5 * 1024**3) == "5.0 GB"

    assert human_duration(45) == "0:45"
    assert human_duration(125) == "2:05"
    assert human_duration(3725) == "1:02:05"
    assert human_duration(-5) == "0:00"


# --------------------------------------------------------------------------------------
# Font resolution
# --------------------------------------------------------------------------------------


def test_resolve_font_prefers_the_exact_path(fonts_dir: Path) -> None:
    """An existing configured font is used verbatim, with no warning."""
    existing = next(fonts_dir.iterdir())
    resolved, warning = resolve_font(existing, fonts_dir=fonts_dir)

    assert resolved == existing
    assert warning is None


def test_resolve_font_falls_back_to_the_bundled_directory(fonts_dir: Path, tmp_path: Path) -> None:
    """A missing font is substituted from the project font directory, with a warning."""
    resolved, warning = resolve_font(tmp_path / "Nonexistent.ttf", fonts_dir=fonts_dir)

    assert resolved.parent == fonts_dir
    assert warning is not None
    assert "falling back" in warning


def test_resolve_font_matches_by_name_in_the_font_directory(fonts_dir: Path) -> None:
    """A font of the same name inside the project directory is preferred over a scan."""
    existing = next(fonts_dir.iterdir())
    resolved, warning = resolve_font(Path("elsewhere") / existing.name, fonts_dir=fonts_dir)

    assert resolved == existing
    assert warning is not None


def test_resolve_font_raises_when_nothing_exists(tmp_path: Path) -> None:
    """With no bundled font and no system scan, resolution fails loudly."""
    empty = tmp_path / "empty"
    empty.mkdir()

    with pytest.raises(FontNotFoundError) as info:
        resolve_font(tmp_path / "missing.ttf", fonts_dir=empty, allow_system_fallback=False)

    assert info.value.hint is not None


# --------------------------------------------------------------------------------------
# Secret redaction
# --------------------------------------------------------------------------------------


def _record(message: str, args: tuple[object, ...] = ()) -> logging.LogRecord:
    """Build a log record for redaction tests."""
    return logging.LogRecord(
        name="pipeline.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg=message,
        args=args,
        exc_info=None,
    )


def test_registered_secret_is_redacted() -> None:
    """A literal registered secret never reaches a handler."""
    secret = "abc123def456ghi789jkl012mno345pqr678stu"
    redactor = SecretRedactingFilter([secret])
    record = _record(f"Calling API with key={secret}")

    redactor.filter(record)

    assert secret not in str(record.msg)
    assert "***REDACTED***" in str(record.msg)


def test_short_values_are_not_redacted() -> None:
    """Short strings are too generic to blanket-replace."""
    redactor = SecretRedactingFilter(["abc"])
    record = _record("the abc of it")

    redactor.filter(record)

    assert "abc" in str(record.msg)


def test_unregistered_api_key_shapes_are_still_redacted() -> None:
    """Pattern matching catches keys that were never registered."""
    redactor = SecretRedactingFilter()

    google_key = redactor.redact("key AIza" + "B" * 35 + " end")
    assert "AIza" not in google_key

    oauth_secret = redactor.redact("GOCSPX-" + "a" * 28)
    assert "GOCSPX" not in oauth_secret

    query = redactor.redact("https://example.com/v?api_key=supersecretvalue123&z=1")
    assert "supersecretvalue123" not in query


def test_bearer_tokens_are_redacted() -> None:
    """Authorization headers echoed into an error body are scrubbed."""
    redactor = SecretRedactingFilter()
    cleaned = redactor.redact("Authorization: Bearer " + "t" * 40)
    assert "t" * 40 not in cleaned


def test_redaction_covers_log_arguments() -> None:
    """Secrets passed as lazy formatting arguments are redacted too."""
    secret = "zzzz1111yyyy2222xxxx3333wwww4444vvvv5555"
    redactor = SecretRedactingFilter([secret])
    record = _record("key is %s", (secret,))

    redactor.filter(record)

    assert record.args is not None
    assert secret not in str(record.args)


def test_filter_never_drops_records() -> None:
    """The filter censors rather than suppresses."""
    assert SecretRedactingFilter().filter(_record("harmless")) is True

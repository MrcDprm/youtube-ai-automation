"""Author After Hours File episode 1: South Goodwin lightship, nineteen fifty four."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, file_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_file_scenario, write_scenario

TERMS = ("night illustration", "archive folder")

CHAPTERS = [
    """The Goodwin Sands do not need a door. They sit off the coast of Kent like a graveyard that keeps its own hours, a ten-mile bank that has taken ships the way a ledger takes names. On the night of the twenty sixth of November, nineteen fifty four, a Trinity House lightvessel was supposed to be the one thing that did not move. Her name was South Goodwin. Her number was Lightvessel ninety. A lightship is a promise written in iron: we stay, so you do not hit the sand. Around midnight the lamp was still a lamp. The radio room was still a room a man could walk to. Then the folder stops having a sentence from that room. Sister ships saw a light leave its station. Shore heard the neighbors. The South Goodwin itself did not finish the call. That is the file. Not a haunting. A radio that did not get its turn. The sands were doing what sands do. The lamp was doing what a lamp is hired to do. The gap is the walk between the galley and the set.""",
    """Start with what a lightship is, because the public treats a light as weather. Lightvessel ninety was built in nineteen thirty seven at Dartmouth, one hundred eighteen feet of iron and steel, unpowered, towed to a station four miles off Dover and told to stay. Engines aboard ran a winch, a foghorn, a lamp. Four mushroom anchors were supposed to hold her. Trinity House crewed her with civilians, mostly men who already knew long water: Horace Thomas Skipp the master, and six others, among them Tom Porter and a fog-signal driver named Viney. For a month they also had a guest. Ronald Murton was twenty two, from the Ministry of Agriculture, aboard to watch migratory birds that used the lightship as a roost. He had not come to be in a disaster file. He had come to count wings. The sandbank he sat above has been called a ship swallower for centuries. Shakespeare put the Goodwins in a play. Ian Fleming parked a fictional lightship on the same compass point. None of that is evidence. It is how a hazard becomes a story before the radio even fails.""",
    """The weather that night was not a mood. Papers later called it the worst gale in a generation: hurricane force, flooding ashore, other ships in trouble in the same hours. Between midnight and one, the men tried to take bearings. Skipp could not at first tell if they were still on the mooring. An unpowered vessel in a storm does not announce drift with a speech. It announces drift by the lamp no longer sitting where a chart says a lamp must sit. Murton, unable to sleep, went up and found the master and crew trying to make the night into numbers. They mustered in the galley, seven seafarers and the guest crammed into a small hot room while the hull argued with the sea. Skipp turned toward the radio room. That sentence is in the survivor's later account and in Trinity House's telling. He did not get the sentence onto the air. The ship lurched, went hard to starboard, and the galley became a room with the wrong door. The file's first blank is here: the call that was intended and not sent.""",
    """The alarm that reached land did not come from Lightvessel ninety. It came from people watching a lamp misbehave. East Goodwin, in some tellings North Goodwin, saw the sister light sweep off station, a red barque married to a compass point until it was not. They radioed the mainland. Ramsgate and Deal coastguards were already uneasy in poor visibility. Lifeboats from Dover and Ramsgate went out and could not close. A lightship is a station. When the station walks, the chart becomes a rumor. The public will later want a last transmission, a sentence that proves someone inside knew. The folder has the neighbors' sentences. It does not have Skipp's. That is not proof of a secret. It is proof of a lurch that arrived between a man and a set. Separate those. The claim is: they were going to call. The evidence is: other lamps called about them. The gap is not a ghost. The gap is time, measured in hull degrees.""",
    """Dawn is when a closed file pretends it will open. A United States Air Force helicopter from the air-sea rescue squadron at Manston found the hull on the sands, on her side, partly a wreck and partly a hill of iron. Someone was on the scaffolding of the lamp, pyjamas, nine hours of holding on. They had to leave and come back with fuel. On the second pass they hovered low and took Ronald Murton off. He was twenty two and he had gone through a skylight when the galley filled. He later said he had heard tapping from inside, a sound he took for men still in a compartment, Skipp and Porter and Viney among them. Hope is a document too. It got written into the morning papers. It is allowed to be true as a hearing and still fail as a rescue. Lifeboats still could not board. The tide still had hours. The helicopter still could not cut a ship open from thirty feet. Murton lived. That is not a miracle the folder invented. It is a winch and a crew who went back.""",
    """The twenty eighth of November is the date the folder tries to finish. Trinity House tender Patricia, a navy ship, divers, cutting gear on a sandbank. They reached the hull when the weather allowed. They did not find the seven. Not a roll call. Not a neat ending. Sand had begun to take the rooms. Later writers will say the sea washed the crew out. That is a theory wearing work clothes. It is not a photograph. The file can hold Murton's tapping and the empty search in the same clip without making them into a haunting. Trapped men tap. Storms move sand. Both can be written. Neither requires a visitor from outside the weather. Do not mock Murton for hearing a hull. Do not promote the tap to a message from the other side. The honest sentence is: he reported a sound, and the search did not return the men the sound implied.""",
    """There is an older page in the same drawer, and it is a temptation. In nineteen forty a previous South Goodwin lightvessel left her station in wartime and was later found as a wreck with a hole that looks like a mine. In eighteen ninety nine a lightship on this sand also broke her ground tackle. The sands keep a habit. Habit is not destiny, but it is a pattern a chart already knew. In nineteen fifty four the question that will not sit still is smaller than war. Were all four mushroom anchors down. An unpowered ship with a short mooring is a bet on iron. If the bet fails, the lamp becomes a drifting hazard, which is the one job a lightship is not allowed. The sister ships did their job by reporting. The South Goodwin's job was to stay and then, failing that, to speak. She stayed until she did not. She did not speak. The folder's cruelty is that the public hears 'lightship' and imagines a lighthouse that can steam. She could not steam. She could only hold, or fail, or fall.""",
    """What did we file, then, besides grief. We filed a weather extreme, a station lost, a guest who lived, seven names that Deal and Ramsgate would have to carry into a fund: Skipp, Cox, Lanham, Philpott, Viney, Lynn, Porter. We filed a helicopter that went twice. We filed divers who arrived late because the Channel does not take appointments. We did not file a last radio from Lightvessel ninety. That missing page is why the night still feels unfinished, and unfinished is not the same as unexplained. A lurch can delete a transmission without deleting physics. The sands can keep men without becoming a myth. The honest open loop is narrower: the lamp moved, the neighbors spoke, the intended call did not land, and the search on the twenty eighth did not close the galley. You may want a villain. The folder offers a gale, a mooring, and a room that filled faster than a walk to a set.""",
    """Leave the file on the desk. The Goodwin Sands are still a bank. Trinity House still marks water, now with machines that do not sleep in a galley. The replacement South Goodwin later got a helipad, a sentence that reads like an apology in steel. Ronald Murton went ashore. The seven did not. The radio room on Lightvessel ninety did not get to be the author of its own last line. That is not a ghost story. It is a chain of minutes: bearings, galley, a turned back, a starboard fall, a sister lamp reporting a drift, a helicopter at dawn, a search two days later that found weather and sand. If you need a moral, do not take 'the sea is haunted.' Take this: a light that does not move is a staff of men, and when the light moves, the first thing the chart loses is their sentence. The folder remains open where Skipp's call should be. Open is the correct stamp. Closed would be a lie the Channel did not earn.""",
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, ten-second cadence)."""
    seconds = index * 10
    return f"{seconds // 60:02d}{seconds % 60:02d}"


STYLE = (
    "Painterly night illustration, 16:9, mud-green and charcoal, weak yellow lamp, "
    "fog, no photoreal faces, no flags, no gore, no stickman, no MS Paint cartoon."
)

_ROWS: list[tuple[str, str, str]] = [
    ("sands-bank", "The Goodwin Sands do not need a door.", f"Dark sandbank in a night channel, pale foam, distant Kent shore smudge. {STYLE}"),
    ("ledger-names", "A bank that takes ships the way a ledger takes names.", f"Open ledger on a dark desk, wet sand grains on the page, no people. {STYLE}"),
    ("kent-night", "Off the coast of Kent, twenty sixth of November, nineteen fifty four.", f"Simple night map of Kent coast and a sandbank, no flags, date not written. {STYLE}"),
    ("lamp-promise", "A lightship is a promise written in iron.", f"Unpowered lightvessel lamp glowing in storm murk, hull small against waves. {STYLE}"),
    ("stay-sand", "We stay, so you do not hit the sand.", f"Chart line from lamp to hidden sandbar, weak yellow thread. {STYLE}"),
    ("midnight-lamp", "Around midnight the lamp was still a lamp.", f"Close lamp glass in rain, charcoal sky. {STYLE}"),
    ("radio-room", "The radio room was still a room a man could walk to.", f"Empty radio room, headphones on hook, weak lamp, no operator face. {STYLE}"),
    ("folder-blank", "Then the folder stops having a sentence from that room.", f"Manila folder open, one page blank, yellow lamp. {STYLE}"),
    ("sister-saw", "Sister ships saw a light leave its station.", f"Two distant lamps, one drifting off a dotted station mark. {STYLE}"),
    ("shore-heard", "Shore heard the neighbors. South Goodwin did not finish the call.", f"Shore radio set glowing, empty chair, storm window. {STYLE}"),
    ("not-haunting", "Not a haunting. A radio that did not get its turn.", f"Radio handset hanging, not haunted, just unused. {STYLE}"),
    ("gap-walk", "The gap is the walk between the galley and the set.", f"Narrow ship corridor, galley glow one end, radio door the other. {STYLE}"),
    ("public-weather", "The public treats a light as weather.", f"Window lamp mistaken for a storm glow, no people. {STYLE}"),
    ("dartmouth-hull", "Built nineteen thirty seven, Dartmouth, iron and steel.", f"Shipyard hull at night, no flags, wet iron. {STYLE}"),
    ("unpowered", "Unpowered, towed to a station four miles off Dover.", f"Tug silhouette towing a dark lightvessel, no faces. {STYLE}"),
    ("winch-fog", "Engines for a winch, a foghorn, a lamp.", f"Foghorn throat and lamp cage, no crew. {STYLE}"),
    ("mushroom-anchors", "Four mushroom anchors were supposed to hold her.", f"Four mushroom anchors on a chain, sand below. {STYLE}"),
    ("civilians", "Trinity House civilians who knew long water.", f"Empty oilskins on pegs in a dim cabin. {STYLE}"),
    ("skipp-name", "Horace Thomas Skipp the master.", f"Nameplate SKIPP on a cabin door, no portrait. {STYLE}"),
    ("six-others", "Six others, among them Porter and Viney.", f"Six empty mugs on a galley shelf. {STYLE}"),
    ("murton-guest", "Ronald Murton, twenty two, Ministry of Agriculture.", f"Bird notebook and binoculars on a bunk, no face. {STYLE}"),
    ("count-wings", "Aboard a month to count wings on the lamp.", f"Birds as tiny pale marks around a lamp, not cute cartoon. {STYLE}"),
    ("swallower", "The sandbank called a ship swallower.", f"Masts sticking from sand at night, distant, no corpses. {STYLE}"),
    ("not-play", "A play and a novel are not evidence.", f"Closed book beside a real chart, chart winning. {STYLE}"),
    ("not-mood", "The weather that night was not a mood.", f"Barometer needle buried in storm, cabin lamp. {STYLE}"),
    ("force-gale", "Hurricane force, flooding ashore in the same hours.", f"Coast town windows dark, spray, no people. {STYLE}"),
    ("bearings", "Between midnight and one they tried to take bearings.", f"Compass and parallel rulers sliding on a wet chart. {STYLE}"),
    ("on-station", "Skipp could not tell if they were still on the mooring.", f"Two chart positions overlapping, question not written. {STYLE}"),
    ("drift-quiet", "Drift does not announce itself with a speech.", f"Lamp slightly off a station ring on a chart. {STYLE}"),
    ("galley-muster", "They mustered in the galley, eight people in a small room.", f"Crowded galley implied by coats and steam, silhouettes only, no faces. {STYLE}"),
    ("turned-radio", "Skipp turned toward the radio room.", f"Silhouette in a hatch toward a radio glow, no face. {STYLE}"),
    ("no-air", "He did not get the sentence onto the air.", f"Microphone unkeyed, empty chair. {STYLE}"),
    ("starboard", "The ship lurched hard to starboard.", f"Interior tilting, cups leaving a table, no people falling. {STYLE}"),
    ("wrong-door", "The galley became a room with the wrong door.", f"Galley door underwater-dark, air pocket lamp. {STYLE}"),
    ("first-blank", "The file's first blank: the call intended and not sent.", f"Clipboard with a blank radio log line. {STYLE}"),
    ("neighbors", "The alarm came from people watching a lamp misbehave.", f"Another lightvessel watching a drifting lamp. {STYLE}"),
    ("east-north", "East Goodwin saw the sister light leave.", f"Two lamps, one leaving a dotted circle. {STYLE}"),
    ("coastguard", "Ramsgate and Deal uneasy in poor visibility.", f"Coastguard window, rain, radio glow, empty. {STYLE}"),
    ("boats-out", "Lifeboats went out and could not close.", f"Lifeboat in huge night sea, far from a dark hull. {STYLE}"),
    ("station-walks", "When the station walks, the chart becomes a rumor.", f"Chart with a walking lamp icon, no cartoon face. {STYLE}"),
    ("want-last", "The public wants a last transmission.", f"Crowd of blank paper expecting a quote. {STYLE}"),
    ("neighbors-sentences", "The folder has the neighbors' sentences, not Skipp's.", f"Two radio logs filled, one empty. {STYLE}"),
    ("not-secret", "Not proof of a secret. Proof of a lurch.", f"Hull angle diagram, simple, dark. {STYLE}"),
    ("claim-evidence", "Claim: they were going to call. Evidence: other lamps called.", f"Split: unkeyed mic vs distant lamp. {STYLE}"),
    ("dawn-hull", "Dawn: hull on the sands, on her side.", f"Capsized lightvessel on a sandbank at grey dawn, no bodies. {STYLE}"),
    ("scaffolding", "Someone on the lamp scaffolding.", f"Tiny silhouette on lamp cage, distant, no face detail. {STYLE}"),
    ("helicopter", "A rescue helicopter from Manston had to leave and return.", f"Helicopter shape over wreck, no national markings, no flags. {STYLE}"),
    ("second-pass", "On the second pass they took Murton off.", f"Winch line toward the lamp cage, silhouette. {STYLE}"),
    ("skylight", "He had gone through a skylight when the galley filled.", f"Skylight from below, water line, no drowning figure. {STYLE}"),
    ("tapping", "He later said he heard tapping from inside.", f"Ear toward a steel wall, implied, no face. {STYLE}"),
    ("hope-paper", "Hope got written into the morning papers.", f"Newspaper stack, headline not readable, grey dawn. {STYLE}"),
    ("cannot-cut", "A helicopter cannot cut a ship open from thirty feet.", f"Helicopter high above a sealed hull. {STYLE}"),
    ("murton-lived", "Murton lived. A winch and a crew who went back.", f"Hospital-window dawn, empty bed implied, no face. {STYLE}"),
    ("twenty-eighth", "The twenty eighth of November tries to finish the folder.", f"Calendar page, storm still drawn in the margin. {STYLE}"),
    ("divers-late", "Divers arrived when the weather allowed.", f"Divers as distant shapes, hull in sand, no gore. {STYLE}"),
    ("not-found", "They did not find the seven.", f"Empty cabins in a tilted hull, sand on the floor. {STYLE}"),
    ("tap-and-empty", "Tapping and an empty search in the same clip.", f"Folder with two photos: wall, empty bunk. {STYLE}"),
    ("older-page", "An older page: a wartime lightvessel that left station.", f"Older wreck silhouette, separate from nineteen fifty four. {STYLE}"),
    ("anchors-question", "The question: were all four mushroom anchors down.", f"Four anchors, one chain slack. {STYLE}"),
    ("open-stamp", "The folder remains open where Skipp's call should be.", f"Rubber stamp OPEN beside a blank radio line, yellow lamp. {STYLE}"),
]


def _beats() -> list[tuple[str, str, str]]:
    """Stamp each row with a ten-second mmss slug prefix."""
    need = file_beat_count(600.0)
    if len(_ROWS) != need:
        raise SystemExit(f"need {need} beats, got {len(_ROWS)}")
    stamped: list[tuple[str, str, str]] = []
    used: set[str] = set()
    for index, (slug, covers, prompt) in enumerate(_ROWS):
        full = f"{_stamp(index)}-{slug}"
        if full in used:
            raise SystemExit(f"duplicate slug {full}")
        used.add(full)
        stamped.append((full, covers, prompt))
    return stamped


def main() -> None:
    beats = _beats()
    draft = DraftScript(
        title="The Night the Lightship Stopped Answering",
        description=(
            "South Goodwin, nineteen fifty four. The sister lamps reported a drift. "
            "The radio room on Lightvessel ninety did not get its sentence on the air. "
            "The folder is still open where the call should be."
        ),
        tags=(
            "mystery",
            "lightship",
            "night",
            "archive",
            "radio",
            "sea",
            "storm",
            "kent",
            "sands",
            "file",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="WENT QUIET",
    )
    scenario = build_file_scenario(
        draft,
        topic="The Night the Lightship Stopped Answering",
        language="en",
        minutes=10,
        target_seconds=600.0,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-file.json"
    named = PROJECT_ROOT / "senaryo-file-lightship.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))
    print("voice", scenario.tts.voice, "rate", scenario.tts.rate, "cat", scenario.youtube.category_id)
    print("hook", scenario.youtube.thumbnail_hook)


if __name__ == "__main__":
    main()

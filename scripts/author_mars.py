"""Author Drawn Anyway episode 5: Mars Climate Orbiter, nineteen ninety nine."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 600.0
MINUTES = 9
VOICE = "en-US-GuyNeural"
RATE = "+2%"

CHAPTERS = [
    """NASA once lost a Mars probe to a unit conversion. That is not a metaphor, and it is not a cartoon you invented after a spreadsheet. On the eleventh of December nineteen ninety eight, Mars Climate Orbiter left Cape Canaveral on a Delta Two, bound to become the first interplanetary weather satellite and a radio relay for a lander still on the pad. Nine and a half months later, on Thursday the twenty third of September nineteen ninety nine, it fired its main engine to grab Mars. The carrier signal was last seen at about nine oh four fifty two UTC, forty nine seconds earlier than the predicted occultation. Exhaustive attempts to find it ran through the twenty fifth. They did not. Keep that picture. A spacecraft that worked. A ground file that did not. Pound-force seconds where newton-seconds were specified. A factor of four point four five hiding in the cruise. Everything after this is just that picture arriving at the wrong altitude.""",
    """Start with why the file even existed. In the mid nineties NASA's Mars Surveyor program handed JPL the lead and picked Lockheed Martin Astronautics in Denver as prime contractor for the hardware. JPL kept navigation, mission design, and the overall map. Lockheed flew the bus and, later, spacecraft operations from Colorado. The pair was Mars Surveyor ninety eight: Climate Orbiter plus Polar Lander, about three hundred twenty seven point six million dollars for both, not counting Deep Space Two. The official idea was a weather station in orbit and a relay for a south-polar landing in December. The unofficial weather in the building was faster, better, cheaper, which is a slogan that does not print units on a file. The spacecraft was to skim the upper atmosphere for weeks of aerobraking after capture, using a five and a half meter solar array as a brake. Planned first periapsis after insertion: two hundred twenty six kilometers. Plans that assume two software teams share a unit without checking the handshake should be stored with the other fiction.""",
    """Here is the boring mechanism that ate the mission, and it is not a conspiracy. Spacecraft attitude uses reaction wheels. Wheels saturate. You dump momentum with tiny thruster firings called angular momentum desaturation, AMD events. Telemetry comes down. Ground software named SM_FORCES turns those firings into an impulse number and writes an AMD file. The JPL operations navigation team feeds that file into trajectory models. The Software Interface Specification said the impulse bit would be newton-seconds. The software on the spacecraft used metric and was correct. The mismatch lived only in the ground code. Lockheed's SM_FORCES reported pound-force seconds. Navigation treated the same digits as newtons. One pound-force is about four point four five newtons, so every desat was underestimated by that factor. Small forces. Small print. A planet-sized miss.""",
    """The error did not arrive as a single bang. For the first four months of cruise the AMD files were so messy, format errors and bad attitude quaternions, that navigators did not even use them. They got emails when a desat happened and tried to model the shove themselves. Files were not usable until April nineteen ninety nine. Within a week the numbers already looked low. Doppler could only see the thrust along the Earth line of sight. Most of the AMD shove was perpendicular to that line, and perpendicular to the flight path, which is a fancy way of saying the mistake was aimed at altitude and hiding from the radio. AMD events also happened ten to fourteen times more often than the ops navigators expected, because the solar array was lopsided compared with Mars Global Surveyor. A daily barbecue flip that would have cancelled momentum was deleted from the plan and that decision was not walked over to navigation. The ops navigation team had come aboard shortly before launch. They had not sat in the ground-software tests or the design reviews. Critical momentum lore stayed with the people who had already left the room. If this already sounds like a bad idea written in two cities, you are paying attention.""",
    """On the eighth of September they computed Trajectory Correction Maneuver four. On the fifteenth they flew it, aiming for that two hundred twenty six kilometer periapsis. During the next week orbit determination slid the number down to one hundred fifty to one hundred seventy kilometers. Twenty four hours before insertion, about one hundred ten. Eighty kilometers was thought to be the floor the airframe could survive. Throughout spring and summer, working-level people had already noticed residuals between expected and observed Doppler on the more frequent AMD events. Those notes stayed informal. Three orbit-determination schemes disagreed: Doppler-only kept placing insertion closer to the planet than range. The discrepancies were not resolved. A contingency TCM-five existed on paper to raise a dangerous periapsis. It was discussed verbally shortly before the insertion procedure started. It was never executed. Tests and procedures for it were not finished. The onboard insertion timeline did not leave room to upload, fire, and check a last shove. Polar Lander still needed the orbiter as a relay on a clock. So they went to the burn with a number that kept getting shorter.""",
    """Mars orbit insertion engine start: nine oh oh forty six UTC, the twenty third of September. About five minutes into a planned sixteen minute burn, the spacecraft went behind the planet. Occultation hit forty nine seconds early. Signal was not back when the clock said it should be. Controllers at JPL in Pasadena and Lockheed in Denver hunted through the twenty fifth. After the fact, with the small-forces delta-V corrected, the board judged the first periapsis at about fifty seven kilometers, too low to live. Either the atmosphere ate it or it skipped into a useless orbit. The cartoon is the file, not a Hollywood fireball. Do not turn it into a gore reel of melting metal. The leftover fact is a specification that two teams did not share out loud.""",
    """NASA stood up a Mishap Investigation Board on the fifteenth of October, chaired by Arthur G. Stephenson, director of Marshall Space Flight Center. Phase I, dated the tenth of November nineteen ninety nine, had to move fast because Polar Lander was still inbound for early December. The root cause they wrote down is the sentence you already know: failure to use metric units in the Small Forces ground software. Eight contributing causes sat under it: systems engineering that did not walk from development into operations, communications that failed between Denver and Pasadena, a navigation team that boarded late and missed the software tests and design reviews, a missing end-to-end check of the AMD handshake. The board told the lander team to audit units on every file passed between JPL navigation and spacecraft operations. That is not a secret cabal. That is a project that treated a unit as obvious. Obvious is how a factor of four point four five lives for nine months in a file both sides thought they understood.""",
    """Aftermath is where the spreadsheet beats the newsreel. Polar Lander would fail on its own later; that is a different receipt, and this episode is not that autopsy. This receipt is Climate Orbiter: onboard metric, ground English, SIS not followed, files late, thrusters mostly invisible to Doppler, a last correction that stayed verbal. The pair of Surveyor ninety eight ships cost about three hundred twenty seven point six million, of which the hardware, the rocket, and the operations each took a slice. You are allowed to laugh at pounds versus newtons. You are not required to pretend the people were cartoon villains, or that Mars reached up and snatched a healthy trajectory, or that a slogan about cheapness is a complete autopsy. A file can hold a working spacecraft and a wrong impulse bit at the same time. The working spacecraft is not the plot. The impulse bit is.""",
    """So who won. Not the thrusters. Not the weather satellite that never took a weather shift. The factor of four point four five won the headline. Stephenson's board won a sentence NASA still assigns as homework. Denver and Pasadena won a reminder that a specification is not a vibe. If you need a moral, skip space is hard as a shrug. Take this: a trajectory model is a terrible place to store an unchecked unit. The next time someone hands you a file both teams swear is obvious, remember April, when the numbers already looked low, and TCM-five, which stayed a conversation. Would you have stopped the burn at one hundred ten kilometers. A working bus, a ground file in the wrong pounds, a factor of four point four five, and a planet that did not get a vote. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags, "
    "no photoreal faces, no NASA logo replicas, no exploding bodies. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("units-open", "NASA lost a Mars probe to a unit conversion.", f"Cartoon title beat: a simple toy spacecraft beside giant LBF and N labels, cream Mars disk. {STYLE}"),
    ("not-a-spreadsheet", "Not a metaphor. Not a cartoon after a spreadsheet.", f"Ink the mascot shaking his head at a spreadsheet with a red X, mouth closed. {STYLE}"),
    ("december-launch", "Eleventh of December nineteen ninety eight, Cape Canaveral.", f"Cartoon calendar December 11 1998, tiny rocket leaving a cream coast, no flags. {STYLE}"),
    ("weather-satellite", "First interplanetary weather satellite, plus a lander relay.", f"A toy orbiter with a WEATHER badge and a tiny lander icon on a leash. {STYLE}"),
    ("nine-months", "Nine and a half months later: Mars insertion day.", f"A dotted cruise line from Earth-dot to Mars-dot, 9.5 MONTHS. {STYLE}"),
    ("last-signal", "Last carrier at about 09:04:52 UTC, September 23, 1999.", f"A radio dish, a clock 09:04:52, a signal line that stops. {STYLE}"),
    ("forty-nine-early", "Occultation forty nine seconds earlier than predicted.", f"A stopwatch showing -49s, Mars disk covering a tiny craft. {STYLE}"),
    ("keep-picture", "A working spacecraft. A ground file that did not.", f"Split: healthy toy probe versus a folder labeled WRONG UNITS. {STYLE}"),
    ("four-four-five", "Pound-force seconds where newton-seconds were specified.", f"Two rubber stamps: lbf-s versus N-s, the left one circled. {STYLE}"),
    ("surveyor-office", "Why the file existed: Mars Surveyor ninety eight.", f"A project office door MSP 98, two ship icons on the glass. {STYLE}"),
    ("two-cities", "JPL navigation. Lockheed hardware in Denver.", f"Two simple city desks with a dotted file flying between them, no logos stolen. {STYLE}"),
    ("three-twenty-seven", "About 327.6 million for orbiter and lander together.", f"A cartoon invoice 327.6 M, two tiny spacecraft line items. {STYLE}"),
    ("faster-cheaper", "The building weather was faster, better, cheaper.", f"A slogan banner FASTER BETTER CHEAPER over an empty UNITS checkbox. {STYLE}"),
    ("aerobrake-plan", "After capture: weeks of aerobraking on a 5.5 meter array.", f"A toy craft dipping a single solar wing through a thin pink air layer. {STYLE}"),
    ("two-twenty-six", "Planned first periapsis: 226 kilometers.", f"A Mars disk with a 226 KM altitude ring, neat and hopeful. {STYLE}"),
    ("wheels-saturate", "Reaction wheels saturate. You dump momentum with thrusters.", f"Cartoon flywheels with a FULL meter, tiny thruster puffs, no fireball. {STYLE}"),
    ("amd-events", "Those dumps are AMD events, angular momentum desaturation.", f"A clipboard labeled AMD EVENT, a small puff icon. {STYLE}"),
    ("sm-forces", "Ground software SM_FORCES writes the AMD file.", f"A computer named SM_FORCES printing a file AMD. {STYLE}"),
    ("sis-said-newtons", "The interface spec said newton-seconds.", f"A spec binder SIS with N-s highlighted in mustard. {STYLE}"),
    ("onboard-correct", "Onboard software used metric and was correct.", f"A spacecraft computer with a green METRIC stamp. {STYLE}"),
    ("ground-pounds", "Ground SM_FORCES reported pound-force seconds.", f"A ground PC with a red lbf-s stamp on its printout. {STYLE}"),
    ("same-digits", "Navigation treated the same digits as newtons.", f"One number 1.00 under two unit hats, N and lbf. {STYLE}"),
    ("factor-hiding", "Every desat underestimated by 4.45.", f"A scale 1 versus 4.45, the small weight on the trajectory. {STYLE}"),
    ("messy-four-months", "First four months: AMD files too messy to use.", f"A stack of error-stamped files, navigators using a paper airplane EMAIL. {STYLE}"),
    ("april-low", "April 1999: files work, numbers already look low.", f"Calendar April 1999, a graph sagging under EXPECTED. {STYLE}"),
    ("doppler-blind", "Doppler only sees along the Earth line of sight.", f"Earth-dot, a thin LOS beam, thruster arrow sideways missing the beam. {STYLE}"),
    ("aimed-at-altitude", "The hidden shove was aimed at altitude.", f"A trajectory dipping, a sideways AMD arrow pushing it down. {STYLE}"),
    ("ten-to-fourteen", "AMD events 10 to 14 times more often than expected.", f"A tally exploding 10-14x, surprised navigator hat. {STYLE}"),
    ("lopsided-wing", "The solar array was lopsided compared with Global Surveyor.", f"Two craft: symmetric wings versus one big wing, momentum swirl. {STYLE}"),
    ("barbecue-cut", "A daily barbecue flip was deleted, not walked to navigation.", f"A BBQ MODE plan with a red X, a memo that never leaves the desk. {STYLE}"),
    ("tcm-four", "September 8: they compute TCM-4. September 15: they fly it.", f"Calendar Sep 8 compute, Sep 15 fire, aiming at 226 KM. {STYLE}"),
    ("one-fifty", "Next week the number slides to 150-170 kilometers.", f"Altitude rings shrinking 226 to 160, cream Mars. {STYLE}"),
    ("one-ten", "Twenty four hours out: about 110 kilometers.", f"A 24H clock, 110 KM ring almost on the disk. {STYLE}"),
    ("eighty-floor", "Eighty kilometers was thought to be the survival floor.", f"A FLOOR tape at 80 KM, the craft still above it, barely. {STYLE}"),
    ("doppler-screams", "Doppler-only solutions kept screaming closer-in.", f"Two clipboards: DOPPLER low, RANGE higher, unresolved. {STYLE}"),
    ("tcm-five-paper", "Contingency TCM-5 existed on paper to raise periapsis.", f"A dusty TCM-5 folder labeled CONTINGENCY, unopened. {STYLE}"),
    ("verbal-only", "It was discussed verbally shortly before insertion. Never flown.", f"Speech bubbles over a console, a big NOT FLOWN stamp. {STYLE}"),
    ("no-room", "The onboard burn timeline left no room to upload a last shove.", f"A packed timeline bar, TCM-5 squeezed off the end. {STYLE}"),
    ("relay-clock", "Polar Lander still needed the orbiter as a relay on a clock.", f"A lander hourglass tied to an orbiter icon. {STYLE}"),
    ("engine-start", "Insertion start 09:00:46 UTC, September 23.", f"Clock 09:00:46, a tiny engine flame icon, no disaster gore. {STYLE}"),
    ("behind-the-planet", "Five minutes in, it went behind Mars. Signal did not return.", f"Mars disk eclipsing a craft, radio waves stopping. {STYLE}"),
    ("fifty-seven", "After the fact: about 57 kilometers. Too low to live.", f"A 57 KM ring cutting the atmosphere layer, craft as a dotted outline. {STYLE}"),
    ("not-a-fireball", "The cartoon is the file, not a Hollywood fireball.", f"Ink ripping a FIREBALL movie ticket, holding the AMD folder, mouth closed. {STYLE}"),
    ("stephenson-board", "October 15: Arthur G. Stephenson chairs the mishap board.", f"A board table nameplate STEPHENSON, PHASE I folder, no portrait. {STYLE}"),
    ("november-tenth", "November 10, 1999: Phase I names the root cause.", f"Calendar Nov 10 1999, a stamp ROOT CAUSE: UNITS. {STYLE}"),
    ("eight-causes", "Eight contributing causes under the sentence you know.", f"A stack of eight sticky notes: tests, cities, reviews, handshake. {STYLE}"),
    ("late-navigators", "Ops navigation boarded late, missed software tests and reviews.", f"An empty chair at TEST, a late hat arriving at LAUNCH. {STYLE}"),
    ("no-end-to-end", "Nobody end-to-end checked the AMD handshake.", f"Two pipes that do not quite meet, a 4.45 leak. {STYLE}"),
    ("not-a-cabal", "Not a secret cabal. A unit treated as obvious.", f"Ink stamping OBVIOUS on a spec, then frowning, mouth closed. {STYLE}"),
    ("other-receipt", "Polar Lander is a different receipt. This one is the impulse bit.", f"Two folders: THIS FILE and OTHER FILE, the first one open. {STYLE}"),
    ("working-bus", "A working bus and a wrong impulse bit in the same file.", f"Healthy toy spacecraft sitting on a wrong-units printout. {STYLE}"),
    ("who-won", "Who won. The factor 4.45 won the headline.", f"A trophy labeled 4.45, tiny spacecraft in the audience. {STYLE}"),
    ("stop-the-burn", "Would you have stopped the burn at 110 kilometers.", f"A big STOP handle next to a 110 KM gauge, Ink watching, mouth closed. {STYLE}"),
    ("comment-hook", "Tell me in the comments. That is the receipt. Drawn anyway.", f"Ink the mascot pointing at the viewer, mouth closed, cream paper. {STYLE}"),
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, ten-second cadence)."""
    seconds = index * 10
    return f"{seconds // 60:02d}{seconds % 60:02d}"


def _beats() -> list[tuple[str, str, str]]:
    """Stamp each row with a ten-second mmss slug prefix."""
    need = drawn_beat_count(BEAT_SECONDS)
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
        title="The Probe That Died of Units",
        description=(
            "Mars Climate Orbiter, nineteen ninety nine. A working spacecraft, "
            "a ground file in pound-force seconds, and a factor of four point four five."
        ),
        tags=(
            "history",
            "nasa",
            "mars",
            "cartoon",
            "true story",
            "1999",
            "units",
            "engineering",
            "funny",
            "climate orbiter",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="WRONG UNITS",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Probe That Died of Units",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-mars.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    board = PROJECT_ROOT / "output" / "storyboard" / scenario.project_id
    board.mkdir(parents=True, exist_ok=True)
    tsv = board / "beats.tsv"
    lines = ["index\tfilename\tprompt"]
    for index, (slug, _covers, prompt) in enumerate(beats, start=1):
        lines.append(f"{index:03d}\t{index:02d}-{slug}.png\t{prompt}")
    tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")
    chars = sum(len(scene.narration) for scene in scenario.scenes)
    print(scenario.project_id)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", chars)
    print("voice", scenario.tts.voice, "rate", scenario.tts.rate)
    print("accent", scenario.subtitles.accent_color, "numerals", scenario.subtitles.numeral_display)
    print("hook", scenario.youtube.thumbnail_hook)
    print("tsv", tsv)


if __name__ == "__main__":
    main()

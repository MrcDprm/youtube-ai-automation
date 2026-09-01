"""Author Drawn Anyway episode 26: Hubble spherical aberration, nineteen ninety."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 630.0
MINUTES = 9
VOICE = "en-US-GuyNeural"
RATE = "+2%"

CHAPTERS = [
    """The most expensive science telescope NASA had ever flown was off by about one fiftieth the width of a human hair. That is not a metaphor, and it is not a cartoon you invented after a trivia night about a blurry Hubble joke. On the twenty fourth of April nineteen ninety, Space Shuttle Discovery, mission STS-31, put the Hubble Space Telescope into orbit at eight thirty three in the morning Eastern. On the twenty seventh of June, NASA told the press the primary mirror had the wrong curve. Spherical aberration. Too flat at the outer edge by about two point two microns. Light did not meet at one focus. Keep that split: the glass was polished to a polish, and the polish was the wrong prescription. Then put a red X on the joke that NASA never tested anything. The leftover is not a conspiracy. The leftover is a test they trusted more than the tests that were right.""",
    """Start with why one measuring box was supposed to be the truth. Hubble is a Ritchey-Chrétien Cassegrain: two hyperbolic mirrors, compact enough to fly. The primary is about seven point nine feet across, two point four meters, Ultra-Low Expansion glass, about one thousand eight hundred twenty five pounds. NASA wanted it in nineteen eighty three. Technical delays, budget, then Challenger in eighty six grounded the fleet. Wikipedia files about six million dollars a month to keep the telescope in a clean room on nitrogen. Ground software was barely ready even in ninety. Perkin-Elmer in Danbury, Connecticut, later Hughes Danbury, won the mirror. NASA made them subcontract a backup to Kodak, using traditional polishing, because the fancy computer-controlled machines might fail. Kodak and Itek had even bid a double-check plan that would almost certainly have caught the error. That backup now sits in the National Air and Space Museum, uncoated so you can see the structure. Launch spend sat around four point seven billion in later twenty ten dollars. The official idea was: certify the reflective null corrector, then believe only that.""",
    """File the box, because a millimetre is not a vibe. A null corrector is a template. It turns a spherical test wave into the shape a perfect Hubble primary should send back. Perkin-Elmer's reflective null corrector had two small mirrors and a lens. During setup, a metering rod and a field cap with a pinhole were supposed to set the lens. New Scientist, quoting Lew Allen, files stray light: a reflective region around the pinhole bounced the beam off the cap instead of the end of the rod, about one point three millimetres. UPI filed spacing washers of that same thickness as another possible cause. The Allen Board later measured the preserved device and said one point three millimetres accounts in detail for the blur. Zero point four wave rms wavefront error at six hundred thirty two point eight nanometres. Ten times the specified tolerance, NASA later said. During grind they had conventional refractive nulls. For final figuring they switched to the custom reflective box and treated it as the only test that counted. An inverse null corrector, built to mimic a perfect primary, showed the error. A second null used to measure vertex radius showed the error. Both were discounted as themselves flawed. They ground a perfect wrong mirror.""",
    """Here is the leftover the late-night shows filed as a national punchline. Discovery launched on the twenty fourth of April. Crew: Loren Shriver, Charles Bolden, Steven Hawley, Bruce McCandless, Kathryn Sullivan. First light, Wikipedia's service date, the twentieth of May. Both cameras, the Wide Field and Planetary Camera and the Faint Object Camera, showed the same distortion. So it was not one instrument. June twenty seventh: public announcement. July second: Optical Systems Board of Investigation, Lew Allen of JPL in the chair. They found the null corrector still assembled as it had been nine years earlier. The error was in the primary, too flat away from centre. Even with the flaw, NASA notes Hubble could already do science the ground could not. That is not a defence of a millimetre. It is a file: blurry was not the same as blind. Charles Pellerin, astrophysics, pulled about sixty million dollars for a fix and publicly committed to repair by ninety four. Kodak's backup could not be swapped in orbit. Bringing the telescope home was too slow and too expensive. The leftover of a precise wrong curve is that you can write the opposite curve.""",
    """The prescription had a name. Wide Field and Planetary Camera Two was redesigned with its own internal correction. For the other axial instruments, Ball Aerospace and NASA built COSTAR, Corrective Optics Space Telescope Axial Replacement. NASA calls it about the size of a large refrigerator; another NASA page says telephone-booth-sized. Five pairs of small mirrors on arms, some as small as a nickel, to send corrected light to the Faint Object Camera, the Faint Object Spectrograph, and the Goddard High Resolution Spectrograph. To make room, the High Speed Photometer came out. Servicing Mission One, Endeavour, December nineteen ninety three, STS-61. Kathryn Thornton and Thomas Akers among the spacewalkers who put COSTAR in. WFPC2 went in the radial bay. Solar arrays, gyros, magnetometers, computer coprocessors, a boost to a higher orbit. Before and after of galaxy M100 became the receipt. Later instruments carried their own glasses. COSTAR left in two thousand nine, Smithsonian now, Cosmic Origins Spectrograph in the hole.""",
    """Rehook, because the internet likes a story that NASA is a clown college. Put a red X on that sermon. A certified template is not a personality. Ignoring two cheaper tests is logistics, not a plot to waste a decade. The Allen report is public: they placed complete reliance on the reflective null and did not verify its dimensions after original assembly. That is a process failure you can read. It is not a secret. Perkin-Elmer had been trusted because the box was supposed to be more accurate than the backups. The backups were less precise and still loud enough to scream. File both. Do not invent sabotage. Do not invent a cover-up. The leftover is uglier and smaller: a pinhole reflection, a millimetre, and a meeting that believed the expensive instrument.""",
    """File what the glasses actually did. After ninety three, Hubble became the poster of a repaired machine. More than one and a half million observations in NASA's later count. WFPC2 worked until later cameras replaced it. By two thousand two, new instruments had built-in correction and COSTAR was leftover hardware. The High Speed Photometer, the instrument that paid for the glasses, sits at the University of Wisconsin-Madison. The error never left the primary. Every later camera is still a prescription written against two point two microns. That is the honest leftover. You do not sand a two-metre hyperboloid in a spacesuit. You add the opposite mistake on purpose. A backup Kodak mirror on a museum floor is a costume for a test plan that would have caught it on the ground. A nickel-sized corrector is a costume for a millimetre nobody remeasured. The inverse null had already won, and then lost the meeting.""",
    """None of this is a hymn to a perfect agency, and none of it is a cartoon of grinders as villains. They had a two point four metre disk. They had a custom interferometer. They had a Shuttle delay that bought years of nitrogen and still did not include a second look at the box. You are allowed to laugh at a national telescope that needed glasses, and at a field cap that pretended to be the end of a rod, and at a late-night joke that outlived the blur. You are not required to laugh at Sullivan deploying a payload, or at Pellerin moving sixty million, or at a photometer that got pulled so the rest of the light could focus. The official idea was: the certified null is the mirror. The street idea was: Hubble launched broken. The leftover idea is: they already had the error in two other tests, and the fix was a prescription for a curve they had measured too well.""",
    """So who won. Not the reflective box. Not the joke that nothing was tested. The inverse null won a warning that was filed as noise. Kodak won a mirror that never flew. Allen won a report that named a millimetre. Pellerin won a repair date. Thornton and Akers won a refrigerator of mirrors. The High Speed Photometer won a museum in Madison. Hubble won decades of pictures after someone wrote the opposite glasses. If you need a moral, skip NASA is dumb. Take this: a perfect polish is a terrible whole story, and a millimetre is a terrible honest one. The next time someone tells you Hubble launched as a failure, ask whether they mean the two point two microns or the tests that already saw them, and whether the prescription was luck or arithmetic. Would you have believed the expensive box, or the cheap ones that disagreed. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no cruelty, not mud-green archive night, not After Hours File dark. "
    "Hubble shown as a candy telescope, a primary mirror disk, a tiny millimetre ruler, glasses, "
    "a test box, not photoreal NASA logos, not a conspiracy board. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("hair-width", "Off by about 1/50 the width of a human hair. 2.2 microns too flat at the edge.", f"A hair next to a 2.2 MICRON tag, a candy mirror disk. Cream paper. {STYLE}"),
    ("not-trivia", "Not a blurry-Hubble trivia gag.", f"Ink shaking his head at a BLURRY JOKE stamp with a red X, mouth closed. {STYLE}"),
    ("april-24", "24 April 1990, Discovery STS-31, Hubble into orbit.", f"A shuttle tag DISCOVERY STS-31, date 24 APR 1990. {STYLE}"),
    ("june-27", "27 June: NASA announced the primary had the wrong curve.", f"A press card 27 JUN 1990, WRONG CURVE. {STYLE}"),
    ("two-foci", "Spherical aberration: light did not meet at one focus.", f"A candy mirror with two focus dots instead of one. {STYLE}"),
    ("x-never-tested", "Put a red X on the joke that NASA never tested anything.", f"A NEVER TESTED stamp with a giant red X. {STYLE}"),
    ("wrong-box", "Leftover: a test they trusted more than the tests that were right.", f"A gold TEST box beating two smaller RIGHT tests. {STYLE}"),
    ("cassegrain", "Ritchey-Chrétien Cassegrain: two hyperbolic mirrors, compact enough to fly.", f"A two-mirror cartoon telescope, tag RITCHEY-CHRETIEN. {STYLE}"),
    ("mirror-spec", "Primary: 7.9 feet, 2.4 m, 1,825 pounds, Ultra-Low Expansion glass.", f"A disk 2.4 M / 1825 LB. {STYLE}"),
    ("wanted-83", "Wanted in 1983. Delays, then Challenger 1986 grounded the fleet.", f"A calendar 1983 slipped to 1990, shuttle grounded tag. Not gore. {STYLE}"),
    ("six-million", "About $6 million a month in a clean room on nitrogen.", f"A meter 6M / MONTH, NITROGEN, CLEAN ROOM. {STYLE}"),
    ("perkin-elmer", "Perkin-Elmer, Danbury. Later Hughes Danbury. Won the mirror.", f"A factory tag PERKIN-ELMER DANBURY. No photoreal logo mash. {STYLE}"),
    ("kodak-backup", "NASA made them subcontract a Kodak backup with traditional polish.", f"Two disks PRIMARY and KODAK BACKUP. {STYLE}"),
    ("itek-bid", "Kodak and Itek bid a double-check that would almost certainly have caught it.", f"Two clipboards DOUBLE CHECK, stamp WOULD HAVE CAUGHT. {STYLE}"),
    ("museum-uncoated", "Kodak backup now at the Air and Space Museum, uncoated.", f"A museum disk UNCOATED, SMITHSONIAN. {STYLE}"),
    ("official-rnc", "Official idea: certify the reflective null corrector, believe only that.", f"A certified stamp RNC ONLY. {STYLE}"),
    ("null-template", "A null corrector is a template for a perfect primary.", f"A small optical box labeled TEMPLATE. {STYLE}"),
    ("two-mirrors-lens", "RNC: two small mirrors and a lens.", f"Two tiny mirrors and a lens in a candy box. {STYLE}"),
    ("pinhole-cap", "Metering rod and field cap with a pinhole were supposed to set the lens.", f"A rod, a cap with a PINHOLE. {STYLE}"),
    ("stray-light", "Stray reflection off the cap, not the rod: about 1.3 millimetres.", f"A bounce arrow CAP NOT ROD, 1.3 MM. {STYLE}"),
    ("washers", "UPI: spacing washers of that same thickness as another possible cause.", f"Tiny washers 1.3 MM, tag POSSIBLE CAUSE. {STYLE}"),
    ("allen-accounts", "Allen Board: 1.3 mm accounts in detail for the blur.", f"A report card 1.3 MM = BLUR, ALLEN. No portrait. {STYLE}"),
    ("point-four-wave", "0.4-wave rms at 632.8 nm. Ten times the specified tolerance.", f"A tolerance bar 10X SPEC, 0.4 WAVE. {STYLE}"),
    ("switched-box", "Final figuring switched to the custom reflective box as the only test that counted.", f"A switch to RNC ONLY. {STYLE}"),
    ("inverse-null", "An inverse null, mimicking a perfect primary, showed the error.", f"A box INVERSE NULL, stamp SAW IT. {STYLE}"),
    ("vertex-null", "A second null for vertex radius showed the error too.", f"A second box VERTEX, stamp ALSO SAW IT. {STYLE}"),
    ("discounted", "Both discounted as themselves flawed. A perfect wrong mirror.", f"Two tests in a DISCOUNTED bin, a shiny WRONG mirror. {STYLE}"),
    ("sts-31-crew", "Discovery 8:33 a.m. Eastern. Shriver, Bolden, Hawley, McCandless, Sullivan.", f"Five nameplates, clock 8:33 EDT, no portraits. {STYLE}"),
    ("may-20", "First light / entered service: 20 May. Both cameras, same distortion.", f"Two cameras WFPC and FOC, same BLUR stamp. {STYLE}"),
    ("july-2-board", "2 July: Optical Systems Board, Lew Allen of JPL.", f"A folder BOARD 2 JUL, nameplate ALLEN JPL. {STYLE}"),
    ("nine-years", "The null still assembled as it had been nine years earlier.", f"A dusty box 9 YEARS, SAME SETUP. {STYLE}"),
    ("not-blind", "Blurry was not the same as blind. Ground could not do that science.", f"A fuzzy star still tagged SCIENCE, not a black screen. {STYLE}"),
    ("pellerin-60", "Pellerin: about $60 million, publicly committed to repair by 1994.", f"A budget card 60M, date BY 1994, PELLERIN. {STYLE}"),
    ("cant-swap", "Kodak backup could not be swapped in orbit. Home refill too slow.", f"A no-swap stamp IN ORBIT, backup disk on the ground. {STYLE}"),
    ("opposite-curve", "A precise wrong curve means you can write the opposite curve.", f"Two matching S-curves, one inverted, tag PRESCRIPTION. {STYLE}"),
    ("x-clowns", "Rehook: red X on NASA-is-a-clown-college.", f"Ink peeling a CLOWN COLLEGE sticker, mouth closed. {STYLE}"),
    ("wfpc2", "WFPC2 redesigned with its own internal correction.", f"A camera box WFPC2, tag BUILT-IN GLASSES. {STYLE}"),
    ("costar-fridge", "COSTAR: Ball Aerospace, fridge-sized, five pairs of small mirrors.", f"A fridge-shaped box COSTAR, tiny nickel mirrors on arms. {STYLE}"),
    ("hsp-out", "High Speed Photometer came out to make room.", f"An instrument slot HSP OUT, COSTAR IN. {STYLE}"),
    ("dec-93", "SM1, Endeavour, December 1993, STS-61. Thornton and Akers among the walkers.", f"A calendar DEC 1993, ENDEAVOUR STS-61. {STYLE}"),
    ("m100-receipt", "Before and after of galaxy M100 became the receipt.", f"Split blurry vs sharp, tag M100. Cartoon galaxy, not a photo. {STYLE}"),
    ("costar-2009", "COSTAR removed 2009, Smithsonian. COS in the hole.", f"A museum tag COSTAR 2009, hole labeled COS. {STYLE}"),
    ("public-report", "Allen report is public: complete reliance, no remeasure after assembly.", f"A public PDF stamp COMPLETE RELIANCE. {STYLE}"),
    ("no-plot", "Not sabotage. Not a cover-up. A pinhole, a millimetre, an expensive box.", f"A conspiracy board with a red X, leftover 1.3 MM. {STYLE}"),
    ("still-in-glass", "The error never left the primary. Later cameras are still the prescription.", f"A mirror with a permanent 2.2 UM tag, new cameras wearing glasses. {STYLE}"),
    ("madison-hsp", "High Speed Photometer at Wisconsin-Madison. It paid for the glasses.", f"A museum tag HSP MADISON. {STYLE}"),
    ("kodak-costume", "A Kodak disk on a museum floor is a costume for a ground test that would have caught it.", f"A floor disk vs a flying blurry tube. {STYLE}"),
    ("who-won-glasses", "Not the reflective box. The glasses won decades of pictures.", f"A pair of glasses beating a gold RNC box. {STYLE}"),
    ("inverse-won", "The inverse null won a warning that was filed as noise.", f"A warning bell in a NOISE folder. {STYLE}"),
    ("ask-the-tests", "Ask whether they mean 2.2 microns or the tests that already saw them.", f"A question mark over 2.2 UM and two test boxes. {STYLE}"),
    ("expensive-or-cheap", "Would you have believed the expensive box, or the cheap ones that disagreed.", f"Split: gold box vs two cheap boxes, a question mark. {STYLE}"),
    ("prescription-math", "The prescription was arithmetic, not luck.", f"A glasses prescription card ARITHMETIC. {STYLE}"),
    ("two-point-two", "A perfect polish is a terrible whole story. A millimetre is a terrible honest one.", f"A polish rag vs a 1.3 MM ruler. {STYLE}"),
    ("receipt", "They already had the error. Drawn anyway.", f"A receipt card BOX vs GLASSES, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Telescope That Launched Blurry",
        description=(
            "Nineteen ninety. Two point two microns, a millimetre in a test box, "
            "and a prescription they could write because the error was so precise."
        ),
        tags=(
            "history",
            "1990",
            "hubble",
            "nasa",
            "telescope",
            "cartoon",
            "true story",
            "logistics",
            "space",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="OFF BY A HAIR",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Telescope That Launched Blurry",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-hubble.json"
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
    print("preset", scenario.video.preset)
    print("tsv", tsv)


if __name__ == "__main__":
    main()

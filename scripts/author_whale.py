"""Author Drawn Anyway episode 3: Florence exploding whale, nineteen seventy."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 480.0
TARGET_SECONDS = 600.0
MINUTES = 8
VOICE = "en-US-GuyNeural"
RATE = "+2%"

CHAPTERS = [
    """Oregon once tried to delete a whale with dynamite. That is not a metaphor, and it is not a cartoon you invented after lunch. On the ninth of November nineteen seventy, a forty five foot sperm whale, about eight tons, washed ashore south of Florence on the Oregon coast. At first it was a curiosity. Beachcombers came. Kids wanted to climb it. Then the smell moved through the dunes like a second weather system, and the curiosity became a complaint to whoever owned the sand. By the twelfth it was a public-works problem: a stink, a crowd risk, and a beach the law treated as a highway. The Oregon State Highway Division got the job because the sand was their right of way, which is a sentence that should have stopped the meeting and did not. The official idea was neat. Blast the carcass into bite-size pieces. Let gulls and crabs clock in as the cleanup crew. George Thornton, an assistant district engineer, told a camera he was quite confident it would work. Keep that picture. A dead whale. A highway department. A half-ton of dynamite. Seagulls as the subcontractors. Everything after this is just that picture failing in public, on camera, with a punchline that still has a parking space.""",
    """Start with why this was a road job. In nineteen seventy, Oregon beaches sat under the Highway Division, not a parks pamphlet with a cute logo. If the sand was a right of way, the whale was a lane closure with a pulse it no longer had. That is a legal fact that sounds like a joke, which is how you know it is going to go well. District engineer Dale Allen had a hunting trip. Thornton later said he got designated because the others took off hunting when the whale broke, conveniently, he thought. To be fair, they had already planned to go. The whale made them anxious to leave. Thornton was a respected engineer with decades at the agency. He was not a cartoon villain and he was not a man who woke up hoping to be a meme. He was the person still in the office when a forty five foot problem arrived without a form for it. If this already sounds like a bad idea written on a work order, you are paying attention. The whale was real. The smell was real. The org chart was real. The plan assumed a carcass would behave like a boulder you could quarry off a shoulder. Plans that assume a whale is a boulder should be stored with the other fiction, next to the seagull timesheet.""",
    """They ran the options that sound grown-up until you put them on a tide chart. Bury it on the beach: the Pacific uncovers things, and a buried whale is a sequel with worse lighting. Tow it out to sea: it can wash back and become next week's meeting with the same smell and a new memo. Cut it up by hand: nobody volunteered to be that meeting, and the Highway Division was not a flensing station. Burn it: a forty five foot oil fire on a public beach is not a brochure they print in Salem. So they called the United States Navy and munitions people and treated the whale like overburden on a road cut. Dynamite on the landward side, hoping the blast would shove the mess toward the water. A military veteran who happened to be in the area said twenty cases was far too much, and that twenty sticks would have done. The crew went with about a half-ton anyway. That gap is the joke and the paperwork. The plan had consultants. The plan had a number. The number was not the veteran's number, which is how a work order becomes a legend.""",
    """On the twelfth of November, about a quarter mile back, maybe seventy five spectators and reporters waited on a dune as if a highway project needed an audience. KATU's Paul Linnman was there with a microphone and a tone that already knew this might be a sentence. Cameraman Doug Brazil rolled. Thornton, in a hard hat, explained the gull-and-crab theory on camera the way you explain a detour. He gave the signal around three forty five in the afternoon. The beach threw up a column of sand and whale maybe a hundred feet high. Chunks flew in directions the plan had not budgeted. People screamed and ran when they glimpsed pieces coming overhead. A parked sedan near the onlookers was crushed. Walter Umenhofer's car became the most famous Oldsmobile on the Oregon coast for the worst reason. Nobody died. That matters, and it does not make the math good. Linnman later said the blast blasted blubber beyond all believable bounds. Believe him as a reporter with a line that scans. Do not turn it into a gore reel. The cartoon is the plan, not the mess. The mess was already a failure of units.""",
    """Here is the part the seagulls did not file in triplicate. The scavengers who were supposed to eat the leftovers did not clock in. The noise possibly scared them off, which is the kind of detail a plan forgets when it casts wildlife as a sanitation department with a union. Most of the whale was still on the sand. Highway workers had to gather what the sky had redistributed and bury it anyway, the option they had rejected as too tidal, now with extra steps and a news crew. The official idea was a disappearing trick. The leftover fact was shovels. If you came for a clean boom and a clean beach, you already lost the plot. Dynamite is happy when the target is rock. A whale is not rock. A whale is oil and mass and a smell that does not respect a blasting cap. That mismatch is the whole afternoon in one sentence, and it is about to live on videotape until the heat death of local news, which is a long time to be wrong in a hard hat.""",
    """Thornton did not enjoy the encore. For years he avoided the story the way you avoid a plunger you already pressed. He once said that every time he talked about it, it blew up in his face, which is the correct joke and also a man who had done a job with the tools he was handed by an org chart that went hunting. The Highway Division is now ODOT. Beaches are not treated as a place you quarry with explosives. Later stranded whales get buried or hauled, the boring methods, the ones that do not need a quarter-mile viewing dune and a cameraman named Doug. Florence still marks the anniversary because America will commemorate a logistics error if the tape is funny enough. The tape is funny. The work order is the plot. You are allowed to laugh at the gull subcontract. You are not required to pretend the whale was a boulder, or that a half-ton was a precise number, or that confidence on camera is the same thing as a tide chart.""",
    """Aftermath is where the shovel beats the newsreel, again. Chunks had to be collected from parking lots and from roofs a surprising distance away. The odor lingered like a guest who would not take a hint. The highway men finished with burial, which is what they would have done if the dynamite had never been invited to the beach in the first place. The veteran with twenty sticks does not get a statue. The half-ton gets a holiday. That is not a conspiracy. That is how a camera chooses a climax. If you are keeping score at home, the score is: zero human deaths, one crushed sedan, one intact problem, one sentence that still scans, and a pile of work that looked like the original meeting with worse weather. A file can hold a confident quote and a shovel at the same time. You are allowed to laugh at the quote. You are not required to forget the shovel.""",
    """So who won. Not the dynamite. Not the seagulls, who declined the contract. Not the sedan. Thornton won a nickname he did not order and a story he tried not to tell. Linnman won a sentence that still scans. Oregon won a training film in reverse: this is how you do not remove a whale. If you need a moral, skip nature is magic. Take this: a half-ton charge is a terrible instrument for a problem that needed a shovel, a truck, and a tide chart. The next time someone sells you a simple blast for a scattered, stinking, eight-ton problem that refuses to be gravel, remember the veteran with twenty sticks, and the crew that brought twenty cases. Remember the hunting trip. Remember the beach that was a highway. Would you have signed the work order. A beach that was a highway, a hunting trip, a confident engineer, a camera rolling, and gulls that did not show. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags, "
    "no photoreal faces, no animal remains, no blood, no guts. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("whale-job", "Oregon once tried to delete a whale with dynamite.", f"Cartoon title beat: tiny highway crew facing a huge simple whale shape on a cream beach. {STYLE}"),
    ("not-a-metaphor", "Not a metaphor. Not a cartoon you invented.", f"Ink the mascot shaking his head at a dynamite plunger labeled METAPHOR with a red X, mouth closed. {STYLE}"),
    ("november-ninth", "Ninth of November, nineteen seventy, Florence.", f"Cartoon calendar November 9 1970, Oregon coast dunes, no flags. {STYLE}"),
    ("forty-five-foot", "A forty five foot sperm whale, about eight tons.", f"Simple cartoon whale silhouette with 45 FT and 8 TONS labels, not gory. {STYLE}"),
    ("stink-dunes", "By the twelfth it was a public-works problem.", f"Cartoon wavy stink lines over dunes and a tiny town, funny not cruel. {STYLE}"),
    ("beach-highway", "The beach was legally a highway right of way.", f"Cartoon beach with a HIGHWAY stamp and a tiny road sign in sand. {STYLE}"),
    ("gull-crew", "Blast it small. Let gulls clock in as cleanup.", f"Cartoon seagulls wearing tiny hard hats, clipboard, not eating anything gory. {STYLE}"),
    ("thornton-confident", "George Thornton said he was quite confident.", f"Cartoon engineer in a hard hat giving a thumbs up beside a work order, no portrait. {STYLE}"),
    ("keep-picture", "A whale, a highway department, a half-ton charge.", f"Three icons in a row: whale shape, highway hat, dynamite crate, cream paper. {STYLE}"),
    ("road-job", "Why this was a road job.", f"Ink pointing at an org chart that says BEACHES = ROADS, mouth closed. {STYLE}"),
    ("hunting-trip", "Dale Allen had a hunting trip. Thornton stayed.", f"Cartoon office with a GONE HUNTING sign and one remaining chair labeled THORNTON. {STYLE}"),
    ("designated", "He got designated when the whale broke.", f"A work order arrow landing on a hard hat, simple and funny. {STYLE}"),
    ("not-a-villain", "He was a respected engineer, not a cartoon villain.", f"Cartoon medal of COMPETENCE next to a whale-shaped problem, no mockery face. {STYLE}"),
    ("no-form", "No form existed for a forty five foot problem.", f"Empty form tray, whale-shaped hole in the paperwork. {STYLE}"),
    ("whale-is-boulder", "The plan assumed a carcass would act like a boulder.", f"Split image: boulder icon versus whale icon, equals sign cracking. {STYLE}"),
    ("bury-uncovers", "Bury it: the Pacific uncovers things.", f"Cartoon shovel and a tide arrow undoing a sand pile. {STYLE}"),
    ("tow-washes", "Tow it out: it can wash back.", f"Cartoon whale shape on a tide loop arrow, coming back to the same beach. {STYLE}"),
    ("no-brochure-fire", "Burn it: not a brochure.", f"A beach BROCHURE with a red X over a fire icon, no flames on an animal. {STYLE}"),
    ("navy-call", "They called the Navy and munitions people.", f"Cartoon telephone to a navy hat, dynamite crate in the corner, toy-like. {STYLE}"),
    ("landward-charge", "Charges on the landward side, shove it to water.", f"Simple diagram: beach, whale outline, arrows toward the ocean, no gore. {STYLE}"),
    ("twenty-sticks", "A veteran said twenty sticks, not twenty cases.", f"Two cartoon crates: 20 STICKS versus 20 CASES, the small one circled. {STYLE}"),
    ("half-ton", "The crew went with about a half-ton anyway.", f"A scale labeled 1/2 TON next to a tiny ignored sticky note. {STYLE}"),
    ("quarter-mile", "Twelfth of November: a quarter mile back on a dune.", f"Cartoon dune with tiny spectators and a measuring tape 1/4 MILE. {STYLE}"),
    ("seventy-five", "Maybe seventy five spectators and reporters.", f"A small cartoon crowd behind a rope, 75, no panic yet. {STYLE}"),
    ("linnman-brazil", "Paul Linnman on mic. Doug Brazil on camera.", f"Cartoon news camera and mic on a dune, KATU-style, no logos stolen. {STYLE}"),
    ("hardhat-theory", "Thornton on camera: gulls and crabs will finish it.", f"Hard-hat engineer pointing at a seagull icon on a chalkboard. {STYLE}"),
    ("three-forty-five", "Signal around three forty five in the afternoon.", f"Cartoon clock 3:45, plunger handle, cream paper. {STYLE}"),
    ("sand-column", "A hundred-foot column of sand, stylized boom cloud.", f"Cartoon sand-and-smoke column, BOOM letters, no animal pieces. {STYLE}"),
    ("people-run", "People ran when bits arced overhead.", f"Tiny cartoon figures running from dashed overhead arcs, not gory. {STYLE}"),
    ("crushed-car", "A parked sedan was crushed.", f"Cartoon car pancaked under a generic weight labeled DEBRIS, no flesh. {STYLE}"),
    ("umenhofer", "Walter Umenhofer's Oldsmobile became famous for the wrong reason.", f"Cartoon car with a tiny FAMOUS FOR WRONG REASON ribbon. {STYLE}"),
    ("nobody-died", "Nobody died. The math was still bad.", f"A clipboard: CASUALTIES 0, PLAN grade F, funny not grim. {STYLE}"),
    ("linnman-line", "Linnman: blasted blubber beyond all believable bounds.", f"A news script with that line underlined, Ink raising an eyebrow, mouth closed. {STYLE}"),
    ("not-a-gore-reel", "The cartoon is the plan, not the mess.", f"Ink ripping a GRIM REEL ticket, mouth closed. {STYLE}"),
    ("gulls-no", "The seagulls did not clock in.", f"Empty time clock, seagulls flying away, CLOSED sign. {STYLE}"),
    ("still-there", "Most of the whale was still on the sand.", f"Same whale outline after the boom cloud, mostly intact, not gory. {STYLE}"),
    ("bury-anyway", "They buried it anyway, the rejected option.", f"Cartoon shovel returning, tide chart, we told you so energy. {STYLE}"),
    ("shovels", "The leftover fact was shovels.", f"A row of shovels beating a dynamite crate in a tiny trophy pose. {STYLE}"),
    ("not-rock", "Dynamite likes rock. A whale is not rock.", f"Rock icon with a check, whale icon with a red X. {STYLE}"),
    ("videotape", "The afternoon lived on local-news tape.", f"Cartoon TV set looping a boom cloud, not gore. {STYLE}"),
    ("thornton-quiet", "Thornton avoided the encore for years.", f"An engineer putting a mute stamp on a whale-shaped microphone. {STYLE}"),
    ("blew-up-face", "Every time he talked, it blew up in his face.", f"Speech bubble turning into a small cartoon boom, no harm. {STYLE}"),
    ("now-they-bury", "Later whales get buried or hauled. Boring on purpose.", f"Cartoon truck and shovel, DYNAMITE crate in a museum case. {STYLE}"),
    ("anniversary", "Florence still marks the anniversary because the tape is funny.", f"A small town banner WHALE DAY, cream paper, no flags as jokes. {STYLE}"),
    ("work-order-plot", "The tape is funny. The work order is the plot.", f"Work order paper larger than the TV set. {STYLE}"),
    ("not-gravel", "An eight-ton problem that refuses to be gravel.", f"Whale shape sitting on a GRAVEL label that does not fit. {STYLE}"),
    ("twenty-vs-twenty", "Twenty sticks versus twenty cases.", f"Ink holding two signs, 20 STICKS and 20 CASES, mouth closed. {STYLE}"),
    ("comment-hook", "Would you have signed the work order. Tell me in the comments.", f"Ink the mascot pointing at the viewer, mouth closed, cream paper. {STYLE}"),
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
        title="They Blew Up a Whale on the Beach",
        description=(
            "Florence, Oregon, nineteen seventy. A highway department, a half-ton of dynamite, "
            "and seagulls who did not clock in. The leftover tool was a shovel."
        ),
        tags=(
            "history",
            "oregon",
            "whale",
            "cartoon",
            "true story",
            "1970",
            "florence",
            "highway",
            "funny",
            "news",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="BLAST FLOP",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="They Blew Up a Whale on the Beach",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-whale.json"
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

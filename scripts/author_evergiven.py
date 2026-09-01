"""Author Drawn Anyway episode 27: Ever Given in the Suez Canal, twenty twenty one."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 630.0
MINUTES = 9
VOICE = "en-AU-WilliamNeural"
RATE = "+4%"

CHAPTERS = [
    """A four hundred metre container ship parked itself across the Suez Canal and stayed there for six days. That is not a metaphor, and it is not a cartoon you invented after a trivia night about a meme excavator. On the twenty third of March twenty twenty one, at seven forty in the morning Egypt time, Ever Given, IMO nine eight one one zero zero zero, ran aground at kilometre one hundred fifty one, near the village of Manshiyet Rugola. Bow in one bank. Stern nearly in the other. Wikipedia files the blockage at six days and seven hours, twenty three to twenty nine March. No injuries reported in the grounding. Keep that split: the ship was trying to go north to Rotterdam, and the canal treated it like a parked truck. Then put a red X on the joke that one cartoon digger did the whole job. The leftover is not geopolitics. The leftover is a fairway too narrow for a wall of boxes in a forty-knot wind.""",
    """Start with why a convoy was supposed to be the truth. The canal opened in eighteen sixty nine. By twenty twenty one, about fifty ships a day, roughly twelve percent of world trade. For much of the length it is single-lane: convoys take turns. Ever Given is about four hundred metres long, nearly sixty metres wide, about twenty thousand TEU, laid down in twenty fifteen, completed in twenty eighteen for Shoei Kisen, IMO nine eight one one zero zero zero. Panama registry, Japanese owner, leased to Evergreen Marine, managed by Bernhard Schulte Shipmanagement, Indian crew. She had already done this canal twenty two times. On that morning she was fifth in a northbound convoy, fifteen ships behind her, coming from Tanjung Pelepas in Malaysia toward Rotterdam. Two Suez Canal Authority pilots boarded, as Egyptian rules require. Containers stacked on deck act like a sail. Bill Kavanagh later called a Suez transit a very complex, high-risk operation. Wind on a box wall will blow a heavy ship off course, and the momentum is hard to recover. The official idea was: pilots, a convoy, and a cut in the sand will keep a giant centred."""
    ,    """File the morning, because a bank is not a parking space. At seven forty, a sandstorm. Winds exceeding forty knots, about seventy four kilometres an hour. Egyptian meteorologists also filed gusts around fifty kilometres an hour in the area that day. File the range. SCA said the ship lost the ability to steer. Evergreen was told a sudden strong wind made the hull deviate and hit the bottom. Admiral Osama Rabie later told a press conference weather was not the main reason, and technical or human errors might be involved, all to be investigated. File both. Evert Lataire at Ghent later pointed at the bank effect: in a tight channel the stern can swing toward the near bank, plus west-to-east wind on a northbound hull. Panama's later investigation, as filed by gCaptain, put the grounding at seven forty one local, about twelve knots, course three five two, eastern bank, no fatalities, slight bow damage. At that spot the canal can look about three hundred metres across. The fairway, in one case study, is about one hundred twenty one. A four hundred metre stick in a one hundred twenty one metre ditch. That is logistics wearing a dust storm."""
    ,    """Here is the leftover the internet filed as a yellow digger. The blockage sat south of the two-channel stretch, so nobody could go around. On the twenty fifth, the Authority suspended navigation. An advisor to the Egyptian president told the press forty eight to seventy two hours, maximum. Peter Berdowski of Boskalis, hired through SMIT Salvage, said days to weeks. Ships behind were moved to make room. Fuel came off. Nine thousand tonnes of ballast water came off. An excavator started digging at the bow, and that picture became the whole story. Dredgers, Wikipedia and Boskalis both file about thirty thousand cubic metres of sand from under bow and stern. Backup plan C was unloading about eighteen thousand three hundred containers with floating cranes or even heavy-lift helicopters. Deemed impractical and hazardous. Yukito Higaki, president of Shoei Kisen, said the ship was not taking water, and once it refloated it should operate. On the twenty seventh a high tide let tugs move her about seventeen metres north. On the twenty eighth, the seagoing tug Alp Guard arrived, two hundred eighty five tonnes of bollard pull, almost doubling the tow. The leftover of a viral digger is that the tide and the tugs still had to win."""
    ,    """The prescription had a clock. On the twenty ninth, the stern came free about four thirty local. The Italian tug Carlo Magno, about one hundred fifty three tonnes of pull, joined. Ballast was shifted. Towing was timed to a supermoon king tide. Boskalis: fifteen oh five local, the ship was pulled free. Wikipedia: fourteen Egyptian, Dutch, and Italian tugs. SCA chairman Rabie said the stern was already one hundred two metres off the bank instead of four. Great Bitter Lake for inspection. Canal checked, found sound, reopened at nineteen hundred local. By then more than four hundred ships were waiting: about two hundred in the Red Sea, under two hundred in the Mediterranean, around fifty in the Bitter Lakes. Lloyd's List, during the blockage, filed about four hundred million dollars of goods delayed per hour, about nine billion a day. File the range with Wikipedia's nine point six. Rabie later estimated Egypt lost twelve to fifteen million a day in fees. The backlog of delayed ships was cleared by the third of April. Six days of parked steel. Then a queue that still had to walk.""",
    """Rehook, because the internet likes a story that a country is a clown college, or that a woman captain parked it. Put a red X on both sermons. A doctored rumour blamed Marwa Elselehdar, Egypt's first woman ship captain. She was first mate on Aida Four, hundreds of miles away in Alexandria. File the rumour. Do not spend it as a cause. Weather was real. Bank effect is real. A certified canal with two pilots is not a personality. Ignoring the sail-area of a box wall is logistics, not a plot. The leftover is uglier and smaller: a kilometre marker, a gust, a fairway, and a meeting that still had to dig sand because you cannot reverse a four hundred metre momentum with a joke.""",
    """File what the parking ticket actually did. On the thirteenth of April a court in Ismailia seized the ship. The claim exceeded nine hundred sixteen million dollars, including three hundred million for salvage bonus and three hundred million for loss of reputation, as UK P and I Club filed it. Twenty five Indian crew stayed on board. Two left on the fifteenth for urgent personal circumstances. Three more when contracts expired at the end of April. The International Transport Workers Federation said the crew was well cared for and also called them human pawns in a compensation game. File both. Shoei Kisen declared general average, so cargo owners could be asked to chip in to rescue the voyage. On the tenth of May the claim came down to six hundred million. A later settlement around five hundred forty million, plus a seventy five ton tug for the Authority to replace one wrecked in the recovery. Released the seventh of July twenty twenty one. Port Said inspections. Finally sailed the twelfth, more than one hundred days after the bank. Rotterdam. Then Felixstowe. Then out of service, through the canal again in August toward Qingdao for repairs, back in regular service in mid-November."""
    ,    """None of this is a hymn to a perfect canal, and none of it is a cartoon of a crew as villains. They had a twenty-two-time regular. They had a sandstorm and a forty-knot gust. They had a single lane and a ship whose boxes were a sail. You are allowed to laugh at a national shortcut that needed a dredger, and at a yellow excavator that outlived the tide, and at a reputation line on an invoice. You are not required to laugh at twenty five people waiting on a seized hull, or at dredge crews moving thirty thousand cubic metres, or at a supermoon that did more work than a meme. The official idea was: the convoy will fit. The street idea was: they parked a ship with a toy digger. The leftover idea is: the fairway was one hundred twenty one metres, the stick was four hundred, and the fix was sand, tugs, and a tide they could not schedule in a press conference.""",
    """So who won. Not the forty-eight-hour promise. Not the rumour captain. The bank won six days. Lloyd's won a number. Boskalis won a sentence: we pulled it off. Alp Guard and Carlo Magno won a pull. The excavator won a meme. The crew won a long wait and then a release. Shoei Kisen won a settlement and a spare tug to hand over. Garden gnome shops in Europe, in one later write-up, won a shortage joke on the back of a delayed box. If you need a moral, skip the canal is doomed. Take this: a viral digger is a terrible whole story, and a one hundred twenty one metre fairway is a terrible honest one. The next time someone tells you one ship closed world trade for fun, ask how many were already in the convoy, and whether the tide did the last metre. Would you have waited for the king tide, or started unloading eighteen thousand boxes. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no cruelty, not mud-green archive night, not After Hours File dark. "
    "Ever Given shown as a candy container ship, a sand bank, a tiny yellow excavator, tugs, "
    "not photoreal shipping logos, not a geopolitics lecture, no national flags as the joke. "
    "Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, oversized black marker, "
    "mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("parked-ship", "A 400-metre ship parked across the Suez Canal for six days.", f"A candy container ship wedged across a narrow blue canal. Cream paper. {STYLE}"),
    ("not-trivia", "Not a meme-excavator trivia gag.", f"Ink shaking his head at a MEME DIGGER stamp with a red X, mouth closed. {STYLE}"),
    ("march-23", "23 March 2021, 7:40 Egypt time, Ever Given aground.", f"A clock 0740, date 23 MAR 2021, tag EVER GIVEN. {STYLE}"),
    ("km-151", "Kilometre 151, near Manshiyet Rugola.", f"A canal marker KM 151, tiny village tag. {STYLE}"),
    ("bow-stern", "Bow in one bank. Stern nearly in the other.", f"A ship as a diagonal stick, bow and stern in sand. {STYLE}"),
    ("x-digger-alone", "Put a red X on the joke that one cartoon digger did the whole job.", f"A tiny yellow digger with a giant red X. {STYLE}"),
    ("fairway", "Leftover: a fairway too narrow for a wall of boxes in a 40-knot wind.", f"A wind arrow 40 KN on a wall of candy boxes in a thin ditch. {STYLE}"),
    ("1869", "Canal opened 1869. By 2021: about 50 ships a day, ~12% of world trade.", f"A tally 50 SHIPS / DAY, 12 PERCENT TRADE, year 1869. {STYLE}"),
    ("single-lane", "Much of the length is single-lane. Convoys take turns.", f"A one-lane canal with a WAIT tag. {STYLE}"),
    ("ship-spec", "About 400 m long, nearly 60 m wide, about 20,000 TEU.", f"A scale 400 M / 60 M / 20K TEU. {STYLE}"),
    ("owners", "Panama registry, Shoei Kisen owner, Evergreen lease, Schulte manager, Indian crew.", f"Four paper tags OWNER / LEASE / MANAGER / CREW. No flags. {STYLE}"),
    ("22-times", "She had already done this canal 22 times.", f"A punch card 22 TRANSITS. {STYLE}"),
    ("fifth-convoy", "Fifth in a northbound convoy, 15 ships behind, Malaysia to Rotterdam.", f"A convoy 5TH, tag 15 BEHIND, arrow ROTTERDAM. {STYLE}"),
    ("two-pilots", "Two Suez Canal Authority pilots boarded.", f"Two nameplates PILOT, tag SCA. No portraits. {STYLE}"),
    ("boxes-sail", "Stacked containers act like a sail.", f"Box stacks catching wind, tag SAIL. {STYLE}"),
    ("official-centred", "Official idea: pilots, a convoy, and a cut will keep a giant centred.", f"A centred-ship stamp OFFICIAL PLAN. {STYLE}"),
    ("sandstorm", "7:40, sandstorm. Winds exceeding 40 knots.", f"A dust cloud, tag 40 KN. {STYLE}"),
    ("lost-steer", "SCA: lost the ability to steer. Evergreen: sudden wind, hull hit bottom.", f"Two press cards STEER LOST and HIT BOTTOM. {STYLE}"),
    ("rabie-weather", "Rabie: weather not the main reason. Technical or human errors to be investigated.", f"A quote card NOT THE MAIN REASON, nameplate RABIE. {STYLE}"),
    ("bank-effect", "Bank effect: stern can swing toward the near bank in a tight channel.", f"A stern swinging toward a sandy bank, tag BANK EFFECT. {STYLE}"),
    ("12-knots", "Panama file: 7:41 local, about 12 knots, course 352, eastern bank.", f"A speed tag 12 KN, course 352. {STYLE}"),
    ("121-metres", "Canal looks ~300 m across. Fairway about 121 m. Ship 400 m.", f"A ruler 121 M FAIRWAY vs 400 M SHIP. {STYLE}"),
    ("no-go-around", "South of the two-channel stretch. Nobody could go around.", f"A blocked canal, NO GO AROUND stamp. {STYLE}"),
    ("48-72", "Advisor: 48 to 72 hours, maximum. Berdowski: days to weeks.", f"Two clocks 48-72 HRS vs DAYS TO WEEKS. {STYLE}"),
    ("ballast-off", "Fuel off. 9,000 tonnes of ballast water off.", f"A tank tag 9000 T BALLAST OFF. {STYLE}"),
    ("excavator-bow", "An excavator started digging at the bow. The picture became the whole story.", f"A tiny yellow excavator at a giant candy bow. {STYLE}"),
    ("30k-sand", "About 30,000 cubic metres of sand dredged from under bow and stern.", f"A pile 30000 M3 SAND. {STYLE}"),
    ("plan-c", "Plan C: unload ~18,300 containers. Deemed impractical.", f"A crane over boxes, stamp IMPRACTICAL. {STYLE}"),
    ("not-taking-water", "Higaki: the ship is not taking water.", f"A hull stamp NOT TAKING WATER, nameplate HIGAKI. {STYLE}"),
    ("alp-guard", "28 March: Alp Guard, 285 tonnes bollard pull, almost doubled the tow.", f"A tug ALP GUARD, tag 285 T PULL. {STYLE}"),
    ("stern-0430", "29 March, ~4:30 local: stern came free.", f"A clock 0430, stern sliding off sand. {STYLE}"),
    ("carlo-magno", "Carlo Magno joined, about 153 tonnes of pull.", f"A second tug CARLO MAGNO, 153 T. {STYLE}"),
    ("king-tide", "Towing timed to a supermoon king tide.", f"A moon and a high-water mark KING TIDE. {STYLE}"),
    ("1505-free", "Boskalis: 15:05 local, pulled free.", f"A clock 1505, ship floating, stamp FREE. {STYLE}"),
    ("bitter-lake", "Towed to the Great Bitter Lake. Canal reopened 19:00.", f"A lake tag BITTER LAKE, clock 1900 OPEN. {STYLE}"),
    ("x-clowns", "Rehook: red X on clown-college and on blaming the wrong captain.", f"Ink peeling a WRONG CAPTAIN sticker, mouth closed. {STYLE}"),
    ("400-waiting", "More than 400 ships waiting. Backlog cleared 3 April.", f"A queue of candy ships, tag 400+, date 3 APR. {STYLE}"),
    ("lloyds-number", "Lloyd's: about $400 million an hour, about $9 billion a day. File the range.", f"A ticker 400M / HOUR, 9B / DAY. {STYLE}"),
    ("egypt-fees", "Rabie: Egypt lost about $12 to $15 million a day in fees.", f"A fee card 12-15M / DAY. {STYLE}"),
    ("ismailia", "13 April: Ismailia court seized the ship. Claim over $916 million.", f"A court stamp SEIZED 13 APR, 916M. {STYLE}"),
    ("reputation", "$300 million salvage bonus and $300 million loss of reputation, UK P&I filed.", f"Two invoice lines SALVAGE 300M, REPUTATION 300M. {STYLE}"),
    ("crew-wait", "25 Indian crew stayed. Some left as contracts expired. Not a hostage cartoon.", f"A crew count 25, a small DEPARTURE ticket. No cruelty. {STYLE}"),
    ("general-average", "Shoei Kisen declared general average. Cargo owners could be asked to chip in.", f"A split bill GENERAL AVERAGE. {STYLE}"),
    ("540-plus-tug", "Settlement around $540 million, plus a 75-ton tug for the Authority.", f"A receipt 540M + 75 T TUG. {STYLE}"),
    ("july-7", "Released 7 July. Sailed 12 July, more than 100 days after the bank.", f"A calendar JUL 7 / JUL 12, tag 100+ DAYS. {STYLE}"),
    ("rotterdam", "Then Rotterdam, Felixstowe, then out of service for repairs.", f"Two port tags ROTTERDAM FELIXSTOWE, stamp REPAIRS. {STYLE}"),
    ("rumour-x", "Marwa Elselehdar was on Aida IV in Alexandria. File the rumour.", f"A rumour stamp WRONG SHIP, red X. No portrait. {STYLE}"),
    ("who-won-bank", "The bank won six days. The excavator won a meme.", f"A sand bank trophy SIX DAYS vs a tiny digger MEME. {STYLE}"),
    ("we-pulled", "Boskalis: we pulled it off.", f"A quote card WE PULLED IT OFF. {STYLE}"),
    ("ask-the-tide", "Ask whether the tide did the last metre.", f"A question mark over a tide gauge. {STYLE}"),
    ("wait-or-unload", "Would you have waited for the king tide, or started unloading 18,000 boxes.", f"Split: a moon vs a crane over boxes, a question mark. {STYLE}"),
    ("121-honest", "A viral digger is a terrible whole story. 121 metres is a terrible honest one.", f"A viral phone vs a 121 M ruler. {STYLE}"),
    ("convoy-question", "Ask how many were already in the convoy.", f"A convoy count 5TH OF MANY. {STYLE}"),
    ("receipt", "The fairway was 121 metres. Drawn anyway.", f"A receipt card 121 M vs 400 M, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Ship That Parked in the Canal",
        description=(
            "Twenty twenty one. A four-hundred-metre stick, a one-hundred-twenty-one-metre "
            "fairway, and a parking ticket that outlived the meme digger."
        ),
        tags=(
            "history",
            "2021",
            "ever given",
            "suez",
            "shipping",
            "cartoon",
            "true story",
            "logistics",
            "canal",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="SIX DAYS PARKED",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Ship That Parked in the Canal",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-evergiven.json"
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

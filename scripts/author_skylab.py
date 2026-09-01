"""Author Drawn Anyway episode 25: Skylab reentry, nineteen seventy nine."""

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
    """The Shire of Esperance fined NASA four hundred dollars for littering after a space station came down on Western Australia. That is not a metaphor, and it is not a cartoon you invented after a trivia night about America dropping a lab on a beach. On the eleventh of July nineteen seventy nine, at sixteen thirty seven Coordinated Universal Time, Skylab began reentry on its thirty four thousand nine hundred eighty first orbit. In Esperance it was already the twelfth, just after midnight. NASA had aimed the leftover metal at the Indian Ocean. Most of it did go there. Some of it did not. Keep that split. Then put a red X on the joke that this is a disaster movie. The leftover is not a fireball over a city. The leftover is a souvenir ticket.""",
    """Start with why a shuttle was supposed to be the save. Skylab was America's first station, launched the fourteenth of May nineteen seventy three on the last Saturn Five from Pad Thirty Nine A. The complex was four pieces: an Orbital Workshop converted from a Saturn upper stage, an airlock, a multiple docking adapter, and an Apollo Telescope Mount with solar arrays. About sixty three seconds up, the micrometeoroid shield, which was also the thermal blanket, tore. One solar wing ripped off. Debris jammed the other. NASA files the on-orbit mass around one hundred seventy thousand pounds, by far the heaviest spacecraft to that date. Wikipedia files about one hundred sixty eight thousand seven hundred fifty, roughly seventy seven tons. File the range. It arrived underpowered and cooking. Mission managers slipped the first crew ten days while engineers invented a save. Skylab-2 put up a sunshade and later freed the stuck panel. Humans on board, NASA later said, were the reason unplanned repairs and extra science happened at all, including new solar flares and a comet in the inner system. Three crews, nine people, stayed twenty eight, fifty nine, and eighty four days. Two hundred seventy experiments. More than one hundred seventy thousand solar images. Forty six thousand Earth photographs. Before leaving on the eighth of February nineteen seventy four, Skylab-4 boosted the empty station to about two hundred sixty nine by two hundred eighty three miles, hoping it would last until nineteen eighty three. By then a Shuttle was supposed to attach a rocket, raise it, or drop it neatly in the Pacific. The Shuttle ran late. The Sun ran hot. Extra solar activity thickened the upper air. Drag ate the orbit. The official idea was: the next vehicle will catch it.""",
    """File the 1979 plan, because a tumble is not a steering wheel. NASA could not park a seventy seven ton workshop on a dime. Flight controllers at Johnson Space Center changed the station's attitude to change the drag, the only leftover lever they had. On the eleventh of July they sent the last command: turn off the control moment gyros, put it in a slow tumble, keep the footprint off a populated band such as North America. They expected breakup over the southern tip of Africa, then the Indian Ocean. Robert Gray at the State Department later said the aim was the South Atlantic or the Indian Ocean. Wikipedia files NASA's odds of any person being hit at about one in one hundred fifty two. Multiply by four billion people and you get a specific-person leftover around one in six hundred billion in the same write-up, and a city of a hundred thousand or more at about one in seven. Special teams waited in case a country asked for help. Newspapers sold mock Skylab insurance. A Nebraska neighborhood painted a target so the station would have something to aim for. T-shirts. Hats. Nightly news. Nightly bets. That is merchandising wearing an orbit. Controllers were not throwing darts at a globe. They were shrinking a footprint with a gyro switch.""",
    """Here is the leftover the movies file as a crash. The breakup ran late. Most surviving pieces still hit water. Some crossed sparsely populated southern Western Australia, a swath from Esperance toward Balladonia and Rawlinna. Locals later told the ABC of a fiery apparition and window-rattling sonic booms in the early hours. NASA first announced it had fallen harmlessly into the Indian Ocean, about two thirty eight in the morning Australian Eastern time in one ABC file, before the land reports stacked up. No one was hurt. File that as the whole injury count. Do not draw it as a town on fire. Flight Director Charles S. Harlan told a news conference: the surprise is over, no more suspense, Skylab is on the planet Earth. A NASA party arrived to check pieces. A makeshift bench with a Geiger counter. Contestants from the Miss Universe pageant in Perth that year flew out to hunt. A large piece later sat on the pageant stage on the twentieth of July. Analysis said the station came apart about ten miles up, lower than the model.""",
    """The San Francisco Examiner offered ten thousand dollars for the first chunk delivered to its office. The Chronicle offered insurance if a subscriber took damage. Stan Thornton, seventeen, in Esperance, found about twenty four pieces at his home, insulation in the usual description. He got a passport, flew to San Francisco, waited a week for Marshall Space Flight Center to say the wreckage was genuine, and collected the Examiner money plus another thousand from a Philadelphia businessman who had flown his family. That is a bag of station as a contest prize. Souvenir hunters were in the desert in under a day. Even pageant contestants flew from Perth. Geoff and Pauline Grewar later found an oxygen tank in nineteen ninety three; the Esperance museum still holds tanks, a nitrogen tank, and scraps. The backup workshop sits at the Smithsonian. The trainer sits at Space Center Houston. NASA's 2019 history still points visitors there. The leftover of a space station is sometimes a glass case, and sometimes a teenager's luggage, and sometimes a litter ticket nobody paid until a radio morning show did it as a gag.""",
    """Rehook, because the internet likes a disaster and a plot. Put a red X on both. A later story claimed Skylab was steered at Pine Gap so secret gear could be recovered. Diplomatic cables called that an obvious untruth and said answering it would be counterproductive. File the rumor. Do not spend it as a mission. The official leftover was an ocean. The street leftover was Australia. The joke leftover was a ticket. Around the nineteenth of July, Esperance Shire presented NASA's team a four hundred dollar littering citation, the same local rule as dumped household waste, meant as a tongue-in-cheek gift they hoped might land in the museum. NASA did not pay. In two thousand nine, Scott Barley of Highway Radio in Barstow, California, crowdfunded the outstanding penalty from morning listeners and handed the shire a novelty cheque. Thirty years of an unpaid joke. A ticket is a costume for a footprint that overshot a model.""",
    """File what the Sun actually did, because July was not a villain in a cape. Skylab was never designed for a crewed, steered landing. Empty tanks, tired gyros, no Shuttle tug. Higher solar activity meant more upper-atmosphere drag, the same physics that makes satellites fall faster in a busy solar cycle. Controllers did the only honest thing left: pick a tumble and a band of ocean, then live with the error bars. International media treated the weeks before as a sweepstakes. Some people were cautious. Some painted bullseyes. Some sold shirts. Esperance later remembered a tourism bump more than a scare. Balladonia, population nine in one later ABC file, found itself on the map when pieces came down near a hotel. That is not the same as saying a seventy seven ton object is a party trick. It is saying the leftover, on the ground, was scraps and a fine, not a body count. NASA's own later history still files the majority in the Indian Ocean and the Australian pieces as the sparse-country remainder. Do not spend sonic booms as an attack. Do not spend a museum oxygen tank as a crater. The backup Orbital Workshop you can still walk around in Washington is the station that did not have to fall.""",
    """None of this is a hymn to a perfect splashdown, and none of it is a cartoon of NASA as clowns who missed a continent on purpose. They had a last Saturn Five. They had a torn blanket at sixty three seconds. They had a Shuttle that was not ready in eighty three. You are allowed to laugh at a four hundred dollar litter ticket on a superpower, and at a Nebraska target painted on a lawn, and at a pageant displaying a piece of workshop. You are not required to laugh at nine people who lived in a converted rocket stage, or at a sunshade that saved the program, or at controllers sending a last gyro command because that was the lever they had. The official idea was: the ocean will take it. The street idea was: they dropped a station on Australia. The leftover idea is: they told it to fall somewhere, and a shire billed them for the somewhere.""",
    """So who won. Not the 1983 rescue that never launched. Not the Pine Gap plot. Harlan won a sentence about suspense being over. Esperance won a museum and a joke invoice. Thornton won ten thousand dollars and a week in a lab queue. Barley's listeners won a thirty-year punchline. The Indian Ocean won most of the mass. Western Australia won the pieces that made the news. If you need a moral, skip space is doomed. Take this: a tumble is a terrible whole story, and a litter ticket is a terrible honest one. The next time someone tells you NASA dumped a station on a town, ask how much landed in water, and whether the fine was a gift for a glass case. Would you have paid the four hundred, or kept the target on the lawn. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no cruelty, no disaster porn, not mud-green archive night, "
    "not After Hours File dark. Skylab shown as a candy workshop, a paper ticket, a map pin, "
    "cartoon metal scraps not burning towns, not people on fire, not craters. Recurring mascot Ink "
    "may cameo: mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("litter-ticket", "Esperance fined NASA $400 for littering after Skylab came down.", f"A candy citation 400 DOLLARS LITTERING, nameplate NASA, tag ESPERANCE. Cream paper. {STYLE}"),
    ("not-trivia", "Not a disaster-movie trivia gag.", f"Ink shaking his head at a DISASTER MOVIE stamp with a red X, mouth closed. {STYLE}"),
    ("july-11", "11 July 1979, 16:37 UTC, orbit 34,981. In Esperance it was already the 12th.", f"A clock 1637 UTC, date 11 JUL 1979, small tag 12 JUL LOCAL. {STYLE}"),
    ("aimed-ocean", "NASA aimed the leftover metal at the Indian Ocean. Most of it did go there.", f"A map arrow to INDIAN OCEAN, stamp MOSTLY WATER. No flags. {STYLE}"),
    ("some-did-not", "Some of it did not.", f"A few candy metal scraps on a cream coastline, tag SOME DID NOT. Not fire. {STYLE}"),
    ("x-disaster", "Put a red X on the disaster-movie joke.", f"A movie clapboard SKYLAB CRASH with a giant red X. {STYLE}"),
    ("leftover-ticket", "Leftover: a souvenir ticket, not a fireball over a city.", f"A souvenir ticket vs a tiny crossed-out fireball icon. Cute not grim. {STYLE}"),
    ("may-14", "Launched 14 May 1973, last Saturn V, Pad 39A.", f"A rocket tag LAST SATURN V, date 14 MAY 1973, pad 39A. {STYLE}"),
    ("sixty-three-sec", "About 63 seconds up: micrometeoroid shield tore. One solar wing gone.", f"A torn blanket tag 63 SEC, one solar wing missing. Not gore. {STYLE}"),
    ("mass-range", "On-orbit mass: about 170,000 lb NASA, about 168,750 Wikipedia. Roughly 77 tons.", f"A scale 170000 LB / 77 TONS, FILE THE RANGE. {STYLE}"),
    ("sunshade", "Skylab-2: sunshade, then freed the stuck panel. First crew slipped 10 days.", f"A candy sunshade on a workshop, tag SKYLAB-2 SAVED. {STYLE}"),
    ("three-crews", "Three crews, nine people: 28, 59, and 84 days.", f"Three duration badges 28 / 59 / 84 DAYS. {STYLE}"),
    ("experiments", "270 experiments. 170,000+ solar images. 46,000 Earth photos.", f"A tally 270 EXPERIMENTS, 170K SUN SHOTS. {STYLE}"),
    ("feb-8-boost", "8 Feb 1974: Skylab-4 boosted to about 269 by 283 miles, hoping for 1983.", f"An orbit card 269x283 MI, tag HOPE 1983. {STYLE}"),
    ("shuttle-late", "Shuttle was supposed to attach a rocket. The Shuttle ran late. The Sun ran hot.", f"A calendar SHUTTLE LATE, a sun with extra DRAG arrows. {STYLE}"),
    ("official-catch", "Official idea: the next vehicle will catch it.", f"A catcher's mitt labeled NEXT VEHICLE, empty. {STYLE}"),
    ("only-lever", "Controllers changed attitude to change drag. The only leftover lever.", f"A lever ATTITUDE = DRAG, Johnson tag. {STYLE}"),
    ("gyros-off", "Last command: turn off control moment gyros, slow tumble, miss North America.", f"A switch GYROS OFF, tumble arrows, stamp MISS CITIES. {STYLE}"),
    ("africa-plan", "Expected breakup over southern Africa, then the Indian Ocean.", f"A dashed path AFRICA TIP to OCEAN. No flags as joke. {STYLE}"),
    ("odds-152", "Odds any person hit: about 1 in 152. A city of 100,000+: about 1 in 7.", f"Two odds cards 1 IN 152 PERSON, 1 IN 7 CITY. {STYLE}"),
    ("nebraska-target", "A Nebraska neighborhood painted a target so it would have something to aim for.", f"A lawn with a painted bullseye, tag NEBRASKA. Cute. {STYLE}"),
    ("shirts-hats", "T-shirts, hats, mock insurance, nightly news. Merchandising wearing an orbit.", f"A T-shirt SKYLAB, a fake insurance slip. {STYLE}"),
    ("breakup-late", "The breakup ran late. Most surviving pieces still hit water.", f"A late clock, most scraps in a blue ocean shape. {STYLE}"),
    ("esperance-swath", "A swath from Esperance toward Balladonia and Rawlinna. Sparse country.", f"A map pin ESPERANCE, tags BALLADONIA RAWLUNNA. No flags. {STYLE}"),
    ("booms-not-fire", "Sonic booms, a fiery apparition in later memory. Not a town on fire. No one hurt.", f"A boom-lines icon, stamp NO ONE HURT. Not disaster. {STYLE}"),
    ("nasa-first-call", "NASA first said Indian Ocean, then land reports stacked up.", f"A press card INDIAN OCEAN, a second stamp ALSO LAND. {STYLE}"),
    ("harlan-quote", "Harlan: The surprise is over. No more suspense. Skylab is on the planet Earth.", f"A quote card ON THE PLANET EARTH, nameplate HARLAN. No portrait. {STYLE}"),
    ("geiger-bench", "A makeshift bench, Geiger counter, pieces checked. Not a war zone.", f"A table, Geiger, candy scraps, tag CHECKED. {STYLE}"),
    ("pageant-piece", "Miss Universe in Perth that year. A large piece on stage 20 July.", f"A stage 20 JUL, a candy workshop fragment on a stand. {STYLE}"),
    ("ten-miles", "Came apart about 10 miles up, lower than the model.", f"An altitude ruler 10 MI, tag LOWER THAN MODEL. {STYLE}"),
    ("examiner-10k", "San Francisco Examiner: $10,000 for the first chunk at the office.", f"A prize banner 10000 FIRST CHUNK, EXAMINER. {STYLE}"),
    ("thornton-24", "Stan Thornton, 17, Esperance: about 24 pieces at home, then a passport.", f"A bag 24 PIECES, tag THORNTON 17, a tiny passport. No photoreal. {STYLE}"),
    ("marshall-wait", "Waited a week for Marshall to authenticate, then the prize plus $1,000 extra.", f"A lab stamp GENUINE, prize 10K + 1K. {STYLE}"),
    ("grewar-tank", "Grewar oxygen tank, 1993. Esperance museum still holds tanks and scraps.", f"A museum case OXYGEN TANK 1993, ESPERANCE. {STYLE}"),
    ("smithsonian", "Backup workshop at the Smithsonian. Trainer at Space Center Houston.", f"Two building tags SMITHSONIAN and HOUSTON TRAINER. {STYLE}"),
    ("x-plot", "Rehook: red X on disaster porn and on a Pine Gap plot.", f"Ink peeling a PINE GAP PLOT sticker, mouth closed. {STYLE}"),
    ("cables-untruth", "Cables: obvious untruth. Answering would be counterproductive. File the rumor.", f"A cable stamp OBVIOUS UNTRUTH, FILE THE RUMOR. {STYLE}"),
    ("july-19-fine", "Around 19 July: Esperance Shire, $400 littering, tongue-in-cheek.", f"A calendar 19 JUL, ticket 400, stamp JOKE GIFT. {STYLE}"),
    ("unpaid-30", "NASA did not pay. 2009: Scott Barley, Highway Radio, listeners, novelty cheque.", f"A novelty cheque 2009, nameplate BARLEY, 30 YEARS. {STYLE}"),
    ("never-landing", "Never designed for a crewed, steered landing. Empty tanks, tired gyros.", f"A workshop with EMPTY TANKS, TIRED GYROS tags. {STYLE}"),
    ("solar-drag", "Hotter Sun, thicker upper air, more drag. Same physics as a busy solar cycle.", f"A sun and atmosphere layer, arrows DRAG. {STYLE}"),
    ("error-bars", "Pick a tumble and a band of ocean, then live with the error bars.", f"A path with wide ERROR BARS over an ocean band. {STYLE}"),
    ("tourism-bump", "Esperance later remembered a tourism bump more than a scare.", f"A postcard ESPERANCE, stamp TOURISM BUMP. {STYLE}"),
    ("not-body-count", "Leftover on the ground: scraps and a fine, not a body count.", f"Scraps plus a ticket, a red X on a body-count ledger. Not gore. {STYLE}"),
    ("converted-stage", "Nine people lived in a converted rocket stage. A sunshade saved the program.", f"A candy workshop interior, sunshade, 9 CREW. {STYLE}"),
    ("last-lever", "A last gyro command because that was the lever they had.", f"A single lever LAST COMMAND. {STYLE}"),
    ("ocean-vs-shire", "Official: the ocean. Street: Australia. Leftover: a shire billed the somewhere.", f"Three cards OCEAN / LAND / TICKET. {STYLE}"),
    ("who-won-water", "The Indian Ocean won most of the mass. WA won the pieces that made the news.", f"A split pie MOSTLY WATER vs NEWS PIECES. {STYLE}"),
    ("museum-or-lawn", "A museum glass case versus a lawn target.", f"A glass case vs a painted lawn bullseye. {STYLE}"),
    ("how-much-water", "Ask how much landed in water, and whether the fine was a gift for a glass case.", f"A question mark over water and a museum ticket. {STYLE}"),
    ("pay-or-target", "Would you have paid the four hundred, or kept the target on the lawn.", f"Split: a 400 ticket vs a lawn target, a question mark. {STYLE}"),
    ("harlan-won", "Harlan won a sentence about suspense being over.", f"A receipt line SUSPENSE OVER. {STYLE}"),
    ("thornton-won", "Thornton won ten thousand dollars and a week in a lab queue.", f"A prize cup 10K, a waiting-room ticket MARSHALL. {STYLE}"),
    ("receipt", "They told it to fall somewhere. Drawn anyway.", f"A receipt card TUMBLE vs TICKET, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Station They Told to Fall Somewhere",
        description=(
            "Nineteen seventy nine. A seventy-seven-ton workshop, an ocean aim, "
            "and a four-hundred-dollar litter ticket."
        ),
        tags=(
            "history",
            "1979",
            "skylab",
            "nasa",
            "esperance",
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
        thumbnail_hook="THEY FINED NASA",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Station They Told to Fall Somewhere",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-skylab.json"
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

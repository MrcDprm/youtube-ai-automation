"""Author Drawn Anyway episode 14: Boston Molasses Flood, nineteen nineteen."""

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
    """A tank of molasses once outran a neighbourhood at lunch. That is not a metaphor, and it is not a cartoon you invented after a trivia night about sticky streets. On Wednesday the fifteenth of January nineteen nineteen, in Boston's North End, a steel tank at five hundred twenty nine Commercial Street, opposite Copp's Hill, near Keany Square, let go at about twelve thirty in the afternoon. Purity Distilling ran the site. United States Industrial Alcohol owned the company. The tank stood about fifty feet high and ninety feet across, and that day it held on the order of two point three million gallons. Witnesses heard a roar like the Elevated, then a bang, then rivets popping like a machine gun. A brown wave ran into the blocks. Twenty one people were killed. About one hundred fifty were hurt. Keep that picture. Then put a red X on the joke line. The leftover is not that molasses is funny. The leftover is that the tank had been leaking, and the company's answer was brown paint.""",
    """Start with why a waterfront needed a silo of syrup. Molasses ferments into ethanol. In those years that ethanol was liquor and, in wartime, a piece of munitions chemistry. The Commercial Street tank sat beside Boston Harbor so ships could offload, then a pipeline could send the stuff to Purity's plant in East Cambridge, between Willow Street and Evereteze Way. Arthur P. Jell, the treasurer, oversaw the build. He was not an architect and not an engineer. Hugh Nawn Construction poured a thick concrete pad. Hammond Iron Works raised the steel. The first Cuban steamer was due with hundreds of thousands of gallons, and the clock on the pier was louder than the spec sheet. The contract talked about a water test, filling the tank to see if it held. They put in about six inches of water. Jell later said a full fill would have taken days they did not have, on a small water connection, with a ship already on the calendar. That is a tank approved by a puddle. It is not a tank approved by a load.""",
    """The leak was a report. Neighbours said the seams wept almost from the first fill in nineteen fifteen. People collected the seepage in pails. The tank groaned when it was filled. Isaac Gonzales, a company man on the site, later told of running back in the night because he dreamed it would come down. File him as a named witness with a bad feeling, not as a ghost story. When locals could see molasses on the steel, Jell had the tank painted brown, the colour of the leak, so the leak would look like the tank. That is logistics wearing a costume. The official plan was still going to work: hold more than two million gallons until Cambridge needed a transfer, keep the waterfront moving, keep the treasurer's calendar. The tank was filled to capacity only a handful of times. January was one of the heavy days. A leak is a sentence you can answer with thicker plate, or with a test, or with a smaller fill. Brown paint is a sentence you answer with a brush.""",
    """January. Boston had been bitter. Then the air jumped, in the usual telling, from about two degrees Fahrenheit toward forty one, above forty on the day itself. The day before, a ship had pumped in a fresh load that had been warmed so it would flow. Older molasses in the tank was colder. Warm syrup on cold syrup is a pressure story, and fermentation can add carbon dioxide if the mix is alive. At about twelve thirty the cylinder failed. Molasses is about forty percent denser than water, about twelve pounds to the gallon, so the potential energy is not a kitchen spill. The wave is filed around thirty five miles an hour. Height is an argument: a later park plaque says forty feet; physics writeups often cite about twenty five at the peak; an older Smithsonian piece said fifteen. File the disagreement. Do not pick a cartoon number because it sounds bigger. Steel plates hit the Boston Elevated Railway's Atlantic Avenue girders. A streetcar tipped on the rails. Engine Thirty One's firehouse was shoved. A truck went into the harbor. Several blocks sat two to three feet deep after the first rush.""",
    """Here is the leftover that is not a punchline. Twenty one dead. About one hundred fifty hurt. Most of the named dead were laborers, teamsters, longshoremen, a firefighter, people whose work put them at the paving yard, the wharf, the firehouse. George Layhe of Engine Thirty One is on that list. Two ten-year-olds are on that list. Do not turn those two names into a drawing. Cadets from the training ship U.S.S. Nantucket, one hundred sixteen of them under Lieutenant Commander H. J. Copeland, came off the nearby pier and waded in. Boston police, the Red Cross, Army and Navy followed. Searching went on for days. Some victims were not found in the harbor for months. Cleanup used salt water from a fireboat and sand to drink the syrup. The harbor stayed brown into summer. Rescue, cleanup, and sightseeing tracked molasses onto subway platforms, streetcar seats, telephone handsets, and homes. The line that stuck was: everything a Bostonian touched was sticky. That is a city as a residue, not a joke you get to spend on twenty one names.""",
    """Rehook, because the internet likes a funny flood and a company that said a bomb did it. United States Industrial Alcohol told the court anarchists had dynamited the tank, because some of the alcohol was for munitions, and Boston in those years had real bomb scares to borrow. There was no blast evidence that held. One hundred nineteen plaintiffs sued. It became a landmark Massachusetts class action, years of hearings, engineers and metallurgists in the room. Court-appointed auditor Hugh W. Ogden found the company responsible. USIA paid about six hundred twenty eight thousand dollars. Relatives of the dead were reported around seven thousand each. In two thousand fourteen, engineer Ronald Mayville wrote that the walls were at least fifty percent too thin even for the codes of the day, the steel too brittle, short on manganese, cracks starting at flawed rivet holes. The tank had been a fatigue machine on a cyclic fill. Brown paint does not thicken plate. A bomb story does not thicken plate either.""",
    """There is a later caption that they were racing Prohibition. The Eighteenth Amendment was ratified the next day, the sixteenth of January nineteen nineteen, and would take effect a year after that. Some writers file the full tank as a last pour before the dry law. File the calendar. Do not let a constitutional date steal a tensile test. In two thousand sixteen a Harvard group ran cold syrup through a model North End and said the high speed in the first rush was credible, then the flood cooled and thickened, which is why a non-Newtonian wall can hit like water and then hold like glue. For decades people said the North End still smelled of molasses on hot days. Edwards Park wrote that the smell remained a distinctive atmosphere of Boston. USIA did not rebuild the tank. The pad is under a ballfield at Langone Park. A Bostonian Society plaque at Puopolo Park still names five hundred twenty nine Commercial Street, twenty one dead, and a wave. The plaque's forty feet is a public sentence. The thinner steel is the private one.""",
    """None of this is a hymn to a sticky joke, and none of it is a cartoon of the North End as a punchline neighbourhood that should have known better than to live next to a leak. They had a treasurer on a steamer deadline. They had six inches of water where a fill test was written. They had seams you could taste with a pail. They had a paint job that made the leak the architecture. The chemistry is thin brittle plate plus a near-full tank plus a warm load on a warm day. The logistics is who you hire when the object is heavier than water and sits beside a school, a firehouse, and an elevated track. You are allowed to laugh at a city that stayed sticky into summer. You are not required to laugh at Engine Thirty One, or at a paving yard, or at two names you will not draw. A leak is a report. Brown paint is a costume. Six inches of water is a costume for a test. The official idea was: this will hold, and then Cambridge will take a pipe.""",
    """So who won. Not the tank. Not the anarchist caption. Not the brown brush. Ogden won a finding. The plaintiffs won a number that does not buy twenty one people back. Mayville won a thickness that should have been on the drawing in nineteen fifteen. The park won a plaque and a diamond over a slab. Building rules after this started insisting that a licensed architect and a civil engineer look at a tank before a neighbourhood has to. If you need a moral, skip never store molasses. Take this: paint is a terrible instrument for a leak, and a leak is a terrible neighbour for two point three million gallons. The next time someone tells you Boston flooded with molasses, ask whether they mean the wave or the brush, and whether the water test was six inches or a tank. Would you have painted it brown, or would you have filled it with water first. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no drowning, no child-victim closeups, no dead horses, no blood. "
    "Disaster shown as a leaking brown tank, a paint brush, a syrup wave hitting buildings and tracks, "
    "court papers, a park plaque, not violence and not trapped people. "
    "Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("painted-brown", "They painted the leaking tank brown.", f"Cartoon title beat: a huge steel tank painted molasses-brown, a paintbrush, cream paper. Hook energy. No people trapped. {STYLE}"),
    ("not-trivia", "Not a sticky-street trivia gag.", f"Ink shaking his head at a TRIVIA FLOOD stamp with a red X, mouth closed. {STYLE}"),
    ("north-end-1919", "15 January 1919, Boston North End.", f"A simple map NORTH END BOSTON, calendar 15 JAN 1919, no flags. {STYLE}"),
    ("commercial-529", "529 Commercial Street, opposite Copp's Hill.", f"A street sign 529 COMMERCIAL, COPP'S HILL across the road. {STYLE}"),
    ("purity-usia", "Purity Distilling. United States Industrial Alcohol.", f"Two company nameplates PURITY and USIA, no portraits. {STYLE}"),
    ("fifty-by-ninety", "About 50 feet high, 90 feet across.", f"A tank diagram 50 FT by 90 FT, cream paper, no people. {STYLE}"),
    ("two-point-three", "On the order of 2.3 million gallons that day.", f"A giant gallon tally 2.3 MILLION, a tiny ship icon. {STYLE}"),
    ("twelve-thirty", "About 12:30 in the afternoon.", f"A round clock 12:30, lunch-hour stamp. {STYLE}"),
    ("rivets", "Rivet pops like a machine gun. File as cartoon bangs, not gore.", f"Cartoon rivets flying off a tank as dots, BANG stamps, no bodies. {STYLE}"),
    ("twenty-one", "21 killed, about 150 hurt. Not a giggle.", f"A somber tally 21 and 150, respectful, no bodies, no children drawn. {STYLE}"),
    ("ethanol-munitions", "Molasses to ethanol: liquor and wartime chemistry.", f"A pipe diagram MOLASSES to ETHANOL, two tags LIQUOR and MUNITIONS as text. {STYLE}"),
    ("cambridge-pipe", "Harbor tank, pipeline to East Cambridge.", f"A simple map HARBOR tank dotted pipe to CAMBRIDGE. No flags. {STYLE}"),
    ("arthur-jell", "Arthur P. Jell, treasurer, oversaw the build.", f"A nameplate ARTHUR P. JELL, TREASURER tag, no portrait. {STYLE}"),
    ("no-engineer", "Not an architect. Not an engineer.", f"A job plaque NO ENGINEER with a red X on a diploma. {STYLE}"),
    ("hammond-nawn", "Hugh Nawn poured the pad. Hammond Iron Works raised the steel.", f"Two contractor cards NAWN PAD and HAMMOND STEEL. {STYLE}"),
    ("six-inches", "The water test was about six inches.", f"A huge tank with a tiny 6 IN puddle labeled TEST. {STYLE}"),
    ("first-leak-1915", "Seams wept from the first fill, 1915.", f"A tank dated 1915 with cartoon drips, LEAK stamp. {STYLE}"),
    ("pails-seepage", "Neighbours collected seepage in pails.", f"Empty pails under dripping seams, no child faces. {STYLE}"),
    ("groaning", "The tank groaned when filled.", f"A tank with comic GROAN sound lines, no gore. {STYLE}"),
    ("brown-paint", "Jell had it painted brown so the leak looked like the tank.", f"A giant paintbrush painting a tank BROWN, leak disappearing into the color. {STYLE}"),
    ("gonzales", "Isaac Gonzales, company man, feared it would come down.", f"A nameplate ISAAC GONZALES, a small NIGHT CHECK tag, no portrait, not a ghost. {STYLE}"),
    ("official-plan", "Official plan: hold millions until Cambridge needed a pipe.", f"A clipboard PLAN: HOLD THEN PIPE, a check mark. {STYLE}"),
    ("two-to-forty-one", "Air from about 2 F toward 41 F.", f"A thermometer jumping 2 to 41, January calendar. {STYLE}"),
    ("warm-load", "The day before: a warmed fresh load pumped in.", f"A ship pumping WARM molasses into a COLD tank, two colors. {STYLE}"),
    ("fermentation", "Warm on cold, and fermentation can add pressure.", f"A tank with tiny CO2 bubbles labeled PRESSURE, not an explosion gore. {STYLE}"),
    ("density", "About 40 percent denser than water. 12 pounds a gallon.", f"A scale WATER vs MOLASSES, molasses side heavier. {STYLE}"),
    ("thirty-five", "Wave filed around 35 miles an hour.", f"A speed badge 35 MPH on a brown cartoon syrup arrow, hitting a building not a person. {STYLE}"),
    ("height-disagreement", "Height is an argument: plaque 40 ft, papers often 25, one piece 15.", f"Three rulers 15 25 40 labeled ARGUMENT, a question mark. {STYLE}"),
    ("el-tracks", "Steel plates hit the Elevated girders. A streetcar tipped.", f"Bent cartoon EL tracks, a streetcar tilted, no people falling. {STYLE}"),
    ("engine-31", "Engine 31 firehouse was shoved.", f"A firehouse labeled ENGINE 31 shifted off a square foundation, no trapped firefighters drawn. {STYLE}"),
    ("truck-harbor", "A truck went into the harbor.", f"A tiny truck icon in cartoon water, HARBOUR stamp, not drowning gore. {STYLE}"),
    ("two-three-feet", "Blocks sat 2 to 3 feet deep after the first rush.", f"A street with a 2-3 FT depth mark, empty of people. {STYLE}"),
    ("cadets-nantucket", "116 cadets from USS Nantucket, Copeland.", f"A ship nameplate USS NANTUCKET, tally 116 CADETS, distant silhouettes not faces in syrup. {STYLE}"),
    ("cleanup-salt", "Fireboat salt water and sand. Harbor brown into summer.", f"A fireboat spraying, a sand pile, a brown harbor until SUMMER. {STYLE}"),
    ("sticky-city", "Molasses tracked onto trains, phones, homes.", f"Sticky subway seat, sticky phone, STICKY CITY stamp, comic not cruel. {STYLE}"),
    ("anarchist-claim", "USIA said anarchists bombed it. No blast evidence that held.", f"A BOMB stamp with a giant red X, court papers. {STYLE}"),
    ("one-nineteen", "119 plaintiffs. A Massachusetts class action.", f"A filing stack 119 PLAINTIFFS, CLASS ACTION stamp. {STYLE}"),
    ("ogden", "Auditor Hugh W. Ogden found the company responsible.", f"A nameplate HUGH W. OGDEN, AUDITOR, LIABLE stamp, no portrait. {STYLE}"),
    ("six-twenty-eight", "USIA paid about $628,000. About $7,000 per victim reported.", f"A check 628000, a smaller tag 7000, not a joke. {STYLE}"),
    ("half-too-thin", "Mayville 2014: walls at least 50 percent too thin.", f"A tank wall cross-section 50 PERCENT TOO THIN, year 2014. {STYLE}"),
    ("manganese", "Steel too brittle, short on manganese, cracks at rivet holes.", f"A rivet hole with a cartoon CRACK line, BRITTLE tag. {STYLE}"),
    ("prohibition-next-day", "18th Amendment ratified the next day. File the calendar, not the cause.", f"A calendar 16 JAN next to the tank, NOT CAUSE stamp. {STYLE}"),
    ("harvard-2016", "Harvard 2016: first rush speed credible, then it thickened.", f"A lab model NORTH END, year 2016, FAST then THICK arrows. {STYLE}"),
    ("non-newtonian", "Hits like water, then holds like glue.", f"Two stamps HIT LIKE WATER and THEN GLUE, a syrup arrow slowing. {STYLE}"),
    ("smell-decades", "For decades, hot days still smelled of molasses.", f"A summer sun over the North End, SMELL stamp, no people suffering. {STYLE}"),
    ("puopolo-plaque", "Puopolo Park plaque: 529 Commercial, 21 dead.", f"A park plaque BOSTON MOLASSES FLOOD, 529 COMMERCIAL, no gore photos. {STYLE}"),
    ("langone-slab", "The pad sits under a ballfield at Langone Park.", f"A baseball diamond with a dotted tank circle under the grass. {STYLE}"),
    ("paint-not-steel", "Brown paint does not thicken plate.", f"A brush vs a steel plate, the plate winning THICKNESS. {STYLE}"),
    ("not-a-joke-neighbourhood", "Not a cartoon of the North End as a punchline.", f"Ink peeling a JOKE sticker off a NORTH END sign, mouth closed. {STYLE}"),
    ("who-won", "Not the tank. Not the brush. Ogden. The plaque. The codes.", f"A gavel, a plaque, and a CODE book beating a tiny paintbrush. {STYLE}"),
    ("licensed-look", "After: licensed architect and civil engineer on a tank.", f"Two stamps ARCHITECT and CIVIL ENGINEER on a tank blueprint. {STYLE}"),
    ("water-or-paint", "Six inches of water, or a brush.", f"Split: 6 IN TEST vs BROWN BRUSH, a red X on the brush as a fix. {STYLE}"),
    ("comment-hook", "Would you have painted it brown. Tell me in the comments.", f"Ink pointing at the viewer, mouth closed, a tiny brown tank and a tiny water bucket. {STYLE}"),
    ("receipt", "A leak is a report. Paint is a costume. Drawn anyway.", f"A receipt card LEAK vs PAINT, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Flood That Was Molasses",
        description=(
            "Boston North End, January nineteen nineteen. A leaking tank, brown paint, "
            "and two point three million gallons."
        ),
        tags=(
            "history",
            "boston molasses flood",
            "1919",
            "north end",
            "cartoon",
            "true story",
            "purity distilling",
            "funny",
            "disaster",
            "logistics",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="THEY PAINTED IT BROWN",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Flood That Was Molasses",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-molasses.json"
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

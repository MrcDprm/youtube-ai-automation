"""Author Drawn Anyway episode 15: Dagen H, Sweden, nineteen sixty seven."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 600.0
MINUTES = 9
VOICE = "en-GB-ThomasNeural"
RATE = "+2%"

CHAPTERS = [
    """A whole country once stopped the cars at four fifty in the morning and walked them to the other kerb. That is not a metaphor, and it is not a cartoon you invented after a trivia night about driving on the left. On Sunday the third of September nineteen sixty seven, Sweden switched from left-hand traffic to right-hand traffic. The day is Dagen H. The H is Högertrafik, right-hand traffic, not a secret agency and not a national flag you salute. At about five in the morning, after a radio countdown, traffic that had been allowed on the road was told it could move again, on the other side. Olof Palme, then minister of communications, later prime minister, went on air and called it a very large change in daily existence. Keep that picture. Then put a red X on the crash-reel joke. The leftover is not that Swedes forgot which way was home. The leftover is that eighty three percent had already voted no, and the state still wrapped the traffic lights in black plastic until the minute it counted.""",
    """Start with why a no vote did not keep the left. In October nineteen fifty five, in a referendum, about eighty three percent said keep left, about fifteen and a half said switch, a sliver left the ballot blank, on a turnout around fifty three percent. The Riksdag still approved Prime Minister Tage Erlander's proposal on the tenth of May nineteen sixty three: right-hand traffic in nineteen sixty seven. The arguments on the table were not a vibe. Norway and Finland, the land borders, already drove on the right, with on the order of five million vehicles a year crossing. More than ninety percent of Swedes already sat in left-hand-drive cars, which is a bad match for overtaking on a narrow two-lane when the steering wheel is on the kerb side of the oncoming lane. City buses were among the few that still had the wheel on the right, doors to the left, because that is how you load a kerb when you drive on the left. Cars on Swedish roads had tripled, five hundred thousand to about one point five million, and were talked of heading toward two point eight million by nineteen seventy five. The official idea was: this will match the neighbours, and then the overtaking view will match the wheel.""",
    """The commission was Statens högertrafikkommission, HTK. The named chief was Lars Skiöld, the man the papers nicknamed the right-hand general, which is a job title you file as logistics, not as a war. Psychologists got a four-year education programme. The H logo went on billboards, buses, milk cartons, and, because this is Sweden in the sixties, underwear, gloves, mugs, ties, a board game, a stamp. Swedish television ran a song contest. The winner was Håll dig till höger, Svensson, Keep to the right, Svensson, written by Expressen journalist Peter Himmelstrand, sung by The Telstars. That is a chorus hired as a road sign you can hum. Yellow centre lines were due to become white. Crews painted a parallel set, then hid them under black tape. Extra poles and signals went up at intersections, wrapped in black plastic, so the morning of H could be a reveal, not a debate. About three hundred fifty thousand signs had to come down or go up, on the order of twenty thousand in Stockholm alone. Headlamps that kicked the wrong way got an opaque decal: not to be removed before the third of September nineteen sixty seven.""",
    """Buses were the expensive sentence. More than a thousand new ones were bought with doors on the right. Some eight thousand older buses were rebuilt with doors on both sides, because you cannot move a kerb overnight and leave the door hanging over the centre line. Gothenburg and Malmö exported left-traffic buses to Pakistan and Kenya, which is a leftover you can put on a shipping tag: the old door still had a country that wanted it. Trams in central Stockholm, in Helsingborg, and most lines in Malmö were pulled and replaced by buses. Norrköping and Gothenburg kept trams, plus a few suburban Stockholm lines. The Stockholm metro, and the railways, stayed on the left. File that. A country can change a kerb and leave a tunnel. Stockholm and Malmö got a longer ban, from ten on Saturday to three on Sunday, so crews could rebuild junctions. Other towns sat still from three Saturday to three Sunday. Nationwide, non-essential traffic was banned from one in the morning to six. The official plan was still going to work: stop, step across, wait, then five o'clock.""",
    """Sunday. From one o'clock the ordinary cars were supposed to be off the road. At four fifty, whatever was still legal on the asphalt had to stop completely, then creep to the right-hand side, then stop again so nobody met a neighbour still finishing the walk. At five, after the countdown on Högertrafikvaka, the right-hand-traffic vigil on Swedish Melody Radio, with C-G Hammarlund, Skiöld, and Palme in the booth, the country was told it had right-hand driving. Palme said he dared say no country had invested so much personal labour, and money, to get uniform international traffic rules. Time magazine later called it a brief but monumental traffic jam. Do not draw a pile-up. On the day, one hundred fifty seven minor accidents were reported, thirty two with personal injuries, a low number serious. The Monday after, one hundred twenty five reported accidents, against a usual Monday band of about one hundred thirty to one hundred ninety eight, none fatal. Motor insurance claims were later filed as down about forty percent. Caution is a speed limit you cannot paint on a sign. It is also not a permanent miracle.""",
    """Rehook, because the internet likes a nation that woke up on the wrong side and crashed for sport. That is not the receipt. The early dip in deaths and claims did not last as a new physics. Claims were talked of returning toward normal over about six weeks. By nineteen sixty nine, accident rates were back near the old line, while car ownership kept rising. Experts had said the right-hand change should help overtaking because the wheel was already on the left of the car. They also said perceived risk jumped higher than the real risk, so people drove as if the road were new, which it was. That is logistics wearing a nervous face. Iceland did the same trick on the twenty sixth of May nineteen sixty eight, H-dagurinn. The Swedish bill, in the BBC's later sum, was about six hundred twenty eight million kronor, about five percent over a budget from two years earlier. The information campaign alone sat around forty three million. Underwear is cheaper than a bus door. A bus door is cheaper than a junction you rebuild twice.""",
    """There is a later caption that the people were overruled, full stop. File the referendum. File the parliament. They are not the same vote. The fifty five no was real. The sixty three yes in the Riksdag was also real. What the commission actually bought was not a conversion of hearts. It bought tape on the new white line, plastic on the new signal, a decal on the lamp, a glove that said right, a song you could not get out of your head, and a four fifty stop that assumed strangers would wait for strangers. Sveriges Radio later notes Sweden had already driven on the right between seventeen eighteen and seventeen thirty four, which is a leftover older than the H logo: the kerb had been argued before the car. You are allowed to laugh at milk cartons with an H. You are not required to laugh at thirty two injuries, or to pretend a plastic bag on a traffic light is a personality test. The 83 percent is a poll. The 4:50 is a procedure.""",
    """None of this is a hymn to Palme, and none of it is a cartoon of Sweden as a nation too obedient to miss a kerb. They had neighbours already on the right. They had cars whose steering wheels were already on the left. They had buses whose doors were not. They had yellow paint due to become white. They had a metro that would keep left in a tunnel while the street above learned a new habit. The chemistry is LHD cars plus right-hand neighbours plus a parliament that would not wait for a second referendum. The logistics is who wraps the light, who peels the tape, who moves the bus stop to the other kerb, who stands still at four fifty so the person still crossing does not become a headline. A crash montage is a terrible instrument for a morning that filed one hundred fifty seven minor accidents. A song is a terrible instrument for a door that has to move. The door still had to move.""",
    """So who won. Not the referendum. Not the underwear. Not the joke that they forgot left from right. HTK won a Sunday that started. Palme won a radio line about labour and money. Skiöld won a nickname. The Telstars won a chorus. The metro won the left-hand tunnel. Kenya and Pakistan won some buses. The headlamp decal won a date printed on the glass. If you need a moral, skip never vote no. Take this: a poll is a terrible instrument for a kerb, and a kerb is a terrible neighbour for a bus door you have not rebuilt. The next time someone tells you Sweden switched sides overnight, ask who was still at four fifty, and whose traffic light was still in a bag. Would you have voted no, and still stopped when the radio said stop. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no crash montage, no wrecked cars as the joke, no blood, no corpses. "
    "The switch shown as clocks, LEFT/RIGHT arrows, black plastic on signals, tape on road lines, "
    "bus doors, an H campaign logo, a radio, not violence. "
    "Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("stop-four-fifty", "Stop at 4:50, then walk to the other kerb.", f"Cartoon title beat: a huge clock 4:50, two arrows LEFT to RIGHT, cream paper. No crash. {STYLE}"),
    ("not-trivia", "Not a forgot-which-side trivia gag.", f"Ink shaking his head at a TRIVIA CRASH stamp with a red X, mouth closed. {STYLE}"),
    ("sunday-1967", "Sunday 3 September 1967, Sweden.", f"A calendar 3 SEP 1967, a simple map SWEDEN, no flag. {STYLE}"),
    ("dagen-h-name", "The day is Dagen H.", f"A big letter H on a cream poster, DAGEN H. No national flag. {STYLE}"),
    ("hogertrafik", "H is Högertrafik, right-hand traffic.", f"A glossary card H = RIGHT-HAND TRAFFIC, an arrow pointing right. {STYLE}"),
    ("left-to-right", "Left-hand traffic became right-hand traffic.", f"A road split LEFT crossed out, RIGHT circled, no flags. {STYLE}"),
    ("palme-radio", "Olof Palme, communications minister, on the radio.", f"A nameplate OLOF PALME, RADIO mic, no portrait. {STYLE}"),
    ("eighty-three", "1955 referendum: about 83 percent said keep left.", f"A ballot tally 83 PERCENT NO, year 1955. {STYLE}"),
    ("neighbours-right", "Norway and Finland already drove on the right.", f"A simple border map NORWAY FINLAND arrows RIGHT, no flags. {STYLE}"),
    ("five-million-cross", "On the order of 5 million vehicles a year crossing.", f"A border gate tally 5 MILLION, tiny car dots. {STYLE}"),
    ("lhd-cars", "More than 90 percent sat in left-hand-drive cars.", f"A car with the wheel on the LEFT, 90 PERCENT tag. {STYLE}"),
    ("buses-wrong-door", "City buses still had the wheel on the right, doors to the left.", f"A bus with doors on the LEFT, KERB tag. {STYLE}"),
    ("cars-tripled", "Cars: 500,000 to about 1.5 million, talk of 2.8 million by 1975.", f"Three piles of tiny cars 0.5M 1.5M 2.8M. {STYLE}"),
    ("erlander-1963", "Riksdag, 10 May 1963: Erlander's proposal, switch in 1967.", f"A parliament stamp 10 MAY 1963, Tage Erlander nameplate, no portrait. {STYLE}"),
    ("htk-skiold", "HTK. Lars Skiöld, the named chief.", f"Two plates HTK and LARS SKIOLD, no portrait. {STYLE}"),
    ("four-year-school", "A four-year education programme, on psychologists' advice.", f"A school primer 4 YEARS, an H logo on the cover. {STYLE}"),
    ("milk-underwear", "H logo on milk cartons and underwear.", f"A milk carton and folded underwear both stamped H, comic not crude. {STYLE}"),
    ("telstars-song", "Winning song: Keep to the right, Svensson. The Telstars.", f"A tiny record KEEP TO THE RIGHT SVENSSON, TELSTARS. {STYLE}"),
    ("yellow-to-white", "Yellow centre lines due to become white.", f"A road with YELLOW line vs WHITE line, before/after. {STYLE}"),
    ("black-tape", "New white lines painted, then hidden under black tape.", f"A road with black tape over a white line, PULL AT DAWN tag. {STYLE}"),
    ("plastic-signals", "New signals wrapped in black plastic until the morning.", f"Traffic lights in black plastic bags, READY stamp. {STYLE}"),
    ("three-fifty-k", "About 350,000 signs to remove or replace.", f"A mountain of signs 350000, a tiny Stockholm tag 20000. {STYLE}"),
    ("headlamp-decal", "Headlamp decal: not to be removed before 3 September 1967.", f"A round headlamp with a sticker DO NOT REMOVE BEFORE 3 SEP. {STYLE}"),
    ("reminder-gloves", "Reminder gloves: drive on the right.", f"A pair of cartoon gloves labeled RIGHT, no gore. {STYLE}"),
    ("thousand-new-buses", "More than 1,000 new buses, doors on the right.", f"A new bus with RIGHT DOORS, tally 1000+. {STYLE}"),
    ("eight-thousand-retrofit", "About 8,000 older buses rebuilt with doors on both sides.", f"A bus with doors BOTH SIDES, tally 8000. {STYLE}"),
    ("export-kenya", "Gothenburg and Malmö exported left-traffic buses to Pakistan and Kenya.", f"A shipping crate BUSES, tags PAKISTAN and KENYA, no flags. {STYLE}"),
    ("trams-out", "Trams out in central Stockholm, Helsingborg, most of Malmö.", f"A tram with a WITHDRAWN stamp, a bus waiting. {STYLE}"),
    ("metro-stayed-left", "Stockholm metro and railways stayed on the left.", f"A tunnel METRO LEFT, a street above marked RIGHT. {STYLE}"),
    ("long-ban-cities", "Stockholm and Malmö: Saturday 10:00 to Sunday 15:00.", f"A longer clock SAT 10 to SUN 15, two city nameplates. {STYLE}"),
    ("one-to-six", "Nationwide: non-essential traffic banned 01:00 to 06:00.", f"A NO CARS stamp, clocks 1:00 and 6:00. {STYLE}"),
    ("four-fifty-stop", "4:50: stop completely.", f"A huge STOP at a clock 4:50, empty road, no crash. {STYLE}"),
    ("creep-right", "Then creep to the right-hand side, then stop again.", f"Cars as simple arrows sliding LEFT to RIGHT, then a WAIT stamp. {STYLE}"),
    ("five-o-clock", "5:00: right-hand driving.", f"A clock 5:00, a stamp SWEDEN NOW RIGHT, no flag. {STYLE}"),
    ("radio-vigil", "Högertrafikvaka on Melody Radio. Hammarlund, Skiöld, Palme.", f"A radio set HOGERTRAFIKVAKA, three name tags, no portraits. {STYLE}"),
    ("palme-labour", "Palme: never before so much labour and money for uniform rules.", f"A radio quote card LABOUR AND MONEY, PALME, no portrait. {STYLE}"),
    ("time-jam", "Time magazine: a brief but monumental traffic jam.", f"A magazine cover BRIEF JAM, cartoon cars in a polite queue, no wrecks. {STYLE}"),
    ("one-fifty-seven", "157 minor accidents that day. 32 with injuries. Not a giggle.", f"A somber tally 157 and 32, no wrecked cars, no blood. {STYLE}"),
    ("monday-numbers", "Monday after: 125 accidents vs a usual 130 to 198. None fatal.", f"A Monday chart 125 vs 130-198, NONE FATAL stamp. {STYLE}"),
    ("forty-percent", "Motor insurance claims down about 40 percent, then not forever.", f"A claims arrow down 40 PERCENT, a later arrow returning. {STYLE}"),
    ("six-weeks", "Toward normal in about six weeks. By 1969, old rates again.", f"A calendar 6 WEEKS then 1969 BACK, not a crash reel. {STYLE}"),
    ("iceland-1968", "Iceland, 26 May 1968, H-dagurinn.", f"A calendar 26 MAY 1968, H-DAGURINN, map ICELAND, no flag. {STYLE}"),
    ("cost-kronor", "About 628 million kronor. About 5 percent over budget.", f"A ledger 628 MILLION KR, 5 PERCENT OVER. {STYLE}"),
    ("info-forty-three", "Information campaign around 43 million kronor.", f"A stack of leaflets 43 MILLION, H logo, milk carton. {STYLE}"),
    ("poll-not-procedure", "The 83 percent is a poll. The 4:50 is a procedure.", f"A ballot vs a clock 4:50, arrow pointing at the clock. {STYLE}"),
    ("seventeen-eighteen", "Sweden had already driven on the right, 1718 to 1734.", f"An old calendar 1718-1734 RIGHT, a tiny horse cart, no flag. {STYLE}"),
    ("not-crash-joke", "A crash montage is a terrible instrument for that morning.", f"Ink peeling a CRASH REEL sticker off a clock, mouth closed. {STYLE}"),
    ("door-had-to-move", "A song is a terrible instrument for a door that has to move.", f"A record vs a bus door, the door winning MOVE. {STYLE}"),
    ("who-won", "Not the referendum. HTK. The metro left. Kenya's buses.", f"A commission stamp, a metro tunnel, a shipping crate beating a ballot. {STYLE}"),
    ("decal-date", "The headlamp decal won a date printed on the glass.", f"Close cartoon of the decal date 3 SEP 1967. {STYLE}"),
    ("kerb-vs-poll", "A poll is a terrible instrument for a kerb.", f"A kerb stone vs a ballot, the kerb labeled LOGISTICS. {STYLE}"),
    ("whose-bag", "Whose traffic light was still in a bag.", f"A traffic light half out of a black plastic bag. {STYLE}"),
    ("comment-hook", "Would you have voted no, and still stopped. Tell me in the comments.", f"Ink pointing at the viewer, mouth closed, a tiny clock 4:50. {STYLE}"),
    ("receipt", "Stop, step across, wait. Drawn anyway.", f"A receipt card 4:50 STOP then 5:00 RIGHT, Ink with marker, mouth closed. {STYLE}"),
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
        title="The Morning Sweden Drove on the Other Side",
        description=(
            "Dagen H, Sunday the third of September nineteen sixty seven. "
            "Four fifty, a plastic bag on the lights, and a kerb that moved."
        ),
        tags=(
            "history",
            "dagen h",
            "sweden",
            "1967",
            "traffic",
            "cartoon",
            "true story",
            "logistics",
            "funny",
            "right hand traffic",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="STOP AT FOUR FIFTY",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Morning Sweden Drove on the Other Side",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-dagenh.json"
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

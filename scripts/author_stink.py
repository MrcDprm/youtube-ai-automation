"""Author Drawn Anyway episode 10: Great Stink, London, eighteen fifty eight."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 600.0
MINUTES = 9
VOICE = "en-AU-WilliamNeural"
RATE = "+4%"

CHAPTERS = [
    """A river once passed a law by sitting under a window. That is not a metaphor, and it is not a cartoon you invented after a heatwave. In June, July and August eighteen fifty eight, in central London, the Thames cooked. Shade temperatures sat around thirty four to thirty six Celsius, forty eight in the sun on the worst days. A high around thirty five is recorded for the sixteenth of June. The river dropped. Sewage that used to hide under water sat on the foreshore and baked. The press named it the Great Stink. Queen Victoria and Prince Albert tried a pleasure cruise and came back in minutes. Members of Parliament, in a nearly new Palace of Westminster built on the bank, soaked the river-side curtains in chloride of lime and still could not work. Keep that picture. A government that already had a sewer plan in a drawer. A chancellor calling the Thames a Stygian pool. A bill that became law in eighteen days. Everything after this is just that picture hiring an engineer who had been waiting.""",
    """Start with why a capital treats a river as a drain. By eighteen fifty eight London had gone from under a million people to about three. Flush toilets and iron pipes put more water into an old map of about two hundred thousand cesspits and three hundred sixty sewers, many of them tired brick. Factories, slaughterhouses, tanneries, all of it found the Thames. In July eighteen fifty five Michael Faraday wrote to The Times: he dropped white paper in to test opacity and found the river a real sewer, even near the bridges. In eighteen fifty seven the government was already pouring chalk lime, chloride of lime and carbolic acid into the water, which is not a cure, it is perfume for a symptom. The official idea was miasma: disease rides on bad air. Three cholera outbreaks had already been blamed on the smell, six thousand five hundred thirty six dead in eighteen thirty one, fourteen thousand one hundred thirty seven in forty eight to forty nine, ten thousand seven hundred thirty eight in fifty three to fifty four. John Snow had already taken the Broad Street pump handle in Soho in eighteen fifty four and argued water, not air. In June eighteen fifty eight, as the stink peaked, Snow died. The file kept the miasma caption.""",
    """The plan in the drawer belonged to Joseph Bazalgette. Assistant surveyor to the Metropolitan Commission of Sewers from eighteen forty nine, chief engineer after Frank Foster died in fifty two, then chief engineer of the Metropolitan Board of Works when the Metropolis Management Act of eighteen fifty five replaced the commission. By June eighteen fifty six he had the definitive scheme: local pipes into bigger pipes into eleven-foot mains, north and south outfalls, high, mid and low levels, pumping to the east, sized for four and a half million people, not three. Sir Benjamin Hall, First Commissioner of Works, did not like the outfalls still inside the capital. Consultants in fifty seven wanted discharge fifteen miles further on, over five point four million pounds. Bazalgette's ceiling was about two point four. In February eighteen fifty eight Palmerston fell, Derby came in, Lord John Manners took Hall's job, Benjamin Disraeli became chancellor. The maps did not change. The river did.""",
    """June is when the river walked into the House. Curtains on the water side were soaked in lime chloride. It failed. There was talk of moving sittings to Oxford or St Albans, which is a sentence about an expensive new palace that could not be inhabited. The Examiner had Disraeli leaving a committee room with papers in one hand and a handkerchief on his nose. On the eleventh of June, Hansard, MP John Brady asked Manners what he had done about the library and the committee rooms. Manners said the Thames was not under his jurisdiction. Four days later another member asked if the government would remedy turning a noble river into a cesspool. Manners said the government had nothing whatever to do with the state of the Thames. Punch called it the Conspiracy to Poison, Father Thames in the dock. At the height, two hundred to two hundred fifty long tons of lime a week went on sewer mouths and the foreshore, about fifteen hundred pounds a week for a smell you could still not legislate in. The official idea was still: not our river.""",
    """Then the smell sat on the Treasury bench. On the fifteenth of June Disraeli tabled the Metropolis Local Management Amendment Bill and opened by calling the Thames a Stygian pool, reeking with ineffable and intolerable horrors. The bill put cleanup on the Metropolitan Board of Works, said sewer outlets should not, as far as possible, sit inside London, and let the Board borrow three million pounds, repaid by a three-penny levy on households for forty years. That is Bazalgette's eighteen fifty six plan with Hall's objection sat on. The Times said Parliament was all but compelled to legislate by the force of sheer stench. Debated in late July, law on the second of August, about eighteen days from a serious start to a statute. The Illustrated London News had already written the hypocrisy receipt: we can colonise the remotest ends of the earth, we can conquer India, we can pay the interest on an enormous debt, but we cannot clean the River Thames. Do not cheer the empire line. File it as a newspaper noticing the mismatch.""",
    """Here is the leftover fact, and it is not that lime curtains work. Bazalgette already had the drawing. Hall had already delayed it on outfalls. The heat did not invent civil engineering. The heat invented a majority. Work started at the beginning of eighteen fifty nine. Four hundred draftsmen on the first phase. Portland cement tested batch by batch because Bazalgette did not trust a hot kiln. The southern outfall, easier, smaller population, opened at Crossness in April eighteen sixty five by the Prince of Wales, four beam engines named like a family album, dinner for five hundred in a pumping station. The north was the crowded side, two thirds of London, a Fleet sewer collapse into Victoria Street in June eighteen sixty two when rain and a railway cutting disagreed. Victoria, Chelsea and Albert Embankments put the pipes in the river wall and stole about fifty two acres back from the water. Bazalgette was knighted after Chelsea opened. The system ran in eighteen seventy five. About three hundred eighteen million bricks, eight hundred eighty thousand cubic yards of concrete and mortar, a final bill near six and a half million.""",
    """Rehook, because the internet likes a smell joke that skips the water. Miasma funded the sewers. Water was what the sewers actually moved. In eighteen sixty six cholera came back, five thousand five hundred ninety six dead, ninety three percent in an East End pocket between Aldgate and Bow that was not yet on Bazalgette's map, and the East London Water Company was putting sewage half a mile below a reservoir that the tide could walk into. After that, the Lancet backed William Farr: the water supply did it. Last outbreak in the capital. Faraday's paper test was three years early. Snow was already in the ground. The river did not become a moral. It became a gradient of two feet per mile and a pumping station that still looks like it wanted to be a church. Abbey Mills, Crossness, listed later, still in the file.""",
    """None of this is a cartoon of MPs as cowards, or of Londoners as a punchline about toilets. They had a unitary sewer board that was new, a chief engineer with a map, a First Commissioner who wanted the outfall further, and a House built on the bank in a summer that would not rain. The chemistry is heat plus low water plus effluent on mud. The logistics is who sits next to the window. When the window was a newspaper, Faraday got a letter. When the window was the library of the Lords, described as a stench trap, Disraeli got a bill. You are allowed to laugh at lime on curtains. You are not required to laugh at cholera tables, or to pretend the eighteen-day statute was a miracle instead of a plan that had been waiting for a nose in the right room.""",
    """So who won. Not the handkerchief. Not Manners saying it was not his river. Not miasma, though miasma signed the cheque. Faraday won a paper boat. Snow won the caption later. Hall won a delay that the heat undid. Disraeli won a sentence about a Stygian pool. Bazalgette won the bricks, the embankment, and a monument that says he placed chains upon the river. The Thames won the only vote that counted: it sat under Parliament until Parliament funded the pipe. If you need a moral, skip never invent plumbing. Take this: a curtain is a terrible instrument for a sewer, and a sewer is a terrible neighbour for a new palace. The next time someone tells you the Great Stink, ask whose plan was already dated June eighteen fifty six, and whose window finally agreed. Would you have moved the House to Oxford. A hot June, lime curtains, eighteen days, three million borrowed. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags, "
    "no photoreal faces, no corpses, no cholera victims, no graphic sewage, no drowning. "
    "Smell shown as comic green-brown puff clouds, not filth closeups. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("window-law", "A river passed a law by sitting under a window.", f"Cartoon title beat: a river puff under a palace window, a bill flying out. Cream paper. Comic smell cloud, not gore. {STYLE}"),
    ("not-heatwave-gag", "Not a metaphor. Not a heatwave gag.", f"Ink shaking his head at a HEATWAVE JOKE stamp with a red X, mouth closed. {STYLE}"),
    ("june-1858", "June to August 1858, central London, the Thames cooked.", f"Calendar JUN-AUG 1858, a thermometer, a cartoon river. No flags. {STYLE}"),
    ("thirty-six", "Shade about 34-36 C, 48 in the sun. June 16 near 35 C.", f"Two thermometers 36 C and 48 C, date June 16. {STYLE}"),
    ("foreshore-bake", "The river dropped. Sewage baked on the foreshore.", f"A low cartoon river, mud banks, comic stink puffs, not graphic. {STYLE}"),
    ("named-stink", "The press named it the Great Stink.", f"A newspaper headline GREAT STINK, cream paper. {STYLE}"),
    ("victoria-cruise", "Victoria and Albert tried a cruise and came back in minutes.", f"A tiny royal boat turning around, clock a few MIN, no portraits. {STYLE}"),
    ("lime-curtains", "Parliament soaked river-side curtains in chloride of lime.", f"Giant curtains dripping LIME, a palace window, comic puffs still getting in. {STYLE}"),
    ("plan-in-drawer", "A sewer plan already sat in a drawer.", f"A DRAWER labeled 1856 PLAN, slightly dusty. {STYLE}"),
    ("stygian-pool", "A chancellor called the Thames a Stygian pool.", f"A speech bubble STYGIAN POOL over a brown cartoon river. Not gore. {STYLE}"),
    ("eighteen-days", "A bill became law in 18 days.", f"A stopwatch 18 DAYS from bill to LAW stamp. {STYLE}"),
    ("three-million-people", "London had grown from under 1 million to about 3.", f"A population arrow 1M to 3M, rooftops. {STYLE}"),
    ("cesspits-sewers", "About 200,000 cesspits and 360 tired sewers.", f"Two tallies 200000 and 360, brick pipes cartoon. {STYLE}"),
    ("faraday-paper", "July 1855: Faraday dropped white paper to test opacity.", f"White paper squares sinking into opaque cartoon water. {STYLE}"),
    ("real-sewer", "He called the whole river a real sewer.", f"A river labeled REAL SEWER, Faraday notebook, no portrait. {STYLE}"),
    ("1857-perfume", "1857: lime and carbolic poured in. Perfume for a symptom.", f"Bottles LIME and CARBOLIC over a river, PERFUME stamp. {STYLE}"),
    ("miasma", "Official idea: disease rides on bad air. Miasma.", f"A MIASMA cloud with a question mark, not a corpse. {STYLE}"),
    ("cholera-tables", "Three outbreaks already blamed on the smell.", f"Three somber clipboards 6536, 14137, 10738. Respectful, no victims shown. {STYLE}"),
    ("broad-street", "Snow took the Broad Street pump handle, 1854. He argued water.", f"A pump with the handle off, WATER not AIR. {STYLE}"),
    ("snow-dies", "June 1858: John Snow died as the stink peaked.", f"A calendar June 1858, a closed WATER paper, respectful. {STYLE}"),
    ("bazalgette-drawer", "The plan belonged to Joseph Bazalgette.", f"An engineer hat and a huge sewer map, no photoreal face. {STYLE}"),
    ("foster-then-mbw", "After Foster died, then MBW in 1855, he kept refining.", f"A job ladder MCS to MBW, 1855 Act book. {STYLE}"),
    ("june-1856-plan", "June 1856: local pipes to 11-ft mains, outfalls east.", f"A nested-pipe diagram 3 FT to 11 FT, arrow EAST. {STYLE}"),
    ("four-point-five", "Sized for 4.5 million, not 3.", f"A capacity tag 4.5M over a 3M city. {STYLE}"),
    ("hall-outfalls", "Benjamin Hall disliked outfalls still inside the capital.", f"A map with INSIDE circled, Hall's NO stamp, no portrait. {STYLE}"),
    ("five-point-four", "Consultants wanted 15 more miles, over 5.4 million pounds.", f"Two price tags 2.4M vs 5.4M, a 15 MI ruler. {STYLE}"),
    ("derby-disraeli", "Feb 1858: Derby in, Manners, Disraeli chancellor.", f"Three hat-pegs DERBY MANNERS DISRAELI, no portraits. {STYLE}"),
    ("maps-same", "The maps did not change. The river did.", f"An unchanged blueprint next to a hotter river puff. {STYLE}"),
    ("not-his-river", "Manners: the Thames is not under my jurisdiction.", f"A minister pointing at a NOT MINE sign on the river. {STYLE}"),
    ("oxford-talk", "Talk of moving the House to Oxford or St Albans.", f"A palace on wheels toward OXFORD, silly not cruel. {STYLE}"),
    ("handkerchief", "Disraeli: papers in one hand, handkerchief on the nose.", f"A cartoon handkerchief vs a stack of bills, no portrait. {STYLE}"),
    ("hansard", "Brady in Hansard: we cannot use the library.", f"A library door with a STENCH TRAP tag. {STYLE}"),
    ("lime-tons", "200-250 long tons of lime a week, about 1,500 pounds.", f"Lime sacks and a weekly bill 1500. {STYLE}"),
    ("june-fifteenth", "June 15: Disraeli tables the amendment bill.", f"Calendar June 15 1858, a bill on a bench. {STYLE}"),
    ("three-million-borrow", "MBW may borrow 3 million, 3-penny levy for 40 years.", f"A loan paper 3M, coin 3d, 40 YR. {STYLE}"),
    ("times-stench", "The Times: compelled by the force of sheer stench.", f"A newspaper pulling a gavel with a smell cloud. {STYLE}"),
    ("august-second", "Law on August 2. About 18 days.", f"Calendar Aug 2 1858, LAW stamp. {STYLE}"),
    ("iln-mismatch", "Illustrated London News: we cannot clean the Thames.", f"A quote card CANNOT CLEAN, not an empire poster, no flags. {STYLE}"),
    ("heat-majority", "The heat did not invent engineering. It invented a majority.", f"A vote tally appearing as a thermometer rises. {STYLE}"),
    ("four-hundred-draftsmen", "1859: 400 draftsmen on the first phase.", f"A room of tiny drafting tables, 400. {STYLE}"),
    ("portland-cement", "Portland cement tested batch by batch.", f"Cement bags under a TEST stamp, kiln with a thermometer. {STYLE}"),
    ("crossness-1865", "Crossness opened April 1865, Prince of Wales, dinner for 500.", f"A fancy pumping station, 500 dinner plates, 1865. No flags. {STYLE}"),
    ("fleet-collapse", "June 1862: Fleet sewer and a railway cutting disagreed.", f"Two trenches, a comic splash onto a street labeled VICTORIA ST. Not disaster-porn. {STYLE}"),
    ("embankments", "Victoria, Chelsea, Albert: pipes in the wall, 52 acres back.", f"Three embankment labels, 52 ACRES arrow from river. {STYLE}"),
    ("six-five", "1875: operational. 318 million bricks, about 6.5 million pounds.", f"A brick pile 318M and a bill 6.5M. {STYLE}"),
    ("miasma-cheque", "Miasma funded the sewers. Water was what they moved.", f"A cheque signed MIASMA, pipes labeled WATER. {STYLE}"),
    ("east-end-1866", "1866 cholera: 5596 dead, 93 percent off the new map.", f"A map with a pocket not connected, somber 93%, no victims. {STYLE}"),
    ("farr-lancet", "Farr and the Lancet: the water supply did it.", f"A Lancet-ish paper WATER SUPPLY, last outbreak stamp. {STYLE}"),
    ("two-feet-mile", "A gradient of 2 feet per mile, a station that wanted to be a church.", f"A slope 2 FT/MI into an ornate pump house. {STYLE}"),
    ("not-cowards", "Not a cartoon of MPs as cowards. The window was the plot.", f"Ink peeling a COWARD sticker off a window, mouth closed. {STYLE}"),
    ("who-sits", "Logistics: who sits next to the window.", f"A window seat labeled DECIDES, a far seat labeled LATER. {STYLE}"),
    ("curtain-terrible", "A curtain is a terrible instrument for a sewer.", f"Lime curtains losing to a river puff. {STYLE}"),
    ("whose-plan", "Ask whose plan was dated June 1856, whose window agreed.", f"A 1856 blueprint vs a 1858 window. {STYLE}"),
    ("comment-hook", "Would you have moved the House to Oxford. Tell me in the comments.", f"Ink pointing at the viewer, mouth closed, a tiny palace on wheels. {STYLE}"),
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
        title="The Summer London Could Not Smell Itself",
        description=(
            "London, eighteen fifty eight. Lime curtains, a Stygian pool, "
            "and a sewer plan that had been waiting for a window."
        ),
        tags=(
            "history",
            "great stink",
            "thames",
            "cartoon",
            "true story",
            "1858",
            "bazalgette",
            "london",
            "funny",
            "sewers",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="THE RIVER WON",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Summer London Could Not Smell Itself",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-stink.json"
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

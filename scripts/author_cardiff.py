"""Author Drawn Anyway episode 7: Cardiff Giant, New York, eighteen sixty nine."""

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
    """New York once dug up a giant behind a barn, and then sold tickets. That is not a metaphor, and it is not a cartoon you invented after Sunday school. On Saturday the sixteenth of October eighteen sixty nine, in Cardiff, a hamlet in the town of LaFayette, about twelve miles south of Syracuse, William Stub Newell hired two men, Gideon Emmons and Henry Nichols, to dig a well behind the barn. Their shovels hit a stone foot. In minutes they had a recumbent figure ten feet four and a half inches long, about two thousand nine hundred ninety pounds of what looked like a petrified man. One of the diggers is supposed to have said some old Indian had been buried there. Treat that as a line people like to tell. Newell put up a tent. The first day was free. Then it was fifty cents for fifteen minutes, three to five hundred visitors a day, and the valley became Giantville. Keep that picture. A well that was not really a well. A cousin with a cigar business in Binghamton. A block of Iowa gypsum. Everything after this is just that picture hiring a box office.""",
    """Start with why anyone would bury a statue on purpose. George Hull, a Binghamton tobacconist, a skeptic, and a man already half in love with Darwin, lost an argument at a Methodist revival with a preacher named Reverend Turk about Genesis six four: there were giants in the earth in those days. Hull did not want the verse as a fossil. He wanted it as a joke that could also print money. The idea of a petrified man was already in the papers. In eighteen fifty eight a California sheet had run a fake letter about a prospector turned to stone inside a geode. Hull made it a work order. In eighteen sixty eight he and a man named H. B. Martin had a gypsum block, ten feet four and a half inches, quarried near Fort Dodge, Iowa, telling workers it was for a Lincoln monument in New York. The stone went to Chicago, to a German cutter, Edward Burkhardt, who hired Henry Salle and Fred Mohrmann. They carved a recumbent man modeled on Hull himself. A geologist had told Hull hair would not petrify, so they left him bald. They hung quilts so the chisels would not advertise, wiped sand into the surface, stained it with sulfuric acid, and beat pores with steel knitting needles set in a board. Cost on the order of twenty six hundred dollars. That is not a miracle. That is a work order with a punchline attached.""",
    """Hull needed dirt that would keep a secret. He cut in his cousin William Stub Newell, farmer, Cardiff. In late November eighteen sixty eight they buried the giant near the barn, wedged under roots so it would look like it had slept through centuries. Hull went home to cigars. Nearly a year later the instruction was: dig the well. On October sixteenth the hired men, not in on the joke, hit the foot. Andrew D. White, later the first president of Cornell, walked the farm and said the well made no sense. It was convenient neither to the house nor to the barn. There was already a spring and a stream. That is the kind of leftover fact a ticket does not print. What we can stand on is the tent, the fifty cents, the crowds so thick that local hotels did four days of business they had never seen. Preachers came to argue it was a witness to Scripture. Showmen came to argue it was a statue, which was closer, and still not the whole receipt. The official idea was a wonder of Onondaga County. The unofficial idea was a ticket.""",
    """Scientists started arriving with unpleasant eyes. John F. Boynton, first geologist on the site, said it could not be a fossilized man. He guessed a statue, maybe a French Jesuit carving from the sixteen hundreds meant to impress local people. Then the age walked back toward a few hundred days. Yale paleontologist Othniel C. Marsh looked at soluble gypsum in wet earth and at fresh tool marks that centuries should have worn off, and called it a most decided humbug. He was surprised any scientific observer had missed it. White noticed grooves that would have taken years if the stone had been local limestone, which it was not. Papers ran gags. One printed a scientific official report that was a blank column. None of that stopped the line. Hull sold his part-interest for twenty three thousand dollars to a syndicate of five men headed by Syracuse horse trader and banker David Hannum. They hauled the giant a dozen miles north to the Bastable in Syracuse. Hannum had a foot twenty one inches long and a crowd that paid. If this already sounds like a bad idea that had already cashed out, you are paying attention.""",
    """Then P. T. Barnum offered fifty thousand dollars to buy the giant. Some later tellings bump that to sixty thousand for a three-month New York lease. Hannum refused. Barnum did not need the original. He had a man take a covert wax impression and made a plaster copy, then told New York that his giant was the real one and Cardiff's was the fake. Ads asked whether it was a statue, a petrifaction, a stupendous fraud, or the remains of a former race. People paid to see the copy, and when the original finally reached the city the copy outsold it. By year's end a half-dozen Cardiff Giants were on the road. David Hannum, watching the wrong crowd spend, is the man quoted as saying there is a sucker born every minute. Later generations pinned the sentence on Barnum, which is its own little hoax. Hannum sued. On the tenth of December eighteen sixty nine Hull confessed to the press. On the second of February eighteen seventy, in New York, Judge George G. Barnard heard both giants called fakes. He told Hannum to bring the giant into court and have it swear it was a bona fide petrifaction if he wanted an injunction. Baring that, he was out of the injunction business. Barnum could not be sued for calling a fake giant a fake. Write that down. That is the adult in the room, and the room still sold tickets.""",
    """Hull later said he had wanted the joke exposed, to show how easily a revival crowd would buy giants in the earth. Believe him as a man who had already banked twenty three thousand. Do not turn it into a morality play about atheists versus Methodists. The leftover fact is not who won Genesis. The leftover fact is gypsum, a tent, and a second giant made of plaster. The Chicago carvers' names got into the papers in early eighteen seventy. The public kept coming anyway and started calling the stone man Old Hoaxey, which is affection for a receipt. Hull even repeated the trick years later with the Solid Muldoon in Colorado, clay and plaster this time, still fifty cents. A file can hold a sermon argument and a box office at the same time. You are allowed to laugh at the sucker line. You are not required to give it to the wrong showman.""",
    """Aftermath is storage, then more tickets. By about eighteen eighty the original was cooling in a Massachusetts barn. It toured the carnival circuit. In nineteen oh one both the Cardiff stone and Barnum's plaster made the Pan-American Exposition in Buffalo. The fair also held a presidential assassination, which is a sentence this giant does not get to steal, and the giant did not steal much attention either. Iowa publisher Gardner Cowles Junior later bought the original as a basement coffee table. In nineteen forty seven he sold it to the Farmers' Museum in Cooperstown, New York State Historical Association, on display by nineteen forty eight. He lies under a shed in a reconstructed village, and you still buy a ticket. Barnum's copy later sat in Fort Dodge, Iowa, where the gypsum block was born, and another copy has been claimed by a Michigan oddities arcade. Two fakes, two museums, one Bible verse, and a well that was a stage direction.""",
    """Rehook, because the internet likes a simple con man. Hull did run a con. Newell did charge. Hannum did buy. Barnum did counterfeit a counterfeit. Marsh did the geology. White did the well that made no sense. None of that makes the giant a victim, or the ticket-buyers a morality exhibit. They paid to see a ten-foot stone man in a hole, then paid to see a plaster man in a museum, then paid again after everyone admitted both were fake. The chemistry is gypsum plus sulfuric acid plus knitting-needle pores plus a year in the ground. The logistics is who owns the silhouette. When Barnum could not buy the asset he cloned it. When Hannum sued, the court noticed you cannot libel a fake by calling it fake. That mismatch is the whole autumn in one sentence.""",
    """So who won. Not the well diggers. Not Reverend Turk's verse. Not Hannum's lawsuit. Hull won a joke that printed money and a confession that still tours. Barnum won the sentence everyone misquotes. Marsh won the word humbug. Barnard won the line about a giant taking an oath. Cooperstown won a shed with a stone man who still requires admission. If you need a moral, skip never trust a farmer. Take this: a ticket is a terrible instrument for settling Genesis, and Genesis is a terrible instrument for pricing gypsum. The next time someone sells you a petrified wonder behind a barn, ask who paid the Chicago chisels, and who owns the plaster twin. Would you have paid the fifty cents. A buried statue, a tent, two fakes, and a sucker line hanging on the wrong coat. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags, "
    "no photoreal faces, no nudity, no anatomical detail. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("giant-open", "New York dug up a giant behind a barn and sold tickets.", f"Cartoon title beat: a huge simple stone man lying behind a tiny barn, ticket booth, cream paper. Modest drape, no nudity. {STYLE}"),
    ("not-sunday-school", "Not a metaphor. Not a Sunday-school cartoon.", f"Ink shaking his head at a SUNDAY SCHOOL stamp over a giant foot, mouth closed. {STYLE}"),
    ("october-sixteenth", "October 16, 1869, Cardiff, south of Syracuse.", f"Cartoon calendar October 16 1869, small valley hamlet, no flags. {STYLE}"),
    ("well-diggers", "Newell hired men to dig a well. They hit a stone foot.", f"Two tiny diggers, a shovel hitting a giant stone foot in a pit. {STYLE}"),
    ("ten-feet", "About ten feet long, roughly 3,000 pounds.", f"A simple recumbent stone figure with 10 FT and 3000 LB labels, modest, no anatomy. {STYLE}"),
    ("tent-fifty-cents", "A tent. First day free, then 50 cents for 15 minutes.", f"A striped tent, price sign 50 CENTS, 15 MIN hourglass. {STYLE}"),
    ("giantville", "The valley became Giantville.", f"A tiny town sign flipped to GIANTVILLE, crowds of simple hats. {STYLE}"),
    ("keep-picture", "A well that was not a well. Iowa gypsum. A Binghamton cigar man.", f"Three icons: fake well, gypsum block, cigar. {STYLE}"),
    ("hull-argument", "George Hull lost an argument about giants in Genesis.", f"A revival tent, a verse card GENESIS, Hull's cigar vs a preacher hat, no portraits. {STYLE}"),
    ("joke-and-money", "He wanted a joke that could also print money.", f"A joke book and a ticket roll taped together. {STYLE}"),
    ("fort-dodge", "1868: a gypsum block quarried near Fort Dodge, Iowa.", f"A quarry, a huge gypsum slab, FORT DODGE label, no flags. {STYLE}"),
    ("lincoln-cover", "He told workers it was a Lincoln monument.", f"A crate stamped LINCOLN MONUMENT with a wink from Ink, mouth closed. {STYLE}"),
    ("chicago-chisels", "Chicago: Burkhardt, Salle, and Mohrmann carved a man.", f"Three tiny sculptors behind quilts, chiseling a modest stone figure. {STYLE}"),
    ("quilts", "They hung quilts so the chisels would not advertise.", f"Quilts draped around a workshop, muffled CHINK marks. {STYLE}"),
    ("acid-pores", "Acid stain and needled pores to look old.", f"A bottle ACID and knitting needles over a stone surface, cartoon not cruel. {STYLE}"),
    ("twenty-six-hundred", "Cost on the order of $2,600.", f"An invoice $2,600, gypsum and chisels as line items. {STYLE}"),
    ("cut-in-newell", "Hull cut in relative Stub Newell, Cardiff farmer.", f"A handshake over a farm, secret envelope, no portraits. {STYLE}"),
    ("november-bury", "November 1868: buried near the barn under roots.", f"Night cartoon: giant lowered into a pit under barn roots. Modest drape. {STYLE}"),
    ("wait-a-year", "Hull went home to cigars. Nearly a year later: dig.", f"A cigar and a calendar skipping from 1868 to 1869. {STYLE}"),
    ("hit-the-foot", "October 16: unsuspecting hired men hit the foot.", f"Shock lines from a shovel on a stone toe, funny not mean. {STYLE}"),
    ("preachers-showmen", "Preachers called it Scripture. Showmen called it a statue.", f"Two signs: SCRIPTURE vs STATUE over the same pit. {STYLE}"),
    ("marsh-humbug", "Othniel C. Marsh: gypsum, fresh tool marks, a decided humbug.", f"A Yale-ish notebook HUMBUG, chisel marks circled on stone. {STYLE}"),
    ("boynton-days", "Boynton walked the age back toward a few hundred days.", f"A timeline from CENTURIES shrinking to DAYS. {STYLE}"),
    ("blank-report", "A paper ran a scientific report that was a blank column.", f"A newspaper with an empty REPORT box, Ink raising an eyebrow. {STYLE}"),
    ("line-kept", "None of that stopped the line.", f"A long ticket line past a HUMBUG sign they ignore. {STYLE}"),
    ("twenty-three-k", "Hull sold his interest for $23,000 to Hannum's syndicate.", f"A bill of sale $23,000, five tiny syndicate hats. {STYLE}"),
    ("syracuse-haul", "They hauled it a dozen miles north to Syracuse.", f"A wagon with a giant crate, 12 MILES arrow. {STYLE}"),
    ("twenty-one-inch", "The foot was 21 inches. The crowd paid.", f"A giant cartoon foot with 21 IN tape, coins in a box. {STYLE}"),
    ("barnum-offer", "Barnum offered $50,000. Hannum refused.", f"Two price tags $50,000 NO and a SHOWMAN hat. {STYLE}"),
    ("wax-copy", "Barnum took a covert wax impression and made plaster.", f"A wax sheet over a silhouette, a plaster twin popping out. Modest, no anatomy. {STYLE}"),
    ("his-is-real", "He told New York his giant was real and Cardiff's was fake.", f"Two banners: MINE REAL and THEIRS FAKE, inverted truth. {STYLE}"),
    ("sucker-line", "Hannum: a sucker born every minute. Later pinned on Barnum.", f"A quote bubble hopping from HANNUM coat to BARNUM coat. {STYLE}"),
    ("december-tenth", "December 10, 1869: Hull confessed to the press.", f"Calendar Dec 10 1869, a CONFESSED stamp on a cigar box. {STYLE}"),
    ("february-court", "February 2, 1870: both fakes. Barnum cannot be sued for that.", f"A gavel, two giant silhouettes marked FAKE, case dismissed. {STYLE}"),
    ("old-hoaxey", "The public kept coming. They called him Old Hoaxey.", f"A fond nickname banner OLD HOAXEY over the stone man. {STYLE}"),
    ("not-genesis-score", "The leftover fact is not who won Genesis.", f"A Bible and a ticket, the ticket circled. {STYLE}"),
    ("massachusetts-barn", "By about 1880: storage in a Massachusetts barn.", f"A dusty barn, giant under a sheet, 1880. {STYLE}"),
    ("buffalo-fair", "1901: Pan-American Exposition, Buffalo, both giants on tour.", f"A fair tent 1901, two giant crates, no assassination scene. {STYLE}"),
    ("cooperstown", "1948: Farmers' Museum, Cooperstown, still a ticket.", f"A museum shed, stone man, TICKETS sign, 1948. {STYLE}"),
    ("fort-dodge-copy", "Barnum's copy later sat in Fort Dodge, where the block was born.", f"Iowa label, plaster twin waving at a quarry. {STYLE}"),
    ("two-museums", "Two fakes, two museums, one verse, a staged well.", f"Two museum tickets and a well icon with a theater mask. {STYLE}"),
    ("counterfeit-squared", "Barnum counterfeited a counterfeit.", f"A copy machine making a giant, FAKE x2. {STYLE}"),
    ("cannot-libel-fake", "You cannot libel a fake by calling it fake.", f"A law book with that sentence, Ink nodding, mouth closed. {STYLE}"),
    ("chemistry", "Gypsum plus acid plus a year in the ground.", f"Three beakers: GYPSUM, ACID, DIRT, equals a ticket. {STYLE}"),
    ("who-owns-negative", "The logistics is who owns the silhouette.", f"A paper outline of a giant, two rival stamps. {STYLE}"),
    ("paid-anyway", "They paid after everyone admitted both were fake.", f"A ticket stub stamped STILL WORTH IT, funny not mean. {STYLE}"),
    ("not-a-victim", "The giant is not a victim. The ticket is the plot.", f"Ink ripping a VICTIM label off the stone man, mouth closed. {STYLE}"),
    ("who-won", "Who won. Not the well. Not the verse. Not the lawsuit.", f"A scoreboard: WELL 0, VERSE 0, LAWSUIT 0, TICKETS 1. {STYLE}"),
    ("wrong-coat", "Barnum won the sentence everyone misquotes.", f"A quote pinned to the wrong coat on a rack. {STYLE}"),
    ("marsh-won-humbug", "Marsh won the word humbug.", f"A dictionary open to HUMBUG, a tiny giant in the margin. {STYLE}"),
    ("shed-admission", "Cooperstown won a shed that still requires admission.", f"A shed and a turnstile, stone man napping. {STYLE}"),
    ("ask-chicago", "Ask who paid the Chicago chisels, and who owns the plaster twin.", f"Two receipts: CHICAGO CHISELS and PLASTER TWIN. {STYLE}"),
    ("fifty-cents-ask", "Would you have paid the fifty cents.", f"A giant 50 CENTS coin hovering over a pit. {STYLE}"),
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
        title="The Giant That Was a Hoax in a Barn",
        description=(
            "Cardiff, New York, eighteen sixty nine. Iowa gypsum, a staged well, "
            "fifty-cent tickets, and a plaster twin that sued its way into a punchline."
        ),
        tags=(
            "history",
            "cardiff giant",
            "hoax",
            "cartoon",
            "true story",
            "1869",
            "barnum",
            "new york",
            "funny",
            "museum",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="HOAX IN A BARN",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Giant That Was a Hoax in a Barn",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-giant.json"
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

"""Author Drawn Anyway episode 28: Liebeck v McDonald's coffee, nineteen ninety two to ninety four."""

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
    """A forty nine cent cup of coffee put a seventy nine year old woman in hospital for eight days. That is not a metaphor, and it is not a cartoon you invented after a trivia night about a clumsy grandma who won millions for being clumsy. On the twenty seventh of February nineteen ninety two, Stella Liebeck ordered coffee at a McDonald's drive-through in Albuquerque, New Mexico. She was in the passenger seat of a nineteen eighty nine Ford Probe that did not have cup holders. Her grandson parked so she could add cream and sugar. She put the cup between her knees and pulled the far side of the lid. The cup tipped. Wikipedia files third-degree burns on six percent of her skin, lesser burns over sixteen, eight days in hospital, skin grafts, two years of treatment. Keep that split: she asked for medical bills, and the company treated it like a joke. Then put a red X on the joke that she was driving and spilled it for fun. The leftover is not cruelty. The leftover is a holding temperature and a lid that was not a warning.""",
    """Start with why a hold temperature was supposed to be the truth. McDonald's required franchisees to keep coffee at one hundred eighty to one hundred ninety degrees Fahrenheit, about eighty two to eighty eight Celsius. Consultants said high brew heat extracts flavour. Drive-through logic said commuters wanted it still hot at the office. McDonald's own research, the trial record later showed, found customers meant to drink it immediately while driving. Home makers sat around one hundred thirty five to one hundred fifty, Albuquerque lawyer Kenneth Wagner later said. Other shops in the city tested at least twenty degrees cooler. Experts told the jury: one hundred ninety degrees can mean a full-thickness burn in about three seconds. One hundred eighty, about twelve to fifteen. One hundred sixty, about twenty seconds, time to wipe it off. The official idea was: hotter is better coffee, and a small reminder on the cup is enough.""",
    """File the ask, because eight hundred dollars is not a medical plan. Liebeck's past bills about ten thousand five hundred. Future care about two thousand five hundred. Her daughter's lost income about five thousand. She sought twenty thousand to cover the stack, about eighteen thousand of it already named. McDonald's offered eight hundred. She had never filed a lawsuit. When they would not move, she hired Houston attorney Reed Morgan, who had already taken a similar hot-coffee case in nineteen eighty six, settled for twenty seven thousand five hundred, and deposed quality man Christopher Appleton, who said he knew the risk and had no plans to turn the heat down. Morgan filed in New Mexico, unreasonably dangerous, defectively manufactured. He offered three hundred thousand. A mediator suggested two hundred twenty five thousand on the eve of trial. McDonald's refused both. From nineteen eighty two to ninety two the company had more than seven hundred burn reports from its coffee, and had settled scald claims for more than five hundred thousand. Appleton testified that number was not enough to change the practice.""",
    """Here is the leftover late night filed as a lottery ticket. Trial, eighth to seventeenth of August nineteen ninety four, Judge Robert H. Scott, Bernalillo County. Twelve jurors, eighteenth of August. Comparative negligence: McDonald's eighty percent, Liebeck twenty. The cup already had a warning. The jury said it was neither large enough nor sufficient. Two hundred thousand compensatory, cut twenty percent to one hundred sixty thousand. Punitive: two point seven million. The New York Times filed Morgan's suggestion: two days of coffee revenue, about one point three five million a day. Scott reduced punitive to four hundred eighty thousand, three times compensatory, six hundred forty thousand total. He called the conduct callous in one write-up, willful, wanton, and reckless in the Tort Museum's. Both sides appealed in December. Then a confidential settlement. Albuquerque Journal ran it first. Associated Press took it worldwide. ABC later called it the poster child of excessive lawsuits. Jonathan Turley called it a meaningful and worthy lawsuit. File both. Do not draw the injuries. Draw the numbers.""",
    """The prescription had a lid. After the verdict, news documented that the Albuquerque store was selling at one hundred fifty eight degrees the next day, a margin measured in seconds, not in comedy. Nationally, a two thousand seven report still filed McDonald's around one hundred seventy six to one hundred ninety four, relying on sterner wording on rigid foam cups. The New York Times in twenty thirteen said service had come down to one hundred seventy to one hundred eighty. The Specialty Coffee Association of America argued for better packaging rather than cooler coffee, and later helped defend other burn cases. So who actually moved: a local thermometer, a louder sentence on a cup, and a slower national range. A warning label is a costume for a temperature you already knew. A foam cup is a costume for seven hundred files you already paid.""",
    """Rehook, because the internet likes a story that America is a clown college of people who sue over coffee. Put a red X on that sermon. She was not driving. The car had no cup holders. She parked to use the lid. The company had seven hundred prior reports and still called eight hundred dollars a full offer. A Seinfeld gag is not a verdict. A tort-reform flyer is not a hospital chart. Susan Saladoff later argued the media version was a purposeful misrepresentation. HBO's Hot Coffee in twenty eleven spent a large chunk on how the details shrank. The New York Times Retro Report in twenty thirteen showed the story losing length and context until McDonald's looked like the victim. File the meme. Do not spend it as a fact. The leftover is uglier and smaller: a hold range, a tiny reminder, and a meeting that treated seven hundred burns as a rounding error.""",
    """File what the label actually did. Major vendors kept facing similar suits: Starbucks, Dunkin, Wendy's, Burger King, hospitals. Wikipedia notes McDonald's had not simply cooled the country after Liebeck, even if one Albuquerque window did. In twenty thirteen the range was still near boiling relative to a kitchen pot. Liebeck died the fifth of August two thousand four, aged ninety one. Her daughter said the burns and the court had taken their toll, and the settlement paid for a live-in nurse. That is not a punchline. That is a receipt for a two-year disability and a joke that outlived her. Do not invent a secret check. The amount stayed confidential. News later guessed under five hundred thousand. File the guess as a guess. The honest leftover is the cup copy: more words, same logistics, a policy that moved slower than a punchline.""",
    """None of this is a hymn to a perfect jury, and none of it is a cartoon of a grandmother as a gold-digger. They had a forty nine cent cup. They had a Ford with no holders. They had a corporate spec hotter than the rest of the block. You are allowed to laugh at a late-night host who skipped the grafts, and at an eight hundred dollar offer next to ten thousand in bills, and at a warning that the jury said was too small. You are not required to laugh at eight days in a ward, or at a daughter who lost three weeks of work, or at Appleton saying restaurants had more pressing dangers. The official idea was: customers want it that hot. The street idea was: she spilled it and won the lottery. The leftover idea is: they already had the temperature, they already had the complaints, and the fix was a louder lid on a policy they did not want to cool.""",
    """So who won. Not the eight hundred dollars. Not the driving joke. Liebeck won a verdict that got cut and then sealed. Morgan won a two-day coffee number the judge would not keep. Scott won a ratio. McDonald's won a poster child it did not write. Tort-reform ads won a mascot. The Albuquerque window won a cooler pot the next morning. The national cup won more ink. Seven hundred earlier files won almost nothing until a jury read them aloud. If you need a moral, skip America is sue-happy. Take this: a sitcom bit is a terrible whole story, and a hold temperature is a terrible honest one. The next time someone tells you she spilled coffee for millions, ask whether she was driving, what the cup said, and whether seven hundred reports count as a warning. Would you have paid the twenty thousand, or kept the one hundred eighty degree spec. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no cruelty, no burn wounds, no injury closeups, "
    "not mud-green archive night, not After Hours File dark. "
    "Coffee shown as a candy cup, a thermometer, a lid, a receipt, a tiny warning line, "
    "not photoreal restaurant logos, not a courtroom blood photo. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("49-cent", "A 49-cent cup put a 79-year-old in hospital for eight days.", f"A candy 49 CENT coffee cup next to a hospital tag 8 DAYS. Cream paper. {STYLE}"),
    ("not-trivia", "Not a clumsy-grandma lottery gag.", f"Ink shaking his head at a LOTTERY COFFEE stamp with a red X, mouth closed. {STYLE}"),
    ("feb-27", "27 February 1992, Albuquerque drive-through.", f"A date card 27 FEB 1992, ALBUQUERQUE. {STYLE}"),
    ("passenger", "Passenger seat. Grandson driving. Not her at the wheel.", f"A car tag PASSENGER, not DRIVER. {STYLE}"),
    ("no-holders", "1989 Ford Probe. No cup holders.", f"An empty dash NO CUP HOLDERS. {STYLE}"),
    ("parked-lid", "Parked to add cream and sugar. She pulled the far side of the lid.", f"A parked car, a lid coming off a candy cup. {STYLE}"),
    ("x-driving", "Put a red X on the joke that she was driving and spilled it for fun.", f"A DRIVING JOKE stamp with a giant red X. {STYLE}"),
    ("hold-180", "Franchise spec: hold coffee at 180 to 190 F.", f"A thermostat 180-190 F. {STYLE}"),
    ("flavour-consult", "Consultants: high brew heat extracts flavour.", f"A flavour beaker tag HOTTER = TASTE. {STYLE}"),
    ("drink-now", "Company research: customers meant to drink it immediately.", f"A cup tag DRINK NOW, not later. {STYLE}"),
    ("home-range", "Home makers about 135 to 150 F. City shops at least 20 F cooler.", f"Two thermometers HOME 140 vs SHOP 180. {STYLE}"),
    ("three-seconds", "190 F: about 3 seconds to a full-thickness burn. 180 F: 12 to 15. 160 F: about 20.", f"Three timers 3 SEC / 15 SEC / 20 SEC. No wounds. {STYLE}"),
    ("wipe-window", "Those extra seconds are time to wipe it off.", f"A wipe-cloth and a 20 SEC window. {STYLE}"),
    ("official-hot", "Official idea: hotter is better, a small reminder on the cup is enough.", f"A tiny cup line HOT, stamp OFFICIAL PLAN. {STYLE}"),
    ("bills-18k", "Bills: about $10,500 past, $2,500 future, $5,000 daughter's lost work. About $18,000 named.", f"A stack of bills 10500 / 2500 / 5000. {STYLE}"),
    ("asked-20k", "She sought $20,000 to cover the stack.", f"A request card 20000. {STYLE}"),
    ("offered-800", "McDonald's offered $800.", f"A tiny cheque 800. {STYLE}"),
    ("never-sued", "She had never filed a lawsuit.", f"A blank lawsuit stamp FIRST TIME. {STYLE}"),
    ("reed-morgan", "Houston attorney Reed Morgan. Similar 1986 case settled $27,500.", f"A folder MORGAN, tag 1986 27500. No portrait. {STYLE}"),
    ("appleton-heat", "Appleton: knew the risk, no plans to turn the heat down.", f"A quote card NO PLANS TO COOL, nameplate APPLETON. {STYLE}"),
    ("300k-225k", "Morgan offered $300,000. Mediator $225,000. Both refused.", f"Two refused stamps 300K and 225K. {STYLE}"),
    ("700-reports", "1982 to 1992: more than 700 burn reports. Settled scalds for more than $500,000.", f"A file cabinet 700 REPORTS, tag 500K PAID. {STYLE}"),
    ("not-enough", "Appleton: that number was not enough to change the practice.", f"A scale 700 vs NOT ENOUGH. {STYLE}"),
    ("aug-94", "Trial 8 to 17 August 1994. Verdict 18 August. Judge Robert H. Scott.", f"A calendar AUG 1994, nameplate SCOTT. {STYLE}"),
    ("80-20", "Jury: McDonald's 80 percent, Liebeck 20.", f"A pie 80 / 20. {STYLE}"),
    ("warning-small", "A warning was already on the cup. Jury: neither large enough nor sufficient.", f"A tiny cup warning vs a TOO SMALL stamp. {STYLE}"),
    ("160k", "Compensatory $200,000, cut 20 percent to $160,000.", f"A math card 200K minus 20% = 160K. {STYLE}"),
    ("two-days", "Punitive $2.7 million: two days of coffee revenue, about $1.35 million a day.", f"A coffee-sales ticker 1.35M / DAY x2. {STYLE}"),
    ("judge-cuts", "Judge cut punitive to $480,000. Total $640,000.", f"A gavel 2.7M down to 480K, total 640K. {STYLE}"),
    ("callous", "Scott: callous. Tort Museum also files willful, wanton, reckless.", f"A stamp CALLOUS. {STYLE}"),
    ("sealed", "Appeals, then a confidential settlement. Do not invent the cheque.", f"A sealed envelope CONFIDENTIAL. {STYLE}"),
    ("poster-child", "ABC: poster child of excessive lawsuits. Turley: meaningful and worthy.", f"Two headlines POSTER CHILD vs WORTHY. {STYLE}"),
    ("158-local", "Next day, Albuquerque window at 158 F. Seconds, not comedy.", f"A local pot 158 F, NEXT DAY. {STYLE}"),
    ("national-slow", "2007: still about 176 to 194 F nationally, louder cup words.", f"A national range 176-194, LOUDER LID. {STYLE}"),
    ("2013-range", "2013 NYT: service 170 to 180 F.", f"A later thermometer 170-180 F. {STYLE}"),
    ("x-clowns", "Rehook: red X on America-is-a-clown-college-of-coffee-suits.", f"Ink peeling a CLOWN COLLEGE sticker, mouth closed. {STYLE}"),
    ("packaging", "Specialty Coffee Association: better packaging, not cooler coffee.", f"A better lid vs a cooler pot, tag PACKAGING. {STYLE}"),
    ("not-driving", "She was not driving. No cup holders. Parked to use the lid.", f"Three cards NOT DRIVING / NO HOLDERS / PARKED. {STYLE}"),
    ("hot-coffee-doc", "HBO Hot Coffee, 2011. Details shrank until the company looked like the victim.", f"A film strip HOT COFFEE 2011, shrinking headline. {STYLE}"),
    ("nyt-retro", "NYT Retro Report 2013: the story lost length and context.", f"A news ticker getting shorter. {STYLE}"),
    ("same-suits", "Other vendors kept facing similar suits. National cooling was slow.", f"A row of candy cups OTHER SHOPS, still hot. No logos mash. {STYLE}"),
    ("died-2004", "Liebeck died 5 August 2004, aged 91. Settlement paid for a live-in nurse.", f"A date 5 AUG 2004, a nurse-tag, respectful, no grave. {STYLE}"),
    ("guess-500", "News later guessed the sealed amount under $500,000. File as a guess.", f"A guess card UNDER 500K, stamp GUESS. {STYLE}"),
    ("louder-lid", "The cup won more ink. The policy moved slower than a punchline.", f"A loud lid vs a slow policy snail. {STYLE}"),
    ("sitcom-x", "A sitcom bit is not a verdict.", f"A sitcom clapboard with a red X. {STYLE}"),
    ("who-won-800", "Not the $800. Not the driving joke.", f"A tiny 800 cheque in a bin, DRIVING JOKE in a bin. {STYLE}"),
    ("window-won", "The Albuquerque window won a cooler pot the next morning.", f"A local window trophy 158 F. {STYLE}"),
    ("ads-won", "Tort-reform ads won a mascot they did not interview.", f"A flyer mascot vs a real file 700. {STYLE}"),
    ("seven-hundred-aloud", "Seven hundred earlier files won almost nothing until a jury read them aloud.", f"A jury box reading a stack 700. No portraits. {STYLE}"),
    ("ask-driving", "Ask whether she was driving, what the cup said, and whether 700 reports count as a warning.", f"A question mark over a wheel, a cup, and 700. {STYLE}"),
    ("pay-or-spec", "Would you have paid the $20,000, or kept the 180-degree spec.", f"Split: a 20K card vs a 180 F spec, a question mark. {STYLE}"),
    ("lid-and-policy", "The leftover: a louder lid on a policy they did not want to cool.", f"A lid and a policy binder. {STYLE}"),
    ("hold-honest", "A sitcom bit is a terrible whole story. A hold temperature is a terrible honest one.", f"A laugh-track box vs a thermometer. {STYLE}"),
    ("receipt", "They already had the temperature. Drawn anyway.", f"A receipt card 180 F vs 800, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Coffee That Made a Warning Label",
        description=(
            "Nineteen ninety two. A forty-nine-cent cup, a one-hundred-eighty-degree hold, "
            "and a lid that had to get louder because the policy already knew."
        ),
        tags=(
            "history",
            "1994",
            "liebeck",
            "coffee",
            "law",
            "cartoon",
            "true story",
            "logistics",
            "warning",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="THEY OFFERED 800",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Coffee That Made a Warning Label",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-liebeck.json"
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

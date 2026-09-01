"""Author Drawn Anyway episode 21: Y2K, nineteen ninety nine to two thousand."""

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
    """A clock once wrote the year as nineteen thousand one hundred. That is not a metaphor, and it is not a cartoon you invented after a trivia night about bunkers and generators. On the first of January two thousand, the United States Naval Observatory, which runs the master clock that keeps the country's official time, put the date on its website as one January nineteen thousand one hundred. A New York video store billed about ninety one thousand two hundred fifty dollars because a tape looked one hundred years overdue. In Japan, ticket machines at thirteen stations paused. Keep those pictures. Then put a red X on the joke that nothing was ever wrong, and another X on the joke that the world ended at midnight. The leftover is not apocalypse. The leftover is two missing digits on a calendar that had been living on punch cards.""",
    """Start with why two digits were supposed to be ordinary. Memory was expensive. Wikipedia files ten dollars to more than one hundred dollars per kilobyte in nineteen seventy five. An IBM fourteen oh one could ship with as little as two kilobytes. Business data lived on eighty-column punch cards. Saving two digits on every date field was real money. Programs prefixed nineteen and stored eighty five for nineteen eighty five. When the year became zero zero, a machine that still assumed nineteen could file two thousand as nineteen hundred. Bob Bemer noticed the problem in nineteen fifty eight, working on genealogical software, and spent about twenty years trying to warn programmers, IBM, the United States government, and the International Organization for Standardization, including a COBOL picture clause for four-digit years. The official plan, if anyone had written one on a card in nineteen sixty, was going to work: the program will be replaced before the century turns. It was not replaced. Alan Greenspan said in nineteen ninety eight that he was one of the culprits, proud of squeezing space by not putting a nineteen before the year, and that it never entered their minds those programs would last more than a few years.""",
    """File the names that turned a punch-card habit into a government calendar. Massachusetts programmer David Eddy sent an e-mail on the twelfth of June nineteen ninety five and later said people had been calling it Century Date Change and Faulty Date Logic; Y two K just came off his fingertips. Peter de Jager's nineteen ninety three Computerworld piece Doomsday two thousand was called, by The New York Times, the information-age equivalent of Paul Revere's ride. Jerome and Marilyn Murray had already published Computers in Crisis in nineteen eighty four. By nineteen eighty seven the New York Stock Exchange had reportedly spent over twenty million dollars and hired about one hundred programmers, mostly because of bonds maturing past two thousand. In nineteen ninety six Senator Daniel Patrick Moynihan commissioned a Congressional Research Service study and urged President Bill Clinton to appoint an aide. In nineteen ninety eight the Year two thousand Information and Readiness Disclosure Act passed, and the President's Council on Year two thousand Conversion, chaired by John Koskinen, coordinated with FEMA. The Senate Special Committee, Robert F. Bennett chair and Christopher J. Dodd vice-chair, later filed the leftover as Crisis Averted.""",
    """Here is the leftover the internet still files as a panic tax. The Senate committee said the United States spent an estimated one hundred billion dollars, eight point five billion of that inside the federal government. Koskinen told reporters the country had spent one hundred billion since nineteen ninety five, and that the rest of the world had spent about another hundred, two hundred billion in his round count. Wikipedia later cites IDC at about one hundred thirty four billion in the United States preparing, thirteen billion more fixing in two thousand and two thousand one, and about three hundred eight billion worldwide. Gartner had floated three hundred to six hundred billion. File the range. Do not invent a nicer round number. Fixes had names: date expansion to four digits, the purest and most expensive; date windowing, a cheap patch that kept two digits and guessed the century; date compression; rewrite; replace the machine. COBOL shops pulled people out of retirement. The International Y two K Cooperation Center opened in Washington in March nineteen ninety nine, World Bank funding, Bruce W. McConnell as director, after national coordinators met at the United Nations in December nineteen ninety eight. That is logistics wearing a midnight.""",
    """Midnight did not arrive everywhere at once. New Zealand's clocks turned first. Koskinen later said he was pleasantly surprised by the lack of problems worldwide, that they had expected more, and that it was too early to declare victory until businesses opened on Monday. The FAA found a Year two thousand glitch in the Notice to Airmen system, attributed to a single line of code; operations never suffered, and the agency repaired it Saturday night. Godiva cash registers in American outlets failed, patched by the third of January. The Bureau of Alcohol, Tobacco and Firearms could not register new firearms dealers for five days. Japan: Ishikawa's Shika plant reported radiation monitoring equipment failed a few seconds after midnight; officials said there was no risk to the public and no excess radiation. NTT Docomo phones deleted new messages instead of old ones. In Germany, Deutsche Oper Berlin's payroll thought it was nineteen hundred and withheld childcare subsidies until accountants reset the year to nineteen ninety nine. In South Korea, a Gwangju video store generated a late fee of about eight million won, roughly seven thousand dollars, for a tape one hundred years overdue. Hundreds of glitches. None of that is a falling sky.""",
    """Rehook, because the internet likes a fake panic and a moral about sheep who bought canned food. Put a red X on that sermon. A two-digit year is not a personality. A website that prints nineteen thousand one hundred is not a census of American intelligence. Koskinen testified that he did not know of a single person working on Year two thousand who thought they had not confronted and avoided a major risk of systemic failure. He also told reporters that three older computers left running as a control group became unusable when the clock ticked over. File both. Ross Anderson at Cambridge said research suggesting the problem was smaller than some claimed was largely ignored by the media. Critics noted that some countries and small shops that did little also saw few disasters. File that too. The leftover is not that programmers invented a fee. The leftover is that unfixed machines in a control room failed, and a patched satellite ground station at Fort Belvoir, Virginia, crashed at seven in the evening Eastern on the thirty first of December nineteen ninety nine because of a patch meant to prevent the glitch, and was restored at eleven forty five on the second of January. A fix is still a machine.""",
    """File the calendar's extra tricks. Nine September nineteen ninety nine could be written nine nine ninety nine, which overlapped the dummy value nine thousand nine hundred ninety nine that operators typed for unknown dates. Fears of a mass halt were larger than what arrived. Then leap year. Two thousand is divisible by four hundred, so it is a leap year in the Gregorian calendar; nineteen hundred was not. Some programs assumed no century year could leap. On the twenty ninth of February, Reagan National's curbside baggage program initially failed to recognize the date. Offutt Air Force Base could not pull aircraft-maintenance records and used paper for a day. Montreal's tax computers read the first of March nineteen hundred. Norway's Signatur trains later failed on the thirty first of December two thousand because onboard computers considered the date invalid; engineers rolled clocks back a month. Windowing patches that treated zero zero through nineteen as two thousand later bit parking meters in twenty twenty. A two-digit year is a costume that keeps finding new midnights. The Senate committee, filing on the twenty ninth of February two thousand, said documented events had been minor, localized, and short-lived, and that the expenditure was justified.""",
    """None of this is a hymn to a gullible checkout, and none of it is a cartoon of engineers as priests who sold an apocalypse. They had eighty-column cards. They had two kilobytes. They had bonds that matured after two thousand. You are allowed to laugh at nineteen thousand one hundred on a Navy clock page, and at a video tape billed for a century, and at a payroll that thought the opera chorus were infants. You are not required to laugh at Moynihan writing a president, or at COBOL people pulled back to read uncommented code, or at Koskinen's control computers that actually died. John Hamre, Deputy Secretary of Defense, had called it the electronic equivalent of El Niño, with nasty surprises around the globe. File the weather metaphor. Do not spend it as a prophecy. Clinton said that if they acted properly it would be the first challenge of the twenty first century successfully met. The official idea was: expand the year before the clock does it for you. The street idea was: midnight is a bomb. The leftover idea is: midnight is a field width.""",
    """So who won. Not the bunkers. Not the headline that nothing happened. Not the headline that everything would. Bemer won a warning that took forty years to become a line item. Eddy won an abbreviation. Koskinen won a council and a Monday morning. Bennett and Dodd won a report titled Crisis Averted. The Naval Observatory won a webpage that could not count. The FAA won one line of code. The die-cut two-digit year won a hundred billion dollar season in one country's round count. If you need a moral, skip never trust a computer. Take this: a punch card is a terrible century, and a two-digit year is a terrible honest one. The next time someone tells you Year two thousand was fake, ask whether they mean the website that printed nineteen thousand one hundred or the three control machines Koskinen said became unusable, and whether the money was a panic or a field expansion. Would you have paid to write nineteen, or waited to see if the clock filed you under nineteen hundred. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no cruelty, not mud-green archive night, not After Hours File dark. "
    "Y2K shown as candy punch cards, two-digit clocks, a 19100 webpage, a video-store receipt, "
    "not apocalypse, not bunkers as the joke, not nuclear disaster. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("clock-19100", "A clock wrote the year as 19100.", f"A candy website clock 1 JAN 19100, master-clock tag, cream paper. {STYLE}"),
    ("not-trivia", "Not a bunkers-and-generators trivia gag.", f"Ink shaking his head at a BUNKERS stamp with a red X, mouth closed. {STYLE}"),
    ("video-late-fee", "A New York video store billed about $91,250 for a tape 100 years overdue.", f"A giant late-fee receipt $91250, 100 YEARS OVERDUE, a tiny VHS. Cute not cruel. {STYLE}"),
    ("japan-tickets", "Japan: ticket machines at 13 stations paused.", f"Thirteen tiny ticket machines PAUSED, tag JAPAN 13 STATIONS. No flags as joke. {STYLE}"),
    ("x-nothing", "Put a red X on nothing-was-wrong.", f"A NOTHING WAS WRONG stamp with a giant red X. {STYLE}"),
    ("x-ended", "Put a red X on the world-ended-at-midnight joke.", f"An END OF WORLD midnight stamp with a giant red X. Not grim. {STYLE}"),
    ("two-digits", "Leftover: two missing digits on a punch-card calendar.", f"A punch card with YEAR __ instead of 19, TWO DIGITS MISSING. {STYLE}"),
    ("memory-cost", "Memory was expensive: $10 to $100+ per kilobyte in 1975.", f"A price tag MEMORY $10-$100 PER KB, year 1975. {STYLE}"),
    ("ibm-1401", "An IBM 1401 could ship with as little as 2 kilobytes.", f"A candy mainframe tag IBM 1401, 2 KB. No photoreal logo mash. {STYLE}"),
    ("eighty-column", "Business data lived on 80-column punch cards.", f"An 80-COLUMN punch card with a date field squeezed. {STYLE}"),
    ("eighty-five", "Store 85 for 1985. Prefix 19.", f"A date field 85 with a sticker 19 glued in front. {STYLE}"),
    ("zero-zero", "When the year became 00, a machine could file 2000 as 1900.", f"A clock 00 splitting into 2000 vs 1900. {STYLE}"),
    ("bemer-1958", "Bob Bemer noticed it in 1958 on genealogical software.", f"A nameplate BOB BEMER, tags 1958 and FAMILY TREE CODE. No portrait. {STYLE}"),
    ("cobol-four", "He wanted COBOL picture clauses for four-digit years.", f"A COBOL card PICTURE 9999 YEAR. {STYLE}"),
    ("official-plan", "Official plan: the program will be replaced before the century turns.", f"A clipboard PLAN: REPLACE BEFORE 2000, a small DID NOT tag. {STYLE}"),
    ("greenspan", "Greenspan 1998: I squeezed space by not putting 19. Culprit.", f"A quote card I SQUEEZED SPACE, nameplate GREENSPAN 1998. No portrait. {STYLE}"),
    ("eddy-y2k", "David Eddy, 12 June 1995: Y2K came off my fingertips.", f"An email slip 12 JUN 1995, Y2K, nameplate DAVID EDDY. {STYLE}"),
    ("de-jager", "Peter de Jager, Computerworld 1993: Doomsday 2000.", f"A magazine clip DOOMSDAY 2000, DE JAGER 1993. Not a real logo. {STYLE}"),
    ("nyse-1987", "NYSE by 1987: over $20 million, about 100 programmers, bonds past 2000.", f"A tally $20M, 100 PROGRAMMERS, BONDS PAST 2000. {STYLE}"),
    ("moynihan", "Moynihan 1996: CRS study, letter to Clinton.", f"A letter stack MOYNIHAN 1996 CRS, TO THE PRESIDENT. No portrait. {STYLE}"),
    ("koskinen-council", "1998: President's Council, John Koskinen, with FEMA.", f"A council sign YEAR 2000 CONVERSION, nameplate KOSKINEN. {STYLE}"),
    ("readiness-act", "Year 2000 Information and Readiness Disclosure Act, 1998.", f"A law folder READINESS DISCLOSURE ACT 1998. {STYLE}"),
    ("bennett-dodd", "Senate committee: Bennett chair, Dodd vice-chair. Crisis Averted.", f"Two nameplates BENNETT and DODD, stamp CRISIS AVERTED. {STYLE}"),
    ("hundred-billion", "US round count: about $100 billion. Federal $8.5 billion.", f"A ledger US $100B, FEDERAL $8.5B. {STYLE}"),
    ("range-costs", "File the range: Koskinen $200B world; IDC about $308B; Gartner $300-600B.", f"Three cards $200B, $308B, $300-600B, FILE THE RANGE. {STYLE}"),
    ("expansion", "Date expansion to four digits: purest, most expensive.", f"A 2-digit year stretching into 4 digits, tag PUREST. {STYLE}"),
    ("windowing", "Date windowing: keep two digits, guess the century.", f"A window over 00-99 guessing 1900s vs 2000s. {STYLE}"),
    ("cobol-retirement", "COBOL shops pulled people out of retirement.", f"A COBOL binder and a RETURNING PASS, no mockery. {STYLE}"),
    ("un-center", "International Y2K Cooperation Center, March 1999, World Bank, McConnell.", f"A Washington office plate IY2KCC MAR 1999, McCONNELL. {STYLE}"),
    ("nz-first", "Midnight did not arrive everywhere at once. New Zealand first.", f"A globe with a FIRST MIDNIGHT pin on New Zealand. No flag as joke. {STYLE}"),
    ("pleasantly", "Koskinen: pleasantly surprised, expected more, too early to declare victory.", f"A briefing card PLEASANTLY SURPRISED, TOO EARLY. {STYLE}"),
    ("faa-one-line", "FAA NOTAM glitch: one line of code. Ops never suffered. Fixed Saturday night.", f"A single glowing CODE LINE, FAA NOTAM, OPS OK. {STYLE}"),
    ("godiva-tills", "Godiva registers failed. Patched by 3 January.", f"Candy cash registers X'd, patch tag 3 JAN. {STYLE}"),
    ("shika-sensor", "Shika plant: radiation monitors failed seconds after midnight. Officials: no public risk.", f"A sensor panel X'd, tag NO PUBLIC RISK. Not a disaster, not gore, no mushroom cloud. {STYLE}"),
    ("berlin-payroll", "Deutsche Oper payroll thought 1900, withheld childcare until year reset to 1999.", f"A payroll slip YEAR 1900, RESET TO 1999. {STYLE}"),
    ("rehook-sheep", "Rehook: red X on the fake-panic sheep sermon.", f"Ink peeling a SHEEP stamp off a clock, mouth closed. {STYLE}"),
    ("koskinen-risk", "Koskinen: no one on the work thought they had not avoided major systemic risk.", f"A quote card AVOIDED MAJOR RISK, KOSKINEN. {STYLE}"),
    ("control-three", "Three control-group computers left unfixed became unusable at rollover.", f"Three old candy computers with UNUSABLE tags at 00:00. {STYLE}"),
    ("file-both", "Cambridge critics said the scare was oversized. File both.", f"Two folders REAL BUG and OVERSIZED SCARE, FILE BOTH. {STYLE}"),
    ("fort-belvoir", "Fort Belvoir: a patch crashed spy-satellite ground gear 31 Dec, restored 2 Jan 11:45pm.", f"A ground dish and a PATCH stamp that tripped a crash, restored 2 JAN. No war, no gore. {STYLE}"),
    ("nine-nine-nine", "9/9/99 overlapped dummy date 9999 for unknown fields.", f"A form field 9999 vs calendar 9 SEP 1999. {STYLE}"),
    ("leap-400", "2000 is a leap year because it is divisible by 400. 1900 was not.", f"A leap-year rule card /400 YES, 1900 NO, 2000 YES. {STYLE}"),
    ("feb-29-airport", "29 Feb: Reagan National curbside baggage program failed the date.", f"Airport curb bags, calendar 29 FEB, program X. {STYLE}"),
    ("paper-offutt", "Offutt: aircraft-maintenance records on paper for a day.", f"A paper stack PAPER FOR A DAY, hangar clipboard. {STYLE}"),
    ("window-2020", "Windowing later bit 2020: parking meters, bills printed 1920.", f"A parking meter 1920, a bill YEAR 1920, tag 2020. {STYLE}"),
    ("senate-minor", "Senate 29 Feb 2000: minor, localized, short-lived. Expenditure justified.", f"A report cover MINOR LOCALIZED, JUSTIFIED. {STYLE}"),
    ("not-fools", "Not a cartoon of shoppers as fools, or engineers as priests of panic.", f"Ink peeling a FOOLS sticker and a PRIESTS sticker, mouth closed. {STYLE}"),
    ("hamre-nino", "Hamre: electronic equivalent of El Niño. File the metaphor. Do not spend it as prophecy.", f"A weather map labeled METAPHOR, not a disaster reel. {STYLE}"),
    ("clinton-met", "Clinton: first challenge of the 21st century successfully met.", f"A podium card FIRST CHALLENGE SUCCESSFULLY MET. No photoreal. {STYLE}"),
    ("field-width", "Official idea: expand the year. Street idea: midnight is a bomb. Leftover: field width.", f"Three cards EXPAND / BOMB / FIELD WIDTH. {STYLE}"),
    ("who-won-digits", "Not the bunkers. The two-digit year won a line item.", f"A punch-card beating a tiny bunker, TWO DIGITS trophy. {STYLE}"),
    ("19100-or-control", "Ask whether they mean 19100 on a webpage or three unusable control machines.", f"Split: webpage 19100 vs three dead PCs, a question mark. {STYLE}"),
    ("pay-or-wait", "Would you have paid to write 19, or waited to be filed under 1900.", f"Split: a $ bill writing 19 vs a clock stamping 1900, a question mark. {STYLE}"),
    ("receipt", "A calendar was two digits short. Drawn anyway.", f"A receipt card FIELD WIDTH vs MIDNIGHT, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Bug That Was a Calendar",
        description=(
            "Y2K, nineteen ninety nine. Two digits on a punch card, a council, "
            "and a website that printed nineteen thousand one hundred."
        ),
        tags=(
            "history",
            "y2k",
            "2000",
            "computers",
            "cartoon",
            "true story",
            "logistics",
            "funny",
            "millennium",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="TWO DIGITS SHORT",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Bug That Was a Calendar",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-y2k.json"
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

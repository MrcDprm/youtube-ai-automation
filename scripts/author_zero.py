"""Author episode: you write zero and treat nothing as a number."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."

CHAPTERS = [
    """Tonight you will write a zero and treat nothing as a number, the way you treat an empty inbox as finished. Your hand will circle a hole on the page as if the hole were always allowed to count. Here is the part that should bother you. The first accountants did not get to borrow a blank. Many ancient systems wrote quantities without a symbol for absence, which is a polite way of saying subtraction had to perform gymnastics every time a column emptied out. So why does your keyboard wear a zero as if zero were physics? Because Babylonian scribes used a placeholder wedge in sexagesimal columns, because Indian mathematicians including Brahmagupta in the seventh century wrote rules for zero as a number, because Islamic scholars carried the idea along trade routes and books, because Fibonacci's Liber Abaci in twelve oh two showed Europe a table that could hold a hole, and because printing and commerce learned that a blank digit is easier to multiply than a philosophical argument. That is the whole plot. Your zero is not emptiness by nature. It is a placeholder that learned to vote. You still write it. The write is flattered. That is its job. The page did not vote. A scribe did, and then a circle that taught your column the hole until the hole started calling itself sense. Sense is a word a placeholder invented so nothing would still feel like law when the clay was gone.""",
    """Start with the hole, because the zero stole a blank space and then sold it back as a digit. Long before calculators, before spreadsheets, before a phone could divide by nothing and call it an error message, people counted things that were present. Absence was a story you told in words, not a symbol you typed. Roman numerals could express many quantities, yet an empty column in their world was a silence you worked around, not a character you pressed. If your zero still feels like the only adult option, notice that the adult option started as a workaround dragged onto a tablet. The tablet did not ask for poetry. The tablet asked for columns that could repeat. Columns are useful when you need a market, a temple, and a tax collector to agree on how much grain is left without waiting for a philosopher to finish a sentence about void. The abacus keeps quantity like beads on a wire. The zero keeps quantity like a hole that forgot it was a trick. You can love both and still admit only one of them is wearing your calculator's default skin.""",
    """Named corners, because a myth of one inventor is how a hole gets a halo it did not earn. Zero is not a single eureka moment you can pin on one hero with a plaque. It is a layer cake of placeholder wedges, Indian numerals, and a circle that behaved nicely when you needed to multiply without crying. Babylonian cuneiform used a wedge mark to hold a column open in sexagesimal notation, a placeholder rather than a full number in the modern sense. In India, Brahmagupta's Brahmasphutasiddhanta in six twenty eight included rules for zero in addition and subtraction. Later Indian and Islamic mathematicians including al-Khwarizmi helped transmit the idea through texts and trade. Leonardo of Pisa, known as Fibonacci, published Liber Abaci in twelve oh two and showed European merchants a numeral system with a zero that could sit in a column like a polite absence. If you still treat zero as sacred emptiness, file the paperwork separately from the history. Zero did not fall out of a meditation. It fell out of columns that needed a mark for nothing, then exported the habit along books until the habit felt like math. Your keyboard is a placeholder wearing a circle.""",
    """Watch the hole leave the wedge, because a horizontal market of speed needed a digit that did not require a speech about void every time a column emptied. Early accounting tricks were honest and exhausting. Rewrite the whole sum. Skip the blank. Argue with a philosopher. Repeat. A zero in a column is a small insult to silence with a large gift to multiplication. The circle flexes across fonts and centuries. The column repeats. The placeholder presses against other digits with a grudge soft enough not to break addition. The symbol says nothing here without asking the clerk to become a poet. I am not giving you a list of firsts. I am pointing at the swap. We took a blank that said skip this column and we replaced it with a character that said count the absence. Count is easier to teach in a textbook. Count is easier to print on a page. Count is easier to repeat when the ledger speeds up. The ledger is the real inventor. The ledger does not care about your nostalgia for Roman gymnastics. The ledger cares about digits that fit.""",
    """This is the rehook. You think zero is a fact, the way one is a fact. Zero is a policy. In a modern spreadsheet the policy is already on, because the alternative is trusting every column to leave a gap and hope nobody misreads the gap as a smudge. Gaps are honest. Zeros are scalable. Scalable is how a placeholder escapes the philosopher's bench and becomes something a school can teach in numbers. I am not calling you clumsy for liking a circle. I am un-naturing the hole. The hole is a wedge mark wearing a font. The font said absence can be law. Law is a feeling when your hand writes zero without remembering when it learned it. If you have ever divided a bill and felt relief that empty seats become zero, congratulations. You have been living inside a column's factor list. The relief is real. The relief is also a truce you never signed. A truce is not a page that voted. A truce is a spreadsheet with circles.""",
    """Mass production did not invent counting. It inventoried the answer. When the same ledger had to repeat across shops, zero became the digit you could typeset, print, ship, and teach without translating a placeholder ritual for every merchant. Double-entry bookkeeping, scientific notation, computers: decades later the zero could sit in a register as a bit pattern, a useful chapter about engineering, not the origin story of the hole itself. Do not make tonight a biopic about one monk in a scriptorium. Make it about the object: circle, column, repeat, multiply. A catalog is a quiet referendum. If your phone has a zero key and your history book has Roman numerals, that gap is not evolution. It is inventory. Inventory is how the past loses a fight without filing a complaint.""",
    """This is you, already, in the middle of the story. A Tuesday, a receipt, a line item that reads zero and still prints. You stare at the circle because checkout would feel broken without a digit for none, which is the most modern impossibility there is. None of this makes you mathematical by nature. It makes you a person born after Liber Abaci and after schools turned placeholders into homework and after a circle learned to host balances, temperatures, and error codes that beep. You can feel both in the same glance: relief that you do not have to leave a column blank and hope, and a tiny insult that a wedge mark outlasted the clay. The relief is real. The insult is the blank column failing for a second in your imagination. You paid for a cleaner sum with a symbol you never voted on. The symbol is cheerful. Cheerful is how a hole stays in the century without looking like a hole.""",
    """A numeral system is a pile of compromises with a circle attached. That sentence is rude and almost fair. Take zero away and arithmetic becomes a workshop puzzle nobody wins, or a rewrite on every sum until the merchant breaks. Columns, multiplication tables, assembly of digits: the zero is a diagram of how to mark absence without stopping the row, written by scribes you will not meet. You still write. The write is a vote for a placeholder that was sold as obvious. I am not telling you to hunt for a Babylonian wedge as a personality. I am telling you the personality was always the swap: a blank column, a wedge mark, Brahmagupta's rules, al-Khwarizmi's texts, Fibonacci's table, a printed textbook, a register that stores nothing as a number. The crowd is still on the page. The crowd is you and a spreadsheet treating a circle as a treaty. So what did we trade? We traded silence for a visible absence. We traded philosophical pauses for a digit payroll software can love. We gained a shared hole that lets a cashier, a scientist, and a CPU agree on none without rewriting the row. Help can be a miracle and still be a part number. We also gained a myth that zero is nothing pure, that the circle is the only adult way to mark empty, that a blank column is a joke you outgrow. We kept the placeholder and called it a number. We kept the blank and called it history. Both can be true and still not be a reason to forget zero is a policy that learned manners.""",
    """This is you. You will write the zero again. The circle will still be there. You will feel nothing, which is the victory. Look at the digit. That is not the sky and it is not a single hero monk. That is a Babylonian wedge, Brahmagupta in six twenty eight, texts crossing through Islamic scholars, Fibonacci in twelve oh two, a printed textbook, and a register that still owns your receipt so you will keep treating nothing as law. You are allowed to write. You are allowed to hate empty columns and still multiply. Just stop calling zero natural, or inevitable, or proof that you are modern. Tonight, when the circle holds a column open, look at it like a leftover salute to a blank that left the clay. The salute is cheerful. The hole is the point. Go when the row lets you. Know which placeholder you are still obeying.""",
]


def _stamp(index: int) -> str:
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("write-zero", "Tonight you write a zero and treat nothing as a number.", f"Stickman writing zero, NOTHING AS NUMBER, {PAINT}"),
    ("empty-inbox", "The way you treat an empty inbox as finished.", f"Empty inbox FINISHED vs zero, {PAINT}"),
    ("circle-hole", "Your hand circles a hole as if the hole were always allowed to count.", f"Hand circling hole ALLOWED TO COUNT, {PAINT}"),
    ("no-blank", "The first accountants did not get to borrow a blank.", f"Accountant red X blank borrow, {PAINT}"),
    ("no-absence", "Ancient systems wrote quantities without a symbol for absence.", f"Ancient numbers no absence symbol, {PAINT}"),
    ("subtraction-gymnastics", "Subtraction had to perform gymnastics when a column emptied.", f"Subtraction gymnastics empty column, {PAINT}"),
    ("why-zero-key", "Why does your keyboard wear a zero as if zero were physics?", f"Keyboard zero PHYSICS costume, {PAINT}"),
    ("babylon-wedge", "Babylonian scribes used a placeholder wedge in sexagesimal columns.", f"Babylon wedge placeholder column, {PAINT}"),
    ("brahmagupta-628", "Brahmagupta in the seventh century wrote rules for zero as a number.", f"Brahmagupta 628 ZERO RULES book, {PAINT}"),
    ("islamic-books", "Islamic scholars carried the idea along trade routes and books.", f"Trade route books carrying zero idea, {PAINT}"),
    ("fibonacci-1202", "Fibonacci Liber Abaci twelve oh two showed Europe a table with a hole.", f"Fibonacci 1202 LIBER ABACI hole, {PAINT}"),
    ("printing-commerce", "Printing and commerce learned a blank digit is easier to multiply.", f"Printing commerce multiply zero digit, {PAINT}"),
    ("not-emptiness", "Your zero is not emptiness by nature.", f"EMPTINESS red X zero wins, {PAINT}"),
    ("placeholder-vote", "A placeholder that learned to vote.", f"Placeholder wearing VOTE badge, {PAINT}"),
    ("write-flattered", "The write is flattered. That is its job.", f"Smiling zero FLATTERED badge, {PAINT}"),
    ("page-no-vote", "The page did not vote. A scribe did.", f"Page NO VOTE scribe hand up, {PAINT}"),
    ("hole-sense", "The hole taught your column until it called itself sense.", f"Column word SENSE after hole, {PAINT}"),
    ("start-hole", "Start with the hole.", f"Zero hole labeled START, {PAINT}"),
    ("zero-stole-blank", "Zero stole a blank space and sold it back as a digit.", f"Blank stolen by zero digit, {PAINT}"),
    ("before-calculators", "Long before calculators, spreadsheets, divide-by-zero errors.", f"Timeline before calculator spreadsheet, {PAINT}"),
    ("counted-present", "People counted things that were present.", f"Present things counted checkmarks, {PAINT}"),
    ("absence-in-words", "Absence was a story in words not a symbol you typed.", f"Absence words not typed symbol, {PAINT}"),
    ("roman-silence", "Roman numerals worked around empty columns as silence.", f"Roman numerals silence empty column, {PAINT}"),
    ("workaround-tablet", "The adult option started as a workaround on a tablet.", f"Workaround dragged onto tablet, {PAINT}"),
    ("columns-repeat", "The tablet asked for columns that could repeat.", f"Repeating columns on tablet, {PAINT}"),
    ("grain-left", "Market temple tax collector agree how much grain is left.", f"Market temple tax grain left agree, {PAINT}"),
    ("abacus-beads", "The abacus keeps quantity like beads on a wire.", f"Abacus beads on wire, {PAINT}"),
    ("hole-trick", "Zero keeps quantity like a hole that forgot it was a trick.", f"Hole forgot TRICK reminder, {PAINT}"),
    ("named-corners", "Named corners. One inventor is a halo the hole did not earn.", f"Halo on zero MYTH sticker, {PAINT}"),
    ("not-one-hero", "Zero is not one eureka moment on a plaque.", f"Hero plaque red X layer cake, {PAINT}"),
    ("layer-cake", "Placeholder wedges, Indian numerals, circle that multiplied.", f"Layer cake wedge Indian circle, {PAINT}"),
    ("babylon-placeholder", "Babylonian wedge held a column open, placeholder not full number.", f"Cuneiform wedge placeholder column, {PAINT}"),
    ("brahmagupta-rules", "Brahmasphutasiddhanta six twenty eight rules for zero.", f"Brahmasphutasiddhanta 628 zero rules, {PAINT}"),
    ("al-khwarizmi", "Islamic mathematicians including al-Khwarizmi transmitted the idea.", f"Al-Khwarizmi texts transmitting zero, {PAINT}"),
    ("fibonacci-merchants", "Fibonacci showed European merchants zero in a column.", f"Fibonacci merchants zero column, {PAINT}"),
    ("not-sacred", "Zero is not sacred emptiness.", f"SACRED EMPTINESS red X, {PAINT}"),
    ("mark-for-nothing", "Columns needed a mark for nothing.", f"Column needs MARK FOR NOTHING, {PAINT}"),
    ("placeholder-circle", "Your keyboard is a placeholder wearing a circle.", f"Keyboard placeholder circle costume, {PAINT}"),
    ("hole-leaves-wedge", "Watch the hole leave the wedge.", f"Hole walking away from wedge, {PAINT}"),
    ("market-speed", "A market of speed needed a digit not a speech about void.", f"Market speed needs digit not void speech, {PAINT}"),
    ("rewrite-skip", "Rewrite the sum. Skip the blank. Argue with philosopher. Repeat.", f"Four panel REWRITE SKIP ARGUE REPEAT, {PAINT}"),
    ("insult-silence", "Zero is a small insult to silence.", f"Zero insulting silence cloud, {PAINT}"),
    ("gift-multiply", "A large gift to multiplication.", f"Multiplication happy gift from zero, {PAINT}"),
    ("circle-flexes", "The circle flexes across fonts and centuries.", f"Zero circle flexing fonts centuries, {PAINT}"),
    ("placeholder-grudge", "Placeholder presses digits with soft grudge.", f"Placeholder GRUDGE SOFT on digits, {PAINT}"),
    ("nothing-here", "The symbol says nothing here without poetry.", f"ZERO says NOTHING HERE no poem, {PAINT}"),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", f"FIRSTS red X SWAP arrow, {PAINT}"),
    ("blank-to-character", "Skip this column replaced by count the absence.", f"SKIP COLUMN vs COUNT ABSENCE, {PAINT}"),
    ("print-page", "Easier to print on a page.", f"Zero easy PRINT on page, {PAINT}"),
    ("ledger-inventor", "The ledger is the real inventor.", f"Ledger wearing INVENTOR badge, {PAINT}"),
    ("digits-fit", "The ledger cares about digits that fit.", f"Digits fitting ledger slot, {PAINT}"),
    ("rehook-fact", "Rehook: you think zero is a fact like one.", f"Zero vs one both labeled FACT, {PAINT}"),
    ("zero-policy", "Zero is a policy.", f"Zero stamped POLICY, {PAINT}"),
    ("leave-gap", "Trust every column to leave a gap and hope.", f"Gap hope red X smudge risk, {PAINT}"),
    ("gaps-honest", "Gaps are honest.", f"Gap labeled HONEST, {PAINT}"),
    ("zeros-scalable", "Zeros are scalable.", f"Zeros multiplying SCALABLE, {PAINT}"),
    ("school-teaches", "Scalable is how placeholder escapes philosopher's bench.", f"Philosopher bench to school numbers, {PAINT}"),
    ("un-nature-hole", "Not calling you clumsy. Un-naturing the hole.", f"NATURE sticker peeling off zero, {PAINT}"),
    ("wedge-font", "The hole is a wedge mark wearing a font.", f"Wedge inside font costume, {PAINT}"),
    ("absence-law", "The font said absence can be law.", f"Font stamp ABSENCE LAW, {PAINT}"),
    ("divide-bill", "Divide a bill, empty seats become zero.", f"Bill split empty seats zero relief, {PAINT}"),
    ("factor-list", "Living inside a column's factor list.", f"Column factor list around stickman, {PAINT}"),
    ("spreadsheet-circles", "A truce is a spreadsheet with circles.", f"Spreadsheet circles truce, {PAINT}"),
    ("mass-inventoried", "Mass production inventoried the answer.", f"INVENT COUNT red X INVENTORIED, {PAINT}"),
    ("ledger-repeat", "Same ledger repeated across shops.", f"Identical ledgers row of shops, {PAINT}"),
    ("typeset-teach", "Zero you could typeset print ship teach.", f"Zero TYPESET PRINT SHIP TEACH, {PAINT}"),
    ("double-entry", "Double-entry bookkeeping scientific notation computers.", f"Double entry science computer brief icons, {PAINT}"),
    ("not-biopic", "Not tonight a biopic about one monk.", f"MONK BIOPIC red X object focus, {PAINT}"),
    ("object-circle", "Make it about the object: circle column repeat multiply.", f"Circle column repeat multiply cycle, {PAINT}"),
    ("quiet-referendum", "A catalog is a quiet referendum.", f"Catalog voting QUIET REFERENDUM, {PAINT}"),
    ("phone-vs-roman", "Phone has zero key, history book has Roman numerals.", f"Phone zero vs Roman book gap, {PAINT}"),
    ("inventory-fight", "That gap is inventory.", f"Inventory beating Roman numerals, {PAINT}"),
    ("this-is-you", "This is you. A Tuesday. A receipt.", f"Stickman Tuesday receipt zero line, {PAINT}"),
    ("line-zero", "A line item reads zero and still prints.", f"Receipt line ZERO still prints, {PAINT}"),
    ("checkout-none", "Checkout feels broken without a digit for none.", f"Checkout broken without zero digit, {PAINT}"),
    ("modern-impossibility", "The most modern impossibility there is.", f"MODERN IMPOSSIBILITY cloud, {PAINT}"),
    ("not-mathematical", "None of this makes you mathematical by nature.", f"MATHEMATICAL NATURE red X, {PAINT}"),
    ("born-after-fibonacci", "Born after Liber Abaci and school homework.", f"Timeline Fibonacci school homework, {PAINT}"),
    ("error-codes", "Circle hosts balances temperatures error codes.", f"Zero in balance temp error code icons, {PAINT}"),
    ("relief-no-blank", "Relief you do not leave a column blank and hope.", f"Happy no blank column hope, {PAINT}"),
    ("insult-wedge", "A tiny insult that a wedge outlasted clay.", f"Wedge beating clay insult cloud, {PAINT}"),
    ("never-voted", "You paid for a cleaner sum you never voted on.", f"Receipt never voted zero symbol, {PAINT}"),
    ("cheerful-hole", "Cheerful is how a hole stays without looking like a hole.", f"Smiling zero hole disguise, {PAINT}"),
    ("compromises-circle", "Numeral system is compromises with a circle attached.", f"Compromise stack circle on top, {PAINT}"),
    ("take-zero-away", "Take zero away and arithmetic becomes a puzzle.", f"Arithmetic puzzle no zero, {PAINT}"),
    ("diagram-absence", "Zero marks absence without stopping the row.", f"Diagram absence row continues, {PAINT}"),
    ("watch-vote", "The write is a vote for placeholder sold as obvious.", f"Writing zero voting OBVIOUS, {PAINT}"),
    ("swap-personality", "Swap: blank column wedge Brahmagupta al-Khwarizmi Fibonacci textbook register.", f"Six icons blank wedge Brahmagupta Fibonacci register, {PAINT}"),
    ("crowd-page", "The crowd is still on the page.", f"Many stickmen on one page with zeros, {PAINT}"),
    ("circle-treaty", "You and spreadsheet treating circle as treaty.", f"Spreadsheet zero treaty paper, {PAINT}"),
    ("what-trade", "So what did we trade?", f"Trade scale silence vs visible absence, {PAINT}"),
    ("silence-absence", "We traded silence for visible absence.", f"Silence vs VISIBLE ABSENCE scale, {PAINT}"),
    ("pause-digit", "Philosophical pauses for digit software loves.", f"Philosophy pause vs DIGIT payroll, {PAINT}"),
    ("shared-hole", "Shared hole cashier scientist CPU agree on none.", f"Cashier scientist CPU agree NONE, {PAINT}"),
    ("miracle-part", "Help can be miracle and still part number.", f"Halo zero PART NUMBER tag, {PAINT}"),
    ("zero-nothing-myth", "Myth that zero is nothing pure.", f"ZERO=NOTHING PURE myth, {PAINT}"),
    ("blank-joke", "Myth blank column is joke you outgrow.", f"BLANK JOKE red X, {PAINT}"),
    ("kept-placeholder", "We kept placeholder and called it number.", f"Placeholder renamed NUMBER, {PAINT}"),
    ("kept-blank-history", "We kept blank and called it history.", f"Blank in museum HISTORY label, {PAINT}"),
    ("policy-manners", "Zero is policy that learned manners.", f"Zero policy polite bow tie, {PAINT}"),
    ("write-again", "You will write zero again. Circle still there.", f"Callback writing zero again, {PAINT}"),
    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at zero, {PAINT}"),
    ("look-digit", "Look at digit. Not sky not single hero monk.", f"Zero between red X sky red X monk, {PAINT}"),
    ("named-stack", "Babylon wedge Brahmagupta Islamic texts Fibonacci textbook register.", f"Stack wedge Brahmagupta Fibonacci register, {PAINT}"),
    ("zero-law", "Register owns receipt so nothing stays law.", f"Register receipt zero stamped LAW, {PAINT}"),
    ("allowed-write", "Allowed to write and hate empty columns and multiply.", f"Write ok hate empty columns multiply, {PAINT}"),
    ("not-natural", "Stop calling zero natural.", f"NATURAL stamp red X on zero, {PAINT}"),
    ("not-inevitable", "Not inevitable. Not proof you are modern.", f"INEVITABLE MODERN red X, {PAINT}"),
    ("leftover-blank", "Leftover salute to blank that left clay.", f"Salute blank leaving clay, {PAINT}"),
    ("hole-point", "Salute cheerful. Hole is the point.", f"Cheerful salute on zero hole, {PAINT}"),
    ("know-placeholder", "Go when row lets you. Know which placeholder you obey.", f"Stickman which placeholder obeying, {PAINT}"),
    ("glance-cheerful", "Cheerful is how zero stays without looking like scribe.", f"Smiling zero scribe ghost hidden, {PAINT}"),
    ("divide-by-zero", "Divide by zero is error message not origin story.", f"Divide by zero ERROR not origin, {PAINT}"),
    ("column-open", "Column open is design brief of zero.", f"COLUMN OPEN design brief stamp, {PAINT}"),
    ("multiplication-table", "Multiplication table needs zero like a seat.", f"Times table zero seat empty, {PAINT}"),
    ("temperature-zero", "Temperature scale uses zero as agreed cold anchor.", f"Thermometer zero cold anchor, {PAINT}"),
    ("binary-bit", "Computer bit can store nothing as pattern.", f"Binary bit stores nothing pattern, {PAINT}"),
    ("placeholder-clay", "Placeholder started on clay not in calculator.", f"Clay tablet placeholder origin, {PAINT}"),
    ("indian-numerals", "Indian numerals carried circle across columns.", f"Indian numerals circle columns, {PAINT}"),
    ("merchant-ledger", "Merchant ledger wanted rows that never stop.", f"Merchant ledger rows never stop, {PAINT}"),
    ("school-circle", "School taught circle before philosophy finished.", f"School circle before philosophy done, {PAINT}"),
    ("void-speech", "Void speech is slow. Zero stroke is fast.", f"Void speech slow zero stroke fast, {PAINT}"),
    ("placeholder-commute", "Placeholder learned to commute on your keyboard.", f"Placeholder commuting on keyboard, {PAINT}"),
    ("abacus-empty", "An empty wire on the abacus wanted a name.", f"Empty abacus wire wants name, {PAINT}"),
    ("roman-subtract", "Roman subtraction was a workout zero avoids.", f"Roman subtract workout zero avoids, {PAINT}"),
    ("column-zero-seat", "Zero is the seat that keeps the row honest.", f"Zero seat keeps row honest, {PAINT}"),
    ("register-none", "Register stores none so none can add.", f"Register stores NONE can add, {PAINT}"),
    ("textbook-circle", "Textbook circle beat philosophy to the lesson.", f"Textbook circle beats philosophy, {PAINT}"),
    ("merchant-row", "Merchant row that never stops needs a hole.", f"Merchant row never stops needs hole, {PAINT}"),
    ("wedge-to-circle", "The wedge became a circle when columns sped up.", f"Wedge morphing into circle columns speed, {PAINT}"),
    ("curb-read", "Readable absence is whole design brief.", f"READABLE ABSENCE design brief, {PAINT}"),
    ("final-callback", "Wedge. Circle. Your column.", f"Final callback wedge circle your column, {PAINT}"),
]


def _beats() -> list[tuple[str, str, str]]:
    if len(_ROWS) != paint_beat_count(660.0):
        raise SystemExit(f"need {paint_beat_count(660.0)} beats, got {len(_ROWS)}")
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
        title="Why Nothing Became a Number",
        description=(
            "Zero feels obvious. Ancient systems had no symbol for absence. "
            "Babylonian placeholders, Brahmagupta's rules, Islamic texts, and "
            "Fibonacci's Liber Abaci turned a blank column into a digit."
        ),
        tags=(
            "zero",
            "number",
            "mathematics",
            "brahmagupta",
            "fibonacci",
            "history",
            "why",
            "placeholder",
            "numerals",
            "math",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="ZERO HOLE?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Nothing Became a Number",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-zero.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    board = PROJECT_ROOT / "output" / "storyboard" / scenario.project_id
    board.mkdir(parents=True, exist_ok=True)
    tsv = board / "beats.tsv"
    lines = ["index\tfilename\tprompt"]
    for index, (slug, _covers, prompt) in enumerate(beats, start=1):
        lines.append(f"{index:03d}\t{index:02d}-{slug}.png\t{prompt}")
    tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(scenario.project_id)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))
    print("accent", scenario.subtitles.accent_color, "rate", scenario.tts.rate)
    print("hook", scenario.youtube.thumbnail_hook)
    print("tsv", tsv)


if __name__ == "__main__":
    main()

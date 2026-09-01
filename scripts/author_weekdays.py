"""Author episode: you check a calendar and live inside seven boxes."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9"

CHAPTERS = [
    """Tonight you will tap a calendar and see seven boxes in a row before the pattern repeats. Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday. Or Sunday first, if your phone was set by someone who thinks the week is a sermon with a weekend attached. You will not think of it as a vote. It will feel like weather. Here is the part that should bother you. The Moon takes about twenty nine and a half days to finish the cycle your apps politely call a month, and twenty nine point five does not divide cleanly into seven, which means the week is not a child of the sky you can see at night. So why does your life still snap into seven-day chunks as if the universe held a meeting? Because ancient Mesopotamia liked sevens, because Rome wanted a shared rest day on an imperial spreadsheet, because seven wandering lights in the sky got turned into words you still mutter before coffee, and because ISO and your kitchen wall never agreed on where the row should start. That is the whole plot. Your week is not astronomy. It is a grid that learned to look like a fact, and you check it every morning as if the grid had opinions about your laundry. The grid does. The grid is flattered. That is its job.""",
    """Start with the Moon, because the week stole a rhythm and then denied the theft. A lunar month is about twenty nine and a half days from new to new, depending on who is counting and whether they are selling you an app subscription. Divide that by seven and you get four weeks plus a leftover fraction that would wander around the year like a sock that never matches. Early farmers watched the Moon anyway. Planting, tides, fasting, feasts tied to phases. None of that required a neat seven-day belt that repeats forever without talking to the Moon. If your calendar still feels like it belongs to the sky, notice that the sky's loudest clock does not fit the belt you live in. A month is a phase story. A week is a counter story. Counters are useful when you need everyone in a city to show up on the same day without waiting for clouds. The Moon keeps time like a slow drum. The week keeps time like a metronome that forgot which song it was hired for. You can love both and still admit only one of them is wearing your phone's default skin.""",
    """Named corners, because a myth of one inventor is how a grid gets a halo it did not earn. In ancient Mesopotamia, especially under Babylonian practice, priests and scribes tracked time in layers: lunar months, festival cycles, market intervals, and a seven-day unit that shows up on cuneiform tablets and in later Jewish and Christian calendars as if it had always been there. The number seven was already busy. Seven was a completeness gesture in the region's math and ritual bookkeeping, not a telescope discovery. Sumerian and Babylonian astronomy was serious about the sky. It was also serious about administrative rhythm. A seven-day pulse let temple and town agree on when to rest, when to reckon, when to stop pretending the harvest could be scheduled by vibes alone. If you still treat seven as sacred math, file the paperwork separately from the physics. The week did not fall out of a lunar division. It fell out of a culture that liked sevens on clay and then exported the habit along trade routes and conquered calendars. Your row of boxes is a Mesopotamian souvenir that learned English.""",
    """This is the sky part people remember wrong. Before telescopes expanded the neighborhood, naked-eye watchers saw seven bright wanderers against the fixed stars: the Sun, the Moon, Mars, Mercury, Jupiter, Venus, and Saturn. Seven lights that moved. Seven names that moved with them. That is not proof the week was invented because someone counted planets on a Tuesday. It is proof that when humans already liked seven, the sky handed them a chorus that fit the costume. Saturn slow. Mercury quick. Venus bright. Mars reddish and alarming if you are in a mood. The Sun and Moon boss the obvious day and night. Jupiter fat with importance. Put that choir next to a seven-day counter and the labels start to feel inevitable, the way a rhyme feels inevitable after you have heard it in childhood. Inevitable is a feeling schedules train. The planets did not vote on your payroll cycle. They got drafted into it after the draft board had already chosen seven seats.""",
    """Watch the names travel. In Romance languages the weekday words still carry planetary luggage with the covers half off. French lundi from Luna, Monday moon day. Mardi from Mars. Mercredi from Mercury. Jeudi from Jove, Jupiter. Vendredi from Venus. English hides the same ancestry under Germanic gods and Norse replacements, which is how you get Tuesday from Tiw and Wednesday from Woden while Italian keeps singing Mercury on mercoledì. Spanish lunes, martes, miércoles, jueves, viernes. The weekend breaks the planet parade on Saturday and Sunday, Saturn and Sun in the English names, sabato and domenica carrying their own Latin skeletons. None of this means Romans invented the week on a whim last Thursday. It means once the seven-day grid existed, labeling days after the seven classical luminaries was a mnemonic that survived because mnemonics are cheap to teach and hard to unlearn. Your mouth still rehearses a planet roster when you ask if it is mercredi. The roster is not astronomy class. It is a sticker on a counter.""",
    """Rome enters as logistics, not as a sermon. Constantine, emperor, issued a Sunday law in three hundred twenty one of the common era that shows up in the Code of Justinian as a civil rest provision tied to the Sun day, dies Solis, on the imperial books. File the date. File the text as governance. The punchline is not that an emperor invented faith in a lamp. The punchline is that an empire with soldiers, courts, and market days needed a synchronized pause that could ride on an already circulating seven-day rhythm Christian communities were using alongside older customs. Spread is what laws do when they are written in capital letters and backed by tax collectors. Sunday as a protected day off traveled because Rome could stamp it, not because a calendar page is a confessional. If your week still feels Christian in the bones, notice how much of that feeling is actually a day-off contract wearing an old hat. Contracts can be cheerful. Cheerful is how a rest day stays in the century without looking like a memo from a desk you never saw.""",
    """This is the rehook. You think the week starts where your calendar starts. That is not astronomy either. That is a default setting with a flag on it. ISO eight six zero one, the international standard your spreadsheets pretend to respect, puts Monday at position one and Sunday at seven, which makes Sunday the end cap of the row. Many United States calendars, phones, and planners put Sunday first because church bulletins, television grids, and twentieth-century paper habits won the top-left square on this side of the Atlantic. Mexico, Canada, Japan, Israel, and plenty of others pick sides for their own reasons that are boring and local and perfectly real. Two honest answers to the same question: where does the loop begin? Neither answer is the Moon. Neither answer is Babylon. Both answers are interfaces. If you have ever felt a small rage when someone else's week view looks wrong, congratulations. You have been trained to treat a UI choice like morality. Morality is a word the grid uses when it wants you to stop asking who picked the first box.""",
    """So what did we trade? We traded a sky-tied month for a portable counter that survives lunar awkwardness. We traded local festival chaos for a seven-day pulse that payroll software can love. We traded planet names as poetry for planet names as habit. We gained a shared week that lets a shipping container, a school district, and a group chat agree on when Thursday is without negotiating with the Moon. That is not nothing. A nurse who knows her weekend is a real thing is living inside a political and administrative outcome, not a personality trait of Saturn. The trick is pretending the seven-box row is nature. It is not. It is Mesopotamian rhythm, a classical planet chorus, a Roman rest memo, Romance mnemonics, ISO defaults, and a wall calendar that puts Sunday on the left because someone in marketing liked the look. Deals can be rewritten. Some already were, quietly, when apps let you start weeks on Monday and called it a setting as if settings were not history with a toggle switch.""",
    """This is you. You will open the calendar again. Seven boxes will still be there. You will feel nothing, which is the victory. Put your finger on the row. That is not the Moon finishing a month. That is a clay counter, a wandering-light sticker book, a Sun-day law in three hundred twenty one, lundi and martes and Wednesday hiding Mercury under a Norse hat, ISO Monday on one screen and Sunday first on another, and a grid that taught you to treat a loop like a law. You are allowed to live inside the loop. You are allowed to hate Monday and still obey it. Just stop calling the seven natural, or inevitable, or proof that the sky voted. Tonight, when you check what day it is, look at the calendar like a contract with seven seats that never held an election. The seats are cheerful. The contract is the point. Know which box your app puts first. Know that the Moon did not pick it. Go when the row lets you. The row is cheerful. Cheerful is how a counter stays on the wall without looking like Mesopotamia holding a clipboard.""",
]

def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, five-second cadence)."""
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("seven-boxes", "You tap a calendar and see seven boxes in a row.", f"Stickman tapping a phone calendar with seven colored squares, {PAINT}"),
    ("mon-sun", "Monday through Sunday. Or Sunday first.", f"Two calendars side by side, one starts MON one starts SUN, {PAINT}"),
    ("not-a-vote", "You will not think of it as a vote.", f"Calendar labeled NOT A VOTE, shrugging stickman, {PAINT}"),
    ("feels-weather", "It feels like weather.", f"Calendar wearing a cloud costume, {PAINT}"),
    ("moon-month", "The Moon takes about twenty nine and a half days.", f"Moon cycle arrow 29.5 DAYS, {PAINT}"),
    ("no-clean-divide", "Twenty nine point five does not divide cleanly into seven.", f"Division 29.5 / 7 = MESSY, red X on neat fit, {PAINT}"),
    ("not-sky-child", "The week is not a child of the night sky.", f"Week belt disconnected from Moon, {PAINT}"),
    ("universe-meeting", "Why seven-day chunks as if the universe held a meeting?", f"Stickman at a UNIVERSE MEETING sign, seven chairs, {PAINT}"),
    ("mesopotamia-sevens", "Ancient Mesopotamia liked sevens.", f"Clay tablet with seven marks, MESOPOTAMIA tag, {PAINT}"),
    ("rome-rest", "Rome wanted a shared rest day on a spreadsheet.", f"Roman scroll labeled REST DAY spreadsheet, {PAINT}"),
    ("wandering-lights", "Seven wandering lights became words before coffee.", f"Seven planet icons above a coffee mug, {PAINT}"),
    ("iso-vs-wall", "ISO and your kitchen wall never agreed on the start.", f"ISO Monday vs wall calendar Sunday first, {PAINT}"),
    ("not-astronomy", "Your week is not astronomy.", f"ASTRONOMY stamp with red X, calendar wins, {PAINT}"),
    ("grid-as-fact", "A grid that learned to look like a fact.", f"Grid wearing a FACT mask, {PAINT}"),
    ("laundry-opinions", "The grid has opinions about your laundry.", f"Calendar pointing at laundry basket, {PAINT}"),
    ("grid-flattered", "The grid is flattered. That is its job.", f"Smiling calendar, FLATTERED badge, {PAINT}"),
    ("start-moon", "Start with the Moon. The week stole a rhythm.", f"Moon drum stolen by a seven-day belt, {PAINT}"),
    ("twenty-nine-half", "A lunar month is about twenty nine and a half days.", f"Moon phases in a 29.5 day loop, {PAINT}"),
    ("app-subscription", "Depending on who is counting and selling subscriptions.", f"Moon behind a paywall APP SUB, {PAINT}"),
    ("four-plus-fraction", "Four weeks plus a leftover fraction.", f"4 weeks + FRACTION sock, {PAINT}"),
    ("sock-year", "A fraction wandering the year like a mismatched sock.", f"Sock labeled FRACTION walking around a year circle, {PAINT}"),
    ("farmers-moon", "Farmers watched the Moon for planting and tides.", f"Stick farmer, Moon, crops and tide arrows, {PAINT}"),
    ("phases-feasts", "Fasting and feasts tied to phases.", f"Moon phases with FEAST and FAST tags, {PAINT}"),
    ("no-seven-belt", "None of that required a neat seven-day belt.", f"Seven-day belt with red X over Moon link, {PAINT}"),
    ("sky-belt-mismatch", "The sky's loudest clock does not fit your belt.", f"Big Moon clock vs small 7-day belt, mismatch, {PAINT}"),
    ("phase-story", "A month is a phase story.", f"Moon phases comic strip PHASE STORY, {PAINT}"),
    ("counter-story", "A week is a counter story.", f"Metronome labeled COUNTER STORY, {PAINT}"),
    ("same-day-city", "Counters get everyone in a city on the same day.", f"City stickmen synced on same calendar day, {PAINT}"),
    ("moon-drum", "The Moon keeps time like a slow drum.", f"Moon beating a slow drum, {PAINT}"),
    ("week-metronome", "The week keeps time like a forgetful metronome.", f"Seven-day metronome with question mark song, {PAINT}"),
    ("phone-skin", "Only one of them wears your phone's default skin.", f"Phone wearing a 7-day skin not a Moon skin, {PAINT}"),
    ("named-corners", "Named corners. One inventor is a halo the grid did not earn.", f"Halo on calendar, MYTH sticker, {PAINT}"),
    ("mesopotamia-layers", "Mesopotamia tracked months, festivals, markets, seven-day units.", f"Layered clay tablets MONTH FESTIVAL MARKET 7, {PAINT}"),
    ("cuneiform-seven", "Seven-day units show up on cuneiform tablets.", f"Cuneiform wedge marks in groups of seven, {PAINT}"),
    ("seven-busy", "The number seven was already busy.", f"Number 7 juggling many tags, {PAINT}"),
    ("completeness-gesture", "Seven was a completeness gesture, not a telescope find.", f"Seven as COMPLETE hand gesture, telescope with red X, {PAINT}"),
    ("babylon-sky", "Babylonian astronomy was serious about the sky.", f"Stick scribe star chart, BABYLON tag, {PAINT}"),
    ("admin-rhythm", "It was also serious about administrative rhythm.", f"Clipboard ADMIN RHYTHM next to stars, {PAINT}"),
    ("temple-town", "Temple and town agreed on when to rest and reckon.", f"Temple and town sharing a seven-day pulse, {PAINT}"),
    ("not-vibes-harvest", "Harvest could not be scheduled by vibes alone.", f"Harvest calendar vs VIBES cloud with red X, {PAINT}"),
    ("paperwork-physics", "File paperwork separately from physics.", f"PAPERWORK folder separate from PHYSICS folder, {PAINT}"),
    ("not-lunar-division", "The week did not fall out of a lunar division.", f"Week falling from clay not from Moon math, {PAINT}"),
    ("sevens-on-clay", "A culture that liked sevens on clay exported the habit.", f"Clay tablet exported on trade route arrows, {PAINT}"),
    ("souvenir-english", "Your row of boxes is a Mesopotamian souvenir that learned English.", f"Seven boxes with SOUVENIR tag and English labels, {PAINT}"),
    ("sky-part-wrong", "The sky part people remember wrong.", f"Wrong SKY MYTH thought bubble with red X, {PAINT}"),
    ("seven-wanderers", "Seven bright wanderers: Sun Moon Mars Mercury Jupiter Venus Saturn.", f"Seven planet sun moon icons in a row, {PAINT}"),
    ("seven-lights", "Seven lights that moved.", f"Moving lights among fixed stars, {PAINT}"),
    ("seven-names", "Seven names that moved with them.", f"Name tags orbiting seven lights, {PAINT}"),
    ("not-tuesday-proof", "Not proof someone counted planets on a Tuesday.", f"TUESDAY PLANET COUNT myth with red X, {PAINT}"),
    ("chorus-costume", "The sky handed a chorus that fit a seven costume.", f"Seven seats choir of planets, {PAINT}"),
    ("saturn-slow", "Saturn slow.", f"Saturn with a SLOW turtle, {PAINT}"),
    ("mercury-quick", "Mercury quick.", f"Mercury with speed lines QUICK, {PAINT}"),
    ("venus-bright", "Venus bright.", f"Bright Venus star, {PAINT}"),
    ("mars-alarm", "Mars reddish and alarming.", f"Red Mars with ALARM bell, {PAINT}"),
    ("sun-moon-boss", "Sun and Moon boss day and night.", f"Sun and Moon as bosses over day/night, {PAINT}"),
    ("jupiter-important", "Jupiter fat with importance.", f"Large Jupiter with IMPORTANT crown, {PAINT}"),
    ("inevitable-rhyme", "Labels feel inevitable like a childhood rhyme.", f"Planet labels as nursery rhyme, {PAINT}"),
    ("schedules-train", "Inevitable is a feeling schedules train.", f"Schedule train tracks labeled INEVITABLE, {PAINT}"),
    ("no-payroll-vote", "Planets did not vote on your payroll cycle.", f"Planets at ballot box with red X, {PAINT}"),
    ("seven-seats", "Drafted after the board chose seven seats.", f"Seven empty seats then planet stickers applied, {PAINT}"),
    ("names-travel", "Watch the names travel.", f"Weekday words on arrows traveling, {PAINT}"),
    ("romance-luggage", "Romance weekday words carry planetary luggage.", f"Suitcase with LUNDI MARDI tags, {PAINT}"),
    ("french-lundi", "French lundi from Luna. Mardi from Mars.", f"French LUNDI MARDI with Moon and Mars icons, {PAINT}"),
    ("mercredi-jeudi", "Mercredi from Mercury. Jeudi from Jupiter.", f"MERCREDI JEUDI with Mercury Jupiter, {PAINT}"),
    ("vendredi-venus", "Vendredi from Venus.", f"VENDREDI with Venus, {PAINT}"),
    ("english-norse", "English hides ancestry under Norse replacements.", f"Tiw Woden hiding under Tuesday Wednesday, {PAINT}"),
    ("italian-mercury", "Italian mercoledì still sings Mercury.", f"Italian MERCOLEDI with Mercury note, {PAINT}"),
    ("spanish-row", "Spanish lunes martes miércoles jueves viernes.", f"Spanish weekday row with planets, {PAINT}"),
    ("weekend-break", "Saturday and Sunday break the planet parade.", f"Planet parade stopping at SAT SUN, {PAINT}"),
    ("sabato-domenica", "Sabato and domenica carry Latin skeletons.", f"SABATO DOMENICA bone tags, {PAINT}"),
    ("not-last-thursday", "Romans did not invent the week on a whim last Thursday.", f"LAST THURSDAY INVENTION joke with red X, {PAINT}"),
    ("mnemonic-survived", "Planet labels were a cheap mnemonic that survived.", f"Mnemonic sticker book PLANETS on days, {PAINT}"),
    ("mercredi-mouth", "Your mouth rehearses a roster when you say mercredi.", f"Stickman mouth with planet roster, {PAINT}"),
    ("sticker-counter", "The roster is a sticker on a counter, not astronomy class.", f"Planet sticker on a seven-day counter, {PAINT}"),
    ("rome-logistics", "Rome enters as logistics, not as a sermon.", f"Roman scroll LOGISTICS not SERMON, {PAINT}"),
    ("constantine-321", "Constantine issued a Sunday law in three hundred twenty one.", f"Emperor nameplate CONSTANTINE 321 CE, Sunday sun icon, {PAINT}"),
    ("dies-solis", "Dies Solis on the imperial books.", f"Latin DIES SOLIS on ledger, {PAINT}"),
    ("justinian-code", "It shows up in the Code of Justinian as civil rest.", f"Code of Justinian book REST DAY, {PAINT}"),
    ("not-faith-lamp", "Punchline is not faith invented in a lamp.", f"LAMP FAITH MYTH with red X, {PAINT}"),
    ("empire-sync", "An empire needed a synchronized pause.", f"Empire map with SYNC PAUSE stamp, {PAINT}"),
    ("seven-day-rhythm", "Riding on a circulating seven-day rhythm.", f"Seven-day wheel already spinning, Rome stamp, {PAINT}"),
    ("spread-laws", "Spread is what laws do in capital letters.", f"CAPITAL LETTERS law spreading on map, {PAINT}"),
    ("tax-collectors", "Backed by tax collectors.", f"Tax collector stamp on Sunday rest paper, {PAINT}"),
    ("stamp-not-confessional", "Sunday traveled because Rome could stamp it.", f"Rubber stamp on calendar not confessional booth, {PAINT}"),
    ("day-off-contract", "Much of the feeling is a day-off contract in an old hat.", f"Contract paper wearing old hat, {PAINT}"),
    ("cheerful-rest", "Cheerful is how a rest day stays without looking like a memo.", f"Cheerful Sunday sun, hidden memo, {PAINT}"),
    ("rehook-start", "Rehook: you think the week starts where your calendar starts.", f"Stickman pointing at calendar start box, {PAINT}"),
    ("default-flag", "That is a default setting with a flag on it.", f"Settings toggle with tiny flag, {PAINT}"),
    ("iso-8601", "ISO eight six zero one puts Monday at one.", f"ISO 8601 row MON=1 SUN=7, {PAINT}"),
    ("sunday-end-cap", "Sunday is the end cap at seven.", f"Sunday box at end labeled 7, {PAINT}"),
    ("us-sunday-first", "Many United States calendars put Sunday first.", f"US calendar Sunday top-left, {PAINT}"),
    ("tv-grids", "Television grids and paper habits won the square.", f"TV grid and paper calendar fighting for corner, {PAINT}"),
    ("others-pick", "Mexico Canada Japan Israel pick sides for local reasons.", f"Small flags on different week-start calendars, {PAINT}"),
    ("where-loop", "Two honest answers: where does the loop begin?", f"Two calendars LOOP START arrows, {PAINT}"),
    ("neither-moon", "Neither answer is the Moon.", f"Moon with red X at loop start debate, {PAINT}"),
    ("neither-babylon", "Neither answer is Babylon.", f"Babylon clay tablet with red X at loop start, {PAINT}"),
    ("both-interfaces", "Both answers are interfaces.", f"UI buttons labeled INTERFACE, {PAINT}"),
    ("week-view-rage", "Rage when someone else's week view looks wrong.", f"Two stickmen angry at each other's calendar layout, {PAINT}"),
    ("ui-morality", "Trained to treat a UI choice like morality.", f"UI toggle stamped MORALITY with red X, {PAINT}"),
    ("first-box", "Morality is the grid stopping you asking who picked the first box.", f"FIRST BOX question blocked by grid, {PAINT}"),
    ("what-trade", "So what did we trade?", f"Trade scale OLD vs NEW week, {PAINT}"),
    ("portable-counter", "A portable counter that survives lunar awkwardness.", f"Seven-day counter surviving Moon fraction, {PAINT}"),
    ("payroll-pulse", "A seven-day pulse payroll software can love.", f"Payroll software hugging seven-day grid, {PAINT}"),
    ("poetry-to-habit", "Planet names went from poetry to habit.", f"Poetry book turning into habit sticker, {PAINT}"),
    ("shared-thursday", "Container, school, group chat agree on Thursday.", f"Ship school chat bubble all say THURSDAY, {PAINT}"),
    ("nurse-weekend", "A nurse's weekend is an administrative outcome.", f"Nurse with real WEEKEND badge not Saturn trait, {PAINT}"),
    ("not-nature", "The trick is pretending the row is nature.", f"NATURE mask on seven boxes with red X, {PAINT}"),
    ("mesopotamian-chorus", "Mesopotamian rhythm, planet chorus, Roman memo, ISO defaults.", f"Four icons clay planets scroll ISO, {PAINT}"),
    ("marketing-sunday", "Sunday left because marketing liked the look.", f"Marketing poster picks Sunday first, {PAINT}"),
    ("deals-rewritten", "Deals can be rewritten quietly in app settings.", f"App toggle REWRITE DEAL, {PAINT}"),
    ("history-toggle", "Settings are history with a toggle switch.", f"History book with toggle switch, {PAINT}"),
    ("this-is-you", "This is you. You will open the calendar again.", f"Stickman opening calendar again callback, {PAINT}"),
    ("seven-still", "Seven boxes will still be there.", f"Same seven boxes waiting, {PAINT}"),
    ("feel-nothing", "You will feel nothing. That is the victory.", f"Blank calm face at calendar victory, {PAINT}"),
    ("finger-row", "Put your finger on the row.", f"Finger on seven-day row, {PAINT}"),
    ("not-moon-month", "That is not the Moon finishing a month.", f"Moon month cycle with red X under finger, {PAINT}"),
    ("clay-counter", "A clay counter and a wandering-light sticker book.", f"Clay tablet plus planet sticker book, {PAINT}"),
    ("sun-law-321", "A Sun-day law in three hundred twenty one.", f"321 sun law scroll, {PAINT}"),
    ("norse-mercury", "Wednesday hides Mercury under a Norse hat.", f"Mercury under Woden hat on Wednesday, {PAINT}"),
    ("two-screens", "ISO Monday on one screen, Sunday first on another.", f"Two phones different week starts, {PAINT}"),
    ("loop-as-law", "A grid taught you to treat a loop like a law.", f"Loop circle stamped LAW, {PAINT}"),
    ("live-in-loop", "You are allowed to live inside the loop.", f"Stickman cozy inside seven-box loop, {PAINT}"),
    ("hate-monday", "Allowed to hate Monday and still obey it.", f"Hate Monday cloud but still on calendar, {PAINT}"),
    ("not-natural-seven", "Stop calling the seven natural or inevitable.", f"NATURAL INEVITABLE stamps with red X, {PAINT}"),
    ("sky-no-vote", "Not proof the sky voted.", f"Ballot box SKY VOTED with red X, {PAINT}"),
    ("seven-seats-election", "A contract with seven seats that never held an election.", f"Seven chairs NO ELECTION sign, {PAINT}"),
    ("cheerful-seats", "The seats are cheerful. The contract is the point.", f"Cheerful seven seats, CONTRACT spotlight, {PAINT}"),
    ("know-first-box", "Know which box your app puts first.", f"App highlight on first box WHICH START, {PAINT}"),
    ("moon-not-pick", "Know the Moon did not pick it.", f"Moon shrugging NOT MY PICK, {PAINT}"),
    ("go-when-row", "Go when the row lets you.", f"Stickman walking when calendar row opens, {PAINT}"),
    ("counter-clipboard", "Cheerful counter on the wall without Mesopotamia clipboard.", f"Wall calendar smiling, hidden clay clipboard, {PAINT}"),
    ("final-callback", "Seven boxes. Moon fraction. Your finger.", f"Final callback seven boxes Moon fraction stickman finger, {PAINT}"),
]


def _beats() -> list[tuple[str, str, str]]:
    """Stamp each row with a five-second mmss slug prefix."""
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
        title="Why Your Week Has Seven Days",
        description=(
            "Seven boxes feel like weather. The Moon does not divide by seven. "
            "Mesopotamia, seven wanderers, Romance names, Constantine in three "
            "hundred twenty one, ISO Monday versus Sunday first."
        ),
        tags=(
            "week",
            "calendar",
            "history",
            "days",
            "why",
            "monday",
            "sunday",
            "moon",
            "babylon",
            "planets",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="SEVEN DAYS?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Your Week Has Seven Days",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-weekdays.json"
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


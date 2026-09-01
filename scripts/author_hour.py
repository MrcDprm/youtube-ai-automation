"""Author episode: you glance at a circle and live inside sixty leftovers."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."

CHAPTERS = [
    """Tonight you will glance at a clock face and treat sixty as a fact, the way you treat a door as something that opens. Your wrist will expect twelve little ticks and a hand that visits each one as if the circle were physics. Here is the part that should bother you. Your body did not grow sixty-minute hours. Your lungs do not breathe in base sixty. The day you live in is a solar argument that refuses to factor cleanly, and yet your phone still slices it into chunks of sixty as if the Sun had voted on a spreadsheet. So why does an hour wear sixty minutes as if sixty were nature? Because Mesopotamian scribes liked a number that divides without tantrums, because Babylonian astronomers built star tables in sexagesimal columns, because Greek observers including Hipparchus and Claudius Ptolemy inherited that grid for angles and time, because medieval clockmakers needed gears that could agree with the sky on a town wall, and because a wristwatch in the twenty-first century is still a tiny museum of a clay habit you never signed. That is the whole plot. Your hour is not a heartbeat. It is a base-sixty souvenir that learned to look like a law, and you obey it every morning as if the law had opinions about your coffee. The law does. The law is flattered. That is its job. The circle did not vote. A scribe did, and then a gear train that taught your wrist the grid until the grid started calling itself sense. Sense is a word a sexagesimal column invented so a leftover would still feel like truth when the clay was gone.""",
    """Start with the clay, because the clock stole a counter and then sold it back as chrome. Long before gears, before minute hands, before a factory could stamp a dial, people in Mesopotamia were already counting in sixties. Sumerian scribes left early number tablets. Babylonian mathematics, as later scholars read it on cuneiform, treated sixty as a first-class citizen the way your calculator treats ten. Sexagesimal is not a cute nickname. It is a place-value system where the column to the left means sixty times the column to the right, the same trick decimal uses with tens, only wearing a Mesopotamian hat. If your hour still feels like it belongs to the sky, notice that the sky's loudest cycle, the day, does not politely factor into sixty without remainder. A day is a rotation story. An hour is a bookkeeping story. Bookkeeping is useful when you need a temple, a market, and a watchman to agree on when the gate closes without waiting for a cloud. The Sun keeps time like a slow drum. The sexagesimal grid keeps time like a metronome that forgot which song it was hired for. You can love both and still admit only one of them is wearing your phone's default skin.""",
    """Named corners, because a myth of one inventor is how a number gets a halo it did not earn. The sexagesimal habit is not a single eureka moment you can pin on one hero with a plaque. It is a layer cake of administrative need, astronomical patience, and a number that behaves nicely when you split it. Sixty divides evenly by two, three, four, five, six, ten, twelve, fifteen, twenty, and thirty. Try that with a prime like fifty nine and watch a scribe throw a stylus. Fractions matter when you are sharing grain, land, wages, and star positions across months that refuse to be tidy. Babylonian astronomers tracked lunar cycles, planetary wanderings, and eclipse possibilities in tables that reward a base with many factors. If you still treat sixty as sacred math, file the paperwork separately from the physics. Sixty did not fall out of a heartbeat. It fell out of a culture that needed a counter flexible enough for commerce and sky work on the same clay, and then exported the habit along trade routes and copied tables until the habit felt like weather. Your dial is a Mesopotamian souvenir that learned English and learned to tick.""",
    """This is the sky part people remember wrong. Greek astronomy did not invent sexagesimal from a blank slate. It inherited a grid already busy in Babylonian practice and then used it where precision wanted a fine mesh. Hipparchus, working in the second century before the common era, compiled star catalogues and geometric tools that lean on angular divisions compatible with sixties. Claudius Ptolemy, in the second century of the common era, wrote the Almagest, a star manual that treats celestial motion with the kind of fractional patience sexagesimal rewards. That is not proof the hour was invented because someone counted stars on a Tuesday. It is proof that when humans already liked sixty for angles, the sky handed them a chorus that fit the costume. Inevitable is a feeling schedules train. The planets did not vote on your wristwatch. They got drafted into a grid after the draft board had already chosen sixty seats. The seats were useful. Useful is how a leftover stays in the century without looking like a leftover.""",
    """Watch the number travel from clay to circle. Medieval Europe did not wake up one morning and decide sixty was cute. Clockmakers inherited a bundle: Roman daylight hours that could stretch and shrink with the season, church bells that marked prayer, water clocks and sand glasses that leaked honesty at their own pace, and then mechanical escapements that wanted a gear train with teeth that could repeat without shame. When public clocks spread across town squares in the late Middle Ages, they were civic furniture and a contract. Show up when the bell says, not when your shadow feels like noon. Dividing a circle into sixty parts for minutes, and grouping minutes into hours, rides the same sexagesimal comfort Babylonian scribes enjoyed: lots of clean fractions, lots of shared agreement. The punchline is not that a monk invented your commute. The punchline is that a town needed synchronized pulses and borrowed a grid old enough to feel eternal. Eternal is a word dials use when they want you to stop asking who picked the tick marks.""",
    """This is the rehook. You think the hour is a fact, the way gravity is a fact. The hour is a policy. In a modern day the policy is already on, because the alternative is trusting every meeting to negotiate with a sundial that moves with the season and a boss who thinks patience is a personality test. Sundials are honest. Sexagesimal grids are scalable. Scalable is how a schedule escapes the temple bench and becomes something a city can own in numbers. I am not calling you clumsy for liking a circle. I am un-naturing the tick. The tick is a clay column wearing a gear. The gear said rotation can be law. Law is a feeling when your eyes find twelve and sixty without remembering when they learned it. If you have ever tried to split an hour into thirds and felt relief that twenty minutes exists without a decimal mess, congratulations. You have been living inside Babylon's factor list. The relief is real. The relief is also a truce you never signed. A truce is not a Sun that voted. A truce is a spreadsheet with teeth.""",
    """Mass production did not invent the minute. It inventoried it. When the same watch face had to repeat across models, the sexagesimal dial became the part you could source, stamp, ship, and replace without translating a different base for every wrist. Railroads and telegraphs later wanted a shared minute so engines would miss each other and wires would agree, which is a different chapter about zones and shame, but the face on your wrist still carries the older grid underneath. Pocket watches became wristwatches after armies needed a shared minute within a trench, and the minute still arrived in packets of sixty because the packets were already culturally loud. A catalog is a quiet referendum. If your smartwatch has a circle and your history book has clay tablets, that gap is not evolution. It is inventory. Inventory is how the past wins a fight without filing a complaint. The past is cheerful. Cheerful is how a sexagesimal habit stays on a dial without looking like Mesopotamia holding a clipboard.""",
    """This is you, already, in the middle of the story. A Tuesday, a microwave, a timer that beeps in minutes you did not invent. You stare at the digits because boiling pasta would feel impossible without a grid, which is the most modern impossibility there is. None of this makes you mathematical by nature. It makes you a person born after town clocks and after wristwatches became real estate and after a circle learned to host alarms, calendars, and notifications that buzz. You can feel both in the same glance: relief that you can split an hour into halves and thirds without a calculator tantrum, and a tiny insult that a clay habit outlasted the clay. The relief is real. The insult is the sexagesimal column failing for a second in your imagination. You paid for a synchronized life with a base you never voted on. The base is cheerful. Cheerful is how a dial stays in the century without looking like a column. The dial still has a circle. The circle still feels like a fact. A fact used to be a factor list on a tablet. Your tablet is the rotation of a ring that forgot the clay. The rotation is cheerful. Cheerful is how a Babylon habit stays on a wrist without looking dusty.""",
    """A day is a pile of compromises with minutes attached. That sentence is rude and almost fair. Take the sexagesimal hour away and the schedule becomes a workshop puzzle nobody wins, or a decimal dial on every model until the thirds break. Star tables, gear ratios, assembly time, school bells: the hour is a diagram of how to split a day without fighting prime numbers, written by scribes you will not meet. You still glance. The glance is a vote for a grid that was sold as obvious. I am not telling you to hunt for clay tablets as a personality. I am telling you the personality was always the swap: a Sumerian counter, a Babylonian table, Hipparchus with a catalogue, Ptolemy with a manual, a town clock with teeth, a wristwatch with a crown, a phone that stopped listing sundials. The crowd is still on the dial. The crowd is you and a microwave treating a circle as a treaty. The treaty cannot see a workshop. The template can, if a human overrode it, which is a sentence assembly logs are not supposed to hide. A log is a promise in a cabinet you will never open. The cabinet is the real clock face. The face is a costume. Costume is how a sexagesimal grid stays on a Tuesday without looking like clay. The clay is still under the ring. The ring is still a permission slip you never signed. So what did we trade? We traded a sky-tied day for a portable counter that survives awkward fractions. We traded local bells for a minute pulse payroll software can love. We gained a shared hour that lets a train, a school district, and a group chat agree on when the meeting starts without negotiating with prime numbers. That is not nothing. A nurse who knows her break is twenty minutes is living inside an administrative outcome, not a personality trait of sixty. The trick is pretending the sexagesimal row is nature. It is not. It is Mesopotamian factors, a Greek star manual, a medieval gear train, a wristwatch crown, and a phone default you never changed. Deals can be rewritten. Some already were, quietly, when digital clocks let you show decimal seconds in a settings menu and called it a feature as if features were not history with a toggle switch. This is you. You will look at the clock again. Sixty will still be there. You will feel nothing, which is the victory. Look at the dial. That is not the Sun and it is not a heartbeat. That is a sexagesimal column, a Babylonian table habit, Hipparchus and Ptolemy wearing angles, a town square bell, a gear train that replaced leaking water, a wristwatch that replaced a pocket, and a circle that still owns your microwave so you will keep treating ticks as law. You are allowed to glance. You are allowed to hate waiting and still boil pasta. Just stop calling the hour natural, or inevitable, or proof that you are modern. Tonight, when the timer beeps, look at it like a leftover salute to a factor list that left the clay. The salute is cheerful. The beep is the point. Go when the ring lets you. Know which grid you are still obeying. The glance is cheerful. Cheerful is how a clock stays on the wall without looking like a scribe you never met.""",
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, five-second cadence)."""
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("glance-sixty", "Tonight you glance at a clock and treat sixty as a fact.", f"Stickman glancing at wall clock, SIXTY stamped FACT, {PAINT}"),
    ("twelve-ticks", "Your wrist expects twelve little ticks.", f"Wristwatch with twelve tick marks highlighted, {PAINT}"),
    ("body-no-sixty", "Your body did not grow sixty-minute hours.", f"Human body with red X over 60 MIN HOUR, {PAINT}"),
    ("solar-argument", "The day is a solar argument that refuses to factor cleanly.", f"Sun arguing with fraction mess, {PAINT}"),
    ("phone-slices", "Your phone slices the day into chunks of sixty.", f"Phone cutting day into 60 chunks, {PAINT}"),
    ("why-sixty", "Why does an hour wear sixty minutes as if sixty were nature?", f"Hour wearing 60 MIN NATURE costume, question mark, {PAINT}"),
    ("mesopotamian-scribes", "Mesopotamian scribes liked a number that divides without tantrums.", f"Scribe with calm number 60, no tantrum, {PAINT}"),
    ("babylonian-tables", "Babylonian astronomers built star tables in sexagesimal columns.", f"Star table in sexagesimal columns, BABYLON tag, {PAINT}"),
    ("hipparchus-ptolemy", "Greek observers Hipparchus and Claudius Ptolemy inherited that grid.", f"Two Greek labels Hipparchus and Ptolemy holding grid, {PAINT}"),
    ("medieval-gears", "Medieval clockmakers needed gears that agreed with the sky.", f"Medieval gears matching sky chart, {PAINT}"),
    ("wrist-museum", "A wristwatch is a tiny museum of a clay habit.", f"Wristwatch with tiny clay tablet inside, MUSEUM, {PAINT}"),
    ("not-heartbeat", "Your hour is not a heartbeat.", f"HEARTBEAT red X, clock wins, {PAINT}"),
    ("base-sixty-souvenir", "A base-sixty souvenir that learned to look like a law.", f"Souvenir tag BASE 60 wearing LAW mask, {PAINT}"),
    ("law-flattered", "The law is flattered. That is its job.", f"Smiling clock, FLATTERED badge, {PAINT}"),
    ("circle-no-vote", "The circle did not vote. A scribe did.", f"Circle with NO VOTE, scribe raising hand, {PAINT}"),
    ("gear-train", "Then a gear train taught your wrist the grid.", f"Gear train wrapping wrist, grid arrows, {PAINT}"),
    ("start-clay", "Start with the clay.", f"Clay tablet labeled START, {PAINT}"),
    ("clock-stole-counter", "The clock stole a counter and sold it back as chrome.", f"Counter stolen by chrome clock, {PAINT}"),
    ("before-gears", "Long before gears, before minute hands.", f"Timeline before gears minute hands, {PAINT}"),
    ("mesopotamia-sixties", "People in Mesopotamia were counting in sixties.", f"Map MESOPOTAMIA with 60 counters, {PAINT}"),
    ("sumerian-tablets", "Sumerian scribes left early number tablets.", f"Sumerian tablet with numbers, {PAINT}"),
    ("babylonian-math", "Babylonian mathematics treated sixty as a first-class citizen.", f"Number 60 on VIP pass FIRST CLASS, {PAINT}"),
    ("place-value-sixty", "A place-value system: left column means sixty times the right.", f"Two columns 1 and 60 place value arrows, {PAINT}"),
    ("decimal-trick", "The same trick decimal uses with tens, wearing a Mesopotamian hat.", f"Decimal 10 hat swap to Mesopotamian 60 hat, {PAINT}"),
    ("sky-vs-hour", "The sky's cycle does not factor cleanly into sixty.", f"Day cycle vs 60 red X neat fit, {PAINT}"),
    ("hour-bookkeeping", "An hour is a bookkeeping story.", f"Ledger labeled HOUR BOOKKEEPING, {PAINT}"),
    ("gate-closes", "Agree on when the gate closes without waiting for a cloud.", f"Town gate clock vs cloud, {PAINT}"),
    ("sun-drum", "The Sun keeps time like a slow drum.", f"Sun as slow drum, {PAINT}"),
    ("grid-metronome", "The grid keeps time like a metronome that forgot the song.", f"Metronome with question WHICH SONG, {PAINT}"),
    ("phone-skin", "Only one of them is wearing your phone's default skin.", f"Phone wearing sexagesimal skin, sun bare, {PAINT}"),
    ("named-corners", "Named corners. One inventor is a halo sixty did not earn.", f"Halo on 60, MYTH sticker, {PAINT}"),
    ("not-one-eureka", "Not a single eureka moment on one hero with a plaque.", f"Plaque ONE HERO red X, layer cake instead, {PAINT}"),
    ("layer-cake", "A layer cake of administrative need and astronomical patience.", f"Layer cake ADMIN SKY PATIENCE labels, {PAINT}"),
    ("sixty-divides", "Sixty divides evenly by two, three, four, five, six.", f"60 split into 2 3 4 5 6 clean pieces, {PAINT}"),
    ("ten-twelve-fifteen", "Ten, twelve, fifteen, twenty, and thirty.", f"Factors 10 12 15 20 30 checkmarks, {PAINT}"),
    ("fifty-nine-stylus", "Try fifty nine and watch a scribe throw a stylus.", f"Scribe throwing stylus at 59 fraction mess, {PAINT}"),
    ("fractions-grain", "Fractions matter when sharing grain, land, wages, star positions.", f"Grain land wages stars sharing pie chart, {PAINT}"),
    ("babylon-astronomers", "Babylonian astronomers tracked lunar cycles and eclipses.", f"Lunar cycle eclipse table Babylon, {PAINT}"),
    ("tables-reward", "Tables that reward a base with many factors.", f"Star table smiling at factor list, {PAINT}"),
    ("clay-export", "Exported the habit until the habit felt like weather.", f"Clay tablet exporting 60 on trade route, {PAINT}"),
    ("souvenir-english", "A Mesopotamian souvenir that learned English and learned to tick.", f"Souvenir 60 speaking English ticking, {PAINT}"),
    ("sky-part-wrong", "The sky part people remember wrong.", f"SKY PART WRONG sign, {PAINT}"),
    ("greek-inherited", "Greek astronomy inherited a grid already busy in Babylon.", f"Greek figure receiving grid from Babylon, {PAINT}"),
    ("hipparchus-stars", "Hipparchus compiled star catalogues in the second century BCE.", f"Hipparchus with star catalogue 2nd c BCE, {PAINT}"),
    ("angular-divisions", "Angular divisions compatible with sixties.", f"Circle divided in 60 angular marks, {PAINT}"),
    ("ptolemy-almagest", "Claudius Ptolemy wrote the Almagest in the second century CE.", f"Ptolemy holding ALMAGEST book 2nd c CE, {PAINT}"),
    ("not-tuesday-stars", "Not proof the hour was invented counting stars on Tuesday.", f"Calendar Tuesday stars red X causation, {PAINT}"),
    ("sky-chorus", "The sky handed them a chorus that fit the costume.", f"Sky planets as chorus in 60 costumes, {PAINT}"),
    ("planets-no-vote", "The planets did not vote on your wristwatch.", f"Planets at ballot box NO VOTE, {PAINT}"),
    ("sixty-seats", "The draft board had already chosen sixty seats.", f"Draft board with 60 empty seats, {PAINT}"),
    ("useful-leftover", "Useful is how a leftover stays without looking like one.", f"Leftover 60 in disguise USEFUL, {PAINT}"),
    ("clay-to-circle", "Watch the number travel from clay to circle.", f"Arrow clay tablet morphing to clock circle, {PAINT}"),
    ("medieval-not-cute", "Medieval Europe did not decide sixty was cute one morning.", f"Medieval town CUTE red X on 60, {PAINT}"),
    ("roman-hours", "Roman daylight hours could stretch and shrink with the season.", f"Stretchy sun hours Roman style, {PAINT}"),
    ("church-bells", "Church bells marked prayer.", f"Church bell PRAYER time, {PAINT}"),
    ("water-sand-clocks", "Water clocks and sand glasses leaked at their own pace.", f"Water clock and hourglass leaking, {PAINT}"),
    ("escapement-teeth", "Mechanical escapements wanted gear teeth that could repeat.", f"Escapement gear teeth repeating cleanly, {PAINT}"),
    ("public-clocks", "Public clocks spread across town squares.", f"Town square clock tower crowd, {PAINT}"),
    ("civic-furniture", "Civic furniture and a contract.", f"Clock as furniture plus CONTRACT paper, {PAINT}"),
    ("sixty-parts", "Dividing a circle into sixty parts for minutes.", f"Circle cut into 60 minute slices, {PAINT}"),
    ("scribe-comfort", "The same comfort Babylonian scribes enjoyed.", f"Scribe and clockmaker same comfort smile, {PAINT}"),
    ("not-monk-commute", "Not that a monk invented your commute.", f"Monk COMMUTE red X, town contract instead, {PAINT}"),
    ("synchronized-pulses", "A town needed synchronized pulses.", f"Town pulse wave syncing bells, {PAINT}"),
    ("eternal-tick", "Eternal is a word dials use about tick marks.", f"Dial saying ETERNAL hiding WHO PICKED, {PAINT}"),
    ("rehook-fact", "Rehook: you think the hour is a fact like gravity.", f"Hour vs gravity both labeled FACT, {PAINT}"),
    ("hour-policy", "The hour is a policy.", f"Hour stamped POLICY, {PAINT}"),
    ("sundial-season", "Trusting a sundial that moves with the season.", f"Sundial stretching with seasons, TRUST red X, {PAINT}"),
    ("boss-patience", "A boss who thinks patience is a personality test.", f"Boss clipboard PATIENCE TEST, {PAINT}"),
    ("sundials-honest", "Sundials are honest.", f"Sundial HONEST stamp, {PAINT}"),
    ("grid-scalable", "Sexagesimal grids are scalable.", f"Grid multiplying SCALABLE, {PAINT}"),
    ("city-in-numbers", "Scalable is how a schedule escapes the bench and a city owns it.", f"Bench to city clocks many, {PAINT}"),
    ("un-nature-tick", "Not calling you clumsy. Un-naturing the tick.", f"NATURE sticker peeling off clock tick, {PAINT}"),
    ("clay-wearing-gear", "The tick is a clay column wearing a gear.", f"Clay column inside gear costume, {PAINT}"),
    ("rotation-law", "The gear said rotation can be law.", f"Gear stamped ROTATION LAW, {PAINT}"),
    ("twelve-sixty-learned", "Eyes find twelve and sixty without remembering when they learned.", f"Eyes on dial blank memory bubble, {PAINT}"),
    ("thirds-relief", "Split an hour into thirds: twenty minutes without decimal mess.", f"Hour split in thirds 20 min each clean, {PAINT}"),
    ("babylon-factor", "Living inside Babylon's factor list.", f"Stickman inside factor list 2 3 4 5 6, {PAINT}"),
    ("truce-unsigned", "A truce you never signed.", f"TRUCE paper unsigned, {PAINT}"),
    ("spreadsheet-teeth", "A truce is a spreadsheet with teeth.", f"Spreadsheet with gear teeth, {PAINT}"),
    ("mass-inventoried", "Mass production did not invent the minute. It inventoried it.", f"INVENT red X, INVENTORIED check on dial shelf, {PAINT}"),
    ("same-watch-face", "The same watch face had to repeat across models.", f"Identical watch faces row, {PAINT}"),
    ("source-stamp-ship", "Source, stamp, ship, and replace without translating a different base.", f"Watch parts SOURCE STAMP SHIP boxes, {PAINT}"),
    ("railroad-minute", "Railroads wanted a shared minute so engines would miss each other.", f"Two trains sharing one minute hand, {PAINT}"),
    ("older-grid-under", "The face still carries the older grid underneath.", f"Smartwatch ghost of 60 grid under face, {PAINT}"),
    ("trench-wrist", "Armies needed a shared minute within a trench.", f"Soldier wristwatch in trench shared minute, {PAINT}"),
    ("packets-sixty", "The minute arrived in packets of sixty because the packets were loud.", f"60 packets labeled culturally loud, {PAINT}"),
    ("quiet-referendum", "A catalog is a quiet referendum.", f"Catalog voting booth QUIET REFERENDUM, {PAINT}"),
    ("clay-vs-smartwatch", "Smartwatch circle, history book clay tablets.", f"Smartwatch vs book clay gap, {PAINT}"),
    ("inventory-fight", "That gap is inventory. Inventory is how the past wins.", f"Inventory shelf beating sundial, {PAINT}"),
    ("this-is-you", "This is you. A Tuesday. A microwave. A timer in minutes you did not invent.", f"Stickman Tuesday microwave timer, {PAINT}"),
    ("stare-digits", "You stare at the digits because pasta needs a grid.", f"Stickman staring at timer digits pasta, {PAINT}"),
    ("not-math-nature", "None of this makes you mathematical by nature.", f"MATH NATURE stamp red X, {PAINT}"),
    ("born-after-clocks", "Born after town clocks and wristwatches as real estate.", f"Timeline town clock then wristwatch, {PAINT}"),
    ("circle-hosts", "A circle learned to host alarms, calendars, notifications.", f"Clock with alarm calendar buzz icons, {PAINT}"),
    ("relief-thirds", "Relief you split an hour into halves and thirds easily.", f"Hour halves thirds happy stickman, {PAINT}"),
    ("insult-clay-gone", "A tiny insult that a clay habit outlasted the clay.", f"Clay ghost outlasting broken tablet, insult cloud, {PAINT}"),
    ("never-voted", "You paid for a synchronized life with a base you never voted on.", f"Receipt BASE 60 never voted, {PAINT}"),
    ("cheerful-dial", "Cheerful is how a dial stays without looking like a column.", f"Smiling clock face hiding column, {PAINT}"),
    ("fact-was-factors", "A fact used to be a factor list on a tablet.", f"FACT equals factor list on tablet, {PAINT}"),
    ("ring-forgot-clay", "Your ring forgot the clay.", f"Wristwatch ring, clay forgotten ghost, {PAINT}"),
    ("compromises-minutes", "A day is compromises with minutes attached.", f"Compromise stack with minutes on top, {PAINT}"),
    ("take-hour-away", "Take the sexagesimal hour away and the schedule becomes a puzzle.", f"Schedule puzzle pieces no 60, {PAINT}"),
    ("decimal-thirds-break", "Or a decimal dial until the thirds break.", f"Decimal dial thirds breaking, {PAINT}"),
    ("diagram-split", "Star tables, gear ratios, school bells: split a day without prime fights.", f"Diagram split day no prime fight, {PAINT}"),
    ("glance-vote", "The glance is a vote for a grid sold as obvious.", f"Glance voting OBVIOUS grid, {PAINT}"),
    ("not-tablet-personality", "Not telling you to hunt clay tablets as a personality.", f"Tablet personality hat red X, {PAINT}"),
    ("swap-personality", "The personality was the swap: Sumer, Babylon, Hipparchus, Ptolemy, town clock, wrist.", f"Six icons Sumer Babylon Hipparchus Ptolemy clock wrist, {PAINT}"),
    ("crowd-dial", "The crowd is still on the dial.", f"Many stickmen on one clock face, {PAINT}"),
    ("circle-treaty", "You and a microwave treating a circle as a treaty.", f"Microwave and stickman circle treaty paper, {PAINT}"),
    ("treaty-blind", "The treaty cannot see a workshop.", f"Treaty blindfold workshop behind, {PAINT}"),
    ("cabinet-face", "A log in a cabinet you will never open. The real clock face.", f"Locked cabinet LOG real clock face, {PAINT}"),
    ("clay-under-ring", "The clay is still under the ring.", f"Clay ghost under watch ring, {PAINT}"),
    ("what-trade", "So what did we trade?", f"Trade scale clay grid vs modern clock, {PAINT}"),
    ("sky-tied-day", "A sky-tied day for a portable counter surviving awkward fractions.", f"Sun tied day vs portable 60 counter, {PAINT}"),
    ("minute-pulse", "Local bells for a minute pulse payroll software can love.", f"Payroll software hugging minute pulse, {PAINT}"),
    ("shared-hour", "A shared hour for trains, schools, and group chats.", f"Train school chat agreeing on hour, {PAINT}"),
    ("nurse-twenty", "A nurse who knows her break is twenty minutes.", f"Nurse break 20 MIN not personality of 60, {PAINT}"),
    ("not-nature-row", "Stop pretending the sexagesimal row is nature.", f"NATURE stamp red X on 60 row, {PAINT}"),
    ("deals-rewritten", "Deals can be rewritten quietly in settings menus.", f"Settings toggle history with switch, {PAINT}"),
    ("look-again", "You will look at the clock again. Sixty will still be there.", f"Callback stickman looking at clock 60, {PAINT}"),
    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at clock, {PAINT}"),
    ("not-sun-heartbeat", "That is not the Sun and it is not a heartbeat.", f"Sun and HEARTBEAT red X, dial center, {PAINT}"),
    ("named-stack", "Sexagesimal column, Babylon table, Hipparchus, Ptolemy, town bell, gear, wrist.", f"Stack of named icons ending in wrist, {PAINT}"),
    ("microwave-law", "A circle that owns your microwave so ticks stay law.", f"Microwave obeying clock LAW stamp, {PAINT}"),
    ("allowed-glance", "You are allowed to glance. Allowed to hate waiting and still boil pasta.", f"Glance ok hate waiting still pasta, {PAINT}"),
    ("not-natural", "Stop calling the hour natural.", f"NATURAL stamp red X on hour, {PAINT}"),
    ("not-inevitable", "Not inevitable. Not proof you are modern.", f"INEVITABLE MODERN stamps red X, {PAINT}"),
    ("leftover-clay", "A leftover salute to a factor list that left the clay.", f"Salute to factor list leaving clay, {PAINT}"),
    ("beep-point", "The salute is cheerful. The beep is the point.", f"Cheerful salute on microwave BEEP, {PAINT}"),
    ("know-grid", "Go when the ring lets you. Know which grid you are still obeying.", f"Stickman leaving, grid labeled which, {PAINT}"),
    ("glance-cheerful", "The glance is cheerful. Cheerful is how a clock stays without looking like a scribe.", f"Smiling glance at clock, scribe ghost hidden, {PAINT}"),
    ("final-callback", "Clay. Stars. Your wrist.", f"Final callback clay stars label wrist on clock, {PAINT}"),
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
        title="Why an Hour Has Sixty Minutes",
        description=(
            "Sixty minutes feels obvious. Mesopotamian scribes counted in "
            "sexagesimal. Hipparchus and Ptolemy inherited the grid. Medieval "
            "gears and modern wristwatches still run on Babylon's factor list."
        ),
        tags=(
            "time",
            "hour",
            "minute",
            "sexagesimal",
            "babylon",
            "history",
            "why",
            "clock",
            "astronomy",
            "hipparchus",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="SIXTY?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why an Hour Has Sixty Minutes",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-hour.json"
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

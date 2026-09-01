"""Author episode: you stab dinner with a fork and treat the tines as table law."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."

CHAPTERS = [
    """Tonight you will stab a plate with a fork and treat the tines as table law. Your hand will find four metal prongs as if the fork were always the adult option. Here is the part that should bother you. The first diners at your table did not agree. Many of them tore bread with fingers, shared knives, and let the food come to the mouth without a middleman made of steel. So why does your wrist lift a fork as if lifting were physics? Because Italian courts refined the pronged tool long before English travelers stopped laughing at it, because Catherine de Medici's entourage helped spread fork habits into French service in the fifteen thirties, because Thomas Coryat wrote home about Italian forks in sixteen eleven and made England notice, because etiquette books turned a luxury into a lesson, and because factories learned that stamped tines are easier to ship than a lecture about clean hands. That is the whole plot. Your fork is not nature by birth. It is a leftover finger habit wearing a metal costume with four opinions. You still eat. The eat is flattered. That is its job. The plate did not vote. A table custom did, and then a fork that taught your wrist the stab until the stab started calling itself sense. Sense is a word tines invented so dinner would still feel like law when the fingers left the story.""",
    """Start with the finger, because the fork stole a grab and then sold it back as manners. Before pronged tools sat beside every plate, before four tines became the boring default, before a salad could be a small war you win with stainless steel, eating was a negotiation with heat and sauce you could not outsource. Early diners shared. Early hosts offered bread as a wipe. When forks arrived at wealthy tables, they were honest and late. A fork that says pierce here is a finger wearing armor. It does not say the bite is polite until the room agrees the room is watching. If your fork still feels like the only adult option, notice that the adult option started as a court habit dragged onto a table that was not a lecture hall. The table did not offer a sermon. The finger still wanted the food until the finger got tired of being the only transport. The finger was not a miracle. It was logistics.""",
    """Named corners, because a myth of one queen is how a fork gets a halo it did not earn. The dinner fork is not a single eureka moment you can pin on one wedding in one year. It is a layer cake of Byzantine prongs, Italian refinement, French service, English mockery, and a stamped utensil that behaved nicely when you needed to sell a place setting in a catalog. Catherine de Medici did not invent the fork in a laboratory, but her marriage to Henry the second in fifteen thirty-three is a named corner where Italian table tools traveled with a court that already loved ceremony. Thomas Coryat's Coryat's Crudities in sixteen eleven is a named English witness who saw forks in Italy and wrote home like a man reporting a scandal that would become normal. Louis the fourteenth's court helped turn separate courses into separate tools. If you still treat the fork as sacred silver, file the etiquette book separately from the bite. Your tines are a traveler complaint wearing centuries of table homework.""",
    """Watch the finger leave the plate, because a horizontal table of guests needed a tool that did not require every diner to share one knife like a treaty. Early eating tricks were honest and exhausting. Tear with hands. Wipe with bread. Pass the blade. Repeat. A fork is a small insult to shared germs with a large gift to the host. The tines grip food. The wrist repeats. The fork says route the bite here without asking the sauce to negotiate with every thumb. I am not giving you a list of firsts. I am pointing at the swap. We took a finger that said grab this and we replaced it with prongs that said pierce and lift here. Pierce is easier to teach in an etiquette book. Pierce is easier to stamp in a factory line. Pierce is easier to repeat when the dining room grows. The line is the real inventor. The line does not care about your nostalgia for a shared knife. The line cares about tines that match and tables that stay inside the lesson plan.""",
    """This is the rehook. You think the fork is a fact, the way a plate is a fact. The fork is a policy. In a modern dining room the policy is already on, because the alternative is trusting every guest to handle hot food with fingers while a host watches for sauce on cuffs. Fingers are honest. Forks are scalable. Scalable is how a court habit escapes the palace and becomes something a department store can own in numbers. I am not calling you prissy for liking a fork. I am un-naturing the tines. The tines are a finger wearing a metal lesson. The lesson said shared blades can be law. Law is a feeling when your wrist lifts a fork without remembering when it learned the lift. If you have ever eaten somewhere with only a spoon and a knife, even a camp meal with no prongs, you know the fork is not physics. It is a compromise that won a table vote. A vote is not a cooking show. A vote is a spreadsheet with silver plate, stainless stamp, and a wedding registry.""",
    """Watch the stamp travel. Mass production did not invent hunger. It inventoried the answer. When the same place setting had to repeat across a middle-class table, the fork became the part you could stamp, plate, ship, and replace without translating a court ritual for every dining room. Stainless steel, four tines, salad fork, dessert fork: decades later the drawer could multiply, a useful chapter about alloys and catalogs, not the origin story of the prong itself. Do not make tonight a etiquette war about which nation won the politest bite. Make it about the object: metal, tine, wrist, repeat. A catalog is a quiet referendum. If your drawer has six forks and your history book has a shared knife, that gap is not evolution. It is inventory. Inventory is how the past loses a fight without filing a complaint.""",
    """This is you, already, in the middle of the story. A Wednesday, a restaurant table, a lift you have performed a thousand times without thanking a traveler who got mocked for writing home. You stab a leaf because tearing would feel reckless without tines, which is the most modern impossibility there is. None of this makes you fussy by nature. It makes you a person born after Coryat's joke aged into habit and after drawers learned specialization and after a fork learned to host courses that multiply. You can feel both in the same motion: relief that you do not have to negotiate sauce with a thumb, and a tiny insult that a court habit won a wrist slot. The relief is real. The insult is the finger failing for a second in your imagination. You paid for table peace with a tool you never voted on. The tool is cheerful. Cheerful is how a fork stays in the century without looking like a finger.""",
    """A table is a pile of compromises with a utensil drawer attached. That sentence is rude and almost fair. Take the fork away and the meal becomes a workshop puzzle nobody wins, or a host who becomes a knife broker until the roast cools. Tine length, sauce grip, course count, replacement stamp: the fork is a diagram of how to eat without sending the whole shirt into the laundry story, written by someone you will not meet. You still lift. The lift is a vote for prongs that were sold as obvious. I am not telling you to hunt for fingers as a personality. I am telling you the personality was always the swap: a grab, a shared blade, a traveler joke, a French service line, a registry sheet that forgot your bread wipe. The crowd is still at the table. The crowd is you and a wedding fleet treating a fork as a treaty. So what did we trade? We traded a finger that told the truth about heat for a tool that could be stamped, plated, and taught. That tooling is real help: fewer shared blades, a guest who keeps cuffs clean, a bite you can route with a drawer. Help can be a miracle and still be a part number. We also gained a myth that the fork is nature and the tines are the only adult table. We kept the finger and called it casual. We kept the court and called it history. Both can be true and still not be a reason to forget the fork is a policy that learned manners.""",
    """This is you. You will set the fork down. The tines will still be there. You will feel nothing, which is the victory. Look at the prongs. That is not the sky and it is not a cooking hero. That is a finger, a shared knife, a fifteen thirty-three court caravan, a sixteen eleven travel book that made England blush, a molded stamp that replaced a grab, a registry photograph that replaced a bread wipe, a brief later chapter about salad forks if you must, and a tool that still owns your wrist so you will keep treating metal as law. You are allowed to lift. You are allowed to hate sauce season and still dine. Just stop calling the fork natural, or inevitable, or proof that you are civilized. Tonight, when the tines catch the plate light, look at them like a leftover salute to a finger that left the bite. The salute is cheerful. The stab is the point. Eat when the room lets you. Know which prong you are still obeying.""",
]


def _stamp(index: int) -> str:
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("stab-plate", "Tonight you stab a plate with a fork and treat the tines as table law.", f"Stickman stabbing plate with fork TABLE LAW, {PAINT}"),
    ("hand-tines", "Your hand finds four metal prongs as if the fork were always the adult option.", f"Hand on four tines ADULT OPTION question mark, {PAINT}"),
    ("fork-physics", "As if lifting a fork were physics.", f"Fork lift stamped PHYSICS question mark, {PAINT}"),
    ("first-no-agree", "The first diners at your table did not agree.", f"Early diner shaking head at fork, {PAINT}"),
    ("fingers-knives", "They tore bread with fingers and shared knives.", f"Fingers bread shared KNIVES labels, {PAINT}"),
    ("why-wrist-lift", "Why does your wrist lift a fork as if lifting were physics?", f"Wrist lifting fork PHYSICS stamp, {PAINT}"),
    ("italian-courts", "Italian courts refined the pronged tool before English travelers stopped laughing.", f"Italian court refining FORK prongs, {PAINT}"),
    ("catherine-1533", "Catherine de Medici helped spread fork habits into French service in fifteen thirty-three.", f"Catherine de Medici 1533 FORK HABITS caravan, {PAINT}"),
    ("coryat-1611", "Thomas Coryat wrote home about Italian forks in sixteen eleven.", f"Thomas Coryat 1611 Coryat Crudities travel book, {PAINT}"),
    ("etiquette-books", "Etiquette books turned a luxury into a lesson.", f"Etiquette book LUXURY to LESSON arrow, {PAINT}"),
    ("stamped-tines", "Stamped tines are easier to ship than a lecture about clean hands.", f"Stamped tines vs lecture CLEAN HANDS, {PAINT}"),
    ("not-nature", "Your fork is not nature by birth.", f"NATURE BY BIRTH stamp red X on fork, {PAINT}"),
    ("finger-costume", "A leftover finger habit wearing a metal costume with four opinions.", f"Finger morphing into fork COSTUME four tines, {PAINT}"),
    ("eat-flattered", "The eat is flattered. That is its job.", f"Smiling fork FLATTERED badge, {PAINT}"),
    ("plate-no-vote", "The plate did not vote. A table custom did.", f"Plate NO VOTE table custom raising hand, {PAINT}"),
    ("stab-sense", "The stab taught your wrist until it called itself sense.", f"Wrist word SENSE after fork stab, {PAINT}"),
    ("start-finger", "Start with the finger.", f"Finger labeled START, {PAINT}"),
    ("fork-stole-grab", "The fork stole a grab and sold it back as manners.", f"Finger grab stolen by fork MANNERS, {PAINT}"),
    ("before-prongs", "Before pronged tools sat beside every plate, before four tines became default.", f"Timeline before four tine default, {PAINT}"),
    ("heat-sauce", "Eating was a negotiation with heat and sauce you could not outsource.", f"Negotiation with HEAT SAUCE no outsource, {PAINT}"),
    ("diners-shared", "Early diners shared. Early hosts offered bread as a wipe.", f"Diners sharing bread WIPE label, {PAINT}"),
    ("forks-late", "When forks arrived at wealthy tables, they were honest and late.", f"Fork at wealthy table HONEST LATE labels, {PAINT}"),
    ("pierce-here", "A fork that says pierce here is a finger wearing armor.", f"PIERCE HERE finger wearing armor fork, {PAINT}"),
    ("room-watching", "The bite is polite until the room agrees the room is watching.", f"Room WATCHING polite bite agreement, {PAINT}"),
    ("court-habit", "A court habit dragged onto a table not a lecture hall.", f"Court habit on table NOT LECTURE HALL, {PAINT}"),
    ("finger-wanted-food", "The finger still wanted the food until the finger got tired.", f"Finger speech bubble WANT FOOD, {PAINT}"),
    ("finger-transport", "The finger got tired of being the only transport.", f"Tired finger ONLY TRANSPORT label, {PAINT}"),
    ("not-miracle", "The finger was not a miracle. It was logistics.", f"LOGISTICS stamp on finger not miracle, {PAINT}"),
    ("named-corners", "Named corners. One queen is a halo the fork did not earn.", f"Halo on fork MYTH sticker, {PAINT}"),
    ("not-one-wedding", "The dinner fork is not one eureka moment at one wedding.", f"Wedding eureka red X many layers, {PAINT}"),
    ("layer-cake", "Byzantine prongs, Italian refinement, French service, English mockery.", f"Layer cake Byzantine Italian French English, {PAINT}"),
    ("catherine-corner", "Catherine de Medici marriage fifteen thirty-three is a named corner.", f"1533 marriage FORK CORNER signpost, {PAINT}"),
    ("coryat-witness", "Coryat's Crudities is a named English witness who wrote home.", f"Coryat witness writing home about fork, {PAINT}"),
    ("louis-courses", "Louis the fourteenth court helped turn courses into separate tools.", f"Louis XIV court separate COURSES tools, {PAINT}"),
    ("habit-part-number", "The quiet way a habit becomes a part number.", f"Habit becoming PART NUMBER arrow, {PAINT}"),
    ("traveler-complaint", "Your tines are a traveler complaint wearing centuries of table homework.", f"Traveler complaint wearing homework coat, {PAINT}"),
    ("finger-leaves", "Watch the finger leave the plate.", f"Finger walking away from plate, {PAINT}"),
    ("shared-knife", "A table that did not require every diner to share one knife like a treaty.", f"Shared knife TREATY red X fork wins, {PAINT}"),
    ("tear-wipe-pass", "Tear with hands. Wipe with bread. Pass the blade. Repeat.", f"Three panel TEAR WIPE PASS REPEAT, {PAINT}"),
    ("small-insult", "A fork is a small insult to shared germs with a large gift to the host.", f"Fork insulting shared germs gift to host, {PAINT}"),
    ("tines-grip", "The tines grip food. The wrist repeats.", f"Tines grip food wrist repeats, {PAINT}"),
    ("route-bite", "The fork says route the bite here without sauce negotiating every thumb.", f"ROUTE BITE HERE no thumb negotiate, {PAINT}"),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", f"FIRSTS red X SWAP arrow, {PAINT}"),
    ("finger-grab", "We took a finger that said grab this.", f"Finger speech bubble GRAB THIS, {PAINT}"),
    ("prongs-pierce", "We replaced it with prongs that said pierce and lift here.", f"Prongs PIERCE LIFT HERE arrows, {PAINT}"),
    ("pierce-etiquette", "Pierce is easier to teach in an etiquette book.", f"Etiquette book teaching PIERCE checkmark, {PAINT}"),
    ("pierce-stamp", "Pierce is easier to stamp in a factory line.", f"Factory stamping fork tines PIERCE, {PAINT}"),
    ("line-inventor", "The line is the real inventor.", f"Factory line labeled REAL INVENTOR, {PAINT}"),
    ("knife-nostalgia", "The line does not care about nostalgia for a shared knife.", f"Shared knife nostalgia red X, {PAINT}"),
    ("rehook-fact", "You think the fork is a fact, the way a plate is a fact.", f"Fork vs plate both labeled FACT, {PAINT}"),
    ("fork-policy", "The fork is a policy.", f"POLICY stamp on fork, {PAINT}"),
    ("sauce-cuffs", "Trusting every guest to handle hot food while a host watches sauce on cuffs.", f"Hot food sauce on cuffs red X fork wins, {PAINT}"),
    ("fingers-honest", "Fingers are honest. Forks are scalable.", f"FINGERS honest FORKS scalable scales, {PAINT}"),
    ("un-naturing", "I am un-naturing the tines.", f"Fork NATURAL stamp peeling off, {PAINT}"),
    ("finger-lesson", "The tines are a finger wearing a metal lesson.", f"Finger wearing metal LESSON coat, {PAINT}"),
    ("blade-law", "The lesson said shared blades can be law.", f"Shared blades CAN BE LAW stamp, {PAINT}"),
    ("spoon-knife-only", "If you ate somewhere with only a spoon and a knife.", f"Camp meal spoon knife no fork, {PAINT}"),
    ("not-physics", "You know the fork is not physics.", f"PHYSICS stamp red X on fork, {PAINT}"),
    ("table-vote", "A compromise that won a table vote.", f"Dining table voting fork wins, {PAINT}"),
    ("spreadsheet-silver", "A vote is a spreadsheet with silver plate and a wedding registry.", f"Spreadsheet silver registry catalog, {PAINT}"),
    ("stamp-travel", "Watch the stamp travel.", f"Metal stamp traveling across frame, {PAINT}"),
    ("inventoried-answer", "Mass production inventoried the answer.", f"Factory inventory forks shelf, {PAINT}"),
    ("stamp-ship-replace", "Stamp, plate, ship, replace without a court ritual.", f"STAMP PLATE SHIP REPLACE conveyor, {PAINT}"),
    ("stainless-four", "Stainless steel, four tines, salad fork: a later chapter.", f"Stainless four tines LATER CHAPTER, {PAINT}"),
    ("no-etiquette-war", "Do not make tonight an etiquette war about which nation won.", f"ETIQUETTE WAR stamp red X, {PAINT}"),
    ("object-metal", "Make it about the object: metal, tine, wrist, repeat.", f"METAL TINE WRIST REPEAT icons, {PAINT}"),
    ("catalog-referendum", "A catalog is a quiet referendum.", f"Quiet catalog REFERENDUM whisper, {PAINT}"),
    ("drawer-vs-knife", "Your drawer has six forks and your history book has a shared knife.", f"Six forks vs shared knife gap, {PAINT}"),
    ("inventory-fight", "Inventory is how the past loses a fight without filing a complaint.", f"Past losing fight INVENTORY filing cabinet, {PAINT}"),
    ("this-is-you", "This is you, already, in the middle of the story.", f"Stickman labeled THIS IS YOU restaurant table, {PAINT}"),
    ("wednesday-lift", "A Wednesday, a restaurant table, a lift without thanking a traveler.", f"Wednesday restaurant lift no thank traveler, {PAINT}"),
    ("stab-leaf", "You stab a leaf because tearing would feel reckless.", f"Stabbing salad leaf RECKLESS without fork, {PAINT}"),
    ("modern-impossibility", "The most modern impossibility there is.", f"MODERN IMPOSSIBILITY stamp on lift, {PAINT}"),
    ("after-coryat", "Born after Coryat's joke aged into habit.", f"Timeline after Coryat joke became habit, {PAINT}"),
    ("drawer-specialize", "After drawers learned specialization.", f"Drawer learning SPECIALIZATION morph, {PAINT}"),
    ("courses-multiply", "After a fork learned to host courses that multiply.", f"Fork hosting multiplying courses, {PAINT}"),
    ("relief-insult", "Relief you do not negotiate sauce with a thumb, insult a court habit won.", f"Relief checkmark insult court habit wins, {PAINT}"),
    ("finger-imagination", "The finger failing for a second in your imagination.", f"Ghost finger failing imagination, {PAINT}"),
    ("never-voted", "You paid for table peace with a tool you never voted on.", f"Table peace NEVER VOTED stamp, {PAINT}"),
    ("cheerful-fork", "Cheerful is how a fork stays without looking like a finger.", f"Smiling fork finger costume hidden, {PAINT}"),
    ("compromises-drawer", "A table is a pile of compromises with a utensil drawer attached.", f"Table pile COMPROMISES drawer bolted, {PAINT}"),
    ("take-fork-away", "Take the fork away and the meal becomes a workshop puzzle.", f"Meal puzzle nobody wins no fork, {PAINT}"),
    ("tine-geometry", "Tine length, sauce grip, course count, replacement stamp.", f"TINE SAUCE COURSE STAMP labels, {PAINT}"),
    ("diagram-bite", "The fork is a diagram of how to eat without the laundry story.", f"Fork diagram BITE without laundry story, {PAINT}"),
    ("lift-vote", "The lift is a vote for prongs sold as obvious.", f"Lift voting PRONGS OBVIOUS, {PAINT}"),
    ("personality-swap", "The personality was always the swap.", f"SWAP arrow finger to fork, {PAINT}"),
    ("grab-blade", "A grab, a shared blade.", f"Grab and shared blade icons, {PAINT}"),
    ("joke-service", "A traveler joke, a French service line.", f"Traveler joke French service icons, {PAINT}"),
    ("registry-forgot", "A registry sheet that forgot your bread wipe.", f"Registry sheet forgetting bread wipe, {PAINT}"),
    ("treaty-wedding", "You and a wedding fleet treating a fork as a treaty.", f"Wedding fleet fork TREATY handshake, {PAINT}"),
    ("what-we-traded", "We traded a finger that told the truth about heat.", f"Finger truth HEAT traded away, {PAINT}"),
    ("stamped-taught", "For a tool that could be stamped, plated, and taught.", f"Stamped plated taught fork on line, {PAINT}"),
    ("real-help", "Real help: fewer shared blades, cuffs stay clean.", f"Fewer shared blades CLEAN CUFFS, {PAINT}"),
    ("miracle-part-number", "Help can be a miracle and still be a part number.", f"MIRACLE and PART NUMBER both true, {PAINT}"),
    ("myth-nature", "A myth that the fork is nature and tines are the only adult table.", f"MYTH NATURE ADULT TABLE stamps, {PAINT}"),
    ("finger-casual", "We kept the finger and called it casual.", f"Finger labeled CASUAL picnic, {PAINT}"),
    ("court-history", "We kept the court and called it history.", f"Court labeled HISTORY museum, {PAINT}"),
    ("policy-manners", "The fork is a policy that learned manners.", f"Policy fork in polite bow tie, {PAINT}"),
    ("byzantine-prong", "There was an era when the Byzantine prong was already old news.", f"Byzantine prong OLD NEWS label, {PAINT}"),
    ("english-mockery", "English mockery aged into drawer inventory.", f"English mockery aging into DRAWER, {PAINT}"),
    ("drawer-real-estate", "The drawer is real estate with a piercing department.", f"Drawer REAL ESTATE piercing department, {PAINT}"),
    ("table-separate", "Table peace arrived as a separate homework assignment.", f"Table peace SEPARATE HOMEWORK label, {PAINT}"),
    ("restaurant-line", "The restaurant line taught the fork what waiting means.", f"Restaurant line teaching WAITING, {PAINT}"),
    ("registry-photograph", "A registry photograph learned to sell.", f"Registry photograph learned to SELL, {PAINT}"),
    ("bite-before-agree", "The bite wanted speed before the room agreed.", f"Bite wanting speed room disagreeing, {PAINT}"),
    ("four-tine-policy", "Four tines is a table policy written in metal.", f"Four tines TABLE POLICY label, {PAINT}"),
    ("catalog-etiquette", "The catalog beat the sermon when manners sounded alike.", f"Catalog beating sermon MANNERS alike, {PAINT}"),
    ("clink-sound", "The clink sound is a contract your ears learned to trust.", f"Fork clink sound CONTRACT ears trust, {PAINT}"),
    ("metal-wear", "Metal wears, stamps swap, the tines stay.", f"Worn metal new stamp same TINES, {PAINT}"),
    ("etiquette-shelf", "Etiquette writers did not invent the fork. They shelved the finger.", f"Etiquette writer placing finger on SHELF fork wins, {PAINT}"),
    ("fleet-treaty", "A wedding fleet is a treaty written in identical forks.", f"Identical forks TREATY label, {PAINT}"),
    ("wrist-memory", "Your wrist remembers a stab you never chose.", f"Wrist with fork stab MEMORY ghost, {PAINT}"),
    ("finger-ghost", "The finger is still a ghost in every place setting.", f"Finger ghost in modern place setting, {PAINT}"),
    ("metal-cheerful", "Metal is cheerful. Cheerful is how policy wears a fork.", f"Cheerful metal fork POLICY costume, {PAINT}"),
    ("lift-before-bite", "You lift before you bite as if bite required permission.", f"Lift then BITE PERMISSION stamp, {PAINT}"),
    ("layout-metal", "A pile of people who agreed not to argue with tines.", f"People nodding at fork tines no argue, {PAINT}"),
    ("set-down", "You will set the fork down. The tines will still be there.", f"Callback setting fork down tines remain, {PAINT}"),
    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at fork clink, {PAINT}"),
    ("look-tines", "Look at the prongs. Not the sky and not a cooking hero.", f"Tines between red X sky and red X hero, {PAINT}"),
    ("named-stack", "Finger, shared knife, fifteen thirty-three caravan, sixteen eleven travel book, molded stamp.", f"Stack icons finger knife caravan book stamp, {PAINT}"),
    ("tine-law", "A tool that owns your wrist so metal stays law.", f"Wrist fork stamped LAW, {PAINT}"),
    ("allowed-lift", "You are allowed to lift. Allowed to hate sauce season and still dine.", f"Lift ok hate sauce still dining, {PAINT}"),
    ("not-natural", "Stop calling the fork natural.", f"NATURAL stamp red X on fork, {PAINT}"),
    ("not-inevitable", "Not inevitable. Not proof you are civilized.", f"INEVITABLE CIVILIZED stamps red X, {PAINT}"),
    ("leftover-finger", "A leftover salute to a finger that left the bite.", f"Salute to finger leaving bite, {PAINT}"),
    ("stab-point", "The salute is cheerful. The stab is the point.", f"Cheerful salute on fork stab, {PAINT}"),
    ("know-prong", "Eat when the room lets you. Know which prong you are still obeying.", f"Stickman dining fork labeled which prong, {PAINT}"),
    ("glance-cheerful", "Cheerful is how tines stay without looking like a finger.", f"Smiling tines finger ghost hidden, {PAINT}"),
    ("salad-chapter", "Salad fork is a brief later chapter if you must.", f"Salad fork LATER CHAPTER label, {PAINT}"),
    ("tine-repeat", "A costume that repeats on every registry without asking your nostalgia.", f"Fork costume repeating REGISTRY no nostalgia, {PAINT}"),
    ("prong-first", "The tine meets the plate before the lesson does.", f"Tine meeting plate before LESSON, {PAINT}"),
    ("final-callback", "A finger. A travel book. Your lift.", f"Final callback finger TRAVEL BOOK YOUR LIFT, {PAINT}"),
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
        title="Why You Stab Dinner With a Fork",
        description=(
            "Your fork feels obvious. Early diners used fingers and shared knives. "
            "Catherine de Medici and Thomas Coryat helped spread pronged habits. "
            "The tines are logistics."
        ),
        tags=(
            "fork",
            "table manners",
            "etiquette",
            "history",
            "why",
            "utensil",
            "dining",
            "catherine de medici",
            "thomas coryat",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="FORK WEIRD?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why You Stab Dinner With a Fork",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-fork.json"
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

"""Author episode: you reach for a cup slot and treat interior as the sale."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."

CHAPTERS = [
    """Tonight you will reach for a plastic ring and treat the cabin as the sale. Your hand will find a cup slot as if the car grew a kitchen because cars do kitchens. Here is the part that should bother you. The first motorists did not agree. Many of them gripped a wheel and accepted that coffee lived in peril between their knees, on the floor, or in a passenger's lap like a hostage. So why does your dash wear a cup ring as if the ring were physics? Because drive-through windows arrived before stable slots did, because minivan showrooms learned that families buy interior peace faster than they buy horsepower bragging rights, because Chrysler's nineteen eighty four front-wheel-drive vans put cupholders in the conversation when the engine was already a commodity, and because factories learned that a molded ring is easier to photograph than a dyno chart. That is the whole plot. Your sip is not ergonomics by nature. It is a leftover diner habit that learned to live in molded plastic. You still reach. The reach is flattered. That is its job. The road did not vote. A showroom did, and then a ring that taught your wrist the slot until the slot started calling itself sense. Sense is a word a cup invented so a commute would still feel like law when the diner was gone.""",
    """Start with the knee, because the cup holder stole a lap and then sold it back as plastic. Before minivans, before molded consoles, before a dashboard could host six rings without irony, drinking in a car was a negotiation with gravity you could not argue with. Early drivers wedged. Early passengers guarded. Some cars offered nothing but a flat tray and the social contract that you would not brake hard. When slots arrived, they were honest and late. A ring that says hold here is a diner cup wearing geometry. It does not say the coffee is safe until the mold agrees with your cup size. If your holder still feels like the only adult option, notice that the adult option started as fast-food paperwork dragged onto a cabin that was not a table. The cabin did not offer a saucer. The cup still wanted a hand until the hand got tired of being the only suspension. The hand was not a miracle. It was logistics.""",
    """Named corners, because a myth of one inventor is how a ring gets a halo it did not earn. The cup holder is not a single eureka moment you can pin on one hero with a plaque. It is a layer cake of drive-through culture, family vans, and a molded circle that behaved nicely when you needed to sell an interior in a photograph. Chrysler's nineteen eighty four Dodge Caravan and Plymouth Voyager did not invent the cup, but they helped teach American showrooms that the cabin could be the pitch when horsepower numbers started sounding alike. Honda and Toyota followed with family vans that treated storage like furniture. Patent archives fill with ring shapes from the nineteen eighties onward, which is the quiet way a habit becomes a part number. If you still treat the slot as sacred plastic, file the brochure separately from the commute. Your ring is a minivan showroom complaint wearing a decade of molded circles.""",
    """Watch the cup leave the hand, because a horizontal car of errands needed a ring that did not require a passenger to become a table. Early coffee tricks were honest and exhausting. Hold between knees. Balance on the dash. Pass to the right. Repeat. A molded holder is a small insult to gravity with a large gift to the driver. The ring grips low. The console repeats. The slot says stay here without asking the latte to negotiate with every stoplight. I am not giving you a list of firsts. I am pointing at the swap. We took a lap that said guard this and we replaced it with a circle that said route the cup here. Route is easier to teach in a brochure. Route is easier to mold into a dozen trims. Route is easier to repeat when the line speeds up. The line is the real inventor. The line does not care about your nostalgia for a knee brace. The line cares about rings that fit and drivers who stay inside the cabin plan.""",
    """This is the rehook. You think the cup holder is a fact, the way a seat is a fact. The cup holder is a policy. In a modern cabin the policy is already on, because the alternative is trusting every driver to balance a hot cup on a slope while merging at forty miles an hour with one hand on hope. Hope is honest. Rings are scalable. Scalable is how a convenience escapes the diner booth and becomes something a fleet can own in numbers. I am not calling you clumsy for liking a slot. I am un-naturing the circle. The circle is a lap wearing a console. The console said spill risk can be law. Law is a feeling when your hand finds a ring without remembering when it learned it. If you have ever driven something with no holder, even a rental with a smooth dash, you know the slot is not physics. It is a compromise that won a production vote. A vote is not a horsepower chart. A vote is a spreadsheet with plastic and a trim catalog.""",
    """Watch the mold travel. Mass production did not invent coffee. It inventoried the answer. When the same cabin had to repeat across a family line, the cup holder became the part you could mold, spec, ship, and replace without translating a knee ritual for every chassis. Heated rings, adjustable grips, oversized slots for travel mugs: decades later the circle could warm and flex, a useful chapter about watts and molds, not the origin story of the ring itself. Do not make tonight a brochure war about which brand won. Make it about the object: plastic, ring, console, repeat. A catalog is a quiet referendum. If your minivan has six rings and your history book has a knee brace, that gap is not evolution. It is inventory. Inventory is how the past loses a fight without filing a complaint.""",
    """This is you, already, in the middle of the story. A Tuesday, a drive-through window, a reach you have performed a thousand times without thanking a showroom photographer. You slide a cup into plastic because turning would feel reckless without a ring, which is the most modern impossibility there is. None of this makes you weak by nature. It makes you a person born after the nineteen eighty four van brochures and after consoles learned furniture and after a ring learned to host travel mugs that beep. You can feel both in the same motion: relief that you do not have to guard a cup with your knees, and a tiny insult that a diner habit won a dash slot. The relief is real. The insult is the knee brace failing for a second in your imagination. You paid for interior peace with a part you never voted on. The part is cheerful. Cheerful is how a ring stays in the century without looking like a lap.""",
    """A car is a pile of compromises with a console attached. That sentence is rude and almost fair. Take the cup holder away and the cabin becomes a workshop puzzle nobody wins, or a passenger who becomes a table until the coffee cools. Mold geometry, spill radius, assembly time, replacement trim: the ring is a diagram of how to sip without sending the whole drink into the footwell story, written by someone you will not meet. You still reach. The reach is a vote for a circle that was sold as obvious. I am not telling you to hunt for a knee brace as a personality. I am telling you the personality was always the swap: a lap guard, a dash balance, a minivan brochure, a molded console line, a trim sheet that forgot your diner booth. The crowd is still in the cabin. The crowd is you and a school-run fleet treating a ring as a treaty. So what did we trade? We traded a knee that told the truth about gravity for a slot that could be molded, photographed, and forgotten. That tooling is real help: fewer spills, a passenger who keeps dignity, a coffee you can route with a parts bin. Help can be a miracle and still be a part number. We also gained a myth that the cup holder is nature and the ring is the only adult cabin. We kept the lap and called it a console. We kept the diner and called it history. Both can be true and still not be a reason to forget the holder is a policy that learned manners.""",
    """This is you. You will pull away from the window. The ring will still be there. You will feel nothing, which is the victory. Look at the slot. That is not the sky and it is not a horsepower hero. That is a knee brace, a dash balance, a nineteen eighty four van brochure, a molded console that replaced a lap, a showroom photograph that replaced a dyno chart, a brief later chapter about heated rings if you must, and a circle that still owns your commute so you will keep treating plastic as law. You are allowed to reach. You are allowed to hate spill season and still drive. Just stop calling the cup holder natural, or inevitable, or proof that you are modern. Tonight, when the cup clicks into plastic, look at it like a leftover salute to a lap that left the cabin. The salute is cheerful. The ring is the point. Go when the slot lets you. Know which circle you are still obeying.""",
]


def _stamp(index: int) -> str:
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("reach-ring", "Tonight you reach for a plastic ring and treat the cabin as the sale.", f"Stickman reaching cup ring CABIN IS SALE, {PAINT}"),
    ("hand-slot", "Your hand finds a cup slot as if the car grew a kitchen.", f"Hand finding cup slot CAR KITCHEN label, {PAINT}"),
    ("cars-kitchens", "Because cars do kitchens.", f"Car sprouting kitchen like fruit, {PAINT}"),
    ("first-no-agree", "The first motorists did not agree.", f"Early driver shaking head at cup holder, {PAINT}"),
    ("knee-peril", "Coffee lived in peril between knees, on the floor, or in a passenger lap.", f"Coffee KNEE FLOOR LAP peril labels, {PAINT}"),
    ("why-dash-ring", "Why does your dash wear a cup ring as if the ring were physics?", f"Cup ring stamped PHYSICS question mark, {PAINT}"),
    ("drive-through", "Drive-through windows arrived before stable slots did.", f"Drive-through window before cup slot timeline, {PAINT}"),
    ("minivan-showroom", "Minivan showrooms learned families buy interior peace faster than horsepower bragging.", f"Interior peace beats HORSEPOWER bragging chart, {PAINT}"),
    ("chrysler-1984", "Chrysler nineteen eighty four vans put cupholders in the conversation.", f"1984 van CUPHOLDERS IN CONVERSATION badge, {PAINT}"),
    ("engine-commodity", "When the engine was already a commodity.", f"Engine labeled COMMODITY same as others, {PAINT}"),
    ("molded-ring-photo", "A molded ring is easier to photograph than a dyno chart.", f"Molded ring vs dyno chart photo easier, {PAINT}"),
    ("not-ergonomics", "Your sip is not ergonomics by nature.", f"ERGONOMICS BY NATURE stamp red X on ring, {PAINT}"),
    ("diner-habit", "A leftover diner habit that learned to live in molded plastic.", f"Diner cup morphing into plastic ring, {PAINT}"),
    ("reach-flattered", "The reach is flattered. That is its job.", f"Smiling cup ring FLATTERED badge, {PAINT}"),
    ("road-no-vote", "The road did not vote. A showroom did.", f"Road NO VOTE showroom raising hand, {PAINT}"),
    ("slot-sense", "The slot taught your wrist until it called itself sense.", f"Wrist word SENSE after cup slot, {PAINT}"),
    ("start-knee", "Start with the knee.", f"Knee labeled START, {PAINT}"),
    ("holder-stole-lap", "The cup holder stole a lap and sold it back as plastic.", f"Lap stolen by plastic cup holder, {PAINT}"),
    ("before-minivans", "Before minivans, before molded consoles, before six rings without irony.", f"Timeline before minivan console six rings, {PAINT}"),
    ("gravity-negotiation", "Drinking in a car was a negotiation with gravity.", f"Driver negotiating with GRAVITY, {PAINT}"),
    ("wedged-guarded", "Early drivers wedged. Early passengers guarded.", f"Driver wedging passenger guarding cup, {PAINT}"),
    ("flat-tray", "Some cars offered a flat tray and the contract you would not brake hard.", f"Flat tray NO BRAKE HARD contract, {PAINT}"),
    ("slots-late", "When slots arrived, they were honest and late.", f"Slots HONEST LATE labels, {PAINT}"),
    ("hold-here", "A ring that says hold here is a diner cup wearing geometry.", f"HOLD HERE diner cup wearing geometry, {PAINT}"),
    ("mold-cup-size", "Coffee is safe until the mold agrees with your cup size.", f"Mold measuring cup size agreement, {PAINT}"),
    ("fast-food-cabin", "Fast-food paperwork dragged onto a cabin not a table.", f"Fast food papers on cabin NOT TABLE, {PAINT}"),
    ("cup-wanted-hand", "The cup still wanted a hand until the hand got tired.", f"Cup speech bubble WANT HAND, {PAINT}"),
    ("hand-suspension", "The hand got tired of being the only suspension.", f"Tired hand ONLY SUSPENSION label, {PAINT}"),
    ("not-miracle", "The hand was not a miracle. It was logistics.", f"LOGISTICS stamp on hand not miracle, {PAINT}"),
    ("named-corners", "Named corners. One inventor is a halo the ring did not earn.", f"Halo on cup ring MYTH sticker, {PAINT}"),
    ("not-one-hero", "The cup holder is not one eureka moment on a plaque.", f"Hero plaque red X many layers, {PAINT}"),
    ("layer-cake", "Drive-through culture, family vans, molded circle in a photograph.", f"Layer cake drive-through van molded ring, {PAINT}"),
    ("caravan-voyager", "Nineteen eighty four Dodge Caravan and Plymouth Voyager.", f"1984 Caravan Voyager van icons no logos, {PAINT}"),
    ("cabin-pitch", "They helped teach showrooms the cabin could be the pitch.", f"Showroom CABIN IS PITCH sign, {PAINT}"),
    ("horsepower-alike", "When horsepower numbers started sounding alike.", f"Horsepower numbers all sound ALIKE, {PAINT}"),
    ("honda-toyota", "Honda and Toyota followed with family vans that treated storage like furniture.", f"Family vans storage as FURNITURE, {PAINT}"),
    ("patent-rings", "Patent archives fill with ring shapes from the nineteen eighties onward.", f"Patent archive ring shapes 1980s, {PAINT}"),
    ("habit-part-number", "The quiet way a habit becomes a part number.", f"Habit becoming PART NUMBER arrow, {PAINT}"),
    ("minivan-complaint", "Your ring is a minivan showroom complaint wearing molded circles.", f"Minivan complaint wearing molded circles coat, {PAINT}"),
    ("cup-leaves-hand", "Watch the cup leave the hand.", f"Hand releasing cup walking away, {PAINT}"),
    ("errands-ring", "A car of errands needed a ring without a passenger becoming a table.", f"Ring safe vs passenger as table red X, {PAINT}"),
    ("knees-dash-pass", "Hold between knees. Balance on dash. Pass to the right. Repeat.", f"Three panel KNEES DASH PASS REPEAT, {PAINT}"),
    ("small-insult", "A molded holder is a small insult to gravity.", f"Cup ring insulting gravity cloud, {PAINT}"),
    ("ring-grips", "The ring grips low. The console repeats.", f"Ring grips low console repeats, {PAINT}"),
    ("stay-here", "The slot says stay here without the latte negotiating every stoplight.", f"STAY HERE slot no stoplight negotiate, {PAINT}"),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", f"FIRSTS red X SWAP arrow, {PAINT}"),
    ("lap-guard", "We took a lap that said guard this.", f"Lap speech bubble GUARD THIS, {PAINT}"),
    ("circle-route", "We replaced it with a circle that said route the cup here.", f"Circle ROUTE CUP HERE arrows, {PAINT}"),
    ("route-brochure", "Route is easier to teach in a brochure.", f"Brochure teaching ROUTE checkmark, {PAINT}"),
    ("route-mold", "Route is easier to mold into a dozen trims.", f"Same ring molding dozen trims, {PAINT}"),
    ("line-inventor", "The line is the real inventor.", f"Factory line labeled REAL INVENTOR, {PAINT}"),
    ("knee-nostalgia", "The line does not care about nostalgia for a knee brace.", f"Knee brace nostalgia red X, {PAINT}"),
    ("rehook-fact", "You think the cup holder is a fact, the way a seat is a fact.", f"Cup holder vs seat both labeled FACT, {PAINT}"),
    ("holder-policy", "The cup holder is a policy.", f"POLICY stamp on cup ring, {PAINT}"),
    ("hot-cup-merge", "Trusting every driver to balance a hot cup while merging.", f"Hot cup merging red X ring wins, {PAINT}"),
    ("hope-honest", "Hope is honest. Rings are scalable.", f"HOPE honest RINGS scalable scales, {PAINT}"),
    ("un-naturing", "I am un-naturing the circle.", f"Circle NATURAL stamp peeling off, {PAINT}"),
    ("lap-console", "The circle is a lap wearing a console.", f"Lap wearing console costume, {PAINT}"),
    ("spill-law", "The console said spill risk can be law.", f"Console SPILL RISK IS LAW, {PAINT}"),
    ("rental-smooth", "If you drove something with no holder, a rental with smooth dash.", f"Rental smooth dash no holder, {PAINT}"),
    ("not-physics", "You know the slot is not physics.", f"PHYSICS stamp red X on cup slot, {PAINT}"),
    ("production-vote", "A compromise that won a production vote.", f"Production line voting for ring wins, {PAINT}"),
    ("spreadsheet-plastic", "A vote is a spreadsheet with plastic and a trim catalog.", f"Spreadsheet plastic trim catalog, {PAINT}"),
    ("mold-travel", "Watch the mold travel.", f"Plastic mold traveling across frame, {PAINT}"),
    ("inventoried-answer", "Mass production inventoried the answer.", f"Factory inventory cup rings shelf, {PAINT}"),
    ("mold-spec-ship", "Mold, spec, ship, replace without a knee ritual.", f"MOLD SPEC SHIP REPLACE conveyor, {PAINT}"),
    ("heated-rings", "Heated rings, adjustable grips, travel mugs: a later chapter.", f"Heated ring travel mug LATER CHAPTER, {PAINT}"),
    ("no-brochure-war", "Do not make tonight a brochure war about which brand won.", f"BROCHURE WAR stamp red X, {PAINT}"),
    ("object-plastic", "Make it about the object: plastic, ring, console, repeat.", f"PLASTIC RING CONSOLE REPEAT icons, {PAINT}"),
    ("catalog-referendum", "A catalog is a quiet referendum.", f"Quiet catalog REFERENDUM whisper, {PAINT}"),
    ("minivan-vs-knee", "Your minivan has six rings and your history book has a knee brace.", f"Six rings vs knee brace gap, {PAINT}"),
    ("inventory-fight", "Inventory is how the past loses a fight without filing a complaint.", f"Past losing fight INVENTORY filing cabinet, {PAINT}"),
    ("this-is-you", "This is you, already, in the middle of the story.", f"Stickman labeled THIS IS YOU drive-through, {PAINT}"),
    ("tuesday-reach", "A Tuesday, a drive-through window, a reach without thanking a photographer.", f"Tuesday drive-through reach no thank you, {PAINT}"),
    ("slide-cup", "You slide a cup into plastic because turning would feel reckless.", f"Cup sliding into ring RECKLESS without, {PAINT}"),
    ("modern-impossibility", "The most modern impossibility there is.", f"MODERN IMPOSSIBILITY stamp on turn, {PAINT}"),
    ("after-1984", "Born after nineteen eighty four van brochures.", f"Timeline after 1984 van brochure, {PAINT}"),
    ("console-furniture", "After consoles learned furniture.", f"Console learning FURNITURE morph, {PAINT}"),
    ("travel-mug-beeps", "After a ring learned to host travel mugs.", f"Ring hosting oversized travel mug, {PAINT}"),
    ("relief-insult", "Relief you do not guard with knees, insult a diner habit won.", f"Relief checkmark insult diner habit wins, {PAINT}"),
    ("knee-imagination", "The knee brace failing in your imagination.", f"Ghost knee brace failing imagination, {PAINT}"),
    ("never-voted", "You paid for interior peace with a part you never voted on.", f"Interior peace NEVER VOTED stamp, {PAINT}"),
    ("cheerful-ring", "Cheerful is how a ring stays without looking like a lap.", f"Smiling ring lap costume hidden, {PAINT}"),
    ("compromises-console", "A car is a pile of compromises with a console attached.", f"Car pile COMPROMISES console bolted, {PAINT}"),
    ("take-holder-away", "Take the cup holder away and the cabin becomes a workshop puzzle.", f"Cabin puzzle nobody wins no holder, {PAINT}"),
    ("mold-spill", "Mold geometry, spill radius, assembly time, replacement trim.", f"MOLD SPILL RADIUS TRIM labels, {PAINT}"),
    ("diagram-sip", "The ring is a diagram of how to sip without the footwell story.", f"Ring diagram SIP without footwell story, {PAINT}"),
    ("reach-vote", "The reach is a vote for a circle sold as obvious.", f"Reach voting CIRCLE OBVIOUS, {PAINT}"),
    ("personality-swap", "The personality was always the swap.", f"SWAP arrow lap to molded ring, {PAINT}"),
    ("lap-guard-icon", "A lap guard, a dash balance.", f"Lap guard and dash balance icons, {PAINT}"),
    ("minivan-brochure", "A minivan brochure, a molded console line.", f"Minivan brochure console line icons, {PAINT}"),
    ("trim-forgot-diner", "A trim sheet that forgot your diner booth.", f"Trim sheet forgetting diner booth, {PAINT}"),
    ("treaty-fleet", "You and a school-run fleet treating a ring as a treaty.", f"School run fleet ring TREATY handshake, {PAINT}"),
    ("what-we-traded", "We traded a knee that told the truth about gravity.", f"Knee truth GRAVITY traded away, {PAINT}"),
    ("molded-photographed", "For a slot that could be molded, photographed, and forgotten.", f"Molded photographed forgotten ring on line, {PAINT}"),
    ("real-help", "Real help: fewer spills, dignity, coffee from a parts bin.", f"Fewer spills dignity COFFEE parts bin, {PAINT}"),
    ("miracle-part-number", "Help can be a miracle and still be a part number.", f"MIRACLE and PART NUMBER both true, {PAINT}"),
    ("myth-nature", "A myth that the cup holder is nature and the ring is the only adult cabin.", f"MYTH NATURE ADULT CABIN stamps, {PAINT}"),
    ("lap-console-name", "We kept the lap and called it a console.", f"Lap wearing CONSOLE name tag, {PAINT}"),
    ("diner-history", "We kept the diner and called it history.", f"Diner booth labeled HISTORY museum, {PAINT}"),
    ("policy-manners", "The holder is a policy that learned manners.", f"Policy cup ring in polite bow tie, {PAINT}"),
    ("dyno-era", "There was an era when the dyno chart was the whole sermon.", f"Dyno chart preaching WHOLE SERMON label, {PAINT}"),
    ("spill-footwell", "A spill in the footwell is a lecture nobody wants.", f"Spill in footwell LECTURE red X, {PAINT}"),
    ("console-real-estate", "The console is real estate with a beverage department.", f"Console REAL ESTATE beverage department, {PAINT}"),
    ("interior-separate", "Interior peace arrived as a separate homework assignment.", f"Interior peace SEPARATE HOMEWORK label, {PAINT}"),
    ("drive-through-line", "The drive-through line taught the cabin what waiting means.", f"Drive-through line teaching WAITING, {PAINT}"),
    ("trim-photograph", "A trim sheet is a photograph that learned to sell.", f"Trim sheet photograph learned to SELL, {PAINT}"),
    ("coffee-commute", "The commute wanted coffee before the cabin agreed.", f"Commute wanting coffee cabin disagreeing, {PAINT}"),
    ("ring-count", "Six rings is a family policy written in plastic.", f"Six cup rings FAMILY POLICY label, {PAINT}"),
    ("brochure-dyno", "The brochure beat the dyno when the numbers sounded alike.", f"Brochure beating dyno chart ALIKE numbers, {PAINT}"),
    ("click-sound", "The click sound is a contract your ears learned to trust.", f"Cup click sound CONTRACT ears trust, {PAINT}"),
    ("plastic-wear", "Plastic wears, molds swap, the circle stays.", f"Worn plastic new mold same CIRCLE, {PAINT}"),
    ("regulators-shelf", "Regulators did not invent the ring. They shelved it.", f"Regulator placing ring on SHELF not invent, {PAINT}"),
    ("fleet-treaty", "A school-run fleet is a treaty written in identical rings.", f"Identical cup rings TREATY label, {PAINT}"),
    ("wrist-memory", "Your wrist remembers a slot you never chose.", f"Wrist with slot MEMORY ghost, {PAINT}"),
    ("knee-ghost", "The knee brace is still a ghost in every cabin.", f"Knee brace ghost in modern cabin, {PAINT}"),
    ("plastic-cheerful", "Plastic is cheerful. Cheerful is how policy wears a circle.", f"Cheerful plastic circle POLICY costume, {PAINT}"),
    ("reach-before-roll", "You reach before you roll as if roll required permission.", f"Reach then ROLL PERMISSION stamp, {PAINT}"),
    ("layout-plastic", "A pile of people who agreed not to argue with plastic.", f"People nodding at plastic no argue, {PAINT}"),
    ("pull-away", "You will pull away from the window. The ring will still be there.", f"Callback pulling away cup in ring, {PAINT}"),
    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at cup click, {PAINT}"),
    ("look-slot", "Look at the slot. Not the sky and not a horsepower hero.", f"Slot between red X sky and red X hero, {PAINT}"),
    ("named-stack", "Knee brace, dash balance, nineteen eighty four brochure, molded console, showroom photo.", f"Stack icons knee dash brochure console photo, {PAINT}"),
    ("circle-law", "A circle that owns your commute so plastic stays law.", f"Commute circle stamped LAW, {PAINT}"),
    ("allowed-reach", "You are allowed to reach. Allowed to hate spill season and still drive.", f"Reach ok hate spills still driving, {PAINT}"),
    ("not-natural", "Stop calling the cup holder natural.", f"NATURAL stamp red X on ring, {PAINT}"),
    ("not-inevitable", "Not inevitable. Not proof you are modern.", f"INEVITABLE MODERN stamps red X, {PAINT}"),
    ("leftover-lap", "A leftover salute to a lap that left the cabin.", f"Salute to lap leaving cabin, {PAINT}"),
    ("ring-point", "The salute is cheerful. The ring is the point.", f"Cheerful salute on plastic ring, {PAINT}"),
    ("know-circle", "Go when the slot lets you. Know which circle you are still obeying.", f"Stickman driving cup labeled which circle, {PAINT}"),
    ("glance-cheerful", "Cheerful is how a ring stays without looking like a lap.", f"Smiling ring lap ghost hidden, {PAINT}"),
    ("final-callback", "A knee. A showroom. Your reach.", f"Final callback knee SHOWROOM YOUR REACH, {PAINT}"),
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
        title="Why a Cup Holder Beat Horsepower",
        description=(
            "Your cup slot feels obvious. Early drivers balanced coffee on knees. "
            "Nineteen eighty four minivan brochures made the cabin the pitch. "
            "The molded ring is logistics."
        ),
        tags=(
            "cup holder",
            "minivan",
            "car interior",
            "chrysler",
            "history",
            "why",
            "car",
            "design",
            "horsepower",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="CUP WON?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why a Cup Holder Beat Horsepower",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-cupholder.json"
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

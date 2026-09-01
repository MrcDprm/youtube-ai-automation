"""Author episode: you touch painted plastic and treat a bumper as the car's face."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."

CHAPTERS = [
    """Tonight you will touch painted plastic at the front of a car and treat it as the car's face. Your hand will find a bumper that matches the body color as if the bumper were always a costume. Here is the part that should bother you. The first motorists did not agree. Many of them parked behind chrome bars that shone like jewelry and dared a fender to disagree. So why does your front end wear body paint as if paint were physics? Because the National Highway Traffic Safety Administration wrote a five-mile-per-hour bumper rule in nineteen seventy-two, because nineteen seventies showrooms had to sell cars that could kiss a post without writing a repair estimate, because pedestrian rules later asked the front end to be less like a blade, and because factories learned that a plastic fascia is easier to mold in one color than a chrome bar is to polish after every parking lot negotiation. That is the whole plot. Your bumper is not armor by nature. It is a leftover chrome attitude wearing a painted cover over foam. You still park. The park is flattered. That is its job. The curb did not vote. A regulation did, and then a fascia that taught your eye the color match until the match started calling itself sense. Sense is a word plastic invented so a commute would still feel like law when the chrome left the lot.""",
    """Start with the chrome bar, because the bumper stole a shine and then sold it back as paint. Before federal five-mile-per-hour rules, before black rubber blocks embarrassed every sedan, before a front end could be one molded smile in body color, parking was a negotiation with metal you could see from across the street. Early drivers accepted dents as honesty. Early bumpers announced themselves. When painted plastic arrived, it was honest and late. A fascia that says match the door is a chrome bar wearing makeup. It does not say the car is safe until the foam behind the paint agrees with the test lab. If your bumper still feels like the only adult option, notice that the adult option started as a parking lot repair bill dragged onto a front end that was not a face. The front end did not offer a blade. The chrome still wanted to shine until the shine got tired of being the only warning. The shine was not a miracle. It was logistics.""",
    """Named corners, because a myth of one designer is how a fascia gets a halo it did not earn. The painted bumper is not a single eureka moment you can pin on one hero with a clay model. It is a layer cake of NHTSA Standard two fifteen, insurance spreadsheets, pedestrian committees, and a molded cover that behaved nicely when you needed to sell a car in a photograph. Ralph Nader did not invent the plastic bumper, but the safety argument he helped normalize made showrooms nervous about chrome that looked tough and bent expensive. Volvo's pedestrian work in the nineteen seventies and eighties helped teach Europe that a front end could be a compromise with a walker's knee, not a declaration of war. European pedestrian protection rules in the two thousands turned the front into homework. If you still treat the painted cover as sacred sheet metal, file the brochure separately from the parking lot. Your fascia is a five-mile-per-hour test complaint wearing decades of molded color.""",
    """Watch the chrome leave the lot, because a horizontal nation of drivers needed a front end that did not send every tap to a body shop invoice. Early parking tricks were honest and exhausting. Tap a post. Bend a bar. Polish or replace. Repeat. A plastic fascia is a small insult to visible damage with a large gift to the accountant. The cover grips color. The foam repeats. The bumper says absorb here without asking the fender to negotiate with every shopping cart. I am not giving you a list of firsts. I am pointing at the swap. We took a chrome bar that said look at my shine and we replaced it with a painted shell that said hide the bruise here. Hide is easier to teach in a brochure. Hide is easier to mold into a dozen trims. Hide is easier to repeat when the line speeds up. The line is the real inventor. The line does not care about your nostalgia for a chrome grin. The line cares about fascias that pass tests and owners who stay inside the warranty plan.""",
    """This is the rehook. You think the painted bumper is a fact, the way a wheel is a fact. The painted bumper is a policy. In a modern car the policy is already on, because the alternative is trusting every driver to treat a chrome bar like jewelry while a pedestrian meets a rigid edge at thirty kilometers an hour. Rigid is honest. Foam is scalable. Scalable is how a safety compromise escapes the test lab and becomes something a fleet can own in numbers. I am not calling you vain for liking a color match. I am un-naturing the fascia. The fascia is a chrome bar wearing a body-color coat. The coat said parking taps can be law. Law is a feeling when your eye sees one continuous color without remembering when it learned it. If you have ever driven something with exposed chrome bumpers, even a classic at a show with bars that gleam, you know the cover is not physics. It is a compromise that won a production vote. A vote is not a design school lecture. A vote is a spreadsheet with foam, paint, and a trim catalog.""",
    """Watch the mold travel. Mass production did not invent parking. It inventoried the answer. When the same front end had to repeat across a family line, the fascia became the part you could mold, paint, ship, and replace without translating a chrome polish ritual for every chassis. Energy absorbers, crush cans, pedestrian-friendly curves: decades later the shell could flex and forgive, a useful chapter about foam and labs, not the origin story of the cover itself. Do not make tonight a brochure war about which brand won the prettiest front end. Make it about the object: plastic, foam, paint, repeat. A catalog is a quiet referendum. If your crossover has a seamless nose and your history book has a chrome bar, that gap is not evolution. It is inventory. Inventory is how the past loses a fight without filing a complaint.""",
    """This is you, already, in the middle of the story. A Saturday, a grocery lot, a pull-in you have performed a thousand times without thanking a crash test dummy. You ease forward because reversing would feel reckless without a forgiving nose, which is the most modern impossibility there is. None of this makes you careless by nature. It makes you a person born after the nineteen seventies rubber-block era and after fascias learned color match and after a cover learned to host sensors that beep. You can feel both in the same motion: relief that you do not have to polish chrome after every cart, and a tiny insult that a parking lot habit won a painted shell. The relief is real. The insult is the chrome bar failing for a second in your imagination. You paid for visual peace with a part you never voted on. The part is cheerful. Cheerful is how a fascia stays in the century without looking like a bar.""",
    """A car is a pile of compromises with a front end attached. That sentence is rude and almost fair. Take the painted cover away and the car becomes a workshop puzzle nobody wins, or a repair bill that arrives before the latte cools. Foam geometry, pedestrian height, assembly time, replacement trim: the fascia is a diagram of how to park without sending the whole fender into the insurance story, written by someone you will not meet. You still pull in. The pull-in is a vote for a shell that was sold as obvious. I am not telling you to hunt for chrome as a personality. I am telling you the personality was always the swap: a shining bar, a black rubber block, a five-mile-per-hour test, a molded color line, a trim sheet that forgot your polish cloth. The crowd is still in the lot. The crowd is you and a grocery fleet treating a fascia as a treaty. So what did we trade? We traded a chrome bar that told the truth about every tap for a shell that could be molded, painted, and forgiven. That tooling is real help: fewer visible scars, a pedestrian who meets foam first, a front end you can replace with a parts bin. Help can be a miracle and still be a part number. We also gained a myth that the painted bumper is nature and the fascia is the only adult face. We kept the chrome and called it heritage. We kept the bar and called it history. Both can be true and still not be a reason to forget the bumper is a policy that learned manners.""",
    """This is you. You will back into the space. The painted nose will still be there. You will feel nothing, which is the victory. Look at the fascia. That is not the sky and it is not a design hero. That is a chrome bar, a black rubber block, a nineteen seventy-two NHTSA test, a molded cover that replaced a shine, a showroom photograph that replaced a polish cloth, a brief later chapter about pedestrian curves if you must, and a shell that still owns your parking lot so you will keep treating plastic as law. You are allowed to pull in. You are allowed to hate repair season and still drive. Just stop calling the painted bumper natural, or inevitable, or proof that you are modern. Tonight, when the color-matched nose catches the lot light, look at it like a leftover salute to a chrome bar that left the front end. The salute is cheerful. The costume is the point. Go when the space lets you. Know which cover you are still obeying.""",
]


def _stamp(index: int) -> str:
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("touch-fascia", "Tonight you touch painted plastic and treat the bumper as the car's face.", f"Stickman touching painted front fascia CAR FACE, {PAINT}"),
    ("hand-color", "Your hand finds a bumper that matches body color as if paint were physics.", f"Hand on color-matched bumper PHYSICS question mark, {PAINT}"),
    ("bumper-costume", "As if the bumper were always a costume.", f"Bumper wearing COSTUME label over foam, {PAINT}"),
    ("first-no-agree", "The first motorists did not agree.", f"Early driver shaking head at painted bumper, {PAINT}"),
    ("chrome-bars", "They parked behind chrome bars that shone like jewelry.", f"Chrome bumper bars SHINE LIKE JEWELRY, {PAINT}"),
    ("why-body-paint", "Why does your front end wear body paint as if paint were physics?", f"Body paint stamped PHYSICS question mark, {PAINT}"),
    ("nhtsa-1972", "NHTSA wrote a five-mile-per-hour bumper rule in nineteen seventy-two.", f"NHTSA 1972 FIVE MPH BUMPER document, {PAINT}"),
    ("kiss-post", "Cars that could kiss a post without a repair estimate.", f"Car kissing post NO REPAIR ESTIMATE, {PAINT}"),
    ("pedestrian-rules", "Pedestrian rules asked the front end to be less like a blade.", f"Front end BLADE red X pedestrian curve, {PAINT}"),
    ("plastic-fascia", "A plastic fascia is easier to mold in one color than chrome is to polish.", f"Plastic fascia vs chrome polish easier mold, {PAINT}"),
    ("not-armor", "Your bumper is not armor by nature.", f"ARMOR BY NATURE stamp red X on fascia, {PAINT}"),
    ("chrome-foam", "A leftover chrome attitude wearing a painted cover over foam.", f"Chrome attitude morphing into painted foam cover, {PAINT}"),
    ("park-flattered", "The park is flattered. That is its job.", f"Smiling bumper FLATTERED badge, {PAINT}"),
    ("curb-no-vote", "The curb did not vote. A regulation did.", f"Curb NO VOTE regulation raising hand, {PAINT}"),
    ("match-sense", "The color match taught your eye until it called itself sense.", f"Eye word SENSE after color match, {PAINT}"),
    ("start-chrome", "Start with the chrome bar.", f"Chrome bar labeled START, {PAINT}"),
    ("bumper-stole-shine", "The bumper stole a shine and sold it back as paint.", f"Chrome shine stolen by painted cover, {PAINT}"),
    ("before-5mph", "Before federal five-mile-per-hour rules, before black rubber blocks.", f"Timeline before 5mph rubber block era, {PAINT}"),
    ("parking-negotiation", "Parking was a negotiation with metal you could see from across the street.", f"Parking negotiation with visible metal, {PAINT}"),
    ("dents-honesty", "Early drivers accepted dents as honesty.", f"Dent labeled HONESTY checkmark, {PAINT}"),
    ("bumpers-announced", "Early bumpers announced themselves.", f"Chrome bumper ANNOUNCING itself loudly, {PAINT}"),
    ("plastic-late", "When painted plastic arrived, it was honest and late.", f"Painted plastic HONEST LATE labels, {PAINT}"),
    ("match-door", "A fascia that says match the door is a chrome bar wearing makeup.", f"MATCH DOOR chrome bar wearing makeup, {PAINT}"),
    ("foam-test-lab", "Safe until the foam behind the paint agrees with the test lab.", f"Foam behind paint agreeing with TEST LAB, {PAINT}"),
    ("repair-bill", "A parking lot repair bill dragged onto a front end not a face.", f"Repair bill on front end NOT FACE, {PAINT}"),
    ("chrome-wanted-shine", "The chrome still wanted to shine until the shine got tired.", f"Chrome speech bubble WANT SHINE, {PAINT}"),
    ("shine-warning", "The shine got tired of being the only warning.", f"Tired shine ONLY WARNING label, {PAINT}"),
    ("not-miracle", "The shine was not a miracle. It was logistics.", f"LOGISTICS stamp on chrome not miracle, {PAINT}"),
    ("named-corners", "Named corners. One designer is a halo the fascia did not earn.", f"Halo on bumper MYTH sticker, {PAINT}"),
    ("not-one-hero", "The painted bumper is not one eureka moment on a clay model.", f"Hero clay model red X many layers, {PAINT}"),
    ("layer-cake", "NHTSA two fifteen, insurance spreadsheets, pedestrian committees, molded cover.", f"Layer cake NHTSA insurance pedestrian mold, {PAINT}"),
    ("nader-nervous", "Ralph Nader helped normalize safety arguments that made chrome nervous.", f"Safety argument making chrome NERVOUS, {PAINT}"),
    ("volvo-pedestrian", "Volvo pedestrian work taught Europe a front end could compromise with a knee.", f"Volvo front end compromising with KNEE not war, {PAINT}"),
    ("eu-rules", "European pedestrian protection rules turned the front into homework.", f"EU pedestrian rules HOMEWORK stamp, {PAINT}"),
    ("habit-part-number", "The quiet way a habit becomes a part number.", f"Habit becoming PART NUMBER arrow, {PAINT}"),
    ("test-complaint", "Your fascia is a five-mile-per-hour test complaint wearing molded color.", f"5mph test complaint wearing color coat, {PAINT}"),
    ("chrome-leaves", "Watch the chrome leave the lot.", f"Chrome bar walking away from lot, {PAINT}"),
    ("tap-invoice", "A front end that did not send every tap to a body shop invoice.", f"Tap to body shop INVOICE red X, {PAINT}"),
    ("tap-bend-polish", "Tap a post. Bend a bar. Polish or replace. Repeat.", f"Three panel TAP BEND POLISH REPEAT, {PAINT}"),
    ("small-insult", "A plastic fascia is a small insult to visible damage.", f"Plastic fascia insulting visible damage, {PAINT}"),
    ("cover-grips", "The cover grips color. The foam repeats.", f"Cover grips color foam repeats, {PAINT}"),
    ("absorb-here", "The bumper says absorb here without asking the fender to negotiate.", f"ABSORB HERE no fender negotiate, {PAINT}"),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", f"FIRSTS red X SWAP arrow, {PAINT}"),
    ("chrome-shine", "We took a chrome bar that said look at my shine.", f"Chrome bar LOOK AT MY SHINE speech, {PAINT}"),
    ("shell-hide", "We replaced it with a painted shell that said hide the bruise here.", f"Painted shell HIDE BRUISE HERE, {PAINT}"),
    ("hide-brochure", "Hide is easier to teach in a brochure.", f"Brochure teaching HIDE checkmark, {PAINT}"),
    ("hide-mold", "Hide is easier to mold into a dozen trims.", f"Same fascia molding dozen trims, {PAINT}"),
    ("line-inventor", "The line is the real inventor.", f"Factory line labeled REAL INVENTOR, {PAINT}"),
    ("chrome-nostalgia", "The line does not care about nostalgia for a chrome grin.", f"Chrome grin nostalgia red X, {PAINT}"),
    ("rehook-fact", "You think the painted bumper is a fact, the way a wheel is a fact.", f"Painted bumper vs wheel both labeled FACT, {PAINT}"),
    ("bumper-policy", "The painted bumper is a policy.", f"POLICY stamp on fascia, {PAINT}"),
    ("pedestrian-edge", "A pedestrian meets a rigid edge at thirty kilometers an hour.", f"Rigid edge vs pedestrian red X foam wins, {PAINT}"),
    ("rigid-honest", "Rigid is honest. Foam is scalable.", f"RIGID honest FOAM scalable scales, {PAINT}"),
    ("un-naturing", "I am un-naturing the fascia.", f"Fascia NATURAL stamp peeling off, {PAINT}"),
    ("chrome-coat", "The fascia is a chrome bar wearing a body-color coat.", f"Chrome bar wearing body color COAT, {PAINT}"),
    ("parking-law", "The coat said parking taps can be law.", f"Coat PARKING TAPS IS LAW, {PAINT}"),
    ("classic-chrome", "If you drove something with exposed chrome bumpers at a show.", f"Classic show chrome bumpers gleaming, {PAINT}"),
    ("not-physics", "You know the cover is not physics.", f"PHYSICS stamp red X on fascia, {PAINT}"),
    ("production-vote", "A compromise that won a production vote.", f"Production line voting for fascia wins, {PAINT}"),
    ("spreadsheet-foam", "A vote is a spreadsheet with foam, paint, and a trim catalog.", f"Spreadsheet foam paint trim catalog, {PAINT}"),
    ("mold-travel", "Watch the mold travel.", f"Plastic mold traveling across frame, {PAINT}"),
    ("inventoried-answer", "Mass production inventoried the answer.", f"Factory inventory fascias shelf, {PAINT}"),
    ("mold-paint-ship", "Mold, paint, ship, replace without a chrome polish ritual.", f"MOLD PAINT SHIP REPLACE conveyor, {PAINT}"),
    ("energy-absorber", "Energy absorbers, crush cans, pedestrian-friendly curves: a later chapter.", f"Energy absorber crush can LATER CHAPTER, {PAINT}"),
    ("no-brochure-war", "Do not make tonight a brochure war about which brand won.", f"BROCHURE WAR stamp red X, {PAINT}"),
    ("object-plastic", "Make it about the object: plastic, foam, paint, repeat.", f"PLASTIC FOAM PAINT REPEAT icons, {PAINT}"),
    ("catalog-referendum", "A catalog is a quiet referendum.", f"Quiet catalog REFERENDUM whisper, {PAINT}"),
    ("crossover-vs-chrome", "Your crossover has a seamless nose and your history book has a chrome bar.", f"Seamless nose vs chrome bar gap, {PAINT}"),
    ("inventory-fight", "Inventory is how the past loses a fight without filing a complaint.", f"Past losing fight INVENTORY filing cabinet, {PAINT}"),
    ("this-is-you", "This is you, already, in the middle of the story.", f"Stickman labeled THIS IS YOU grocery lot, {PAINT}"),
    ("saturday-pull", "A Saturday, a grocery lot, a pull-in without thanking a crash dummy.", f"Saturday grocery pull-in no thank dummy, {PAINT}"),
    ("ease-forward", "You ease forward because reversing would feel reckless.", f"Ease forward RECKLESS without forgiving nose, {PAINT}"),
    ("modern-impossibility", "The most modern impossibility there is.", f"MODERN IMPOSSIBILITY stamp on pull-in, {PAINT}"),
    ("after-rubber", "Born after the nineteen seventies rubber-block era.", f"Timeline after 1970s rubber block era, {PAINT}"),
    ("fascia-color", "After fascias learned color match.", f"Fascia learning COLOR MATCH morph, {PAINT}"),
    ("sensor-beeps", "After a cover learned to host sensors that beep.", f"Fascia hosting parking sensors beeping, {PAINT}"),
    ("relief-insult", "Relief you do not polish chrome, insult a parking habit won.", f"Relief checkmark insult parking habit wins, {PAINT}"),
    ("chrome-imagination", "The chrome bar failing in your imagination.", f"Ghost chrome bar failing imagination, {PAINT}"),
    ("never-voted", "You paid for visual peace with a part you never voted on.", f"Visual peace NEVER VOTED stamp, {PAINT}"),
    ("cheerful-fascia", "Cheerful is how a fascia stays without looking like a bar.", f"Smiling fascia chrome bar costume hidden, {PAINT}"),
    ("compromises-front", "A car is a pile of compromises with a front end attached.", f"Car pile COMPROMISES front end bolted, {PAINT}"),
    ("take-cover-away", "Take the painted cover away and the car becomes a workshop puzzle.", f"Front end puzzle nobody wins no cover, {PAINT}"),
    ("foam-geometry", "Foam geometry, pedestrian height, assembly time, replacement trim.", f"FOAM PEDESTRIAN HEIGHT TRIM labels, {PAINT}"),
    ("diagram-park", "The fascia is a diagram of how to park without the insurance story.", f"Fascia diagram PARK without insurance story, {PAINT}"),
    ("pull-vote", "The pull-in is a vote for a shell sold as obvious.", f"Pull-in voting SHELL OBVIOUS, {PAINT}"),
    ("personality-swap", "The personality was always the swap.", f"SWAP arrow chrome to painted shell, {PAINT}"),
    ("chrome-rubber", "A shining bar, a black rubber block.", f"Chrome bar and rubber block icons, {PAINT}"),
    ("test-mold", "A five-mile-per-hour test, a molded color line.", f"5mph test molded color line icons, {PAINT}"),
    ("trim-forgot-polish", "A trim sheet that forgot your polish cloth.", f"Trim sheet forgetting polish cloth, {PAINT}"),
    ("treaty-fleet", "You and a grocery fleet treating a fascia as a treaty.", f"Grocery fleet fascia TREATY handshake, {PAINT}"),
    ("what-we-traded", "We traded a chrome bar that told the truth about every tap.", f"Chrome truth EVERY TAP traded away, {PAINT}"),
    ("molded-forgiven", "For a shell that could be molded, painted, and forgiven.", f"Molded painted forgiven shell on line, {PAINT}"),
    ("real-help", "Real help: fewer visible scars, pedestrian meets foam first.", f"Fewer scars pedestrian FOAM FIRST, {PAINT}"),
    ("miracle-part-number", "Help can be a miracle and still be a part number.", f"MIRACLE and PART NUMBER both true, {PAINT}"),
    ("myth-nature", "A myth that the painted bumper is nature and the fascia is the only adult face.", f"MYTH NATURE ADULT FACE stamps, {PAINT}"),
    ("chrome-heritage", "We kept the chrome and called it heritage.", f"Chrome labeled HERITAGE museum, {PAINT}"),
    ("bar-history", "We kept the bar and called it history.", f"Chrome bar labeled HISTORY, {PAINT}"),
    ("policy-manners", "The bumper is a policy that learned manners.", f"Policy bumper in polite bow tie, {PAINT}"),
    ("showroom-era", "There was an era when the chrome bar was the whole sermon.", f"Chrome bar preaching WHOLE SERMON label, {PAINT}"),
    ("black-rubber", "Black rubber blocks embarrassed every sedan for a decade.", f"Black rubber bumper EMBARRASSED sedan, {PAINT}"),
    ("fascia-real-estate", "The front end is real estate with a safety department.", f"Front end REAL ESTATE safety department, {PAINT}"),
    ("visual-separate", "Visual peace arrived as a separate homework assignment.", f"Visual peace SEPARATE HOMEWORK label, {PAINT}"),
    ("parking-lot-line", "The parking lot line taught the fascia what waiting means.", f"Parking lot line teaching WAITING, {PAINT}"),
    ("trim-photograph", "A trim sheet is a photograph that learned to sell.", f"Trim sheet photograph learned to SELL, {PAINT}"),
    ("car-lot", "The lot wanted forgiveness before the owner agreed.", f"Lot wanting forgiveness owner disagreeing, {PAINT}"),
    ("color-count", "One color is a family policy written in plastic.", f"One color FAMILY POLICY label, {PAINT}"),
    ("brochure-chrome", "The brochure beat the chrome when repair bills sounded alike.", f"Brochure beating chrome REPAIR BILLS alike, {PAINT}"),
    ("tap-sound", "The tap sound is a contract your ears learned to ignore.", f"Light tap sound CONTRACT ears ignore, {PAINT}"),
    ("plastic-wear", "Plastic wears, molds swap, the shell stays.", f"Worn plastic new mold same SHELL, {PAINT}"),
    ("regulators-shelf", "Regulators did not invent the fascia. They shelved the chrome.", f"Regulator placing chrome on SHELF fascia wins, {PAINT}"),
    ("fleet-treaty", "A grocery fleet is a treaty written in identical noses.", f"Identical fascias TREATY label, {PAINT}"),
    ("eye-memory", "Your eye remembers a color match you never chose.", f"Eye with color match MEMORY ghost, {PAINT}"),
    ("chrome-ghost", "The chrome bar is still a ghost in every front end.", f"Chrome bar ghost in modern fascia, {PAINT}"),
    ("plastic-cheerful", "Plastic is cheerful. Cheerful is how policy wears a shell.", f"Cheerful plastic shell POLICY costume, {PAINT}"),
    ("pull-before-park", "You pull in before you park as if park required permission.", f"Pull in then PARK PERMISSION stamp, {PAINT}"),
    ("layout-plastic", "A pile of people who agreed not to argue with plastic.", f"People nodding at plastic no argue, {PAINT}"),
    ("back-space", "You will back into the space. The painted nose will still be there.", f"Callback backing in painted nose, {PAINT}"),
    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at parking, {PAINT}"),
    ("look-fascia", "Look at the fascia. Not the sky and not a design hero.", f"Fascia between red X sky and red X hero, {PAINT}"),
    ("named-stack", "Chrome bar, rubber block, nineteen seventy-two test, molded cover, showroom photo.", f"Stack icons chrome rubber test mold photo, {PAINT}"),
    ("shell-law", "A shell that owns your parking lot so plastic stays law.", f"Parking lot shell stamped LAW, {PAINT}"),
    ("allowed-pull", "You are allowed to pull in. Allowed to hate repair season and still drive.", f"Pull in ok hate repairs still driving, {PAINT}"),
    ("not-natural", "Stop calling the painted bumper natural.", f"NATURAL stamp red X on fascia, {PAINT}"),
    ("not-inevitable", "Not inevitable. Not proof you are modern.", f"INEVITABLE MODERN stamps red X, {PAINT}"),
    ("leftover-chrome", "A leftover salute to a chrome bar that left the front end.", f"Salute to chrome bar leaving front end, {PAINT}"),
    ("costume-point", "The salute is cheerful. The costume is the point.", f"Cheerful salute on plastic costume, {PAINT}"),
    ("know-cover", "Go when the space lets you. Know which cover you are still obeying.", f"Stickman parking fascia labeled which cover, {PAINT}"),
    ("glance-cheerful", "Cheerful is how a shell stays without looking like a bar.", f"Smiling shell chrome ghost hidden, {PAINT}"),
    ("fmvss-label", "Standard two fifteen is a number that ate the chrome grin.", f"FMVSS 215 number eating chrome grin, {PAINT}"),
    ("foam-first", "The foam meets the world before the paint does.", f"Foam layer meeting world before paint, {PAINT}"),
    ("costume-repeat", "A costume that repeats on every trim without asking your nostalgia.", f"Costume repeating every TRIM no nostalgia, {PAINT}"),
    ("final-callback", "A chrome bar. A test lab. Your pull-in.", f"Final callback chrome TEST LAB YOUR PULL-IN, {PAINT}"),
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
        title="Why Your Bumper Became a Costume",
        description=(
            "Your color-matched bumper feels obvious. Early cars wore chrome bars. "
            "NHTSA's nineteen seventy-two five-mile-per-hour rule changed the front end. "
            "The painted fascia is logistics."
        ),
        tags=(
            "bumper",
            "car design",
            "chrome",
            "nhtsa",
            "pedestrian safety",
            "history",
            "why",
            "car",
            "plastic",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="CHROME GONE?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Your Bumper Became a Costume",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-bumper.json"
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

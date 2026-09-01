"""Author episode: you watch rain and treat a rubber arm as obvious."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."

CHAPTERS = [
    """Tonight you will watch rain hit a windshield and treat a rubber arm as obvious. Your eyes will expect a blade to sweep the glass as if the car grew a squeegee because squeegees are what cars do. Here is the part that should bother you. The first drivers did not agree. Many of them leaned out into the weather, wiped with a sleeve, or stopped the whole machine to argue with a storm. So why does your glass wear a rubber arm as if the arm were physics? Because shop windows already had squeegees, because early windshields arrived as a luxury pane that rain could bully, because Mary Anderson filed a United States patent in nineteen oh three for a swinging arm with a rubber blade and a lever inside the cabin, and because factories learned that visibility is easier to sell when the driver keeps both hands on the wheel instead of one hand on the sky. That is the whole plot. Your wipe is not weatherproofing by nature. It is a leftover squeegee habit that learned to pivot. You still watch the arc. The arc is flattered. That is its job. The rain did not vote. A lever did, and then an arm that taught your windshield the sweep until the sweep started calling itself sense. Sense is a word a rubber blade invented so a storm would still feel like law when the hand was gone.""",
    """Start with the glass, because the wiper stole a squeegee and then sold it back as chrome. Before enclosed cabins, before laminated safety glass, before a dashboard could host a lever, driving in rain was a negotiation with your own face. Goggles helped until they fogged. A cap helped until the wind disagreed. Some drivers carried a cloth. Some drivers simply accepted that forward motion and forward sight were not the same hobby. When windshields became a thing, they were a promise: look ahead while the world gets wet. The promise was honest. The rain was also honest. Rain does not care about your schedule. Rain cares about surface tension and gravity and the smug physics of beads. If your rubber arm still feels like the only adult option, notice that the adult option started as window-shop furniture dragged onto a road that was not a storefront. The road did not offer a ledge. The glass still wanted clearing. Clearing wanted a human arm until the human arm got tired of being outside the cabin. The arm was not a miracle. It was logistics.""",
    """Named corners, because a myth of one inventor is how a blade gets a halo it did not earn. Mary Anderson was not the only person who looked at wet glass and thought the joke was bad. She was an early loud example with paperwork. In the winter of nineteen oh two, visiting New York City, she watched a streetcar driver struggle: open the window, reach into sleet, lose the fight, lose the view, lose the rhythm of a route that could not pause for dignity. On the tenth of November, nineteen oh three, the United States Patent Office issued her patent for a device that mounted on the glass, carried a rubber blade on a hinged arm, and moved with a lever from inside. She was from Alabama. The city was New York. The problem was universal and rude. Manufacturers did not immediately beat a path to her door. That is not proof the idea was silly. It is proof that adoption is a second invention. Patents are loud. Catalogs are louder. If you still treat the wiper as a single eureka moment, file the hero separately from the hinge. Your sweep is a New York streetcar complaint wearing a century of rubber.""",
    """Watch the arm leave the hand, because a horizontal car of speed needed a hinge that did not require a torso in the storm. Early clearing tricks were honest and exhausting. Lean out. Wipe. Repeat. Stop the car. Stand in rain like a person trying to restart a thought. Split the difference with a passenger who drew the short straw. A rubber blade on an arm is a small insult to the weather with a large gift to the cabin. The blade flexes. The arm pivots. The spring presses rubber against glass with a grudge soft enough not to scratch. The lever says move now without asking the driver to become a flag in a gale. I am not giving you a list of firsts. I am pointing at the swap. We took a hand that said reach into the rain and we replaced it with an arm that said pull here. Pull is easier to teach in a manual. Pull is easier to bolt to a dozen models. Pull is easier to repeat when the line speeds up. The line is the real inventor. The line does not care about your nostalgia for a sleeve. The line cares about parts that fit and drivers who stay inside.""",
    """This is the rehook. You think the wiper is a fact, the way a door is a fact. The wiper is a policy. In a modern cabin the policy is already on, because the alternative is trusting every driver to lean into a storm at forty miles an hour with one hand on cloth and one hand on hope. Sleeves are honest. Arms are scalable. Scalable is how a machine escapes the hobbyist bench and becomes something a city can own in numbers. I am not calling you clumsy for liking a sweep. I am un-naturing the arc. The arc is a shop squeegee wearing a pivot. The pivot said rotation can be law. Law is a feeling when your eyes find a clean stripe without remembering when they learned it. If you have ever driven something with no wiper, even a golf cart in a drizzle, you know the rubber arm is not physics. It is a compromise that won a production vote. A vote is not a raindrop. A vote is a spreadsheet with elbows and a gasket catalog.""",
    """Watch the blade travel. Mass production did not invent rain. It inventoried the answer. When the same windshield had to repeat across models, the wiper became the part you could source, stamp, ship, and replace without translating a hand-wipe ritual for every chassis. Cadillac offered windshield wipers as optional equipment in the nineteen twenties before the habit went standard, which is the quiet way a luxury teaches a fleet what normal means. Trico and other suppliers turned rubber and arms into a shelf you could order from instead of a story you had to invent in a downpour. Decades later, Robert Kearns would fuss with intermittent timing so the blade could rest between drops, a useful chapter about pulses and patents, not the origin story of the arm itself. Do not make tonight a biopic about one engineer in a courtroom. Make it about the object: rubber, tension, sweep, repeat. A catalog is a quiet referendum. If your rental car has a wiper and your history book has a sleeve, that gap is not evolution. It is inventory. Inventory is how the past loses a fight without filing a complaint.""",
    """This is you, already, in the middle of the story. A Tuesday, a drizzle, a windshield you have watched sweep a thousand times without thanking a streetcar. You sit with the defroster and stare at the arc because merging would feel impossible without a stripe, which is the most modern impossibility there is. None of this makes you mechanical by nature. It makes you a person born after Mary Anderson's patent and after optional Cadillac wipers and after an arm learned to host motors, sprayers, and sensors that beep. You can feel both in the same glance: relief that you do not have to become a flag in a gale, and a tiny insult that a shop squeegee won a factory pivot. The relief is real. The insult is the sleeve failing for a second in your imagination. You paid for a clearer view with a part you never voted on. The part is cheerful. Cheerful is how an arm stays in the century without looking like an arm.""",
    """A car is a pile of compromises with glass attached. That sentence is rude and almost fair. Take the wiper away and the cabin becomes a workshop puzzle nobody wins, or a sleeve on every model until the shoulder gets soaked. Visibility, spring tension, assembly time, repair manuals: the arm is a diagram of how to see without sending the whole human into the weather, written by someone you will not meet. You still watch. The watch is a vote for a hinge that was sold as obvious. I am not telling you to hunt for a streetcar as a personality. I am telling you the personality was always the swap: a wet sleeve, a luxury pane, Mary Anderson with a lever, a Cadillac option line, a supplier shelf, a motor that forgot your pull. The crowd is still in the cabin. The crowd is you and a rental fleet treating an arc as a treaty. So what did we trade? We traded a hand that told the truth about rain for an arm that could be timed, tooled, and forgotten. That tooling is real help: fewer stops, a passenger who keeps dignity, a view you can service from a parts bin. Help can be a miracle and still be a part number. We also gained a myth that the wiper is nature and the sweep is the only adult view. We kept the squeegee and called it an arm. We kept the hand and called it history. Both can be true and still not be a reason to forget the wiper is a policy that learned manners. Deals can be rewritten. Some already were, quietly, when intermittent timing let the blade rest. The layout we kept is a pile of people who agreed not to argue with rubber.""",
    """This is you. You will put your hands on the wheel. The rain will still be there. The arm will still sweep. You will feel nothing, which is the victory. Look at the glass. That is not the sky and it is not a streetcar hero. That is a shop squeegee, a luxury pane bullied by beads, Mary Anderson in nineteen oh three with a lever and a rubber blade, a Cadillac option that taught a fleet, a supplier shelf that replaced a sleeve, a brief later chapter about intermittent pulses if you must, and an arc that still owns your merge lane so you will keep treating rubber as law. You are allowed to watch. You are allowed to hate the drizzle and still drive. Just stop calling the wiper natural, or inevitable, or proof that you are modern. Tonight, when the blade clears a stripe, look at it like a leftover salute to a hand that left the window. The salute is cheerful. The glass is the point. Go when the arc lets you. Know which arm you are still obeying.""",
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, five-second cadence)."""
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("watch-rain", "Tonight you watch rain hit a windshield and treat a rubber arm as obvious.", f"Stickman watching rain on windshield, RUBBER ARM OBVIOUS, {PAINT}"),
    ("eyes-sweep", "Your eyes expect a blade to sweep the glass.", f"Wiper blade sweeping glass arc, {PAINT}"),
    ("car-squeegee", "As if the car grew a squeegee because cars do squeegees.", f"Car sprouting squeegee like fruit, {PAINT}"),
    ("first-drivers-no", "The first drivers did not agree.", f"Early driver shaking head at wiper, {PAINT}"),
    ("lean-weather", "Many leaned out into the weather.", f"Driver leaning out window into rain, {PAINT}"),
    ("sleeve-wipe", "Wiped with a sleeve or stopped to argue with a storm.", f"Sleeve wipe vs storm argument, {PAINT}"),
    ("why-rubber-arm", "Why does your glass wear a rubber arm as if it were physics?", f"Rubber arm stamped PHYSICS with question mark, {PAINT}"),
    ("shop-squeegee", "Shop windows already had squeegees.", f"Shop window squeegee on storefront, {PAINT}"),
    ("luxury-pane", "Early windshields arrived as a luxury pane rain could bully.", f"Luxury glass pane bullied by raindrops, {PAINT}"),
    ("anderson-1903", "Mary Anderson filed a United States patent in nineteen oh three.", f"Patent paper 1903 MARY ANDERSON label, {PAINT}"),
    ("swinging-arm", "A swinging arm with a rubber blade and a lever inside.", f"Hinged arm rubber blade inside lever, {PAINT}"),
    ("both-hands", "Visibility when the driver keeps both hands on the wheel.", f"Two hands on wheel not one in rain, {PAINT}"),
    ("not-weatherproof", "Your wipe is not weatherproofing by nature.", f"WEATHERPROOF stamp red X on wiper, {PAINT}"),
    ("squeegee-pivot", "A leftover squeegee habit that learned to pivot.", f"Squeegee morphing into pivot arm, {PAINT}"),
    ("arc-flattered", "The arc is flattered. That is its job.", f"Smiling wiper arc FLATTERED badge, {PAINT}"),
    ("rain-no-vote", "The rain did not vote. A lever did.", f"Rain cloud NO VOTE, lever raising hand, {PAINT}"),
    ("sweep-sense", "The sweep taught your glass until it called itself sense.", f"Glass word SENSE appearing after sweep, {PAINT}"),
    ("start-glass", "Start with the glass.", f"Windshield labeled START, {PAINT}"),
    ("wiper-stole", "The wiper stole a squeegee and sold it back as chrome.", f"Squeegee stolen by chrome wiper arm, {PAINT}"),
    ("before-cabins", "Before enclosed cabins, before laminated safety glass.", f"Timeline before cabin laminated glass, {PAINT}"),
    ("rain-negotiation", "Driving in rain was a negotiation with your own face.", f"Driver face arguing with rain, {PAINT}"),
    ("goggles-fog", "Goggles helped until they fogged.", f"Fogged goggles on driver red X clear, {PAINT}"),
    ("motion-not-sight", "Forward motion and forward sight were not the same hobby.", f"MOTION vs SIGHT different hobbies arrows, {PAINT}"),
    ("windshield-promise", "Windshields were a promise: look ahead while the world gets wet.", f"Glass promise LOOK AHEAD wet world, {PAINT}"),
    ("rain-honest", "Rain does not care about your schedule.", f"Rain ignoring calendar SCHEDULE, {PAINT}"),
    ("beads-physics", "Rain cares about surface tension, gravity, smug beads.", f"Rain beads physics labels, {PAINT}"),
    ("shop-furniture", "Window-shop furniture dragged onto a road not a storefront.", f"Shop squeegee on highway NOT STOREFRONT, {PAINT}"),
    ("arm-tired", "Clearing wanted a human arm until the arm got tired of being outside.", f"Arm outside cabin tired, wants inside, {PAINT}"),
    ("not-miracle", "The arm was not a miracle. It was logistics.", f"LOGISTICS stamp on wiper arm not miracle, {PAINT}"),
    ("named-corners", "Named corners. One inventor is a halo the blade did not earn.", f"Halo on wiper MYTH sticker, {PAINT}"),
    ("not-only-person", "Mary Anderson was not the only person who looked at wet glass.", f"Many thought bubbles wet glass, one loud Anderson, {PAINT}"),
    ("paperwork-example", "An early loud example with paperwork.", f"Loud example with PATENT paperwork, {PAINT}"),
    ("winter-1902", "Winter nineteen oh two, visiting New York City.", f"NYC snow 1902 streetcar scene, {PAINT}"),
    ("streetcar-struggle", "She watched a streetcar driver struggle.", f"Streetcar driver reaching into sleet, {PAINT}"),
    ("nov-10-1903", "Tenth of November nineteen oh three, the Patent Office issued her patent.", f"Calendar NOV 10 1903 patent stamp, {PAINT}"),
    ("mounted-blade", "Mounted on the glass, rubber blade on a hinged arm.", f"Glass mount hinged arm rubber blade, {PAINT}"),
    ("lever-inside", "Moved with a lever from inside the cabin.", f"Inside lever pulling arm, {PAINT}"),
    ("universal-rude", "The problem was universal and rude.", f"UNIVERSAL RUDE cloud over wet glass, {PAINT}"),
    ("no-beaten-path", "Manufacturers did not immediately beat a path to her door.", f"Empty path to factory door, {PAINT}"),
    ("adoption-second", "Adoption is a second invention.", f"INVENTION 1 idea INVENTION 2 adoption, {PAINT}"),
    ("patents-loud", "Patents are loud. Catalogs are louder.", f"Patent megaphone vs catalog louder, {PAINT}"),
    ("streetcar-complaint", "Your sweep is a New York streetcar complaint wearing a century of rubber.", f"Streetcar complaint wearing rubber century coat, {PAINT}"),
    ("arm-leaves-hand", "Watch the arm leave the hand.", f"Hand releasing wiper arm walking away, {PAINT}"),
    ("speed-no-torso", "A car of speed needed a hinge without a torso in the storm.", f"Hinge safe inside vs torso in storm red X, {PAINT}"),
    ("lean-wipe-repeat", "Lean out. Wipe. Repeat.", f"Three panel LEAN WIPE REPEAT, {PAINT}"),
    ("small-insult", "A rubber blade on an arm is a small insult to the weather.", f"Rubber blade insulting rain cloud, {PAINT}"),
    ("blade-flexes", "The blade flexes. The arm pivots.", f"Flexing blade pivoting arm diagram, {PAINT}"),
    ("spring-grudge", "Spring presses rubber against glass with a grudge soft enough not to scratch.", f"Spring pressing rubber GRUDGE SOFT, {PAINT}"),
    ("pull-not-flag", "Pull here without becoming a flag in a gale.", f"PULL HERE lever vs flag in gale red X, {PAINT}"),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", f"FIRSTS list red X SWAP arrow, {PAINT}"),
    ("hand-to-arm", "A hand that said reach into rain replaced by an arm that said pull here.", f"REACH RAIN hand vs PULL HERE arm, {PAINT}"),
    ("bolt-dozen", "Easier to bolt to a dozen models.", f"Same wiper bolting twelve car models, {PAINT}"),
    ("line-speeds", "Easier to repeat when the line speeds up.", f"Assembly line repeating wiper arms faster, {PAINT}"),
    ("line-inventor", "The line is the real inventor.", f"Factory line wearing INVENTOR badge, {PAINT}"),
    ("parts-fit", "The line cares about parts that fit and drivers who stay inside.", f"Wiper part fitting slot STAY INSIDE, {PAINT}"),
    ("rehook-fact", "Rehook: you think the wiper is a fact like a door.", f"Wiper vs door both labeled FACT, {PAINT}"),
    ("wiper-policy", "The wiper is a policy.", f"Wiper stamped POLICY, {PAINT}"),
    ("trust-lean-storm", "Trusting every driver to lean into a storm at forty miles an hour.", f"Driver leaning at 40 MPH TRUST red X, {PAINT}"),
    ("hand-cloth-hope", "One hand on cloth and one hand on hope.", f"Cloth in one hand HOPE in other, {PAINT}"),
    ("sleeves-honest", "Sleeves are honest.", f"Sleeve wipe HONEST stamp, {PAINT}"),
    ("arms-scalable", "Arms are scalable.", f"Wiper arms multiplying SCALABLE, {PAINT}"),
    ("city-numbers", "Scalable is how a machine escapes the bench and a city owns it in numbers.", f"Bench to city fleet many wipers, {PAINT}"),
    ("un-nature-arc", "Not calling you clumsy. Un-naturing the arc.", f"NATURE sticker peeling off wiper arc, {PAINT}"),
    ("squeegee-pivot-costume", "The arc is a shop squeegee wearing a pivot.", f"Shop squeegee inside pivot costume, {PAINT}"),
    ("rotation-law", "The pivot said rotation can be law.", f"Pivot stamped ROTATION LAW, {PAINT}"),
    ("clean-stripe", "Eyes find a clean stripe without remembering when they learned.", f"Clean stripe on glass blank memory bubble, {PAINT}"),
    ("production-vote", "A compromise that won a production vote.", f"Ballot box PRODUCTION VOTE wiper wins, {PAINT}"),
    ("spreadsheet-gasket", "A vote is a spreadsheet with elbows and a gasket catalog.", f"Spreadsheet elbows gasket catalog, {PAINT}"),
    ("blade-travel", "Watch the blade travel.", f"Wiper blade walking across glass, {PAINT}"),
    ("mass-inventoried", "Mass production did not invent rain. It inventoried the answer.", f"INVENT RAIN red X INVENTORIED answer check, {PAINT}"),
    ("same-windshield", "The same windshield had to repeat across models.", f"Identical windshields row of cars, {PAINT}"),
    ("source-stamp-ship", "Source, stamp, ship, and replace without translating a hand-wipe ritual.", f"Wiper parts SOURCE STAMP SHIP boxes, {PAINT}"),
    ("cadillac-optional", "Cadillac offered wipers as optional equipment in the nineteen twenties.", f"Optional wiper tag 1920s luxury car generic, {PAINT}"),
    ("luxury-teaches", "A luxury teaches a fleet what normal means.", f"Luxury car teaching fleet NORMAL arrow, {PAINT}"),
    ("trico-shelf", "Trico and suppliers turned rubber and arms into a shelf you could order.", f"Supplier shelf TRICO rubber arms order, {PAINT}"),
    ("kearns-brief", "Robert Kearns fussed with intermittent timing so the blade could rest.", f"Intermittent pulse timer brief label not hero, {PAINT}"),
    ("not-biopic", "Not tonight a biopic about one engineer in a courtroom.", f"COURROOM BIOPIC red X object focus instead, {PAINT}"),
    ("object-rubber", "Make it about the object: rubber, tension, sweep, repeat.", f"Rubber tension sweep repeat cycle diagram, {PAINT}"),
    ("quiet-referendum", "A catalog is a quiet referendum.", f"Catalog voting booth QUIET REFERENDUM, {PAINT}"),
    ("rental-vs-sleeve", "Rental car has a wiper, history book has a sleeve.", f"Rental wiper vs book sleeve gap, {PAINT}"),
    ("inventory-fight", "That gap is inventory. Inventory is how the past loses without complaining.", f"Inventory shelf beating sleeve wipe, {PAINT}"),
    ("this-is-you", "This is you. A Tuesday. A drizzle. A windshield watched a thousand times.", f"Stickman Tuesday drizzle windshield, {PAINT}"),
    ("stare-arc", "You stare at the arc because merging needs a stripe.", f"Merging stickman staring at clean stripe, {PAINT}"),
    ("modern-impossibility", "The most modern impossibility there is.", f"MODERN IMPOSSIBILITY cloud over merge, {PAINT}"),
    ("not-mechanical", "None of this makes you mechanical by nature.", f"MECHANICAL NATURE stamp red X, {PAINT}"),
    ("born-after-patent", "Born after Mary Anderson patent and optional Cadillac wipers.", f"Timeline 1903 patent then optional wiper, {PAINT}"),
    ("arm-hosts", "An arm learned to host motors, sprayers, sensors that beep.", f"Wiper with motor sprayer sensor beep icons, {PAINT}"),
    ("relief-not-flag", "Relief you do not become a flag in a gale.", f"Safe inside vs flag in gale happy stickman, {PAINT}"),
    ("insult-squeegee", "A tiny insult that a shop squeegee won a factory pivot.", f"Sad squeegee winning factory pivot insult cloud, {PAINT}"),
    ("never-voted", "You paid for a clearer view with a part you never voted on.", f"Receipt wiper part never voted, {PAINT}"),
    ("cheerful-arm", "Cheerful is how an arm stays without looking like an arm.", f"Smiling wiper arm disguise, {PAINT}"),
    ("test-wanted-hand", "A test used to want your hand.", f"Rain test WANT HAND speech bubble, {PAINT}"),
    ("blade-forgot", "Rubber blade that forgot the streetcar.", f"Blade rotating streetcar forgotten ghost, {PAINT}"),
    ("compromises-glass", "A car is a pile of compromises with glass attached.", f"Compromise stack with glass on top, {PAINT}"),
    ("take-wiper-away", "Take the wiper away and the cabin becomes a workshop puzzle.", f"Cabin puzzle pieces no wiper, {PAINT}"),
    ("shoulder-soaked", "Or a sleeve on every model until the shoulder gets soaked.", f"Soaked shoulder BREAK sign, {PAINT}"),
    ("diagram-see", "Visibility, spring tension, assembly: see without sending the human into weather.", f"Diagram human inside arm clears rain, {PAINT}"),
    ("watch-vote", "The watch is a vote for a hinge sold as obvious.", f"Watching wiper voting OBVIOUS hinge, {PAINT}"),
    ("not-streetcar-personality", "Not telling you to hunt a streetcar as a personality.", f"Streetcar personality hat red X, {PAINT}"),
    ("swap-personality", "The personality was the swap: sleeve, pane, Anderson, Cadillac, shelf, motor.", f"Six icons sleeve pane Anderson Cadillac shelf motor, {PAINT}"),
    ("crowd-cabin", "The crowd is still in the cabin.", f"Many stickmen in one cabin watching wipe, {PAINT}"),
    ("arc-treaty", "You and a rental fleet treating an arc as a treaty.", f"Rental cars arc treaty paper, {PAINT}"),
    ("treaty-blind", "The treaty cannot see a workshop.", f"Treaty blindfold workshop behind, {PAINT}"),
    ("cabinet-glass", "A log in a cabinet you will never open. The real windshield.", f"Locked cabinet LOG real windshield, {PAINT}"),
    ("squeegee-under", "The squeegee is still under the blade.", f"Squeegee ghost under rubber blade, {PAINT}"),
    ("what-trade", "So what did we trade?", f"Trade scale sleeve vs wiper arm, {PAINT}"),
    ("hand-truth", "A hand that told the truth about rain.", f"Hand in rain honest TRUTH arrow, {PAINT}"),
    ("arm-tooled", "For an arm that could be timed, tooled, and forgotten.", f"Wiper on factory timer TOOLED, {PAINT}"),
    ("fewer-stops", "Fewer stops, passenger keeps dignity, view from a parts bin.", f"Happy passenger parts bin view, {PAINT}"),
    ("miracle-part", "Help can be a miracle and still be a part number.", f"Halo on wiper PART NUMBER tag, {PAINT}"),
    ("wiper-nature-myth", "A myth that the wiper is nature, the only adult view.", f"WIPER=NATURE myth ADULT VIEW, {PAINT}"),
    ("sleeve-joke", "A myth that a sleeve is a joke you outgrow.", f"SLEEVE JOKE stamp red X, {PAINT}"),
    ("line-word-adult", "Adult is a word the line uses.", f"Factory line holding word ADULT, {PAINT}"),
    ("kept-squeegee-arm", "We kept the squeegee and called it an arm.", f"Squeegee renamed ARM, {PAINT}"),
    ("kept-hand-history", "We kept the hand and called it history.", f"Hand in museum labeled HISTORY, {PAINT}"),
    ("policy-manners", "The wiper is a policy that learned manners.", f"Policy wiper in polite bow tie, {PAINT}"),
    ("intermittent-rest", "Intermittent timing let the blade rest between drops.", f"Blade resting between drops INTERMITTENT, {PAINT}"),
    ("sleeve-truce", "A sleeve is a truce you wear.", f"Sleeve wipe TRUCE label, {PAINT}"),
    ("layout-rubber", "The layout we kept is people who agreed not to argue with rubber.", f"People nodding at rubber arm no argue, {PAINT}"),
    ("hands-wheel", "You put your hands on the wheel. The rain will still be there.", f"Callback hands on wheel rain on glass, {PAINT}"),
    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at clean glass, {PAINT}"),
    ("look-glass", "Look at the glass. Not the sky and not a streetcar hero.", f"Glass between red X sky and red X hero, {PAINT}"),
    ("named-stack", "Squeegee, luxury pane, Anderson nineteen oh three, Cadillac option, supplier shelf.", f"Stack icons squeegee pane Anderson Cadillac shelf, {PAINT}"),
    ("arc-law", "An arc that owns your merge lane so rubber stays law.", f"Merge lane wiper arc stamped LAW, {PAINT}"),
    ("allowed-watch", "You are allowed to watch. Allowed to hate drizzle and still drive.", f"Watch ok hate drizzle still driving, {PAINT}"),
    ("not-natural", "Stop calling the wiper natural.", f"NATURAL stamp red X on wiper, {PAINT}"),
    ("not-inevitable", "Not inevitable. Not proof you are modern.", f"INEVITABLE MODERN stamps red X, {PAINT}"),
    ("leftover-hand", "A leftover salute to a hand that left the window.", f"Salute to hand leaving window, {PAINT}"),
    ("glass-point", "The salute is cheerful. The glass is the point.", f"Cheerful salute on clean glass, {PAINT}"),
    ("know-arm", "Go when the arc lets you. Know which arm you are still obeying.", f"Stickman driving arc labeled which arm, {PAINT}"),
    ("glance-cheerful", "Cheerful is how a wiper stays without looking like a sleeve.", f"Smiling wiper sleeve ghost hidden, {PAINT}"),
    ("final-callback", "A squeegee. New York. Your glass.", f"Final callback squeegee NYC label your glass, {PAINT}"),
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
        title="Why Rain Needed a Rubber Arm",
        description=(
            "Your wiper feels obvious. Early drivers wiped by hand. "
            "Mary Anderson patented a rubber blade on an arm in nineteen oh three. "
            "Cadillac made wipers optional, then normal. The sweep is logistics."
        ),
        tags=(
            "wiper",
            "windshield",
            "rain",
            "mary anderson",
            "history",
            "why",
            "car",
            "patent",
            "cadillac",
            "invention",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="RUBBER ARM?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Rain Needed a Rubber Arm",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-rain.json"
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

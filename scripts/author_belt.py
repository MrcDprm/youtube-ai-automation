"""Author episode: you click a strap and treat sitting still as obvious."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."

CHAPTERS = [
    """Tonight you will click a strap across your chest and treat sitting still as obvious. Your hand will find a buckle as if the car grew a ribbon because cars do ribbons. Here is the part that should bother you. The first motorists did not agree. Many of them rode on benches with nothing but hope and a hard stop between them and the windshield. So why does your seat wear a strap as if the strap were physics? Because aircraft already had harness logic, because lap belts arrived as a half answer that could slide, because Nils Bohlin at Volvo patented a three-point belt in nineteen fifty nine and bolted it to the Amazon as a standard part, because Volvo then opened the patent so rivals could copy the geometry without a royalty fight, and because factories learned that a body held at three points is easier to certify than a lecture about caution. That is the whole plot. Your click is not safety by nature. It is a leftover harness habit that learned to live in a cabin. You still buckle. The buckle is flattered. That is its job. The road did not vote. A strap did, and then a latch that taught your shoulder the diagonal until the diagonal started calling itself sense. Sense is a word a buckle invented so a bench would still feel like law when the harness was gone.""",
    """Start with the bench, because the belt stole a harness and then sold it back as nylon. Before enclosed cabins, before laminated glass, before a dashboard could host a retractor, riding in a car was a negotiation with momentum you could not see. Early drivers leaned. Early passengers held a rail. Some cars offered nothing but upholstery and the social contract that you would not lunge. When lap belts appeared, they were honest and incomplete. A strap across the lap says stay in the seat. It does not say stay with the seat when the seat moves faster than your ribs remember. If your three-point still feels like the only adult option, notice that the adult option started as aviation paperwork dragged onto a road that was not a runway. The road did not offer ejection seats. The bench still wanted holding. Holding wanted a human grip until the human grip got tired of being the only plan. The grip was not a miracle. It was logistics.""",
    """Named corners, because a myth of one inventor is how a strap gets a halo it did not earn. Nils Bohlin was not the only person who looked at a bench and thought the joke was incomplete. He was an early loud example with a patent and a Swedish factory behind him. Born in nineteen twenty, trained in aircraft work, hired by Volvo after helping Saab think about how a body leaves a seat when the seat is no longer optional. On the thirteenth of August, nineteen fifty nine, the United States Patent Office issued his patent for a three-point safety belt. Volvo put it on the Amazon model the same year as standard equipment, which is the quiet way a luxury teaches a fleet what normal means. Volvo then shared the design. That is not proof engineers are saints. It is proof that adoption is a second invention, and that a shared geometry beats a locked drawer when the product is a strap everyone needs to copy. If you still treat the belt as a single eureka moment, file the hero separately from the latch. Your click is a Gothenburg harness wearing a century of nylon.""",
    """Watch the strap leave the hand, because a horizontal car of speed needed a diagonal that did not require a torso to invent itself mid-turn. Early restraint tricks were honest and exhausting. Grip the rail. Brace a foot. Trust the door. Repeat. A three-point belt is a small insult to momentum with a large gift to the cabin. The lap section anchors low. The shoulder section crosses the chest without asking the driver to assemble a harness like a parachute rig before every grocery run. The buckle says click here without asking the passenger to read a manual in a parking lot. I am not giving you a list of firsts. I am pointing at the swap. We took a bench that said hold on and we replaced it with a strap that said route force here. Route is easier to teach in a showroom. Route is easier to bolt to a dozen models. Route is easier to repeat when the line speeds up. The line is the real inventor. The line does not care about your nostalgia for an unbuckled bench. The line cares about parts that fit and bodies that stay inside the plan.""",
    """This is the rehook. You think the belt is a fact, the way a door is a fact. The belt is a policy. In a modern cabin the policy is already on, because the alternative is trusting every driver to remember a lecture about momentum while merging at forty miles an hour with one hand on coffee and one hand on hope. Hope is honest. Straps are scalable. Scalable is how a restraint escapes the test bench and becomes something a city can own in numbers. I am not calling you clumsy for liking a click. I am un-naturing the diagonal. The diagonal is a harness wearing a retractor. The retractor said slack can be law. Law is a feeling when your shoulder finds a strap without remembering when it learned it. If you have ever ridden in something with no belt, even a golf cart on a slope, you know the three-point is not physics. It is a compromise that won a production vote. A vote is not a bench. A vote is a spreadsheet with webbing and a latch catalog.""",
    """Watch the webbing travel. Mass production did not invent momentum. It inventoried the answer. When the same seat had to repeat across models, the belt became the part you could source, stamp, ship, and replace without translating a harness ritual for every chassis. Retractors, pretensioners, warning chimes: decades later the strap could spool and tighten, a useful chapter about pulses and sensors, not the origin story of the diagonal itself. Do not make tonight a biopic about one engineer in a courtroom. Make it about the object: nylon, latch, route, repeat. A catalog is a quiet referendum. If your rental car has a three-point and your history book has a bare bench, that gap is not evolution. It is inventory. Inventory is how the past loses a fight without filing a complaint. Volvo sharing the patent is the loudest quiet page in that inventory. A page is not a halo. A page is a factory agreeing that a strap should fit more than one badge.""",
    """This is you, already, in the middle of the story. A Tuesday, a parking lot, a click you have performed a thousand times without thanking a Swedish engineer. You reach across your chest because starting would feel reckless without a strap, which is the most modern impossibility there is. None of this makes you cautious by nature. It makes you a person born after the Amazon in nineteen fifty nine and after lap belts learned a shoulder and after a retractor learned to host a chime that beeps. You can feel both in the same motion: relief that you do not have to invent a harness before every errand, and a tiny insult that an aircraft habit won a cabin latch. The relief is real. The insult is the unbuckled bench failing for a second in your imagination. You paid for a held body with a part you never voted on. The part is cheerful. Cheerful is how a strap stays in the century without looking like a harness.""",
    """A car is a pile of compromises with a bench attached. That sentence is rude and almost fair. Take the belt away and the cabin becomes a workshop puzzle nobody wins, or a lecture on every model until the shoulder gives up. Routing, latch geometry, assembly time, replacement webbing: the strap is a diagram of how to stay without sending the whole human into the windshield story, written by someone you will not meet. You still click. The click is a vote for a diagonal that was sold as obvious. I am not telling you to hunt for a bare bench as a personality. I am telling you the personality was always the swap: an open bench, a lap belt that slid, Nils Bohlin with a three-point, a Volvo Amazon line, a shared patent, a retractor that forgot your pull. The crowd is still in the cabin. The crowd is you and a rental fleet treating a strap as a treaty. So what did we trade? We traded a bench that told the truth about momentum for a strap that could be timed, tooled, and forgotten. That tooling is real help: fewer lectures, a passenger who keeps dignity, a body you can route with a parts bin. Help can be a miracle and still be a part number. We also gained a myth that the belt is nature and the click is the only adult start. We kept the harness and called it a seatbelt. We kept the bench and called it history. Both can be true and still not be a reason to forget the belt is a policy that learned manners. Deals can be rewritten. Some already were, quietly, when pretensioners tightened the slack. The layout we kept is a pile of people who agreed not to argue with nylon.""",
    """This is you. You will put your hands on the wheel. The strap will still be there. You will feel nothing, which is the victory. Look at the buckle. That is not the sky and it is not a Swedish hero. That is a bench with no plan, a lap belt that half answered, Nils Bohlin in nineteen fifty nine with a three-point and a Volvo Amazon, a shared patent that taught rivals, a retractor shelf that replaced a grip, a brief later chapter about pretensioners if you must, and a diagonal that still owns your parking lot so you will keep treating nylon as law. You are allowed to click. You are allowed to hate the chime and still drive. Just stop calling the belt natural, or inevitable, or proof that you are modern. Tonight, when the latch catches, look at it like a leftover salute to a bench that left the harness. The salute is cheerful. The webbing is the point. Go when the strap lets you. Know which diagonal you are still obeying.""",
]


def _stamp(index: int) -> str:
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("click-strap", "Tonight you click a strap across your chest and treat sitting still as obvious.", f"Stickman clicking chest strap SITTING STILL OBVIOUS, {PAINT}"),
    ("hand-buckle", "Your hand finds a buckle as if the car grew a ribbon.", f"Hand finding buckle CAR RIBBON label, {PAINT}"),
    ("cars-do-ribbons", "Because cars do ribbons.", f"Car sprouting ribbon like fruit, {PAINT}"),
    ("first-no-agree", "The first motorists did not agree.", f"Early motorist shaking head at belt, {PAINT}"),
    ("bench-hope", "Many rode on benches with nothing but hope and a hard stop.", f"Bench rider HOPE vs HARD STOP label, {PAINT}"),
    ("why-strap-physics", "Why does your seat wear a strap as if the strap were physics?", f"Strap stamped PHYSICS with question mark, {PAINT}"),
    ("aircraft-harness", "Aircraft already had harness logic.", f"Airplane harness logic diagram, {PAINT}"),
    ("lap-half-answer", "Lap belts arrived as a half answer that could slide.", f"Lap belt sliding HALF ANSWER label, {PAINT}"),
    ("bohlin-1959", "Nils Bohlin at Volvo patented a three-point belt in nineteen fifty nine.", f"Patent paper 1959 NILS BOHLIN VOLVO, {PAINT}"),
    ("amazon-standard", "Bolted it to the Amazon as a standard part.", f"Volvo Amazon car with STANDARD BELT badge, {PAINT}"),
    ("opened-patent", "Volvo opened the patent so rivals could copy the geometry.", f"Open patent drawer RIVALS COPY label, {PAINT}"),
    ("three-points-certify", "A body held at three points is easier to certify than a lecture.", f"Three anchor points vs LECTURE red X, {PAINT}"),
    ("not-safety-nature", "Your click is not safety by nature.", f"SAFETY BY NATURE stamp red X on buckle, {PAINT}"),
    ("harness-habit", "A leftover harness habit that learned to live in a cabin.", f"Harness morphing into cabin belt, {PAINT}"),
    ("buckle-flattered", "The buckle is flattered. That is its job.", f"Smiling buckle FLATTERED badge, {PAINT}"),
    ("road-no-vote", "The road did not vote. A strap did.", f"Road NO VOTE strap raising hand, {PAINT}"),
    ("diagonal-sense", "The diagonal taught your shoulder until it called itself sense.", f"Shoulder diagonal word SENSE appearing, {PAINT}"),
    ("start-bench", "Start with the bench.", f"Car bench labeled START, {PAINT}"),
    ("belt-stole-harness", "The belt stole a harness and sold it back as nylon.", f"Harness stolen by nylon belt, {PAINT}"),
    ("before-retractor", "Before enclosed cabins, before laminated glass, before a retractor.", f"Timeline before cabin glass retractor, {PAINT}"),
    ("momentum-negotiation", "Riding was a negotiation with momentum you could not see.", f"Driver negotiating with invisible MOMENTUM, {PAINT}"),
    ("lean-rail", "Early drivers leaned. Early passengers held a rail.", f"Driver leaning passenger holding rail, {PAINT}"),
    ("upholstery-contract", "Some cars offered upholstery and the social contract you would not lunge.", f"Upholstery SOCIAL CONTRACT no lunge, {PAINT}"),
    ("lap-honest", "When lap belts appeared, they were honest and incomplete.", f"Lap belt HONEST INCOMPLETE labels, {PAINT}"),
    ("stay-in-seat", "A strap across the lap says stay in the seat.", f"Lap strap STAY IN SEAT arrow, {PAINT}"),
    ("seat-moves-faster", "It does not say stay with the seat when the seat moves faster than your ribs.", f"Seat moving faster than ribs diagram, {PAINT}"),
    ("aviation-paperwork", "Aviation paperwork dragged onto a road not a runway.", f"Aviation papers dragged onto highway NOT RUNWAY, {PAINT}"),
    ("bench-wanted-holding", "The bench still wanted holding.", f"Bench speech bubble WANT HOLDING, {PAINT}"),
    ("grip-tired", "Holding wanted a human grip until the grip got tired of being the only plan.", f"Tired hand grip ONLY PLAN label, {PAINT}"),
    ("not-miracle", "The grip was not a miracle. It was logistics.", f"LOGISTICS stamp on grip not miracle, {PAINT}"),
    ("named-corners", "Named corners. One inventor is a halo the strap did not earn.", f"Halo on belt MYTH sticker, {PAINT}"),
    ("not-only-person", "Nils Bohlin was not the only person who looked at a bench.", f"Many thought bubbles bench one loud Bohlin, {PAINT}"),
    ("patent-factory", "An early loud example with a patent and a Swedish factory.", f"Loud example PATENT SWEDISH FACTORY, {PAINT}"),
    ("born-1920", "Born in nineteen twenty, trained in aircraft work.", f"Timeline 1920 AIRCRAFT WORK label, {PAINT}"),
    ("saab-volvo", "Hired by Volvo after helping Saab think about how a body leaves a seat.", f"Saab to Volvo arrow body leaves seat, {PAINT}"),
    ("aug-13-1959", "Thirteenth of August nineteen fifty nine, the Patent Office issued his patent.", f"Calendar AUG 13 1959 patent stamp, {PAINT}"),
    ("three-point-patent", "Patent for a three-point safety belt.", f"Three-point belt patent diagram, {PAINT}"),
    ("amazon-same-year", "Volvo put it on the Amazon the same year as standard equipment.", f"Amazon 1959 STANDARD EQUIPMENT badge, {PAINT}"),
    ("luxury-teaches", "The quiet way a luxury teaches a fleet what normal means.", f"Luxury car teaching fleet NORMAL arrow, {PAINT}"),
    ("shared-design", "Volvo then shared the design.", f"Shared design open hands rivals, {PAINT}"),
    ("adoption-second", "Adoption is a second invention.", f"INVENTION 1 idea INVENTION 2 adoption, {PAINT}"),
    ("shared-geometry", "A shared geometry beats a locked drawer.", f"Shared geometry vs locked drawer wins, {PAINT}"),
    ("gothenburg-harness", "Your click is a Gothenburg harness wearing a century of nylon.", f"Gothenburg harness wearing nylon century coat, {PAINT}"),
    ("strap-leaves-hand", "Watch the strap leave the hand.", f"Hand releasing strap walking away, {PAINT}"),
    ("speed-diagonal", "A car of speed needed a diagonal without a torso inventing itself mid-turn.", f"Diagonal safe vs torso inventing red X, {PAINT}"),
    ("grip-rail", "Grip the rail. Brace a foot. Trust the door. Repeat.", f"Three panel GRIP RAIL BRACE TRUST REPEAT, {PAINT}"),
    ("small-insult", "A three-point belt is a small insult to momentum.", f"Belt insulting momentum cloud, {PAINT}"),
    ("lap-anchors", "The lap section anchors low.", f"Lap section ANCHOR LOW arrow, {PAINT}"),
    ("shoulder-crosses", "The shoulder section crosses the chest without a parachute rig.", f"Shoulder crosses chest no parachute rig, {PAINT}"),
    ("buckle-click", "The buckle says click here without a manual in a parking lot.", f"Buckle CLICK HERE no manual, {PAINT}"),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", f"FIRSTS red X SWAP arrow, {PAINT}"),
    ("bench-hold-on", "We took a bench that said hold on.", f"Bench speech bubble HOLD ON, {PAINT}"),
    ("strap-route", "We replaced it with a strap that said route force here.", f"Strap ROUTE FORCE HERE arrows, {PAINT}"),
    ("route-showroom", "Route is easier to teach in a showroom.", f"Showroom teaching ROUTE checkmark, {PAINT}"),
    ("route-bolt", "Route is easier to bolt to a dozen models.", f"Same belt bolting dozen car models, {PAINT}"),
    ("line-inventor", "The line is the real inventor.", f"Factory line labeled REAL INVENTOR, {PAINT}"),
    ("unbuckled-bench", "The line does not care about nostalgia for an unbuckled bench.", f"Unbuckled bench nostalgia red X, {PAINT}"),
    ("rehook-fact", "You think the belt is a fact, the way a door is a fact.", f"Belt vs door both labeled FACT, {PAINT}"),
    ("belt-policy", "The belt is a policy.", f"POLICY stamp on seatbelt, {PAINT}"),
    ("lecture-merge", "The alternative is trusting a lecture about momentum while merging.", f"Lecture while merging red X strap wins, {PAINT}"),
    ("hope-honest", "Hope is honest. Straps are scalable.", f"HOPE honest STRAPS scalable scales, {PAINT}"),
    ("un-naturing", "I am un-naturing the diagonal.", f"Diagonal NATURAL stamp peeling off, {PAINT}"),
    ("harness-retractor", "The diagonal is a harness wearing a retractor.", f"Harness wearing retractor costume, {PAINT}"),
    ("slack-law", "The retractor said slack can be law.", f"Retractor spool SLACK IS LAW, {PAINT}"),
    ("golf-cart", "If you rode something with no belt, even a golf cart on a slope.", f"Golf cart slope no belt, {PAINT}"),
    ("not-physics", "You know the three-point is not physics.", f"PHYSICS stamp red X on three-point, {PAINT}"),
    ("production-vote", "A compromise that won a production vote.", f"Production line voting for belt wins, {PAINT}"),
    ("spreadsheet-webbing", "A vote is a spreadsheet with webbing and a latch catalog.", f"Spreadsheet webbing latch catalog, {PAINT}"),
    ("webbing-travel", "Watch the webbing travel.", f"Webbing spooling across frame, {PAINT}"),
    ("inventoried-answer", "Mass production inventoried the answer.", f"Factory inventory belt parts shelf, {PAINT}"),
    ("source-stamp-ship", "Source, stamp, ship, replace without a harness ritual.", f"SOURCE STAMP SHIP REPLACE conveyor, {PAINT}"),
    ("retractor-chapter", "Retractors, pretensioners, warning chimes: a later chapter.", f"Retractor pretensioner chime LATER CHAPTER, {PAINT}"),
    ("object-nylon", "Make it about the object: nylon, latch, route, repeat.", f"NYLON LATCH ROUTE REPEAT icons, {PAINT}"),
    ("catalog-referendum", "A catalog is a quiet referendum.", f"Quiet catalog REFERENDUM whisper, {PAINT}"),
    ("rental-vs-bench", "Your rental has a three-point and your history book has a bare bench.", f"Rental belt vs history bare bench gap, {PAINT}"),
    ("inventory-fight", "Inventory is how the past loses a fight without filing a complaint.", f"Past losing fight INVENTORY filing cabinet, {PAINT}"),
    ("volvo-sharing", "Volvo sharing the patent is the loudest quiet page.", f"Volvo open patent LOUD QUIET PAGE, {PAINT}"),
    ("page-not-halo", "A page is not a halo. A factory agreeing a strap should fit more than one badge.", f"Factory nodding strap fits many badges, {PAINT}"),
    ("this-is-you", "This is you, already, in the middle of the story.", f"Stickman labeled THIS IS YOU parking lot, {PAINT}"),
    ("tuesday-click", "A Tuesday, a parking lot, a click without thanking a Swedish engineer.", f"Tuesday parking lot click no thank you, {PAINT}"),
    ("reach-chest", "You reach across your chest because starting would feel reckless.", f"Hand reaching chest RECKLESS without strap, {PAINT}"),
    ("modern-impossibility", "The most modern impossibility there is.", f"MODERN IMPOSSIBILITY stamp on merge, {PAINT}"),
    ("after-amazon", "Born after the Amazon in nineteen fifty nine.", f"Timeline after 1959 Amazon belt, {PAINT}"),
    ("lap-shoulder", "After lap belts learned a shoulder.", f"Lap belt growing shoulder arrow, {PAINT}"),
    ("chime-beeps", "After a retractor learned to host a chime that beeps.", f"Retractor with beeping chime, {PAINT}"),
    ("relief-insult", "Relief you do not invent a harness, insult an aircraft habit won.", f"Relief checkmark insult aircraft habit wins, {PAINT}"),
    ("unbuckled-imagination", "The unbuckled bench failing in your imagination.", f"Ghost bare bench failing imagination, {PAINT}"),
    ("never-voted", "You paid for a held body with a part you never voted on.", f"Held body receipt NEVER VOTED stamp, {PAINT}"),
    ("cheerful-strap", "Cheerful is how a strap stays without looking like a harness.", f"Smiling strap harness costume hidden, {PAINT}"),
    ("compromises-bench", "A car is a pile of compromises with a bench attached.", f"Car pile COMPROMISES bench bolted, {PAINT}"),
    ("take-belt-away", "Take the belt away and the cabin becomes a workshop puzzle.", f"Cabin puzzle nobody wins no belt, {PAINT}"),
    ("routing-geometry", "Routing, latch geometry, assembly time, replacement webbing.", f"ROUTING GEOMETRY ASSEMBLY WEBBING labels, {PAINT}"),
    ("diagram-stay", "The strap is a diagram of how to stay without the windshield story.", f"Strap diagram STAY without windshield story, {PAINT}"),
    ("click-vote", "The click is a vote for a diagonal sold as obvious.", f"Click lever voting DIAGONAL OBVIOUS, {PAINT}"),
    ("personality-swap", "The personality was always the swap.", f"SWAP arrow open bench to three-point, {PAINT}"),
    ("open-bench", "An open bench, a lap belt that slid.", f"Open bench lap belt sliding, {PAINT}"),
    ("bohlin-three-point", "Nils Bohlin with a three-point.", f"Bohlin stick figure three-point belt, {PAINT}"),
    ("shared-patent-line", "A shared patent, a retractor that forgot your pull.", f"Shared patent retractor forgot pull, {PAINT}"),
    ("treaty-crowd", "You and a rental fleet treating a strap as a treaty.", f"Rental fleet strap TREATY handshake, {PAINT}"),
    ("what-we-traded", "We traded a bench that told the truth about momentum.", f"Bench truth MOMENTUM traded away, {PAINT}"),
    ("timed-tooled", "For a strap that could be timed, tooled, and forgotten.", f"Timed tooled forgotten belt on line, {PAINT}"),
    ("real-help", "Real help: fewer lectures, dignity, a body you can route.", f"Fewer lectures dignity ROUTE body, {PAINT}"),
    ("miracle-part-number", "Help can be a miracle and still be a part number.", f"MIRACLE and PART NUMBER both true, {PAINT}"),
    ("myth-nature", "A myth that the belt is nature and the click is the only adult start.", f"MYTH NATURE ADULT START stamps, {PAINT}"),
    ("harness-seatbelt", "We kept the harness and called it a seatbelt.", f"Harness wearing SEATBELT name tag, {PAINT}"),
    ("bench-history", "We kept the bench and called it history.", f"Bench labeled HISTORY museum, {PAINT}"),
    ("policy-manners", "The belt is a policy that learned manners.", f"Policy belt in polite bow tie, {PAINT}"),
    ("pretensioner-slack", "Pretensioners tightened the slack quietly.", f"Pretensioner tightening slack QUIETLY, {PAINT}"),
    ("lap-only-era", "There was an era when the lap belt was the whole sermon.", f"Lap belt preaching WHOLE SERMON label, {PAINT}"),
    ("shoulder-separate", "Shoulder straps arrived as a separate homework assignment.", f"Shoulder strap SEPARATE HOMEWORK label, {PAINT}"),
    ("buckle-sound", "The click sound is a contract your ears learned to trust.", f"Buckle click sound CONTRACT ears trust, {PAINT}"),
    ("webbing-fray", "Webbing frays, buckles swap, the geometry stays.", f"Frayed webbing new buckle same GEOMETRY, {PAINT}"),
    ("regulators-shelf", "Regulators did not invent the diagonal. They shelved it.", f"Regulator placing diagonal on SHELF not invent, {PAINT}"),
    ("rental-fleet", "A rental fleet is a treaty written in identical latches.", f"Identical rental car latches TREATY label, {PAINT}"),
    ("shoulder-memory", "Your shoulder remembers a diagonal you never chose.", f"Shoulder with diagonal MEMORY ghost, {PAINT}"),
    ("bench-ghost", "The bare bench is still a ghost in every cabin.", f"Bare bench ghost in modern cabin, {PAINT}"),
    ("nylon-cheerful", "Nylon is cheerful. Cheerful is how policy wears fabric.", f"Cheerful nylon fabric POLICY costume, {PAINT}"),
    ("click-before-roll", "You click before you roll as if roll required permission.", f"Click then ROLL PERMISSION stamp, {PAINT}"),
    ("layout-nylon", "A pile of people who agreed not to argue with nylon.", f"People nodding at nylon no argue, {PAINT}"),
    ("hands-wheel", "You put your hands on the wheel. The strap will still be there.", f"Callback hands wheel strap across chest, {PAINT}"),
    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at buckle, {PAINT}"),
    ("look-buckle", "Look at the buckle. Not the sky and not a Swedish hero.", f"Buckle between red X sky and red X hero, {PAINT}"),
    ("named-stack", "Bench, lap belt, Bohlin nineteen fifty nine, Amazon, shared patent, retractor.", f"Stack icons bench lap Bohlin Amazon patent retractor, {PAINT}"),
    ("diagonal-law", "A diagonal that owns your parking lot so nylon stays law.", f"Parking lot diagonal stamped LAW, {PAINT}"),
    ("allowed-click", "You are allowed to click. Allowed to hate the chime and still drive.", f"Click ok hate chime still driving, {PAINT}"),
    ("not-natural", "Stop calling the belt natural.", f"NATURAL stamp red X on belt, {PAINT}"),
    ("not-inevitable", "Not inevitable. Not proof you are modern.", f"INEVITABLE MODERN stamps red X, {PAINT}"),
    ("leftover-bench", "A leftover salute to a bench that left the harness.", f"Salute to bench leaving harness, {PAINT}"),
    ("webbing-point", "The salute is cheerful. The webbing is the point.", f"Cheerful salute on nylon webbing, {PAINT}"),
    ("know-diagonal", "Go when the strap lets you. Know which diagonal you are still obeying.", f"Stickman driving strap labeled which diagonal, {PAINT}"),
    ("glance-cheerful", "Cheerful is how a strap stays without looking like a harness.", f"Smiling strap harness ghost hidden, {PAINT}"),
    ("final-callback", "A bench. Gothenburg. Your click.", f"Final callback bench Gothenburg YOUR CLICK, {PAINT}"),
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
        title="Why You Wear a Strap to Sit Still",
        description=(
            "Your seatbelt click feels obvious. Early cars had bare benches. "
            "Nils Bohlin patented the three-point belt at Volvo in nineteen fifty nine. "
            "Volvo shared the design. The diagonal is logistics."
        ),
        tags=(
            "seatbelt",
            "volvo",
            "nils bohlin",
            "safety",
            "history",
            "why",
            "car",
            "three-point",
            "invention",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="CLICK STRAP?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why You Wear a Strap to Sit Still",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-belt.json"
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

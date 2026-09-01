"""Author episode: you grip a circle that used to be a boat stick."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."

CHAPTERS = [
    """Tonight you will grip a circle and call it obvious. Your hands will find ten and two without a lesson, as if the car grew a ring because rings are what cars do. Here is the part that should bother you. The first automobiles did not agree. Many of them steered with a stick, a tiller, a lever that looked like a boat still pretending it was wet. So why does your dashboard wear a wheel as if the wheel were physics? Because ships already had tillers, because early cars copied the wet habit on dry roads, because Alfred Vacheron ran the eighteen ninety four Paris Rouen on a Panhard with a wheel where a stick used to be, and because factories learned that a circle is easier to bolt to a column than a lever is to argue with in a cramped cabin. That is the whole plot. Your grip is not ergonomics by nature. It is a leftover tiller that learned to roll. You still turn. The turn is flattered. That is its job. The road did not vote. A stick did, and then a wheel that taught your wrists the circle until the circle started calling itself sense. Sense is a word a tiller invented so a lever would still feel like law when the water was gone.""",
    """Start with the wet stick, because the wheel stole a rudder and then sold it back as chrome. For thousands of years, if you wanted a hull to obey, you put a lever at the stern and pushed the world sideways. A tiller is not mystical. It is a stick with leverage and a grudge. You move the stick, the rudder moves, the boat argues with the current, and the argument is honest because you can feel the water push back. When the automobile arrived, it arrived as a carriage that forgot the horse and kept the anxiety. Early builders knew boats. Boats had a vocabulary. A tiller was a vocabulary word that did not need a manual. If your wheel still feels like the only adult option, notice that the adult option started as maritime furniture dragged onto a road that was not liquid. The road did not push back like water. The stick still worked. The stick was also in the way of your knees, your passenger, and any plan to put a dashboard between you and the engine. The wheel was not a miracle. It was real estate.""",
    """Named corners, because a myth of one inventor is how a stick gets a halo it did not earn. Panhard et Levassor was already building serious machines in Paris when the newspaper Le Petit Journal organized a road trial from Paris to Rouen in eighteen ninety four. Alfred Vacheron entered a Panhard et Levassor car fitted with a steering wheel, a choice that reads like a footnote until you notice footnotes are how habits start. He was not the only soul on earth to think of a wheel. He was an early loud example on a famous run, the kind of example catalogs copy. Emile Levassor and the Panhard shop were busy turning carriages into engines with opinions. Tillers still showed up on competitors. Wheels showed up where leverage, visibility, and factory repeatability could agree. If you still treat the wheel as the default human interface, file the paperwork separately from the prototype. The default was negotiated in workshops, not discovered in a forest. Your circle is a Paris trial wearing a century of bolts.""",
    """Watch the stick leave the stern, because a horizontal car of speed needed a hinge that did not poke the chest. Tillers on early cars could be vertical levers you yanked like an elevator argument, or horizontal bars you slid like a boat that refused to admit the pond was gone. Both layouts share a problem. A lever wants space. Space is what a cabin sells when the engine stops being a rumor and starts being a roommate. A wheel stacks rotation into a column. A column is a factory's love language. You can mount it, gear it, hide the linkage behind a firewall, and hand the same part to ten workers without ten arguments. I am not giving you a list of firsts. I am pointing at the swap. We took a stick that said push here and we replaced it with a ring that said rotate here. Rotate is easier to teach in a showroom. Rotate is easier to photograph for a catalog. Rotate is easier to repeat when the line speeds up. The line is the real inventor. The line does not care about your nostalgia for a tiller. The line cares about parts that fit.""",
    """This is the rehook. You think the wheel is a fact, the way a door knob is a fact. The wheel is a policy. In a modern cabin the policy is already on, because the alternative is trusting every driver to learn a stick that moves in three dimensions while looking over an engine that wants to be a furnace. Tillers are honest. Wheels are scalable. Scalable is how a machine escapes the hobbyist bench and becomes something a city can own in numbers. I am not calling you clumsy for liking a circle. I am un-naturing the grip. The grip is a boat lever wearing a column. The column said rotation can be law. Law is a feeling when your hands find ten and two without remembering when they learned it. If you have ever driven something with a tiller, even a golf cart or a lawn rig, you know the wheel is not physics. It is a compromise that won a production vote. A vote is not a rudder. A vote is a spreadsheet with elbows.""",
    """Watch the lock travel. Mass production did not invent steering. It inventoried it. When the same dashboard had to repeat across models, the wheel became the part you could source, stamp, ship, and replace without translating a tiller layout for every chassis. Dealers liked it. Drivers liked the idea of a ship captain without the wet. Repair shops liked a column you could recognize in the dark. Racing and speed records helped the wheel feel modern, not because circles are faster, but because a wheel lets you turn hard without relocating your torso. The stick did not vanish in a single year. It faded the way habits fade when catalogs stop listing them. A catalog is a quiet referendum. If your rental car has a wheel and your history book has a tiller, that gap is not evolution. It is inventory. Inventory is how the past loses a fight without filing a complaint.""",
    """This is you, already, in the middle of the story. A Tuesday, a parking lot, a circle you have turned a thousand times without thanking a boat. You sit with the seatbelt and stare at the column because backing up would feel impossible without a ring, which is the most modern impossibility there is. None of this makes you mechanical by nature. It makes you a person born after Panhard trials and after dashboards became real estate and after a wheel learned to host horns, airbags, and buttons that beep. You can feel both in the same grip: relief that you do not have to shove a lever through your passenger's knee, and a tiny insult that a maritime stick lost to a factory column. The relief is real. The insult is the tiller failing for a second in your imagination. You paid for a simpler cabin with a part you never voted on. The part is cheerful. Cheerful is how a column stays in the century without looking like a column. The wheel still has a circle. The circle still feels like a captain. A captain used to have a stick. Your stick is the rotation of a ring that forgot the sea. The rotation is cheerful. Cheerful is how a boat habit stays on asphalt without looking wet.""",
    """A car is a pile of compromises with wheels attached. That sentence is rude and almost fair. Take the wheel away and the cabin becomes a workshop puzzle nobody wins, or a tiller on every model until the knee room breaks. Visibility, linkage, assembly time, repair manuals: the wheel is a diagram of how to turn without moving the whole human, written by someone you will not meet. You still grip. The grip is a vote for a hinge that was sold as obvious. I am not telling you to hunt for a tiller as a personality. I am telling you the personality was always the swap: a stern stick, a carriage lever, a Paris trial on a Panhard, a column on a line, a catalog that stopped listing the stick. The crowd is still in the cabin. The crowd is you and a rental fleet treating a circle as a treaty. The treaty cannot see a workshop. The template can, if a human overrode it, which is a sentence assembly logs are not supposed to hide. A log is a promise in a cabinet you will never open. The cabinet is the real dashboard. The dashboard is a costume. Costume is how a column stays in a Tuesday without looking like a boat. The boat is still under the ring. The ring is still a permission slip you never signed. So what did we trade? We traded a stick that told the truth about leverage for a ring that could be timed, tooled, and forgotten. That tooling is real help: fewer knee fights, a passenger who keeps their ribs, a linkage you can service from under the hood. Help can be a miracle and still be a part number. We also gained a myth that the wheel is nature, that the circle is the only adult grip, that a tiller is a joke you outgrow. Adult is a word the line uses. We kept the boat and called it a dashboard. We kept the stick and called it history. Both can be true and still not be a reason to forget the wheel is a policy that learned manners. Deals can be rewritten. Some already were, quietly, when power steering made the circle lighter and when a joystick flirted with concept cars and lost to the column again. Again is slower than a tiller. A tiller is a truce you shove. A truce is not a cabin that learned to be roomy and still kind. Kind would be a different layout. The layout we kept is a pile of people who agreed not to argue with a ring.""",
    """This is you. You will put your hands on the wheel. The circle will still be there. You will feel nothing, which is the victory. Look at the column. That is not the sky and it is not a captain. That is a stern stick, a carriage lever, Alfred Vacheron on a Panhard at Paris Rouen in eighteen ninety four, a factory column that replaced a knee argument, a catalog that stopped listing tillers, and a ring that still owns your parking lot so you will keep treating rotation as law. You are allowed to grip. You are allowed to hate parallel parking and still turn. Just stop calling the wheel natural, or inevitable, or proof that you are modern. Tonight, when you back out, look at it like a leftover salute to a stick that left the stern. The salute is cheerful. The asphalt is the point. Go when the ring lets you. Know which circle you are still obeying. The grip is cheerful. Cheerful is how a wheel stays in the cabin without looking like a tiller you used to shove.""",
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, five-second cadence)."""
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("grip-circle", "Tonight you grip a circle and call it obvious.", f"Stickman hands on steering wheel labeled OBVIOUS, {PAINT}"),
    ("ten-two", "Your hands find ten and two without a lesson.", f"Clock hands 10 and 2 on a wheel, {PAINT}"),
    ("car-ring", "As if the car grew a ring because cars do rings.", f"Car sprouting a ring like fruit, {PAINT}"),
    ("first-cars-no", "The first automobiles did not agree.", f"Early car shaking head at a wheel, {PAINT}"),
    ("stick-tiller", "Many steered with a stick, a tiller, a lever.", f"Vertical tiller lever in early car, {PAINT}"),
    ("boat-pretending", "A boat still pretending it was wet.", f"Car with a tiny boat flag on a tiller, {PAINT}"),
    ("why-wheel", "Why does your dashboard wear a wheel as if it were physics?", f"Dashboard wheel stamped PHYSICS with question mark, {PAINT}"),
    ("ships-had-tillers", "Ships already had tillers.", f"Stern tiller on a simple ship, {PAINT}"),
    ("wet-on-dry", "Early cars copied the wet habit on dry roads.", f"Water splash icon on dry road car, {PAINT}"),
    ("vacheron-1894", "Alfred Vacheron, eighteen ninety four Paris Rouen, Panhard.", f"Race banner PARIS ROUEN 1894, Panhard car, {PAINT}"),
    ("wheel-not-stick", "A wheel where a stick used to be.", f"Stick crossed out, wheel circled, on Panhard, {PAINT}"),
    ("factory-column", "Factories learned a circle bolts to a column easier.", f"Wheel bolting to a column, easier than lever, {PAINT}"),
    ("not-ergonomics", "Your grip is not ergonomics by nature.", f"ERGONOMICS stamp with red X, hands on wheel, {PAINT}"),
    ("tiller-rolled", "A leftover tiller that learned to roll.", f"Tiller morphing into a wheel, {PAINT}"),
    ("circle-sense", "The circle taught your wrists until it called itself sense.", f"Wrists on wheel, word SENSE appearing, {PAINT}"),
    ("start-wet-stick", "Start with the wet stick.", f"Large tiller at ship stern labeled START, {PAINT}"),
    ("wheel-stole-rudder", "The wheel stole a rudder and sold it back as chrome.", f"Rudder stolen by a chrome wheel, {PAINT}"),
    ("stern-lever", "Put a lever at the stern and push the world sideways.", f"Stickman pushing stern tiller, world tilts, {PAINT}"),
    ("stick-leverage", "A tiller is a stick with leverage and a grudge.", f"Tiller stick with LEVERAGE and grumpy face, {PAINT}"),
    ("rudder-honest", "Move the stick, the rudder moves, the argument is honest.", f"Stick to rudder arrow, honest label, {PAINT}"),
    ("water-pushback", "You can feel the water push back.", f"Hand on tiller, water pushing arrow, {PAINT}"),
    ("carriage-anxiety", "A carriage that forgot the horse and kept the anxiety.", f"Horse ghost, anxious early car, {PAINT}"),
    ("builders-knew-boats", "Early builders knew boats.", f"Boat blueprint next to early car, {PAINT}"),
    ("tiller-vocabulary", "A tiller was a vocabulary word that did not need a manual.", f"Dictionary entry TILLER, no manual, {PAINT}"),
    ("maritime-furniture", "Maritime furniture dragged onto a road that was not liquid.", f"Ship tiller on asphalt with NOT LIQUID sign, {PAINT}"),
    ("knees-passenger", "The stick was in the way of knees and your passenger.", f"Tiller poking passenger knees, {PAINT}"),
    ("dashboard-plan", "In the way of any plan to put a dashboard between you and the engine.", f"Tiller blocking dashboard slot, {PAINT}"),
    ("wheel-real-estate", "The wheel was not a miracle. It was real estate.", f"Wheel as REAL ESTATE sign on dashboard, {PAINT}"),
    ("named-corners", "Named corners. One inventor is a halo the stick did not earn.", f"Halo on wheel, MYTH sticker, {PAINT}"),
    ("panhard-paris", "Panhard et Levassor building serious machines in Paris.", f"Panhard factory sign PARIS, early car, {PAINT}"),
    ("petit-journal", "Le Petit Journal organized a trial Paris to Rouen.", f"Newspaper LE PETIT JOURNAL, map Paris Rouen, {PAINT}"),
    ("vacheron-entered", "Alfred Vacheron entered a Panhard with a steering wheel.", f"Driver nameplate VACHERON, wheel on Panhard, {PAINT}"),
    ("footnote-habit", "A footnote until footnotes are how habits start.", f"Tiny footnote growing into big habit arrow, {PAINT}"),
    ("not-only-soul", "Not the only soul to think of a wheel.", f"Many thought bubbles with wheels, one loud Vacheron, {PAINT}"),
    ("levassor-shop", "Emile Levassor and the Panhard shop turned carriages into engines.", f"Carriage plus engine equals car in workshop, {PAINT}"),
    ("tillers-competitors", "Tillers still showed up on competitors.", f"Two cars, one tiller one wheel, {PAINT}"),
    ("leverage-visibility", "Wheels where leverage, visibility, and repeatability agreed.", f"Three checkmarks leverage visibility repeat, {PAINT}"),
    ("default-negotiated", "The default was negotiated in workshops, not a forest.", f"Workshop handshake, FOREST DISCOVERY with red X, {PAINT}"),
    ("paris-trial-century", "Your circle is a Paris trial wearing a century of bolts.", f"Paris Rouen medal on a bolted column, {PAINT}"),
    ("stick-leaves-stern", "Watch the stick leave the stern.", f"Tiller walking away from ship stern, {PAINT}"),
    ("speed-needs-hinge", "A car of speed needed a hinge that did not poke the chest.", f"Tiller poking chest, red X, wheel safe, {PAINT}"),
    ("vertical-lever", "Tillers could be vertical levers you yanked.", f"Vertical tiller yanked like elevator, {PAINT}"),
    ("lever-wants-space", "A lever wants space.", f"Lever expanding, cramped cabin, {PAINT}"),
    ("engine-roommate", "The engine stops being a rumor and starts being a roommate.", f"Engine sitting in passenger seat ROOMMATE, {PAINT}"),
    ("wheel-stacks", "A wheel stacks rotation into a column.", f"Rotation arrows stacking into column, {PAINT}"),
    ("column-love", "A column is a factory's love language.", f"Factory heart on a steering column, {PAINT}"),
    ("ten-workers", "Hand the same part to ten workers without ten arguments.", f"Ten workers same wheel part, peace, {PAINT}"),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", f"FIRSTS list red X, SWAP arrow, {PAINT}"),
    ("push-to-rotate", "A stick that said push here replaced by a ring that said rotate here.", f"PUSH HERE stick vs ROTATE HERE wheel, {PAINT}"),
    ("rotate-showroom", "Rotate is easier to teach in a showroom.", f"Showroom teacher pointing at wheel rotate, {PAINT}"),
    ("line-speeds-up", "Easier to repeat when the line speeds up.", f"Assembly line repeating wheels faster, {PAINT}"),
    ("line-inventor", "The line is the real inventor.", f"Factory line wearing INVENTOR badge, {PAINT}"),
    ("parts-that-fit", "The line cares about parts that fit.", f"Wheel part fitting slot PARTS THAT FIT, {PAINT}"),
    ("rehook-fact", "Rehook: you think the wheel is a fact like a door knob.", f"Wheel vs doorknob both labeled FACT, {PAINT}"),
    ("wheel-policy", "The wheel is a policy.", f"Wheel stamped POLICY, {PAINT}"),
    ("not-trust-stick", "The alternative is trusting every driver to learn a stick in three dimensions.", f"3D tiller maze, TRUST DRIVER red X, {PAINT}"),
    ("engine-furnace", "Over an engine that wants to be a furnace.", f"Engine with FURNACE flames under driver, {PAINT}"),
    ("tillers-honest", "Tillers are honest.", f"Tiller with HONEST stamp, {PAINT}"),
    ("wheels-scalable", "Wheels are scalable.", f"Wheel multiplying on assembly line SCALABLE, {PAINT}"),
    ("city-in-numbers", "Scalable is how a machine escapes the bench and a city owns it in numbers.", f"Bench to city fleet many cars, {PAINT}"),
    ("un-nature-grip", "Not calling you clumsy. Un-naturing the grip.", f"NATURE sticker peeling off hands on wheel, {PAINT}"),
    ("boat-wearing-column", "The grip is a boat lever wearing a column.", f"Boat tiller inside column costume, {PAINT}"),
    ("rotation-law", "The column said rotation can be law.", f"Column stamped ROTATION LAW, {PAINT}"),
    ("ten-two-feeling", "Hands find ten and two without remembering when they learned.", f"Hands 10-2 with blank memory bubble, {PAINT}"),
    ("tiller-golf-cart", "Drive a tiller golf cart and you know the wheel is not physics.", f"Golf cart tiller vs car wheel, PHYSICS red X, {PAINT}"),
    ("production-vote", "A compromise that won a production vote.", f"Ballot box PRODUCTION VOTE wheel wins, {PAINT}"),
    ("spreadsheet-elbows", "A vote is a spreadsheet with elbows.", f"Spreadsheet with elbow icons, {PAINT}"),
    ("lock-travel", "Watch the lock travel.", f"Steering lock walking onto highway, {PAINT}"),
    ("mass-inventoried", "Mass production did not invent steering. It inventoried it.", f"INVENT red X, INVENTORIED check on wheel shelf, {PAINT}"),
    ("same-dashboard", "The same dashboard had to repeat across models.", f"Identical dashboards row of cars, {PAINT}"),
    ("source-stamp-ship", "A part you could source, stamp, ship, and replace.", f"Wheel parts SOURCE STAMP SHIP boxes, {PAINT}"),
    ("no-tiller-translate", "Without translating a tiller layout for every chassis.", f"Tiller layouts chaos vs one wheel column, {PAINT}"),
    ("dealers-liked", "Dealers liked it.", f"Dealer thumbs up at wheel column, {PAINT}"),
    ("repair-dark", "Repair shops liked a column recognizable in the dark.", f"Mechanic finding column in dark, {PAINT}"),
    ("racing-modern", "Racing helped the wheel feel modern.", f"Race car wheel labeled MODERN, {PAINT}"),
    ("stick-faded", "The stick faded when catalogs stopped listing them.", f"Catalog page tiller faded out, {PAINT}"),
    ("quiet-referendum", "A catalog is a quiet referendum.", f"Catalog voting booth QUIET REFERENDUM, {PAINT}"),
    ("rental-vs-book", "Rental car has a wheel, history book has a tiller.", f"Rental wheel vs book tiller gap, {PAINT}"),
    ("inventory-fight", "That gap is inventory. Inventory is how the past loses without complaining.", f"Inventory shelf beating tiller stick, {PAINT}"),
    ("this-is-you", "This is you. A Tuesday. A parking lot. A circle turned a thousand times.", f"Stickman Tuesday parking lot, wheel, {PAINT}"),
    ("stare-column", "You stare at the column because backing up needs a ring.", f"Backing up stickman staring at wheel ring, {PAINT}"),
    ("modern-impossibility", "The most modern impossibility there is.", f"MODERN IMPOSSIBILITY cloud over reverse, {PAINT}"),
    ("not-mechanical", "None of this makes you mechanical by nature.", f"MECHANICAL NATURE stamp red X, {PAINT}"),
    ("born-after-trial", "Born after Panhard trials and dashboards as real estate.", f"Timeline Panhard trial then dashboard, {PAINT}"),
    ("wheel-hosts", "A wheel learned to host horns, airbags, buttons that beep.", f"Wheel with horn airbag beep buttons, {PAINT}"),
    ("relief-knee", "Relief you do not shove a lever through your passenger's knee.", f"Safe wheel vs tiller poking passenger, {PAINT}"),
    ("insult-stick-lost", "A tiny insult that a maritime stick lost to a factory column.", f"Sad tiller losing to column, tiny insult cloud, {PAINT}"),
    ("never-voted", "You paid for a simpler cabin with a part you never voted on.", f"Cabin receipt part never voted, {PAINT}"),
    ("cheerful-column", "Cheerful is how a column stays without looking like a column.", f"Smiling column disguise, {PAINT}"),
    ("captain-had-stick", "A captain used to have a stick.", f"Captain with stick at stern, {PAINT}"),
    ("ring-forgot-sea", "Your stick is rotation of a ring that forgot the sea.", f"Wheel rotating, sea forgotten ghost, {PAINT}"),
    ("compromises-wheels", "A car is a pile of compromises with wheels attached.", f"Compromise stack with wheels on top, {PAINT}"),
    ("take-wheel-away", "Take the wheel away and the cabin becomes a workshop puzzle.", f"Cabin puzzle pieces no wheel, {PAINT}"),
    ("knee-room-breaks", "Or a tiller on every model until knee room breaks.", f"Cramped knees BREAK sign, {PAINT}"),
    ("diagram-turn", "Visibility, linkage, assembly: a diagram of turn without moving the whole human.", f"Diagram human still wheel turns car, {PAINT}"),
    ("grip-vote", "The grip is a vote for a hinge sold as obvious.", f"Grip voting OBVIOUS hinge, {PAINT}"),
    ("not-tiller-personality", "Not telling you to hunt a tiller as a personality.", f"Tiller personality hat red X, {PAINT}"),
    ("swap-personality", "The personality was the swap: stern, lever, Paris, column, catalog.", f"Five icons stern lever Paris column catalog, {PAINT}"),
    ("crowd-cabin", "The crowd is still in the cabin.", f"Many stickmen in one cabin, {PAINT}"),
    ("circle-treaty", "You and a rental fleet treating a circle as a treaty.", f"Rental cars circle treaty paper, {PAINT}"),
    ("treaty-blind", "The treaty cannot see a workshop.", f"Treaty paper blindfold workshop behind, {PAINT}"),
    ("cabinet-dashboard", "A log in a cabinet you will never open. The real dashboard.", f"Locked cabinet LOG real dashboard, {PAINT}"),
    ("boat-under-ring", "The boat is still under the ring.", f"Boat ghost under steering wheel ring, {PAINT}"),
    ("what-trade", "So what did we trade?", f"Trade scale stick vs wheel, {PAINT}"),
    ("stick-truth", "A stick that told the truth about leverage.", f"Tiller honest leverage arrow, {PAINT}"),
    ("ring-tooled", "For a ring that could be timed, tooled, and forgotten.", f"Wheel on factory timer TOOLED, {PAINT}"),
    ("fewer-knee-fights", "Fewer knee fights, passenger keeps ribs, service from under hood.", f"Happy passenger, hood service column, {PAINT}"),
    ("miracle-part-number", "Help can be a miracle and still be a part number.", f"Halo on wheel with PART NUMBER tag, {PAINT}"),
    ("wheel-nature-myth", "A myth that the wheel is nature, the only adult grip.", f"WHEEL=NATURE myth, ADULT GRIP, {PAINT}"),
    ("tiller-joke", "A myth that a tiller is a joke you outgrow.", f"TILLER JOKE stamp with red X, {PAINT}"),
    ("line-word-adult", "Adult is a word the line uses.", f"Factory line holding word ADULT, {PAINT}"),
    ("kept-boat-dashboard", "We kept the boat and called it a dashboard.", f"Boat renamed DASHBOARD, {PAINT}"),
    ("kept-stick-history", "We kept the stick and called it history.", f"Stick in museum labeled HISTORY, {PAINT}"),
    ("policy-manners", "The wheel is a policy that learned manners.", f"Policy wheel in polite bow tie, {PAINT}"),
    ("power-steering", "Power steering made the circle lighter.", f"Lighter wheel POWER STEERING feather, {PAINT}"),
    ("joystick-lost", "A joystick flirted with concept cars and lost to the column again.", f"Joystick losing to column again, {PAINT}"),
    ("tiller-truce", "A tiller is a truce you shove.", f"Tiller shove TRUCE label, {PAINT}"),
    ("layout-ring", "The layout we kept is people who agreed not to argue with a ring.", f"People nodding at ring no argue, {PAINT}"),
    ("hands-on-wheel", "You put your hands on the wheel. The circle will still be there.", f"Callback hands on wheel circle, {PAINT}"),
    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at wheel, {PAINT}"),
    ("look-column", "Look at the column. Not the sky and not a captain.", f"Column between red X sky and red X captain, {PAINT}"),
    ("stern-carriage-paris", "A stern stick, a carriage lever, Vacheron Panhard Paris Rouen.", f"Three icons stern lever Vacheron race, {PAINT}"),
    ("factory-catalog", "A factory column, a catalog that stopped listing tillers.", f"Column factory plus catalog no tiller, {PAINT}"),
    ("rotation-as-law", "A ring that owns your parking lot so rotation stays law.", f"Parking lot wheel stamped LAW, {PAINT}"),
    ("allowed-grip", "You are allowed to grip. Allowed to hate parking and still turn.", f"Grip ok, hate parking cloud, still turning, {PAINT}"),
    ("not-natural", "Stop calling the wheel natural.", f"NATURAL stamp red X on wheel, {PAINT}"),
    ("not-inevitable", "Not inevitable. Not proof you are modern.", f"INEVITABLE MODERN stamps red X, {PAINT}"),
    ("leftover-stern", "A leftover salute to a stick that left the stern.", f"Salute to tiller leaving stern, {PAINT}"),
    ("asphalt-point", "The salute is cheerful. The asphalt is the point.", f"Cheerful salute on asphalt, {PAINT}"),
    ("know-circle", "Go when the ring lets you. Know which circle you are still obeying.", f"Stickman driving, circle labeled which, {PAINT}"),
    ("grip-cheerful", "The grip is cheerful. Cheerful is how a wheel stays without looking like a tiller.", f"Smiling grip, wheel, tiller ghost hidden, {PAINT}"),
    ("final-callback", "A stick. Paris. Your hands.", f"Final callback stick Paris label hands on wheel, {PAINT}"),
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
        title="Why a Stick Became a Steering Wheel",
        description=(
            "Your wheel feels obvious. Early cars used boat tillers. "
            "Alfred Vacheron ran Paris Rouen in eighteen ninety four on a "
            "Panhard with a wheel. Factories picked the circle for the line."
        ),
        tags=(
            "steering",
            "wheel",
            "tiller",
            "history",
            "car",
            "why",
            "automobile",
            "panhard",
            "ship",
            "factory",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="A STICK?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why a Stick Became a Steering Wheel",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-stick.json"
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

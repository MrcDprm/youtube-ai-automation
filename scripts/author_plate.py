"""Author episode: you glance at a plate and treat it as decoration."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."

CHAPTERS = [
    """Tonight you will glance at a number plate and treat it as decoration, the way you treat a bumper sticker as personality. Your eyes will read letters and digits as if the car grew a name tag because cars do names. Here is the part that should bother you. The first motorists did not drive around with a tax receipt bolted to the back. Many cities learned the hard way that a machine without a label is a machine that can vanish into a crowd. So why does your bumper wear a plate as if the plate were physics? Because Paris needed to know who owned the smoke, because Germany and the Netherlands turned registration into a habit before the century turned, because the United Kingdom passed the Motor Car Act in nineteen oh three and made a plate the price of admission to the road, because American states from New York onward decided a tin rectangle could carry a fee you already paid, and because mass production learned that a standardized tag is easier to enforce than a handshake at every corner. That is the whole plot. Your plate is not identity by nature. It is a registration receipt that learned to look like chrome. You still glance. The glance is flattered. That is its job. The road did not vote. A clerk did, and then a rectangle that taught your bumper the digits until the digits started calling themselves sense. Sense is a word a tax form invented so a fee would still feel like law when the ledger was gone.""",
    """Start with the receipt, because the plate stole a ledger line and then sold it back as metal. Long before reflective film, before vanity spelling, before a camera could read your digits from a gantry, a car was a novelty with no serial number the street could see. Early drivers paid fees in offices. Offices love paper. Paper hates moving vehicles. If your plate still feels like the only adult option, notice that the adult option started as bookkeeping dragged onto a fender. The fender did not ask for poetry. The fender asked for proof. Proof is useful when you need a city, a garage, and a stranger with a notebook to agree that this machine already paid its entry fee without waiting for a clerk to open a drawer. The road keeps traffic like a slow river. The plate keeps traffic like a badge that forgot it was a bill. You can love both and still admit only one of them is wearing your rental car's default skin.""",
    """Named corners, because a myth of one inventor is how a rectangle gets a halo it did not earn. The number plate is not a single eureka moment you can pin on one hero with a plaque. It is a layer cake of municipal panic, road funds, and a tin tag that behaved nicely when you needed to spot a car in a line. France's Paris police ordinance of eighteen ninety three required identification marks on vehicles. Germany's Imperial decree in eighteen ninety six spread registration habits. The Netherlands followed in eighteen ninety eight. In the United Kingdom, the Motor Car Act of nineteen oh three required registration and display of number plates. In the United States, New York began issuing plates in nineteen oh one, Massachusetts in nineteen oh three, and the habit spread state by state like a form that learned to drive. If you still treat the plate as sacred metal, file the paperwork separately from the romance. The plate did not fall out of a factory aesthetic. It fell out of treasuries that needed a visible receipt, then exported the habit along roads until the habit felt like chrome. Your bumper is a ledger line wearing paint.""",
    """Watch the number leave the office, because a horizontal city of speed needed a label that did not require a clerk at every corner. Early enforcement tricks were honest and exhausting. Stop the car. Ask for papers. Match a description. Repeat. A tin rectangle on a bumper is a small insult to anonymity with a large gift to the treasury. The digits flex across states and years. The rectangle repeats. The bolt holes press metal against metal with a grudge soft enough not to rust on the first rainy Tuesday. The display says paid here without asking the driver to carry a folder in the glove box. I am not giving you a list of firsts. I am pointing at the swap. We took a fee that lived in a ledger and we replaced it with a tag that said read this from the curb. Read is easier to teach in a manual. Read is easier to photograph for a ticket camera. Read is easier to repeat when the line speeds up. The line is the real inventor. The line does not care about your nostalgia for an unmarked fender. The line cares about tags that fit and drivers who stay inside the system.""",
    """This is the rehook. You think the plate is a fact, the way a door is a fact. The plate is a policy. In a modern city the policy is already on, because the alternative is trusting every driver to prove registration with a handshake and a hope that the stranger with a notebook remembers your face. Handshakes are honest. Tags are scalable. Scalable is how a fee escapes the clerk's bench and becomes something a city can own in numbers. I am not calling you clumsy for liking a rectangle. I am un-naturing the digits. The digits are a tax receipt wearing a font. The font said visibility can be law. Law is a feeling when your eyes find a plate without remembering when they learned it. If you have ever rented a car and felt relief that the tag was already there, congratulations. You have been living inside a treasury's factor list. The relief is real. The relief is also a truce you never signed. A truce is not a road that voted. A truce is a spreadsheet with bolt holes.""",
    """Mass production did not invent the car. It inventoried the answer. When the same model had to repeat across a fleet, the plate became the part you could issue, stamp, ship, and replace without translating a registration ritual for every chassis. Reflective sheeting, standardized sizes, automated readers: decades later the tag could glow in a headlight beam, a useful chapter about optics and enforcement, not the origin story of the fee itself. Do not make tonight a biopic about one contractor in a workshop. Make it about the object: tin, digits, repeat, enforce. A catalog is a quiet referendum. If your rental has a plate and your history book has an unmarked horseless carriage, that gap is not evolution. It is inventory. Inventory is how the past loses a fight without filing a complaint.""",
    """This is you, already, in the middle of the story. A Tuesday, a parking lot, a rectangle you have walked past a thousand times without thanking a clerk. You stare at the digits because leaving would feel suspicious without a tag, which is the most modern impossibility there is. None of this makes you bureaucratic by nature. It makes you a person born after the Motor Car Act and after states turned fees into metal and after a tag learned to host vanity spelling, toll readers, and cameras that blink. You can feel both in the same glance: relief that you do not have to explain your car to every corner, and a tiny insult that a ledger line won a bumper bolt. The relief is real. The insult is the unmarked fender failing for a second in your imagination. You paid for a visible receipt with a part you never voted on. The part is cheerful. Cheerful is how a tag stays in the century without looking like a tag.""",
    """A car is a pile of compromises with a receipt attached. That sentence is rude and almost fair. Take the plate away and the road becomes a workshop puzzle nobody wins, or a handshake at every model until the treasury breaks. Visibility, font size, assembly time, replacement fees: the tag is a diagram of how to prove payment without opening a drawer, written by clerks you will not meet. You still glance. The glance is a vote for a rectangle that was sold as obvious. I am not telling you to hunt for a horseless carriage as a personality. I am telling you the personality was always the swap: an unmarked fender, a Paris ordinance, a German decree, a British act, an American state issue line, a reflective sheet, a camera that forgot your handshake. The crowd is still on the road. The crowd is you and a rental fleet treating a tag as a treaty. So what did we trade? We traded anonymity for a visible fee. We traded a clerk's drawer for a tin rectangle payroll software can love. We gained a shared label that lets a garage, a city, and a gantry agree on which car paid without negotiating at every corner. Help can be a miracle and still be a part number. We also gained a myth that the plate is identity, that the digits are the only adult view, that an unmarked bumper is a joke you outgrow. We kept the receipt and called it a plate. We kept the handshake and called it history. Both can be true and still not be a reason to forget the plate is a policy that learned manners.""",
    """This is you. You will walk to the car. The rectangle will still be there. You will feel nothing, which is the victory. Look at the bumper. That is not the sky and it is not a hero inventor. That is a Paris ordinance, a German decree, the United Kingdom Motor Car Act of nineteen oh three, New York and Massachusetts learning to issue tin, a reflective sheet, a camera gantry, and digits that still own your parking lot so you will keep treating metal as law. You are allowed to glance. You are allowed to hate bureaucracy and still drive. Just stop calling the plate natural, or inevitable, or proof that you are modern. Tonight, when the tag catches light, look at it like a leftover salute to a ledger line that left the office. The salute is cheerful. The metal is the point. Go when the digits let you. Know which receipt you are still obeying.""",
]


def _stamp(index: int) -> str:
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("glance-plate", "Tonight you glance at a number plate and treat it as decoration.", f"Stickman glancing at plate, DECORATION label, {PAINT}"),
    ("bumper-sticker", "The way you treat a bumper sticker as personality.", f"Bumper sticker PERSONALITY vs plate, {PAINT}"),
    ("letters-digits", "Your eyes read letters and digits as if the car grew a name tag.", f"Car with NAME TAG letters digits, {PAINT}"),
    ("first-no-plate", "The first motorists did not drive with a tax receipt bolted to the back.", f"Early car no plate red X tax receipt, {PAINT}"),
    ("vanish-crowd", "A machine without a label can vanish into a crowd.", f"Car vanishing into crowd no label, {PAINT}"),
    ("why-bumper-plate", "Why does your bumper wear a plate as if the plate were physics?", f"Plate stamped PHYSICS question mark, {PAINT}"),
    ("paris-smoke", "Paris needed to know who owned the smoke.", f"Paris smoke car WHO OWNS label, {PAINT}"),
    ("germany-netherlands", "Germany and the Netherlands turned registration into a habit.", f"Germany Netherlands registration habit arrows, {PAINT}"),
    ("motor-car-act", "United Kingdom Motor Car Act nineteen oh three.", f"Motor Car Act 1903 UK document, {PAINT}"),
    ("ny-mass-plates", "New York nineteen oh one, Massachusetts nineteen oh three.", f"NY 1901 MA 1903 plate timeline, {PAINT}"),
    ("tin-fee", "A tin rectangle could carry a fee you already paid.", f"Tin rectangle FEE PAID stamp, {PAINT}"),
    ("standard-tag", "Mass production learned a standardized tag is easier to enforce.", f"Standard tag bolts enforce checkmark, {PAINT}"),
    ("not-identity", "Your plate is not identity by nature.", f"IDENTITY red X plate wins, {PAINT}"),
    ("receipt-chrome", "A registration receipt that learned to look like chrome.", f"Receipt wearing CHROME mask, {PAINT}"),
    ("glance-flattered", "The glance is flattered. That is its job.", f"Smiling plate FLATTERED badge, {PAINT}"),
    ("road-no-vote", "The road did not vote. A clerk did.", f"Road NO VOTE clerk raising hand, {PAINT}"),
    ("digits-sense", "The digits taught your bumper until they called themselves sense.", f"Bumper word SENSE after digits, {PAINT}"),
    ("start-receipt", "Start with the receipt.", f"Receipt labeled START, {PAINT}"),
    ("plate-stole-ledger", "The plate stole a ledger line and sold it back as metal.", f"Ledger line stolen by metal plate, {PAINT}"),
    ("before-reflective", "Long before reflective film, vanity spelling, gantry cameras.", f"Timeline before reflective vanity camera, {PAINT}"),
    ("no-serial", "A car was a novelty with no serial number the street could see.", f"Car with red X street serial number, {PAINT}"),
    ("fees-offices", "Early drivers paid fees in offices. Offices love paper.", f"Driver paying fee office PAPER LOVES, {PAINT}"),
    ("paper-hates", "Paper hates moving vehicles.", f"Paper chasing car PAPER HATES MOVING, {PAINT}"),
    ("bookkeeping-fender", "Bookkeeping dragged onto a fender.", f"Ledger dragged onto fender, {PAINT}"),
    ("fender-proof", "The fender asked for proof.", f"Fender speech bubble PROOF, {PAINT}"),
    ("city-garage-agree", "City garage stranger agree machine paid entry fee.", f"City garage stranger agreeing PAID, {PAINT}"),
    ("road-river", "The road keeps traffic like a slow river.", f"Road slow river traffic, {PAINT}"),
    ("badge-bill", "The plate keeps traffic like a badge that forgot it was a bill.", f"Badge forgot BILL reminder, {PAINT}"),
    ("named-corners", "Named corners. One inventor is a halo the rectangle did not earn.", f"Halo on plate MYTH sticker, {PAINT}"),
    ("not-one-hero", "The number plate is not one eureka moment on a plaque.", f"Hero plaque red X many layers, {PAINT}"),
    ("layer-cake", "Municipal panic, road funds, tin tag in a line.", f"Layer cake panic funds tin tag, {PAINT}"),
    ("paris-1893", "Paris police ordinance eighteen ninety three required identification marks.", f"Paris 1893 ORDINANCE ID MARKS, {PAINT}"),
    ("germany-1896", "Germany Imperial decree eighteen ninety six spread registration.", f"Germany 1896 decree registration, {PAINT}"),
    ("netherlands-1898", "The Netherlands followed in eighteen ninety eight.", f"Netherlands 1898 registration follow, {PAINT}"),
    ("uk-1903-act", "Motor Car Act nineteen oh three required plates in the UK.", f"UK 1903 ACT plates required, {PAINT}"),
    ("us-spread", "American states spread the habit state by state.", f"US map states spreading plate habit, {PAINT}"),
    ("not-sacred", "The plate is not sacred metal.", f"SACRED METAL stamp red X, {PAINT}"),
    ("treasury-visible", "Treasuries needed a visible receipt.", f"Treasury wants VISIBLE RECEIPT, {PAINT}"),
    ("ledger-line-paint", "Your bumper is a ledger line wearing paint.", f"Ledger line wearing paint on bumper, {PAINT}"),
    ("number-leaves-office", "Watch the number leave the office.", f"Digits walking away from office, {PAINT}"),
    ("city-speed-label", "A city of speed needed a label without a clerk at every corner.", f"City speed needs label no clerk every corner, {PAINT}"),
    ("stop-ask-papers", "Stop the car. Ask for papers. Match description. Repeat.", f"Three panel STOP ASK MATCH REPEAT, {PAINT}"),
    ("insult-anonymity", "A tin rectangle is a small insult to anonymity.", f"Tin plate insulting anonymity cloud, {PAINT}"),
    ("digits-flex", "The digits flex across states and years.", f"Digits changing states years flex, {PAINT}"),
    ("bolt-grudge", "Bolt holes press metal with a grudge soft enough not to rust.", f"Bolts pressing metal GRUDGE SOFT, {PAINT}"),
    ("paid-here", "The display says paid here without a folder in the glove box.", f"PAID HERE plate no glove folder, {PAINT}"),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", f"FIRSTS red X SWAP arrow, {PAINT}"),
    ("ledger-to-tag", "A fee in a ledger replaced by a tag read from the curb.", f"LEDGER fee vs TAG curb read, {PAINT}"),
    ("photograph-ticket", "Easier to photograph for a ticket camera.", f"Camera photographing plate ticket, {PAINT}"),
    ("line-inventor", "The line is the real inventor.", f"Factory line wearing INVENTOR badge, {PAINT}"),
    ("tags-fit", "The line cares about tags that fit.", f"Plate tag fitting slot, {PAINT}"),
    ("rehook-fact", "Rehook: you think the plate is a fact like a door.", f"Plate vs door both labeled FACT, {PAINT}"),
    ("plate-policy", "The plate is a policy.", f"Plate stamped POLICY, {PAINT}"),
    ("handshake-hope", "Prove registration with a handshake and hope.", f"Handshake HOPE red X at corner, {PAINT}"),
    ("handshakes-honest", "Handshakes are honest.", f"Handshake HONEST stamp, {PAINT}"),
    ("tags-scalable", "Tags are scalable.", f"Plate tags multiplying SCALABLE, {PAINT}"),
    ("city-numbers", "Scalable is how a fee escapes the clerk's bench.", f"Clerk bench to city fleet tags, {PAINT}"),
    ("un-nature-digits", "Not calling you clumsy. Un-naturing the digits.", f"NATURE sticker peeling off digits, {PAINT}"),
    ("receipt-font", "The digits are a tax receipt wearing a font.", f"Receipt inside font costume, {PAINT}"),
    ("visibility-law", "The font said visibility can be law.", f"Font stamp VISIBILITY LAW, {PAINT}"),
    ("rental-relief", "Rent a car and feel relief the tag was already there.", f"Rental car relief tag there, {PAINT}"),
    ("treasury-factor", "You have been living inside a treasury's factor list.", f"Treasury factor list around driver, {PAINT}"),
    ("spreadsheet-bolts", "A truce is a spreadsheet with bolt holes.", f"Spreadsheet bolt holes truce, {PAINT}"),
    ("mass-inventoried", "Mass production inventoried the answer.", f"INVENT CAR red X INVENTORIED answer, {PAINT}"),
    ("same-fleet", "The same model had to repeat across a fleet.", f"Identical cars row fleet plates, {PAINT}"),
    ("issue-stamp-ship", "Issue, stamp, ship, and replace without a ritual.", f"Plate ISSUE STAMP SHIP boxes, {PAINT}"),
    ("reflective-chapter", "Reflective sheeting and automated readers: a later chapter.", f"Reflective reader brief label not hero, {PAINT}"),
    ("not-biopic", "Not tonight a biopic about one contractor.", f"WORKSHOP BIOPIC red X object focus, {PAINT}"),
    ("object-tin", "Make it about the object: tin, digits, repeat, enforce.", f"Tin digits repeat enforce cycle, {PAINT}"),
    ("quiet-referendum", "A catalog is a quiet referendum.", f"Catalog voting booth QUIET REFERENDUM, {PAINT}"),
    ("rental-vs-carriage", "Rental has a plate, history book has unmarked carriage.", f"Rental plate vs unmarked carriage gap, {PAINT}"),
    ("inventory-fight", "That gap is inventory.", f"Inventory shelf beating unmarked fender, {PAINT}"),
    ("this-is-you", "This is you. A Tuesday. A parking lot.", f"Stickman Tuesday parking lot plate, {PAINT}"),
    ("stare-digits", "You stare at digits because leaving feels suspicious without a tag.", f"Suspicious leaving without tag stare, {PAINT}"),
    ("modern-impossibility", "The most modern impossibility there is.", f"MODERN IMPOSSIBILITY cloud, {PAINT}"),
    ("not-bureaucratic", "None of this makes you bureaucratic by nature.", f"BUREAUCRATIC NATURE red X, {PAINT}"),
    ("born-after-act", "Born after Motor Car Act and state fees as metal.", f"Timeline 1903 act metal plates, {PAINT}"),
    ("vanity-cameras", "Tag learned vanity spelling, toll readers, cameras.", f"Plate vanity toll camera icons, {PAINT}"),
    ("relief-no-corner", "Relief you do not explain your car at every corner.", f"Happy stickman no explain every corner, {PAINT}"),
    ("insult-ledger", "A tiny insult that a ledger line won a bumper bolt.", f"Ledger line winning bolt insult, {PAINT}"),
    ("never-voted", "You paid for a visible receipt you never voted on.", f"Receipt never voted tag, {PAINT}"),
    ("cheerful-tag", "Cheerful is how a tag stays without looking like a tag.", f"Smiling plate disguise, {PAINT}"),
    ("compromises-receipt", "A car is compromises with a receipt attached.", f"Compromise stack receipt on car, {PAINT}"),
    ("take-plate-away", "Take the plate away and the road becomes a puzzle.", f"Road puzzle no plates, {PAINT}"),
    ("diagram-proof", "The tag is how to prove payment without opening a drawer.", f"Diagram prove pay no drawer, {PAINT}"),
    ("watch-vote", "The glance is a vote for a rectangle sold as obvious.", f"Glance voting OBVIOUS rectangle, {PAINT}"),
    ("swap-personality", "Swap: unmarked fender, Paris, Germany, UK act, US states, reflective, camera.", f"Six icons fender Paris UK US camera, {PAINT}"),
    ("crowd-road", "The crowd is still on the road.", f"Many stickmen on road with plates, {PAINT}"),
    ("tag-treaty", "You and a rental fleet treating a tag as a treaty.", f"Rental fleet tag treaty paper, {PAINT}"),
    ("what-trade", "So what did we trade?", f"Trade scale anonymity vs visible tag, {PAINT}"),
    ("anonymity-fee", "We traded anonymity for a visible fee.", f"Anonymity vs VISIBLE FEE scale, {PAINT}"),
    ("drawer-rectangle", "We traded a clerk's drawer for a tin rectangle.", f"Drawer vs tin rectangle swap, {PAINT}"),
    ("shared-label", "We gained a shared label garage city gantry agree on.", f"Garage city gantry agreeing label, {PAINT}"),
    ("miracle-part", "Help can be a miracle and still be a part number.", f"Halo on plate PART NUMBER tag, {PAINT}"),
    ("plate-identity-myth", "A myth that the plate is identity.", f"PLATE=IDENTITY myth stamp, {PAINT}"),
    ("unmarked-joke", "A myth that an unmarked bumper is a joke you outgrow.", f"UNMARKED JOKE red X, {PAINT}"),
    ("kept-receipt-plate", "We kept the receipt and called it a plate.", f"Receipt renamed PLATE, {PAINT}"),
    ("kept-handshake-history", "We kept the handshake and called it history.", f"Handshake in museum HISTORY, {PAINT}"),
    ("policy-manners", "The plate is a policy that learned manners.", f"Policy plate polite bow tie, {PAINT}"),
    ("walk-to-car", "You will walk to the car. The rectangle will still be there.", f"Callback walking to car plate, {PAINT}"),
    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at plate, {PAINT}"),
    ("look-bumper", "Look at the bumper. Not the sky and not a hero inventor.", f"Bumper between red X sky red X hero, {PAINT}"),
    ("named-stack", "Paris ordinance, German decree, UK act, New York tin, reflective, gantry.", f"Stack icons Paris UK NY reflective gantry, {PAINT}"),
    ("digits-law", "Digits that own your parking lot so metal stays law.", f"Parking lot digits stamped LAW, {PAINT}"),
    ("allowed-glance", "You are allowed to glance and hate bureaucracy and still drive.", f"Glance ok hate bureaucracy driving, {PAINT}"),
    ("not-natural", "Stop calling the plate natural.", f"NATURAL stamp red X on plate, {PAINT}"),
    ("not-inevitable", "Not inevitable. Not proof you are modern.", f"INEVITABLE MODERN stamps red X, {PAINT}"),
    ("leftover-ledger", "A leftover salute to a ledger line that left the office.", f"Salute to ledger leaving office, {PAINT}"),
    ("metal-point", "The salute is cheerful. The metal is the point.", f"Cheerful salute on shiny plate, {PAINT}"),
    ("know-receipt", "Go when the digits let you. Know which receipt you are still obeying.", f"Stickman driving plate which receipt, {PAINT}"),
    ("glance-cheerful", "Cheerful is how a plate stays without looking like a clerk.", f"Smiling plate clerk ghost hidden, {PAINT}"),
    ("gantry-brief", "A gantry is a later chapter about optics not the origin fee.", f"Gantry brief chapter not origin, {PAINT}"),
    ("font-size", "Font size and bolt spacing: bureaucracy you can read from the curb.", f"Font size bolt spacing CURB READ, {PAINT}"),
    ("replacement-fee", "Replace the tag and the fee shows up again.", f"Replacement tag FEE AGAIN receipt, {PAINT}"),
    ("state-colors", "State colors are a filing system wearing paint.", f"State colors FILING SYSTEM paint, {PAINT}"),
    ("horseless-unmarked", "Horseless carriages had no tag because the crowd was small.", f"Small crowd horseless no tag, {PAINT}"),
    ("crowd-grew", "The crowd grew and the treasury wanted names.", f"Crowd growing treasury wants NAMES, {PAINT}"),
    ("enforce-scale", "Enforcement scales when the label faces the street.", f"Enforcement scaling street-facing label, {PAINT}"),
    ("office-stamp", "Every plate is an office stamp that learned to drive.", f"Office stamp driving on bumper, {PAINT}"),
    ("toll-reader", "Toll readers are the receipt checking itself.", f"Toll reader checking receipt itself, {PAINT}"),
    ("vanity-spelling", "Vanity spelling is a fee wearing a joke you paid for.", f"Vanity spelling FEE JOKE paid, {PAINT}"),
    ("parking-gate", "A parking gate reads the treaty on your bumper.", f"Parking gate reading bumper treaty, {PAINT}"),
    ("clerk-bench", "The clerk's bench wanted a label the street could read.", f"Clerk bench wants street-readable label, {PAINT}"),
    ("fee-renewal", "Renew the registration and the plate gets a new year.", f"Registration renewal new year on plate, {PAINT}"),
    ("metal-not-name", "The metal is not your name. It is your payment visible.", f"METAL NOT NAME payment visible, {PAINT}"),
    ("unmarked-tuesday", "An unmarked bumper on a modern Tuesday looks unfinished.", f"Unmarked bumper UNFINISHED Tuesday, {PAINT}"),
    ("bolt-holes", "Bolt holes are where bureaucracy touches the car.", f"Bolt holes BUREAUCRACY touches car, {PAINT}"),
    ("plate-font-law", "The font is law you can read at thirty feet.", f"Font LAW readable 30 feet, {PAINT}"),
    ("gantry-wave", "A gantry wave is the receipt checking itself at speed.", f"Gantry wave receipt at speed, {PAINT}"),
    ("office-to-bumper", "The office learned to commute on your bumper.", f"Office commuting on bumper tag, {PAINT}"),
    ("curb-read", "Readable from the curb is the whole design brief.", f"CURB READ design brief stamp, {PAINT}"),
    ("final-callback", "Receipt. Rectangle. Your bumper.", f"Final callback receipt rectangle your bumper, {PAINT}"),
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
        title="Why a Number Plate Is a Tax Receipt",
        description=(
            "Your plate feels like decoration. Early cars had no tags. "
            "Paris 1893, Germany 1896, UK Motor Car Act 1903, and US states "
            "turned registration fees into tin receipts bolted to the bumper."
        ),
        tags=(
            "number plate",
            "license plate",
            "registration",
            "tax",
            "motor car act",
            "history",
            "why",
            "car",
            "paris",
            "vehicle",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="TAX RECEIPT?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why a Number Plate Is a Tax Receipt",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-plate.json"
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

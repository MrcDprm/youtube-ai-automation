"""Author episode 14: your cardboard is a child of a steel box that deleted the dock."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you will peel packing tape and feel like the story is over. A cardboard rectangle on a kitchen floor. A thing you ordered that used to live on another continent. You will not think of it as a political act. It will feel like a delivery doing its job. Here is the part that should bother you. The cardboard is a child. The parent is a steel box the size of a small room, stacked on a ship you will never stand on, lifted by a crane you will never meet. For most of the history of cargo, a dock was a place where people unpacked the world by hand: barrels, sacks, crates that did not agree with each other. So why does everything now arrive already the same shape? Because a trucker named Malcolm McLean got tired of watching trailers wait for a puzzle of loose freight, and in nineteen fifty six he sailed fifty eight boxes from Newark to Houston on a converted tanker called Ideal X, and then the ocean learned one size. That is the whole plot. Your tape is not the ending. It is the last lid. You still slice. The slice is flattered. That is its job. The dock did not vote. A rectangle did, and then a crane that taught the world to stop unpacking until your door.""",
    """Start with the older dock, because the steel box stole a craft and then sold it back as a socket. Before containers, cargo was a personality. A sack of coffee did not stack like a piano. A barrel rolled. A crate splintered. Stevedores made a living out of disagreement. Loading a ship was a week, sometimes more, a human puzzle in weather, with theft as a tax the waterfront collected in the dark. If your tracking page still feels like a miracle, notice that the miracle used to be a thousand hands and a shouting foreman. Hands get tired. Hands know which crate is yours. Hands can drop a piano and then lie about the piano. The box cannot. That is the sales pitch and also the theft. We took a waterfront that was a place, and we turned it into a plug. A plug does not know your coffee. A plug only knows corners that match corners, and a crane that is late is a city that forgot how to unpack. Disagreement used to be a wage. Agreement is a corner.""",
    """Named ships, because a myth of one genius is how a rectangle gets a halo it did not weld alone. Malcolm McLean had been a trucker from North Carolina who hated the idle hours while his trailer sat on a dock waiting to be emptied into a hold like a piggy bank. In nineteen fifty six, on the twenty sixth of April, the Ideal X left Port Newark with fifty eight trailer-sized boxes and arrived in Houston as a demonstration that the trailer could skip being a trailer and become a brick. Sea-Land grew from that brick. Later the world agreed, more or less, on a steel size: twenty feet, forty feet, corner castings that a crane could grab without asking a man to invent a knot. I am not asking you to love a corporation. I am pointing at the swap. We took a craft of loading, put it in a rectangle that never opened until the last mile, and called the result cheap stuff. Cheap stuff is a word a catalog uses. The catalog never had to live next to the old docks. Next to the old docks you could still smell tar and hear a piano argue with a sack. Next to a socket you smell diesel and a beep.""",
    """Watch the dock leave the city, because a ship that does not unpack does not need a neighborhood. Once the box held, ports moved to cheap land and deep water: Newark and Elizabeth instead of Manhattan's finger piers, Felixstowe instead of a romantic quay. Longshoremen fought for a livelihood that a gantry crane was invented to delete. I am not giving you a list of firsts. I am pointing at the swap. We took a waterfront that could steal your afternoon and feed a street, and we replaced it with a socket that feeds a warehouse an hour inland. A socket is fair in the way a vending slot is fair. It does not know a piano. It does not know a family that lived above the bar. It knows twenty feet. Twenty feet is a permission slip printed in corrugated steel. If your city still has a pretty pier with no cargo, that pier is a fossil of work. Work is expensive. A crane is cheap. Cheap is how a planet stays in the century without hiring a choir of hands. A choir would at least drop a crate in public. A crane just stacks and calls the stacking speed.""",
    """This is the rehook. You think a box is packaging, the way a bag is packaging. A shipping container is a treaty. Same corners, same locks, same height so a crane in one country can trust a crane in another without a conversation. In an age of flags and tariffs the box is the thing that refused to be local. I am not calling you spoiled for ordering a kettle. I am un-naturing the tape. The tape is McLean's idle trailer wearing cardboard. The idle hours said waiting is a tax. The rectangle said stop unpacking. Stop unpacking is a feeling when your hallway is full. If the box is delayed, that is not the ocean being rude. That is a socket admitting the only hurry that counts is the one a crane can grab. A crane is a stevedore who learned to be a skeleton of steel and never blink. Never blinking is how a treaty stays employed after the neighborhood leaves.""",
    """Watch the lock travel. Factories learned to pack for a rectangle instead of a customer. Warehouses became boxes that do not float. Your hallway learned to be a tiny dock. A barcode is a stevedore who moved into a beep. You still perform the little rituals: sign here, leave at the door, photograph the porch, apologize when the box is too big for the stairs. The rituals are how a vanished waterfront stays polite. A polite delivery is still a delivery. If your free shipping still feels like weather, notice it is a queue of steel rooms that learned to hide. The ocean is optional only if the box says so. Optional ocean is a city that bet your kettle on a sailing you will never watch. Never watching is the modern contract. The contract is corrugated. Corrugated is how a planet stays in a Tuesday without looking like a dock. The dock still has water. The water still looks like weather. Weather is a word the box taught the ocean to wear.""",
    """This is you, already, in the middle of the story. A Tuesday, a blade on tape, a logo you will recycle. You slice and stare at foam because the steel parent is too big to fit in the myth of a purchase. None of this makes you a sailor. It makes you a person born after Ideal X and after ports fled the pretty water and after a crane replaced a thousand arguments about sacks. You can feel both in the same cardboard: relief that a kettle did not require a dock of shouting, and a tiny insult that the world only works if nothing special happens to the corners. The relief is real. The insult is the last lid failing for a second. You paid for cheap distance with a trust you cannot inspect in a hold. The trust is cheerful. Cheerful is how a rectangle stays in the century without looking like a deleted neighborhood. The box still has ribs. The ribs still feel like a building. A building used to have a street. Your street is a tracking number. The number is cheerful. Cheerful is how a missing pier stays in the century without looking missing.""",
    """A planet is a pile of rectangles with countries attached. That sentence is rude and almost fair. Take the boxes away and the store becomes a wait measured in seasons, or a dock on every waterfront until the payroll of hands breaks the price. Coffee, a hospital pump, a toy: the rectangle is a diagram of who is allowed to be far away and still cheap. You still slice. The slice is a vote for a socket that was sold as speed. I am not telling you to buy local as a personality. I am telling you the personality was always the swap: a trucker, a converted tanker, fifty eight boxes, a crane that did not get tired of corners. The crowd is still in the supply chain. The crowd is you and a porch camera treating a beep as a treaty. The treaty cannot see a piano. The crane can, if a human packed it, which is a sentence a hold is not supposed to hide. A hold is a promise in a stack you will never climb. The stack is the real dock. The dock is a costume. Costume is how a socket stays in a Tuesday without looking like a dare. The dare is still under the tape. The tape is still a permission slip the dock no longer gets to sign.""",
    """So what did we trade? We traded a world that had to be unpacked in public for a world that could be stacked, sailed, and forgotten until a kitchen. That stacking is real help: fruit in winter, a part for a hospital, a wage in a factory that could finally pack without a poet of sacks. Help can be a miracle and still be a rectangle. We also gained a myth that shipping is weather, that cardboard is the box, that cheap is a personality. Weather is a word the catalog uses. We kept the dock and called it a warehouse. We kept the stevedore and called it a beep. Both can be true and still not be a reason to forget the steel room is a treaty that learned manners. Deals can be rewritten. Some already were, quietly, when ports moved and when a union fought for a remainder of the craft. A remainder is slower than a crane. A crane is a truce you stack. A truce is not a waterfront that learned to stay a street. A street would be a different planet. The planet we kept is a stack of people who agreed not to unpack in public.""",
    """This is you. You will pick up the tape. The cardboard will still be there. You will feel nothing, which is the victory. Look at the rectangle. That is not the ocean and it is not a dock. That is a trucker who hated idle hours, fifty eight boxes in nineteen fifty six, Newark to Houston, a converted tanker, a crane that grabbed corners, a waterfront that became a socket, a pretty pier with no cargo, and a last lid you slice so you will keep treating steel as weather. You are allowed to love the kettle. You are allowed to hate the hallway and still order. Just stop calling the sameness natural, or inevitable, or proof that distance is free. Tonight, when the tape gives, look at it like a leftover unpacking that the dock is no longer allowed to do. The leftover is cheerful. The missing dock is the point. Open if you want. Know which box you are still opening. The slice is cheerful. Cheerful is how a steel room stays in the ocean without looking like a street you used to have.""",
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, five-second cadence)."""
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("peel-tape", "You peel packing tape and feel like the story is over.", "Stickman peeling packing tape on a cardboard box, MS Paint, white background."),
    ("cardboard-kitchen", "A cardboard rectangle on a kitchen floor.", "Cardboard box on a kitchen floor, MS Paint."),
    ("other-continent", "A thing you ordered that used to live on another continent.", "Tiny kettle, dotted line over an ocean, MS Paint."),
    ("not-political", "You will not think of it as a political act.", "Box labeled NOT POLITICS, shrugging stickman, MS Paint."),
    ("delivery-job", "It feels like a delivery doing its job.", "Smiling delivery box, stickman, MS Paint."),
    ("cardboard-child", "The cardboard is a child. The parent is a steel box.", "Tiny cardboard child, huge steel parent box, MS Paint."),
    ("steel-room", "A steel box the size of a small room.", "Steel shipping box as a tiny room, MS Paint."),
    ("stacked-ship", "Stacked on a ship you will never stand on.", "Stickman far away, stacked boxes on a ship, MS Paint."),
    ("crane-unmet", "Lifted by a crane you will never meet.", "Tall gantry crane, tiny stickman waving unmet, MS Paint."),
    ("older-unpack", "A dock was where people unpacked the world by hand.", "Old dock, stick people unpacking barrels, MS Paint."),
    ("barrels-sacks", "Barrels, sacks, crates that did not agree.", "Barrel sack crate arguing, MS Paint."),
    ("why-same", "Why does everything arrive already the same shape?", "Many same rectangles, questioning stickman, MS Paint."),
    ("mclean-tired", "A trucker named Malcolm McLean got tired of waiting trailers.", "Stick trucker, idle trailer, tired face, MS Paint."),
    ("fifty-eight", "Nineteen fifty six: fifty eight boxes, Newark to Houston.", "58 boxes, NEWARK to HOUSTON, 1956, MS Paint."),
    ("ideal-x", "A converted tanker called Ideal X.", "Simple tanker labeled IDEAL X, boxes on deck, MS Paint."),
    ("ocean-one-size", "Then the ocean learned one size.", "Ocean wearing a ONE SIZE stamp, MS Paint."),
    ("tape-not-ending", "Your tape is not the ending. It is the last lid.", "Tape as a last lid, MS Paint."),
    ("dock-no-vote", "The dock did not vote. A rectangle did.", "Rectangle ballot beating a dock, MS Paint."),
    ("until-your-door", "A crane taught the world to stop unpacking until your door.", "Crane, STOP UNPACKING, stickman door, MS Paint."),
    ("older-dock", "Start with the older dock.", "Old crowded dock, no steel boxes, MS Paint."),
    ("stole-craft", "The steel box stole a craft and sold it back as a socket.", "Box stealing a craft hat, SOCKET tag, MS Paint."),
    ("cargo-personality", "Before containers, cargo was a personality.", "Each crate with a different face, MS Paint."),
    ("coffee-piano", "A sack of coffee did not stack like a piano.", "Coffee sack vs piano, not stacking, MS Paint."),
    ("barrel-rolled", "A barrel rolled. A crate splintered.", "Rolling barrel, splintered crate, MS Paint."),
    ("stevedores", "Stevedores made a living out of disagreement.", "Stick dock workers arguing crates, MS Paint."),
    ("week-loading", "Loading a ship was a week, a human puzzle in weather.", "Calendar WEEK, wet puzzle of cargo, MS Paint."),
    ("theft-tax", "Theft as a tax the waterfront collected in the dark.", "Dark dock, missing crate dotted outline, MS Paint."),
    ("thousand-hands", "The miracle used to be a thousand hands and a shouting foreman.", "Many hands, shouting stick foreman, MS Paint."),
    ("hands-know", "Hands know which crate is yours. Hands can drop a piano.", "Hands labeling a crate, piano wobbling, MS Paint."),
    ("box-cannot", "The box cannot. That is the sales pitch and the theft.", "Steel box with NO DROP sign, MS Paint."),
    ("place-to-plug", "A waterfront that was a place became a plug.", "Dock becoming a wall plug, MS Paint."),
    ("plug-no-coffee", "A plug does not know your coffee. It knows matching corners.", "Plug ignoring coffee, matching corners, MS Paint."),
    ("crane-late", "A crane that is late is a city that forgot how to unpack.", "Late crane, city with FORGOT UNPACK, MS Paint."),
    ("named-ships", "Named ships. A myth of one genius is a halo.", "Halo on a steel box, MYTH sticker, MS Paint."),
    ("nc-trucker", "McLean, a trucker from North Carolina, hated idle hours.", "Stick trucker, IDLE clock, NC hills doodle, MS Paint."),
    ("piggy-bank", "Trailer waiting to be emptied into a hold like a piggy bank.", "Trailer as a piggy bank over a ship hold, MS Paint."),
    ("april-1956", "Twenty sixth of April, nineteen fifty six, Ideal X leaves Newark.", "Calendar April 26 1956, ship leaving, MS Paint."),
    ("trailer-brick", "The trailer skipped being a trailer and became a brick.", "Trailer becoming a steel brick, MS Paint."),
    ("sea-land", "Sea-Land grew from that brick.", "Brick growing into a company of boxes, MS Paint."),
    ("twenty-forty", "The world agreed on twenty feet and forty feet.", "20 ft and 40 ft steel boxes, MS Paint."),
    ("corner-castings", "Corner castings a crane could grab without inventing a knot.", "Box corners grabbed by a crane, knot with red X, MS Paint."),
    ("not-corp", "Not asking you to love a corporation. Pointing at the swap.", "CORP heart with red X, SWAP arrow, MS Paint."),
    ("never-opened", "A rectangle that never opened until the last mile.", "Sealed steel box, LAST MILE scissors, MS Paint."),
    ("cheap-stuff", "Called the result cheap stuff. A catalog word.", "CHEAP STUFF catalog, MS Paint."),
    ("dock-leaves", "Watch the dock leave the city.", "Dock walking out of a city, MS Paint."),
    ("no-neighborhood", "A ship that does not unpack does not need a neighborhood.", "Ship ignoring a neighborhood, MS Paint."),
    ("ports-moved", "Ports moved to cheap land and deep water.", "Port relocating to cheap empty land, MS Paint."),
    ("finger-piers", "Newark instead of Manhattan finger piers.", "Finger piers empty, boxes inland, MS Paint."),
    ("longshore-fight", "Longshoremen fought a livelihood a crane was invented to delete.", "Stick dock workers vs gantry crane, MS Paint."),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", "FIRSTS list with red X, SWAP arrow, MS Paint."),
    ("feed-street", "A waterfront that could steal your afternoon and feed a street.", "Old dock feeding a street of shops, MS Paint."),
    ("inland-warehouse", "A socket that feeds a warehouse an hour inland.", "Socket cable to an inland warehouse, MS Paint."),
    ("vending-fair", "A socket is fair like a vending slot is fair.", "Box socket as a vending slot FAIR, MS Paint."),
    ("no-piano", "It does not know a piano. It does not know a family above a bar.", "Piano and upstairs family ignored by box, MS Paint."),
    ("twenty-slip", "It knows twenty feet. A permission slip in corrugated steel.", "20 FT permission slip of steel, MS Paint."),
    ("pretty-pier", "A pretty pier with no cargo is a fossil of work.", "Pretty pier FOSSIL tag, no cargo, MS Paint."),
    ("work-expensive", "Work is expensive. A crane is cheap.", "Price tags: hands vs crane, MS Paint."),
    ("no-choir-hands", "A planet without a choir of hands.", "Empty work gloves, stacked boxes, MS Paint."),
    ("rehook-packaging", "Rehook: you think a box is packaging like a bag.", "Bag vs huge steel box, stickman, MS Paint."),
    ("box-treaty", "A shipping container is a treaty.", "Steel box stamped TREATY, MS Paint."),
    ("same-corners", "Same corners, same locks, same height.", "Matching corners locks height, MS Paint."),
    ("crane-trust", "A crane in one country trusts a crane in another.", "Two cranes shaking hands via a box, MS Paint."),
    ("refused-local", "The box refused to be local.", "Box with LOCAL sticker peeling off, MS Paint."),
    ("not-spoiled", "Not calling you spoiled for ordering a kettle.", "Kettle order, SPOILED with red X, MS Paint."),
    ("un-nature-tape", "Un-naturing the tape.", "NATURE sticker peeling off packing tape, MS Paint."),
    ("idle-cardboard", "The tape is McLean's idle trailer wearing cardboard.", "Idle trailer inside cardboard, MS Paint."),
    ("waiting-tax", "Idle hours said waiting is a tax.", "Waiting clock stamped TAX, MS Paint."),
    ("stop-unpacking", "The rectangle said stop unpacking.", "Steel box shouting STOP UNPACKING, MS Paint."),
    ("hallway-full", "Stop unpacking is a feeling when your hallway is full.", "Hallway full of boxes, MS Paint."),
    ("socket-hurry", "The only hurry that counts is the one a crane can grab.", "Crane grabbing a hurry, MS Paint."),
    ("crane-skeleton", "A crane is a stevedore who learned to be a steel skeleton.", "Crane as a stick stevedore skeleton, MS Paint."),
    ("lock-travel", "Watch the lock travel.", "Box lock walking into a factory, MS Paint."),
    ("pack-for-rectangle", "Factories packed for a rectangle instead of a customer.", "Factory packing into a rectangle, customer far, MS Paint."),
    ("warehouse-float", "Warehouses became boxes that do not float.", "Warehouse as a steel box on land, MS Paint."),
    ("hallway-dock", "Your hallway learned to be a tiny dock.", "Hallway with a tiny dock, MS Paint."),
    ("barcode-beep", "A barcode is a stevedore who moved into a beep.", "Barcode wearing a dock hat, BEEP, MS Paint."),
    ("sign-here", "Sign here. Leave at the door. Photograph the porch.", "Three ritual panels, stickman, MS Paint."),
    ("box-too-big", "Apologize when the box is too big for the stairs.", "Huge box stuck on stairs, MS Paint."),
    ("polite-vanished", "Rituals are how a vanished waterfront stays polite.", "Vanished dock in a polite hat, MS Paint."),
    ("free-shipping", "Free shipping is a queue of steel rooms that learned to hide.", "FREE tag, hidden steel rooms, MS Paint."),
    ("ocean-optional", "The ocean is optional only if the box says so.", "Ocean switch locked by a steel box, MS Paint."),
    ("unread-sailing", "A sailing you will never watch.", "Unread SAILING clipboard, MS Paint."),
    ("corrugated-contract", "The contract is corrugated.", "Corrugated contract paper, MS Paint."),
    ("this-is-you", "This is you. A Tuesday. A blade on tape.", "Stickman Tuesday slicing tape, MS Paint."),
    ("logo-recycle", "A logo you will recycle.", "Box logo going into a recycle bin, MS Paint."),
    ("foam-stare", "You slice and stare at foam. The steel parent is too big.", "Foam peanuts, tiny steel parent far away, MS Paint."),
    ("not-sailor", "None of this makes you a sailor.", "SAILOR hat with red X, kitchen, MS Paint."),
    ("born-after", "Born after Ideal X, after ports fled, after a crane replaced arguments.", "Timeline: Ideal X, fleeing port, crane, MS Paint."),
    ("relief-no-shout", "Relief that a kettle did not require a dock of shouting.", "Quiet kettle, shouting dock with truce, MS Paint."),
    ("insult-corners", "A tiny insult that the world only works if corners stay boring.", "Boring matching corners, insulted stickman, MS Paint."),
    ("lid-fail", "The insult is the last lid failing for a second.", "Last lid cracking, MS Paint."),
    ("cheap-distance", "You paid for cheap distance with a trust you cannot inspect.", "Cheap distance tag, unopened trust in a hold, MS Paint."),
    ("cheerful-rect", "Cheerful is how a rectangle stays without looking deleted.", "Cheerful rectangle costume, MS Paint."),
    ("ribs-building", "The box still has ribs. The ribs still feel like a building.", "Box ribs as a building, MS Paint."),
    ("street-tracking", "A building used to have a street. Your street is a tracking number.", "Street becoming a tracking number, MS Paint."),
    ("pile-rects", "A planet is a pile of rectangles with countries attached.", "Rectangles stacked into a planet, MS Paint."),
    ("seasons-wait", "Take the boxes away and the store waits in seasons.", "Store calendar of seasons, no boxes, MS Paint."),
    ("payroll-hands", "Or a dock on every waterfront until hands break the price.", "Too many hands, broken price tag, MS Paint."),
    ("who-far", "Coffee, a hospital pump, a toy: who is allowed to be far and cheap.", "Coffee pump toy, FAR+CHEAP, MS Paint."),
    ("slice-vote", "The slice is a vote for a socket sold as speed.", "Slice voting SOCKET, SPEED poster, MS Paint."),
    ("not-local-personality", "Not telling you to buy local as a personality.", "LOCAL personality hat with red X, MS Paint."),
    ("swap-icons", "The personality was the swap: trucker, tanker, fifty eight, crane.", "Four swap icons, MS Paint."),
    ("porch-camera", "You and a porch camera treating a beep as a treaty.", "Porch camera, beep, treaty paper, MS Paint."),
    ("treaty-blind", "The treaty cannot see a piano.", "Treaty paper with closed eyes, piano, MS Paint."),
    ("human-packed", "The crane can, if a human packed it.", "Human packing a piano into a box, MS Paint."),
    ("hold-promise", "A hold is a promise in a stack you will never climb.", "Locked stack of boxes labeled HOLD, MS Paint."),
    ("stack-real-dock", "The stack is the real dock. The dock is a costume.", "Stack of boxes in a dock costume, MS Paint."),
    ("trade-public", "We traded unpacking in public for stacking sailed forgotten until a kitchen.", "Public unpack vs kitchen unbox, MS Paint."),
    ("fruit-winter", "Fruit in winter, a hospital part, a wage that could pack without a poet.", "Winter fruit, hospital part, wage, MS Paint."),
    ("miracle-rect", "Help can be a miracle and still be a rectangle.", "Halo on a steel box, MS Paint."),
    ("shipping-weather", "A myth that shipping is weather, that cardboard is the box.", "WEATHER myth, cardboard fake box, MS Paint."),
    ("dock-warehouse", "We kept the dock and called it a warehouse.", "Dock renamed WAREHOUSE, MS Paint."),
    ("stevedore-beep", "We kept the stevedore and called it a beep.", "Stevedore renamed BEEP, MS Paint."),
    ("treaty-manners", "The steel room is a treaty that learned manners.", "Steel box in a tuxedo, MS Paint."),
    ("ports-moved-quietly", "Ports moved. A union fought for a remainder of the craft.", "Moving port, union hat remainder, MS Paint."),
    ("remainder-slower", "A remainder is slower than a crane. A crane is a truce you stack.", "Slow remainder vs stacked crane truce, MS Paint."),
    ("not-stay-street", "A truce is not a waterfront that learned to stay a street.", "Waterfront street vs truce, MS Paint."),
    ("pick-tape", "You pick up the tape. The cardboard will still be there.", "Callback: stickman holding tape, cardboard, MS Paint."),
    ("feel-nothing", "You will feel nothing, which is the victory.", "Blank calm face, cardboard box, MS Paint."),
    ("look-rect", "Look at the rectangle. Not the ocean and not a dock.", "Box between red-X ocean and red-X dock, MS Paint."),
    ("trucker-idle", "A trucker who hated idle hours. Fifty eight boxes.", "Stick trucker, idle clock, 58, MS Paint."),
    ("newark-houston", "Nineteen fifty six. Newark to Houston. A converted tanker.", "1956, two city labels, tanker, MS Paint."),
    ("crane-corners", "A crane that grabbed corners. A waterfront that became a socket.", "Crane on corners, dock becoming socket, MS Paint."),
    ("pretty-no-cargo", "A pretty pier with no cargo. A last lid you slice.", "Pretty empty pier, last lid, MS Paint."),
    ("love-kettle", "You are allowed to love the kettle. Hate the hallway and still order.", "Happy kettle, hated hallway, order button, MS Paint."),
    ("not-natural", "Stop calling the sameness natural.", "SAMENESS NATURAL sticker with red X, MS Paint."),
    ("not-free-distance", "Not proof that distance is free.", "DISTANCE FREE stamp with red X, MS Paint."),
    ("leftover-unpack", "Tape gives: leftover unpacking the dock is no longer allowed.", "Tape giving, dock with NOT ALLOWED unpack, MS Paint."),
    ("missing-dock", "The leftover is cheerful. The missing dock is the point.", "Cheerful leftover, missing dock outline, MS Paint."),
    ("know-box", "Open if you want. Know which box you are still opening.", "Stickman opening, steel parent labeled which, MS Paint."),
    ("slice-cheerful", "The slice is cheerful. Cheerful is how a steel room stays without looking like a street.", "Smiling slice, steel room, street with red X, MS Paint."),
    ("final-callback", "Tape. Newark. Houston. Your door.", "Final callback: tape, two place labels, stickman door, MS Paint."),
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
        title="Why a Steel Box Deleted the Dock",
        description=(
            "The cardboard on your floor is a child. The parent is steel. "
            "Malcolm McLean sailed fifty eight boxes in nineteen fifty six, "
            "the crane grabbed the corners, the waterfront became a socket. "
            "You still slice the tape."
        ),
        tags=(
            "container",
            "shipping",
            "history",
            "port",
            "why",
            "box",
            "trade",
            "dock",
            "cargo",
            "crane",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="ONE BOX?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why a Steel Box Deleted the Dock",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-container.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))
    print("accent", scenario.subtitles.accent_color, "rate", scenario.tts.rate)
    print("hook", scenario.youtube.thumbnail_hook)


if __name__ == "__main__":
    main()

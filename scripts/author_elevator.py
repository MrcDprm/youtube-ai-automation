"""Author episode 12: you trust a box on a rope because Otis sold a demo, not a feeling."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you will jab the close-door button as if the elevator were a stubborn animal. The doors will close on their own schedule, or they will not, and you will jab again because jabbing feels like work. You will not think of it as a political act. It will feel like a box doing its job. Here is the part that should bother you. You are standing in a closet hanging from a rope, over a hole in a building, trusting a machine you cannot see. For most of the history of lifting, that closet was a freight accident waiting for a snap. So why do you step in as if gravity had signed a contract? Because a mechanic from Vermont cut the rope on purpose in New York, in eighteen fifty four, and shouted that everyone was safe, and then cities learned to grow up instead of out. That is the whole plot. Your button is not a remote control. It is a lullaby for a fear the demo already sold. You still press. The press is flattered. That is its job. The rope did not vote. A fairground stunt did, and then a skyline that taught your thumb the poke until the poke started calling itself hurry. Hurry is a word a lobby invented so a hole would feel like a room. The room is still a closet. The closet is still a bet.""",
    """Start with the older lift, because the passenger car stole a warehouse hook and then sold it as a room. Before Otis, hoists hauled barrels and bricks. A rope broke, a platform fell, a worker became a rumor. Hotels and warehouses used steam and belts and hope. Hope is not an engineering spec. People walked stairs because stairs do not negotiate with a cable. A five-story building was already a mountain for knees and for water buckets. If your legs still choose the elevator for two floors, notice that two floors used to be a class: the rich lived low so they would not climb, and the poor climbed so the rich would not smell the kitchen. The attic was cheap because the attic was a hike. Gravity was rent. The box reversed the rent. It also reversed the fear, which is a harder trick than reversing a pulley. A pulley is honest about being a machine. A mirrored closet is a pulley that learned to dress. Dressing is how a warehouse hook got invited into a lobby and then started charging for the view.""",
    """Elisha Graves Otis was a mechanic from Vermont who had already failed at a few lives: farmer, millwright, inventor of a brake that would bite if the rope went slack. In eighteen fifty two he fitted that brake to a hoist in Yonkers. In eighteen fifty four, at the New York Crystal Palace, he rode a platform up, had an axeman cut the rope in public, and the platform jerked, caught, and stayed. He is supposed to have said all safe, gentlemen. Whether the quote is lacquer or fact, the stunt is the product. Safety as a theater you could watch without dying. The company that took his name sold the theater to buildings that wanted more floors than a staircase would forgive. In eighteen fifty seven a passenger elevator opened at the Haughwout Building on Broadway, a cast-iron store that suddenly had a reason to be tall. Height stopped being a dare. Height became inventory. Inventory is a word a store uses when a floor is no longer a hike. A hike used to be the tax on living above the street. The tax moved into a shaft, and the shaft learned to smile with brass.""",
    """Watch the city turn vertical, because a vertical city is a stack of trust. Once the car did not fall as a hobby, architects stacked offices like dishes. Steel frames and the box discovered each other. By the last decades of the eighteen hundreds, New York and Chicago were arguing in the sky. I am not giving you a list of firsts. I am pointing at the swap. We took a death that belonged to freight, put a mirror and a brass button in it, and called the result civilization. The operator was a job: a person in a stool who knew the floors by feel. Then the operator vanished into a panel you mash with a knuckle. If your building still has a human in the car, that human is a fossil of courtesy. Courtesy is expensive. A panel is cheap. Cheap is how a skyline stays in the century without hiring a choir of elevator men. A choir would at least say the floor names out loud. A panel just lights a number and pretends the number is a conversation. Conversation is what you lost when the stool left.""",
    """This is the rehook. You think the close-door button is a tool, the way a light switch is a tool. Often it is a placebo. In a lot of modern cars the button does nothing for ordinary passengers. It is there so your impatience has a place to land. Firefighters and staff may have a key that makes it real. Accessibility rules delayed doors so a person with a walker is not eaten by a schedule. I am not calling you a fool for pressing. I am un-naturing the poke. The poke is Otis's demo wearing a plastic square. The demo said the box will catch you. The square says you can boss the box. Bossing is a feeling. Catching is a ratchet. If the doors ignore you, that is not the elevator being rude. That is the building admitting the only hurry that counts is the one with a key. A key is a class in your pocket. Your finger is a class that got a square so it would not notice. Notice is slower than a jab. A jab is how a placebo stays employed.""",
    """Watch the lock travel. Department stores put the box in the middle like a fountain of floors. Apartment towers sold a view as a product the stairs could not deliver. Hospitals rolled beds into cars that had to be wide enough for a life. Malls stacked parking so you would forget you were in a machine. You still perform the little rituals: stand back, face the door, do not skip with a crowd, apologize when you hold it. The rituals are how a fear stays polite. A polite fear is still a fear. Express elevators skip the kitchen floors the way first class skips the wing. If your office skybridge still feels like weather, notice it is a corridor that refused the ground. The ground is optional now. Optional ground is a city that bet your life on a cable inspection you will never read. Never reading is the modern contract. The contract is laminated in a lobby you walk through as if walking through were free. Walking through is the fee. The fee is a ding.""",
    """This is you, already, in the middle of the story. A Tuesday, a lobby, a number lighting up as if it liked you. You step in with strangers and stare at the glowing digits because eye contact in a falling closet is too much truth. None of this makes you brave. It makes you a person born after a public rope-cut and after Broadway learned to be tall and after a panel replaced a human who used to say good morning. You can feel both in the same ride: relief that your knees are off duty, and a tiny insult when the close-door button ghosts you. The relief is real. The insult is the lullaby failing for a second. You paid for the sky with a trust you cannot inspect. The trust is cheerful. Cheerful is how a hole in a building stays in the century without looking like a hole. The hole still has a number. The number still feels like a greeting. A greeting used to have a voice. Your voice is the ding, which is a machine coughing politely so you will keep staring at the floor lights instead of the cable.""",
    """Skyscrapers are elevators with offices attached. That sentence is rude and almost fair. Take the box away and the tower becomes a stair argument nobody wins. Fire codes, express shafts, sky lobbies: the building is a diagram of who is allowed to skip. You still jab. The jab is a vote for hurry in a machine that was sold as safety. I am not telling you to take the stairs as a personality. I am telling you the personality was always the demo: a man on a platform, a rope cut, a crowd exhaling. The crowd is still in the car. The crowd is you and three people checking their phones as if phones could catch a fall. The phones cannot. The brake can, if the inspection was not a fiction. Fiction is a word maintenance logs are not supposed to be. A log is a promise written in a basement you will never visit. The basement is the real lobby. The lobby is a costume. Costume is how a shaft stays in a Tuesday without looking like a dare you agreed to at the ding.""",
    """So what did we trade? We traded a city that had to be walkable in height for a city that could be stacked, rented, and hurried. That stack is real help: a hospital floor, a cheap attic that became a cheap view, a job on the fortieth story that is not a pilgrimage. Help can be a miracle and still be a cable. We also gained a myth that the button is power, that the car is a room, that falling is a movie problem. Movies are a word the lobby uses. We kept the rope and called it a ride. We kept the fear and called it a button. Both can be true and still not be a reason to forget the box is a hoist that learned manners. Deals can be rewritten. Some already were, quietly, when doors learned to wait for a walker and when a key made the close button honest. Honesty is slower than a jab. A jab is a truce you poke. A truce is not a building that learned to be short. Short would be a different skyline. The skyline we kept is a stack of people who agreed not to look at the rope.""",
    """This is you. You will pick up your finger. The square will still be there. You will feel nothing, which is the victory. Put your thumb on close door. That is not the sky and it is not a staircase. That is a Vermont mechanic, a cut rope in eighteen fifty four, a shout about safety, a Broadway store that wanted height, a skyline of stacked trust, an operator who vanished into plastic, and a button that often lies so you will keep stepping in. You are allowed to love the ride. You are allowed to take the stairs and feel superior for two floors. Just stop calling the box natural, or inevitable, or proof that you are late. Tonight, when you jab, look at it like a lullaby for a fairground stunt that never left the lobby. The lullaby is cheerful. The hole is the point. Ride if you want. Know which rope you are still trusting. The poke is cheerful. Cheerful is how a falling closet stays in the building without looking like a dare. The dare is still under the ding. The ding is still a permission slip you never signed, and you still step in as if signing were someone else's job.""",
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, five-second cadence)."""
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("jab-button", "You jab the close-door button as if the elevator were stubborn.", "Stickman jabbing CLOSE DOOR button in an elevator, MS Paint, white background."),
    ("own-schedule", "The doors close on their own schedule. You jab again.", "Elevator doors ignoring a finger, second jab, MS Paint."),
    ("not-political", "You will not think of it as a political act.", "Elevator labeled NOT POLITICS, shrugging stickman, MS Paint."),
    ("box-job", "It feels like a box doing its job.", "Smiling elevator box, stickman inside, MS Paint."),
    ("closet-rope", "You are in a closet hanging from a rope over a hole.", "Closet-car on a rope over a building hole, MS Paint."),
    ("trust-unseen", "Trusting a machine you cannot see.", "Stickman trusting a hidden gear behind a wall, MS Paint."),
    ("freight-snap", "The closet was a freight accident waiting for a snap.", "Barrel hoist snapping, falling platform, MS Paint."),
    ("gravity-contract", "Why step in as if gravity had signed a contract?", "Gravity signing a contract, elevator waiting, MS Paint."),
    ("vermont-cut", "A mechanic from Vermont cut the rope on purpose in New York.", "Stick mechanic, axe on a rope, NY 1854, MS Paint."),
    ("all-safe", "He shouted that everyone was safe. Cities learned to grow up.", "Crowd, safe platform, city growing upward, MS Paint."),
    ("not-remote", "Your button is not a remote control. It is a lullaby for a fear.", "Button as a lullaby note, remote with red X, MS Paint."),
    ("press-flattered", "You still press. The press is flattered.", "Smiling elevator button being pressed, MS Paint."),
    ("stunt-voted", "The rope did not vote. A fairground stunt did.", "Fair stunt trophy beating a rope, MS Paint."),
    ("thumb-hurry", "A skyline taught your thumb the poke until the poke called itself hurry.", "Skyline, poking thumb labeled HURRY, MS Paint."),
    ("older-lift", "Start with the older lift.", "Old warehouse hoist, no passenger car, MS Paint."),
    ("warehouse-hook", "The passenger car stole a warehouse hook and sold it as a room.", "Hook becoming a tiny room, MS Paint."),
    ("barrels-bricks", "Hoists hauled barrels and bricks. A rope broke.", "Barrels and bricks, broken rope, MS Paint."),
    ("worker-rumor", "A platform fell. A worker became a rumor.", "Fallen platform, rumor cloud, MS Paint."),
    ("steam-hope", "Hotels used steam and belts and hope. Hope is not a spec.", "Steam hoist, word HOPE with red X spec, MS Paint."),
    ("stairs-no-cable", "People walked stairs because stairs do not negotiate with a cable.", "Stairs vs a arguing cable, MS Paint."),
    ("five-story-mountain", "A five-story building was a mountain for knees and buckets.", "Five floors as a mountain, buckets, knees, MS Paint."),
    ("two-floors-class", "Two floors used to be a class. The rich lived low.", "Rich on floor 1, poor climbing, MS Paint."),
    ("attic-hike", "The attic was cheap because the attic was a hike.", "Cheap attic, hiking stickman, MS Paint."),
    ("gravity-rent", "Gravity was rent. The box reversed the rent.", "Gravity as a landlord, elevator reversing rent, MS Paint."),
    ("harder-fear", "Reversing the fear is harder than reversing a pulley.", "Fear vs a pulley, arm wrestle, MS Paint."),
    ("otis-vermont", "Elisha Graves Otis, mechanic from Vermont.", "Stick mechanic OTIS, Vermont hills, MS Paint."),
    ("failed-lives", "He had failed at a few lives: farmer, millwright.", "Three hats: farmer millwright inventor, MS Paint."),
    ("brake-bite", "A brake that would bite if the rope went slack.", "Toothed brake biting a rail, slack rope, MS Paint."),
    ("yonkers-1852", "Eighteen fifty two: the brake on a hoist in Yonkers.", "Yonkers hoist 1852, brake, MS Paint."),
    ("crystal-palace", "Eighteen fifty four, New York Crystal Palace, a public cut.", "Crystal Palace doodle, platform, axe, 1854, MS Paint."),
    ("axeman-cut", "An axeman cut the rope. The platform jerked, caught, stayed.", "Axe cutting rope, platform catching, MS Paint."),
    ("all-safe-gentlemen", "All safe, gentlemen. Stunt as product.", "Banner ALL SAFE, crowd exhaling, MS Paint."),
    ("lacquer-or-fact", "Whether the quote is lacquer or fact, the stunt is the product.", "Quote in lacquer vs the catching platform, MS Paint."),
    ("safety-theater", "Safety as a theater you could watch without dying.", "Theater stage of a safe hoist, audience, MS Paint."),
    ("more-floors", "Buildings wanted more floors than a staircase would forgive.", "Tall building vs tired staircase, MS Paint."),
    ("haughwout-1857", "Eighteen fifty seven: passenger elevator, Haughwout Building, Broadway.", "Cast-iron store BROADWAY 1857, elevator, MS Paint."),
    ("height-inventory", "Height stopped being a dare. Height became inventory.", "Floors as inventory boxes, MS Paint."),
    ("city-vertical", "Watch the city turn vertical. A stack of trust.", "City stacking floors labeled TRUST, MS Paint."),
    ("car-not-hobby", "Once the car did not fall as a hobby, architects stacked offices.", "Stacked office dishes, MS Paint."),
    ("steel-box", "Steel frames and the box discovered each other.", "Steel frame hugging an elevator, MS Paint."),
    ("ny-chicago", "New York and Chicago arguing in the sky.", "Two skylines arguing, MS Paint."),
    ("not-a-list", "Not a list of firsts. Pointing at the swap.", "FIRSTS list with red X, SWAP arrow, MS Paint."),
    ("freight-death", "A death that belonged to freight got a mirror and a brass button.", "Freight warning sign, then mirror and brass button, MS Paint."),
    ("called-civ", "And called the result civilization.", "Elevator labeled CIVILIZATION, MS Paint."),
    ("operator-job", "The operator was a job: floors by feel.", "Stick operator on a stool, feeling floors, MS Paint."),
    ("operator-vanished", "Then the operator vanished into a panel you mash.", "Operator fading into a button panel, MS Paint."),
    ("human-fossil", "A human in the car is a fossil of courtesy.", "Operator as a fossil, MS Paint."),
    ("panel-cheap", "Courtesy is expensive. A panel is cheap.", "Price tags: operator vs panel, MS Paint."),
    ("no-choir", "A skyline without a choir of elevator men.", "Skyline, empty operator hats, MS Paint."),
    ("rehook-tool", "Rehook: you think close-door is a tool like a light switch.", "Close-door button vs light switch, stickman, MS Paint."),
    ("placebo", "Often it is a placebo.", "Button labeled PLACEBO, MS Paint."),
    ("does-nothing", "In many cars the button does nothing for ordinary passengers.", "Finger press, doors ignoring, ordinary sticker, MS Paint."),
    ("impatience-land", "It is there so your impatience has a place to land.", "Impatience landing on a square button, MS Paint."),
    ("key-real", "Firefighters and staff may have a key that makes it real.", "Key making the button light up REAL, MS Paint."),
    ("walker-wait", "Doors delayed so a walker is not eaten by a schedule.", "Walker stickman, slow doors, MS Paint."),
    ("un-nature-poke", "Not calling you a fool. Un-naturing the poke.", "Nature sticker peeling off a poke, MS Paint."),
    ("demo-square", "The poke is Otis's demo wearing a plastic square.", "1854 demo inside a plastic button, MS Paint."),
    ("box-will-catch", "The demo said the box will catch you.", "Safety brake catching a car, MS Paint."),
    ("boss-the-box", "The square says you can boss the box.", "Stickman bossing an elevator, MS Paint."),
    ("bossing-feeling", "Bossing is a feeling. Catching is a ratchet.", "Feeling cloud vs a ratchet, MS Paint."),
    ("hurry-with-key", "The only hurry that counts is the one with a key.", "Key hurry vs jab hurry, MS Paint."),
    ("lock-travel", "Watch the lock travel.", "Elevator lock walking into a store, MS Paint."),
    ("store-fountain", "Department stores put the box in the middle like a fountain of floors.", "Store fountain of elevator floors, MS Paint."),
    ("view-product", "Towers sold a view the stairs could not deliver.", "Window view vs tired stairs, MS Paint."),
    ("hospital-beds", "Hospitals rolled beds into cars wide enough for a life.", "Hospital bed in a wide elevator, MS Paint."),
    ("mall-parking", "Malls stacked parking so you forget you are in a machine.", "Parking stack, forgotten machine, MS Paint."),
    ("rituals", "Stand back, face the door, apologize when you hold it.", "Three ritual panels, stick people, MS Paint."),
    ("polite-fear", "Rituals are how a fear stays polite.", "Fear in a polite hat, MS Paint."),
    ("express-skip", "Express elevators skip kitchen floors like first class skips the wing.", "Express car skipping floors, MS Paint."),
    ("skybridge", "A skybridge is a corridor that refused the ground.", "Skybridge with ground red X, MS Paint."),
    ("ground-optional", "The ground is optional now.", "Optional ground switch, MS Paint."),
    ("unread-inspection", "A city that bet your life on a cable inspection you never read.", "Unread inspection clipboard, cable, MS Paint."),
    ("this-is-you", "This is you. A Tuesday lobby. A number lighting up.", "Stickman Tuesday lobby, glowing floor number, MS Paint."),
    ("strangers-digits", "You stare at glowing digits because eye contact is too much truth.", "Strangers in a car staring at numbers, MS Paint."),
    ("not-brave", "None of this makes you brave. Born after a public rope-cut.", "Not-brave sticker, cut rope, modern lobby, MS Paint."),
    ("broadway-tall", "After Broadway learned to be tall.", "Broadway getting tall, MS Paint."),
    ("good-morning-gone", "A panel replaced a human who used to say good morning.", "Good morning fading, button panel, MS Paint."),
    ("knees-off", "Relief that your knees are off duty.", "Knees in a hammock, elevator, MS Paint."),
    ("button-ghosts", "A tiny insult when the close-door button ghosts you.", "Ghost button, insulted stickman, MS Paint."),
    ("lullaby-fail", "The insult is the lullaby failing for a second.", "Broken lullaby note, MS Paint."),
    ("trust-inspect", "You paid for the sky with a trust you cannot inspect.", "Sky for sale, unopened trust box, MS Paint."),
    ("cheerful-hole", "Cheerful is how a hole stays without looking like a hole.", "Building hole in a cheerful costume, MS Paint."),
    ("towers-are-elevators", "Skyscrapers are elevators with offices attached.", "Tower that is mostly elevator shaft, tiny offices, MS Paint."),
    ("rude-fair", "That sentence is rude and almost fair.", "Rude stamp on a fair sentence, MS Paint."),
    ("stair-argument", "Take the box away and the tower is a stair argument nobody wins.", "Tower of arguing stairs, no elevator, MS Paint."),
    ("sky-lobbies", "Fire codes, express shafts, sky lobbies: who is allowed to skip.", "Diagram of skippers vs climbers, MS Paint."),
    ("jab-vote", "The jab is a vote for hurry in a machine sold as safety.", "Jab voting HURRY, safety poster, MS Paint."),
    ("not-stairs-personality", "Not telling you to take the stairs as a personality.", "Stairs personality hat with red X, MS Paint."),
    ("demo-man", "The personality was the demo: a man, a platform, a rope cut.", "Demo trio: man platform rope, MS Paint."),
    ("crowd-exhale", "A crowd exhaling. The crowd is still in the car.", "Crowd in an elevator exhaling, MS Paint."),
    ("phones-cannot", "Phones cannot catch a fall. The brake can.", "Phone with red X, brake catching, MS Paint."),
    ("inspection-fiction", "If the inspection was not a fiction.", "Inspection log NOT FICTION, MS Paint."),
    ("trade-walkable", "We traded a walkable height for a stacked hurried city.", "Walkable short city vs stacked city, MS Paint."),
    ("stack-helps", "A hospital floor, a cheap view, a job on the fortieth story.", "Hospital, view, floor 40, MS Paint."),
    ("miracle-cable", "Help can be a miracle and still be a cable.", "Halo on a cable, MS Paint."),
    ("button-is-power", "A myth that the button is power, that the car is a room.", "Button POWER myth, car as fake living room, MS Paint."),
    ("falling-movie", "A myth that falling is a movie problem.", "Movie clapper, falling car with red X, MS Paint."),
    ("lobby-word", "Movies are a word the lobby uses.", "Lobby holding the word MOVIES, MS Paint."),
    ("rope-called-ride", "We kept the rope and called it a ride.", "Rope renamed RIDE, MS Paint."),
    ("fear-called-button", "We kept the fear and called it a button.", "Fear renamed BUTTON, MS Paint."),
    ("hoist-manners", "The box is a hoist that learned manners.", "Hoist in a tuxedo, MS Paint."),
    ("walker-key-honest", "Doors wait for a walker. A key makes close honest.", "Walker plus key lighting CLOSE, MS Paint."),
    ("jab-truce", "A jab is a truce you poke. Not a building that learned to be short.", "Poke truce vs short building, MS Paint."),
    ("pick-up-finger", "You pick up your finger. The square will still be there.", "Callback: stickman finger over CLOSE DOOR, MS Paint."),
    ("feel-nothing", "You will feel nothing, which is the victory.", "Blank calm face, elevator buttons, MS Paint."),
    ("thumb-close", "Put your thumb on close door.", "Giant thumb on CLOSE DOOR, MS Paint."),
    ("not-stairs", "Not the sky and not a staircase.", "Button between red-X sky and red-X stairs, MS Paint."),
    ("vermont-mechanic", "A Vermont mechanic. A cut rope in eighteen fifty four.", "Otis, cut rope, 1854, MS Paint."),
    ("shout-safety", "A shout about safety. A Broadway store that wanted height.", "Shout SAFE, Broadway store growing, MS Paint."),
    ("stacked-trust", "A skyline of stacked trust. An operator vanished into plastic.", "Stacked trust, fading operator, plastic panel, MS Paint."),
    ("button-lies", "A button that often lies so you will keep stepping in.", "Lying button, stickman still entering, MS Paint."),
    ("love-the-ride", "You are allowed to love the ride.", "Happy stickman in an elevator, MS Paint."),
    ("stairs-superior", "You are allowed to take the stairs and feel superior for two floors.", "Smug stair stickman vs elevator, MS Paint."),
    ("not-natural", "Stop calling the box natural.", "Elevator NATURAL sticker with red X, MS Paint."),
    ("not-late-proof", "Not proof that you are late.", "LATE stamp with red X, MS Paint."),
    ("lullaby-stunt", "When you jab, a lullaby for a fairground stunt that never left the lobby.", "Jab, lullaby, stunt ghost in lobby, MS Paint."),
    ("hole-is-point", "The lullaby is cheerful. The hole is the point.", "Cheerful lullaby, building hole, MS Paint."),
    ("know-rope", "Ride if you want. Know which rope you are still trusting.", "Stickman riding, rope labeled which, MS Paint."),
    ("poke-cheerful", "The poke is cheerful. Cheerful is how a falling closet stays.", "Smiling poke, closet-car in a building, MS Paint."),
    ("stubborn-animal", "You jab as if the elevator were a stubborn animal.", "Elevator box as a stubborn mule, poking stickman, MS Paint."),
    ("grow-up-not-out", "Cities learned to grow up instead of out.", "City stretching up, sprawl with red X, MS Paint."),
    ("kitchen-smell", "The poor climbed so the rich would not smell the kitchen.", "Kitchen smell rising, rich on floor one, MS Paint."),
    ("water-buckets", "Five stories were a mountain for water buckets.", "Stickman hauling buckets up stairs, MS Paint."),
    ("fortieth-not-hike", "A job on the fortieth story that is not a pilgrimage.", "Floor 40 job, pilgrimage hat with red X, MS Paint."),
    ("cheap-view", "A cheap attic that became a cheap view.", "Attic window now selling a view, MS Paint."),
    ("three-phones", "You and three people checking phones as if phones could catch a fall.", "Four stickmen, phones, falling car, MS Paint."),
    ("maintenance-log", "Fiction is a word maintenance logs are not supposed to be.", "Maintenance log stamped TRUE, MS Paint."),
    ("honesty-slower", "Honesty is slower than a jab. A jab is a truce you poke.", "Slow HONEST turtle vs fast jab, MS Paint."),
    ("doors-own-time", "The doors have a clock you are not on.", "Door clock vs stickman watch, MS Paint."),
    ("lobby-mirror", "A mirror so you look at yourself instead of the cable.", "Elevator mirror, hidden cable, MS Paint."),
    ("ding-permission", "The ding is permission to pretend the hole is a room.", "Ding bell, hole wearing a room costume, MS Paint."),
    ("final-callback", "Close door. Yonkers. Broadway. Your thumb.", "Final callback: button, two place labels, stickman thumb, MS Paint."),
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
        title="Why You Trust a Box on a Rope",
        description=(
            "The close-door button feels like power. It is often a lullaby. "
            "Otis cut a rope in eighteen fifty four, Broadway got tall, "
            "the operator vanished into plastic. You still jab."
        ),
        tags=(
            "elevator",
            "otis",
            "skyscraper",
            "history",
            "button",
            "why",
            "buildings",
            "safety",
            "city",
            "close-door",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="CLOSE DOOR?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why You Trust a Box on a Rope",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-elevator.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))
    print("accent", scenario.subtitles.accent_color, "rate", scenario.tts.rate)
    print("hook", scenario.youtube.thumbnail_hook)


if __name__ == "__main__":
    main()

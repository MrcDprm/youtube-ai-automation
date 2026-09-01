"""Author episode 9: food used to rot, then a can invented the pantry."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you will open a can. The lid will curl like a metal tongue and a smell will come out that does not belong to this room or this week. Soup. Beans. Peaches that remember a summer you were not in. You will not think of it as a political act. It will feel like a cupboard doing its job. Here is the part that should bother you. For most of human history, dinner had an expiration date written in flies and weather. Meat went green. Milk went sharp. Fruit was a calendar, and then it was compost. Armies marched on whatever the nearest field would give them, and then they starved when the field said no. So why does your pantry pretend that August lives in January? Because a French confectioner learned to trap heat in a bottle for an emperor who needed to feed men far from farms, and then a tin learned to travel. That is the whole plot. Your leftover is not a personality. It is a war problem that moved into the kitchen and put on a paper label. You still turn the key. The key is flattered. That is its job. The flies did not vote. A prize committee did, and then a factory, and then a grocery aisle that taught your hand the motion until the motion started calling itself dinner.""",
    """Start with the older death of food, because the can stole time and then denied the theft. Before factories, preservation was a local argument with rot. You smoked. You dried. You packed in fat. You buried in cold cellars that failed in a warm week. A peasant kitchen knew the year as a sequence of panics: slaughter, then scarcity, then green shoots, then too much fruit and no way to keep it. Ships carried hard biscuit and barrelled meat that tasted like the barrel. The navy did not eat peaches in February. They ate whatever had been insulted into lasting, and they still got scurvy and still threw spoiled casks overboard. Fresh was a geography. If you were not near the cow, you were not near the milk. The modern cupboard erases geography. It also erases the old honesty that food is a clock. You can hate the smell of a forgotten fridge drawer and still notice what the smell was protecting: a limit. The can deleted the limit and called the deletion progress, which is a word that never has to do the dishes.""",
    """Napoleon needed calories that could walk. In the first years of the eighteen hundreds, France offered a prize for a way to keep food edible far from kitchens. Nicolas Appert, a confectioner and bottler in Massy, won it. He packed meat and vegetables into glass, sealed them, and heated the jars in a water bath until the inside stopped being a farm and started being a vault. He did not have germ theory. He had a kitchen and a stubborn empiricism. In eighteen ten he published The Art of Preserving Animal and Vegetable Substances for Many Years, a title that sounds like a boast because it was one. The army wanted miles. Appert sold miles in a bottle. Glass broke. Glass was heavy. Glass was still a miracle if you had ever watched a ham turn on you in three summer days. The prize was twelve thousand francs, which is a polite way of saying the state paid a cook to invent logistics. You still eat the logistics. You just call them lunch.""",
    """Britain took the miracle off glass and put it in metal. In eighteen ten Peter Durand patented a tin-plated iron canister, a letter to the future that said: stop breaking. Bryan Donkin and John Hall built a factory on the Bermondsey marshes and began selling canned meat to the Royal Navy. Early cans were thick as armor. Opening them was a job for a hammer and a chisel, which is not a kitchen vibe, it is a siege vibe. Sailors did the siege. Officers wrote home that the meat was surprisingly not a crime. The can was not kindness. It was a way to keep an empire's stomach on a timetable that did not care about harvest. If your tuna still feels like a quiet little cylinder of the ocean, notice that the ocean was first a navy problem. The shop shelf is a dock that learned to be indoor. The label learned to smile. The metal learned to wait.""",
    """America scaled the vault until it became a habit. The Civil War taught both armies that a tin could outlast a campaign. Factories in Baltimore and Chicago learned to stuff the calendar into steel. Gail Borden had already condensed milk into a sweet, shelf-stable paste in the eighteen fifties, a dairy that did not need a cow in the next room. After the war, grocery cans climbed into ordinary houses: tomatoes, salmon, peaches that had no right to be peaches in a snow month. By the early nineteen hundreds a city pantry could look like a warehouse in miniature. The warehouse was the point. You were no longer a person living next to a field. You were a person living next to a supply chain that had learned to play dead until you were hungry. Playing dead is a skill. Bacteria do not applaud. They wait for a dent and a warm warehouse and a skipped sterilizing minute. The skipped minute is how a miracle becomes a recall, and a recall is just a factory admitting the vault had a door.""",
    """This is the rehook. You think a can is safe the way you think a lock is a lock. Safety was a late science, not a birthright of metal. Clostridium botulinum, named from the Latin for sausage, can live where air cannot, make a toxin that does not care about your plans, and turn a poorly processed jar into a quiet disaster. Nineteenth-century canners learned by outbreak. Twentieth-century canners learned by temperature, pH, and pressure cookers that are really small factories. I am not trying to spook your soup. I am trying to un-nature it. The dented can you were told to throw away is a tiny lecture in microbiology wearing a grocery rule. The rule is not superstition. It is a treaty with an organism that likes anaerobic dark. Your cupboard is a peace treaty. Treaties need inspectors. The inspector used to be your nose. Now it is a factory stamp you never meet.""",
    """Watch the tool arrive late, because that is how you know the can was a military object first and a kitchen object second. For decades you opened the vault with violence: hammer, chisel, a bayonet if you had one. In eighteen fifty eight Ezra Warner patented a claw-like opener. In eighteen seventy William Lyman patented a rotating cutter that rode the rim, which is the ancestor of the wheel you still turn while watching a show. The key on a sardine tin is a little surrender flag: we admit this box was not designed for your hands. Pull-tabs and pop-tops are later apologies. If opening a can still feels slightly like breaking into something, good. You are breaking into a nineteenth-century logistics crate that learned manners. The manners are the can opener. The crate is the plot. Your thumb on the tab is a civilian using an army door.""",
    """This is you, already, in the middle of the story. January peaches. A can of beans that outlasted three apartment leases. Spam as a joke and as a wartime protein that refused to leave the joke. A camping trip where the can is the whole plan. A student cupboard that is really a tiny Bermondsey. None of this makes you lazy. It makes you a person born after Appert's bath and after Donkin's tin and after a civil war that taught a continent to trust steel more than a season. You can feel both in the same lunch: relief that dinner does not have to be hunted this afternoon, and a flatness, a factory taste, a sweetness that is really time sugar-coating itself. The relief is real. The flatness is the receipt. You paid for August in January with a little of August's soul. That is not a poem. That is what heat and steel do to a peach. If the peach still tastes like a peach, that is a bonus. If it tastes like the warehouse, that is honest. Honesty is allowed to be beige.""",
    """So what did we trade? We traded a world where food was a clock for a world where food is a warehouse password. We traded seasons you could taste for seasons you can buy. We also gained, for millions, a protein that survived a crossing, a baby milk that did not sour on a train, a disaster ration that is actually a miracle if the road is gone. The trick is pretending the warehouse is a garden. It is not. It is Appert's stubborn bath, a British patent, a navy dock, a war, a botulism treaty, a wheel on a rim, a label that never blinks. Deals can be rewritten. Some already were, quietly, when fresh aisles learned to fake season with jets and plastic, and the can became the unfashionable cousin who still shows up when the power dies. The cousin is ugly. The cousin is loyal. Loyalty is a kind of time travel that does not care about your branding meeting.""",
    """This is you. You will pick up the can. The lid will still curl. You will feel nothing, which is the victory. Put your thumb on the metal. That is not the sky and it is not a garden. That is a prize for an emperor, a glass jar that learned to be tin, a navy that needed miles, a war that stuffed the calendar into steel, a microbe that taught the factory to be afraid, and a little wheel that arrived fifty years late to say please. You are allowed to love the soup. You are allowed to cook the beans from dry and feel superior for an evening. Just stop calling the cupboard natural, or inevitable, or proof that you cannot cook. Tonight, when the lid curls, look at it like a letter from a kitchen in Massy that thought an army should eat. The letter is cheerful. The army is the point. Eat if you want. Know which war you are still opening. The curl is cheerful. Cheerful is how a logistics crate stays in the room without looking like a crate.""",
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, five-second cadence)."""
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


# (slug, covers, prompt) — 132 unique stills, one every five seconds of target runtime.
_ROWS: list[tuple[str, str, str]] = [
    ("can-opener", "You open a can. The lid curls like a metal tongue.", "Stickman turning a can opener, lid curling, MS Paint, white background."),
    ("soup-smell", "A smell comes out that does not belong to this week.", "Open soup can with a smell cloud, stickman sniffing, MS Paint."),
    ("january-peaches", "Peaches that remember a summer you were not in.", "Peach slices in a can labeled JAN, snowflake, MS Paint."),
    ("cupboard-job", "It feels like a cupboard doing its job.", "Simple cupboard of cans, smiling stickman, MS Paint."),
    ("flies-weather", "Dinner had an expiration written in flies and weather.", "Rotting meat, flies, rain cloud, red X on a clock, MS Paint."),
    ("meat-green", "Meat went green. Milk went sharp.", "Green steak and a sour milk jug, disgusted stickman, MS Paint."),
    ("fruit-calendar", "Fruit was a calendar, then compost.", "Apple on a calendar becoming a compost heap, MS Paint."),
    ("army-field", "Armies ate whatever the nearest field would give.", "Tiny soldiers next to a field, empty bowls, MS Paint."),
    ("field-says-no", "Then they starved when the field said no.", "Bare field saying NO, hungry stick soldiers, MS Paint."),
    ("august-january", "Why does your pantry pretend August lives in January?", "August sun stuffed into a January snow can, MS Paint."),
    ("appert-bottle", "A French confectioner trapped heat in a bottle for an emperor.", "Stick cook sealing a hot glass bottle, tiny crown, MS Paint."),
    ("tin-travel", "Then a tin learned to travel.", "Tin can with little legs walking, MS Paint."),
    ("war-in-kitchen", "A war problem moved into the kitchen and put on a paper label.", "Army helmet on a soup can with a cheerful label, MS Paint."),
    ("older-death", "Start with the older death of food.", "Food with a tombstone, stickman looking, MS Paint."),
    ("smoked-dried", "You smoked. You dried. You packed in fat.", "Smokehouse, dried fish, pot of fat, MS Paint."),
    ("cellar-fail", "Cold cellars failed in a warm week.", "Cellar of food sweating in a heat wave, MS Paint."),
    ("slaughter-panic", "The year as panics: slaughter, scarcity, too much fruit.", "Three panels: pig, empty shelf, overflowing apples, MS Paint."),
    ("hard-biscuit", "Ships carried hard biscuit and barrelled meat.", "Ship, hard biscuit, meat barrel, MS Paint."),
    ("no-feb-peach", "The navy did not eat peaches in February.", "Sailor stickman, peach with a red X, February calendar, MS Paint."),
    ("scurvy-cask", "They still got scurvy and threw spoiled casks overboard.", "Ship throwing a barrel, sailor with sore gums, MS Paint."),
    ("fresh-geography", "Fresh was a geography. No cow, no milk.", "Cow far away, empty milk glass, map, MS Paint."),
    ("cupboard-erases", "The modern cupboard erases geography.", "Cupboard erasing a map with a sponge, MS Paint."),
    ("food-is-clock", "Food is a clock. The can deleted the limit.", "Clock made of food, a can covering the hands, MS Paint."),
    ("fridge-drawer", "A forgotten fridge drawer still tells the truth.", "Open fridge drawer with a green leftover, MS Paint."),
    ("limit-protect", "The smell was protecting a limit.", "Nose and a stop-sign smell cloud, MS Paint."),
    ("progress-dishes", "Progress is a word that never has to do the dishes.", "Trophy labeled PROGRESS next to a dirty sink, MS Paint."),
    ("napoleon-calories", "Napoleon needed calories that could walk.", "Tiny Napoleon, walking soup cans, MS Paint."),
    ("france-prize", "France offered a prize to keep food edible far from kitchens.", "Prize ribbon on a sealed jar, map of far kitchens, MS Paint."),
    ("appert-massy", "Nicolas Appert, confectioner in Massy, won it.", "Stick confectioner labeled APPERT, MASSY, MS Paint."),
    ("glass-bath", "He packed jars and heated them in a water bath.", "Jars in a pot of boiling water, MS Paint."),
    ("no-germ-theory", "He did not have germ theory. He had a kitchen.", "Kitchen vs a crossed-out germ doodle, MS Paint."),
    ("art-of-preserving", "Eighteen ten: The Art of Preserving, a boast because it was one.", "Book 1810, boastful stickman, MS Paint."),
    ("army-wanted-miles", "The army wanted miles. Appert sold miles in a bottle.", "Bottle with a road inside, soldiers marching, MS Paint."),
    ("glass-broke", "Glass broke. Glass was heavy.", "Shattered heavy jar, sad stickman, MS Paint."),
    ("ham-three-days", "A ham could turn on you in three summer days.", "Ham with a mean face, calendar 3 DAYS, sun, MS Paint."),
    ("twelve-thousand", "The prize was twelve thousand francs. The state paid a cook for logistics.", "Money bag 12000 F, cook hat, state building, MS Paint."),
    ("you-eat-logistics", "You still eat the logistics. You just call them lunch.", "Lunch plate that is actually a tiny warehouse, MS Paint."),
    ("durand-1810", "Eighteen ten: Peter Durand patents a tin-plated canister.", "Patent paper DURAND 1810, tin can, MS Paint."),
    ("stop-breaking", "A letter to the future that said stop breaking.", "Tin can saying STOP BREAKING to a glass jar, MS Paint."),
    ("donkin-hall", "Donkin and Hall built a factory on the Bermondsey marshes.", "Marsh factory, cans on a belt, label BERMONDSEY, MS Paint."),
    ("navy-cans", "They sold canned meat to the Royal Navy.", "Navy ship loading cans, MS Paint."),
    ("armor-thick", "Early cans were thick as armor.", "Huge thick can like a shield, MS Paint."),
    ("hammer-chisel", "Opening them took a hammer and a chisel.", "Stickman hammering a can with a chisel, MS Paint."),
    ("siege-vibe", "Not a kitchen vibe. A siege vibe.", "Castle siege next to a can, MS Paint."),
    ("not-a-crime", "Officers wrote that the meat was surprisingly not a crime.", "Letter: NOT A CRIME, canned meat, MS Paint."),
    ("empire-stomach", "A timetable for an empire's stomach that ignored harvest.", "Empire map with a stomach clock, no harvest, MS Paint."),
    ("tuna-ocean", "Your tuna feels like a quiet cylinder of the ocean.", "Tuna can with a tiny ocean wave, MS Paint."),
    ("ocean-navy", "The ocean was first a navy problem.", "Navy hat on a fish, MS Paint."),
    ("shelf-is-dock", "The shop shelf is a dock that learned to be indoor.", "Grocery shelf shaped like a dock, MS Paint."),
    ("label-smile", "The label learned to smile. The metal learned to wait.", "Smiling can label, waiting metal, MS Paint."),
    ("civil-war-tin", "The Civil War taught armies a tin could outlast a campaign.", "Two stick armies, cans outlasting a battle, 1860s, MS Paint."),
    ("baltimore-chicago", "Baltimore and Chicago stuffed the calendar into steel.", "Factory cities stuffing months into cans, MS Paint."),
    ("borden-milk", "Gail Borden condensed milk in the eighteen fifties.", "Condensed milk can, cow far away, BORDEN, MS Paint."),
    ("dairy-no-cow", "Dairy that did not need a cow in the next room.", "Milk can, empty barn, stickman pouring, MS Paint."),
    ("grocery-tomatoes", "After the war, tomatoes and salmon climbed into houses.", "Tomato can and salmon can entering a house, MS Paint."),
    ("snow-peach", "Peaches that had no right to be peaches in a snow month.", "Peach can in a snowman scene, MS Paint."),
    ("city-warehouse", "A city pantry looked like a warehouse in miniature.", "Tiny warehouse inside an apartment pantry, MS Paint."),
    ("not-a-field", "You were no longer a person living next to a field.", "Stickman far from a field, next to cans, MS Paint."),
    ("supply-chain", "A supply chain that learned to play dead until you were hungry.", "Cans playing dead, then popping up hungry, MS Paint."),
    ("bacteria-wait", "Bacteria wait for a dent and a warm warehouse.", "Germ doodles at a dented can, warm warehouse, MS Paint."),
    ("rehook-safe", "Rehook: you think a can is safe the way a lock is a lock.", "Can wearing a padlock, stickman trusting it, MS Paint."),
    ("botulinum", "Clostridium botulinum, named from sausage, lives where air cannot.", "Sausage-named germ in a sealed dark can, MS Paint."),
    ("quiet-disaster", "A poorly processed jar can be a quiet disaster.", "Pretty jar with a tiny skull, quiet, MS Paint."),
    ("learn-by-outbreak", "Nineteenth-century canners learned by outbreak.", "Factory plus a warning outbreak arrow, MS Paint."),
    ("pressure-cooker", "Temperature, pH, pressure cookers that are small factories.", "Pressure cooker factory hat, thermometer, MS Paint."),
    ("not-spook-soup", "Not trying to spook your soup. Trying to un-nature it.", "Soup bowl with a nature sticker peeling off, MS Paint."),
    ("dented-lecture", "The dented can you throw away is a microbiology lecture.", "Dented can giving a lecture at a tiny podium, MS Paint."),
    ("anaerobic-dark", "A treaty with an organism that likes anaerobic dark.", "Handshake with a germ in the dark, MS Paint."),
    ("cupboard-treaty", "Your cupboard is a peace treaty.", "Cupboard with a peace treaty paper, MS Paint."),
    ("factory-stamp", "The inspector is a factory stamp you never meet.", "Stamp INSPECTED, faceless factory, MS Paint."),
    ("nose-was-inspector", "The inspector used to be your nose.", "Giant nose with an inspector badge, MS Paint."),
    ("tool-late", "The tool arrived late. Military object first, kitchen second.", "Army can first, kitchen opener second, timeline, MS Paint."),
    ("bayonet-open", "Hammer, chisel, a bayonet if you had one.", "Bayonet opening a can, MS Paint."),
    ("warner-1858", "Eighteen fifty eight: Ezra Warner's claw-like opener.", "Claw can opener, label 1858, MS Paint."),
    ("lyman-1870", "Eighteen seventy: Lyman's rotating cutter on the rim.", "Wheel opener riding a can rim, 1870, MS Paint."),
    ("sardine-key", "The sardine key is a little surrender flag.", "Sardine tin key as a white flag, MS Paint."),
    ("pull-tab", "Pull-tabs are later apologies.", "Pull-tab saying SORRY, MS Paint."),
    ("breaking-in", "Opening a can still feels like breaking into something.", "Stickman burglar at a can door, MS Paint."),
    ("logistics-crate", "A nineteenth-century logistics crate that learned manners.", "Crate in a tuxedo, MS Paint."),
    ("thumb-tab", "Your thumb on the tab is a civilian using an army door.", "Thumb on a tab, tiny army door, MS Paint."),
    ("this-is-you", "This is you. January peaches.", "Stickman eating January peaches from a can, MS Paint."),
    ("three-leases", "A can of beans that outlasted three apartment leases.", "Bean can next to three moving boxes, MS Paint."),
    ("spam-joke", "Spam as a joke and as wartime protein that stayed.", "Spam can laughing and saluting, MS Paint."),
    ("camping-plan", "A camping trip where the can is the whole plan.", "Tent, one can, stickman, MS Paint."),
    ("student-berm", "A student cupboard that is a tiny Bermondsey.", "Dorm cupboard labeled TINY BERMONDSEY, MS Paint."),
    ("not-lazy", "None of this makes you lazy. Born after Appert's bath.", "Bath of jars, baby stickman, modern kitchen, MS Paint."),
    ("trust-steel", "A war taught a continent to trust steel more than a season.", "Steel can beating a season tree at arm wrestling, MS Paint."),
    ("relief-lunch", "Relief that dinner does not have to be hunted this afternoon.", "Stickman not hunting, opening a can instead, MS Paint."),
    ("factory-taste", "A flatness, a factory taste, time sugar-coating itself.", "Flat-tasting peach, factory smokestack, MS Paint."),
    ("august-soul", "You paid for August in January with a little of August's soul.", "January can holding a tiny August ghost, MS Paint."),
    ("heat-steel-peach", "That is what heat and steel do to a peach.", "Peach in a steel can over a flame, MS Paint."),
    ("food-was-clock", "We traded food as a clock for food as a warehouse password.", "Clock swapped for a warehouse key, MS Paint."),
    ("buy-seasons", "Seasons you could taste for seasons you can buy.", "Taste vs price tag on two seasons, MS Paint."),
    ("crossing-protein", "A protein that survived a crossing.", "Can on a ship crossing ocean, MS Paint."),
    ("baby-train", "Baby milk that did not sour on a train.", "Baby bottle can on a train, MS Paint."),
    ("disaster-ration", "A disaster ration that is a miracle if the road is gone.", "Broken road, miracle can, MS Paint."),
    ("warehouse-not-garden", "The trick is pretending the warehouse is a garden.", "Warehouse wearing a flower costume, MS Paint."),
    ("label-never-blinks", "A label that never blinks.", "Can label with unblinking eyes, MS Paint."),
    ("fresh-aisle-jets", "Fresh aisles fake season with jets and plastic.", "Airplane peaches in plastic, MS Paint."),
    ("unfashionable-cousin", "The can is the unfashionable cousin who shows up when the power dies.", "Can with a flashlight in a blackout, MS Paint."),
    ("cousin-loyal", "The cousin is ugly. The cousin is loyal.", "Ugly loyal can hugging stickman, MS Paint."),
    ("time-travel", "Loyalty is time travel that ignores a branding meeting.", "Can time machine, ignored branding chart, MS Paint."),
    ("pick-up-can", "You pick up the can. The lid will still curl.", "Callback: stickman holding a can, lid starting to curl, MS Paint."),
    ("feel-nothing", "You will feel nothing, which is the victory.", "Blank calm face, curling lid, MS Paint."),
    ("thumb-metal", "Put your thumb on the metal.", "Giant thumb on a can lid, MS Paint."),
    ("not-a-garden", "Not the sky and not a garden.", "Can between a red-X sky and a red-X garden, MS Paint."),
    ("prize-emperor", "A prize for an emperor.", "Ribbon on a can, tiny emperor, MS Paint."),
    ("glass-to-tin", "A glass jar that learned to be tin.", "Jar morphing into a tin can, MS Paint."),
    ("navy-miles", "A navy that needed miles.", "Navy can with a mileage counter, MS Paint."),
    ("calendar-steel", "A war that stuffed the calendar into steel.", "Calendar jammed into a steel can, MS Paint."),
    ("microbe-afraid", "A microbe that taught the factory to be afraid.", "Tiny germ scaring a factory, MS Paint."),
    ("wheel-late", "A little wheel that arrived fifty years late to say please.", "Late wheel opener saying PLEASE, MS Paint."),
    ("love-the-soup", "You are allowed to love the soup.", "Happy stickman with soup, MS Paint."),
    ("dry-beans", "You are allowed to cook beans from dry and feel superior.", "Stickman with dry beans looking smug at a can, MS Paint."),
    ("not-natural", "Stop calling the cupboard natural.", "Cupboard with a NATURAL sticker and a red X, MS Paint."),
    ("letter-massy", "A letter from a kitchen in Massy that thought an army should eat.", "Letter stamped MASSY next to soldiers eating, MS Paint."),
    ("letter-cheerful", "The letter is cheerful. The army is the point.", "Cheerful letter, army silhouette, MS Paint."),
    ("eat-know-war", "Eat if you want. Know which war you are still opening.", "Stickman eating, can labeled which war, MS Paint."),
    ("lid-final", "When the lid curls, look at it like a contract.", "Curling lid as a contract page, MS Paint."),
    ("key-flattered", "You still turn the key. The key is flattered.", "Can key with a flattered smile, MS Paint."),
    ("label-yes", "The label votes yes before you have had a thought.", "Can label checking YES, MS Paint."),
    ("shelf-forever", "A shelf that pretends forever is a flavor.", "Shelf of cans labeled FOREVER, MS Paint."),
    ("winter-orchard", "A winter orchard that never had trees.", "Snow orchard made of peach cans, no trees, MS Paint."),
    ("student-midnight", "Midnight beans, no cow, no field, no excuse.", "Midnight stickman eating beans from a can, MS Paint."),
    ("camp-rain", "Rain on a tent. The can is the campfire's cousin.", "Rain tent, can next to a tiny fire, MS Paint."),
    ("dented-choice", "You throw the dented one away. That is the treaty talking.", "Stickman binning a dented can, treaty paper, MS Paint."),
    ("pop-top-civilian", "A pop-top is a civilian apology for a crate.", "Pop-top bowing, old crate behind, MS Paint."),
    ("two-pantries", "Right pantry versus empty pantry. The can still takes sides.", "Split: full can pantry vs empty shelf, MS Paint."),
    ("open-loop-close", "The cupboard did a job. The job had a war in it.", "Cupboard opening, tiny war inside, MS Paint."),
    ("dent-or-eat", "A dent is a vote. Eating is another vote.", "Dented can vs clean can, stickman choosing, MS Paint."),
    ("paper-label-mask", "The paper label is a mask the metal wears to look like food.", "Can wearing a paper-label mask of a peach, MS Paint."),
    ("curl-callback", "The metal tongue curls. Massy. Bermondsey. Your hand.", "Final callback: curling lid, three tiny place labels, stickman hand, MS Paint."),
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
        title="Why Your Food Used To Rot",
        description=(
            "A can feels like a cupboard. It was a war problem. Appert's glass, "
            "Durand's tin, a navy dock, a civil war pantry, botulism as a treaty, "
            "a can opener that arrived late. January peaches are logistics."
        ),
        tags=(
            "canned",
            "food",
            "history",
            "napoleon",
            "appert",
            "preservation",
            "why",
            "pantry",
            "tin",
            "leftovers",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="STILL GOOD?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Your Food Used To Rot",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 24, tzinfo=UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-cans.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print(out)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))


if __name__ == "__main__":
    main()

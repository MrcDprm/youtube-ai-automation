"""Author episode 6: sugar used to be for kings, then write senaryo-paint.json."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you are going to put sugar in something without asking the food if it wanted any. Coffee. Cereal. A spoon that disappears into a dark cup as if that were the natural end of a plant. You will not think of it as a political act. It will taste like morning. Here is the part that should bother you. For most of human history, that sweetness was not a breakfast setting. It was a spice. It sat beside pepper and cinnamon in the houses of people who could buy ships. A pinch was a flex. A bowl was a treasury. Ordinary tongues met honey, fruit, and the occasional accident of ripe anything. So why does your cereal assume a king's pantry? Because cane learned to travel, and then the price of a crystal fell through the floor of a plantation ledger. That is the whole plot. Your sweet tooth is not a personality. It is a supply chain that won, and then moved into the cupboard like it had always lived there. The cupboard believes the story. Your tongue votes yes before you have had a thought.""",
    """Medieval Europe treated sugar the way it treated other rare crystals from far away. Apothecaries weighed it. Cooks for courts used it in tiny doses that announced: we can afford the Indian Ocean, or at least the middlemen who claimed to. Honey was the local sweet. Fruit was seasonal and then it was gone. Cane sugar, when it arrived through Mediterranean traders and later Atlantic islands, was medicine, confection, and status in the same jar. You did not dump it into daily porridge for a child who was not a prince. You displayed it. A sugar sculpture at a feast was closer to jewelry than to a grocery habit. If that sounds precious, good. Precious is the point. The modern breakfast table is what happens when jewelry learns mass production and then pretends it was never jewelry. Your tongue still falls for the old rarity. The warehouse no longer bothers to mention it. Mentioning it would spoil the trick of making a treasure feel like weather.""",
    """The Atlantic turned the jar into an engine. Cane likes heat, water, and brutal work at harvest. European capital found that combination in the Caribbean and Brazil. Barbados, Jamaica, Saint-Domingue, a string of islands that became, in the sixteen and seventeen hundreds, engines for boiling sweetness on a calendar the market could bank. The labor was enslaved people, stolen and worked until the crop paid investors who would never smell the boiling house. I am not going to turn that into a montage. The fact is the engine. Cheap sugar in a London teacup is not a cute colonial anecdote. It is a calorie extracted under a legal regime that treated humans as inventory. When you stir, you are downstream of that inventory system even if the brand on the bag is cheerful and the farm is now a different kind of industrial field with a nicer logo. The crystal kept the smile. The ledger kept the cost. The smile is what you buy. The cost is what the history class is for.""",
    """Britain is where the habit went national and then got called ordinary. Tea arrived as a bitter leaf of empire. Sugar made it drinkable for people who were not monks and did not want to be. By the seventeen hundreds, a laborer's break could include a hot cup and a lump, which sounds small until you multiply it by a kingdom and a working day. The anthropologist Sidney Mintz later argued that this was not just a treat. It was fuel. Sweet calories that did not need a farm kitchen, that fit a factory clock, that kept a body moving through a shift without a second breakfast of meat. In nineteen eighty five he published Sweetness and Power, a book that still reads like someone turning on the lights in your pantry and refusing to turn them off. Sugar was not sneaking into culture. Culture was being rebuilt around a cheap rush. The tea break is a monument. Nobody puts that on the mug, because monuments on mugs are usually flags, not calories.""",
    """Then Europe tried to grow the jewelry at home so a blockade could not steal dessert. Napoleon, cut off from cane by British sea power, needed a sweet that did not require an enemy navy to look the other way. Beet sugar scaled in the eighteen hundreds. Factories in the fields of France and Germany proved you did not need an island to make white crystals that fooled a teacup. The monopoly of the tropics cracked. Prices kept falling. By the later nineteenth century, sugar was climbing into jam, biscuits, condensed milk, and the new candy industries that treated children as a market. A child in a mill town could taste, every week, what a Renaissance duke tasted as a performance. That is not progress in a simple sense. That is a floor dropping until luxury becomes the baseline and the baseline starts to feel like air. You notice air only when it is gone. You notice sugar only when someone takes it away and your coffee tastes like an argument you did not schedule.""",
    """This is the rehook. You think you have a sweet tooth the way you have a fingerprint. You have a twentieth-century default wearing an older appetite. Labels now hide the crystal in places that do not look like dessert: bread, sauce, yogurt that pretends to be virtuous, a bottle of something red that is not fruit. In the nineteen seventies, American processors scaled high-fructose corn syrup because corn policy and chemistry made it cheaper than cane in a lot of factories. I am not giving you a diet, and I am not naming a villain in a white coat for you to hate at lunch. I am giving you a price history. When a flavor is cheaper than the thing it used to decorate, the flavor becomes the thing. Breakfast cereals were not inevitable. They were a business model wearing a cartoon. The cartoon is honest about one fact. It knows you were trained, and it does not apologize for the training.""",
    """Notice what the tongue does when the warehouse wins. Bitter coffee feels unfinished, like a sentence that forgot its verb. Fruit feels like it failed if it is only fruit. Bread without a sweetener in the ingredient list tastes like a mistake you cannot name. That namelessness is the trick. A king would have named it: I have sugar, look at me. You name it: this is how food is. Kids learn the scale before they learn maps. A birthday is a sugar architecture. A reward is a wrapper. None of this makes you weak. It makes you a person born after beet factories and after the Caribbean engine and after Mintz's factory-calorie observation walked into the break room and sat down. The species liked sweet long before cane. Ripe fruit is an old signal: energy, safety, now. What is new is the signal playing all day at full volume, in foods that are not fruit, at a price that makes restraint feel like a hobby for people with spare willpower and a spare hour.""",
    """There was a politics of refusal, and it is worth saying out loud so the story is not only appetite walking into a store. In the seventeen nineties, British abolitionists asked people to boycott slave-grown sugar. Women ran that campaign in kitchens, which is where the empire actually landed, one bowl at a time. Packets said free labor. The boycott did not end the system by itself. It proved something colder. If the crystal in the bowl is a moral object, then breakfast was never innocent, and the innocence was a marketing layer. You can still put sugar in the cup. You can also know that a spoon has been a ballot before. The modern version of the boycott is messier: certifications, arguments in a comments field, a tired label that might mean something or might mean a fee. The old version was clearer because the crime was on the shipping list. Clarity is not the same as purity. It is just a better map, and maps do not stir themselves.""",
    """So what did we trade? We traded a rare sparkle for a constant hum. We traded honey's local ceiling for a global floor so low that manufacturers had to invent new places to hide the crystals so the package would still look like food. We also gained cheap energy, shelf-stable pleasure, a working-class hot drink that was not beer at dawn, and a dessert culture that is genuinely fun when it is chosen instead of defaulted. The trick is pretending the hum is nature. It is not. It is cane, ships, a legal market in people, beet fields, a corn syrup industrial culture, a cartoon mascot that never blinks. Your spoon is a fossil of a court and a plantation and a factory. It still tastes like yes. That yes is the product. The product is very good at not looking like history, which is how history prefers to travel now: inside a habit, wearing a grocery bag.""",
    """This is you. You will lift the spoon. You will hear the crystals hit the cup. You will feel like you are only making coffee, which is a small kindness to yourself before the day starts arguing. You are finishing a sentence that started in a pantry that was a treasury. Put the spoon down for one second. That is not a personality looking back. That is a price that collapsed until a king’s garnish became a grocery reflex so cheap it feels like manners. You are allowed to like it. You are allowed to skip it. Just stop calling the reflex ancient, or natural, or proof that you have no discipline. Tonight, when the spoon hovers, look at it the way a guest at a medieval feast looked at a sugar sculpture: this is wealth, arranged to be eaten, and the eating is the show. The sculpture is gone. The wealth got small and white and boring. The boring is the victory. Stir if you want. Know what you are stirring, then drink.""",
]

BEATS: list[tuple[str, str, str]] = [
    (
        "0000-spoon-coffee",
        "You put sugar in coffee without asking if the food wanted any.",
        "Round-head stickman spooning white crystals into a simple coffee cup, MS Paint, white background.",
    ),
    (
        "0008-cereal",
        "Cereal, a spoon disappearing into a dark cup. Morning.",
        "Bowl of cereal and a coffee cup both getting sugar, stickman at breakfast, MS Paint.",
    ),
    (
        "0016-not-breakfast",
        "For most of history that sweetness was not a breakfast setting.",
        "Breakfast table with a red X over a sugar bowl, confused stickman, MS Paint.",
    ),
    (
        "0024-spice-beside-pepper",
        "It was a spice beside pepper in houses that could buy ships.",
        "Tiny spice jars labeled SUGAR and PEPPER, a toy ship, MS Paint.",
    ),
    (
        "0032-pinch-flex",
        "A pinch was a flex. A bowl was a treasury.",
        "Crown stickman pinching sugar like jewels, a bowl labeled TREASURY, MS Paint.",
    ),
    (
        "0042-honey-fruit",
        "Ordinary tongues met honey, fruit, the occasional ripe accident.",
        "Stickman with a honey pot and an apple, no sugar bag, MS Paint.",
    ),
    (
        "0052-supply-chain",
        "Your sweet tooth is a supply chain that won.",
        "Tongue doodle hooked to a chain of ships and factories, MS Paint.",
    ),
    (
        "0108-apothecary",
        "Apothecaries weighed it. Courts used tiny doses.",
        "Scales, a tiny sugar pile, a court cook stickman, MS Paint.",
    ),
    (
        "0122-honey-local",
        "Honey was the local sweet. Fruit was seasonal.",
        "Beehive and a fruit tree with a calendar, MS Paint.",
    ),
    (
        "0136-feast-jewelry",
        "A sugar sculpture at a feast was closer to jewelry than groceries.",
        "Wobbly sugar castle on a banquet table, jewelry sparkle doodles, MS Paint.",
    ),
    (
        "0150-mass-jewelry",
        "Breakfast is jewelry that learned mass production.",
        "Sugar castle turning into a cereal box, MS Paint.",
    ),
    (
        "0206-cane-heat",
        "Cane likes heat, water, and brutal harvest work.",
        "Green cane stalks, sun, rain, a harvest sickle, no gore, MS Paint.",
    ),
    (
        "0222-caribbean-engine",
        "Caribbean islands became engines for boiling sweetness.",
        "Simple island map, boiling pot, label CARIBBEAN, MS Paint.",
    ),
    (
        "0238-ledger-not-montage",
        "The labor was enslaved people. The fact is the engine.",
        "A ledger book and a ship, no caricatures, stamp COST, MS Paint.",
    ),
    (
        "0254-teacup-downstream",
        "Cheap sugar in a London teacup is downstream of that ledger.",
        "Cheerful teacup, a dotted line back to a ledger, MS Paint.",
    ),
    (
        "0312-tea-bitter",
        "Tea arrived bitter. Sugar made it drinkable for a kingdom.",
        "Bitter tea cup with a frown, sugar lump turning it into a smile, MS Paint.",
    ),
    (
        "0328-laborer-break",
        "A laborer's break: hot cup and a lump, multiplied by a kingdom.",
        "Factory stick worker with tea, many tiny cups across a map of Britain, MS Paint.",
    ),
    (
        "0344-mintz",
        "Sidney Mintz, Sweetness and Power, nineteen eighty five.",
        "Book labeled SWEETNESS AND POWER, stick scholar, 1985, MS Paint.",
    ),
    (
        "0400-factory-fuel",
        "Sweet calories that fit a factory clock.",
        "Clock, sugar lump, stick worker still moving, MS Paint.",
    ),
    (
        "0416-tea-break-monument",
        "The tea break is a monument. Nobody puts that on the mug.",
        "Mug with a tiny monument doodle nobody notices, MS Paint.",
    ),
    (
        "0432-napoleon-beet",
        "Napoleon needed a sweet that did not require a British navy.",
        "Stickman with a simple bicorne, a beet, a blocked ship with a red X, MS Paint.",
    ),
    (
        "0448-beet-factories",
        "Beet sugar scaled in France and Germany. The tropics monopoly cracked.",
        "Beet field, factory, tropical island with a cracked crown, MS Paint.",
    ),
    (
        "0506-jam-candy",
        "Sugar climbed into jam, biscuits, candy. A mill-town child tasted a duke.",
        "Jam jar, biscuit, candy, a child stickman and a tiny duke, MS Paint.",
    ),
    (
        "0522-floor-drops",
        "The floor dropped until luxury became the baseline.",
        "A falling floor labeled PRICE, a crown sinking to a grocery shelf, MS Paint.",
    ),
    (
        "0538-coffee-argument",
        "Take the sugar away and coffee tastes like an argument.",
        "Coffee cup arguing with a sugar bowl, stickman between them, MS Paint.",
    ),
    (
        "0554-not-fingerprint",
        "You think a sweet tooth is a fingerprint. It is a twentieth-century default.",
        "Fingerprint with a red X, a calendar 1900s labeled DEFAULT, MS Paint.",
    ),
    (
        "0610-hidden-labels",
        "Labels hide crystals in bread, sauce, virtuous yogurt.",
        "Three packages, tiny SUGAR ghosts inside, MS Paint.",
    ),
    (
        "0626-hfcs",
        "Nineteen seventies: high-fructose corn syrup cheaper than cane in factories.",
        "Corn cob vs cane, arrow to a factory bottle HFCS, 1970s, MS Paint.",
    ),
    (
        "0642-cereal-cartoon",
        "Breakfast cereals were a business model wearing a cartoon.",
        "Cartoonish cereal box pointing at a trained stickman, MS Paint.",
    ),
    (
        "0658-bitter-unfinished",
        "Bitter coffee feels unfinished. Fruit feels like it failed.",
        "Coffee frowning, a plain apple with a sad face, MS Paint.",
    ),
    (
        "0716-birthday-architecture",
        "A birthday is a sugar architecture. A reward is a wrapper.",
        "Cake like a building, a wrapped candy as a trophy, MS Paint.",
    ),
    (
        "0732-ripe-signal",
        "Ripe fruit is an old signal. Now the signal plays all day at full volume.",
        "Small fruit speaker vs huge sugar speaker blasting, MS Paint.",
    ),
    (
        "0748-boycott-1790s",
        "Seventeen nineties: abolitionists boycotted slave-grown sugar.",
        "Kitchen stickman pushing away a sugar bowl, sign FREE LABOR, 1790s, MS Paint.",
    ),
    (
        "0806-spoon-ballot",
        "A spoon has been a ballot before. Breakfast was never innocent.",
        "Spoon with a tiny ballot box, MS Paint.",
    ),
    (
        "0822-messy-labels",
        "Modern refusal is messier: certifications, a tired label.",
        "A pile of certification stamps on a sugar bag, tired stickman, MS Paint.",
    ),
    (
        "0838-rare-to-hum",
        "We traded a rare sparkle for a constant hum.",
        "Sparkling tiny jar vs a humming warehouse of sugar, MS Paint.",
    ),
    (
        "0854-fossil-spoon",
        "Your spoon is a fossil of a court, a plantation, a factory.",
        "Spoon with three tiny icons: crown, ship, factory, MS Paint.",
    ),
    (
        "0920-lift-spoon",
        "You lift the spoon and feel like you are only making coffee.",
        "Callback start: stickman holding the same breakfast spoon over coffee, MS Paint.",
    ),
    (
        "0940-price-collapsed",
        "A king's garnish became a grocery reflex when the price collapsed.",
        "Crown garnish shrinking into a grocery barcode, MS Paint.",
    ),
    (
        "1030-stir-know",
        "Look at the spoon like a feast sculpture. Stir if you want. Know.",
        "Same spoon beside a tiny sugar castle, stickman about to stir, MS Paint.",
    ),
]


def main() -> None:
    draft = DraftScript(
        title="Why Sugar Used To Be For Kings",
        description=(
            "You put sugar in coffee like it is weather. It was a spice, then a plantation "
            "ledger, then a tea-break fuel. Sidney Mintz, beet sugar, hidden labels. "
            "Your spoon is a collapsed luxury."
        ),
        tags=(
            "sugar",
            "history",
            "food",
            "tea",
            "caribbean",
            "mintz",
            "breakfast",
            "why",
            "empire",
            "candy",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in BEATS
        ),
        thumbnail_hook="ADD SUGAR?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Sugar Used To Be For Kings",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 24, tzinfo=UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-sugar.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print(out)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))


if __name__ == "__main__":
    main()

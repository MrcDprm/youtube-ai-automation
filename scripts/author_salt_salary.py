"""Author episode 2: word-autopsy of salary, then write senaryo-paint.json."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you are going to pick up a glass shaker and dump a cheap white powder on your food. You will not think twice about it. That powder costs almost nothing. You can buy a lifetime of it for the price of a cheap lunch. It sits in a supermarket aisle next to ketchup, pretending it was always this boring. But for most of human history, that pinch on your plate was a kind of money. Armies marched for it. Cities taxed it. Empires fought over the pans that made it. People were fined, jailed, and in some places killed over a handful of crystals you now knock onto fries. And the word on your paycheck is still hiding that fact. Salary. You say it every month. You never hear the salt inside it. So here is the question that will sit in your hand with the shaker. Why did the stuff in your kitchen used to buy a soldier? And why does your bank still speak the language of a mineral?""",
    """The English word salary comes from the Latin salarium. Salarium comes from sal. Salt. For centuries, schoolbooks told a clean little story. Rome paid its soldiers in salt. That version is too neat, and historians will slap your wrist for it. What the sources actually show is messier, and more interesting. A salarium was an allowance attached to a post. Sometimes it was money earmarked so a man could buy salt. Sometimes it was a ration of the mineral itself. Writers in antiquity treat salt as a state concern, not a garnish. Either way, the Roman state treated salt as a payroll problem. You cannot march a legion if the men cramp, spoil their meat, and desert. The Via Salaria, the Salt Road, ran into Rome from the coastal pans near the Tiber's mouth. It was not a tourist trail. It was a supply line older than most of the temples you picture. When a civilization names a highway after a rock, that rock is not a condiment. It is infrastructure. It is the reason a city can keep men in boots.""",
    """Forget flavor for a second. Flavor is the modern excuse. The old reason was death. Before ice factories, before the electric fridge humming in your kitchen, protein had a clock on it. Meat, fish, milk. Hours in heat, and it became a weapon against you. Salt pulled water out of flesh. Bacteria starved. A dead animal became a store of calories you could carry for months. Salt pork in a barrel. Dried cod stacked like lumber. That is not a cooking tip. That is how cities ate in winter. That is how ships crossed oceans without turning into floating graves. That is how an army stayed an army ten days from the last farm. A barrel of salted fish was a battery. A sack of salt was the charger. If you control the charger, you control who gets to live far from the kill. You do not fight wars for pepper because it is pretty. You fight them when the alternative is hunger with a smell, and a winter that does not negotiate.""",
    """Your body is in on the conspiracy. You leak sodium when you sweat. Lose enough of it and your muscles misfire, your brain fogs, you go down in the heat. This is not a wellness slogan. It is why a day's labor in the sun used to come with a mineral, not just bread. Farmers knew this. Soldiers knew this. Herders moved animals toward salt licks the way you hunt a phone charger. In some places, a block of salt was a gift you did not refuse, because refusing it was refusing work. Livestock that cannot replace salt cannot give you milk, meat, or a plow. So the mineral sat at the junction of three hungers. The cell. The herd. The warehouse. No wonder a wage got named after it. You were not being paid in luxury. You were being paid in the thing that kept you upright. A paycheck made of rock sounds like a joke until you try to stand up without it, and then the joke is on the person who thought salt was optional.""",
    """Now zoom out until the kitchen disappears. In the medieval Sahara, camel caravans hauled slabs of salt south from mines like Taghaza, pale bricks on the humps, and hauled gold and stories north toward the Maghreb. In some markets along that belt, salt and gold traded weight for weight, depending on the season and how far you were from the pans. That sounds like a myth until you remember there is no fridge in a desert, and no ocean in the Sahel. A slab that is cheap on the coast is a fortune inland. Venice did not become rich only from silk and spices. The lagoon city sat on salt pans and then on the politics of salt. Offices existed to measure it, tax it, and decide who could sell it. Whoever could tax the white mineral could fund a navy. Maps of old Europe are secretly maps of who could dry seawater and who had to beg for it. A city with pans could buy ships. A city without them bought permission, which is another word for rent.""",
    """Once something is that necessary, the state notices. Ancient China ran salt as a monopoly for centuries. The Han court argued about it in writing you can still read. It was not a side hustle. It was a pillar of imperial revenue, right up there with grain. Control the salt, and you fund the army without inventing a new tax every spring. In France the gabelle, the salt tax, became a hated machine. The price of salt was not the same in every province. A day's walk could change what a pinch cost. Smuggling became a career. The faux sauniers, the false salt-sellers, treated the border like a job. Families were punished for boiling their own brine. When a government makes it illegal to evaporate seawater in your own backyard, you are no longer talking about seasoning. You are talking about a leash. Revolutions do not start only over speeches. They start over the cheap thing you cannot legally make. The most boring mineral in your cupboard has a body count, and the body count is made of paperwork.""",
    """April nineteen thirty. A thin lawyer in homespun cloth walks two hundred forty miles from Ahmedabad to the Arabian Sea. His name is Mohandas Gandhi. Tens of thousands fall in behind him. At Dandi, on the sixth of April, he bends down and picks up a lump of salty mud. That gesture is a crime. Britain has a salt monopoly in India. You are not supposed to make your own. The empire collects revenue from the mineral in every kitchen, including the poorest ones, which is the point of a monopoly on something nobody can live without. Gandhi's Salt March is easy to turn into a poster. Do not. The point is colder than inspiration. If an empire's dignity depends on stopping a man from drying seawater, the empire is admitting what salt really is. It is a tax on staying alive. A handful of crystals, and the largest power on earth flinches. That is not a cooking story. That is a ledger with a beach at the end of it, and your shaker is the quiet descendant of that crime.""",
    """English never threw the mineral away. It just hid it in the furniture of the language. Worth your salt. That phrase is a performance review from a world where salt was not free, and being worth it meant you covered your own ration. A salacious joke is a salted joke, a dirty little savor. Salad is salted greens. Sauce, salsa, sausage. The same family. The same panic about rot. The same trick of making flesh last long enough to become a meal instead of a warning. You think you are speaking modern. You are speaking a pantry. Every time a manager says somebody is not worth their salt, they are accidentally doing Roman accounting in a glass office. The language remembered the payroll. The kitchen forgot the politics. Your mouth is a museum, and the exhibits are still being used as food. That is why the word on the contract never changed, even after the mineral became a joke.""",
    """So what killed the salt economy? Not a speech. A machine. Industrial mining punched into underground seas, whole rooms of white rock under Cheshire and Michigan and places you will never visit. Railroads moved tons instead of camel-loads. Then refrigeration stole salt's main job, which was stopping time on meat. An icebox, then a humming fridge, and suddenly you did not need a barrel to survive next Tuesday. The mineral that funded navies became a filler in a cardboard cylinder next to your stove. In nineteen twenty four, American cities started adding iodine to table salt because cheap salt had become the perfect public-health Trojan horse. Almost everybody used it. Almost nobody could avoid it. The thing that used to be money became the thing that quietly fixed goiter. That is a hell of a demotion. And a hell of a trick. The most political rock on earth put on a grocery costume, and you believed the costume. You were supposed to. That was the point of making it boring.""",
    """This is you. You still need the sodium. You still say salary. You still trust a fridge more than a barrel. You get annoyed when a restaurant charges extra for a flavor that used to buy a road into Rome. None of that makes you foolish. It makes you modern, which is a kind of amnesia with better lighting and a quieter kitchen. The shaker in your hand is the fossil of a payroll. The word in your contract is the fossil of the Via Salaria. A man once walked to the ocean because a government claimed the right to tax the sea, and a million kitchens were the tax office. Tonight, when you tip those crystals onto a plate, you are not seasoning dinner. You are handling a collapsed currency. It just happens to taste like the ocean you no longer have to march toward. Put the shaker down. Look at it. That is not a condiment. That is the last cheap piece of an empire you still get paid in.""",
]

BEATS: list[tuple[str, str, str]] = [
    (
        "0000-shaker",
        "You pick up a glass shaker and dump cheap white powder on food.",
        "Stickman at a simple kitchen table shaking a glass salt shaker onto a plate, MS Paint, white background.",
    ),
    (
        "0008-cheap-lunch",
        "A lifetime of salt costs a cheap lunch.",
        "Giant salt pile next to a tiny lunch sandwich and a price tag labeled CHEAP, confused stickman, MS Paint.",
    ),
    (
        "0016-pinch-money",
        "That pinch used to be a kind of money.",
        "A pinch of salt transforming into clumsy gold coins, stickman staring, MS Paint.",
    ),
    (
        "0024-armies-tax",
        "Armies marched for it. Cities taxed it.",
        "Tiny stick soldiers marching toward a salt pile, a city with a TAX sign, MS Paint.",
    ),
    (
        "0032-salary-word",
        "The word salary still hides the salt.",
        "Huge handwritten word SALARY with SALT boxed in red inside it, stickman pointing, MS Paint.",
    ),
    (
        "0042-kitchen-soldier",
        "Why did the kitchen used to buy a soldier?",
        "Kitchen shaker on one side, stick soldier on the other, giant red question mark, MS Paint.",
    ),
    (
        "0052-salarium",
        "Salary comes from Latin salarium, from sal, salt.",
        "Wobbly flowchart: SAL then SALARIUM then SALARY, Roman stickman, MS Paint.",
    ),
    (
        "0108-too-neat",
        "Rome paid soldiers in salt is too neat.",
        "Schoolbook labeled PAID IN SALT with a big red X, historian stickman shaking a finger, MS Paint.",
    ),
    (
        "0122-allowance",
        "A salarium was an allowance for salt, or a ration.",
        "Two panels: coins labeled FOR SALT, and a salt bag labeled RATION, MS Paint.",
    ),
    (
        "0136-legion-payroll",
        "Rome treated salt as a payroll problem.",
        "Stick legion marching, a clerk with a PAYROLL scroll and a salt bag, MS Paint.",
    ),
    (
        "0150-via-salaria",
        "The Via Salaria, the Salt Road, ran into Rome.",
        "Wobbly map road labeled VIA SALARIA from sea pans into a stick Rome, MS Paint.",
    ),
    (
        "0208-infrastructure",
        "A highway named after a rock is infrastructure.",
        "Road sign shaped like a salt crystal labeled NOT A CONDIMENT, MS Paint.",
    ),
    (
        "0222-forget-flavor",
        "Flavor is the modern excuse. The old reason was death.",
        "Fancy chef hat with a red X, a skull next to rotting meat, MS Paint.",
    ),
    (
        "0236-protein-clock",
        "Before the fridge, protein had a clock on it.",
        "Fridge with a red X, a fish with a ticking clock, stickman sweating, MS Paint.",
    ),
    (
        "0252-water-out",
        "Salt pulled water out. Bacteria starved.",
        "Salt crystals sucking blue water drops from meat, tiny bacteria with X eyes, MS Paint.",
    ),
    (
        "0310-barrel-battery",
        "A barrel of salted fish was a battery.",
        "Wooden barrel labeled BATTERY full of fish, salt sack labeled CHARGER, MS Paint.",
    ),
    (
        "0326-control-charger",
        "Control the charger, control who lives far from the kill.",
        "Stick king holding a salt sack above tiny hungry stickmen, MS Paint.",
    ),
    (
        "0342-sweat-sodium",
        "You leak sodium when you sweat.",
        "Sweating stickman with dotted salt falling off, label SODIUM, MS Paint.",
    ),
    (
        "0356-heat-collapse",
        "Lose enough and you go down in the heat.",
        "Stickman collapsing under a simple yellow sun, muscles as wobbly zigzags, MS Paint.",
    ),
    (
        "0412-salt-lick",
        "Herders moved animals toward salt licks like a charger.",
        "Simple cow and goat walking to a white salt block, phone-charger doodle nearby, MS Paint.",
    ),
    (
        "0428-three-hungers",
        "Cell, herd, warehouse. Three hungers.",
        "Three clumsy boxes labeled CELL, HERD, WAREHOUSE meeting at a salt pile, MS Paint.",
    ),
    (
        "0444-upright-rock",
        "A paycheck made of rock kept you upright.",
        "Stickman standing on a salary rock, another stickman falling without it, MS Paint.",
    ),
    (
        "0502-taghaza",
        "Sahara caravans hauled salt slabs from Taghaza.",
        "Stick camels carrying white slabs, desert, label TAGHAZA, MS Paint.",
    ),
    (
        "0520-salt-gold",
        "Salt and gold traded weight for weight.",
        "Balance scale with a salt slab equal to a gold brick, MS Paint.",
    ),
    (
        "0536-venice-navy",
        "Venice taxed salt pans and funded a navy.",
        "Lagoon city, salt pans, a clumsy ship labeled NAVY, MS Paint.",
    ),
    (
        "0552-dry-seawater",
        "Maps of who could dry seawater and who had to beg.",
        "Two stick cities: one with pans and ships, one begging with empty hands, MS Paint.",
    ),
    (
        "0610-china-monopoly",
        "China ran salt as a monopoly for centuries.",
        "Imperial stick clerk, salt pile, stamp labeled MONOPOLY, crude CHINA label, MS Paint.",
    ),
    (
        "0626-gabelle",
        "France's gabelle made salt prices a hated machine.",
        "Map of provinces with different SALT PRICE tags, angry stick peasants, label GABELLE, MS Paint.",
    ),
    (
        "0642-illegal-brine",
        "Families punished for boiling their own brine.",
        "Stick family over a pot of seawater, giant forbidden red circle, MS Paint.",
    ),
    (
        "0658-leash",
        "Illegal evaporation is a leash, not seasoning.",
        "Salt shaker tied to a leash held by a crown, stickman on the collar, MS Paint.",
    ),
    (
        "0714-gandhi-walk",
        "April nineteen thirty. Gandhi walks two hundred forty miles.",
        "Thin round-head stickman walking a long wobbly road labeled 240 MILES, sea at the end, MS Paint.",
    ),
    (
        "0732-dandi-crime",
        "At Dandi he picks up salty mud. That is a crime.",
        "Stickman picking a white lump from a beach, stamp CRIME, label DANDI, MS Paint.",
    ),
    (
        "0750-empire-flinch",
        "A handful of crystals, and the empire flinches.",
        "Tiny salt crystals in a hand, a huge crown recoiling, MS Paint.",
    ),
    (
        "0808-worth-salt",
        "Worth your salt is a performance review from that world.",
        "Manager stickman holding a review labeled WORTH YOUR SALT, employee sweating, MS Paint.",
    ),
    (
        "0824-pantry-words",
        "Salad, sauce, salsa, sausage. Same panic about rot.",
        "Four wobbly food doodles labeled SALAD SAUCE SALSA SAUSAGE, a rot skull, MS Paint.",
    ),
    (
        "0840-mouth-museum",
        "Your mouth is a museum still used as food.",
        "Open stickman mouth with tiny museum paintings of salt words inside, MS Paint.",
    ),
    (
        "0856-machines",
        "Mining, railroads, refrigeration killed the salt economy.",
        "Three icons: mine, train, fridge, each punching a salt-money bag, MS Paint.",
    ),
    (
        "0914-iodine",
        "Nineteen twenty four: iodine in cheap salt, goiter fix.",
        "Cardboard salt cylinder labeled IODINE 1924, a neck with a red X over a lump, MS Paint.",
    ),
    (
        "0932-grocery-costume",
        "The political rock put on a grocery costume.",
        "Salt crystal wearing a silly grocery-store cape, barcode sticker, MS Paint.",
    ),
    (
        "1010-this-is-you",
        "You still say salary. You still trust a fridge.",
        "Modern stickman with a paycheck and a fridge, shaker in hand, label THIS IS YOU, MS Paint.",
    ),
    (
        "1040-collapsed-currency",
        "The shaker is a collapsed currency that tastes like the ocean.",
        "Same kitchen shaker from the opening, now stamped COLLAPSED CURRENCY, tiny ocean wave, callback, MS Paint.",
    ),
]


def main() -> None:
    draft = DraftScript(
        title="Why Your Salary Used To Be Salt",
        description=(
            "You shake salt on dinner and never hear the payroll inside the word salary. "
            "Rome, the Salt Road, Sahara slabs, the French gabelle, Gandhi at Dandi. "
            "This is the mineral that used to be money."
        ),
        tags=(
            "salary",
            "salt",
            "history",
            "etymology",
            "rome",
            "gandhi",
            "economics",
            "language",
            "food history",
            "why",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in BEATS
        ),
        thumbnail_hook="IT'S SALT",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Your Salary Used To Be Salt",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 23, tzinfo=UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-salary.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print(out)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))


if __name__ == "__main__":
    main()

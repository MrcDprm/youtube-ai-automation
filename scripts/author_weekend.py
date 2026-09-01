"""Author episode 7: Saturday used to be a workday, then write senaryo-paint.json."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight, or this morning, you are going to treat Saturday as if it belonged to you. You will not commute, or you will commute later, or you will feel slightly illegal for sleeping in. The calendar square is a different color. That color feels like nature. Here is the part that should bother you. For most working people in the industrial centuries, Saturday was a workday. The week had six laboring days and one contested holy day, and even that holy day was not a spa with pancakes. So why does a two-day gap now sit in your bones like a right of birth? Because unions, churches, factory owners, and a car company fought over your idle hours, and then shopping malls harvested the winner. That is the whole plot. Your weekend is not a biological season. It is a labor deal that learned to look like weather, and you check the forecast every Thursday night as if the sky had opinions about your shift. The sky does not. The calendar does, and the calendar had lawyers. You still ask the square for permission to be a person. The square is flattered. That is its job.""",
    """Start with the older rest, because the weekend stole its costume and then denied the theft. Jewish law set the seventh day apart. Christian Europe moved the public pause toward Sunday and filled it with church, not brunch, not a productivity podcast. A holy day is a rule about God and neighbors. It is not two days of errands and a streaming queue you apologize for. Peasants still had seasons that worked them to the bone and then dumped idle weeks on them after harvest. That rhythm was weather and crop, not Saturday branded as self-care. When you say I need a weekend, you are not quoting Genesis. You are quoting a timetable that had to be invented after the timetable invented you as a weekday person. The sacred pause is in the family tree. The Saturday sleep-in is the cousin who showed up with a shopping bag and never left, and now sits at the head of the table like blood.""",
    """Factories wanted the week as a tool that did not care about your soul. Six days on the floor. Sunday for the sermon, or for recovery that still had to fit inside a single sunrise. In nineteenth-century Britain, Saturday began to crack first. Early-closing campaigns and half-holidays, often after noon, gave workers a slice of daylight that was not owned by the mill. Football grew in that slice. So did the pub. So did the idea that a man might be a consumer for an afternoon instead of only a pair of hands. The half-day was not kindness from a kind mill. It was a compromise that kept Monday through Friday intact and sold Saturday evening to sport and shops. If your Saturday still feels like a stolen morning plus a purchased afternoon, you are living in that compromise. The theft and the purchase got married. They had a child called the weekend, and the child now bosses you with a color on a phone.""",
    """America later sold the two-day block as modern efficiency with a human face. In nineteen twenty six, Henry Ford's company moved many factory workers onto a five-day week. Ford talked about rest. He also talked about time to buy the cars the rest was supposed to make room for. Leisure as a market. Idle hours as a showroom. That is not a conspiracy chalkboard. It is an industrialist saying the quiet part in interviews you can still read without a decoder ring. In nineteen thirty eight, the Fair Labor Standards Act wrote a forty-hour week into United States federal law for a lot of covered workers, which is a polite way of saying the government notarized a deal the shop floor had been bleeding for. If you have ever felt that Friday afternoon is a national mood, congratulations. Moods can be legislated. Yours was. The legislation did not cover everyone, which is why the mood still has holes in it.""",
    """Other calendars tried to kill the weekend on purpose, which is how you know it had become valuable. The French Revolution installed a ten-day week, the decade, so the old Sunday would starve of attention and of shops closed in its name. It lasted about twelve years and then Sunday crawled back because people would not let go of a shared pause even when a republic told them to be reasonable. In nineteen twenty nine, the Soviet Union tried a continuous work week. Factories would never sleep. Your day off would not match your neighbor's. Families lost the one day they were all unemployed together. By nineteen thirty one the experiment was walking back, which is a rare thing for an experiment to admit. The lesson is ugly and useful. A shared idle day is not inefficiency. It is how a society agrees to be in the same story for twenty-four hours. Take that away and you still have rest. You just do not have each other. The weekend is, among other things, a synchronization protocol wearing pajamas.""",
    """This is the rehook. You think Saturday is yours because you earned it with five hard days. That sentence is half true and half advertisement, and the advertisement is better at repeating itself. The five days are a schedule. The yours is a feeling the schedule trained until it felt like character. People who work retail, hospitals, hotels, and warehouses already know the punchline. Their Saturday is someone else's leisure infrastructure: coffee, bandages, clean sheets, a warehouse door that opens for your parcel. The weekend is a two-class object. For some it is a right. For others it is the product they sell. When you get annoyed that a shop is closed, you are asking a stranger to donate their synchronization so yours can feel complete. The calendar color lied. It did not lie about rest being good. It lied about rest being evenly distributed, like rain, which also never was.""",
    """Watch what the idle hours became once they were fenced and named. Cinemas, stadiums, Sunday papers, then big-box aisles, then a phone that never clocks out and calls the not-clocking a feature. The weekend was supposed to be empty enough to be human. Capital looked at empty and saw a second shift for wallets. I am not scolding you for buying milk on Saturday. Milk goes off. I am pointing at the inversion. A labor win got restaffed as a consumption slot with better lighting. You can feel both in the same morning: relief that you are not at the desk, and a list that is a desk in disguise. Brunch is a ceremony. The ceremony says you have time. The bill says the time was priced. Neither fact cancels the other. Both can sit in the same orange juice and still be true, which is annoying, and also the point.""",
    """There is a moral leftover from the holy day, and it still nags in the ribs. A culture that once said you must stop now, in public, together, still feels itchy when someone emails on Sunday as if the week had no edge. The itch is older than Slack. It is the ghost of a rule that stopping was a duty, not a wellness tip you bought in an app. You can hate the guilt and still notice what the guilt was protecting: a boundary with witnesses, which is harder to violate than a boundary you keep in your head. The modern weekend often has no witnesses. You rest in private, or you fail to rest in private, and the failure is your personality, not a broken civic agreement. That is a lonely upgrade. The old Sunday could be oppressive. The new Saturday can be a second job you give yourself with a to-do app and a sense of virtue. Oppression and loneliness are not the only two options. They are the two we keep picking because they are familiar.""",
    """So what did we trade? We traded a one-day sacred stop, plus six days of grind, for a two-day civil pause that is unevenly real depending on your badge. We traded a world where Saturday was ordinary labor for a world where Saturday is identity: who you are when the lanyard is in a drawer. We also gained, for millions, a stretch of hours in which a body can be more than a cost on a spreadsheet. That is not nothing. A child who sees a parent on Saturday is living inside a political outcome, not a personality trait of the parent. The trick is pretending the outcome is nature, or that everyone got it, or that Ford invented kindness in a memo. It is a deal. Deals can be rewritten. Some already were, quietly, when apps made every hour available and called it flexibility. Flexibility is a weekend that never quite starts, which is a very expensive kind of free. If every hour can be work, Saturday is a costume. Costumes come off. The deal was supposed to keep one on.""",
    """This is you. You will look at the calendar. Saturday will still be a different color. You will feel a small lift, or a small dread if you work the floor that sells other people their lift. Put your finger on the square. That is not the sky. That is a half-holiday, a car plant memo, a labor statute, a failed ten-day week, a Soviet calendar that tried to unsync families, and a mall that opened into the gap like a plant into a crack. You are allowed to sleep in. You are allowed to work a Saturday and still want the deal to include you instead of using you as furniture. Just stop calling the color natural. Tonight, or this morning, when the square arrives, look at it like a contract with crayon on it. The crayon is cheerful. The contract is the point. Keep the day if you can. Know who paid for the ink, and who still does not get a second color.""",
]

BEATS: list[tuple[str, str, str]] = [
    (
        "0000-saturday-yours",
        "You treat Saturday as if it belonged to you.",
        "Round-head stickman in pajamas, calendar Saturday glowing, MS Paint, white background.",
    ),
    (
        "0008-sleep-in",
        "Sleeping in feels slightly illegal. The square is a different color.",
        "Stickman in bed, alarm with a red X, calendar square colored orange, MS Paint.",
    ),
    (
        "0016-six-workdays",
        "For industrial working people Saturday was a workday.",
        "Week bar with six gray WORK blocks and one small Sunday, MS Paint.",
    ),
    (
        "0024-not-birthright",
        "Why does a two-day gap sit in your bones like a birthright?",
        "Stickman hugging two calendar squares labeled MINE, MS Paint.",
    ),
    (
        "0032-labor-deal",
        "Unions, churches, factory owners, a car company fought over idle hours.",
        "Four stick factions tugging a Saturday square, MS Paint.",
    ),
    (
        "0042-not-season",
        "Your weekend is a labor deal that looks like weather.",
        "Calendar wearing a sun-hat, forecast doodle, MS Paint.",
    ),
    (
        "0052-holy-costume",
        "The weekend stole the costume of an older rest.",
        "Weekend squares wearing a tiny halo stolen from a church, MS Paint.",
    ),
    (
        "0108-sunday-church",
        "Christian Europe paused toward Sunday. Church, not brunch.",
        "Simple church, stick congregation, a brunch plate with a red X, MS Paint.",
    ),
    (
        "0122-peasant-seasons",
        "Peasants had harvest weather, not Saturday.",
        "Field, sun, harvest, no Saturday label, MS Paint.",
    ),
    (
        "0136-not-genesis",
        "I need a weekend is not quoting Genesis.",
        "Book labeled GENESIS with a red X, a timetable labeled YOU, MS Paint.",
    ),
    (
        "0150-cousin-shopping",
        "Saturday sleep-in is the cousin who arrived with a shopping bag.",
        "Two stick cousins, halo vs shopping bag, MS Paint.",
    ),
    (
        "0206-six-days-floor",
        "Six days on the factory floor. Sunday for the sermon.",
        "Factory plus a tiny church on Sunday only, MS Paint.",
    ),
    (
        "0222-half-holiday",
        "Nineteenth-century Britain: Saturday half-holidays after noon.",
        "Saturday clock at noon, morning WORK, afternoon FREE, label BRITAIN, MS Paint.",
    ),
    (
        "0238-football-pub",
        "Football grew in that slice. So did the pub.",
        "Clumsy football and a pub mug in a Saturday afternoon box, MS Paint.",
    ),
    (
        "0254-consumer-afternoon",
        "An afternoon to be a consumer. Compromise, not kindness.",
        "Stickman with a shopping basket, mill still standing, MS Paint.",
    ),
    (
        "0312-ford-1926",
        "Nineteen twenty six: Ford moves many workers to a five-day week.",
        "Car plant, calendar dropping Saturday work, label FORD 1926, MS Paint.",
    ),
    (
        "0328-buy-cars",
        "Rest so you have time to buy the cars.",
        "Stick family with a car and empty Saturday, price tag, MS Paint.",
    ),
    (
        "0344-flsa-1938",
        "Nineteen thirty eight: Fair Labor Standards Act, forty-hour week.",
        "Government stamp 40 HOURS 1938, MS Paint.",
    ),
    (
        "0400-friday-mood",
        "Friday afternoon as a national mood. Moods can be legislated.",
        "Map smiling on Friday, gavel, MS Paint.",
    ),
    (
        "0416-french-decade",
        "French Revolution: a ten-day week so Sunday would starve.",
        "Ten-box week, Sunday shrinking, label DECADE, MS Paint.",
    ),
    (
        "0432-sunday-crawled-back",
        "About twelve years later Sunday crawled back.",
        "Sunday square crawling onto the calendar, MS Paint.",
    ),
    (
        "0448-soviet-1929",
        "Nineteen twenty nine: Soviet continuous week. Factories never sleep.",
        "Factory with eyes open all night, staggered off-days, 1929, MS Paint.",
    ),
    (
        "0506-families-unsynced",
        "Your day off would not match your neighbor's. Families lost a shared idle day.",
        "Two neighbor houses, different OFF signs, sad family table, MS Paint.",
    ),
    (
        "0522-sync-pajamas",
        "A shared idle day is a synchronization protocol wearing pajamas.",
        "Pajama stickmen all idle on the same square, network lines, MS Paint.",
    ),
    (
        "0538-earned-ad",
        "You earned Saturday with five hard days. Half true, half advertisement.",
        "Trophy SATURDAY, a tiny ad sticker on it, MS Paint.",
    ),
    (
        "0554-retail-saturday",
        "Retail and hospitals: their Saturday is someone else's leisure.",
        "Shop stick worker, customers in weekend clothes, MS Paint.",
    ),
    (
        "0610-two-class",
        "The weekend is a two-class object: a right, or a product you sell.",
        "Split calendar: RIGHT vs FOR SALE, MS Paint.",
    ),
    (
        "0626-shop-closed",
        "Annoyed a shop is closed: you want a stranger to donate their sync.",
        "Closed shop sign, angry customer stickman, worker sleeping, MS Paint.",
    ),
    (
        "0642-empty-to-wallet",
        "Empty hours looked like a second shift for wallets.",
        "Empty Saturday box filling with coins and a mall, MS Paint.",
    ),
    (
        "0658-list-disguise",
        "Relief you are not at the desk, and a list that is a desk in disguise.",
        "Happy stickman plus a to-do list shaped like a desk, MS Paint.",
    ),
    (
        "0716-brunch-priced",
        "Brunch says you have time. The bill says the time was priced.",
        "Brunch plate and a bill, both smiling, MS Paint.",
    ),
    (
        "0732-sunday-email-itch",
        "The itch when someone emails on Sunday is older than Slack.",
        "Sunday, an email envelope, a ghost church bell, MS Paint.",
    ),
    (
        "0748-duty-not-wellness",
        "Stopping was a duty with witnesses, not a wellness tip.",
        "Crowd stopping together vs one stickman with a wellness app, MS Paint.",
    ),
    (
        "0806-lonely-upgrade",
        "New Saturday can be a second job you give yourself.",
        "Stickman bossing himself with a to-do app on Saturday, MS Paint.",
    ),
    (
        "0822-saturday-identity",
        "We traded Saturday as ordinary labor for Saturday as identity.",
        "Work overalls vs weekend sunglasses on the same square, MS Paint.",
    ),
    (
        "0838-child-sees-parent",
        "A child who sees a parent on Saturday is living inside a political outcome.",
        "Child stickman and parent on a Saturday square, tiny gavel, MS Paint.",
    ),
    (
        "0854-flexibility-never-starts",
        "Apps made every hour available and called it flexibility.",
        "Phone stretching Saturday until it vanishes, label FLEXIBILITY, MS Paint.",
    ),
    (
        "0920-finger-on-square",
        "You look at the calendar. Saturday is still a different color.",
        "Callback: stickman pointing at the glowing Saturday square, MS Paint.",
    ),
    (
        "0940-not-the-sky",
        "That is not the sky. Half-holiday, car memo, statute, failed calendars, a mall.",
        "Saturday square exploding into five tiny icons, MS Paint.",
    ),
    (
        "1030-crayon-contract",
        "Look at it like a contract with crayon on it. Keep the day. Know who paid.",
        "Calendar contract with crayon, stickman holding it, MS Paint.",
    ),
]


def main() -> None:
    draft = DraftScript(
        title="Why Saturday Used To Be A Workday",
        description=(
            "Saturday feels like weather. It was a workday. Holy Sunday, British "
            "half-holidays, Ford in nineteen twenty six, a forty-hour law, a Soviet "
            "calendar that unsynced families. The weekend is a labor deal."
        ),
        tags=(
            "weekend",
            "saturday",
            "history",
            "labor",
            "work",
            "ford",
            "unions",
            "why",
            "calendar",
            "leisure",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in BEATS
        ),
        thumbnail_hook="SATURDAY?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Saturday Used To Be A Workday",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 24, tzinfo=UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-weekend.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print(out)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))


if __name__ == "__main__":
    main()

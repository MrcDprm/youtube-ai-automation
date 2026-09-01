"""Author the first Badly Drawn Why episode and write senaryo-paint.json."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight, when the sun goes down, you are going to flip a switch. Light will flood the room, and you will not think twice about it. But for ninety-nine point nine percent of human history, that switch did not exist. When the sun set, the world went dark. You could not even see your own hand in front of your face. Modern humans almost never experience this. For over three hundred thousand years, every single one of your ancestors spent roughly half their life in near total darkness. They did not even have candles for most of that time. Just the black sky, the stars, and whatever fire they could keep alive. So what did they actually do for all those hours? The answer changes everything we think we know about sleep, storytelling, and what it means to be human. Let's start with fire. Because fire is the reason any of this was possible.""",
    """The earliest solid evidence of humans controlling fire comes from Wonderwerk Cave in South Africa, roughly one million years ago. But fire did not just keep people warm. Fire completely restructured the human day. Before fire, our ancestors were like every other primate. When the sun went down, you climbed a tree or found a sheltered spot, and you stayed still. Moving at night meant becoming food. Our eyes are terrible in the dark compared to the predators that hunted us. Leopards, hyenas, wolves. All of them could see just fine. Fire changed that equation overnight. Literally. A campfire creates a circle of safety roughly thirty feet in diameter. Inside that circle, predators will not come. Outside that circle, you die. This is not an exaggeration. Anthropologists studying modern hunter-gatherer groups have documented that people who wander away from the fire at night are significantly more likely to be killed by predators. Even today.""",
    """But here is what is fascinating. Fire did not just protect humans at night. It gave them something they had never had before. Extra hours. Think about this. Before fire, the useful day ended at sunset. That is maybe twelve hours in summer, as few as eight in winter. Fire suddenly added two to four usable hours to every single day. Over thousands of generations, those extra hours changed our species. In two thousand fourteen, anthropologist Polly Wiessner published a study in the Proceedings of the National Academy of Sciences. She spent years recording conversations among the Ju slash hoansi of the Kalahari Desert, one of the last groups on Earth still living something close to the original human lifestyle. What she found was striking. During the day, about eighty percent of conversations were practical. Who is hunting where. Which plants are ready. Logistics. Economic negotiations. Daytime talk was work.""",
    """But at night around the fire, the entire character of conversation changed. At night, eighty-one percent of conversations were stories. Tales of people in distant places. Adventures. Myths about the origins of the world. Jokes that made the whole camp laugh. Wiessner argued that firelight conversation is where human culture was born. The campfire was the original theater, the original classroom, the original church. It is where humans learned to think beyond the immediate present and imagine things that do not exist yet. It is where we became us. But the night was not just about stories around the fire. There was something else happening. Something scientists only rediscovered in the last thirty years. You were not designed to sleep the way you sleep right now.""",
    """In two thousand one, historian Roger E. Ekirch published a paper that changed sleep science. He had spent sixteen years digging through historical records, and he found something nobody expected. Over five hundred references, spanning centuries. Prayer books from the fourteen hundreds. Court records. Diaries. Medical texts. Letters from ordinary people. Even passages in Homer's Odyssey. All of them mentioned the same thing. First sleep and second sleep. Before the Industrial Age, people did not sleep in one continuous block. They went to bed shortly after sunset, slept for about four hours, then woke up. They stayed awake for one to two hours in the middle of the night. Then they went back to sleep for another four hours until dawn. This was not insomnia. This was normal. This was how every human on the planet slept for thousands of years.""",
    """And what did people do during that wakeful period in the middle of the night? Everything. A sixteenth century French physician recommended that couples use this window because they would do it better. People visited neighbors. They interpreted their dreams while they were still fresh. They wrote. They simply lay in bed in the dark and thought. A doctor's manual from the fifteen hundreds advised patients that the best time to study and reflect was during the watch, as they called it. The quiet hours between first and second sleep, when the mind was calm and the world was still. Historians had been reading these references for centuries, but they kept translating first sleep as something else. Because they could not imagine that people ever slept differently than we do now. The assumption was so deep that translators literally mistranslated ancient Greek and medieval Latin to make it fit their modern experience.""",
    """Then science confirmed what history had been saying all along. In nineteen ninety-two, psychiatrist Thomas Wehr at the National Institute of Mental Health ran an experiment. He took a group of volunteers and removed all artificial light from their lives. For one month, they experienced fourteen hours of darkness every night, just like our ancestors would have before fire extended the evening. Within weeks, every single participant settled into the same pattern. Four hours of sleep, one to three hours of quiet wakefulness, then four more hours of sleep. Nobody told them to do this. Nobody suggested it. They just did it, as if some ancient program had been waiting inside them the whole time, buried under centuries of artificial light. Wehr measured their hormone levels during the wakeful period and found something remarkable. Their brains were producing elevated levels of prolactin, the same hormone released during meditation. They described feeling peaceful, reflective, almost meditative. It was not just a gap in sleep. It was its own distinct state of consciousness. One that most modern humans have never experienced.""",
    """So what killed it? The answer is simpler than you would think. Light. In the sixteen hundreds, cities began installing street lamps. Paris was one of the first, under Louis the Fourteenth, who wanted to reduce crime. London followed. The night, which had been a place of danger and fear, slowly became navigable. Then came cheaper candles. Then gas lamps in the eighteen hundreds. Then in eighteen seventy-nine, Thomas Edison commercialized the electric light bulb. And within a generation, the night as humans had known it for three hundred thousand years was gone. The word curfew comes from the French couvre-feu. It literally means cover fire. In medieval towns, a bell would ring at night, signaling everyone to cover or extinguish their fires. Night was supposed to be dark. Night was when you slept. In many medieval European cities, walking outside after dark without a lantern was literally illegal. Night belonged to criminals and the supernatural. People feared it in a way that is almost impossible for us to understand today. And then we conquered it. We flooded it with light. And we thought that was progress.""",
    """But here is what we lost. Modern humans are exposed to artificial light an average of seven to eight hours after sunset. This light, especially the blue light from screens, suppresses your body's production of melatonin, the hormone that regulates sleep. Your body does not know the difference between a light bulb and the sun. When light hits your retina at eleven p.m., your brain interprets it as daytime. It delays melatonin release. It fragments your sleep. It disrupts the circadian rhythm that evolved over millions of years. Researchers have found that people who go camping for just one week with no artificial light at all have their melatonin cycles reset by nearly two hours. Their bodies start producing melatonin at sunset instead of hours after it. That is all it takes for three hundred thousand years of programming to reassert itself. We did not just change when we sleep. We eliminated an entire phase of human consciousness.""",
    """That quiet reflective state between first and second sleep, the state Wehr's subjects described as peaceful and meditative, does not exist anymore for most people. Instead, we have insomnia. And we treat it like a disorder. But what if it is not a disorder at all? What if waking up at two a.m. and lying there in the dark is not your body malfunctioning? What if it is your body remembering what it was built to do? For three hundred thousand years, your ancestors spent their nights in a rhythm that modern science is only beginning to understand. They gathered around fires and told stories that built civilizations. They slept in two phases with a window of quiet reflection in between. They lived in darkness so complete that the Milky Way was not something you had to drive to a national park to see. It was just the sky. And every night when they woke in the dark between first and second sleep, they lay there in silence and thought about their lives, their dreams, and the world they would wake up to in the morning. We traded all of that for a light switch. And most of us never even knew it was gone.""",
]

BEATS: list[tuple[str, str, str]] = [
    ("0000-switch", "You flip a switch and light floods the room.", "Stickman in a simple night bedroom flipping a wall switch, messy yellow light filling the room, MS Paint, white background."),
    ("0005-no-switch", "For most of history that switch did not exist.", "Same bedroom wall with no switch and a big red X, confused stickman, MS Paint."),
    ("0009-cant-see-hand", "You could not see your own hand in the dark.", "Stickman in a black blob holding a faint hand in front of its face, MS Paint."),
    ("0017-300k-years", "Three hundred thousand years, half a life in darkness.", "Wobbly timeline arrow labeled 300,000 YEARS, left half black, MS Paint."),
    ("0024-stars-fire", "No candles. Stars, sky, a small fire.", "Black sky with stars, tiny campfire, candle with a red X, MS Paint."),
    ("0031-question", "What did they do for all those hours?", "Giant red question mark, tiny sleep and story icons, MS Paint."),
    ("0039-wonderwerk", "Wonderwerk Cave, South Africa, one million years.", "Brown cave with campfire and crude Africa map, labels SOUTH AFRICA and 1,000,000 YEARS, MS Paint."),
    ("0050-fire-extends-day", "Fire restructured the human day.", "Sun, sunset, then a fire stretching a day bar, MS Paint."),
    ("0054-tree-night", "Climb a tree and stay still.", "Stickman sitting still in a clumsy tree at night, MS Paint."),
    ("0102-predators", "Leopards, hyenas, wolves could see just fine.", "Scared stickman, simple leopard hyena wolf shapes, MS Paint."),
    ("0112-safety-circle", "A campfire circle about thirty feet across.", "Campfire, dashed 30 FT circle, stickmen inside, predator outside, MS Paint."),
    ("0124-wander-danger", "Wander from the fire and you die.", "Stickman leaving the fire circle, red warning, MS Paint."),
    ("0135-extra-hours", "Fire gave them extra hours.", "Clock or day bar with EXTRA HOURS in orange, MS Paint."),
    ("0144-hours-evolution", "Twelve hours in summer, eight in winter, plus two to four.", "Summer 12 H bar, winter 8 H bar, fire plus 2-4 H, MS Paint."),
    ("0157-kalahari", "Polly Wiessner recorded the Ju/'hoansi in the Kalahari.", "Desert stickmen, notepad, labels KALAHARI, MS Paint."),
    ("0215-daytime-work", "Daytime talk was eighty percent work.", "Two stickmen, speech bubbles with spear and plant, 80% WORK, MS Paint."),
    ("0226-night-stories", "At night eighty-one percent were stories.", "Campfire, laughing stickmen, 81% STORIES, MS Paint."),
    ("0240-theater-church", "The campfire was theater, classroom, church.", "Fire in front of three clumsy buildings, MS Paint."),
    ("0256-modern-sleep-x", "You were not designed to sleep like this.", "Stickman in one long bed, alarm clock, huge red X, MS Paint."),
    ("0306-first-second-sleep", "First sleep and second sleep.", "Pile of old books labeled FIRST SLEEP and SECOND SLEEP, MS Paint."),
    ("0332-biphasic-timeline", "Four hours, a wake window, four hours. Not insomnia.", "Night bar 4H, 1-2H, 4H, NOT INSOMNIA, MS Paint."),
    ("0352-night-wake", "Neighbors, dreams, writing, thinking in the dark.", "Four tiny panels of night activities, wholesome, MS Paint."),
    ("0410-the-watch", "They called it the watch.", "Calm stickman awake in a dark bed, THE WATCH, MS Paint."),
    ("0422-mistranslation", "Translators erased first sleep to fit modern sleep.", "Stickman at a desk, FIRST SLEEP crossed out, MS Paint."),
    ("0445-wehr-experiment", "Wehr removed all artificial light for a month.", "Three stickmen, lamp with red X, 14 HOURS DARK, MS Paint."),
    ("0502-ancient-program", "Bodies settled into four, wake, four by themselves.", "Stickman head with sleep-wake-sleep inside, ANCIENT PROGRAM, MS Paint."),
    ("0521-prolactin", "Elevated prolactin. Peaceful. Meditative.", "Peaceful sitting stickman, PROLACTIN, MS Paint."),
    ("0545-light-killed-it", "What killed it? Light.", "Giant yellow light bulb, tiny shocked stickman, MS Paint."),
    ("0549-street-lamps", "Paris street lamps under Louis the Fourteenth.", "Stick lamp posts, tiny crown stickman, STREET LAMPS, MS Paint."),
    ("0604-edison-1879", "Candle, gas, Edison eighteen seventy-nine.", "Candle then gas lamp then bulb labeled 1879, MS Paint."),
    ("0615-curfew", "Curfew means cover fire.", "Bell tower, stickman covering a fire, CURFEW, MS Paint."),
    ("0627-night-illegal", "No lantern after dark was illegal.", "Stickman without lantern in a red forbidden circle, MS Paint."),
    ("0648-progress", "We flooded the night and called it progress.", "Yellow city scribbles, stickman, PROGRESS?, MS Paint."),
    ("0653-blue-light", "Blue screens at eleven p.m. feel like noon to your brain.", "Stickman in bed with blue phone, 11 PM = DAY, MS Paint."),
    ("0718-camping-reset", "One week of camping resets melatonin.", "Triangle tent, sunset, CAMPING RESET, MS Paint."),
    ("0733-insomnia", "We lost that state and named the remainder insomnia.", "Split: calm wake window vs INSOMNIA bed, MS Paint."),
    ("0750-2am-not-broken", "Waking at two a.m. is not your body broken.", "Clock 2:00, calm awake stickman, NOT BROKEN, MS Paint."),
    ("0758-ancestors-sky", "The Milky Way was just the sky.", "Campfire stickmen under a milky way scribble, JUST THE SKY, MS Paint."),
    ("0818-thinking-in-dark", "They lay in the dark and thought.", "Stickman in bed, thought bubble of heart dream sunrise, MS Paint."),
    ("0827-light-switch-trade", "We traded all of that for a light switch.", "Stick hand reaching for a switch, fading stars, WE TRADED THIS, MS Paint."),
]


def main() -> None:
    draft = DraftScript(
        title="Why Your Ancestors Slept Twice Every Night",
        description=(
            "Tonight you will flip a switch and think nothing of it. For three hundred thousand "
            "years, night meant something else: fire, stories, and two sleeps with a quiet watch "
            "in between. This is what we lost."
        ),
        tags=(
            "sleep",
            "first sleep",
            "second sleep",
            "history",
            "fire",
            "circadian rhythm",
            "insomnia",
            "anthropology",
            "human evolution",
            "night",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in BEATS
        ),
        thumbnail_hook="2 AM?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Your Ancestors Slept Twice Every Night",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 22, tzinfo=UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    write_scenario(scenario, out)
    print(scenario.project_id)
    print(out)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))


if __name__ == "__main__":
    main()

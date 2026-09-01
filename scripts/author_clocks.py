"""Author episode 3: trains invented being late, then write senaryo-paint.json."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Right now your phone is going to tell you that you are late. Four minutes. Seven minutes. A red word that feels like a personal failure. You will apologize to a calendar. You will walk faster for a meeting that exists only because two devices agreed on a number. Here is the part that should bother you. For most of human history, being late was not a feeling you could have. There was no shared grid of minutes. Noon was when the sun sat over your town, not over an office three valleys away. Your neighbor on the next ridge ate lunch at a different noon, and nobody sent a complaint. A missed visit meant you came with the light you had, not that you had sinned against a number. So why does a red word on a glass rectangle get to accuse you? Because a train had to not hit another train. That is the whole plot. The shame in your chest is a railroad invention, and you have been carrying it like it was a moral law carved into the universe instead of printed on a timetable.""",
    """Before the tracks, time was local and proud of it. Every town ran on the sun it could actually see. When the sun peaked, that was noon. A clock in Bristol and a clock in London disagreed by minutes, and that was not a scandal. It was geography. Church bells marked a neighborhood, not a planet. Farmers worked by light and hunger, not by a second hand. Ships used hourglasses and noon sights because the ocean does not care about your appointment. Markets opened when enough people arrived, which is a terrible way to run a railroad and a perfectly decent way to run a village. The idea that two cities should share a minute would have sounded like asking two churches to share a steeple. You cannot be late to a noon that belongs only to your street. You can only be early to the dark, or late to the harvest, which is a different kind of disaster, and it does not come with a calendar notification buzzing in your pocket.""",
    """Then the railroad arrived and made local noon into a crash hazard. A train leaving one town at what that town called nine o'clock would meet another train whose nine o'clock was a different sun. Timetables written in local time were a pile of almosts. Almost is how you get two engines occupying the same mile of iron. In eighteen forty seven, British railway companies agreed to run on Greenwich time, the time of an observatory on a hill, not the time of each platform's sky. Passengers called it railway time, sometimes as a joke, sometimes as a complaint. Station clocks were set to it. Some towns kept a second minute hand for the old local noon, a little confession that the sky had been overruled. You could stand on a platform and watch two noons live in one face. That is not poetry. That is a committee solving a collision, and then selling the solution as civilization.""",
    """The man who turned this into a globe is easy to caricature, so do not. Sandford Fleming, a Scottish-Canadian engineer, missed a train in Ireland in eighteen seventy six because the printed timetable was a mess of local hours. He did not write a poem about it. He spent years arguing for a single world grid of twenty-four zones, each an hour wide, anchored to a prime meridian. In eighteen eighty four, delegates from twenty-five countries met in Washington and picked Greenwich as that zero line. Not because England was magically the center of the universe. Because British maps, British ships, and British cables already used it, and a standard that already exists beats a prettier standard that does not. France grumbled. Other meridians were proposed. Greenwich won the paperwork. The planet got a filing system. Your jet lag is that filing system arguing with your liver, which never attended the conference.""",
    """America did it as a corporate stunt before it did it as a law. On November eighteenth, eighteen eighty three, the railroads declared the Day of Two Noons. Clocks across the country paused or jumped so four time zones would replace a fog of local suns. Noon happened twice in some places, or seemed to. People stood in the street and watched the hands. Churches and city halls were not asked first. The trains were. Newspapers treated it like a magic trick and a theft in the same column. Congress caught up in nineteen eighteen with the Standard Time Act, which is a polite way of saying the government notarized a timetable. If you have ever felt that the world was reorganized without your vote, congratulations. Your great-grandparents already sat through the original version, staring at a clock that had just been told a new lie about the sun, and then they went to work anyway.""",
    """Factories were already rehearsing the same trick on the ground. Historian E. P. Thompson later described how industrial capitalism did not just buy hours. It taught people to feel those hours in their bones. The church bell had said, come to this place when you can. The factory bell said, you are late, and lateness is a character flaw you will pay for. Supervisors with watches turned sweat into a column of numbers. A day became shifts. A life became punctuality, which is a polite word for obedience with a face. Children learned the lesson early, which is why school still runs on bells that sound like a small emergency. You were not born ashamed of a minute. You were trained. The red word on your phone is the distant grandchild of a foreman who needed bodies at the machine when the machine was ready, not when you were hungry, not when the light was good, not when the baby finally slept.""",
    """Wristwatches finished the job and made the grid portable. Pocket watches were jewelry and status, something you chose to pull out. Then the First World War put a clock on the soldier's wrist because you cannot coordinate artillery with a device in your pocket and mud on your hands. Officers needed a shared minute so explosions would agree. After the war, the wristwatch came home as a civilian fashion and never left. Now the grid lives against your pulse. You check it in line, in bed, at a table with people you like. The railroad needed a shared minute so engines would miss each other. The factory needed a shared minute so labor would not wander. The army needed a shared minute so shells would land together. You inherited all three, compressed into a rectangle that also sells you shoes. Being on time stopped meaning you arrived with the sun. It started meaning you obeyed a network that does not know your name.""",
    """Here is the rehook, because the feeling is the product, and the product is still in your pocket. You are not late to the universe. You are late to an agreement. The sun did not change. Bristol and London still have different skies. Your body still wants to sleep when it is dark and eat when it is hungry. The grid does not care. Airports, stand-up meetings, school drop-offs, the little apology texts typed with one thumb. All of it is railway time wearing civilian clothes. People who live far from the official noon, at the jagged eastern or western edge of a time zone, know this in their teeth. They go to work in what the map calls morning and the sky still calls night. The zone is a rectangle drawn for trains and radio, not for eyelids. You can live inside a wrong hour for decades and call it normal, and then wonder why you feel slightly fake at eight a.m.""",
    """So what did we trade? We traded a thousand local noons for the ability to miss a person by four minutes and feel ruined. We traded the honest disagreement of church clocks for a planet that can schedule a call across an ocean. That is not nothing. Trains that do not collide are a kind of mercy. A doctor who is not two hours adrift is a kind of mercy. A shift that ends is a kind of mercy compared with work that ends when the boss feels like it. The trick is pretending the grid is nature. It is not. It is a meeting in Washington, a railroad circular in eighteen eighty three, a wartime wrist, a factory bell, a phone default you never changed. Standard time is one of the most successful fictions ever sold, because it sold itself as a fact. You cannot see it, so you assume it was always there, like gravity, or like the shame of the little red word that is now yelling at you.""",
    """This is you. You will tap the screen. You will see that you are late. You will feel a heat in the chest that a farmer in eighteen twenty would not have a name for, because his noon was a shadow on a wall. Put the phone face down. The number is still there. It is Greenwich and Fleming and a day of two noons and a bell that treated your body like a timetable. You are allowed to catch the train. You are allowed to keep the appointment. Just stop confusing the appointment with your worth. Tonight, when the red word appears, look at it the way you would look at a station clock with two minute hands. One hand is the sun. The other is a company that did not want two engines in the same mile. You are standing on that platform. You always were. The accusation was printed on a timetable first, and then it learned to live in your pocket.""",
]

BEATS: list[tuple[str, str, str]] = [
    (
        "0000-red-late",
        "Your phone tells you that you are late.",
        "Round-head stickman staring at a simple phone with huge red letters LATE, MS Paint, white background.",
    ),
    (
        "0008-apologize-calendar",
        "You apologize to a calendar and walk faster.",
        "Stickman bowing to a wall calendar, little speed lines, MS Paint.",
    ),
    (
        "0016-no-grid",
        "For most of history being late was not a feeling you could have.",
        "Confused stickman, empty white space, a clock with no hands and a red X, MS Paint.",
    ),
    (
        "0024-local-noon",
        "Noon was when the sun sat over your town.",
        "Simple yellow sun over a tiny town, label LOCAL NOON, MS Paint.",
    ),
    (
        "0032-neighbor-ridge",
        "The next ridge ate lunch at a different noon.",
        "Two hills, two suns at different heights, two stickmen eating, MS Paint.",
    ),
    (
        "0042-shame-railroad",
        "The shame in your chest is a railroad invention.",
        "Stickman clutching chest, a tiny train labeled SHAME, MS Paint.",
    ),
    (
        "0052-town-clocks",
        "A clock in Bristol and a clock in London disagreed by minutes.",
        "Two town clocks showing different times, labels BRISTOL and LONDON, MS Paint.",
    ),
    (
        "0104-not-scandal",
        "That disagreement was geography, not a scandal.",
        "Wobbly map with two clock faces far apart, label GEOGRAPHY, MS Paint.",
    ),
    (
        "0116-church-bells",
        "Church bells marked a neighborhood, not a planet.",
        "Simple church and bell, a small circle of houses, not the whole globe, MS Paint.",
    ),
    (
        "0128-farmers-light",
        "Farmers worked by light and hunger, not a second hand.",
        "Stick farmer, sun, a stomach doodle, a clock with a red X, MS Paint.",
    ),
    (
        "0142-cannot-be-late",
        "You cannot be late to a noon that belongs only to your street.",
        "Street with one sun, stickman shrugging, NO LATE, MS Paint.",
    ),
    (
        "0200-crash-hazard",
        "Local noon became a crash hazard on the tracks.",
        "Two simple trains about to hit on one track, suns over each, MS Paint.",
    ),
    (
        "0214-almosts",
        "Timetables in local time were a pile of almosts.",
        "Messy papers labeled TIMETABLE, stamp ALMOST, MS Paint.",
    ),
    (
        "0228-1847-greenwich",
        "Eighteen forty seven: British railways run on Greenwich time.",
        "Station clock labeled GREENWICH 1847, tiny observatory, MS Paint.",
    ),
    (
        "0244-railway-time",
        "Passengers called it railway time.",
        "Stick passengers pointing at a clock labeled RAILWAY TIME, MS Paint.",
    ),
    (
        "0258-two-hands",
        "Some clocks kept a second hand for the old local noon.",
        "One clock face with two minute hands, labels SKY and TRAIN, MS Paint.",
    ),
    (
        "0314-fleming-missed",
        "Sandford Fleming missed a train in Ireland in eighteen seventy six.",
        "Stickman running after a leaving train, label IRELAND 1876, MS Paint.",
    ),
    (
        "0330-twenty-four-zones",
        "He argued for twenty-four zones, an hour wide.",
        "Globe sliced into 24 orange wedges, label 24 ZONES, MS Paint.",
    ),
    (
        "0346-washington-1884",
        "Eighteen eighty four, Washington picks Greenwich as zero.",
        "Table of stick delegates, a zero on a map at Greenwich, 1884, MS Paint.",
    ),
    (
        "0404-jet-lag",
        "Your jet lag is that filing system arguing with your liver.",
        "Stickman on a plane, a file cabinet vs a liver doodle arguing, MS Paint.",
    ),
    (
        "0420-two-noons",
        "November eighteen eighty three: the Day of Two Noons.",
        "Huge label TWO NOONS, clocks jumping, American stick towns, MS Paint.",
    ),
    (
        "0438-trains-first",
        "Churches were not asked. The trains were.",
        "Train with a check mark, church with a question mark, MS Paint.",
    ),
    (
        "0454-1918-act",
        "Congress notarized the timetable in nineteen eighteen.",
        "Government stickman stamping STANDARD TIME ACT 1918, MS Paint.",
    ),
    (
        "0510-factory-bell",
        "The factory bell said you are late, and lateness is a flaw.",
        "Factory with a bell, stick worker running, stamp FLAW, MS Paint.",
    ),
    (
        "0526-thompson",
        "Industrial time taught people to feel hours in their bones.",
        "Stick skeleton with clock numbers on the bones, MS Paint.",
    ),
    (
        "0542-school-bell",
        "School still runs on bells that sound like a small emergency.",
        "School, ringing bell, tiny stick children lining up, MS Paint.",
    ),
    (
        "0558-foreman",
        "The red word is the grandchild of a foreman with a watch.",
        "Foreman stickman with a watch, arrow to a phone saying LATE, MS Paint.",
    ),
    (
        "0614-wrist-war",
        "World War One put a clock on the soldier's wrist.",
        "Stick soldier with a wristwatch, simple helmet, no gore, MS Paint.",
    ),
    (
        "0630-watch-home",
        "After the war the wristwatch came home and never left.",
        "Civilian stickman, watch glued to wrist, house behind, MS Paint.",
    ),
    (
        "0646-grid-pulse",
        "Now the grid lives against your pulse.",
        "Wrist with a watch, dotted grid wrapping the arm, MS Paint.",
    ),
    (
        "0702-obey-network",
        "On time started meaning you obeyed a network.",
        "Stickman saluting a web of clocks connected by lines, MS Paint.",
    ),
    (
        "0720-late-to-agreement",
        "You are not late to the universe. You are late to an agreement.",
        "Universe doodle shrugging, a contract labeled AGREEMENT, MS Paint.",
    ),
    (
        "0738-zone-edge",
        "People at the edge of a zone go to work in the sky's night.",
        "Time-zone rectangle, stickman with a briefcase under a black sky, MS Paint.",
    ),
    (
        "0756-civilian-clothes",
        "Airports and stand-ups are railway time in civilian clothes.",
        "Train wearing a tiny suit at an airport, MS Paint.",
    ),
    (
        "0814-four-minutes-ruined",
        "Miss a person by four minutes and feel ruined.",
        "Two stickmen missing each other by a small gap, clock 4 MIN, MS Paint.",
    ),
    (
        "0832-fiction-as-fact",
        "Standard time sold itself as a fact, like gravity.",
        "Poster STANDARD TIME with a fake science seal, apple gravity doodle, MS Paint.",
    ),
    (
        "0850-heat-in-chest",
        "The heat in your chest had no name in eighteen twenty.",
        "Stickman with a red chest blob, old farmer stickman shrugging, 1820, MS Paint.",
    ),
    (
        "0920-phone-facedown",
        "Put the phone face down. The number is still there.",
        "Phone face down on a table, LATE still glowing, MS Paint.",
    ),
    (
        "1000-two-hands-callback",
        "Look at it like a station clock with two minute hands.",
        "Callback: station clock, hands labeled SUN and COMPANY, stickman on a platform, MS Paint.",
    ),
    (
        "1035-timetable-first",
        "The accusation was printed on a timetable first.",
        "Same phone LATE next to an old railroad timetable, MS Paint.",
    ),
]


def main() -> None:
    draft = DraftScript(
        title="Why Trains Invented Being Late",
        description=(
            "Your phone calls you late. Noon used to belong to your own street. "
            "Railway time, Sandford Fleming, the Day of Two Noons, factory bells, "
            "the wartime wristwatch. The shame is a timetable."
        ),
        tags=(
            "time",
            "railroad",
            "clocks",
            "history",
            "standard time",
            "trains",
            "punctuality",
            "industrial revolution",
            "why",
            "noon",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in BEATS
        ),
        thumbnail_hook="TWO NOONS?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Trains Invented Being Late",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 23, tzinfo=UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-clocks.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print(out)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))


if __name__ == "__main__":
    main()

"""Author Drawn Anyway episode 12: Tanganyika laughter epidemic, nineteen sixty two."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 600.0
MINUTES = 9
VOICE = "en-GB-ThomasNeural"
RATE = "+2%"

CHAPTERS = [
    """A school once closed because the lessons could not run. That is not a joke about children, and it is not a cartoon you invented after a trivia night. On Tuesday the thirtieth of January nineteen sixty two, at a mission-run boarding school for girls in Kashasha, about twenty five miles from Bukoba, on the western shore of Lake Victoria in Tanganyika, now Tanzania, three pupils began to act in a way the staff could not timetable. Laughing, and also crying. Restlessness. Attacks that lasted a few hours in some cases, up to sixteen days in a few, about seven on average, then a pause, then often another round. Keep that picture. A boarding school of one hundred fifty nine. Teachers who were not taken by it. A first phase that ran about forty eight days until the eighteenth of March, when ninety five pupils had been affected and the school was forced to close. Official plan: send them home, wait, reopen, and the building would be a school again. Everything after this is just that picture hiring a second closed stamp, and a village that had not asked to be a clinic.""",
    """Start with why a classroom became a clinic. The first careful write-up is A. M. Rankin and P. J. Philip, working from Bukoba, in the Central African Journal of Medicine, May nineteen sixty three: an epidemic of laughing in the Bukoba district. They are the named file, not a punchline and not a stand-up act. Teaching staff, European and African, were unaffected. Students could not concentrate. The internet likes a country that laughed itself shut. File that as a caption that skips the crying. Rankin and Philip recorded laughing and crying in the same attacks, plus restlessness, and they did not find a tidy physical sign that fitted a germ you could point to on a slide. Tanganyika had become independent on the ninth of December nineteen sixty one, about seven weeks before the first three desks. That is a calendar, not a cartoon of a nation, and not a cheap explanation you get to shout. A mission boarding school is also logistics: shared dormitories, away from home, ages twelve to eighteen, a timetable that assumed the room would stay a room and the night would stay a night.""",
    """The first phase is a count, and the count is the plot. From the thirtieth of January to the eighteenth of March, ninety five of one hundred fifty nine. About forty eight days. Then the school closed. Closing a boarding school is not a quarantine in the building. It is a bus, a path, a set of homes that were never designed as isolation wards. Girls went home. Some of those homes were in Nshamba, in what is now Muleba District, about fifty five miles west of Bukoba. Rankin and Philip's table, as later summarised by Christian Hempelmann, puts Nshamba from about the twenty eighth of March into April, about thirty four days, two hundred seventeen people out of a village of about ten thousand, schoolchildren and young adults of both sexes. That is not a giggle that hopped a fence for fun. That is what happens when the official remedy is: this building cannot teach, so empty it. The chemistry is attacks that will not sit still in one dormitory. The logistics is who you send the dormitory to when you still need the dormitory to be empty.""",
    """They reopened on the twenty first of May. Fifty seven pupils were involved until the school shut again at the end of June. Same brick. Same lake light. Second closed stamp. In June the file moved to Ramashenye girls' middle school on the outskirts of Bukoba: the tenth to the eighteenth, forty eight of one hundred fifty four, eight days. Concurrent with that, Kanyangereka, about twenty miles south of Bukoba, three people, the family of a case sent home from Ramashenye. At the time Rankin and Philip were writing, two further schools, boys' schools, had closed. A milder occurrence is noted at a Mbarara primary school in Uganda, about a hundred miles north of Bukoba. Later summaries, not the nineteen sixty three table, say about fourteen schools shut and about a thousand people affected, inside about a hundred miles of Bukoba, and that the wider episode faded after about eighteen months. Some popular retellings stretch it toward June nineteen sixty four. Keep the later tally as a later tally. Keep Rankin's named rooms as the rooms you can actually point to.""",
    """Here is the leftover fact, and it is not that laughter is contagious in the way a joke is contagious. Selected people were tested for food poisoning and for signs of toxic substances. Negative. No known virus was assumed to fit the picture. Rankin and Philip still said a virus could not be excluded on clinical grounds alone, which is a doctor refusing to overclaim. They suggested mass hysteria in a susceptible population, probably a culturally determined disease. That is nineteen sixty three language on the last page. Later writers prefer mass psychogenic illness, MPI, because hysteria had already done too much work as an insult. Hempelmann, revisiting the story in two thousand seven, argued the popular version is too fond of the word laughter, and that the attacks were distress, not a delightful village infection you would book a ticket to see. File both the tests and the label. Do not pretend the tests found a maize poison in the school flour. Do not pretend the label is a joke at Kashasha.""",
    """Rehook, because the internet still likes a plague of giggles that shut a country. Usual summaries say no fatalities and no permanent aftereffects. That is not a punchline. That is the floor. Teachers said that for weeks after an episode, lessons still would not hold. That is the school problem in one sentence: the closed sign can come down and the room still is not a room. Benjamin Kagwa later placed Bukoba beside running manias in Kigezi in July nineteen sixty three and Mbale in November, neighbouring files about agitation and running, not this video's joke and not a sequel you owe the comments. Later papers stack independence, boarding, adolescence, a mission timetable, as stress. Rankin did not name three index personalities with social maps. He named three pupils, then a spread through dormitories and through homes. You are allowed to notice that a closed sign is an instrument. You are not required to laugh at the people who could not use a desk.""",
    """There were rumours, because an unexplained attack in a school always hires rumours. Some talk later remembered a poisoned atmosphere, even atomic tests, which Rankin and Philip did not put on the page as their cause. Some talk remembered maize flour. The tests they did run for food and toxins came back negative. A rumour is not a lab. A lab is not a moral. Rankin also wrote that no literate and relatively sophisticated members of society had been attacked, which is their observation about who presented, not a compliment you should turn into a class cartoon. The people in the file were mostly young, mostly in schools and in the homes those schools emptied into. The adults who ran the timetable stayed on the well side of the register. That mismatch is the logistics, not a verdict on anyone's character.""",
    """None of this is a cartoon of girls as a punchline, and none of it is a hymn to a virus that was never found. They had a boarding school that could not keep a lesson. They had staff who stayed well and a register that would not. They closed on the eighteenth of March, which moved the problem onto the road to Nshamba. They reopened on the twenty first of May, which moved it back into the same walls, and the walls did not hold. Ramashenye got eight days. A family in Kanyangereka got three names on a small list because someone was sent home. The official idea was: this will pass in the building, or it will pass at home. Home is how a village of about ten thousand met two hundred seventeen cases. You are allowed to laugh at the trivia card that says a country laughed. You are not required to use that card, and you are not required to use the children as the joke that sells it.""",
    """So who won. Not the joke. Not the word hysteria, though that is the stamp on the nineteen sixty three last page. Rankin and Philip won a short paper from Bukoba. Kashasha won two closures. Nshamba won a month it did not timetable. Ramashenye won eight days. Kanyangereka won a family list of three. The later tally won fourteen schools and a thousand people, which is a poster, not a roll call. If you need a moral, skip never laugh in class. Take this: sending a boarding school home is a terrible instrument for containing an attack that already lives in a group, and a group is a terrible neighbour for a timetable that needs silence. The next time someone tells you the laughter epidemic, ask whose school closed first, and which village the bus was aimed at. Would you have kept them on the grounds, or would you have emptied the dorms. Three desks, two closed stamps, a road to Nshamba. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no child-victim closeups, no laughing-child faces as a gag, no mockery of the sick. "
    "Distress shown as empty desks, CLOSED stamps, maps, and comic LAUGH/CRY letters on a door, not children's faces. "
    "Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("lessons-could-not", "A school closed because the lessons could not run.", f"Cartoon title beat: an empty classroom, a huge CLOSED stamp, comic LAUGH and CRY letters on the door, no children's faces. Cream paper. {STYLE}"),
    ("not-a-joke", "Not a joke about children. Not a trivia gag.", f"Ink shaking his head at a TRIVIA LAUGH stamp with a red X, mouth closed. {STYLE}"),
    ("jan-30-1962", "January 30, 1962, Kashasha, 25 miles from Bukoba.", f"Calendar January 30 1962, a map pin KASHASHA near a simple lake, no flags. {STYLE}"),
    ("lake-victoria", "Western shore of Lake Victoria, Tanganyika, now Tanzania.", f"A simple lake labeled VICTORIA, shore village, TANGANYIKA 1962. No flags. {STYLE}"),
    ("three-desks", "Three pupils first. Not named faces. Three desks.", f"Three empty wooden desks in a row, numbered 1 2 3, no faces. {STYLE}"),
    ("laugh-and-cry", "Laughing and also crying. Restlessness.", f"Two signs LAUGH and CRY on a classroom door, a restless chair. No faces. {STYLE}"),
    ("hours-to-sixteen", "A few hours, up to 16 days, about 7 on average.", f"A timeline ruler HOURS to 16 DAYS, mark at 7. {STYLE}"),
    ("pause-then-again", "A pause, then often another round.", f"A pause button then a REPEAT stamp. {STYLE}"),
    ("one-fifty-nine", "A boarding school of 159. Teachers not taken by it.", f"A register 159, a TEACHERS WELL stamp. No child closeups. {STYLE}"),
    ("march-eighteen", "March 18: 95 affected. School forced to close.", f"A calendar Mar 18 1962, 95 of 159, CLOSED stamp. {STYLE}"),
    ("plan-reopen", "Official plan: send them home, wait, reopen.", f"A three-step recipe HOME WAIT REOPEN. {STYLE}"),
    ("rankin-philip", "Rankin and Philip, Bukoba, CAJM, May 1963.", f"A journal cover 1963, names RANKIN PHILIP, Bukoba. No portraits. {STYLE}"),
    ("named-file", "They are the named file, not a punchline.", f"A FILE folder labeled NAMED, a JOKE stamp unused. {STYLE}"),
    ("staff-well", "European and African teaching staff unaffected.", f"Two staff hats labeled WELL, empty student desks. {STYLE}"),
    ("cannot-concentrate", "Students could not concentrate. Lessons would not hold.", f"An unreadable chalkboard, books closed, no faces. {STYLE}"),
    ("skips-crying", "The internet caption skips the crying.", f"A clickbait card LAUGH EPIDEMIC with CRYING X'd out. Ink frowning, mouth closed. {STYLE}"),
    ("independence-calendar", "Independence December 9, 1961. About 7 weeks earlier.", f"Two calendar pages DEC 9 1961 and JAN 30 1962, 7 WEEKS. No flags as identity. {STYLE}"),
    ("not-a-nation-gag", "A calendar, not a cartoon of a nation.", f"Ink peeling a NATION GAG sticker off a calendar, mouth closed. {STYLE}"),
    ("boarding-logistics", "Boarding: shared dorms, away from home, ages 12-18.", f"A dormitory of empty bunks, a HOME arrow pointing far away. No faces. {STYLE}"),
    ("timetable", "A timetable that assumed the room would stay a room.", f"A class timetable torn, ROOM still printed. {STYLE}"),
    ("forty-eight-days", "First phase about 48 days. 95 of 159.", f"A 48-day bar, fraction 95/159. {STYLE}"),
    ("closing-is-a-bus", "Closing a boarding school is a bus, not a quarantine.", f"A school bus leaving a CLOSED gate, empty dorm behind. No child faces. {STYLE}"),
    ("nshamba-road", "Some homes were in Nshamba, 55 miles west of Bukoba.", f"A road sign 55 MI to NSHAMBA, a small village. {STYLE}"),
    ("muleba", "Now Muleba District. West of Bukoba.", f"A simple district map MULEBA, pin NSHAMBA. No flags. {STYLE}"),
    ("nshamba-217", "Nshamba: about 217 of 10,000, about 34 days.", f"A village tally 217 / 10000, clock 34 DAYS. {STYLE}"),
    ("both-sexes", "Schoolchildren and young adults, both sexes.", f"Two simple silhouettes far away, not closeups, BOTH SEXES tag. Respectful, tiny. {STYLE}"),
    ("not-a-fence-giggle", "Not a giggle that hopped a fence for fun.", f"A fence with a red X on a hopping giggle cartoon. {STYLE}"),
    ("who-you-send", "Logistics: who you send the dormitory to.", f"An arrow from DORM to VILLAGE, question mark. {STYLE}"),
    ("may-twenty-one", "Reopened May 21. Same building.", f"A calendar May 21, the same school, OPEN stamp. {STYLE}"),
    ("fifty-seven", "57 pupils involved until end of June. Second close.", f"A count 57, a second CLOSED stamp. {STYLE}"),
    ("two-stamps", "Same walls. Two closed stamps.", f"One brick school, two red CLOSED stamps overlapping. {STYLE}"),
    ("ramashenye", "Ramashenye girls' middle school, outskirts of Bukoba.", f"A smaller school labeled RAMASHENYE, outskirts of BUKOBA. No faces. {STYLE}"),
    ("june-eight-days", "June 10 to 18: 48 of 154. Eight days.", f"A calendar Jun 10-18, 48/154, 8 DAYS. {STYLE}"),
    ("kanyangereka", "Kanyangereka, 20 miles south. Three people. A family sent home.", f"A small house 20 MI SOUTH, three respectful nameplates not faces. {STYLE}"),
    ("boys-schools", "At writing: two further boys' schools closed.", f"Two schoolhouses with CLOSED, BOYS tag, no faces. {STYLE}"),
    ("mbarara", "Milder note: Mbarara primary, Uganda, about 100 miles north.", f"A map pin MBARARA 100 MI NORTH, smaller school. No flags as identity. {STYLE}"),
    ("later-tally", "Later tally: about 14 schools, about 1,000 people.", f"A later poster 14 SCHOOLS 1000 PEOPLE, labeled LATER TALLY. {STYLE}"),
    ("hundred-miles", "Inside about 100 miles of Bukoba. About 18 months in later summaries.", f"A 100-mile circle around Bukoba, 18 MONTHS stamp. {STYLE}"),
    ("keep-the-rooms", "Keep Rankin's named rooms as the rooms.", f"Four room labels KASHASHA NSHAMBA RAMASHENYE KANYANGEREKA. {STYLE}"),
    ("tests-negative", "Food-poisoning and toxin tests: negative.", f"Test tubes and a NEGATIVE stamp, no bodies. {STYLE}"),
    ("no-known-virus", "No known virus assumed to fit. Could not exclude on clinic alone.", f"A virus doodle with a question mark, NOT EXCLUDED. {STYLE}"),
    ("mass-hysteria-label", "1963 label: mass hysteria, culturally determined.", f"A 1963 stamp MASS HYSTERIA, a later sticker MPI beside it. {STYLE}"),
    ("hempelmann", "Hempelmann 2007: not a delightful village infection.", f"A NOT DELIGHTFUL stamp over a fake happy village postcard. {STYLE}"),
    ("no-maize-poison", "Do not pretend the tests found a maize poison.", f"A maize sack with a red X, TESTS DID NOT FIND THIS. {STYLE}"),
    ("no-fatalities", "Usual summary: no fatalities, no permanent aftereffects.", f"A respectful card 0 DEATHS, no aftereffects icon. {STYLE}"),
    ("weeks-after", "Teachers: for weeks after, lessons still would not hold.", f"A week calendar after an episode, empty lesson boxes. {STYLE}"),
    ("not-girls-gag", "Not a cartoon of girls as a punchline.", f"Ink peeling a GIRLS GAG sticker off a desk, mouth closed. {STYLE}"),
    ("home-is-how", "Home is how a village of 10,000 met 217 cases.", f"A house icon feeding into a village counter 217. {STYLE}"),
    ("trivia-card", "The trivia card says a country laughed. You need not use it.", f"A trivia card COUNTRY LAUGHED in a waste bin. {STYLE}"),
    ("who-won", "Not the joke. Rankin won a four-page paper.", f"A four-page paper from BUKOBA, no portrait. {STYLE}"),
    ("two-closures", "Kashasha won two closures. Nshamba won a month.", f"Two CLOSED stamps and a NSHAMBA calendar month. {STYLE}"),
    ("terrible-instrument", "Sending a boarding school home is a terrible instrument.", f"A bus labeled CONTAINMENT with a cracked stamp. {STYLE}"),
    ("whose-school", "Ask whose school closed first, which village the bus was aimed at.", f"A first CLOSED arrow to a bus aimed at NSHAMBA. {STYLE}"),
    ("comment-hook", "Would you have kept them on the grounds. Tell me in the comments.", f"Ink pointing at the viewer, mouth closed, empty school grounds, no child faces. {STYLE}"),
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, ten-second cadence)."""
    seconds = index * 10
    return f"{seconds // 60:02d}{seconds % 60:02d}"


def _beats() -> list[tuple[str, str, str]]:
    """Stamp each row with a ten-second mmss slug prefix."""
    need = drawn_beat_count(BEAT_SECONDS)
    if len(_ROWS) != need:
        raise SystemExit(f"need {need} beats, got {len(_ROWS)}")
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
        title="The School That Could Not Stop Laughing",
        description=(
            "Kashasha, nineteen sixty two. Laughing and crying, two closed stamps, "
            "and a bus that was not a quarantine."
        ),
        tags=(
            "history",
            "tanganyika",
            "laughter epidemic",
            "cartoon",
            "true story",
            "1962",
            "kashasha",
            "tanzania",
            "funny",
            "school",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="CLOSED THE SCHOOL",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The School That Could Not Stop Laughing",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-laugh.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    board = PROJECT_ROOT / "output" / "storyboard" / scenario.project_id
    board.mkdir(parents=True, exist_ok=True)
    tsv = board / "beats.tsv"
    lines = ["index\tfilename\tprompt"]
    for index, (slug, _covers, prompt) in enumerate(beats, start=1):
        lines.append(f"{index:03d}\t{index:02d}-{slug}.png\t{prompt}")
    tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")
    chars = sum(len(scene.narration) for scene in scenario.scenes)
    print(scenario.project_id)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", chars)
    print("voice", scenario.tts.voice, "rate", scenario.tts.rate)
    print("accent", scenario.subtitles.accent_color, "numerals", scenario.subtitles.numeral_display)
    print("hook", scenario.youtube.thumbnail_hook)
    print("preset", scenario.video.preset)
    print("tsv", tsv)


if __name__ == "__main__":
    main()

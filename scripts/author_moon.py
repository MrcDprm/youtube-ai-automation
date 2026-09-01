"""Author Drawn Anyway episode 19: Great Moon Hoax, eighteen thirty five."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 600.0
MINUTES = 9
VOICE = "en-AU-WilliamNeural"
RATE = "+4%"

CHAPTERS = [
    """A penny paper once sold the Moon as if it were a fire on the next block. That is not a metaphor, and it is not a cartoon you invented after a trivia night about bat-men in a telescope. On Tuesday the twenty fifth of August eighteen thirty five, The Sun of New York, a one-cent daily at the corner of the penny press, began a six-part series under a stacked headline: Great Astronomical Discoveries Lately Made by Sir John Herschel, LL.D., F.R.S., at the Cape of Good Hope, from a supposed supplement to the Edinburgh Journal of Science. The Moon, the paper said, had bison, unicorns, bipedal beavers, sapphire temples, and winged people it named Vespertilio-homo. Keep that picture. Then put a red X on the gullible-1835 joke. The leftover is not that New York could not tell a goat from a galaxy. The leftover is that a real astronomer was really at the Cape, a dead journal was used as a letterhead, and the press run did the rest.""",
    """Start with why a Moon supplement was supposed to be ordinary. Benjamin Day had founded The Sun in eighteen thirty three as a penny paper: a cent on the street, newsboys, fires, murders, a working-class and immigrant read, not a six-cent mercantile sheet sold by subscription to merchants. The brash tabloid logic was already there: street pennies, steam type, a story that could be shouted. Sir John Herschel, son of William Herschel, had sailed for the Cape of Good Hope in January eighteen thirty four to catalogue the southern sky with a real telescope. That expedition was true. He was not looking for temples. Reverend Thomas Dick, a popular science writer, had already told a huge public that worlds were plural and that the Moon alone held on the order of four point two billion inhabitants. In eighteen twenty six the Edinburgh New Philosophical Journal had run a short piece, The Moon and its Inhabitants, on ideas from Olbers, Franz von Paula Gruithuisen, and Carl Friedrich Gauss about signaling lunarians. The official plan, if Locke later told it straight, was satire: reprint the temperature of the age as if it were Herschel's notebook. The Edinburgh Journal of Science, the letterhead on the series, had already stopped publishing. A dead journal is a costume for a live astronomer. A penny is a costume for a press. Science in eighteen thirty five arrived as a reprint you could hold, not as a photograph from the eyepiece.""",
    """The series was advertised on the twenty first of August as an upcoming reprint from The Edinburgh Courant. Four days later the first installment ran. The byline inside the fiction was Dr. Andrew Grant, described as Herschel's companion. Grant did not exist. The instrument did not exist either, not as written: an immense telescope of an entirely new principle, large enough, the copy implied, to turn the Moon into a parish. Then the menagerie. Lunar forests and beaches. A bipedal beaver that carried its young in its arms like a human being, with huts, Locke wrote, constructed better and higher than those of many tribes of human savages. File that sentence as eighteen thirty five talking, not as a joke you get to spend. Then the headline animal: Vespertilio-homo, man-bat, about four feet, copper-colored hair, membranous wings, seen conversing, temples of sapphire. Other papers copied. Lithographs followed. Edgar Allan Poe had published The Unparalleled Adventure of One Hans Pfaall in the Southern Literary Messenger in June of that year, a balloon to the Moon. Poe later said Locke had stolen the idea. File the accusation. Do not pick a courtroom because it sounds neater.""",
    """Here is the leftover that photographs as a nation of fools and is not one. Herschel was a household name. The Cape was far. A supplement from Edinburgh sounded like the way science arrived in eighteen thirty five: slow ships, reprinted journals, no photograph from the eyepiece. At Yale, contemporary accounts say faculty and students waited on the next number; a later telling has men coming to New York looking for the Edinburgh originals and being walked around the Sun's offices until they went home to New Haven still unsure. File the legend as a legend with a building attached. Do not turn a campus into a punchline about professors. James Gordon Bennett's Morning Herald, a rival, called the series a fake within days of the first number. Most buyers, in the usual retelling, treated the exposé as another paper picking a fight. Missionaries, in that same retelling, asked how to get Bibles to the man-bats. That is a circulation story wearing a collar. It is not a census of American religion. The Sun did not print a formal retraction. On the sixteenth of September it admitted the articles were fabricated. Locke did not put his name on the Moon in eighteen thirty five. In eighteen forty, in a letter to the weekly New World, he said the series was his.""",
    """File the numbers without turning them into a stampede of suckers. Benjamin Day announced that the hoax had lifted The Sun to about nineteen thousand three hundred sixty copies, billed as the highest circulation of any newspaper in the world. Historians later said the jump has been exaggerated in the retellings. File both. A pamphlet reprint of the Moon, in one count, sold about forty thousand copies. Other American papers and then European papers ran the copy as if it were still Edinburgh. An Italian edition picked up lithographs of the fauna. That is a supply chain: one compositor in New York, then a continent of second-hand type. The penny press was already a machine for fires and murders. A Moon with temples is a fire that lasts six mornings. Newsboys hawking a cent a copy is logistics. A steam press that can print more of a fiction than of a shipping list is logistics. Satire that forgets to wink is still a product. The series had bison and blueish goats and pelicans in the copy as well as the bats. The menagerie was a catalogue, which is how a serial sells the next morning: you have not finished the zoo.""",
    """Rehook, because the internet likes a stupid past and a moral about fake news as if eighteen thirty five invented the feed. Locke said, later, that he had meant to mock the way religion was being asked to underwrite inhabited worlds, Thomas Dick's billions in particular. Readers did not file it as a sermon. They filed it as Herschel. That is not cruelty. That is a mismatched label on a crate. The crate was a penny paper fighting other penny papers. Day needed street sales. Locke needed a serial that beat the Herald to the curb. Herschel, who had not been consulted, was in South Africa counting stars. When news of the hoax reached him, later accounts say he was not flattered and then, in the usual retelling, not destroyed either. Do not invent his dinner conversation. Invent nothing. The receipt is: a living astronomer's name was rented, a dead journal was rented, and the Moon was a six-day display window.""",
    """The leftover that is not a bat is a shop. Jean-Nicolas Nicollet, a French astronomer then in America, got rumoured into the byline; he was in Mississippi, not in the Sun's composing room. Lewis Gaylord Clark of The Knickerbocker got rumoured in too. There is no good evidence anyone but Locke wrote it. Jean-Nicolas is a red herring with a passport. Clark is a magazine. Locke had already done a sensational write-up of Matthias the Prophet for Day, which is how the owner noticed him: a cult story as a trial run for a sky story. The Sun kept the extra readers, or claimed to, after the joke cooled. Rival editors who had copied the Edinburgh letterhead had to explain why their science page had been a New York fiction. That embarrassment is the closest thing the episode has to a victim with a masthead. A copied Moon is a terrible alibi. A penny is an honest price for a paper that told you, six times, that the telescope was new in principle.""",
    """None of this is a hymn to a credulous city, and none of it is a cartoon of labourers as fools who should have known better than to buy a cent of astronomy. They had Herschel's real voyage. They had Dick's real bestsellers. They had no photograph. They had a journal title that sounded like a library. You are allowed to laugh at a beaver that builds to a moral, and at a man-bat in a sapphire gift shop. You are not required to laugh at a newsboy sleeping on the street for the pennies, or at Yale looking for a supplement, or at Herschel's name being borrowed while he was actually looking at the southern sky. A telescope of an entirely new principle is a costume. Four point two billion lunar inhabitants is a costume Thomas Dick had already sold in hardback. Nineteen thousand copies is a press count. Forty thousand pamphlets is a second press count. The official idea was: this will read as a joke about science wearing a pulpit. The street idea was: Herschel found a zoo.""",
    """So who won. Not the Moon. Not Vespertilio-homo. Not the Edinburgh Journal of Science, which was already closed. Day won a circulation boast. Locke won a letter in eighteen forty and a rumour that never fully died. Herschel won a catalogue of southern stars that did not include temples. Poe won a grievance. Bennett's Herald won an exposé that most buyers did not treat as the last word. The lithographers won bats with copper hair. If you need a moral, skip never trust a newspaper. Take this: a dead journal is a terrible witness, and a living astronomer's name is a terrible rental property. The next time someone tells you eighteen thirty five believed in bat-men, ask whether they mean the series or the reprints, and whether The Sun ever ran a retraction. Would you have paid a penny for Herschel, or would you have waited for the Herald. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no cruelty, not mud-green archive night, not After Hours File dark. "
    "Hoax shown as a candy penny newspaper, a fake telescope, cute cartoon bat-people as ticket-sale props not horror, "
    "a press, a pamphlet stack, not violence. Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, "
    "oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("penny-moon", "A penny paper sold the Moon like a fire on the next block.", f"Cartoon title beat: a giant penny newspaper THE SUN over a candy Moon, cream paper, hook energy. {STYLE}"),
    ("not-trivia", "Not a bat-men trivia gag.", f"Ink shaking his head at a TRIVIA BATS stamp with a red X, mouth closed. {STYLE}"),
    ("aug-25-1835", "Tuesday 25 August 1835, The Sun, New York.", f"A calendar 25 AUG 1835, a masthead THE SUN, no flag. {STYLE}"),
    ("headline-stack", "Headline: Great Astronomical Discoveries by Sir John Herschel, Cape of Good Hope.", f"A stacked headline GREAT ASTRONOMICAL DISCOVERIES HERSCHEL CAPE. {STYLE}"),
    ("dead-journal", "Letterhead: a supplement to the Edinburgh Journal of Science.", f"A journal cover EDINBURGH JOURNAL OF SCIENCE with a small DEAD tag. {STYLE}"),
    ("vespertilio", "Vespertilio-homo: cartoon man-bats as a ticket prop, not horror.", f"A cute candy bat-person labeled VESPERTILIO-HOMO, four feet tag, not scary, not gore. {STYLE}"),
    ("x-on-gullible", "Put a red X on the gullible-1835 joke.", f"A GULLIBLE 1835 stamp with a giant red X. {STYLE}"),
    ("press-run", "Leftover: a real astronomer, a dead journal, a press run.", f"Three cards HERSCHEL REAL, JOURNAL DEAD, PRESS RUN. {STYLE}"),
    ("benjamin-day", "Benjamin Day founded The Sun in 1833 as a penny paper.", f"A nameplate BENJAMIN DAY, tags 1833 and ONE CENT. No portrait. {STYLE}"),
    ("newsboys", "A cent on the street, newsboys, fires and murders.", f"A newsboy stack of pennies, a tiny FIRE and MURDER extra, not gore. {STYLE}"),
    ("herschel-cape", "John Herschel sailed for the Cape in January 1834. That expedition was true.", f"A ship and a Cape map pin JAN 1834, TELESCOPE TRUE. No flags as joke. {STYLE}"),
    ("thomas-dick", "Thomas Dick: the Moon alone on the order of 4.2 billion inhabitants.", f"A book THOMAS DICK, a tally 4.2 BILLION on a candy Moon. {STYLE}"),
    ("1826-piece", "1826: The Moon and its Inhabitants in the Edinburgh New Philosophical Journal.", f"An 1826 journal clip THE MOON AND ITS INHABITANTS. {STYLE}"),
    ("official-plan", "Official plan: satire, reprint the temperature of the age as Herschel.", f"A clipboard PLAN: SATIRE as HERSCHEL NOTEBOOK. {STYLE}"),
    ("aug-21-ad", "Advertised 21 August as a reprint from The Edinburgh Courant.", f"A teaser ad 21 AUG EDINBURGH COURANT COMING. {STYLE}"),
    ("andrew-grant", "Byline: Dr. Andrew Grant, Herschel's companion. Grant did not exist.", f"A nameplate ANDREW GRANT with a red X FICTION. No portrait. {STYLE}"),
    ("new-principle", "An immense telescope of an entirely new principle. It did not exist as written.", f"A giant candy telescope NEW PRINCIPLE with a small DOES NOT EXIST tag. {STYLE}"),
    ("bipedal-beaver", "A bipedal beaver with huts. File the sentence. Do not spend it as a sneer.", f"A cute cartoon beaver standing, a tiny hut, not a racist cartoon of people. {STYLE}"),
    ("sapphire-temples", "Temples of sapphire. Ticket-sale architecture.", f"A candy sapphire temple on a Moon hill, not a real religion joke. {STYLE}"),
    ("other-papers", "Other papers copied. Lithographs followed.", f"A copy stack OTHER PAPERS and a lithograph of a cute bat-person. {STYLE}"),
    ("poe-pfaall", "Poe, June 1835: Hans Pfaall. Later said Locke stole the idea.", f"A balloon book HANS PFAALL, a tag POE 1835, STOLEN? {STYLE}"),
    ("household-name", "Herschel was a household name. The Cape was far.", f"A famous-name plate HERSCHEL, a long dotted line to CAPE. {STYLE}"),
    ("no-photograph", "Science arrived as reprinted journals. No photograph from the eyepiece.", f"A ship of journals, a camera with a red X NO PHOTO. {STYLE}"),
    ("yale-wait", "Yale: faculty and students waited on the next number.", f"A campus sign YALE, a queue for NEXT INSTALLMENT, no photoreal faces. {STYLE}"),
    ("yale-legend", "Legend: men came to New York looking for Edinburgh originals.", f"A New York office tour LOOKING FOR EDINBURGH, LEGEND tag. {STYLE}"),
    ("herald-fake", "Bennett's Morning Herald called the series a fake.", f"A rival masthead MORNING HERALD, stamp FAKE. {STYLE}"),
    ("bibles-collar", "Missionaries and Bibles for man-bats: a circulation story wearing a collar.", f"A tiny Bible stack and a CIRCULATION stamp, not a mockery of faith. {STYLE}"),
    ("no-retraction", "The Sun never printed a formal retraction.", f"A RETRACTION stamp with a giant red X. {STYLE}"),
    ("sept-16", "16 September: admitted the articles were fabricated.", f"A calendar 16 SEP 1835, FABRICATED, still no apology plaque. {STYLE}"),
    ("locke-1840", "Locke named himself in 1840, a letter to the New World.", f"A letter NEW WORLD 1840, nameplate RICHARD ADAMS LOCKE, no portrait. {STYLE}"),
    ("nineteen-three-sixty", "Day: about 19,360 copies. Billed as the world's highest.", f"A circulation badge 19360, WORLD'S HIGHEST with a small FILE tag. {STYLE}"),
    ("exaggerated", "Historians: the jump has been exaggerated. File both.", f"Two columns BOOST vs EXAGGERATED, a FILE BOTH stamp. {STYLE}"),
    ("forty-thousand", "A pamphlet reprint, in one count, about 40,000 copies.", f"A pamphlet stack 40000 COPIES. {STYLE}"),
    ("europe-type", "European papers ran the copy. Italian lithographs of the fauna.", f"A map of reprints EUROPE, a tiny Italian lithograph bat, no flags as joke. {STYLE}"),
    ("six-mornings", "A Moon with temples is a fire that lasts six mornings.", f"Six newspaper days 1-6, a candy Moon over a press. {STYLE}"),
    ("rehook-feed", "Rehook: the internet likes a stupid past and a fake-news sermon.", f"Ink peeling a STUPID PAST sticker off a newspaper, mouth closed. {STYLE}"),
    ("dick-satire", "Locke later: mock Dick's inhabited worlds, religion asked to underwrite the sky.", f"A pulpit and a telescope as two labels on one crate, SATIRE MISSED. {STYLE}"),
    ("mismatched-label", "Readers filed it as Herschel. A mismatched label on a crate.", f"A crate labeled SATIRE with a shipping tag HERSCHEL. {STYLE}"),
    ("day-needed-sales", "Day needed street sales. Locke needed a serial that beat the Herald.", f"Two clocks STREET SALES vs BEAT THE HERALD. {STYLE}"),
    ("herschel-not-asked", "Herschel was not consulted. He was counting southern stars.", f"A star catalogue SOUTHERN SKY, a rented-name tag on HERSCHEL. {STYLE}"),
    ("nicollet-herring", "Nicollet was in Mississippi, not the composing room. Red herring.", f"A map pin MISSISSIPPI, nameplate NICOLLET, RED HERRING. {STYLE}"),
    ("clark-magazine", "Lewis Gaylord Clark of The Knickerbocker: no good evidence he wrote it.", f"A magazine KNICKERBOCKER, stamp NO GOOD EVIDENCE. {STYLE}"),
    ("matthias-trial", "Locke had written Matthias the Prophet for Day. A cult story as a trial run.", f"Two folders MATTHIAS then MOON, TRIAL RUN. No cult gore. {STYLE}"),
    ("copied-alibi", "Rivals who copied the Edinburgh letterhead had a terrible alibi.", f"A copied masthead EDINBURGH with a stamp TERRIBLE ALIBI. {STYLE}"),
    ("not-fools", "Not a cartoon of labourers as fools for a cent of astronomy.", f"Ink peeling a FOOLS sticker off a READERS sign, mouth closed. {STYLE}"),
    ("dick-hardback", "4.2 billion was a costume Dick had already sold in hardback.", f"A hardback 4.2 BILLION beside a penny paper, SAME COSTUME. {STYLE}"),
    ("telescope-costume", "A telescope of an entirely new principle is a costume.", f"A costume telescope on a hanger NEW PRINCIPLE. {STYLE}"),
    ("who-won-press", "Not the Moon. Day won a boast. Locke won an 1840 letter.", f"A press beating a tiny Moon, badges DAY and LOCKE 1840. {STYLE}"),
    ("poe-grievance", "Poe won a grievance. Bennett won an exposé buyers did not treat as last word.", f"Two cards POE GRIEVANCE and HERALD EXPOSE, a shrug. {STYLE}"),
    ("herschel-catalogue", "Herschel won a catalogue of southern stars that did not include temples.", f"A star book NO TEMPLES listed. {STYLE}"),
    ("dead-witness", "A dead journal is a terrible witness.", f"A tombstone-shaped journal DEAD WITNESS, cream paper, not grim. {STYLE}"),
    ("rental-name", "A living astronomer's name is a terrible rental property.", f"A FOR RENT sign on a nameplate HERSCHEL. {STYLE}"),
    ("penny-or-herald", "Would you have paid a penny for Herschel, or waited for the Herald.", f"Split: a penny THE SUN vs a Herald FAKE stamp, a question mark. {STYLE}"),
    ("receipt", "A press run sold the Moon. Drawn anyway.", f"A receipt card PRESS RUN vs MOON, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Newspaper That Sold a Fake Moon",
        description=(
            "New York Sun, August eighteen thirty five. A penny paper, a dead journal, "
            "and bat-men as a press run."
        ),
        tags=(
            "history",
            "great moon hoax",
            "1835",
            "new york sun",
            "cartoon",
            "true story",
            "herschel",
            "newspaper",
            "funny",
            "logistics",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="THEY SOLD THE MOON",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Newspaper That Sold a Fake Moon",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-moon.json"
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

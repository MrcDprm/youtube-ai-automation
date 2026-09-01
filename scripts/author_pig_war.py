"""Author Drawn Anyway episode 4: Pig War, San Juan Island, eighteen fifty nine."""

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
    """Two empires once nearly went to war over a pig. That is not a metaphor, and it is not a cartoon you invented after lunch. On the fifteenth of June eighteen fifty nine, on San Juan Island, between Vancouver Island and the Washington Territory, an American settler named Lyman Cutlar found a hog in his potato patch. This was not the hog's first visit. Cutlar, twenty five, recent arrival, potatoes on about a third of an acre, shot the animal in a moment of irritation. The pig belonged to Charles Griffin, an Irish Hudson's Bay Company man who ran Belle Vue Sheep Farm. Cutlar felt bad enough to walk over and offer money. Griffin did not want a quiet ten dollars. He wanted a hundred, and he wanted the Americans gone. Keep that picture. One pig. One potato patch. A company farm with thousands of sheep. A treaty that could not decide which channel was the border. Everything after this is just that picture hiring navies.""",
    """Start with why a garden was already a border file. In June eighteen forty six the Oregon Treaty set the line on the forty ninth parallel to the middle of the channel which separates the continent from Vancouver's Island, then south to the Strait of Juan de Fuca. The problem was there were two channels. Haro Strait, nearer Vancouver Island, would make San Juan American. Rosario Strait, nearer the mainland, would make it British. The islands sat in the gap like a comma nobody had agreed how to pronounce. The Hudson's Bay Company, working out of Fort Victoria, treated San Juan as theirs. Salmon-curing by eighteen fifty one. Belle Vue Sheep Farm on the southern shore by December eighteen fifty three. In six years the flock grew from about thirteen hundred sixty nine to more than forty five hundred, plus free-ranging cattle and pigs. By spring eighteen fifty nine, about eighteen Americans had staked potato patches and cabins on the same grass. Washington Territory had claimed the islands in eighteen fifty three. The company called the Americans squatters. The Americans called the company a landlord with the wrong map. If this already sounds like a bad idea written into a garden, you are paying attention.""",
    """The morning of the fifteenth had a witness with a name. A Hawaiian herdsman called Jacob laughed that the pig was up to his old game. Cutlar picked up a gun instead of a fence. He later went to Griffin to settle for the hog, not to argue sovereignty. Griffin told him the Americans were a nuisance on the island, had no business there, and he would have them removed. Cutlar said he had come to settle for shooting a hog, and that he considered the soil American. Within a day, four British officials arrived at the farm and threatened arrest unless Cutlar paid a hundred dollars, more than six times what the hog was worth on a quiet invoice. Word went to the mainland. Brigadier General William S. Harney, who did not love the British, commanded the Department of Oregon. A delegation asked him for protection. Harney did not send a mediator with a calculator. He sent infantry. That is how a potato becomes a landing.""",
    """On the twenty seventh of July, Captain George E. Pickett landed Company D of the Ninth United States Infantry, about sixty four men, near the Hudson's Bay wharf on Griffin Bay, just north of Belle Vue. Pickett would later be famous for a different hill. Here he was a captain with a camp in shouting distance of a sheep farm. James Douglas, governor of the Crown Colony of British Columbia and a Hudson's Bay chief factor, was dismayed, then angry. He ordered Captain Geoffrey Phipps Hornby of the thirty one gun steam frigate HMS Tribune to dislodge Pickett, and also to avoid an armed clash if possible, which is two orders that do not fit in one envelope. Hornby was joined by HMS Satellite and HMS Plumper. Pickett refused to withdraw and wrote Harney for help. Hornby accumulated marines, many of them veterans of landings in China, and then did the useful thing: he waited for his admiral instead of starting the nineteenth century's stupidest amphibious assault.""",
    """Rear Admiral Robert Lambert Baynes arrived appalled. He told Douglas he would not involve two great nations in a war over a squabble about a pig. Write that down. That is the adult in the room, and the room still filled with guns. On the tenth of August Lieutenant Colonel Silas Casey landed about one hundred seventy one more men and took command. By the thirty first of August, four hundred sixty one Americans were in the woods north of Belle Vue, with fourteen field cannons. Lieutenant Henry M. Robert, later the man of Robert's Rules of Order, excavated a redoubt for naval guns off the USS Massachusetts. Only one of those guns was emplaced, and the only time it fired was a salute for Winfield Scott. The British drilled with about fifty two guns and hurled practice shot into bluffs along Griffin Bay. Tourists came on excursion boats from Victoria. Officers from both sides attended church aboard Satellite and shared whisky and cigars in Griffin's tidy house. If you came for a bayonet charge, you already lost the plot. The cartoon is the picnic. The war is the paperwork that almost forgot it was a picnic.""",
    """Washington and London, not having been invited to the whisky, were shocked. Officials who had not seen the picnic treated Cutlar's hog as a fuse. President James Buchanan sent Lieutenant General Winfield Scott, who had already sat on two earlier border crises in the eighteen thirties. Scott took about six weeks from New York via the Isthmus of Panama. In October he arranged, through messengers with Douglas, to peel the reinforcements back: one American company on the island, a British warship in Griffin Bay, and a joint military occupation until diplomats could pick a strait. Both nations approved in November. Harney was rebuked and later reassigned for lighting a match in a room full of sheep. Casey's extra soldiers left, save a company under Captain Lewis Cass Hunt. Pickett came back the next April to replace Hunt. On the twenty first of March eighteen sixty, Royal Marines under Captain George Bazalgette landed on the northwest coast and built what is now called English Camp on Garrison Bay, about thirteen miles from American Camp. The leftover tool was not a bigger gun. It was a second camp and a calendar.""",
    """Joint occupation lasted twelve years, which is a long time to share an island because a pig ate potatoes. For part of it the United States was busy with the Civil War. Pickett went east and got a hill named after him. The camps did not get a battle named after them, which is the point. Royal Marines marched south to American Camp to celebrate the Fourth of July. United States troops went the thirteen miles north to toast Queen Victoria's birthday. Picnics, libations, horse races, sack races, track events: the kind of schedule that makes a war look like a club with two clubhouses. Nobody needed a secret plot for this to stay quiet. They needed Hornby to wait, Baynes to refuse the pig war, and Scott to arrive with a smaller idea than Harney's. A file can hold a landing order and a sack race at the same time. You are allowed to laugh at the race. You are not required to pretend the guns were toys. They were real. They just never received a target that was not a bluff, a drill, or a birthday.""",
    """In eighteen seventy one the Treaty of Washington stuffed several leftover Anglo-American claims into one bundle, including this channel. Kaiser Wilhelm the First of Germany got the San Juan file. He sent it to a three-man commission that sat nearly a year, often described as meeting in Geneva. On the twenty first of October eighteen seventy two the ruling came back through the kaiser: the boundary ran through Haro Strait. San Juan was American. Rosario lost. The Royal Marines left English Camp on the twenty fifth of November eighteen seventy two. The last United States troops left American Camp by July eighteen seventy four. Peace on the forty ninth parallel, finished by a German signature on a water fight that started in a garden. The official idea, years late, was a map. The unofficial idea had been that a hundred dollars and a threat of arrest would tidy a potato patch. Maps are slower. Maps, in this case, did not require a second pig.""",
    """So who won. Not the pig, who is the entire casualty list. Not Harney, who got a rebuke instead of a strait. Not Griffin's hundred dollars, which did not become a doctrine. Cutlar kept a story that still has a park. Pickett kept a footnote before the footnote that ate him. Baynes won the sentence. Scott won the occupation that bored everybody into peace. The kaiser won a homework assignment. If you need a moral, skip destiny. Take this: a landing is a terrible instrument for a problem that needed a receipt, a fence, and a treaty that could count to two channels. The next time someone sells you a simple shot for a shared island, remember ten dollars versus a hundred, and the admiral who would not fight a hog. Would you have paid the hundred. Would you have landed the sixty four. A potato patch, a company pig, a captain who waited, and a picnic that outlasted the panic. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags, "
    "no photoreal faces, no blood, no dead animals shown graphic. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("pig-war-open", "Two empires nearly went to war over a pig.", f"Cartoon title beat: a huge simple pig facing two tiny ship silhouettes on a cream island. {STYLE}"),
    ("not-a-metaphor", "Not a metaphor. Not a cartoon you invented.", f"Ink the mascot shaking his head at a WAR stamp over a pig icon, mouth closed. {STYLE}"),
    ("june-fifteenth", "Fifteenth of June, eighteen fifty nine, San Juan Island.", f"Cartoon calendar June 15 1859, island between two coasts, no flags. {STYLE}"),
    ("potato-patch", "Lyman Cutlar found a hog in his potato patch.", f"Tiny cabin, potato rows, a cartoon pig in the garden, funny not cruel. {STYLE}"),
    ("not-first-visit", "This was not the hog's first visit.", f"A pig with a frequent visitor punch card, potatoes checked off. {STYLE}"),
    ("cutlar-shot", "Cutlar, twenty five, shot the animal in irritation.", f"A cartoon KO cloud over a pig silhouette, no blood, potato basket nearby. {STYLE}"),
    ("griffin-farm", "The pig belonged to Charles Griffin of Belle Vue.", f"A sheep-farm sign BELLE VUE, Irish manager hat, pig icon. {STYLE}"),
    ("ten-vs-hundred", "Cutlar offered money. Griffin wanted a hundred.", f"Two price tags: $10 versus $100, the small one ignored. {STYLE}"),
    ("keep-picture", "One pig, one patch, a treaty with two channels.", f"Three icons: pig, potato, forked channel map. {STYLE}"),
    ("treaty-blur", "Why a garden was already a border file.", f"Ink pointing at a treaty scroll with a blurry dotted line, mouth closed. {STYLE}"),
    ("forty-nine", "Oregon Treaty, eighteen forty six, forty ninth parallel.", f"Cartoon map with 49th parallel stopping at a messy water gap. {STYLE}"),
    ("two-channels", "Two channels: Haro or Rosario. Nobody agreed.", f"Split water map labeled HARO and ROSARIO, island stuck in the middle. {STYLE}"),
    ("comma-island", "The islands sat in the gap like a comma.", f"A comma-shaped island between two ink coastlines. {STYLE}"),
    ("hbc-claim", "Hudson's Bay treated San Juan as company ground.", f"A company stamp on an island outline, sheep icons, no flags. {STYLE}"),
    ("salmon-then-sheep", "Salmon-curing, then Belle Vue Sheep Farm.", f"Cartoon salmon crate next to a sheep, timeline arrow 1851 to 1853. {STYLE}"),
    ("flock-grows", "Flock from about thirteen hundred to over forty five hundred.", f"A growing pile of simple sheep shapes, 1369 to 4500 labels. {STYLE}"),
    ("eighteen-settlers", "By spring eighteen fifty nine, about eighteen Americans.", f"Eighteen tiny cabins and potato patches on shared grass. {STYLE}"),
    ("squatters-claims", "Company said squatters. Settlers said wrong map.", f"Two clipboards arguing: SQUATTER versus CLAIM, cream paper. {STYLE}"),
    ("third-acre", "Cutlar's potatoes: about a third of an acre.", f"A tiny fenced potato patch beside a huge sheep pasture. {STYLE}"),
    ("jacob-laughs", "Jacob the herdsman: the pig was up to his old game.", f"Cartoon herdsman pointing at a pig in potatoes, speech: OLD GAME. {STYLE}"),
    ("gun-not-fence", "Cutlar picked up a gun instead of a fence.", f"A fence post unused, a simple gun with a red X over violence, pig KO puff. {STYLE}"),
    ("settle-the-hog", "He went to settle for the hog, not sovereignty.", f"Cutlar with a coin purse at a farm door, HOG NOT BORDER sign. {STYLE}"),
    ("nuisance-line", "Griffin: Americans are a nuisance. I shall have you removed.", f"A speech bubble NUISANCE over a company desk, no portrait. {STYLE}"),
    ("american-soil", "Cutlar: I consider it American soil.", f"A boot on a potato row, SOIL label, simple and tense not jingo. {STYLE}"),
    ("four-officials", "Four British officials threatened arrest for a hundred dollars.", f"Four tiny officials, a $100 bill, handcuffs icon, no flags. {STYLE}"),
    ("harney-match", "General Harney did not send a calculator. He sent infantry.", f"A calculator in the trash, toy soldiers marching toward an island. {STYLE}"),
    ("potato-landing", "That is how a potato becomes a landing.", f"A potato sprouting a tiny troop ship, cream paper. {STYLE}"),
    ("july-twenty-seven", "Twenty seventh of July: Pickett lands.", f"Cartoon calendar July 27, small boat at a wooden wharf. {STYLE}"),
    ("sixty-four", "Company D, Ninth Infantry, about sixty four men.", f"Sixty-four tally marks beside a tiny camp, 64. {STYLE}"),
    ("griffin-bay", "Camp in shouting distance of the sheep farm.", f"Tents next to a sheep barn and a wharf labeled GRIFFIN BAY. {STYLE}"),
    ("douglas-angry", "Governor Douglas was dismayed, then angry.", f"A governor desk with a DISMAYED then ANGRY stamp, no portrait. {STYLE}"),
    ("two-orders", "Dislodge Pickett. Avoid a clash. Two orders, one envelope.", f"One envelope containing two contradictory notes, Ink raising an eyebrow. {STYLE}"),
    ("three-ships", "Tribune, Satellite, Plumper in the bay.", f"Three simple steam-frigate silhouettes, no flags as the joke. {STYLE}"),
    ("pickett-stays", "Pickett refused to withdraw and wrote for help.", f"A tent with a STAYING sign, a letter flying inland. {STYLE}"),
    ("hornby-waits", "Hornby waited for his admiral instead of landing.", f"A captain at a ship's rail, WAIT sign, marines still aboard. {STYLE}"),
    ("baynes-sentence", "Baynes: he would not war two nations over a pig.", f"An admiral hat over a pig icon with a big NO WAR stamp. {STYLE}"),
    ("casey-august", "Tenth of August: Casey lands about one hundred seventy one.", f"Calendar August 10, more tents, 171 label. {STYLE}"),
    ("four-sixty-one", "By month's end: four hundred sixty one Americans, fourteen cannons.", f"A camp diagram 461 and 14 guns, toy-like, no gore. {STYLE}"),
    ("roberts-redoubt", "Henry M. Robert dug a redoubt. Later: rules of order.", f"A shovel digging an earthwork next to a RULES OF ORDER book. {STYLE}"),
    ("tourist-boats", "Tourists came from Victoria to watch the drills.", f"Cartoon excursion boat with tiny spectators, picnic baskets. {STYLE}"),
    ("whisky-church", "Officers shared church, whisky, and cigars at Griffin's house.", f"A tidy farmhouse, cigars and teacups, two hats on one peg. {STYLE}"),
    ("picnic-not-charge", "The cartoon is the picnic, not the bayonet.", f"Ink ripping a BAYONET ticket, holding a picnic blanket, mouth closed. {STYLE}"),
    ("buchanan-scott", "Buchanan sent Winfield Scott, six weeks via Panama.", f"A long dotted travel line New York to an island, SCOTT suitcase. {STYLE}"),
    ("joint-occupation", "Joint occupation: one company, one ship, wait for diplomats.", f"A handshake over a shared island, small camp plus one ship. {STYLE}"),
    ("harney-rebuke", "Harney was rebuked for lighting a match among sheep.", f"A MATCH stamp on a sheep-farm file, REBUKE in red. {STYLE}"),
    ("english-camp", "March twenty first, eighteen sixty: English Camp on Garrison Bay.", f"Calendar March 21 1860, tents on a north bay, 13 MILES arrow. {STYLE}"),
    ("twelve-years", "Twelve years of sharing an island because a pig ate potatoes.", f"A long calendar ribbon 1859 to 1872, pig and potato icons. {STYLE}"),
    ("sack-races", "Fourth of July and the Queen's birthday: sack races.", f"Cartoon sack race between two camps, funny, no flags as identity. {STYLE}"),
    ("kaiser-homework", "Eighteen seventy two: Kaiser Wilhelm gets the channel homework.", f"A German emperor's desk with a strait map and a pig paperweight, no flags. {STYLE}"),
    ("haro-wins", "Twenty first of October: boundary through Haro Strait.", f"Cartoon map with HARO circled, island tinted as the settled side, no flags. {STYLE}"),
    ("marines-leave", "Royal Marines left November twenty fifth, eighteen seventy two.", f"A departing small boat, empty north camp, calendar Nov 25 1872. {STYLE}"),
    ("who-won", "Who won. Not the pig. The pig is the casualty list.", f"A clipboard: HUMAN CASUALTIES 0, PIG 1, funny not grim. {STYLE}"),
    ("ten-or-hundred", "Remember ten dollars versus a hundred, and the admiral who waited.", f"Ink holding $10 and $100 signs, WAIT hat, mouth closed. {STYLE}"),
    ("comment-hook", "Would you have paid the hundred. Tell me in the comments.", f"Ink the mascot pointing at the viewer, mouth closed, cream paper. {STYLE}"),
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
        title="The War Fought Over a Pig",
        description=(
            "San Juan Island, eighteen fifty nine. A potato patch, a company pig, "
            "and two empires that hired navies before they hired a receipt."
        ),
        tags=(
            "history",
            "pig war",
            "san juan",
            "cartoon",
            "true story",
            "1859",
            "border",
            "hudsons bay",
            "funny",
            "oregon treaty",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="ONLY THE PIG",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The War Fought Over a Pig",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-pig.json"
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
    print("tsv", tsv)


if __name__ == "__main__":
    main()

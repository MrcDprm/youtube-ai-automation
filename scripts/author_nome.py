"""Author Drawn Anyway episode 22: Nome serum run, nineteen twenty five."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 630.0
MINUTES = 9
VOICE = "en-US-GuyNeural"
RATE = "+2%"

CHAPTERS = [
    """A statue in Central Park is dedicated to the sled dogs that ran antitoxin to Nome, and the bronze is Balto. That is not a metaphor, and it is not a cartoon you invented after a trivia night about one husky saving Alaska. On the second of February nineteen twenty five, at half past five in the morning, Gunnar Kaasen drove down Front Street with a twenty-pound cylinder that had come six hundred seventy four miles from Nenana in one hundred twenty seven and a half hours. Twenty mushers. About one hundred fifty dogs. The last leg was about fifty three miles. Togo's team had already run two hundred sixty one. Keep that split. Then put a red X on the joke that one dog did the whole trail. The leftover is not a cute montage. The leftover is a relay.""",
    """Start with why a plane was supposed to be the modern plan. Nome sits about two degrees south of the Arctic Circle. In winter the Bering port is icebound. Curtis Welch was the only doctor, with four nurses at Maynard Columbus Hospital. The town's diphtheria antitoxin had expired before the last ship left. On the twenty second of January he radioed that an epidemic was almost inevitable and that he needed one million units; mail was the only transport; about three thousand people lived in the district. The U.S. Public Health Service found one point one million units on the West Coast, too slow by ship. On the twenty sixth, three hundred thousand forgotten units turned up in an Anchorage hospital, glass vials in padded quilts in a metal cylinder a little over twenty pounds. Mayor George Maynard wanted a plane. Alaska had three vintage biplanes, dismantled for winter, open cockpits, water-cooled engines. The board of health voted unanimously for dogs. Governor Scott Bone ordered the first batch by sled. The official plan, if Mark Summers of Hammon Consolidated Gold Fields had written it, was two fast teams meeting at Nulato. The trail from Nulato to Nome usually took thirty days. Welch said the serum would last about six days on the trail. That mismatch is the whole problem.""",
    """File the first handoff, because the statue does not start here. Edward Wetzler, the postal inspector, and the Northern Commercial Company's mail line turned drivers back to their roadhouses. Most Interior legs were Athabascan mail carriers. Wild Bill Shannon took the cylinder at Nenana's train at nine at night on the twenty seventh, minus fifty Fahrenheit, nine dogs led by Blackie. He jogged beside the sled and still took frostbite. At Minto, parts of his face were black from cold, minus sixty two. He warmed the serum, rested four hours, dropped three dogs. Those three later died of the cold; a fourth may have. File it. Do not draw it. Edgar Kalland's hands froze to a birch handlebar until boiling water freed them. Charlie Evans, at minus sixty two, forgot rabbit skins on two short-haired leads; both collapsed; he pulled the sled himself. Tommy Patsy covered thirty six miles in about three and a half hours. Jackscrew Madros jogged the Kaltag Portage. Victor Anagick and Myles Gonangnan took it to Unalakleet and Shaktoolik. Gonangnan refused the ice shortcut and still hit a whiteout. That is two thirds of the miles the papers later forgot.""",
    """Here is the leftover the movies file as Balto. Leonhard Seppala had already left Nome with Togo, a twelve-year-old Siberian, expecting to intercept at Nulato, a six hundred thirty mile round trip he had once done in four days. The telegraph could not catch him in the small villages. Henry Ivanoff, a half mile out of Shaktoolik, tangled with a reindeer and shouted that he had the serum. Seppala turned around, crossed about twenty miles of Norton Sound ice in the dark at a wind chill around minus eighty five, with Togo in a straight line. They made Isaac's Point after eighty four miles in a day. While they slept, the ice they had just crossed blew out to sea. Togo picked the remaining shore ice. They climbed the ridges of Little McKinley, about five thousand feet of up and down in eight miles, and at three in the afternoon on the first of February handed off to Charlie Olson at Golovin, seventy eight miles from Nome. Togo's team: two hundred sixty one miles of the relay, the longest by about two hundred. Balto's team: about fifty three. That is arithmetic, not a grudge.""",
    """Olson took twenty five miles to Bluff in a blizzard that blew the sled off the trail and frostbit his hands while he blanketed dogs. Welch, with winds around eighty miles an hour, ordered a halt so the cylinder would not be lost; the lines died after Solomon. Kaasen waited, then left into a headwind with Balto and Fox. Visibility so poor he could not always see the dogs nearest the sled. A gust flipped the sled and buried the cylinder. He found it with bare hands and took frostbite. He missed Solomon by two miles and kept going. At Point Safety, three in the morning on the second of February, Ed Rohn was asleep, thinking the relay had stopped. Kaasen did not wake him. He ran the last twenty five into Nome. Not a single ampule broken. Frozen, then thawed, ready by noon. Some mushers, including Rohn, thought Kaasen wanted the last street. File the argument. Do not pick a cartoon villain. A last mile is still a mile. A skipped handoff is still logistics.""",
    """Rehook, because the internet likes one dog and a bronze. Put a red X on skipping the relay. Balto became the most famous canine after Rin Tin Tin. On the fifteenth of December nineteen twenty five, Frederick Roth's statue went up in Central Park, dedicated to all the sled dogs, modeled on Balto, wearing Togo's colors in the usual complaint. Seppala said he never had a better dog than Togo, and that Balto was never in a winning team. He said Kaasen's true leader was Fox. No good race record puts Balto in front before nineteen twenty five. File the dispute. Kalland later said, of the Interior run, it was just an everyday occurrence as far as we were concerned. The Senate stopped work to recognize the event. Coolidge sent letters. The H. K. Mulford Company gave gold medals. Los Angeles gave Balto a bone-shaped key. The Native mushers who ran most of the Yukon got less ink. A statue is a costume for a last street. A mail route is a costume for an epidemic.""",
    """File the second cylinder, because the first three hundred thousand units were a delay, not a finale. The one point one million left Seattle on the thirty first of January aboard a schedule that would not hit dog sled until about the eighth of February. Welch asked for half by air. Bone held, then under pressure allowed a plane; the plane failed to start, overheated, failed again, and the mission was scrapped. Ed Rohn did deliver the second batch into Nome on the fifteenth, another blizzard, about ninety miles. By the third of February the first batch was still effective and the outbreak was called under control. Official diphtheria deaths in Nome are listed as five, six, or seven. Welch later thought there were many more cases in camps outside town that never hit the ledger. File the range. Do not spend it as a body count, and do not draw it. Forty three new cases in nineteen twenty six were managed with fresh serum. That is a supply chain with a second truck.""",
    """None of this is a hymn to a single husky, and none of it is a cartoon of a sickroom. They had expired vials and a closed port. They had three biplanes in pieces. They had a six-day clock on a thirty-day trail. You are allowed to laugh at a statue that got the last five percent of the miles, and at a musher who did not wake the next roadhouse. You are not required to laugh at Shannon jogging at minus fifty, or at Evans pulling a sled when two leads went down, or at Togo smelling a line across ice that would be gone by morning. A twenty-pound cylinder is a costume for one million units that had not yet arrived. A train to Nenana is a costume for a coast that would not thaw until July. The official idea was: two teams, Nulato, Seppala's shortcut. The street idea was: Balto. The leftover idea is: twenty names on a mail contract.""",
    """So who won. Not the biplanes. Not the last-street photograph alone. Shannon won a first night and frostbite. Kalland won a handlebar that needed boiling water. Patsy won a speed. Seppala and Togo won two hundred sixty one miles and a later glass case in Wasilla. Kaasen and Balto won Front Street at five thirty and a statue that says six hundred miles even when the bronze is one dog. The Athabascan and Inupiat mail men won two thirds of the distance and a quote about an everyday occurrence. Nome won thawed ampules by noon. If you need a moral, skip dogs are heroes. Take this: a last mile is a terrible whole story, and a relay is a terrible honest one. The next time someone tells you Balto saved Nome, ask how many teams, and whether Togo's ice was already open ocean when the statue was sketched. Would you have given the bronze to the last lead, or to the twenty. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no cruelty, no child-victim closeups, not mud-green archive night, "
    "not After Hours File dark. Serum run shown as candy sleds, a metal cylinder, trail maps, "
    "cartoon huskies not photoreal, not a sickroom, not dying dogs, not disaster. Recurring mascot Ink "
    "may cameo: mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("balto-statue", "A Central Park statue is Balto. The last street was not the whole trail.", f"A candy bronze dog statue labeled BALTO, a tiny CENTRAL PARK tag. Cream paper. {STYLE}"),
    ("not-trivia", "Not a one-husky trivia gag.", f"Ink shaking his head at a ONE DOG SAVED ALASKA stamp with a red X, mouth closed. {STYLE}"),
    ("front-street", "2 Feb 1925, 5:30 a.m., Front Street, Nome.", f"A street sign FRONT STREET, clock 5:30, date 2 FEB 1925. {STYLE}"),
    ("cylinder", "A 20-pound metal cylinder, 674 miles from Nenana in 127.5 hours.", f"A metal cylinder 20 LB, tags 674 MI and 127.5 HRS. {STYLE}"),
    ("twenty-teams", "20 mushers, about 150 dogs.", f"A tally 20 MUSHERS, 150 DOGS, tiny sled icons. {STYLE}"),
    ("split-miles", "Last leg about 53 miles. Togo's team 261.", f"A split ruler BALTO ~53 vs TOGO 261. {STYLE}"),
    ("x-one-dog", "Put a red X on one dog did the whole trail.", f"A ONE DOG WHOLE TRAIL stamp with a giant red X. {STYLE}"),
    ("leftover-relay", "Leftover: a relay, not a cute montage.", f"A baton handoff of a tiny cylinder between two sleds, RELAY. {STYLE}"),
    ("nome-ice", "Nome, icebound port, two degrees south of the Arctic Circle.", f"A candy Nome map pin, ICEBOUND PORT, Arctic Circle line. No flag as joke. {STYLE}"),
    ("welch-hospital", "Curtis Welch, only doctor, four nurses, Maynard Columbus Hospital.", f"A nameplate CURTIS WELCH, tag 4 NURSES, tiny hospital. No portrait, no sickroom. {STYLE}"),
    ("expired", "The town's antitoxin had expired before the last ship.", f"A vial with an EXPIRED tag, a ship sailing away. {STYLE}"),
    ("telegram", "22 Jan: epidemic almost inevitable, one million units, mail only.", f"A telegram 22 JAN, 1 MILLION UNITS, MAIL ONLY. {STYLE}"),
    ("anchorage-find", "26 Jan: 300,000 forgotten units in Anchorage, quilts, 20-pound cylinder.", f"A hospital crate 300000 UNITS, quilt, cylinder. {STYLE}"),
    ("three-planes", "Three vintage biplanes, dismantled, open cockpits. Board voted dogs.", f"Three boxed biplanes, a vote stamp DOGS. {STYLE}"),
    ("bone-order", "Governor Scott Bone: first batch by sled.", f"A nameplate SCOTT BONE, order FIRST BATCH BY SLED. No portrait. {STYLE}"),
    ("nulato-plan", "Official plan: two teams meet at Nulato. Trail usually 30 days. Serum ~6 days.", f"A clipboard NULATO, 30 DAYS vs 6 DAYS. {STYLE}"),
    ("mail-carriers", "Most Interior legs: Athabascan mail carriers. Wetzler turned them to roadhouses.", f"A mail-route map INTERIOR, ATHABASCAN MAIL. {STYLE}"),
    ("shannon-nenana", "Wild Bill Shannon, Nenana train, 27 Jan 9 p.m., -50°F, lead dog Blackie.", f"A train platform NENANA 9PM, -50 F, nameplate SHANNON, dog tag BLACKIE. Cartoon dog not photoreal. {STYLE}"),
    ("kalland-bar", "Kalland: hands froze to a birch handlebar. Boiling water.", f"A sled handle with a kettle of boiling water, nameplate KALLAND. Not gore. {STYLE}"),
    ("evans-pull", "Charlie Evans pulled the sled himself when two leads went down.", f"A musher pulling a sled, nameplate EVANS, minus 62 tag. No dead dogs drawn. {STYLE}"),
    ("patsy-speed", "Tommy Patsy: 36 miles in about 3.5 hours.", f"A speed badge PATSY 36 MI / 3.5 HR. {STYLE}"),
    ("gonangnan", "Gonangnan refused the ice shortcut, still a whiteout to Shaktoolik.", f"A trail fork ICE X vs HILLS, nameplate GONANGNAN. {STYLE}"),
    ("two-thirds", "That is two thirds of the miles the papers later forgot.", f"A pie TWO THIRDS FORGOTTEN, newspaper with a tiny last-street photo. {STYLE}"),
    ("seppala-leaves", "Seppala left Nome with Togo, 12 years old, expecting Nulato.", f"A sled leaving Nome, tags TOGO 12 YR and NULATO. Cartoon husky. {STYLE}"),
    ("ivanoff-shout", "Ivanoff, tangled with a reindeer, shouted: I have the serum.", f"A tangle of harness, a reindeer silhouette, bubble THE SERUM. Cute not cruel. {STYLE}"),
    ("norton-ice", "Seppala recrossed Norton Sound ice in the dark, wind chill about -85°F.", f"A candy ice sheet NORTON SOUND, -85 WC, Togo leading a straight line. {STYLE}"),
    ("ice-gone", "While they slept, the ice they had crossed blew out to sea.", f"An empty bay OPEN OCEAN, a small WAS ICE tag. {STYLE}"),
    ("mckinley-ridges", "Little McKinley: about 5,000 feet of up and down in 8 miles.", f"A ridgeline 5000 FT / 8 MI. {STYLE}"),
    ("golovin-handoff", "1 Feb 3 p.m., Golovin, to Charlie Olson. 78 miles from Nome.", f"A handoff GOLOVIN 3PM, 78 MI TO NOME. {STYLE}"),
    ("togo-261", "Togo's team: 261 miles, longest by about 200. Arithmetic, not a grudge.", f"A bar chart TOGO 261 vs NEXT, ARITHMETIC. {STYLE}"),
    ("olson-bluff", "Olson: 25 miles to Bluff, sled blown off trail.", f"A sled tipped in candy snow, 25 MI BLUFF. Not gore. {STYLE}"),
    ("welch-halt", "Welch ordered a halt in 80 mph wind so the cylinder would not be lost.", f"A STOP stamp, wind 80 MPH, cylinder safe. {STYLE}"),
    ("buried-cylinder", "A gust buried the cylinder. Kaasen found it with bare hands.", f"A cylinder in a snowbank, bare mittens, FOUND. Not gore. {STYLE}"),
    ("rohn-asleep", "Point Safety 3 a.m.: Ed Rohn asleep. Kaasen did not wake him.", f"A dark roadhouse ASLEEP, a sled passing, ROHN. {STYLE}"),
    ("nome-noon", "Front Street 5:30. Ampules unbroken, thawed by noon.", f"A clock 5:30 then NOON, vials OK thawed. {STYLE}"),
    ("rehook-bronze", "Rehook: red X on skipping the relay for one bronze dog.", f"Ink peeling a SKIP THE RELAY sticker off a statue, mouth closed. {STYLE}"),
    ("rin-tin", "Balto: most famous canine after Rin Tin Tin.", f"Two candy fame cards RIN TIN TIN and BALTO. Cartoon dogs. {STYLE}"),
    ("dec-15-statue", "15 Dec 1925: Roth statue, dedicated to all the dogs, modeled on Balto.", f"A plaque DEDICATED TO ALL THE DOGS, 15 DEC 1925. {STYLE}"),
    ("seppala-togo", "Seppala: I never had a better dog than Togo. Balto never in a winning team.", f"A quote card NEVER A BETTER DOG THAN TOGO. {STYLE}"),
    ("kalland-everyday", "Kalland: just an everyday occurrence as far as we were concerned.", f"A quote card EVERYDAY OCCURRENCE, KALLAND. {STYLE}"),
    ("medals-ink", "Coolidge letters, Mulford gold medals. Native mushers got less ink.", f"A medal pile vs a thin newspaper column LESS INK. {STYLE}"),
    ("second-batch", "1.1 million units left Seattle 31 Jan. First 300,000 was a delay.", f"Two crates 300K NOW vs 1.1M LATER. {STYLE}"),
    ("plane-fail", "A plane was allowed, failed to start, overheated, scrapped.", f"A boxed biplane FAIL, OVERHEAT, SCRAPPED. {STYLE}"),
    ("rohn-second", "Ed Rohn delivered the second batch 15 Feb, about 90 miles.", f"A sled 15 FEB, 90 MI, SECOND BATCH. {STYLE}"),
    ("file-range", "Official deaths 5, 6, or 7. Welch thought more outside town. File the range.", f"A ledger 5-7, FILE THE RANGE. No bodies, no children. {STYLE}"),
    ("not-sickroom", "Not a hymn to one husky, and not a cartoon of a sickroom.", f"Ink putting an X on a SICKROOM door, mouth closed. {STYLE}"),
    ("six-vs-thirty", "A six-day clock on a thirty-day trail.", f"Two clocks 6 DAYS vs 30 DAYS. {STYLE}"),
    ("ice-morning", "Togo's ice was open ocean by morning.", f"Dawn over open water, WAS TRAIL. {STYLE}"),
    ("twenty-names", "Official idea: Nulato. Street idea: Balto. Leftover: twenty names on a mail contract.", f"Three cards NULATO / BALTO / 20 NAMES. {STYLE}"),
    ("who-won-relay", "Not the biplanes. The relay won thawed ampules by noon.", f"A relay baton beating a tiny plane, NOON THAWED. {STYLE}"),
    ("wasilla-case", "Togo later: a glass case in Wasilla. Balto: a statue.", f"A glass case WASILLA vs a statue PARK. {STYLE}"),
    ("how-many-teams", "Ask how many teams, and whether Togo's ice was already ocean.", f"A question mark over 20 TEAMS and OPEN OCEAN. {STYLE}"),
    ("bronze-or-twenty", "Would you have given the bronze to the last lead, or to the twenty.", f"Split: a statue vs twenty tiny sleds, a question mark. {STYLE}"),
    ("receipt", "A relay ran the serum. Drawn anyway.", f"A receipt card RELAY vs STATUE, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Dogs That Ran the Serum",
        description=(
            "Nome, nineteen twenty five. A twenty-pound cylinder, twenty teams, "
            "and a statue that kept the last street."
        ),
        tags=(
            "history",
            "nome",
            "1925",
            "balto",
            "togo",
            "cartoon",
            "true story",
            "logistics",
            "alaska",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="TOGO RAN FARTHER",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Dogs That Ran the Serum",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-nome.json"
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

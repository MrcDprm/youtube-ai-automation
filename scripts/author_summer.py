"""Author Drawn Anyway episode 18: Year Without a Summer, eighteen sixteen."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 600.0
MINUTES = 9
VOICE = "en-US-GuyNeural"
RATE = "+2%"

CHAPTERS = [
    """Snow once fell on a June farm, and July still found frost in the beans. That is not a metaphor, and it is not a cartoon you invented after a trivia night about a volcano ruining a picnic. In eighteen sixteen, New England newspapers and diaries filed the year as Eighteen Hundred and Froze to Death, also Poverty Year, also the Year Without a Summer. On the sixth of June, snow fell in Albany, New York, and in Dennysville, Maine. On the eighth of July, frost was reported from Maine to Virginia. In Franconia, New Hampshire, the cold snap killed the bean crop. Keep that picture. Then put a red X on the cursed-summer joke. The leftover is not that weather has moods. The leftover is that a mountain on the island of Sumbawa, then in the Dutch East Indies, had already cancelled sunlight as a farm input, and Vermont was still planting as if July were a contract.""",
    """Start with why summer was supposed to be ordinary. New England farms ran on a calendar: last frost, plant corn, hope the milk stage of the ear finishes before the first freeze of autumn. Historian William G. Atkins later wrote that the granaries of the great west had not then been opened by railroad, so a town ate what it grew or what a neighbour could spare. Europe was still climbing out of the Napoleonic Wars. Waterloo had been June of eighteen fifteen. The official plan, if anyone had written one on a New Hampshire hillside, was going to work: winter ends, the ground thaws, July is warm, oats and maize and hay come in, livestock make the next winter. A late spring is a nuisance. A June snow is a sentence the calendar does not have a box for. Thomas Robbins, in East Windsor, Connecticut, had already written that vegetation did not seem to advance at all. The Albany Advertiser said it had no recollection of so backward a season. That is a farm waiting for a sun that had already been billed elsewhere.""",
    """File the mountain. Mount Tambora stands on Sumbawa. It had rumbled since eighteen twelve. On the fifth of April eighteen fifteen, giant detonations were heard in Makassar, three hundred eighty kilometres away, in Batavia, now Jakarta, one thousand two hundred sixty kilometres away, and in Ternate, one thousand four hundred kilometres away. Sir Stamford Raffles, then on Java, collected accounts. The noise was almost universally attributed to distant cannon, so much so that a detachment of troops was marched from Djocjocarta in the belief a neighbouring post was being attacked, and boats went looking for a ship in distress. On the tenth of April, about seven in the evening, the climax began. Three plumes rose and merged. The explosion is filed as volcanic explosivity index seven, the most recent confirmed seven on the scale. Estimates of dense-rock equivalent sit around thirty seven to forty five cubic kilometres. The peak had been about four thousand three hundred metres. Afterward it stood about two thousand eight hundred fifty one. The caldera is six to seven kilometres across. Sound was heard at least two thousand six hundred kilometres away, in Sumatra, and perhaps farther. That is not a local hill having a tantrum. That is a mountain rewriting the sky.""",
    """The leftover that travels is not lava. Coarser ash fell in days. Finer particles, and sulfur dioxide turned into a sulfate veil, stayed in the stratosphere for months to years. In the northeastern United States in eighteen fifteen a persistent dry fog reddened and dimmed the sun until sunspots were visible to the naked eye. Wind and rain did not disperse it. Clive Oppenheimer later called that fog a stratospheric sulfate aerosol veil. London saw prolonged orange and red twilights in late June and early July of eighteen fifteen, and again in September and October. Global land temperatures for eighteen sixteen are filed down about four tenths to seven tenths of a degree Celsius, enough to wreck a growing season even when the winter months did not look like a cartoon ice age. The eighteen tens were already a cold decade. There had been other eruptions, including Mayon in eighteen fourteen. There was a Dalton Minimum in solar activity. File those as company, not as a conspiracy. Tambora is still the largest observed eruption in the written record. A veil is a logistics instrument: it bills sunlight to nobody, and then the invoice arrives in a field.""",
    """Here is the New England receipt. On the fifth of June, Danville, Vermont, called the day as warm and sultry as any since September. The next morning Chauncey Jerome walked to work in Plymouth, Connecticut, in a thick wool coat, and put on mittens because his hands were so cold. Benjamin Harwood, a Bennington farmer, wrote that about eight in the morning it began to snow, and that the heads of all the mountains on every side were crowned with snow, the most gloomy and extraordinary weather ever seen. Joshua Whitman in North Turner, Maine, said all travellers needed great coats and mittens, and that the oldest person living knew of no such weather on the eighth of June. Cabot, Vermont, still had snow cover reported around eighteen inches on the eighth. Quebec City saw the country look like the middle of December. Then July: frost on the eighth from Maine to Virginia. August: Edward Holyoke, a Salem physician keeping weather notes, wrote that by the twenty first the fields were as empty and white as October. Corn in the milk froze and never ripened. Atkins said scarcely a quarter was fit for food, and much of it not even for animals. Rapid swings from a hot afternoon toward freezing in hours are in the diaries. That is not a vibe. That is a growing season with the plug pulled.""",
    """Rehook, because the internet likes a cursed year and a painting of a red sky. John D. Post later called eighteen sixteen the last great subsistence crisis in the Western world. Put a red X on turning that into a corpse reel. File the prices. Grain rose sharply across Europe. In north and southwest Ireland, wheat, oats, and potatoes failed. In German-speaking lands people demonstrated in front of grain markets and bakeries. Switzerland's east, densely populated, took the famine harder; in the Val de Bagnes an ice dam grew under the Giétro Glacier in the cold summers of eighteen sixteen and eighteen seventeen, and when it collapsed in June eighteen eighteen it killed forty in the flood, after engineer Ignaz Venetz had tried to drain the lake. That is a leftover glacier doing logistics. In China the monsoon misfired: floods in the Yangtze Valley, frost reports from Fort Shuangcheng, mixed snow in Jiangxi and Anhui. In Yunnan a large-scale famine is on the ledger. In India a delayed monsoon and late rains sit in the same year as a cholera strain moving from Bengal. Alexander of Russia could still donate grain westward. Harvests were not wrecked everywhere. Scandinavia and parts of eastern Europe were closer to normal. A veil is not a uniform.""",
    """The leftover that is not weather is a moving van. Crop failure in New England pushed families west when the local crib was empty and the railroad had not yet made Illinois a neighbour. Thomas Jefferson, retired at Monticello, took crop losses that deepened his debts. Sarah Snell Bryant of Cummington, Massachusetts, wrote weather backward. At the Shaker community near New Lebanon, New York, Nicholas Bennet wrote in May that all was froze and the hills barren like winter; they replanted in June; by July seventh the cold had stopped growth. In June eighteen sixteen, Mary Shelley, Percy Bysshe Shelley, Lord Byron, and John William Polidori were stuck indoors at Villa Diodati on Lake Geneva by incessant rain in a wet, ungenial summer. Byron proposed a ghost-story contest. Shelley wrote Frankenstein. Byron's Darkness remembers a day when fowls went to roost at noon and candles had to be lit as at midnight. File the book as indoor rain, not as the cause. J. M. W. Turner painted the yellow and red skies of the veil. The Old Farmer's Almanac story that Robert B. Thomas accidentally printed rain, hail, and snow for July, and then it happened, is a legend the Almanac itself files as apocryphal. Keep the legend in a drawer. Keep the sulfate.""",
    """None of this is a hymn to a cursed planet, and none of it is a cartoon of farmers as fools who should have known better than to plant corn in June. They had a calendar that had worked. They had no telegraph from Sumbawa. They had a dry fog that would not blow away, and a June that put mittens on a clockmaker walking to work. You are allowed to laugh at a summer that needed a fireplace. You are not required to laugh at a bean field in Franconia, or at a crib of moldy corn, or at a number on Sumbawa that historians still argue: Zollinger about ten thousand direct, Tanguy about eleven thousand plus forty nine thousand from hunger and disease on the nearby islands, Oppenheimer at least seventy one thousand, Reid toward a hundred thousand. File the range. Do not spend it as a punchline, and do not draw it. Direct volcanic effects are one ledger. A cancelled July is another. A news flash from a mountain is a costume the sky wore for two years. Four tenths of a degree is a receipt. Eighteen inches of June snow in Cabot is a receipt.""",
    """So who won. Not July. Not the corn in the milk. Not the official idea that winter ends because the almanac says so. The veil won a growing season. Tambora won a caldera. Raffles won a stack of letters that thought the mountain was cannon. Chauncey Jerome won a sentence about mittens in June. Mary Shelley won a novel because the rain would not stop. Venetz won a failed drain and a flood two years later. New England won a westward rumor: if the sun will not arrive, the farm might have to. If you need a moral, skip never live in Vermont. Take this: sunlight is a terrible thing to assume, and a stratospheric invoice is a terrible neighbour for a ninety-day growing season. The next time someone tells you eighteen sixteen had no summer, ask whether they mean the snow in Albany or the mountain on Sumbawa, and whether the corn froze in the milk. Would you have replanted after the June snow, or sold the hillside and gone west. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no famine gore, no starving children, no pyroclastic death, no blood, "
    "not mud-green archive night, not After Hours File dark. Year shown as a candy snow-on-farm, a July frost, "
    "a volcano as a mountain prop, a sun with a veil, a calendar, a price tag on grain, not violence and not bodies. "
    "Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("june-snow", "Snow on a June farm. Frost still in July beans.", f"Cartoon title beat: a farm in candy snow under a JUNE banner, a tiny July calendar with frost, cream paper, hook energy. No people suffering. {STYLE}"),
    ("not-trivia", "Not a volcano-ruined-picnic trivia gag.", f"Ink shaking his head at a TRIVIA VOLCANO stamp with a red X, mouth closed. {STYLE}"),
    ("froze-to-death", "Filed as Eighteen Hundred and Froze to Death. Poverty Year.", f"Two newspaper nameplates 1800 AND FROZE TO DEATH and POVERTY YEAR. {STYLE}"),
    ("albany-june6", "6 June 1816: snow in Albany, New York, and Dennysville, Maine.", f"A simple map ALBANY and DENNYSVILLE, snowflakes, date 6 JUN 1816, no flags. {STYLE}"),
    ("july8-frost", "8 July: frost reported from Maine to Virginia.", f"A map strip MAINE to VIRGINIA, FROST 8 JUL, no flags. {STYLE}"),
    ("franconia-beans", "Franconia, New Hampshire: the cold snap killed the beans.", f"A field sign FRANCONIA BEANS with a frost X, no people starving. {STYLE}"),
    ("x-on-curse", "Put a red X on the cursed-summer joke.", f"A CURSED SUMMER stamp with a giant red X. {STYLE}"),
    ("sumbawa", "The leftover: a mountain on Sumbawa had cancelled sunlight.", f"A candy mountain labeled TAMBORA SUMBAWA, a tiny sun with a dimmer switch. {STYLE}"),
    ("calendar-plan", "New England plan: last frost, plant corn, harvest before autumn freeze.", f"A farm calendar LAST FROST then CORN then HARVEST. {STYLE}"),
    ("no-railroad", "Atkins: the western granaries were not yet a railroad neighbour.", f"An empty tracks sign NO RAILROAD YET, a local crib of corn. {STYLE}"),
    ("waterloo-1815", "Europe still climbing out of the Napoleonic Wars. Waterloo: June 1815.", f"A calendar JUN 1815 WATERLOO beside a farm 1816, no battle gore, no flags as joke. {STYLE}"),
    ("official-plan", "Official plan: winter ends, July is warm, hay comes in.", f"A clipboard PLAN: WINTER ENDS, JULY WARM, HAY. {STYLE}"),
    ("robbins", "Thomas Robbins, East Windsor: vegetation does not advance at all.", f"A nameplate THOMAS ROBBINS EAST WINDSOR, a stalled sprout. No portrait. {STYLE}"),
    ("albany-advertiser", "Albany Advertiser: no recollection of so backward a season.", f"A newspaper clip ALBANY ADVERTISER BACKWARD SEASON. {STYLE}"),
    ("tambora-1812", "Tambora on Sumbawa had rumbled since 1812.", f"A mountain with a small RUMBLE 1812 tag. {STYLE}"),
    ("april5-cannon", "5 April 1815: detonations heard hundreds of kilometres away.", f"A date 5 APR 1815, sound rings to MAKASSAR BATAVIA TERNATE. {STYLE}"),
    ("raffles-troops", "Raffles: noise taken for cannon. Troops marched from Djocjocarta.", f"A nameplate RAFFLES, a CANNON stamp, tiny marching boots as icons not an army gore. {STYLE}"),
    ("april10-7pm", "10 April, about 7 pm: three plumes rose and merged.", f"A clock 7:00, three candy plumes merging, not a disaster-porn blast. {STYLE}"),
    ("vei-seven", "Filed VEI 7. Most recent confirmed seven.", f"A scale badge VEI 7, MOST RECENT CONFIRMED. {STYLE}"),
    ("thirty-seven", "Dense-rock equivalent about 37 to 45 cubic kilometres.", f"A volume block 37-45 KM3. {STYLE}"),
    ("peak-cut", "Peak from about 4,300 m down to about 2,851 m.", f"A mountain diagram 4300 m sliced to 2851 m. {STYLE}"),
    ("caldera", "Caldera 6 to 7 kilometres across.", f"A bowl diagram CALDERA 6-7 KM. {STYLE}"),
    ("heard-2600", "Heard at least 2,600 km away.", f"A distance ruler 2600 KM SOUND. {STYLE}"),
    ("dry-fog", "Northeastern US, 1815: a dry fog wind could not blow away.", f"A red-cream DRY FOG over a tiny sun, SUNSPOTS visible as dots. {STYLE}"),
    ("oppenheimer-veil", "Oppenheimer: a stratospheric sulfate aerosol veil.", f"A nameplate OPPENHEIMER, a veil over a candy Earth, no globe-as-flag. {STYLE}"),
    ("london-twilight", "London, 1815: orange-red twilights in June-July and autumn.", f"A London skyline silhouette, orange-pink twilight, year 1815, cream paper not dark archive. {STYLE}"),
    ("four-tenths", "1816: global land about 0.4 to 0.7 C down.", f"A thermometer 0.4-0.7 C, year 1816. {STYLE}"),
    ("company-not-plot", "Mayon 1814, Dalton Minimum: company, not a conspiracy.", f"Two side tags MAYON 1814 and DALTON MINIMUM, NOT A PLOT stamp. {STYLE}"),
    ("danville-sultry", "5 June, Danville VT: as warm as any day since September.", f"A thermometer high, DANVILLE 5 JUN, then a cold arrow. {STYLE}"),
    ("jerome-mittens", "6 June: Chauncey Jerome, Plymouth CT, coat and mittens to work.", f"A nameplate CHAUNCEY JEROME, a pair of mittens, JUNE. No portrait. {STYLE}"),
    ("harwood-snow", "Harwood, Bennington: snow at 8 am, mountains crowned white.", f"Candy mountains with snow caps, BENNINGTON, clock 8 AM. {STYLE}"),
    ("cabot-18", "Cabot, Vermont: snow cover still about 18 inches on the 8th.", f"A ruler 18 IN on a snowy hillside CABOT VT. {STYLE}"),
    ("quebec-december", "Quebec City: the country looked like mid-December.", f"A Quebec street in candy June snow, MID-DECEMBER stamp. {STYLE}"),
    ("holyoke-october", "21 August: Holyoke, fields as empty and white as October.", f"A field EMPTY AS OCTOBER, date 21 AUG, nameplate HOLYOKE. {STYLE}"),
    ("corn-in-milk", "Corn in the milk froze and never ripened. Scarcely a quarter fit for food.", f"An ear of corn tagged IN THE MILK with a frost X, 1/4 USABLE. No starving people. {STYLE}"),
    ("rehook-curse", "Rehook: the internet likes a cursed year and a red sky.", f"Ink peeling a CURSED YEAR sticker off a calendar, mouth closed. {STYLE}"),
    ("post-crisis", "John D. Post: last great subsistence crisis in the Western world.", f"A book card JOHN D. POST, LAST GREAT SUBSISTENCE CRISIS. {STYLE}"),
    ("x-on-reel", "Red X on turning that into a corpse reel.", f"A CORPSE REEL stamp with a giant red X. No bodies. {STYLE}"),
    ("grain-prices", "Grain prices rose sharply across Europe.", f"A price tag GRAIN UP on a sack, a bakery window, no riots gore. {STYLE}"),
    ("ireland-three", "Ireland: wheat, oats, and potatoes failed in the north and southwest.", f"Three crop cards WHEAT OATS POTATO with frost marks, IRELAND, no famine bodies. {STYLE}"),
    ("swiss-ice-dam", "Val de Bagnes: Giétro ice dam, Venetz, collapse June 1818.", f"A cartoon ice dam GIETRO, nameplate VENETZ, date JUN 1818. No drowning gore. {STYLE}"),
    ("yangtze", "China: monsoon misfire, Yangtze floods, Yunnan on the famine ledger.", f"A simple map YANGTZE FLOOD and YUNNAN tag, no flags, no bodies. {STYLE}"),
    ("westward", "New England leftover: a moving van when the local crib was empty.", f"A cartoon wagon WEST with a tiny empty crib, no suffering faces. {STYLE}"),
    ("jefferson-debt", "Jefferson at Monticello: crop losses deepened his debts.", f"A nameplate JEFFERSON MONTICELLO, a DEBT tag on a crop ledger. No portrait. {STYLE}"),
    ("shakers-froze", "New Lebanon Shakers: all was froze, replanted, then July stopped growth.", f"A field sign SHAKERS NEW LEBANON, FROZE then REPLANT then STOP. {STYLE}"),
    ("diodati-rain", "Villa Diodati, June 1816: rain kept them indoors. Ghost-story contest.", f"A lakeside villa DIODATI, rain, a card GHOST STORY CONTEST. {STYLE}"),
    ("frankenstein-indoor", "Shelley wrote Frankenstein. File the book as indoor rain, not the cause.", f"A book FRANKENSTEIN, tag INDOOR RAIN, NOT THE CAUSE. No monster gore. {STYLE}"),
    ("almanac-legend", "Farmer's Almanac July snow prediction: legend, apocryphal. Keep the sulfate.", f"An almanac JULY SNOW with a LEGEND stamp and a red X, a bottle SULFATE winning. {STYLE}"),
    ("not-fools", "Not a cartoon of farmers as fools who should have known.", f"Ink peeling a FOOLS sticker off a FARMERS sign, mouth closed. {STYLE}"),
    ("no-telegraph", "They had no telegraph from Sumbawa.", f"A broken wire NO TELEGRAPH, Sumbawa on one end, a farm on the other. {STYLE}"),
    ("file-the-range", "Sumbawa death toll is a range. File it. Do not spend it as a joke.", f"A ledger RANGE with question marks, a red X on JOKE. No corpses. {STYLE}"),
    ("four-tenths-receipt", "Four tenths of a degree is a receipt. Eighteen inches of June snow is a receipt.", f"Two receipts 0.4 C and 18 IN JUNE SNOW. {STYLE}"),
    ("replant-or-west", "Would you have replanted after the June snow, or gone west.", f"Split: a seed bag REPLANT vs a wagon WEST, a question mark. {STYLE}"),
    ("receipt", "Sunlight is a terrible thing to assume. Drawn anyway.", f"A receipt card SUNLIGHT vs VEIL, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Year Summer Forgot to Arrive",
        description=(
            "Eighteen sixteen. June snow in Albany, frost in July, "
            "and a mountain on Sumbawa that billed the sunlight."
        ),
        tags=(
            "history",
            "year without a summer",
            "1816",
            "tambora",
            "cartoon",
            "true story",
            "new england",
            "volcano",
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
        thumbnail_hook="FROST IN JULY",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Year Summer Forgot to Arrive",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-summer.json"
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

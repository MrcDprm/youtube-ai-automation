"""Author Drawn Anyway episode 13: War of the Bucket, Modena and Bologna, thirteen twenty five."""

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
    """A wooden bucket once outlived a war it did not start. That is not a metaphor, and it is not a cartoon you invented after a trivia night. In thirteen twenty five, in Emilia, northern Italy, the city of Bologna and the city of Modena went to war. The internet caption is that Modena stole a bucket from a Bolognese well and Bologna raised thirty two thousand men to get it back. Keep that picture, then put a red X on the cause line. The named fight is the Battle of Zappolino, the fifteenth of November thirteen twenty five, in Bolognese country, now a hamlet of Castello di Serravalle. Passerino Bonacolsi of Mantua led Modena. Bologna's captain in the field is filed as Malatesta of Rimini after the siege of Monteveglio. About two thousand men were killed on both sides. That is not a giggle, and it is not a number you get to spend as a punchline. The bucket, if you take the later souvenir story, came from a well outside Porta San Felice after the routing, on the way home, when nobody was staying to knock the gate down. Everything after this is just that picture hiring a poem three hundred years late to write the title the internet still recites.""",
    """Start with why two cities already had a border that bit. For more than a century northern Italy had been arguing who licensed a government: the pope's party, called Guelphs, and the emperor's party, called Ghibellines. Bologna sat Guelph. Modena sat Ghibelline. File those names as factions, not as flags you salute and not as two sports shirts. In twelve ninety six Bologna took Bazzano and Savigno from Modena. Pope Boniface the Eighth confirmed the title. Azzo the Eighth d'Este ran Modena from twelve ninety three to thirteen oh eight and picked fights partly to look useful at home among nobles who were not warm. His successor in the city was Passerino Bonacolsi, a Mantuan, agent of Louis of Bavaria, King of the Romans, with Parma and Reggio also in his pocket. Pope John the Twenty Second declared him a rebel against the Church and offered indulgences, crusader-style, to anyone who could harm his person or his goods, as if harming a neighbour were a voyage to recover a tomb. That is a border with a sermon attached. It is not a pail, and it was not waiting for a well.""",
    """The months before November are raids, not a well. In July the Bolognese went into Modenese land between the canals and burned fields. In August a crowd headed by Bologna's podesta spent two weeks ravaging other Modenese ground. In September Mantua took a turn. At the end of that month the strategic Bolognese fortress of Monteveglio was betrayed to Modena by malcontents inside. Two renegade castellans were executed. Do not draw that. File it as why Bologna had to answer, not as a spectacle. Monteveglio is a castle on the approach, a lock on the road, not a bucket on a rope. War, in the sense of a mustered army marching, is what you do when a neighbour holds your lock. The trivia card prefers a pail because a pail photographs and fits in a glass case. A betrayed rocca does not go viral unless you already know which hill sits between the two cities. The official idea in Bologna was not retrieve the oak. It was get the fortress back before the map changed for good.""",
    """November. Bologna mustered on the order of thirty thousand foot and a couple of thousand horse, with help talked of from Florence and Romagna, and went to sit on Monteveglio. Modena's column is filed around two thousand horse and five thousand foot, with professional Germans in the mix, Azzone Visconti of Milan, Rinaldo of Ferrara, Cangrande della Scala arriving and then leaving for Verona. Numbers in chronicles are a sport. Treat thirty two thousand versus seven thousand as the usual poster, not a census you can audit. On the fifteenth, around sunset, at Zappolino, Bonacolsi hit while the Bolognese were still sorting a feigned river crossing from the night before toward Marano sul Panaro. Griffoni dates the fight the next day if you start the calendar at sunset. Within a couple of hours the larger army broke and ran for the walls of Bologna. About two thousand dead is the number that keeps being written. Matteo Griffoni, a Bolognese chronicler, is the named witness for the fight. He does not mention a bucket. That absence is the leftover before the leftover. If a stolen well had started the march, a Bolognese memorialist had a reason to complain about the oak. He complained about the hill instead.""",
    """Here is the leftover fact, and it is not that oak wins wars. The Modenese did not siege Bologna. They wrecked outlying castles, Crespellano, Zola, Samoggia, Anzola, Castelfranco, Piumazzo, and the Reno lock near Casalecchio, which is a sentence about water as a weapon, not a gore reel you are owed. Then they ran a palio outside the gates, a prize race, to the eternal memory of the expedition and the eternal shame of Bologna, the Latin is in the Modenese chronicle William Heywood quotes in his book on central Italian sports. Then they went home. Some accounts say they lifted a wooden bucket from a well just outside Porta San Felice and carried it as a trophy. Twenty six captured notables sat in Modena for eleven weeks. In January, peace talks put Monteveglio and the other castles back to Bologna, a return toward the old map, probably paid as ransom into Bonacolsi's hands. The lock went home. The pail, if it came, stayed. That is the only logistics that still hangs on a wall. A ransom can move a fortress. A glass case cannot move a cause.""",
    """Rehook, because the internet likes a war fought over a bucket and a death count it can treat as a joke. Alessandro Tassoni of Modena wrote La secchia rapita, the stolen bucket, a mock-heroic poem, drafted about sixteen fourteen to sixteen fifteen, published in Paris in sixteen twenty two. Twelve cantos. He called the mix eroicomico, heroic-comic. In an introduction under a pen name he said some figures were idealised, not roll calls, which is a poet admitting the cast is not a muster list. That book is how a trophy story became the title of the war. Antonio Salieri later made an opera of the same name in seventeen seventy two. Encyclopaedia Britannica in nineteen eleven still had the bucket in the basement of the Ghirlandina, Modena's cathedral tower. Today the usual filing is: the old oak in the Palazzo Comunale, the town hall, behind glass, and a replica in the tower where it had hung for centuries. Se non e vero, e ben trovato, even if it is not true it makes a good story. File that as an Italian warning label, not a licence to skip Monteveglio. A good story is a neighbour of a true one. It is not the same address, and it does not get to collect the rent on two thousand dead.""",
    """There is a version where two Modenese sneak into the citadel of San Felice, steal the town's favourite pail, Bologna demands it back, Modena refuses, and thirty two thousand men die for oak. That is Tassoni's joke doing later work as a caption on a well. A well bucket is a plausible souvenir after you have already stood at the gate and declined to siege. It is a terrible casus belli for a border that had been on fire since July, with a fortress lost in September. Guelph and Ghibelline were not two sports teams. They were who you called when your neighbour took a castle, and who called you a rebel when the pope needed a sermon. You are allowed to laugh at a pail in a glass case. You are not required to laugh at two thousand dead, or to pretend a seventeenth-century poem is a fourteenth-century declaration of war, or to hang the declaration on a rope. The sneak-thief version is a later caption looking for a well that could carry a war it did not fund.""",
    """None of this is a hymn to Modena, and none of it is a cartoon of Bologna as fools who would die for a well. They had a fortress betrayed in September. They had a pope offering indulgences against Bonacolsi. They had a larger militia and a smaller professional opposite. They lost in a couple of hours on a hill at Zappolino. The chemistry is numbers plus a feint plus a flank. The logistics is what you carry home when you will not stay for a siege. A palio is a race you stage as a receipt. A bucket is a receipt you can still hang when the castles have gone home in January. Griffoni wrote the battle and skipped the pail. Tassoni wrote the pail and made it the war. The object in the town hall is real oak. The cause line on the trivia card is the part that waited three hundred years for a poet who already knew how to mix a joke with an epic and still sell both. You can keep the oak. You cannot keep the caption if the chronicle is empty where the well should be.""",
    """So who won. Not the well. Not the caption. Bonacolsi won a winter of hostages and a ransom map that put the castles back. Bologna won the lock again in January and, at home, a coat of arms pairing John the Twenty Second with Robert of Anjou on the wall, which is a sentence about an old alliance still claiming to be alive. Tassoni won the title the internet still uses. The Ghirlandina won a replica. The Palazzo Comunale won the glass case. If you need a moral, skip never steal a bucket. Take this: a trophy is a terrible instrument for a casus belli, and a casus belli is a terrible neighbour for a well. The next time someone tells you the war of the bucket, ask whether the pail walked out before Zappolino or after Porta San Felice, and whose chronicle skipped it. Would you have hung it in the tower, or would you have put Monteveglio back on the card. A betrayed castle, two hours, a palio, a pail that waited. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no beheadings, no battle-porn, no blood. "
    "War shown as maps, closed castles, a wooden bucket trophy, a poem book, not violence. "
    "Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("bucket-waited", "A wooden bucket outlived a war it did not start.", f"Cartoon title beat: a huge oak bucket on a pedestal, a tiny battlefield map behind it with a red X on CAUSE. Cream paper. No gore. {STYLE}"),
    ("not-trivia", "Not a metaphor. Not a trivia gag.", f"Ink shaking his head at a TRIVIA WAR stamp with a red X, mouth closed. {STYLE}"),
    ("emilia-1325", "1325, Emilia, northern Italy. Bologna and Modena.", f"A simple map BOLOGNA and MODENA, year 1325, no flags. {STYLE}"),
    ("internet-caption", "Internet caption: they stole a bucket, 32,000 men marched.", f"A clickbait card STOLEN BUCKET 32000, question mark. {STYLE}"),
    ("x-on-cause", "Put a red X on the cause line.", f"A cause line BUCKET with a giant red X. {STYLE}"),
    ("zappolino", "Battle of Zappolino, 15 November 1325.", f"Calendar 15 NOV 1325, a hill labeled ZAPPOLINO. {STYLE}"),
    ("serravalle", "Now a hamlet of Castello di Serravalle.", f"A small village sign CASTELLO DI SERRAVALLE. {STYLE}"),
    ("bonacolsi", "Passerino Bonacolsi of Mantua led Modena.", f"A nameplate PASSERINO BONACOLSI, Mantua tag, no portrait. {STYLE}"),
    ("malatesta", "Malatesta of Rimini filed as Bologna's field captain.", f"A nameplate MALATESTA RIMINI, no portrait. {STYLE}"),
    ("two-thousand", "About 2,000 killed on both sides. Not a giggle.", f"A somber tally 2000, respectful, no bodies. {STYLE}"),
    ("porta-san-felice", "Bucket story: a well outside Porta San Felice, after.", f"A city gate PORTA SAN FELICE, a well, a bucket, AFTER stamp. {STYLE}"),
    ("poem-late", "A poem three hundred years late hired the title.", f"A book 1622 next to a clock 300 YR LATE. {STYLE}"),
    ("guelph-ghibelline", "Guelphs with the pope, Ghibellines with the emperor.", f"Two desks PAPA and EMPEROR, no flags as identity. {STYLE}"),
    ("bologna-modena-sides", "Bologna Guelph. Modena Ghibelline. Factions, not flags.", f"Two city nameplates, two faction tags, no banners as identity. {STYLE}"),
    ("bazzano-1296", "1296: Bologna took Bazzano and Savigno. Boniface VIII confirmed.", f"A 1296 deed BAZZANO SAVIGNO, papal seal cartoon not a flag. {STYLE}"),
    ("azzo-este", "Azzo VIII d'Este ran Modena 1293-1308.", f"A job plaque AZZO VIII 1293-1308, no portrait. {STYLE}"),
    ("passerino-pocket", "Bonacolsi: Mantua, Parma, Reggio, Louis of Bavaria's agent.", f"Three city keys MANTUA PARMA REGGIO on a ring. {STYLE}"),
    ("john-xxii", "Pope John XXII: rebel against the Church. Indulgences offered.", f"A 1325 paper INDULGENCE vs BONACOLSI, no gore. {STYLE}"),
    ("not-a-pail", "A border with a sermon. Not a pail.", f"A border ditch vs a tiny bucket with a red X on CAUSE. {STYLE}"),
    ("july-fields", "July: Bolognese burned fields between the canals.", f"Empty fields and canals, a fire icon small not disaster-porn. {STYLE}"),
    ("august-podesta", "August: two weeks of raids, headed by Bologna's podesta.", f"A calendar AUGUST, two weeks shaded, no violence closeup. {STYLE}"),
    ("september-mantua", "September: Mantua took a turn.", f"A calendar SEP, MANTUA arrow. {STYLE}"),
    ("monteveglio", "End of September: Monteveglio betrayed to Modena.", f"A hill fortress MONTEVEGLIO, BETRAYED stamp, no gore. {STYLE}"),
    ("castle-not-bucket", "A castle on the approach, not a bucket on a rope.", f"A castle vs a well-bucket, arrow pointing at the castle. {STYLE}"),
    ("pail-photographs", "A pail photographs. A betrayed rocca does not go viral.", f"A camera flashing at a bucket, ignoring a castle. {STYLE}"),
    ("thirty-thousand-foot", "Bologna: on the order of 30,000 foot, a couple thousand horse.", f"A poster 30000 FOOT, not a gore army. Tiny dots. {STYLE}"),
    ("modena-column", "Modena: about 2,000 horse and 5,000 foot. Usual poster 32k vs 7k.", f"Two posters 32K vs 7K labeled USUAL POSTER. {STYLE}"),
    ("feint-marano", "Feigned river crossing toward Marano sul Panaro the night before.", f"A river, a fake arrow NORTH, a real path SOUTH to MARANO. {STYLE}"),
    ("couple-of-hours", "Within a couple of hours the larger army broke.", f"A clock TWO HOURS, a ROUT stamp, no bodies. {STYLE}"),
    ("griffoni", "Matteo Griffoni named the fight. He does not mention a bucket.", f"A chronicle page BATTLE yes, BUCKET blank. {STYLE}"),
    ("no-siege", "Modena did not siege Bologna.", f"City walls, a NO SIEGE stamp, army turning away. {STYLE}"),
    ("reno-lock", "They broke the Reno lock near Casalecchio. Water as a weapon.", f"A canal lock broken, water arrow, not drowning gore. {STYLE}"),
    ("palio-gates", "A palio outside the gates: a prize race as a receipt.", f"A comic horse race PALIO outside a city gate, not cruelty. {STYLE}"),
    ("latin-shame", "Latin: eternal memory of the expedition, eternal shame of Bologna.", f"A Latin scroll SHAME OF BOLOGNA, comic not cruel. {STYLE}"),
    ("twenty-six", "26 captured notables, 11 weeks in Modena.", f"A tally 26 HOSTAGES, clock 11 WEEKS. No cages closeup. {STYLE}"),
    ("january-peace", "January: Monteveglio and castles back to Bologna. Ransom map.", f"A January calendar, CASTLES RETURNED, a coin RANSOM. {STYLE}"),
    ("lock-home-pail-stayed", "The lock went home. The pail, if it came, stayed.", f"A castle walking home, a bucket staying on a shelf. {STYLE}"),
    ("tassoni", "Tassoni: La secchia rapita, about 1614-15, Paris 1622.", f"A mock-epic book LA SECCHIA RAPITA, dates 1614 and 1622. {STYLE}"),
    ("eroicomico", "He called it eroicomico. Some figures idealised, not roll calls.", f"A stamp HEROIC-COMIC, a NOT A ROLL CALL tag. {STYLE}"),
    ("salieri", "Salieri's opera, 1772, same title.", f"A tiny opera house 1772, same bucket on the poster. {STYLE}"),
    ("ghirlandina-1911", "Britannica 1911: bucket in the Ghirlandina basement.", f"A tower GHIRLANDINA, a basement bucket, 1911. {STYLE}"),
    ("town-hall-glass", "Today: old oak in Palazzo Comunale, replica in the tower.", f"A glass case PALAZZO COMUNALE and a tower replica. {STYLE}"),
    ("ben-trovato", "Se non e vero, e ben trovato. A warning label, not a licence.", f"An Italian proverb card, a WARNING not LICENCE stamp. {STYLE}"),
    ("sneak-version", "The sneak-thief version: San Felice citadel, demand, refuse, war.", f"A comic sneak with a bucket, a DEMAND stamp, labeled LATER CAPTION. {STYLE}"),
    ("plausible-souvenir", "A well bucket is a plausible souvenir after you already stood at the gate.", f"A gate, a well, a SOUVENIR tag, AFTER the fight. {STYLE}"),
    ("terrible-casus", "A terrible casus belli for a border on fire since July.", f"A July-to-November calendar on fire at the edges, a tiny bucket too small to be the cause. {STYLE}"),
    ("not-sports", "Guelph and Ghibelline were not two sports teams.", f"Ink peeling a SPORTS TEAM sticker off two city names, mouth closed. {STYLE}"),
    ("not-fools", "Not a cartoon of Bologna as fools who would die for a well.", f"Ink peeling a FOOLS sticker off a well, mouth closed. {STYLE}"),
    ("trophy-vs-casus", "A trophy is a terrible instrument for a casus belli.", f"A trophy cup labeled CAUSE with a crack. {STYLE}"),
    ("who-won", "Not the well. Not the caption. Tassoni won the title.", f"A well vs a caption card vs TASSONI's book winning TITLE. {STYLE}"),
    ("january-lock", "Bologna won the lock again in January.", f"MONTEVEGLIO key returning in JANUARY. {STYLE}"),
    ("glass-case", "The town hall won the glass case. The tower won a replica.", f"Split: glass case ORIGINAL, tower REPLICA. {STYLE}"),
    ("before-or-after", "Ask: pail before Zappolino, or after Porta San Felice.", f"Two clocks BEFORE and AFTER, a bucket on AFTER. {STYLE}"),
    ("comment-hook", "Would you have hung it in the tower. Tell me in the comments.", f"Ink pointing at the viewer, mouth closed, a tiny bucket in a tiny tower. {STYLE}"),
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
        title="The War Fought Over a Wooden Bucket",
        description=(
            "Modena and Bologna, thirteen twenty five. Monteveglio, Zappolino, "
            "and a pail that waited until after the gate."
        ),
        tags=(
            "history",
            "war of the bucket",
            "modena",
            "bologna",
            "cartoon",
            "true story",
            "1325",
            "zappolino",
            "funny",
            "italy",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="THE BUCKET WAITED",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The War Fought Over a Wooden Bucket",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-bucket.json"
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

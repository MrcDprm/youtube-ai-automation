"""Author Drawn Anyway episode 1: Emu War, Campion, nineteen thirty two."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")

CHAPTERS = [
    """Australia once sent the army to fight birds. That is not a metaphor and it is not a meme that started on the internet. In November nineteen thirty two, in the Campion district of Western Australia's wheatbelt, farmers watched emus walk through fences like the fences were a suggestion. About twenty thousand of the birds had moved in after breeding season, eating wheat and opening holes for rabbits. The farmers, many of them World War One veterans on dry government land, asked Defence Minister Sir George Pearce for machine guns. Pearce said yes. The force that arrived was not a division. It was Major Gwynydd Purves Wynne-Aubrey Meredith, Sergeant S. McMurray, and Gunner J. O'Halloran. Two Lewis guns. Ten thousand rounds. A Fox Movietone camera, because of course there was a camera. The official idea was a cull. The unofficial idea was target practice that would also look like help. The emus did not attend the briefing. Keep that picture. Three men. A paddock. A species that treats a straight line as an insult. Everything after this is just that picture getting more expensive.""",
    """Start with why anyone thought this was a job for artillery. After the war, discharged veterans were handed farms in marginal country around Chandler and Walgoolan. The Depression dropped wheat prices. Promised subsidies did not show up. Then the emus migrated toward the coast and found cleared paddocks and stock water laid out like a buffet. They spoiled crops and wrecked fences. A deputation of ex-soldiers told Pearce they already knew what a Lewis gun could do. Western Australia would pay to move the men. Farmers would house them and pay for ammunition. Soldiers would pull the triggers. Pearce liked that the birds would make good practice. He later got nicknamed Minister of the Emu War in the Senate, which is the kind of promotion nobody puts on a CV. Rain delayed the start. The emus scattered on wet ground. On the second of November the rain eased and the three-man war clocked in. If this already sounds like a bad idea written in triplicate, you are paying attention. The wheat was real. The guns were real. The plan assumed the birds would stand still. Plans that assume a wild animal will stand still should be stored with the other fiction.""",
    """On day one they saw about fifty emus near Campion, out of range. Settlers tried to herd them into an ambush, the way you herd sheep if sheep could do forty miles an hour and then fragment. The flock split into little groups and ran. The first burst did almost nothing because range is a real number. A later burst killed a number of birds. That afternoon, maybe a dozen more. If you came for a neat turkey-shoot, you already lost the plot. Emus do not line up. They are tall, fast, and they change direction like the ground insulted them. Meredith was from the Seventh Heavy Artillery. His equipment was built for a different argument. The argument here was: a wheatbelt full of birds that refuse to be a parade. A Lewis gun is happy when the target is a line. An emu is happy when the target is anywhere else. That mismatch is the whole war in one sentence, and it is about to repeat until December.""",
    """On the fourth of November he waited at a dam. More than a thousand emus came in. The gunners held fire until the birds were close. Then a Lewis gun jammed after twelve. The rest of the thousand did what a thousand unimpressed dinosaurs-with-feathers do: they left. Observers said each pack had a lookout, a big dark-plumed bird standing about six feet, warning the others. Meredith bolted a gun onto a truck. The truck could not catch them. The ride was so rough the gunner could not fire. By the eighth of November they had burned through about twenty five hundred rounds. How many birds? One account says fifty. Settlers said up to five hundred. That gap is the joke and the paperwork. Meredith reported no human casualties except dignity. Parliament started asking questions. Negative headlines said only a few emus had died. Pearce withdrew the men and the guns the same day. Six days, two guns, and a withdrawal. That is not a secret plot. That is a jam, a truck, and a flock that would not pose. If you have ever tried to photograph a toddler, you already understand the tactics. The toddler is faster. The toddler does not care about your schedule.""",
    """The emus did not withdraw. Heat and drought kept pushing them into paddocks. Premier James Mitchell wanted the army back. A base commander’s note claimed three hundred kills in the first pass, which is a rounder story than the messy week. On the twelfth of November Pearce approved a restart. The plan was to lend the guns to the state if the state found gunners. The state still did not have the gunners, so Meredith went back out on the thirteenth. First two days: about forty birds. The fifteenth was a dud. By the second of December they were claiming about a hundred emus a week, which sounds like progress until you remember the original complaint was twenty thousand visitors. On the tenth of December Meredith was recalled. The second attempt had lasted long enough to generate a report with suspiciously tidy arithmetic. If you are keeping score at home, this is the part where a second try is supposed to fix the first. It mostly produced better stationery.""",
    """Here is the report you are not supposed to swallow whole. Meredith claimed nine hundred eighty six confirmed kills and nine thousand eight hundred sixty rounds, which is exactly ten rounds per confirmed bird. Historians side-eye that kind of neatness. He also claimed about twenty five hundred more died of wounds, a number nobody could audit in a wheat field. Ornithologist Dominic Serventy later wrote that the machine-gunners’ dream of point-blank fire into serried masses dissolved, because the emu command had ordered guerrilla tactics. Meredith said the birds could face machine guns with the invulnerability of tanks. Believe the tank line as a frustrated soldier’s metaphor. Do not turn it into a superhero origin. The Coolgardie Miner later insisted the guns saved the wheat. Other officials could not bear to be reminded. Both can sit in the same cartoon: a method that looked serious, and a result that looked like a punchline. A file can hold a tidy ratio and a messy paddock at the same time. You are allowed to laugh at the ratio. You are not required to pretend the paddock was imaginary.""",
    """Aftermath is where the spreadsheet beats the newsreel. Farmers asked for soldiers again in nineteen thirty four, nineteen forty three, and nineteen forty eight. The government said no. The bounty system that had existed since nineteen twenty three kept running. In nineteen thirty four, fifty seven thousand thirty four bounties were claimed in six months. That is an ugly number and also a number that moved. Exclusion fences did more quiet work than two Lewis guns on a truck. Conservationists in Britain protested an “extermination of the rare emu,” which would have surprised anyone who had just lost a paddock. In nineteen fifty, a parliamentarian still wanted army .303 ammunition released to farmers. Five hundred thousand rounds got approved. The military cameo of thirty two was already a story people told to make a room laugh. The birds were still the birds. The policy had quietly switched tools. If the first week was a farce, the later years were a form. Forms do not make good newsreels. They do, sometimes, keep wheat standing. That is the boring ending history prefers, which is why the newsreel ending is the one you remember.""",
    """So who won. Not the three men, not the camera, not the nickname. The emus won the headline. The farmers eventually won fences and bounties. The army won a chapter it cannot close with a medal. If you need a moral, skip “nature is magic.” Take this: a machine gun is a terrible instrument for a fast, scattered, six-foot problem that refuses to stand in a row. Meredith’s men suffered no wounds. Their dignity filed a complaint. Pearce got a title he did not order. Campion went back to being a district with wheat and weather. The next time someone sells you a simple tool for a scattered problem, remember the truck that could not catch a bird. Would you have taken the job. Two guns, a jam at the dam, a truck that could not catch a bird, and a newsreel waiting for a victory that never lined up. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags, "
    "no photoreal faces. Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, "
    "oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("army-vs-birds", "Australia once sent the army to fight birds.", f"Cartoon title beat: three tiny soldiers facing a huge emu on cream paper. {STYLE}"),
    ("not-a-meme", "Not a metaphor. Not an internet meme.", f"Ink the mascot shaking his head at a glowing phone, mouth closed. {STYLE}"),
    ("campion-map", "November nineteen thirty two, Campion, wheatbelt.", f"Simple cartoon map of Western Australia wheat paddocks, no flags. {STYLE}"),
    ("fences-suggestion", "Emus walked through fences like fences were a suggestion.", f"Cartoon emu stepping through a broken wire fence, wheat behind. {STYLE}"),
    ("twenty-thousand", "About twenty thousand birds after breeding season.", f"A horizon packed with simple emu shapes, not a swarm of blood. {STYLE}"),
    ("veteran-farmers", "Many farmers were World War One veterans on dry land.", f"Cartoon small farmhouse and a medal in a drawer, no battle gore. {STYLE}"),
    ("pearce-yes", "They asked Sir George Pearce for machine guns. He said yes.", f"Cartoon minister stamping YES on a bird-shaped request, no portrait. {STYLE}"),
    ("three-men", "The force was three men, not a division.", f"Three cartoon soldiers in a line, tiny against a paddock. {STYLE}"),
    ("two-lewis", "Two Lewis guns. Ten thousand rounds.", f"Two cartoon machine guns and a crate of ammo, toy-like, no gore. {STYLE}"),
    ("movietone", "A Fox Movietone camera came too.", f"Cartoon newsreel camera on a tripod in a paddock. {STYLE}"),
    ("cull-practice", "Official cull. Unofficial target practice.", f"Split image: wheat icon versus a paper target with an emu silhouette. {STYLE}"),
    ("no-briefing", "The emus did not attend the briefing.", f"Empty folding chairs, emus already running past the tent. {STYLE}"),
    ("veteran-land", "Veterans were handed farms in marginal country.", f"Cartoon land grant paper over red dry dirt. {STYLE}"),
    ("depression-wheat", "Depression prices fell. Subsidies did not show up.", f"Cartoon wheat price arrow down, empty envelope. {STYLE}"),
    ("coast-buffet", "Emus found paddocks and stock water like a buffet.", f"Cartoon emus at a water trough beside wheat, funny not cruel. {STYLE}"),
    ("rabbits-follow", "Fences broke. Rabbits followed.", f"Cartoon rabbit popping through an emu-shaped hole in a fence. {STYLE}"),
    ("ex-soldiers-know", "Ex-soldiers said they knew what a Lewis gun could do.", f"Cartoon veterans pointing at a gun manual, no combat scene. {STYLE}"),
    ("who-pays", "The state moved them. Farmers fed them. Soldiers fired.", f"Three cartoon wallets labeled state, farm, army, simple icons. {STYLE}"),
    ("nickname", "Pearce got nicknamed Minister of the Emu War.", f"Cartoon nameplate with a tiny emu perched on it. {STYLE}"),
    ("rain-delay", "Rain delayed the start. The birds scattered.", f"Cartoon rain over paddocks, emus spreading out. {STYLE}"),
    ("november-second", "Second of November, three-man war clocks in.", f"Cartoon calendar November two, soldiers arriving by truck. {STYLE}"),
    ("fifty-outrange", "Day one: about fifty emus, out of range.", f"Tiny soldiers, distant emu dots, range circle too short. {STYLE}"),
    ("herd-fails", "Settlers tried to herd them. The flock split.", f"Cartoon farmers waving hats, emus splitting like fireworks. {STYLE}"),
    ("first-burst", "The first burst did almost nothing.", f"Cartoon dotted bullets falling short of running birds, no hits shown. {STYLE}"),
    ("maybe-dozen", "Later, a number, then maybe a dozen.", f"A small tally chalked on a fence post, cartoon, no corpses. {STYLE}"),
    ("not-turkey", "This was not a turkey shoot.", f"Ink the mascot ripping a carnival-shoot ticket, mouth closed. {STYLE}"),
    ("refuse-parade", "They refuse to be a parade.", f"Emus running in chaotic arrows, soldiers in a neat useless line. {STYLE}"),
    ("dam-wait", "Fourth of November: an ambush at a dam.", f"Cartoon dam, soldiers hiding, water glinting, cream paper. {STYLE}"),
    ("thousand-come", "More than a thousand emus came in.", f"A wide cartoon river of emu shapes approaching water. {STYLE}"),
    ("gun-jam", "The gun jammed after twelve.", f"Cartoon Lewis gun with a big JAM cloud, birds already leaving. {STYLE}"),
    ("lookout-bird", "Each pack had a six-foot lookout bird.", f"One tall cartoon emu on a rise, watching, no gore. {STYLE}"),
    ("truck-gun", "They bolted a gun onto a truck.", f"Cartoon truck with a gun on the bed, bouncing, cannot aim. {STYLE}"),
    ("truck-loses", "The truck could not catch them.", f"Emu pulling ahead of a dusty cartoon truck, motion lines. {STYLE}"),
    ("twenty-five-hundred", "By the eighth: about twenty five hundred rounds gone.", f"Cartoon ammo crate almost empty, confused tally. {STYLE}"),
    ("count-gap", "Fifty killed, or two hundred, or five hundred.", f"Three cartoon clipboards with different numbers, arguing. {STYLE}"),
    ("dignity-only", "No human casualties except dignity.", f"A cartoon medal of dignity cracked in half, funny. {STYLE}"),
    ("pearce-pulls", "Headlines laughed. Pearce pulled the guns.", f"Cartoon newspaper stack and soldiers packing a truck. {STYLE}"),
    ("emus-stay", "The emus did not withdraw.", f"Emus still in wheat, soldiers' dust cloud leaving. {STYLE}"),
    ("mitchell", "Premier James Mitchell wanted the army back.", f"Cartoon premier stamping REQUEST AGAIN, no portrait. {STYLE}"),
    ("three-hundred-claim", "A base note claimed three hundred kills.", f"A tidy round number on a form, rubber stamp, suspicious. {STYLE}"),
    ("restart", "Twelfth of November: restart approved.", f"Cartoon calendar November twelve, guns coming back. {STYLE}"),
    ("no-gunners", "The state still lacked gunners. Meredith returned.", f"Empty gunner chair, Meredith's hat returning to a peg. {STYLE}"),
    ("forty-then-dud", "Two days, about forty birds. Then a dud day.", f"A cartoon graph that rises then faceplants. {STYLE}"),
    ("hundred-a-week", "By December, about a hundred a week.", f"A small weekly tally beside a huge twenty-thousand flock ghost. {STYLE}"),
    ("tenth-december", "Tenth of December: recalled, tidy arithmetic incoming.", f"Cartoon desk, report folder, calendar December ten. {STYLE}"),
    ("ten-per-bird", "Nine hundred eighty six kills, ten rounds each, too neat.", f"A calculator showing ten point zero zero, raised eyebrow from Ink. {STYLE}"),
    ("serventy", "Serventy: the emu command ordered guerrilla tactics.", f"Tiny emu squads splitting, cartoon arrows, no gore. {STYLE}"),
    ("who-won", "Would you have taken the job. Tell me in the comments.", f"Ink the mascot pointing at the viewer, mouth closed, cream paper. {STYLE}"),
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, ten-second cadence)."""
    seconds = index * 10
    return f"{seconds // 60:02d}{seconds % 60:02d}"


def _beats() -> list[tuple[str, str, str]]:
    """Stamp each row with a ten-second mmss slug prefix."""
    need = drawn_beat_count(480.0)
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
        title="The Army That Lost to Emus",
        description=(
            "Campion, nineteen thirty two. Three soldiers, two Lewis guns, twenty thousand emus. "
            "The birds did not line up. The report still tries to."
        ),
        tags=(
            "history",
            "emu",
            "australia",
            "cartoon",
            "true story",
            "army",
            "wheat",
            "1932",
            "campion",
            "funny",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="BIRDS WON",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Army That Lost to Emus",
        language="en",
        minutes=8,
        target_seconds=480.0,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-emu.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    board = PROJECT_ROOT / "output" / "storyboard" / scenario.project_id
    board.mkdir(parents=True, exist_ok=True)
    tsv = board / "beats.tsv"
    lines = ["index\tfilename\tprompt"]
    for index, (slug, _covers, prompt) in enumerate(beats, start=1):
        lines.append(f"{index:03d}\t{index:02d}-{slug}.png\t{prompt}")
    tsv.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(scenario.project_id)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))
    print("voice", scenario.tts.voice, "rate", scenario.tts.rate, "cat", scenario.youtube.category_id)
    print("hook", scenario.youtube.thumbnail_hook)
    print("tsv", tsv)


if __name__ == "__main__":
    main()

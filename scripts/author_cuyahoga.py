"""Author Drawn Anyway episode 6: Cuyahoga River fire, Cleveland, nineteen sixty nine."""

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
    """A river in Cleveland caught fire. That is not a metaphor, and it is not a cartoon you invented after a chemistry class. On Sunday the twenty second of June nineteen sixty nine, an oil slick and a raft of industrial debris on the Cuyahoga ignited near railroad bridges by Republic Steel. A spark from a passing train, some tellings say a flare, was enough. The alarm went at eleven fifty six in the morning. The fire lasted less than half an hour. Damage was mostly two trestles, about fifty thousand dollars in the usual tally, forty five thousand on the Norfolk and Western, five thousand on the Newburgh and South Shore. Nobody got a photograph. Keep that picture. A short fire on a working river. A city that already knew the water could burn. A magazine that would later print a picture from nineteen fifty two. Everything after this is just that picture hiring a caption.""",
    """Start with why a river burns, because water does not volunteer. Oil floats. Debris piles where railroad bridges pinch the channel. For a century Cleveland treated this stretch as industrial plumbing: mills, docks, sewers, a wet conveyor into Lake Erie. In that light a river fire felt like a workplace accident, not a miracle of physics. The Cuyahoga had burned more than ten times already. November nineteen fifty two was the ugly one: tugs, buildings, shipyards, damage in the millions, photographers on the docks, and that is the blaze people still see when they close their eyes. A fire in nineteen twelve killed five dock workers. Those numbers belong in the file so sixty nine cannot steal their scale. If you came for nineteen sixty nine as the first time water misbehaved, you already lost the plot. The sixty nine fire was not the worst morning. It was the morning that arrived after the country had started wanting a different kind of river, which is a logistics change, not a sermon about who should feel ashamed.""",
    """The morning itself was a trestle job. Historian Paul Nelson, working from Cleveland fire records, put the burning surface at about three hundred feet across. Flames on the creosote-coated trestle jumped high, even a hundred feet in one account, which sounds like a disaster movie until you remember the clock. Land companies and the fireboat Anthony J. Celebrezze knocked it down in twenty or thirty minutes, before any camera clocked in. The Plain Dealer gave it a slice on page eleven C, no byline, because industrial rivers catching fire was not a novelty in the Flats. Clevelanders were not shocked. They lived next to the plumbing. Railroad bridges near Republic Steel had been trapping debris for years; oil made the raft flammable; a Sunday train supplied the rest. The official idea, locally, was: put the trestle out, count the damage, go back to Monday. The unofficial idea, about to walk in with a mayor, was that Monday could be a tour.""",
    """Monday the twenty third, Mayor Carl Stokes took the press to the river. Stokes was already a national story: first Black mayor of a major American city, elected in nineteen sixty seven. He did not need a fire to exist. He used the fire as a map. The river crossed too many towns, too many permits, too many suburbs he did not govern. Cleaning Cleveland's pipes would not clean what arrived from upstream. Betty Klaric of the Cleveland Press, one of the country's first full-time environment reporters, had been on Save Lake Erie Now for years. She covered the tour. National magazines later lifted that local reporting. Public utilities director Ben Stefanski had already sold a hundred million dollar bond in nineteen sixty eight, two to one, more yes votes than anything else on the ballot, sewers and treatment to protect the lake. The fire did not invent that vote. The fire arrived after the vote, which is the detail textbooks like to skip because it is less cinematic than a flame on water.""",
    """August first, Time magazine opened a new Environment section and put Stokes in it. The essay, later filed under America's sewage system and the price of optimism, listed other dirty urban rivers, then called the Cuyahoga, about eighty miles long, among the worst. Chocolate-brown, oily, bubbling, a river that oozes rather than flows, and a grim joke about decaying instead of drowning. Treat that as Time's packaging. Do not turn it into a gore reel. Time also ran a photograph of a river on fire that was not this fire. It was November nineteen fifty two, the expensive one, tugs in the frame, the picture that looks like the end of a city. There is still no known photo of the twenty minute job in sixty nine. In nineteen sixty nine the Santa Barbara oil spill had already eaten more national ink. Months later, Cleveland's small fire became the symbol and Santa Barbara became a footnote. That swap is the plot. A caption can outrank a clock.""",
    """Here is the leftover fact, and it is not a conspiracy. The famous image is seventeen years early. The famous fire is a short alarm. The city had already passed the bond. Nationally the Water Pollution Control Act of nineteen sixty five was already law. Stokes would testify in nineteen seventy that cities could not fix a watershed with a city limit. His brother, Congressman Louis Stokes, pushed cleanup money in the House. Northeast Ohio built a regional sewer district. Ohio stood up a state environmental agency. The federal Clean Water Act arrived in nineteen seventy two. Earth Day was April nineteen seventy. The Environmental Protection Agency opened in December that year. Some textbooks draw a straight fuse from one Sunday trestle to all of that. The National Park Service's own write-up calls that the myth: people agree on June twenty two, then myth walks in when the fire is billed as the primary cause of the whole environmental toolbox. The fire was a reminder. The work was already a file.""",
    """Rehook, because the internet likes a simple villain. Industry did load the river. Oil did float. Debris did trap at the bridges. That is the chemistry. What the sixty nine morning did not do is invent pollution, invent Earth Day, or secretly write the Clean Water Act in thirty minutes. Deindustrialization was already thinning some of the load as plants cut back. Clevelanders had already voted to tax themselves for pipes. Stefanski had lined up papers, citizen groups, even suburban governments, and called clean water apple pie: nobody wanted to vote against it. The symbol still matters. Symbols are how a country files a feeling. You are allowed to laugh at a river that burned. You are not required to pretend the twenty minute fire was a five-alarm apocalypse, or that the Time photograph was shot that Sunday, or that guilt is a substitute for a sewer interceptor. A file can hold a small fire and a large caption at the same time.""",
    """Aftermath is where the jokes beat the incident report. Cleveland collected years of burning-river punchlines, then beers and festivals that recoded the insult as a souvenir. Parts of the Flats turned from mill yard to nightlife once the water stopped being a punchline you could smell. Fish came back in stretches that had been written off as empty of even the worms that live on waste. That recovery is boring in the best way: permits, plants, regional pipes, a law with teeth. The leftover tool was not a bigger hose. It was a different definition of what a river is for. When it is a sewer, fire is a maintenance issue. When it is a public water, fire is a scandal. Sixty nine sits on that hinge. The hinge was already turning in sixty eight. The magazine froze the hinge as a flame from fifty two.""",
    """So who won. Not the trestle. Not the spark. The nineteen fifty two photograph won the textbook. Time won a sentence about ooze. Stokes won a national microphone for a regional pipe problem. Klaric won years of unglamorous copy that suddenly had a picture, even if it was the wrong year. If you need a moral, skip nature is magic. Take this: a caption is a terrible instrument for a twenty minute fire, and a twenty minute fire is a terrible summary of a hundred million dollar bond. The next time someone shows you a river in flames and dates it sixty nine, ask which Sunday, and which negative. Would you have printed the fifty two photo. A short fire, no snapshot, a mayor on a tour, and a picture from another decade. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags, "
    "no photoreal faces, no drowning, no decaying bodies, no graphic fire victims. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("river-fire-open", "A river in Cleveland caught fire.", f"Cartoon title beat: a cream river with comic oil rainbow and tiny flames under a trestle, Cleveland mill silhouettes. {STYLE}"),
    ("not-a-metaphor", "Not a metaphor. Not a chemistry-class cartoon.", f"Ink the mascot shaking his head at a flask labeled METAPHOR with a red X, mouth closed. {STYLE}"),
    ("june-twenty-two", "Sunday, June 22, 1969, the Cuyahoga.", f"Cartoon calendar June 22 1969, a winding river into a lake, no flags. {STYLE}"),
    ("oil-and-debris", "Oil slick and debris piled at railroad bridges.", f"Toy trestles pinching a channel, debris raft and oil sheen, not gory. {STYLE}"),
    ("train-spark", "A spark from a passing train was enough.", f"A tiny locomotive over a bridge, one comic spark dropping toward the water. {STYLE}"),
    ("eleven-fifty-six", "Alarm at 11:56 a.m.", f"A fire-alarm box and a clock 11:56, cream paper. {STYLE}"),
    ("half-hour", "The fire lasted less than half an hour.", f"A stopwatch under 30 MIN, small comic flames already shrinking. {STYLE}"),
    ("fifty-thousand", "About $50,000 damage, mostly two trestles.", f"Two broken toy trestles, a price tag $50,000. {STYLE}"),
    ("no-photo", "Nobody got a photograph.", f"A camera with an empty frame and a NO SHOT stamp. {STYLE}"),
    ("why-it-burns", "Why a river burns: oil floats, debris piles.", f"A simple diagram: oil on water, debris at a pinch point. {STYLE}"),
    ("industrial-pipe", "This stretch was treated as industrial plumbing.", f"A river drawn as a pipe through mills, PIPE stamp, no guilt poster. {STYLE}"),
    ("more-than-ten", "It had burned more than ten times already.", f"A tally of many small flame icons across a century timeline. {STYLE}"),
    ("fifty-two-worse", "November 1952 was the ugly expensive one.", f"Calendar Nov 1952, tugs and docks as toys, $ MILLIONS tag, no gore. {STYLE}"),
    ("nineteen-twelve", "A 1912 fire killed five dock workers.", f"A somber clipboard 1912, CASUALTIES 5, respectful not graphic. {STYLE}"),
    ("not-the-first", "1969 was not the first time water misbehaved.", f"Ink pointing at a FIRST? stamp with a red X, mouth closed. {STYLE}"),
    ("trestle-job", "The morning itself was a trestle job.", f"Close on a creosote trestle with comic flames, firefighters tiny. {STYLE}"),
    ("three-hundred-feet", "Burning surface about 300 feet across.", f"A 300 FT measuring tape across a small oily circle. {STYLE}"),
    ("hundred-feet-high", "Trestle flames jumped high, even 100 feet in one account.", f"A 100 FT height arrow on a trestle, cartoon not disaster-movie. {STYLE}"),
    ("celebrezze", "Fireboat Anthony J. Celebrezze helped knock it down.", f"A cheerful toy fireboat labeled CELEBREZZE spraying the water. {STYLE}"),
    ("page-eleven", "The Plain Dealer put it on page 11-C, no byline.", f"A newspaper with a tiny 11-C box, the fire almost a footnote. {STYLE}"),
    ("not-shocked", "Clevelanders were not shocked.", f"Tiny workers shrugging at a river flame like a leaky pipe. {STYLE}"),
    ("monday-tour", "Monday: Mayor Carl Stokes took the press to the river.", f"A mayor's hat leading reporters along a rail, no portrait. {STYLE}"),
    ("stokes-map", "He used the fire as a map of jurisdictions.", f"A river crossing many town-limit stamps Stokes cannot reach. {STYLE}"),
    ("betty-klaric", "Betty Klaric covered it for the Cleveland Press.", f"A reporter notebook SAVE LAKE ERIE, press hat, no photoreal face. {STYLE}"),
    ("hundred-million", "1968: voters passed a $100 million bond, two to one.", f"A ballot box 1968, $100M, 2-to-1 checkmark. {STYLE}"),
    ("stefanski", "Ben Stefanski had already sold the pipes.", f"A utilities desk, sewer-pipe blueprint, BOND stamp. {STYLE}"),
    ("after-the-vote", "The fire arrived after the vote.", f"A timeline: VOTE then FIRE, the vote first. {STYLE}"),
    ("time-august", "August 1, Time opens an Environment section.", f"A magazine cover-ish ENVIRONMENT, August 1 1969, no logos stolen. {STYLE}"),
    ("oozes-line", "Time: the river oozes rather than flows.", f"A sluggish cartoon river labeled OOZES, not a corpse. {STYLE}"),
    ("wrong-photo", "The photograph was not this fire. It was 1952.", f"A photo frame dated 1952 hanging on a 1969 calendar. {STYLE}"),
    ("no-sixty-nine-shot", "Still no known photo of the 1969 job.", f"An empty evidence board, 1969 slot blank. {STYLE}"),
    ("santa-barbara", "Santa Barbara's oil spill had already eaten more ink.", f"Two newspaper stacks: SANTA BARBARA tall, CLEVELAND small then growing. {STYLE}"),
    ("caption-outranks", "A caption can outrank a clock.", f"A giant CAPTION crushing a tiny stopwatch. {STYLE}"),
    ("seventeen-early", "The famous image is seventeen years early.", f"A ruler 17 YEARS between two flame icons. {STYLE}"),
    ("already-law", "The 1965 Water Pollution Control Act was already law.", f"A law book 1965 on a desk, fire still in the future. {STYLE}"),
    ("stokes-senate", "Stokes later testified that city limits cannot fix a watershed.", f"A Senate-hearing table, a river map bigger than a city box. {STYLE}"),
    ("louis-stokes", "Congressman Louis Stokes pushed cleanup money in the House.", f"A House folder CLEANUP FUNDS, two Stokes nameplates, no portraits. {STYLE}"),
    ("earth-day", "Earth Day, April 1970. Students marched to the river.", f"Tiny marchers and a river, April 1970 calendar, no flags as identity. {STYLE}"),
    ("epa-december", "EPA opened December 1970. Clean Water Act 1972.", f"Two stamps: EPA DEC 1970 and CWA 1972. {STYLE}"),
    ("not-a-straight-fuse", "A straight fuse from one trestle to all of that is the myth.", f"A fuse that branches into many files, not one spark. {STYLE}"),
    ("reminder-not-inventor", "The fire was a reminder. The work was already a file.", f"A REMINDER sticky on a thick WORK folder. {STYLE}"),
    ("chemistry-not-sermon", "Oil floated. Debris trapped. That is chemistry, not a sermon.", f"Ink holding a CHEMISTRY flask, a SERMON book closed, mouth closed. {STYLE}"),
    ("two-definitions", "Sewer versus public water: fire as maintenance or scandal.", f"Split signs: MAINTENANCE and SCANDAL over the same river. {STYLE}"),
    ("hinge-sixty-eight", "The hinge was already turning in 1968. The magazine froze a flame.", f"A door hinge labeled 1968, a magazine pinning a flame icon. {STYLE}"),
    ("jokes-then-beer", "Punchlines, then beers and festivals named for the burn.", f"A joke microphone next to a souvenir bottle BURNING RIVER, not a drunk gag. {STYLE}"),
    ("fish-back", "Fish came back in stretches written off.", f"Simple cartoon fish returning to a cleaner blue-cream river. {STYLE}"),
    ("boring-recovery", "Recovery is permits, plants, regional pipes.", f"Three icons: PERMIT, PLANT, PIPE, trophy for boredom. {STYLE}"),
    ("not-a-bigger-hose", "The leftover tool was not a bigger hose.", f"A giant hose in a museum case, a tiny law book on the desk. {STYLE}"),
    ("who-won", "Who won. The 1952 photograph won the textbook.", f"A textbook swallowing a 1952 photo, the 1969 alarm tiny. {STYLE}"),
    ("time-won-ooze", "Time won a sentence about ooze.", f"A quote bubble OOZES bigger than a fireboat. {STYLE}"),
    ("stokes-won-mic", "Stokes won a microphone for a regional pipe problem.", f"A microphone labeled PIPES not FLAMES. {STYLE}"),
    ("ask-the-negative", "Ask which Sunday, and which negative.", f"Two film negatives, 1952 and 1969, only one has an image. {STYLE}"),
    ("would-you-print", "Would you have printed the 1952 photo.", f"A PRINT? stamp hovering over the wrong-year picture. {STYLE}"),
    ("comment-hook", "Tell me in the comments. That is the receipt. Drawn anyway.", f"Ink the mascot pointing at the viewer, mouth closed, cream paper. {STYLE}"),
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
        title="The River That Caught Fire",
        description=(
            "Cleveland, June twenty two, nineteen sixty nine. A twenty-minute trestle fire, "
            "no photograph, and a magazine that printed nineteen fifty two."
        ),
        tags=(
            "history",
            "cleveland",
            "cuyahoga",
            "cartoon",
            "true story",
            "1969",
            "river",
            "environment",
            "funny",
            "ohio",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="WRONG PHOTO",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The River That Caught Fire",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-cuyahoga.json"
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

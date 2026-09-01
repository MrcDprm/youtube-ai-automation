"""Author Drawn Anyway episode 8: Strasbourg dancing plague, fifteen eighteen."""

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
    """A city once tried to cure dancing by hiring a band. That is not a metaphor, and it is not a cartoon you invented after a festival. In July fifteen eighteen, in Strasbourg, then an imperial free city in Alsace in the Holy Roman Empire, a woman later named Frau Troffea, or Trauffea in some spellings, stepped into a street and began to dance with no music. Four of the six surviving chronicles put a named woman first. Ned Pennant-Rea, working the later retellings, puts her on the fourteenth, on a cobbled street outside a half-timbered house, no fiddle, no drum. She kept going for about a week, collapsing from exhaustion, resting, starting again. Some accounts say her husband joined. Within days more than thirty people were moving the same way. This is not a party. Observers said the motion looked vacant, not joyful, arms thrashing, sweat, cries for help. Keep that picture without turning it into gore. A street with no soundtrack. A council that would later rent guild halls. Physicians who would write hot blood. Everything after this is just that picture hiring musicians.""",
    """Start with why a street becomes a clinic. Strasbourg in fifteen eighteen was already brittle, even by the rough standard of the early sixteen hundreds. John Waller, writing in The Lancet in two thousand nine, lists the pile: a succession of appalling harvests, the highest grain prices for over a generation, syphilis arriving as a new terror, old killers like leprosy and plague still in the file. People already believed Saint Vitus, a fourth-century martyr and patron of dancers and of people with seizures, could curse you into dancing if you failed to propitiate him. That belief is not a punchline about peasants. It is the local instruction set. When Troffea did not stop, neighbors did not invent a nightclub. They watched a fear they already had walk into daylight. Historian Lynneth Miller notes the city's first move was medical, not a miracle hunt. By the end of a week the count is usually given as about three dozen. By August the range in the papers is fifty to four hundred. The Imlin family chronicle is the source for the high number. Treat four hundred as a ceiling a later household wrote down, not a turnstile you can audit.""",
    """The city did what cities do. It called the physicians. The clergy were ready to call it Saint Vitus. The privy council listened to the guild of physicians instead and declared a natural disease from overheated blood. Humoral theory said bleed it. The doctors on the ground prescribed the older remedy used on past dancing manias: the afflicted must dance themselves free of it. Daniel Specklin, a sixteenth-century architect chronicling the file, records the work order. Carpenters and tanners were to transform their guild halls into temporary dance floors. Platforms went up in the horse market and in the grain market, in full view of anyone still shopping. Dozens of musicians were paid to play drums, fiddles, pipes, and horns. Healthy dancers were brought in as encouragement. Strong men were hired to keep people upright so the motion would not stop. The official idea was controlled exhaustion, a fever danced out under a roof the city already owned. The unofficial idea, which nobody put on the invoice, was a stage with a crowd.""",
    """If you came for a morality play about stupid officials, slow down. They were following the medical brief they had. Hot blood cools if you sweat it. A market is a place you already own. A guild hall already has a roof and a guild that can take orders. Hiring a band is cheaper than inventing a new disease, and cheaper than admitting you do not have one. It is also a terrible instrument for a fear that spreads by watching. More people joined. The contagion got a soundtrack. At some point the council reversed itself. Public dancing banned. Music banned. The cure had become the amplifier. Write that down. That mismatch is the plot. Not a joke at the dancers, who were asking for help in a square that now had a beat. A work order that advertised the symptom it was trying to spend. When a treatment requires an audience, the audience is part of the dose.""",
    """Then the file changed religions again. If the dance was a curse, only a shrine could close it. The remaining dancers were sent a day's ride west to Saverne, Zabern in German, to a mountaintop chapel of Saint Vitus. Priests placed the still-moving under a wooden carving of the saint, small crosses in their hands, red shoes on their feet. Holy water sprinkled, crosses of consecrated oil painted on the tops and soles. Incense. Latin incantations. Word came back to Strasbourg that Vitus had forgiven them, which in this file means the stream of pilgrims slowed to a trickle within about a week. The episode ran from mid-July into late August or early September, more than a month. Similar outbreaks had already happened along the Rhine and Moselle, including a famous one at Aachen in thirteen seventy four, and a churchyard story from Colbigk in Saxony centuries earlier. Strasbourg did not invent choreomania. Strasbourg hired a venue for it, then tried to unhire the venue.""",
    """Here is the leftover fact, and it is not a body count. Later writers, and John Waller repeating them with a careful if, talk about fifteen dying a day at the height, which would run into the hundreds if you multiply it by enough weeks. Strasbourg's own contemporary notes, physician notes, cathedral sermons, local chronicles, and orders from the city council, are clear that people danced. They do not print that daily number. They do not even print whether anyone died. Collapses from heat, hunger, thirst, and exhaustion are easy to imagine on a July platform. A specific toll is not in the fifteen eighteen paperwork. Do not turn absence into a miracle of zero, and do not turn a later rate into a receipt. The punchline you can stand on is logistical: they built stages, then banned the band, then booked a shrine. That sequence is in the file. The graveyard arithmetic is a product, not a tally.""",
    """Rehook, because the internet likes a fungus. Ergot on damp rye can cause convulsions and visions. Waller argued in The Lancet that ergot is a poor fit: people poisoned like that do not keep dancing for days at a time, they would not all react the same way, and the outbreaks cluster on the Rhine and Moselle, rivers that link towns, not a single crop map. Robert Bartholomew guessed adherents of heretical sects dancing for divine favor. Paracelsus, writing about a decade later, hostile to the story, split a natural cause in the blood, he talked about laughing veins, from an imagined influence that jumped from person to person, and he declined to make it purely a divine spanking. You can keep the argument. You do not get to skip the invoice. The city paid musicians to treat a street. That is the sentence that survives a theory war, whether you side with Waller, with rye, or with a saint.""",
    """None of this makes the dancers a gag reel, or the council a cartoon of incompetence you get to feel superior to. They had humoral medicine, a saint with a dancing curse already in the folklore, grain stress, disease, and a public square. The chemistry, if you need a word, is attention plus a script people already feared, a trance Waller called stress-induced, not a rave. The logistics is who owns the floor. When the floor was a grain market with a paid band, the file grew. When the floor was a chapel off-stage, the file shrank. A caption can call that mass psychogenic illness. A work order called it recovery. Both captions hired carpenters. You are allowed to laugh at the idea of prescribing more dancing. You are not required to laugh at the people who could not stop, and you are not entitled to a corpse montage the fifteen eighteen clerks did not file.""",
    """So who won. Not the horse market. Not the hot-blood theory. Not the death-toll arithmetic from a later century. Specklin won a sentence about platforms. The physicians won a week of being believed. Saint Vitus won the last booking. The dancers won the only thing this file should give them: they were patients, not a festival, not a meme about shoe blood. If you need a moral, skip never have a party. Take this: a stage is a terrible instrument for a contagious fear, and a contagious fear is a terrible brief for a band. The next time someone tells you they danced themselves to death in Strasbourg, ask which chronicle printed the deaths, and whether the city had already rented the grain market. Would you have hired the musicians. A street, two guild halls, a mute stamp, a hill chapel, red shoes as ritual not a wound. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags, "
    "no photoreal faces, no bleeding, no corpses, no mockery of the sick, no child victims. "
    "Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, oversized black marker, "
    "mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("street-no-band", "A city tried to cure dancing by hiring a band.", f"Cartoon title beat: a cobbled street, one woman mid-step, empty music stand, cream paper. Kind, not mocking. {STYLE}"),
    ("not-a-festival", "Not a metaphor. Not a festival cartoon.", f"Ink shaking his head at a FESTIVAL stamp with a red X, mouth closed. {STYLE}"),
    ("july-1518", "July 1518, Strasbourg in Alsace.", f"Cartoon calendar July 1518, a half-timbered street, no flags. {STYLE}"),
    ("frau-troffea", "Frau Troffea began to dance with no music.", f"A named woman silhouette dancing, a silent fiddle with an X. No portrait. {STYLE}"),
    ("four-chronicles", "Four of six chronicles put a named woman first.", f"Six little chronicle books, four circled, two dim. {STYLE}"),
    ("fourteenth", "A later retelling pins the day as July 14.", f"A calendar 14 circled with LATER written small. {STYLE}"),
    ("a-week", "She kept going about a week, rest, then again.", f"Seven day boxes, a rest pillow on one, dance swirl on others. Not cruel. {STYLE}"),
    ("thirty-more", "Within days more than 30 people were moving the same way.", f"A small crowd of simple figures, 30+ label, not a party. {STYLE}"),
    ("not-joyful", "Observers said the motion looked vacant, not joyful.", f"A JOY meter at empty, a vacant-not-mean cartoon face. {STYLE}"),
    ("keep-picture", "A street. A council. Physicians writing hot blood.", f"Three icons: street, council table, HOT BLOOD flask. {STYLE}"),
    ("brittle-city", "Strasbourg was already brittle in 1518.", f"A city skyline with a CRACK label, cream paper. No flags. {STYLE}"),
    ("waller-pile", "Waller: bad harvests, high grain, disease in the file.", f"A Lancet-ish notebook: GRAIN, HARVEST, DISEASE stacked. {STYLE}"),
    ("vitus-curse", "People already believed Saint Vitus could curse a dance.", f"A saint icon and a DANCE curse tag, not a horror poster. {STYLE}"),
    ("instruction-set", "That belief was the local instruction set.", f"A manual titled IF VITUS, THEN DANCE. Ink reading, mouth closed. {STYLE}"),
    ("three-dozen", "By week's end about three dozen.", f"A tally 36, simple hats, not a rave. {STYLE}"),
    ("fifty-to-four-hundred", "By August the range is 50 to 400.", f"A slider from 50 to 400, IMLIN tag on the high end. {STYLE}"),
    ("not-a-turnstile", "Four hundred is a chronicle ceiling, not a turnstile.", f"A turnstile with a question mark, 400 in quotes. {STYLE}"),
    ("call-physicians", "The city called the physicians.", f"A council table passing a folder to a PHYSICIANS hat. {STYLE}"),
    ("hot-blood", "They called it a natural disease from overheated blood.", f"A thermometer flask labeled HOT BLOOD, not gore. {STYLE}"),
    ("dance-free", "Prescription: dance themselves free of it.", f"A prescription pad: DANCE IT OUT. {STYLE}"),
    ("specklin", "Daniel Specklin records the work order.", f"An architect's notebook SPECKLIN, guild-hall sketch. {STYLE}"),
    ("guild-halls", "Carpenters and tanners turned halls into floors.", f"Two guild signs CARPENTERS and TANNERS over a dance floor. {STYLE}"),
    ("two-markets", "Platforms in the horse market and the grain market.", f"Two stages labeled HORSE MARKET and GRAIN MARKET. {STYLE}"),
    ("hired-band", "Dozens of musicians: drums, fiddles, pipes, horns.", f"A cartoon band with those four instruments, paid sacks. {STYLE}"),
    ("healthy-dancers", "Healthy dancers brought in as encouragement.", f"Helpers in bright shoes beside tired simple figures, kind not mocking. {STYLE}"),
    ("strong-men", "Strong men hired to keep people upright.", f"Two helpers supporting a tired dancer, respectful, no slapstick cruelty. {STYLE}"),
    ("controlled-exhaustion", "The official idea was controlled exhaustion.", f"A plan diagram: STAGE then REST then CURE? {STYLE}"),
    ("the-stage", "The unofficial idea was a stage.", f"A spotlight on a market platform, INVOICE under it. {STYLE}"),
    ("following-brief", "They were following the medical brief they had.", f"Ink pointing at a BRIEF folder, not a STUPID stamp, mouth closed. {STYLE}"),
    ("watching-spreads", "A fear that spreads by watching.", f"Eyes in a crowd, dotted arrows of attention, no gore. {STYLE}"),
    ("soundtrack", "The contagion got a soundtrack.", f"Sound notes flying off a stage into side streets. {STYLE}"),
    ("ban-dancing", "Then the council banned public dancing.", f"A big NO DANCING seal over the market. {STYLE}"),
    ("ban-music", "They banned the music too.", f"Instruments with mute bags, BAND CLOSED. {STYLE}"),
    ("mismatch", "A work order that advertised the symptom.", f"A poster CURE that looks identical to the symptom swirl. {STYLE}"),
    ("shrine-plan", "If it was a curse, only a shrine could close it.", f"A road arrow from market to CHAPEL. {STYLE}"),
    ("saverne", "A day's ride to Saverne, Saint Vitus in the hills.", f"A hill chapel SAVERNE, small travelers, no flags. {STYLE}"),
    ("red-shoes", "Red shoes, holy water, painted crosses on the soles.", f"A pair of red shoes with tiny crosses, objects not wounds. {STYLE}"),
    ("incense-latin", "Incense, Latin, small crosses in their hands.", f"Smoke curls and a Latin book, kind ritual, not horror. {STYLE}"),
    ("forgiven", "Word came back that Vitus had forgiven them.", f"A FORGIVEN banner, the pilgrim stream shrinking. {STYLE}"),
    ("more-than-month", "Mid-July into late August or early September.", f"A summer bar from JUL to SEP, over a month. {STYLE}"),
    ("aachen-1374", "Aachen had a famous outbreak in 1374.", f"A timeline: 1374 AACHEN, then 1518 STRASBOURG. {STYLE}"),
    ("unhire-venue", "They hired a venue, then tried to unhire it.", f"A lease paper torn between HIRE and UNHIRE. {STYLE}"),
    ("no-body-count", "Contemporary notes do not print a death toll.", f"A 1518 ledger with the DEATHS line blank. Respectful. {STYLE}"),
    ("fifteen-a-day", "Later: 15 a day, if true, into the hundreds.", f"A calculator 15 x DAYS = ?, IF TRUE in small type. {STYLE}"),
    ("not-a-receipt", "A later rate is not a 1518 receipt.", f"A receipt stamped LATER, not 1518. {STYLE}"),
    ("ergot-rehook", "The internet likes a fungus. Ergot is a poor fit.", f"A rye ear with a red X, Waller's NO stamp. {STYLE}"),
    ("rhine-cluster", "Outbreaks cluster on the Rhine and Moselle.", f"A simple river map, dots along two rivers, no flags. {STYLE}"),
    ("paracelsus", "Paracelsus later split hot blood from imagined influence.", f"Two flasks: NATURAL and IMAGINED, PARACELSUS label. {STYLE}"),
    ("invoice-survives", "The city paid musicians. That sentence survives theories.", f"A paid invoice MUSICIANS on top of theory books. {STYLE}"),
    ("not-a-gag", "The dancers are not a gag reel.", f"Ink peeling a GAG sticker off a patient tag, mouth closed. {STYLE}"),
    ("who-owns-floor", "The logistics is who owns the floor.", f"Two floors: MARKET WITH BAND vs CHAPEL, arrows of size. {STYLE}"),
    ("stage-terrible", "A stage is a terrible instrument for contagious fear.", f"A stage shrinking a fear? No: a fear growing on a stage. {STYLE}"),
    ("which-chronicle", "Ask which chronicle, and whether they rented the grain market.", f"A chronicle vs a GRAIN MARKET rental slip. {STYLE}"),
    ("comment-hook", "Would you have hired the musicians. Tell me in the comments.", f"Ink pointing at the viewer, mouth closed, a tiny mute trumpet. {STYLE}"),
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
        title="The Town That Could Not Stop Dancing",
        description=(
            "Strasbourg, fifteen eighteen. Hot blood, a hired band in the grain market, "
            "and a shrine that had to undo the stage."
        ),
        tags=(
            "history",
            "dancing plague",
            "strasbourg",
            "cartoon",
            "true story",
            "1518",
            "saint vitus",
            "alsace",
            "funny",
            "medicine",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="DANCE IT OUT",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Town That Could Not Stop Dancing",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-dance.json"
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

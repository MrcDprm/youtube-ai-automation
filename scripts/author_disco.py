"""Author Drawn Anyway episode 11: Disco Demolition Night, Chicago, nineteen seventy nine."""

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
    """A baseball game once lost to a crate of vinyl in center field. That is not a metaphor, and it is not a culture-war cartoon you invented after a trivia night. On Thursday the twelfth of July nineteen seventy nine, at Comiskey Park on the South Side of Chicago, the Chicago White Sox hosted the Detroit Tigers in a twi-night doubleheader. Anyone who brought a disco record could walk in for ninety eight cents, because WLUP sat at ninety seven point nine on the dial. Between games, a crate in center field was supposed to explode, the crowd was supposed to clap, and game two was supposed to start. Keep that picture. Owner Bill Veeck. Promotions director Mike Veeck, his son. Radio man Steve Dahl. Official hope: about twenty thousand people. Official plan: a box, a bang, then baseball. Everything after this is just that picture hiring a forfeit stamp.""",
    """Start with why a radio man thought a ballpark was a booth. On Christmas Eve nineteen seventy eight, Steve Dahl was fired from WDAI when the station switched from rock to disco. He was twenty four. Rival album-rock station WLUP hired him. He mocked the old slogan Disco DAI as Disco DIE, and he built a listener club with a joke name, the Insane Coho Lips. His partner on air was Garry Meier. The slogan on the banners would be Disco Sucks. Treat that as a radio product, not a moral you have to salute. Disco itself had gone huge after Saturday Night Fever in nineteen seventy seven. Stations copied New York's WKTU. In Chicago, a rock DJ who had just lost a job to a format change now had a crate, a frequency, and a grudge that sold tickets. Early in seventy nine, a WLUP man told Mike Veeck that Dahl already wanted to blow up records live from a shopping mall. The park was simply bigger. That is the setup. Not a thesis. A venue upgrade.""",
    """Bill Veeck had been selling baseball as a circus since the nineteen forties. You can draw more people, he said, with a losing team plus bread and circuses than with a losing team and a long still silence. Mike was promotions director. A White Sox versus Tigers game rained out on the second of May had been stacked onto Thursday the twelfth of July as a twi-night doubleheader. Teen night was already on the calendar, half price. Then they stacked vinyl. WLUP was ninety seven point nine, so the ticket joke was ninety eight cents with a disco record. Dahl would destroy the collected vinyl between games. The club hoped for twenty thousand, about five thousand more than a dull night. They hired security for thirty five thousand. Comiskey seated about forty four thousand four hundred ninety two. The night before, fifteen thousand five hundred twenty had shown up. The White Sox went in at forty wins and forty six losses. The official idea was: this will be loud, and then we will play.""",
    """Bill Veeck checked himself out of hospital tests because he was worried the promotion would become a disaster. His fear arrived on foot. The doubleheader sold out. At least twenty thousand people were still outside. Some leapt turnstiles, climbed fences, came through windows. Official attendance was forty seven thousand seven hundred ninety five. Bill later said fifty to fifty five thousand were inside, the biggest crowd of his second stint as owner. Chicago police closed off-ramps from the Dan Ryan Expressway near the park. The collection box was about four feet by six by five. Once it overflowed, records went to seats. First pitch was due at six in the evening, Central Daylight Time. Lorelei, a WLUP public-appearance model that summer, threw it. As game one started, Mike got word thousands were still trying to enter without tickets. He sent security to the gates. That left the grass thin. Uncollected LPs started flying from the stands like discs. Tigers designated hitter Rusty Staub said they sliced the air and stuck in the dirt. He told teammates to wear batting helmets. The game stopped several times. Detroit won it, four to one. Pat Underwood got the win. Fred Howard took the loss.""",
    """At eight forty, Dahl came onto the field in army fatigues and a helmet, with Meier and Lorelei, circling in a Jeep toward center field. Ken Kravec, booked to start game two, was already warming up. Dahl told the crowd this was now officially the world's largest anti-disco rally, and that the giant box of records would be blown up real good. He set off the explosives. The vinyl went. So did a hole in the outfield grass. File the boom as a cartoon bang, not a war reel. With most of the guards still at the gates, the first of five thousand to seven thousand people came over the wall. Kravec left the mound and joined a barricaded clubhouse. Some climbed foul poles. Some set records on fire. The batting cage was wrecked. The bases were pulled up and stolen. Bill Veeck stood near where home plate had been and asked people to go back. Harry Caray tried the public address. The scoreboard flashed please return to your seats. They played Take Me Out to the Ball Game. It did not work. Security had padlocked all but one gate, trying to keep the outside from becoming the inside.""",
    """Here is the leftover fact, and it is not that disco died in a crater. At nine oh eight, Chicago police in riot gear arrived. The people on the grass left. Thirty nine were arrested for disorderly conduct. Estimates of injuries run from none to over thirty. Nobody died. Veeck wanted game two once the dirt was raked. Crew chief Dave Phillips said the field was still unplayable after groundskeepers spent an hour on debris. Tigers manager Sparky Anderson would not send his club out. He argued a game is postponed for an act of God, and a home team owes a playable field. Phillips called American League president Lee MacPhail, who postponed the second game to Sunday. Anderson wanted a forfeit. The next day MacPhail gave him one, nine to nothing, and said the White Sox had failed to provide acceptable playing conditions. It remains the last American League forfeit. The crate did what it was hired to do. The second game did not.""",
    """Rehook, because the internet likes a night disco died. Dahl said later disco was probably already on its way out, and that the night may have hurried it. Record companies started calling the same songs dance music. Dave Marsh in Rolling Stone called the crowd a paranoid fantasy about where rock radio could lead. Nile Rodgers likened the pile of vinyl to a book burning. Gloria Gaynor said she believed it was an economic idea dressed as a crowd. Dahl has spent decades saying it was not racist and not homophobic, that it was a romp later reframed. File the argument. Do not pretend there was no argument. Also do not let the argument steal the receipt. Mike Veeck stayed with the club into late nineteen eighty, then left baseball for years and said he had been blackballed. He later said that when the first person came down the outfield wall, he knew that life was over. Bill sold the team in nineteen eighty one. The promotion sold tickets. It also sold a forfeit.""",
    """None of this is a cartoon of fifty thousand teenagers as a punchline, and none of it is a hymn to Disco Sucks. They had a radio frequency that became a price. They had a box four by six by five that did not scale. They had security counted for thirty five thousand and a park that printed forty seven thousand seven hundred ninety five, plus whoever came through the windows. They put the guards at the gates because the outside was still trying to become the inside, which is how the grass lost its guards. The chemistry is cheap tickets plus vinyl plus a crater in center field. The logistics is who you staff for. When you staff the turnstiles, the crate is unsupervised. When the crate goes bang, the second game is a field condition. You are allowed to laugh at ninety eight cents. You are not required to laugh at a batting cage, or to pretend a forfeit is a culture thesis that arrived with a Jeep. White Sox pitcher Rich Wortham said it would not have happened on country and western night. File the quote. The field still had a hole.""",
    """So who won. Not the crate. Not the Jeep. Not the slogan on the banners. Detroit won game one, four to one, and was handed game two in the morning. Sparky Anderson won a rulebook argument. Lee MacPhail won a nine to nothing line in the standings. Harry Caray won a public address that nobody obeyed. Dahl won a headline he is still answering. Mike Veeck won a story he has spent a career retelling, and a decade out of the sport. Bill Veeck won the biggest crowd of that second run, and a forfeit. If you need a moral, skip never book a radio man. Take this: a crate is a terrible instrument for a doubleheader, and a doubleheader is a terrible neighbour for a radio army you cannot count at the gate. The next time someone tells you they blew up disco, ask whose security was at the gates, and whose second game got a stamp. Would you have stacked a crate of vinyl on a baseball field for ninety eight cents. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no injuries closeup, no sexualized figures, no riot-porn. "
    "Explosion shown as a comic BOOM with vinyl shards, not fireballs of people. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("crate-ate-game", "A crate of vinyl ate a baseball game.", f"Cartoon title beat: a giant wooden crate of vinyl records sitting on a baseball diamond, a tiny FORFEIT stamp falling. Cream paper. Comic, not gore. {STYLE}"),
    ("not-sermon", "Not a metaphor. Not a culture-war sermon.", f"Ink shaking his head at a CULTURE WAR stamp with a red X, mouth closed. {STYLE}"),
    ("july-12-1979", "July 12, 1979, Comiskey Park, Chicago South Side.", f"Calendar July 12 1979, a cartoon brick ballpark, no flags. {STYLE}"),
    ("doubleheader", "Twi-night doubleheader: White Sox vs Detroit Tigers.", f"Two stacked tickets GAME 1 GAME 2, generic baseball caps, no photoreal players. {STYLE}"),
    ("ninety-eight-cents", "98 cents if you brought a disco record. WLUP 97.9.", f"A huge 98 CENTS ticket next to a vinyl disc and a radio dial 97.9. {STYLE}"),
    ("named-people", "Bill Veeck, Mike Veeck, Steve Dahl. Named by 0:40.", f"Three cartoon nameplates BILL MIKE STEVE, no photoreal faces, a tiny park. {STYLE}"),
    ("hoped-twenty", "Official hope: about 20,000 people. Then baseball.", f"A hopeful crowd meter at 20000, a baseball waiting. {STYLE}"),
    ("crate-center", "Between games: blow up a crate in center field.", f"A crate in center field with a comic fuse, CENTER FIELD sign. {STYLE}"),
    ("christmas-eve", "Dahl fired Christmas Eve 1978 when WDAI went disco.", f"A Christmas Eve 1978 pink slip, radio tower DISCO, no portrait. {STYLE}"),
    ("wlup-hired", "WLUP hired him. Disco DAI mocked as Disco DIE.", f"Two slogan cards DISCO DAI vs DISCO DIE, a radio mic. {STYLE}"),
    ("coho-lips", "Insane Coho Lips. A listener club with a joke name.", f"A silly fish-lips club badge INSANE COHO LIPS, cartoon not army. {STYLE}"),
    ("meier-slogan", "Garry Meier on air. Disco Sucks as a radio product.", f"Two mics, a DISCO SUCKS bumper sticker as a product not a hymn. {STYLE}"),
    ("saturday-night", "Disco went huge after Saturday Night Fever, 1977.", f"A 1977 movie marquee SATURDAY NIGHT FEVER, vinyl flying, no photoreal Travolta. {STYLE}"),
    ("mall-to-park", "He already wanted a mall crate. The park was bigger.", f"A tiny mall crate next to a huge ballpark crate, UPGRADE arrow. {STYLE}"),
    ("bread-circuses", "Veeck: losing team plus bread and circuses.", f"A circus tent on a baseball field, BREAD AND CIRCUSES banner. No flags. {STYLE}"),
    ("rainout-may2", "May 2 rainout stacked onto July 12 as game two.", f"A raincloud MAY 2 dumping a ticket onto JULY 12. {STYLE}"),
    ("teen-night", "Teen night already half price. Then they stacked vinyl.", f"A TEEN NIGHT half-price stub under a stack of records. {STYLE}"),
    ("security-35k", "Hoped 20,000. Hired security for 35,000.", f"Two clipboards 20000 HOPE and 35000 SECURITY. {STYLE}"),
    ("capacity", "Comiskey seated about 44,492.", f"A stadium seating chart labeled 44492. {STYLE}"),
    ("previous-night", "Night before: 15,520 in the park.", f"A sparse cartoon crowd 15520, empty seats. {STYLE}"),
    ("sox-record", "White Sox went in 40-46.", f"A standings card 40-46, not a lecture. {STYLE}"),
    ("loud-then-play", "Official idea: this will be loud, then we play.", f"A two-step recipe LOUD then PLAY, Ink nodding, mouth closed. {STYLE}"),
    ("hospital-out", "Bill checked out of hospital tests. He was worried.", f"A hospital gown on a hook, a worried owner silhouette walking to the park, no photoreal. {STYLE}"),
    ("sold-out", "Sold out. At least 20,000 still outside.", f"A SOLD OUT stamp, a crowd outside a brick wall. {STYLE}"),
    ("windows-fences", "Turnstiles, fences, windows. Extra people inside.", f"Cartoon figures climbing a fence and a window, comic not riot-porn. {STYLE}"),
    ("official-47795", "Official attendance 47,795. Veeck said 50-55 thousand.", f"A ticket counter 47795 vs a handwritten 50-55K. {STYLE}"),
    ("dan-ryan", "Police closed Dan Ryan ramps near the park.", f"A highway off-ramp with a CLOSED cone, park in the distance. {STYLE}"),
    ("box-size", "Collection box about 4 by 6 by 5 feet. It overflowed.", f"A wooden box 4x6x5 overflowing with vinyl. {STYLE}"),
    ("seats-vinyl", "Extra records went to seats, not the crate.", f"Vinyl discs stacked on bleacher seats. {STYLE}"),
    ("six-pm", "First pitch 6:00 pm CDT.", f"A stadium clock 6:00 CDT, a baseball on the mound. {STYLE}"),
    ("lorelei-pitch", "Lorelei threw the first pitch. Then baseball tried.", f"A cartoon first-pitch silhouette, modest clothing, no sexualizing, a baseball in air. {STYLE}"),
    ("security-gates", "Mike sent security to the gates. Field left thin.", f"Guards clustered at GATES, the grass empty of guards. {STYLE}"),
    ("frisbee-lps", "Uncollected LPs thrown like flying discs.", f"Vinyl records flying like frisbees onto cartoon grass. Not gore. {STYLE}"),
    ("staub-helmets", "Rusty Staub: wear batting helmets. Vinyl can slice.", f"A batting helmet beside a vinyl disc stuck in dirt, HELMETS sign. No photoreal. {STYLE}"),
    ("tigers-4-1", "Detroit won game one 4-1. Underwood, Howard.", f"A scoreboard TIGERS 4 SOX 1, names UNDERWOOD HOWARD. {STYLE}"),
    ("eight-forty", "8:40: Dahl in a helmet, a Jeep, center field.", f"A cartoon Jeep in center field, helmet, no photoreal face, 8:40. {STYLE}"),
    ("worlds-largest", "He called it the world's largest anti-disco rally.", f"A megaphone WORLD'S LARGEST ANTI-DISCO RALLY. {STYLE}"),
    ("boom-crater", "Explosion. Comic BOOM. A hole in the outfield grass.", f"Giant comic BOOM letters, vinyl shards, a grass crater, nobody hurt on camera. {STYLE}"),
    ("five-to-seven", "Then 5,000 to 7,000 people on the grass.", f"Tiny cartoon crowd pouring onto a diamond, 5000-7000 tag, not riot-porn. {STYLE}"),
    ("kravec-runs", "Ken Kravec left the mound. Clubhouse barricade.", f"A pitcher running toward a CLUBHOUSE door, mound empty. {STYLE}"),
    ("batting-cage", "Batting cage wrecked. Bases stolen. Cartoon mess.", f"A bent batting cage, bases walking away with little legs, comic. {STYLE}"),
    ("caray-pa", "Harry Caray on the PA. Scoreboard: please return to seats.", f"A PA mic and scoreboard PLEASE RETURN TO YOUR SEATS. No photoreal. {STYLE}"),
    ("padlocked", "Security padlocked all but one gate.", f"A chain and padlock on stadium gates, one small EXIT. {STYLE}"),
    ("nine-oh-eight", "9:08: police. Crowd left the grass.", f"A clock 9:08, cartoon police hats, people walking off grass, no violence. {STYLE}"),
    ("thirty-nine", "39 arrests, disorderly conduct. Nobody died.", f"A respectful tally 39 ARRESTS, 0 DEATHS. {STYLE}"),
    ("phillips-unplayable", "Dave Phillips: field still unplayable after an hour.", f"A rake, a crater, UNPLAYABLE stamp, clock one hour. {STYLE}"),
    ("sparky-forfeit", "Sparky Anderson: forfeit. Home team owes a field.", f"A rulebook and FORFEIT stamp, manager cap, no portrait. {STYLE}"),
    ("macphail", "Lee MacPhail next day: forfeit 9-0. Last AL forfeit.", f"A morning newspaper FORFEIT 9-0, LAST AL FORFEIT. {STYLE}"),
    ("leftover-gates", "Leftover fact: security was at the gates. Crate in center.", f"Split panel GATES full of guards, CENTER FIELD crate alone. {STYLE}"),
    ("mike-next-job", "Mike Veeck: first person down the wall, life over.", f"A tiny figure on an outfield wall, a NEXT JOB thought bubble, no photoreal. {STYLE}"),
    ("disco-debate", "Later argument: radio stunt vs prejudice. File both.", f"Two folders STUNT and PREJUDICE, a FILE BOTH stamp. Ink serious, mouth closed. {STYLE}"),
    ("not-a-mob-gag", "Not a cartoon of fans as a punchline. The plan undercounted radio.", f"Ink peeling a MOB GAG sticker off a ticket stub, mouth closed. {STYLE}"),
    ("ninety-eight-receipt", "98 cents bought a crowd the gates could not meter.", f"A 98 CENTS coin crushing a turnstile, comic. {STYLE}"),
    ("comment-hook", "Would you have stacked a crate on a baseball field. Tell me in the comments.", f"Ink pointing at the viewer, mouth closed, a tiny crate on a diamond. {STYLE}"),
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
        title="The Night They Blew Up Disco",
        description=(
            "Chicago, nineteen seventy nine. Ninety eight cents, a crate in center field, "
            "and a doubleheader that hired a forfeit."
        ),
        tags=(
            "history",
            "disco demolition",
            "comiskey park",
            "cartoon",
            "true story",
            "1979",
            "white sox",
            "steve dahl",
            "funny",
            "baseball",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="ATE GAME TWO",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Night They Blew Up Disco",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-disco.json"
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

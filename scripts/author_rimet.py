"""Author Drawn Anyway episode 23: Jules Rimet trophy theft, nineteen sixty six."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 630.0
MINUTES = 9
VOICE = "en-AU-WilliamNeural"
RATE = "+4%"

CHAPTERS = [
    """A black-and-white dog named Pickles found the World Cup under a hedge, wrapped in newspaper and tied with string. That is not a metaphor, and it is not a cartoon you invented after a trivia night about a collie who saved football. On the twentieth of March nineteen sixty six, a Sunday, somebody took the Jules Rimet Trophy out of a locked glass case at Methodist Central Hall in Westminster, while the guards were on coffee and a lavatory break. The stamps in the same building were valued at about three million pounds. The cup's official metal value was about three thousand. Keep that split. Then put a red X on the joke that this was a genius heist movie. The leftover is not Ocean's Eleven. The leftover is a padlock, a wooden bar, and a parcel in Beulah Hill.""",
    """Start with why a stamp show was supposed to be the safe plan. The Football Association had the silver-gilt trophy from January, parked at Lancaster Gate, and loaned it out for publicity by the hour. The cup itself had been made in nineteen thirty, gold plate over silver, a lapis base. During the last war, FIFA vice-president Ottorino Barassi hid Italy's winning trophy in a shoebox under a bed. That is the older costume: a World Cup as something you can lose in a bedroom. In late February, Stanley Gibbons asked to put it in Stampex, their Sport with Stamps exhibition at Central Hall. Sir Stanley Rous, president of FIFA, set conditions: a reputable security firm, a locked glass case, a guard day and night, insurance at thirty thousand pounds even though the official valuation was three thousand. The stamps next to it were valued at about three million. Rous treated the cup as cheap silver. Central Hall sits yards from the Houses of Parliament and close to New Scotland Yard. Stampex opened on Saturday the nineteenth of March. Extra guards stood by the cabinet while the public was in, eight in the morning to eight at night. After hours, that extra body went home, which already broke Rous's around-the-clock line. On Sundays the hall ran Methodist services. The official idea was: nobody steals the cheaper thing in a room full of stamps.""",
    """File the Sunday, because the cabinet does not start as a mystery. Two uniformed officers were meant to cover the trophy around the clock, with two plainclothes in the daytime, and Atherton files four uniformed on two floors plus extras when the doors were open. On the twentieth, exhibition rooms were closed; church doors were open; corridors were public. A guard checked doors at nine. About nine thirty, two maintenance men opened the front and were escorted through the Stampex rooms to clean. They saw the trophy in the case and later said they locked the back doors when they left. Police interviewed them. They were not treated as the job. Guards checked the cup at eleven. Then the first-floor pair sat in the office with coffee while about two hundred people sat in a service below. Frank Hudson left around eleven twenty five for the toilet and saw a man by the public telephone. Minutes later the man was still there, using it. Public corridor. No alarm in his head. At about twelve ten the next circuit found the case forced and the cup gone. The rear doors' wooden bar was on the floor; screws and bolts that held the mounts had been taken from the outside. A padlock had been taken off the back of the glass case. None of the guards had heard a thing. Scotland Yard gave it to the Flying Squad. A churchgoer, Mrs Coombes, described a man. Hudson's man did not match. Two descriptions. The papers got a third. That is not a mastermind. That is a door that unbolted.""",
    """Here is the leftover the films file as a ransom thriller. On Monday the twenty first, Joe Mears, chairman of the Football Association and of Chelsea, got a call: a parcel would arrive at the club, of interest, follow the instructions. It went to his home. Inside: the removable lining from the top of the trophy, and a demand for fifteen thousand pounds. Place an ad in the Evening News personal column: Willing to do business. Joe. Get the cup back by Friday, or it is one for the pot. Do not tell the police. A man calling himself Jackson then changed the notes to fives and tens. Mears told Detective Inspector Charles Buggy of the Flying Squad anyway. The bank packed a suitcase with paper, real notes only on the ends. Mears had an angina attack. His wife handed the phone to an assistant named McPhee, who was Buggy. Jackson agreed to meet at the gates of Battersea Park. He checked the suitcase and did not notice the paper. He got in the car to fetch the cup. Then he spotted what he called a funny old van, the Flying Squad kind with bars on the windows. At Kennington he jumped from the moving car. Buggy caught him in a back garden. At the station Jackson was Edward Betchley, mid-forties, Camberwell, a dealer, one prior conviction. He said he had not stolen it. He named a customer he called only The Pole, five hundred pounds to be the middleman. Mrs Coombes picked him in a lineup. Hudson picked someone else. File both. Do not draw a cartoon villain with a monocle.""",
    """The cup was still missing. On the evening of Sunday the twenty seventh, David Corbett, twenty six, a Thames lighterman, left fifty Beulah Hill in Upper Norwood to make a phone call and took Pickles for the walk. Pickles sniffed a parcel under the hedge by a parked car, newspaper, string. Corbett tore it open and did not know what he had until he saw the winners' names on the base. He took it to Gipsy Hill police station. They moved him and the metal to Cannon Row. Harold Mayes of the World Cup committee said it was genuine. Police held Corbett as a possible thief until his alibi for the twentieth cleared. They announced the find the next morning and kept the trophy as evidence until the eighteenth of April, then gave it back to the FA, ten weeks before kickoff. History Today later interviewed Corbett and filed the walk at about nine at night. That is a hedge, not a sting. Betchley did not dump it while running in Kennington; Beulah Hill is over six miles from St Agnes Place. Atherton's leftover: someone else panicking after the arrest is likelier than a film chase.""",
    """Rehook, because the internet likes one dog and a heist. Put a red X on skipping the padlock. The Football Association, before the story even went fully public, sent secretary Denis Follows to silversmith George Bird in Fenchurch Street and asked for a replica, keep your mouth shut. Very few people, including Rous, knew. After England won four to two at Wembley, the replica did the public work, including a Blue Peter appearance with Pickles; the original sat under lock, later a bank vault in one later officer's account, until it went to the next hosts. Betchley went to trial in July. Police called him an astute criminal; he had one prior, six months in nineteen fifty four, army, docks, then fancy goods to street traders, County Court debts. He was convicted of demanding money with menaces with intent to steal, two years concurrent. He was not convicted of stealing the cup. Justice Lyell did not buy the five-hundred-pound errand and said no other supposition made sense except a larger share of the fifteen thousand. Betchley died of emphysema in nineteen sixty nine. The Pole never sat in the dock. A journalist in twenty eighteen named Sidney Cugullere; that is a byline, not a verdict. File the claim. Do not spend it as a closed case. A statue of a dog is a costume for a cabinet that lost its padlock. A stamp exhibition is a costume for a thirty-thousand-pound insurance line.""",
    """File the leftover metal, because March was not a finale. Pickles got a silver medal from the National Canine Defence League and a week of television. Corbett got rewards later counted at about five thousand pounds in one BBC file and about six thousand in History Today, six times an England player's World Cup bonus in the six-thousand version. The FA did not send a thank-you letter; Corbett and Pickles did go to the players' dinner. Bobby Charlton's wife made a fuss of the dog. In nineteen seventy Brazil kept the original after a third win, Jules Rimet's old rule. In nineteen eighty three it was stolen from the Brazilian Football Confederation and never recovered; people say it was melted. File the rumor as a rumor. The Bird replica later went to auction; FIFA bought it in nineteen ninety seven; it sits in the National Football Museum in Manchester. A hedge in Norwood is a costume for a cup that would later vanish for good. A collie is a costume for a security plan that treated three thousand pounds of gilt as the object nobody would bother to take.""",
    """None of this is a hymn to a clever dog, and none of it is a cartoon of a criminal mastermind in gloves. They had a Methodist hall on a Sunday. They had coffee in an office. They had a wooden bar whose bolts faced the alley. You are allowed to laugh at a fifteen-thousand-pound suitcase stuffed with paper, and at a funny old van that kept reappearing, and at a World Cup that spent a week under a hedge. You are not required to laugh at Mears in bed with angina, or at Hudson walking past a telephone, or at Corbett being treated as a thief for handing the thing in. The official idea was: the stamps are the treasure, so the cup is safe. The street idea was: a dog found the World Cup. The leftover idea is: a padlock on the back of a glass case, and a replica already on order while the original was still missing.""",
    """So who won. Not the stamps. Not The Pole, who never had to answer a charge. Not the funny old van. Hudson won a telephone he could not explain. Buggy won an arrest without a cup. Betchley won two years for the note, not the case. Corbett won a house later, and a morning at Cannon Row as a suspect. Pickles won a medal and a dinner. George Bird won a secret copy that outlived the original. Nome had a relay. This had a hedge. If you need a moral, skip dogs are heroes. Take this: a last-mile collie is a terrible whole story, and a padlock is a terrible honest one. The next time someone tells you Pickles saved the World Cup, ask who unscrewed the door bar, and whether the replica was already being made when the dog sniffed the paper. Would you have given the statue to the dog, or to the lock. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no cruelty, no child-victim closeups, not mud-green archive night, "
    "not After Hours File dark. Trophy theft shown as a candy gold cup, a padlock, a newspaper parcel, "
    "a cartoon black-and-white dog not photoreal, a glass case, not a heist movie, not guns, not melting "
    "people, not a stadium riot. Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, oversized "
    "black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("hedge-parcel", "Pickles found the World Cup under a hedge, newspaper and string.", f"A candy newspaper parcel under a hedge, string, a tiny gold cup peeking. Cream paper. {STYLE}"),
    ("not-trivia", "Not a collie-saved-football trivia gag.", f"Ink shaking his head at a DOG SAVED FOOTBALL stamp with a red X, mouth closed. {STYLE}"),
    ("central-hall", "20 March 1966, Sunday, Methodist Central Hall, Westminster.", f"A building tag CENTRAL HALL, date 20 MAR 1966, SUNDAY. No flag as joke. {STYLE}"),
    ("stamps-vs-cup", "Stamps about £3 million. Cup official metal about £3,000.", f"A split price STAMPS 3M vs CUP 3K. {STYLE}"),
    ("x-heist-film", "Put a red X on the genius heist-movie joke.", f"An OCEANS ELEVEN clapboard with a giant red X. Cute not cruel. {STYLE}"),
    ("leftover-padlock", "Leftover: a padlock, a wooden bar, a parcel in Beulah Hill.", f"A padlock, a wooden door bar, a hedge tag BEULAH HILL. {STYLE}"),
    ("lancaster-gate", "FA had the silver-gilt trophy from January at Lancaster Gate. Older costume: Barassi's shoebox.", f"A crate JULES RIMET, tag LANCASTER GATE, a small SHOEBOX WWII tag. {STYLE}"),
    ("stampex-ask", "Stanley Gibbons asked to put it in Stampex, Sport with Stamps.", f"A poster STAMPEX, SPORT WITH STAMPS, tiny cup in a case. {STYLE}"),
    ("rous-rules", "Rous: security firm, locked glass, guard day and night, insured £30,000.", f"A clipboard ROUS RULES, 30K INSURED, GUARD DAY NIGHT. No portrait. {STYLE}"),
    ("cheap-silver", "Rous treated the cup as cheap silver next to the stamps.", f"A cheap-silver price tag on a candy gold cup, STAMPS bigger. {STYLE}"),
    ("near-yard", "Central Hall: near Parliament, close to New Scotland Yard.", f"A map pin CENTRAL HALL, tags PARLIAMENT and SCOTLAND YARD. No flags. {STYLE}"),
    ("opened-19", "Stampex opened Saturday 19 March. Extra guards 8am-8pm. After hours broke Rous's 24h line.", f"A calendar 19 MAR SAT, OPEN 8-8, AFTER HOURS empty chair. {STYLE}"),
    ("sunday-services", "On Sundays the hall ran Methodist services.", f"A sign SUNDAY SERVICE, exhibition door CLOSED. Not mockery. {STYLE}"),
    ("official-idea", "Official idea: nobody steals the cheaper thing in a room of stamps.", f"A stamp CHEAPER OBJECT SAFE with a tiny cup. {STYLE}"),
    ("two-floors", "Four uniformed guards, two floors. Exhibition closed, church open.", f"A two-floor plan, 4 GUARDS, church doors OPEN. {STYLE}"),
    ("maintenance", "Maintenance men cleaned, saw the trophy, left. Not treated as suspects.", f"A mop and a glass case, tag SAW IT, LEFT. {STYLE}"),
    ("eleven-check", "Guards checked the trophy at 11:00, then coffee in the office.", f"A clock 11:00, two coffee cups, tiny cup still in case. {STYLE}"),
    ("hudson-phone", "Hudson, about 11:25, saw a man by the public telephone.", f"A payphone in a corridor, nameplate HUDSON, 11:25. No portrait. {STYLE}"),
    ("twelve-ten", "About 12:10: case forced, cup gone.", f"An empty glass case, clock 12:10, GONE stamp. {STYLE}"),
    ("door-bar", "Wooden bar on the floor; mounts unscrewed from outside.", f"A wooden bar on the floor, screws tagged FROM OUTSIDE. {STYLE}"),
    ("padlock-off", "A padlock taken off the back of the glass case.", f"A dangling padlock OFF the back of a candy glass case. {STYLE}"),
    ("two-descriptions", "Mrs Coombes described a man. Hudson's man did not match.", f"Two mismatched silhouette cards COOMBES vs HUDSON. No photoreal faces. {STYLE}"),
    ("flying-squad", "Scotland Yard gave it to the Flying Squad.", f"A folder FLYING SQUAD, Central Hall tag. {STYLE}"),
    ("mears-call", "21 March: Joe Mears got a call. Parcel of interest. Follow instructions.", f"A phone and a note PARCEL TOMORROW, nameplate MEARS. No portrait. {STYLE}"),
    ("lining-note", "Parcel: removable lining plus £15,000 demand. One for the pot.", f"A trophy lining piece, ransom card 15000, ONE FOR THE POT. Not gore. {STYLE}"),
    ("evening-news", "Ad in Evening News: Willing to do business. Joe.", f"A newspaper personal ad WILLING TO DO BUSINESS JOE. {STYLE}"),
    ("jackson-notes", "Jackson changed the notes to fives and tens.", f"A cash tag 5s AND 10s, name JACKSON. {STYLE}"),
    ("paper-suitcase", "Bank packed a suitcase with paper, real notes only on the ends.", f"A suitcase of paper bundles, real notes on the ends only. {STYLE}"),
    ("mcphee-buggy", "Mears ill. Assistant McPhee was DI Charles Buggy.", f"A nameplate MCPHEE with a small badge BUGGY underneath. {STYLE}"),
    ("battersea-gate", "Meet at the gates of Battersea Park. Jackson checked the case, missed the paper.", f"Park gates BATTERSEA, a suitcase, MISSED THE PAPER. {STYLE}"),
    ("funny-van", "Jackson spotted a funny old van, Flying Squad bars on the windows.", f"A boxy van FUNNY OLD VAN, barred rear windows. Cute not grim. {STYLE}"),
    ("kennington-jump", "Kennington: Jackson jumped from the moving car. Caught in a garden.", f"A car, a jump arrow KENNINGTON, a garden fence. No violence. {STYLE}"),
    ("betchley-id", "Jackson was Edward Betchley, Camberwell dealer. Named only The Pole.", f"A card BETCHLEY, a blank card THE POLE. No photoreal. {STYLE}"),
    ("lineup-split", "Coombes picked him. Hudson picked someone else. File both.", f"A lineup of candy silhouettes, tick and X, FILE BOTH. {STYLE}"),
    ("corbett-walk", "27 March evening: Corbett, 26, Thames lighterman, 50 Beulah Hill, Pickles.", f"A house number 50 BEULAH HILL, dog leash, date 27 MAR. Cartoon dog. {STYLE}"),
    ("winners-base", "Corbett saw the winners' names on the base and knew.", f"The cup base with tiny winner plaques, a lightbulb tag NAMES. {STYLE}"),
    ("gipsy-hill", "Handed in at Gipsy Hill, then Cannon Row. Mayes said genuine.", f"A police desk GIPSY HILL, stamp GENUINE, MAYES. {STYLE}"),
    ("alibi-clear", "Corbett held as a possible thief until his alibi for the 20th cleared.", f"A SUSPECT stamp peeling off Corbett's nameplate, ALIBI OK. {STYLE}"),
    ("april-18", "Police kept it as evidence until 18 April, then back to the FA.", f"A calendar 18 APR, RETURN TO FA, 10 WEEKS TO KICKOFF. {STYLE}"),
    ("six-miles", "Beulah Hill is over six miles from Kennington. Not dumped in the chase.", f"A ruler 6+ MILES, KENNINGTON vs BEULAH HILL. {STYLE}"),
    ("x-skip-lock", "Rehook: red X on skipping the padlock for one dog.", f"Ink peeling a SKIP THE PADLOCK sticker, mouth closed. {STYLE}"),
    ("bird-replica", "Denis Follows asked George Bird for a replica. Keep your mouth shut.", f"A silversmith bench, two cups ORIGINAL vs COPY, tag BIRD. {STYLE}"),
    ("two-years", "Betchley: two years for the demand, not convicted of stealing the cup.", f"A court stamp 2 YEARS, NOT THEFT. {STYLE}"),
    ("pole-byline", "The Pole never sat in the dock. A 2018 byline is not a verdict.", f"An empty chair THE POLE, a newspaper 2018, NOT A VERDICT. {STYLE}"),
    ("pickles-medal", "Pickles: National Canine Defence League silver medal, TV week.", f"A cartoon dog with a silver medal NCDL. Not photoreal. {STYLE}"),
    ("five-or-six", "Corbett rewards: about £5,000 in one file, about £6,000 in another.", f"A ledger 5K-6K, FILE THE RANGE. {STYLE}"),
    ("brazil-1983", "Original to Brazil 1970; stolen 1983, never recovered. Melted is a rumor.", f"An empty pedestal 1983, tag NEVER RECOVERED, rumor MELTED in small type. {STYLE}"),
    ("museum-copy", "FIFA bought the Bird replica in 1997. National Football Museum, Manchester.", f"A museum case MANCHESTER, tag REPLICA 1997. {STYLE}"),
    ("coffee-office", "A Methodist hall on a Sunday. Coffee in an office. Bolts facing the alley.", f"Coffee cups, a hall, bolts tagged ALLEY SIDE. {STYLE}"),
    ("who-won-hedge", "Not the stamps. A hedge in Norwood held the cup for a week.", f"A hedge beating a pile of stamps, tag HELD A WEEK. {STYLE}"),
    ("replica-already", "A replica was already on order while the original was still missing.", f"An order slip REPLICA while a missing-cup poster hangs. {STYLE}"),
    ("ask-the-bar", "Ask who unscrewed the door bar, and whether the copy was already being made.", f"A question mark over a wooden bar and a silversmith order. {STYLE}"),
    ("dog-or-lock", "Would you have given the statue to the dog, or to the lock.", f"Split: a cartoon dog medal vs a giant padlock, a question mark. {STYLE}"),
    ("receipt", "A padlock lost the cup. A hedge found it. Drawn anyway.", f"A receipt card PADLOCK vs HEDGE, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Trophy That Vanished in a Bag",
        description=(
            "England, nineteen sixty six. A padlock, a stamp show, and a dog "
            "who found the World Cup under a hedge."
        ),
        tags=(
            "history",
            "1966",
            "world cup",
            "jules rimet",
            "pickles",
            "cartoon",
            "true story",
            "logistics",
            "london",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="A DOG FOUND IT",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Trophy That Vanished in a Bag",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-rimet.json"
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

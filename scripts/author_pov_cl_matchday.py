"""Author Every Level POV ep2: Your Life on a Champions League Matchday."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, pov_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_pov_scenario, write_scenario
from scripts.pov_pacing import EPISODE_CHAPTER_ENERGY, beat_covers

TERMS = ("cartoon pov illustration", "football rank cartoon")
TARGET_SECONDS = 840.0
MINUTES = 14
PROJECT_ID = "your-life-on-a-champions-league-matchday-14dk-20260902"
EPISODE_KEY = "cl-matchday"
VOICE = "en-US-ChristopherNeural"
RATE = "+5%"
ZOOM = 1.20
SCENE_GAP = 0.22

STYLE = (
    "Bold cartoon POV, thick ink outlines, flat fills of pitch green, stadium amber, cream paper, "
    "tomato red accents, slight paper grain, non-photorealistic, illustrated, first-person football "
    "matchday story, not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, "
    "no photoreal faces, no UEFA logos, no real club crests, no national flags as identity, no child closeups. "
    "Recurring protagonist Kit: young adult, green hoodie or generic match kit, short dark hair, mouth closed."
)

CHAPTERS = [
    """Matchday does not start at kickoff. Matchday starts when your alarm wins an argument you lost at midnight. You are not a hero yet. You are a person who needs tape, carbs, and a seat on a bus that smells like laundry and nerves. This is your life on a Champions League matchday, and if you think the tunnel is the beginning, you have skipped the part that breaks people. By full time you will understand that the loudest moment is sometimes the quietest hour before breakfast. Stay. Phase one is not glamour. Phase one is finding your left boot.""",
    """Phase one. Five forty-five in the morning. Phone on the nightstand like a referee you cannot argue with. You check the weather in a city you fly to later, even though you will play indoors under lights that fake summer. You lay out tape, pre-wrap, and the same lucky socks you pretend not to believe in. Breakfast is not a feast. It is timing. Oats, banana, water, then more water. Your partner sleeps through the ritual. Your house feels normal for six minutes. Then you remember sixty thousand seats and one touch. The day has a schedule now. You are already late in your head.""",
    """Phase two. Team breakfast at the hotel. Long table, short conversations. Nutritionist marks your plate like homework. Someone jokes about eggs and gets the look. You sit near seniors because seating is politics without speeches. Coffee is allowed until it is not. You listen to ankle updates the way civilians listen to weather. A starter is quiet. A sub is too loud. Both are afraid. You sign a clipboard for anti-doping that treats you like a suspect and a saint at once. The bus leaves at nine. You are dressed for travel, not for glory.""",
    """Phase three. The bus. Same seat if you are superstitious. Headphones if you are smart. Window if you want the city to feel far away. The driver knows the route. You do not. Security escort at the training ground gate like you are valuable luggage. You pass fans with phones outside a fence you cannot see through. Training kits today. Then media. Then lunch. Then nothing, which is the hardest session. Waiting is a skill they never put on the whiteboard. You scroll once and put the phone away because the screen makes your heart race faster than sprints.""",
    """Phase four. Arrival at the stadium hours before the public. Concrete ramps, cold air, credential on a lanyard that makes cleaners nod at you like you belong. The dressing room is not cinematic yet. It is hooks, ice tubs, and a smell you cannot describe to friends. Your shirt hangs with your name spelled correctly, which matters more than you admit. Boots go in your cubby, not the floor. Physio asks about a tight hamstring you said was fine yesterday. You say fine again. Fine is a contract word on matchday.""",
    """Phase five. Pre-match meal three hours out. Pasta again. Sauce again. Salt again. You eat like a job because it is. The chef has cooked for musicians and boxers and still looks nervous when the gaffer walks in. You are allowed dessert if you are starting. You are allowed silence if you are not. Tactics on a screen: their left back jumps, their number nine runs channels, their set pieces are tall and angry. You memorize one detail because too many details turn your legs to questions.""",
    """Phase six. Warm-up on the pitch while the stadium is still a skeleton. Ball thumps echo like the building is empty on purpose. You do rondos, stretches, sprints that look easy on television and feel like debt. Cameras appear at the tunnel mouth. You act normal, which means you do not look at the stands. The grass is too green, too short, too perfect, like a lie you agree to play on. You take a photo in your head you will never post. The whistle for warm-up ending is the first whistle that matters.""",
    """Phase seven. Back in the dressing room. Final tape. Final words. The gaffer does not give a movie speech. He gives one instruction repeated until it sticks: press the trap, hit the channel, stay connected. You put on the match shirt and the weight changes. Music loud, then off. Silence is the real anthem. You line up in the corridor. Heart rate climbs without running. Someone spits into a bin like punctuation. You touch the sign above the door on the way out because ritual is how fear gets a uniform.""",
    """Phase eight. The tunnel. Lights at the end like a stage you did not audition for. You hear the crowd before you see grass. The anthem plays and your body remembers every youth game that was not this. Opponents breathe the same air. You stand shoulder to shoulder with people who will tackle you in ten minutes and share water later if the rules allow. The referee waits. The camera sweeps. You walk out and the noise hits your chest before the ball moves. Matchday finally looks like television. It feels like work.""",
    """Phase nine. First half. Time compresses. You hear your name once from the bench area and forget it instantly. One touch too heavy and the whole stadium sighs like a single person. One pass split and you feel tall for half a second. The game is faster because stakes are real. You scan, breathe, scan again. Halftime feels impossible and immediate. You drink without tasting. You are not thinking about glory. You are thinking about the next five meters.""",
    """Phase ten. Half-time. Orange slices and cold towels. Tablet with heat maps you pretend to understand in thirty seconds. The gaffer points at one clip, not ten. Fix this, or we lose the week. You change shirt because sweat has weight. Someone gets an injection for pain with a nod like it is normal. It is normal here. You look at the score and the clock and understand that the second half is a different match with the same bruises.""",
    """Phase eleven. Second half. Legs heavier. Mind sharper if you are lucky. The sub board glows like a verdict. You watch numbers flip and hope yours appears or does not, depending on the lie you tell yourself. Set pieces become architecture. A corner is a courtroom. A free kick is a contract negotiation with gravity. You foul once and apologize to nobody. You win a header and hear your own breath in the noise. Eighty minutes and the game opens a door called panic or belief.""",
    """Phase twelve. Final phase. Full time or extra time if the tie demands it. Whistle blows and the stadium exhales. You shake hands because respect is cheaper than hate. Mixed zone if you scored. Silent bus if you did not. Ice on knees in a plastic tub. Phone floods with messages from people who watched three seconds and send paragraphs. You eat chicken at midnight. You sleep at two. Tomorrow the body reminds you what matchday cost. The highlight reel will skip the morning. You will not.""",
    """So which phase owns you. Alarm phase. Bus phase. Tunnel phase. Halftime tablet phase. Full-time ice phase. Champions League matchday is not one moment. It is a chain of small disciplines that look boring until you miss one. Tell me which hour would break you before kickoff even arrives. Tell me if you thought matchday started when the anthem played. That is the receipt. Rank Run POV.""",
]

_REHOOKS = [
    "Kickoff is a lie on television. Matchday starts when the alarm wins.",
    "Left boot missing. Heart already running. Welcome to phase one.",
    "Eggs are homework. Seating is politics. Nobody is relaxed here.",
    "Bus window world. Your heart races faster than the schedule.",
    "Hooks and ice tubs. History sits on plastic chairs.",
    "Diagrams lie politely. You still chase half a second of space.",
    "Empty stand rehearsal. The grass has to feel real before the roar.",
    "Short words. Long fear. Courage is walking anyway.",
    "Tunnel compresses your whole life into twenty steps.",
    "Amnesia and math. Courage between doubt, every minute.",
    "Orange slices and red zones. Verbs win at halftime.",
    "The board is a lottery you trained for in silence.",
    "Full time is not finished. The body invoices you at midnight.",
    "Comment your weakest hour before the anthem — be honest.",
]

_CHAPTER_EXTRAS = [
    """The broadcast will show you ninety minutes. Your body will invoice you for eighteen hours. That gap is the job. Fans see the roar. They do not see the clipboard, the pasta, the quiet bus, the tape on a carpet at dawn. Matchday is logistics wearing a kit.""",
    """You have done this on bad pitches and good ones. European nights add security, cameras, and a clock that does not care about your sleep. The ritual stays: water, tape, same seat, same silence. Superstition is just anxiety with a uniform.""",
    """Hotel breakfast is where teams pretend they are normal. The nutritionist is the real gaffer until noon. You learn to eat while reading a lineup prediction that is wrong. You learn that silence at table is not peace. It is concentration with toast.""",
    """Travel days shrink the world to a bus window. You pass ordinary streets where matchday is not a religion. That contrast keeps you sane. You arrive at a gate that separates you from the crowd forever, even when the crowd loves you.""",
    """Dressing rooms are churches with laundry. Every hook is a contract. Every ice tub is a confession. You sit where last week's hero sat and pretend history does not weigh on plastic chairs. The shirt goes on and you become a name on a back, not a person with a kitchen at home.""",
    """Tactics meetings turn opponents into diagrams. Diagrams lie politely. Still, you cling to one truth: where the space opens for half a second. That half second is why you woke at five forty-five.""",
    """Warm-up is performance for nobody and everybody. The empty stand watches like a future audience. You touch the grass to convince your brain the pitch is real. Then you run and the brain catches up.""",
    """Final words are short because fear is long. Music hides noise. Silence hides thoughts. You walk the corridor and every step is a decision to stay present. That is matchday courage before the camera finds you.""",
    """The tunnel compresses adulthood into a walk. Lights, anthem, breath, grass. You remember being a kid with a ball in a park. You are still that kid with rent and a GPS vest. The whistle releases you into the only part strangers think is the whole day.""",
    """First half is amnesia and math. Forget the crowd when you touch the ball. Remember the crowd when you lose it. You play intervals of courage between intervals of doubt. That is not weakness. That is professional.""",
    """Halftime is a reset with a clock. Orange slices taste like childhood and obligation. The tablet shows red zones you will fix for one minute and forget for ten. The gaffer speaks in verbs, not poetry. Verbs win.""",
    """Second half is when subs become stories. The board is a lottery you trained for. Set pieces turn tall players into monuments. You run on fumes that look like energy on television. Eighty minutes is where seasons lean.""",
    """After the whistle, matchday is still not finished. Recovery starts in the tunnel. Messages arrive from people who love the score more than the schedule. You eat late, sleep late, pay tomorrow. The body keeps the receipt the broadcast throws away.""",
    """Phases, not highlights. That is the truth matchday sells backwards. Tell me your weakest hour: dawn, bus, wait, tunnel, or midnight ice. That answer is more honest than a goal clip.""",
]

_CHAPTER_EXTRAS_B = [
    """You will rewatch the goal and forget the bus. That is how the sport sells itself. This episode is the bus. The clipboard. The tape that will not stick in humidity. The meal you eat without tasting because your mouth is dry from pretending you are calm.""",
    """The best players look bored at breakfast because boredom is control. You are still learning that face. Matchday morning is acting class with protein.""",
    """Someone always arrives late and the whole table pretends not to count. You arrive early because fear is punctual. Both strategies work until they do not.""",
    """The bus takes the long way on purpose so you do not see the crowd too early. Management calls it focus. You call it delaying the verdict.""",
    """The dressing room television plays without sound. You watch a cooking show and think about nothing. That is also preparation.""",
    """You have eaten this pasta in eleven cities. It tastes like responsibility. You finish anyway because tomorrow's you is already owed.""",
    """A steward asks for an autograph during warm-up and you sign because kindness is faster than explaining you are working. Then you sprint and remember you are working.""",
    """In the corridor you hear the opponent laugh and hate them for being human. Then you remember you will laugh too if you win. Matchday makes everyone temporary villains.""",
    """The anthem ends and grass is suddenly real. All morning was prelude. Now the clock belongs to the referee, not your nutritionist.""",
    """You misplace a pass and the error feels permanent for four seconds. Then the game moves and forgiveness is possible if you sprint back. Matchday rewards repentance with lungs.""",
    """Halftime oranges taste like childhood and obligation. You eat two and think about your dad driving you to youth games in rain. European nights inherit Sunday mornings.""",
    """Your calf tightens at sixty minutes and you tell nobody. You tell the physio at sixty-five when denial stops working. Honesty has a timetable on matchday.""",
    """After full time you sit on the floor and untie boots like they are handcuffs. Victory or loss, the laces take the same time. That equality is strange comfort.""",
    """Comment which phase would break you. Be honest. Dawn is underrated as a villain.""",
]


def _full_chapters() -> list[str]:
    return [
        f"{body} {rehook} {extra} {extra_b}"
        for body, rehook, extra, extra_b in zip(
            CHAPTERS, _REHOOKS, _CHAPTER_EXTRAS, _CHAPTER_EXTRAS_B, strict=True
        )
    ]


_BEAT_TEMPLATES: list[list[tuple[str, str, str]]] = [
    [
        ("not-kickoff", "Matchday does not start at kickoff.", f"Kit alarm ringing, KICKOFF crossed out, MATCHDAY AT DAWN. {STYLE}"),
        ("alarm-wins", "Alarm wins at midnight argument.", f"Kit reaching for phone alarm 5:45 AM, dark room. {STYLE}"),
        ("tape-carbs-bus", "Tape, carbs, bus that smells.", f"Tape roll, banana, team bus smell lines, Kit packing bag. {STYLE}"),
        ("tunnel-not-start", "Tunnel is not the beginning.", f"Tunnel in distance, SKIP arrow to morning routine. {STYLE}"),
        ("quietest-hour", "Quietest hour before breakfast.", f"Kit silent at kitchen table, steam from mug, cream paper. {STYLE}"),
        ("find-left-boot", "Phase one: find your left boot.", f"Kit searching one boot under bed, LEFT BOOT stamp. {STYLE}"),
    ],
    [
        ("phase-one", "Phase one: five forty-five AM.", f"Title PHASE 1, clock 5:45, Kit sitting up. {STYLE}"),
        ("weather-check", "Check weather in another city.", f"Kit phone weather app foreign city, hoodie on. {STYLE}"),
        ("lucky-socks", "Same lucky socks ritual.", f"Kit laying lucky socks next to tape, superstition. {STYLE}"),
        ("oats-banana", "Oats, banana, water timing.", f"Breakfast bowl oats banana water bottles lined up. {STYLE}"),
        ("sixty-thousand", "Sixty thousand seats in your head.", f"Stadium silhouette over quiet kitchen, Kit staring. {STYLE}"),
        ("already-late", "Already late in your head.", f"Kit rushing checklist, LATE IN HEAD stamp. {STYLE}"),
    ],
    [
        ("phase-two", "Phase two: team breakfast.", f"Title PHASE 2, hotel breakfast table long. {STYLE}"),
        ("nutritionist-plate", "Nutritionist marks your plate.", f"Plate with check marks, nutritionist clipboard, Kit eating. {STYLE}"),
        ("seating-politics", "Seating is politics.", f"Kit choosing seat near seniors, empty chairs politics. {STYLE}"),
        ("ankle-updates", "Listen to ankle updates.", f"Teammates whisper ankle icons, Kit listening. {STYLE}"),
        ("doping-clipboard", "Anti-doping clipboard.", f"Kit signing clipboard ANTI-DOPING, neutral. {STYLE}"),
        ("bus-nine", "Bus leaves at nine.", f"Bus door 9 AM, Kit with travel clothes not kit. {STYLE}"),
    ],
    [
        ("phase-three", "Phase three: the bus.", f"Title PHASE 3, team bus interior Kit window seat. {STYLE}"),
        ("same-seat", "Same seat if superstitious.", f"Kit same bus seat number taped, ritual. {STYLE}"),
        ("security-gate", "Security escort at gate.", f"Bus at training ground gate security, Kit looking out. {STYLE}"),
        ("fans-fence", "Fans with phones outside fence.", f"Fans silhouettes phones outside fence, Kit inside bus. {STYLE}"),
        ("waiting-skill", "Waiting is the hardest session.", f"Kit waiting room clock, WAITING IS WORK stamp. {STYLE}"),
        ("phone-away", "Put phone away, heart races.", f"Kit putting phone face down, deep breath. {STYLE}"),
    ],
    [
        ("phase-four", "Phase four: stadium arrival.", f"Title PHASE 4, stadium concrete ramp Kit credential. {STYLE}"),
        ("credential-lanyard", "Credential on lanyard.", f"Kit lanyard CREDENTIAL, cleaner nodding. {STYLE}"),
        ("dressing-room-hooks", "Dressing room hooks and ice.", f"Empty dressing room hooks ice tubs, Kit entering. {STYLE}"),
        ("name-on-back", "Shirt with name correct.", f"Kit shirt hanger NAME ON BACK, careful hands. {STYLE}"),
        ("physio-fine", "Physio asks, you say fine.", f"Physio clipboard hamstring, Kit saying FINE. {STYLE}"),
        ("fine-contract", "Fine is a contract word.", f"Word FINE on contract paper, Kit serious. {STYLE}"),
    ],
    [
        ("phase-five", "Phase five: pre-match meal.", f"Title PHASE 5, pasta bowls team cafeteria. {STYLE}"),
        ("pasta-job", "Eat pasta like a job.", f"Kit eating plain pasta, JOB stamp not joy. {STYLE}"),
        ("tactics-screen", "Tactics on a screen.", f"Tablet tactics arrows, Kit watching one detail circled. {STYLE}"),
        ("left-back-jumps", "Their left back jumps.", f"Diagram left back jumping, Kit memorizing. {STYLE}"),
        ("one-detail", "Memorize one detail only.", f"One arrow highlighted, many faded, Kit focus. {STYLE}"),
        ("three-hours-out", "Three hours to kickoff.", f"Clock 3 HOURS, Kit calm face. {STYLE}"),
    ],
    [
        ("phase-six", "Phase six: warm-up on pitch.", f"Title PHASE 6, empty stadium Kit rondo. {STYLE}"),
        ("skeleton-stadium", "Stadium still a skeleton.", f"Empty stands skeleton seats, Kit small on pitch. {STYLE}"),
        ("grass-too-perfect", "Grass too green, too short.", f"Perfect grass cross-section TOO PERFECT label. {STYLE}"),
        ("tunnel-cameras", "Cameras at tunnel mouth.", f"Camera silhouettes tunnel, Kit warming up ignore. {STYLE}"),
        ("photo-in-head", "Photo in head you never post.", f"Kit mental snapshot bubble, not on phone. {STYLE}"),
        ("warmup-whistle", "First whistle that matters.", f"Referee whistle warm-up end, Kit alert. {STYLE}"),
    ],
    [
        ("phase-seven", "Phase seven: final dressing room.", f"Title PHASE 7, Kit final tape mirror. {STYLE}"),
        ("one-instruction", "One instruction repeated.", f"Whiteboard PRESS THE TRAP repeated, gaffer point. {STYLE}"),
        ("shirt-weight", "Match shirt changes weight.", f"Kit pulling shirt on, weight arrows down. {STYLE}"),
        ("music-then-silence", "Music loud, then silence.", f"Speaker OFF silence, Kit lined up corridor. {STYLE}"),
        ("touch-sign", "Touch sign above door.", f"Kit hand touches DO NOT LITTER sign ritual, corridor. {STYLE}"),
        ("heart-no-run", "Heart climbs without running.", f"Heart rate monitor climbing Kit standing still. {STYLE}"),
    ],
    [
        ("phase-eight", "Phase eight: the tunnel.", f"Title PHASE 8, tunnel lights end Kit lineup. {STYLE}"),
        ("lights-stage", "Lights like a stage.", f"Tunnel bright exit, Kit walking toward light. {STYLE}"),
        ("crowd-before-grass", "Hear crowd before grass.", f"Sound waves before pitch visible, Kit breath. {STYLE}"),
        ("anthem-body", "Anthem your body remembers.", f"Kit tunnel anthem moment no flags no logos. {STYLE}"),
        ("shoulder-opponents", "Shoulder to shoulder then tackle.", f"Kit next opponent silhouette respectful distance. {STYLE}"),
        ("noise-chest", "Noise hits chest first.", f"Kit hand chest sound waves emerging pitch. {STYLE}"),
    ],
    [
        ("phase-nine", "Phase nine: first half.", f"Title PHASE 9, Kit on pitch first half blur. {STYLE}"),
        ("time-compresses", "Time compresses.", f"Clock melting 45 MIN, Kit running. {STYLE}"),
        ("one-touch-heavy", "One touch too heavy, stadium sighs.", f"Kit heavy touch, crowd sigh cloud. {STYLE}"),
        ("split-pass-tall", "Split pass, feel tall half second.", f"Kit through ball line, tall silhouette half second. {STYLE}"),
        ("next-five-meters", "Think next five meters.", f"Five meter arrow on pitch POV Kit. {STYLE}"),
        ("halftime-impossible", "Halftime feels impossible.", f"45 MIN far away sign, Kit sprinting. {STYLE}"),
    ],
    [
        ("phase-ten", "Phase ten: half-time.", f"Title PHASE 10, dressing room half-time Kit towel. {STYLE}"),
        ("orange-slices", "Orange slices and cold towels.", f"Orange slices tray cold towel Kit sitting. {STYLE}"),
        ("heat-map-tablet", "Tablet heat maps thirty seconds.", f"Tablet heat map red zones, Kit glance. {STYLE}"),
        ("one-clip-gaffer", "Gaffer shows one clip.", f"Single clip on screen FIX THIS, Kit nod. {STYLE}"),
        ("change-shirt", "Change shirt, sweat has weight.", f"Kit swapping wet shirt fresh one. {STYLE}"),
        ("second-half-different", "Second half different match.", f"Same scoreboard NEW MATCH label half-time. {STYLE}"),
    ],
    [
        ("phase-eleven", "Phase eleven: second half.", f"Title PHASE 11, Kit tired legs second half. {STYLE}"),
        ("sub-board-verdict", "Sub board glows like verdict.", f"Electronic board numbers, Kit watching hopeful. {STYLE}"),
        ("set-piece-court", "Set piece is a courtroom.", f"Corner flag courtroom metaphor, Kit jumping. {STYLE}"),
        ("eighty-minutes-door", "Eighty minutes: panic or belief.", f"Door labeled 80 MIN PANIC or BELIEF Kit choosing. {STYLE}"),
        ("extra-time", "Extra time if tie demands.", f"EXTRA TIME clock optional, Kit ready. {STYLE}"),
        ("win-header-breath", "Win header, hear own breath.", f"Kit header win, own breath visible in noise. {STYLE}"),
    ],
    [
        ("phase-twelve", "Phase twelve: full time.", f"Title PHASE 12, whistle full time Kit exhale. {STYLE}"),
        ("handshake-respect", "Handshake because respect cheaper.", f"Kit handshake line opponents, no animosity. {STYLE}"),
        ("mixed-zone", "Mixed zone if you scored.", f"Microphone mixed zone if scored, Kit optional. {STYLE}"),
        ("ice-knees", "Ice on knees midnight chicken.", f"Kit knee ice tub later midnight meal. {STYLE}"),
        ("highlight-skips-morning", "Highlights skip the morning.", f"TV highlight reel skipping 5 AM alarm crossed out. {STYLE}"),
        ("body-receipt", "Body keeps the receipt.", f"Kit sore body map RECEIPT stamp. {STYLE}"),
    ],
    [
        ("which-phase", "Which phase owns you.", f"Kit facing twelve phase doors WHICH PHASE. {STYLE}"),
        ("chain-disciplines", "Chain of small disciplines.", f"Chain links alarm bus tunnel ice, Kit holding. {STYLE}"),
        ("hour-breaks-you", "Which hour breaks you before kickoff.", f"Clock hours 5 7 9 12 tunnel, Kit question mark. {STYLE}"),
        ("anthem-not-start", "Thought anthem was the start.", f"Anthem crossed out, dawn circled, Kit wiser. {STYLE}"),
        ("comment-hour", "Tell me your weakest hour.", f"Comment bubble WEAKEST HOUR Kit POV camera. {STYLE}"),
        ("every-level-receipt", "Every level POV receipt.", f"EVERY LEVEL POV title Kit mouth closed thumbs up. {STYLE}"),
    ],
]


def _build_rows() -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    energies = EPISODE_CHAPTER_ENERGY[EPISODE_KEY]
    for chapter_index, templates in enumerate(_BEAT_TEMPLATES, start=1):
        energy = energies[chapter_index - 1]
        for beat_index, (slug, _covers, prompt) in enumerate(templates, start=1):
            rows.append((f"r{chapter_index:02d}-{slug}", beat_covers(energy, beat_index), prompt))
    return rows


def main() -> None:
    need = pov_beat_count(TARGET_SECONDS)
    beats = _build_rows()
    if len(beats) != need:
        raise SystemExit(f"Expected {need} beats, got {len(beats)}")

    draft = DraftScript(
        title="Your Life on a Champions League Matchday",
        description=(
            "From the five AM alarm to full-time ice — your life through every phase of a "
            "Champions League matchday, cartoon POV."
        ),
        tags=(
            "champions league",
            "football",
            "soccer",
            "pov",
            "matchday",
            "cartoon",
            "every level",
            "tunnel",
            "warm up",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in _full_chapters()
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="NOT KICKOFF YET",
    )
    scenario = build_pov_scenario(
        draft,
        topic="Your Life on a Champions League Matchday",
        project_id=PROJECT_ID,
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        scene_gap=SCENE_GAP,
        zoom_body_end=ZOOM,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-pov.json"
    named = PROJECT_ROOT / "senaryo-pov-cl-matchday.json"
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
    print("hook", scenario.youtube.thumbnail_hook)
    print("tsv", tsv)


if __name__ == "__main__":
    main()

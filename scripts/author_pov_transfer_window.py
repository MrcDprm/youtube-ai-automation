"""Author Every Level POV ep5: Your Life through the January Transfer Window."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, pov_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_pov_scenario, write_scenario
from scripts.pov_pacing import EPISODE_CHAPTER_ENERGY, beat_covers

TERMS = ("cartoon pov illustration", "football transfer cartoon")
TARGET_SECONDS = 840.0
MINUTES = 14
PROJECT_ID = "your-life-through-the-january-transfer-window-14dk-20260902"
EPISODE_KEY = "transfer-window"
VOICE = "en-US-ChristopherNeural"
RATE = "+3%"
ZOOM = 1.19
SCENE_GAP = 0.20

STYLE = (
    "Bold cartoon POV, thick ink outlines, flat fills of pitch green, stadium amber, cream paper, "
    "tomato red accents, slight paper grain, non-photorealistic, illustrated, first-person football "
    "transfer window story, not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, "
    "no photoreal faces, no real club crests, no national flags as identity, no child closeups. "
    "Recurring protagonist Kit: young adult, green hoodie or generic kit, short dark hair, mouth closed."
)

CHAPTERS = [
    """January does not feel like a month. It feels like a door that opens twice a year and asks whether your life still fits the shirt you are wearing. This is your life through the January transfer window — agent calls, medical rooms, and a bench at a club that barely knows your name yet. Not the highlight reel. The waiting. The rumors that arrive before breakfast. The training session where your teammates look at you like a question mark. By the end you will know why players stare at their phones in the car park and why a clean medical is not a celebration. It is a receipt. Stay. Level one is not a big-money move. Level one is noise you did not ask for.""",
    """Level one. Rumor season. Your name appears in a feed you swore you would not refresh. A fan account posts a grainy photo and writes linked with an emoji you hate. You tell yourself it is fiction. Your cousin texts before your agent does. Training feels normal until someone jokes that you already packed. You laugh too quickly. You delete the app and reopen it in the shower. Coaches say focus on the match. Focus is a luxury when your future is being typed by strangers. You learn that January starts in the thumb, not on the pitch.""",
    """Level two. The agent call. Your phone buzzes during a meal you were actually enjoying. The voice is calm in the way adults get calm when money is involved. There is interest, they say. Not a done deal. Interest is the word that turns your week into weather. You ask who. They say not yet. You ask if you should tell the club. They say let us see. You hang up and stare at the wall like it has an answer. Your partner asks if you are moving. You say probably not. Probably not is January's favorite lie.""",
    """Level three. Training while linked. You walk onto the grass at a club that still pays you and everyone is polite in a new way. The captain asks how you are. Too kind. The winger does not look you in the eye. You perform normality like a skill. The coach pulls you aside and says ignore the noise. You nod like a student. Inside you count hours until the window closes. A photographer you never noticed before stands near the fence. You wonder if today is the day your picture becomes a rumor with legs.""",
    """Level four. The official approach. Your agent says the club has made contact. Not fans. The club. Paperwork language enters your kitchen. Release clause. Personal terms. Loan with obligation. Words that sound like furniture. You sit at a table that suddenly looks temporary. Your parents ask what it means. You explain like you understand more than you do. The current club knows now. Meetings get shorter. Smiles get professional. You are still required to win a header on Saturday while your life is being priced in another building.""",
    """Level five. Negotiation week. You do not attend most of the calls. That is the point. Football teaches you early that your career is discussed in rooms where your chair is empty. Your agent sends updates with too many exclamation marks or too few. A number appears. You are told not to tell teammates. You are told to rest. Rest feels like holding your breath for days. Someone posts that you agreed terms. You did not. Someone else posts that you rejected everyone. You did not do that either. January turns you into a character you did not audition for.""",
    """Level six. Medical scheduled. The deal is close enough that someone books a flight you will take alone. Medical is not a doctor being nice. Medical is a club buying insurance with your body. You pack shorts you may never wear at that club. You google the city at two in the morning. You wonder if your current teammates already chose your replacement in the group chat you are not in. Your agent says act normal. Normal has left the building. You set three alarms for a flight that could change everything or nothing.""",
    """Level seven. Medical day. Fluorescent lights. Treadmill. Heart monitor. A stranger in a tracksuit watches you like a purchase. You pass tests you did not know existed. Someone measures your hamstring and writes a number that decides whether a chairman smiles. You sit in a corridor scrolling messages you cannot answer yet. Passed is not signed. Signed is not announced. You eat a club sandwich that tastes like suspense. Outside, reporters guess your name from a blurred car window. You learn that your body can be approved before your life is.""",
    """Level eight. Deadline day. The calendar turns cruel. Hours become currency. Your phone becomes a slot machine. Done deal posts appear for players who are still packing. You refresh like it is a job. Your agent says wait. The club says wait. Waiting is the transfer window's native language. A rival bid rumor appears. You do not know if it is leverage or truth. Tea goes cold. The window closes and careers snap shut like lids. Some players celebrate. Some players discover they are staying and must pretend relief is joy.""",
    """Level nine. The announcement. Your name is on a graphic with a generic font and a number you did not choose. Comments arrive before congratulations. Fans argue about money they estimate. You smile in a photo at a training ground you visited once. Your old teammates send messages that are kind and distant at the same time. Your new teammates add you to a chat and say welcome with emoji you read too carefully. You are official now. Official does not mean settled. It means the next level begins immediately.""",
    """Level ten. First day at the new club. New badge on the wall. Not a real crest — generic shapes, same pressure. You park where someone points. You collect a lanyard like it is a passport. The kit room has a cubby with your surname spelled correctly, which feels oddly moving. You introduce yourself to people whose jobs you will depend on and whose names you will forget from nerves. The manager says simple first. Simple is hard when every pass is an audition. You learn that transfers do not end with a photo. They start with being new.""",
    """Level eleven. Learning the playbook. Meetings with clips. Arrows on a screen. A language of calls you half know. You nod when you should ask. You ask when you should nod. Teammates run patterns muscle memory built for them. You chase shapes like a late student. The assistant says you will get it. You wonder how many weeks simple takes. Video sessions feel like homework with millions watching. You stay late to walk patterns alone. The building empties. The lights stay on for players who cannot afford to look lost.""",
    """Level twelve. Bench at the new club. Matchday and your seat is plastic. You watch players you were supposed to replace play well enough to delay you. The manager says the moment will come. The moment is a calendar nobody shares. You warm up and the crowd claps politely. You sit again. Social media says wasted signing. You say nothing because nothing is the policy. You count minutes like debts. You cheer goals you partly envy. You learn that a transfer fee is not playing time. It is a loan your body must repay in silence.""",
    """So where are you in the window. Rumor thumb. Agent call at dinner. Training under side eyes. Official approach language. Negotiation rooms without you. Medical corridor. Deadline refresh. Announcement comments. New cubby first day. Playbook arrows. Plastic bench. Tell me if you have ever been the rumor, the medical, or the bench — and which part hurt more than the move itself. That is the receipt. Rank Run POV.""",
]

_REHOOKS = [
    "January is not a month. It is a door that opens on your phone.",
    "Your name in a feed before your agent calls. Welcome to rumor season.",
    "Interest is not a deal. Interest is weather that ruins dinner.",
    "Politeness is a new kind of side-eye at training.",
    "Paperwork language in your kitchen. Your life priced elsewhere.",
    "Empty chair negotiations. Your career discussed without you.",
    "Medical scheduled. Your body becomes a document.",
    "Fluorescent truth. Passed is not signed.",
    "Deadline day. Refresh is survival. Waiting is the native language.",
    "Official graphic. Comments land before congratulations.",
    "New cubby. Correct surname. Nerves anyway.",
    "Playbook homework with millions watching.",
    "Plastic bench. Fee is not minutes.",
    "Comment: rumor, medical, or bench — pick your poison.",
]

_CHAPTER_EXTRAS = [
    """The window sells moves and hides the hallway between clubs. This episode is that hallway: phones, tests, and seats you did not earn yet.""",
    """Rumors start in feeds and end in dressing rooms. January teaches you that silence is never fully yours.""",
    """Agent calm is a skill. The call that ruins your appetite is still the call that pays the rent.""",
    """Training while linked is acting class with cleats. Everyone sees the rumor. Nobody agrees on the script.""",
    """Official contact turns your apartment into a temporary office. Football grammar arrives with tea.""",
    """Negotiation week is breath-holding as a lifestyle. You are the topic in rooms you never enter.""",
    """Medical scheduled means your body is a document. Pack light. Worry heavy.""",
    """Medical day is fluorescent truth. Passed tests still do not sign the contract.""",
    """Deadline day turns hours into superstition. Refresh is not a hobby. It is survival.""",
    """Announcement day is performance. Welcome messages and comment sections arrive together.""",
    """First day is small humiliations and big cubbies. New club smell is real.""",
    """Playbook week is late-student energy at elite speed. Arrows do not wait.""",
    """Bench at a new club is debt you pay in public. Fees do not guarantee minutes.""",
    """Window phases stick with you. Comment which one you know.""",
]

_CHAPTER_EXTRAS_B = [
    """You will meet players who moved in January and say it was fine. Fine is what you say when the story is still being edited.""",
    """You screenshot a rumor and delete it like shame. The thumb remembers.""",
    """You miss a family moment because the agent said quick call. Quick is never quick.""",
    """You score in training and wonder if the watching photographer cares. Everything feels observed.""",
    """You mispronounce a contract word and laugh too loud. Paperwork is humbling.""",
    """You wake at four to a fake done deal and cannot fall back asleep. Leverage lives in your notifications.""",
    """You sit on a plane with headphones and no announcement. Travel without certainty is its own sport.""",
    """You pass the medical and still check your pulse in the taxi. Approval does not calm the chest.""",
    """You watch the clock hit window closed and feel your shoulders drop without permission. Relief is physical.""",
    """You read welcome messages twice to see who used your first name. Tone analysis at midnight.""",
    """You forget where the ice bath is and pretend you wanted water. New building, old pride.""",
    """You draw arrows in a notebook like school. Million-euro homework still feels like school.""",
    """You celebrate a teammate goal you wanted. Bench character is a weekly test.""",
    """Comment honestly. Rumor, medical, or bench — pick your poison.""",
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
        ("window-door", "January feels like a door.", f"Kit at calendar door JANUARY WINDOW. {STYLE}"),
        ("agent-medical-bench", "Agent calls, medical, bench.", f"Split phone stethoscope bench icons Kit POV. {STYLE}"),
        ("not-highlight", "Not the highlight reel.", f"Kit rejecting highlight reel WAITING stamp. {STYLE}"),
        ("phone-carpark", "Phones in the car park.", f"Kit in car park staring at glowing phone. {STYLE}"),
        ("clean-medical", "Clean medical is a receipt.", f"MEDICAL RECEIPT stamp Kit corridor. {STYLE}"),
        ("level-one-noise", "Level one is noise.", f"Title LEVEL 1 NOISE Kit with rumor clouds. {STYLE}"),
    ],
    [
        ("rumor-season", "Level one: rumor season.", f"Title LEVEL 1 RUMOR SEASON Kit scrolling feed. {STYLE}"),
        ("name-in-feed", "Your name in a feed.", f"Phone screen grainy photo LINKED emoji Kit shocked. {STYLE}"),
        ("cousin-texts", "Cousin texts before agent.", f"COUSIN TEXT vs AGENT CALL split Kit. {STYLE}"),
        ("delete-reopen", "Delete app, reopen in shower.", f"Kit in shower phone steam DELETE REOPEN. {STYLE}"),
        ("focus-luxury", "Focus is a luxury.", f"Coach FOCUS while Kit sees rumor arrows. {STYLE}"),
        ("january-thumb", "January starts in the thumb.", f"Giant thumb on phone JANUARY STARTS HERE. {STYLE}"),
    ],
    [
        ("agent-call", "Level two: the agent call.", f"Title LEVEL 2 AGENT CALL Kit at dinner phone buzz. {STYLE}"),
        ("calm-voice", "Calm voice, money weather.", f"Agent silhouette calm MONEY WEATHER Kit listening. {STYLE}"),
        ("interest-not-done", "Interest, not a done deal.", f"INTEREST word spinning not DONE DEAL Kit. {STYLE}"),
        ("who-not-yet", "Who? Not yet.", f"Kit asking WHO agent shrugs NOT YET. {STYLE}"),
        ("probably-not", "Probably not is a lie.", f"Partner asking moving Kit says PROBABLY NOT. {STYLE}"),
        ("wall-answer", "Wall has no answer.", f"Kit staring at blank wall after call. {STYLE}"),
    ],
    [
        ("training-linked", "Level three: training linked.", f"Title LEVEL 3 TRAINING LINKED Kit walking to pitch. {STYLE}"),
        ("polite-new-way", "Everyone polite in new way.", f"Teammates too kind side-eye Kit POLITE. {STYLE}"),
        ("perform-normal", "Perform normality like skill.", f"Kit acting NORMAL mask on pitch. {STYLE}"),
        ("ignore-noise", "Coach says ignore noise.", f"Coach IGNORE NOISE Kit counting window hours. {STYLE}"),
        ("photographer-fence", "Photographer at the fence.", f"Mystery photographer fence Kit training. {STYLE}"),
        ("question-mark", "Teammates see question mark.", f"Kit silhouette with question mark over head. {STYLE}"),
    ],
    [
        ("official-approach", "Level four: official approach.", f"Title LEVEL 4 OFFICIAL APPROACH Kit at kitchen table. {STYLE}"),
        ("paperwork-language", "Paperwork language arrives.", f"Release clause PERSONAL TERMS floating Kit. {STYLE}"),
        ("temporary-table", "Table looks temporary.", f"Kitchen table TEMPORARY label Kit family. {STYLE}"),
        ("parents-ask", "Parents ask what it means.", f"Kit explaining contract words to parents. {STYLE}"),
        ("priced-elsewhere", "Life priced elsewhere.", f"Kit heading ball while PRICE tag in other building. {STYLE}"),
        ("professional-smiles", "Smiles get professional.", f"Short meetings PROFESSIONAL SMILES Kit nodding. {STYLE}"),
    ],
    [
        ("negotiation-week", "Level five: negotiation week.", f"Title LEVEL 5 NEGOTIATION Kit empty chair in meeting room. {STYLE}"),
        ("empty-chair", "Career discussed without you.", f"Empty chair YOUR CAREER HERE boardroom. {STYLE}"),
        ("agent-updates", "Agent updates punctuation.", f"Phone messages too many or too few exclamation Kit. {STYLE}"),
        ("hold-breath", "Rest feels like breath-holding.", f"Kit in bed HOLD BREATH days counter. {STYLE}"),
        ("fake-agreed", "Fake agreed terms post.", f"Social AGREE TERMS fake news Kit frustrated. {STYLE}"),
        ("character-audition", "Character you did not audition for.", f"Kit wearing wrong costume CHARACTER. {STYLE}"),
    ],
    [
        ("medical-scheduled", "Level six: medical scheduled.", f"Title LEVEL 6 MEDICAL SCHEDULED Kit packing bag. {STYLE}"),
        ("body-insurance", "Body as insurance document.", f"Kit body outline INSURANCE DOCUMENT stamp. {STYLE}"),
        ("solo-flight", "Flight you take alone.", f"Kit alone at airport departure board. {STYLE}"),
        ("google-city", "Google city at 2am.", f"Kit phone map 2AM city search glow. {STYLE}"),
        ("replacement-chat", "Replacement group chat.", f"Kit outside phone GROUP CHAT without you. {STYLE}"),
        ("three-alarms", "Three alarms for flight.", f"Kit setting THREE ALARMS bedside nervous. {STYLE}"),
    ],
    [
        ("medical-day", "Level seven: medical day.", f"Title LEVEL 7 MEDICAL DAY Kit fluorescent corridor. {STYLE}"),
        ("treadmill-monitor", "Treadmill and heart monitor.", f"Kit on treadmill HEART MONITOR wires. {STYLE}"),
        ("hamstring-number", "Hamstring number decides.", f"Doctor measuring hamstring CHAIRMAN SMILE arrow. {STYLE}"),
        ("passed-not-signed", "Passed is not signed.", f"PASSED stamp vs SIGNED stamp Kit waiting. {STYLE}"),
        ("club-sandwich", "Club sandwich suspense.", f"Kit eating generic club sandwich SUSPENSE. {STYLE}"),
        ("blurred-car", "Blurred car reporters.", f"Reporters blurred car window guessing Kit inside. {STYLE}"),
    ],
    [
        ("deadline-day", "Level eight: deadline day.", f"Title LEVEL 8 DEADLINE DAY Kit clock counting down. {STYLE}"),
        ("hours-currency", "Hours become currency.", f"Clock hours as coins Kit counting. {STYLE}"),
        ("phone-slot", "Phone is a slot machine.", f"Kit phone slot machine DONE DEAL spinning. {STYLE}"),
        ("wait-language", "Waiting is native language.", f"WAIT word cloud agent club Kit. {STYLE}"),
        ("window-closes", "Window closes like a lid.", f"Calendar lid snapping WINDOW CLOSED Kit. {STYLE}"),
        ("pretend-relief", "Pretend relief is joy.", f"Kit smiling RELIEF vs JOY mask teammates. {STYLE}"),
    ],
    [
        ("announcement", "Level nine: announcement.", f"Title LEVEL 9 ANNOUNCEMENT Kit generic transfer graphic. {STYLE}"),
        ("generic-font", "Name on generic graphic.", f"Transfer graphic generic font Kit photo. {STYLE}"),
        ("comments-first", "Comments before congrats.", f"Phone COMMENTS flood before CONGRATS Kit. {STYLE}"),
        ("kind-distant", "Kind and distant texts.", f"Old teammates messages KIND DISTANT Kit reading. {STYLE}"),
        ("welcome-chat", "Welcome chat emoji read carefully.", f"New team chat WELCOME emoji Kit analyzing. {STYLE}"),
        ("official-not-settled", "Official not settled.", f"OFFICIAL stamp arrow NEXT LEVEL Kit. {STYLE}"),
    ],
    [
        ("first-day-new", "Level ten: first day new club.", f"Title LEVEL 10 FIRST DAY Kit new training ground entrance. {STYLE}"),
        ("lanyard-passport", "Lanyard like passport.", f"Kit holding lanyard PASSPORT badge. {STYLE}"),
        ("cubby-surname", "Cubby with correct surname.", f"Kit cubby SURNAME spelled right emotional. {STYLE}"),
        ("forget-names", "Forget names from nerves.", f"Kit handshake FORGOT NAME thought bubble. {STYLE}"),
        ("simple-audition", "Simple is an audition.", f"Manager SIMPLE FIRST Kit pass under pressure. {STYLE}"),
        ("transfer-starts-new", "Transfer starts with new.", f"Photo ends NEW BEGINNING arrow Kit walking in. {STYLE}"),
    ],
    [
        ("playbook-week", "Level eleven: learning playbook.", f"Title LEVEL 11 PLAYBOOK Kit in video room. {STYLE}"),
        ("arrows-screen", "Arrows on screen.", f"Tactical screen arrows Kit nodding confused. {STYLE}"),
        ("nod-ask-wrong", "Nod when should ask.", f"Kit NOD vs ASK wrong timing icons. {STYLE}"),
        ("late-student", "Chase shapes like student.", f"Kit chasing pattern shapes LATE STUDENT. {STYLE}"),
        ("homework-millions", "Homework with millions watching.", f"Notebook homework MILLIONS WATCHING Kit. {STYLE}"),
        ("lights-stay-on", "Lights on after others leave.", f"Empty facility Kit alone under lights. {STYLE}"),
    ],
    [
        ("bench-new-club", "Level twelve: bench new club.", f"Title LEVEL 12 BENCH Kit plastic seat matchday. {STYLE}"),
        ("plastic-seat", "Seat is plastic.", f"Kit on plastic bench watching kickoff. {STYLE}"),
        ("moment-calendar", "Moment is secret calendar.", f"Manager MOMENT COMING secret calendar Kit. {STYLE}"),
        ("warm-up-sit", "Warm up, sit again.", f"Kit warm-up tunnel then back to bench. {STYLE}"),
        ("wasted-signing", "Social says wasted signing.", f"Phone WASTED SIGNING comment Kit stone face. {STYLE}"),
        ("fee-not-minutes", "Fee is not minutes.", f"Transfer fee tag vs MINUTES counter Kit. {STYLE}"),
    ],
    [
        ("where-window", "Where are you in the window.", f"Kit pointing WINDOW PHASES chart comment hook. {STYLE}"),
        ("rumor-medical-bench", "Rumor, medical, or bench.", f"Three doors RUMOR MEDICAL BENCH Kit choosing. {STYLE}"),
        ("hurt-more", "Which part hurt more.", f"Kit weighing heart scale HURT MORE. {STYLE}"),
        ("hallway-between", "Hallway between clubs.", f"Kit in corridor between two generic club doors. {STYLE}"),
        ("comment-poison", "Pick your poison comment.", f"Comment bubble PICK YOUR POISON Kit POV. {STYLE}"),
        ("every-level-receipt", "Every level POV receipt.", f"Kit holding receipt EVERY LEVEL POV end card. {STYLE}"),
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
        title="Your Life through the January Transfer Window",
        description=(
            "Agent calls, medical rooms, deadline-day refresh, and a bench at a new club — "
            "your life through the January transfer window, cartoon POV."
        ),
        tags=(
            "transfer window",
            "january transfer",
            "football transfer",
            "agent",
            "medical",
            "deadline day",
            "football",
            "soccer",
            "pov",
            "cartoon",
            "every level",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in _full_chapters()
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="WINDOW STRESS",
    )
    scenario = build_pov_scenario(
        draft,
        topic="Your Life through the January Transfer Window",
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
    named = PROJECT_ROOT / "senaryo-pov-transfer-window.json"
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
    print("chars", sum(len(s.narration) for s in scenario.scenes))
    print("hook", scenario.youtube.thumbnail_hook)
    print("tsv", tsv)


if __name__ == "__main__":
    main()

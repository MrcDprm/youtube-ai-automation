"""Author Every Level POV pilot: Your Life at Every Level of Football."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, pov_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_pov_scenario, write_scenario

TERMS = ("cartoon pov illustration", "football rank cartoon")
TARGET_SECONDS = 840.0
MINUTES = 14
VOICE = "en-US-GuyNeural"
RATE = "+2%"

STYLE = (
    "Bold cartoon POV, thick ink outlines, flat fills of pitch green, stadium amber, cream paper, "
    "tomato red accents, slight paper grain, non-photorealistic, illustrated, first-person football "
    "rank story, not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, "
    "no photoreal faces, no national flags as identity, no child closeups. "
    "Recurring protagonist Kit: young adult, green hoodie, short dark hair, mouth closed, readable silhouette."
)

CHAPTERS = [
    """You wake up already counting levels. Not FIFA cards. Not a video game ladder. Real mud on your boots, real rent due, real scouts with clipboards who forget your name before the handshake dries. This is your life at every level of football, and the game does not care which screen you watched last night. By the end you will know what changes when the crowd stops being your mates and starts being sixty thousand strangers who paid to judge your first touch. Stay. The first level is not glamorous. The first level is a park goal made of backpacks.""",
    """Level one. Park kickabout. Two jumpers on the ground, no nets, a dog that owns the right wing. You play until your mum texts or the streetlights win. Boots are whatever survived last season. The ball is heavy because it is wet. Nobody tracks stats. Nobody cares about your weak foot. You learn the only currency that matters here: show up again tomorrow. If you do not come back, you were never serious. The scout myth starts here, in the lie that someone is always watching. They are not. Not yet.""",
    """Level two. Sunday league. Someone collects subs in a freezer bag. The pitch is bumpy enough to punish vanity. You share a dressing room that smells like paint and deep heat. The manager is also the driver, also the physio, also the guy who argues about the fifty-fifty that decided nothing. You get thirty minutes if you are lucky. Win and you drink tea from a mug with a cracked handle. Lose and you fix the net for free. Pay is zero. Pride is optional. Injuries are real. This is where you learn that commitment has a bus schedule.""",
    """Level three. County or regional step. Travel on a minibus where the back seat is a negotiation. You wear a kit that almost matches. Opponents know your patterns because you played them twice already this season. A parent films vertically for the group chat. You start hearing the word pathway, which means someone might pay your petrol if you are good on a wet Tuesday. Still no salary. Still a day job waiting on Monday. The level is not higher because the football is pretty. It is higher because the excuses stop working.""",
    """Level four. Semi-pro. You sign something that is not quite a contract. You get paid enough to notice, not enough to quit the warehouse. Training is twice a week if the floodlights work. The physio is a student with tape and optimism. You meet players who were academy kids and fell through the floor. You meet players who never went and built thighs like tree trunks. Everyone pretends this is temporary. Some have been pretending for six years. You learn the cruel math: one bad month and the gaffer stops calling.""",
    """Level five. Academy invite. Not the cinematic version. Shared digs, cafeteria rules, school in the morning, drills in the afternoon. You wear GPS vests that turn your lungs into graphs. Coaches speak in percentages. You are one of thirty boys who all believe they are the one. Release day is a PDF and a handshake that hurts more than any tackle. You learn that talent is the entry ticket, not the prize. Sleep matters. Attitude matters. The kid who stays late is not always loved. Sometimes he is warned.""",
    """Level six. Reserves or development squad. You train with the first team sometimes. Mostly you play in empty stands with echo for applause. You touch the match ball like it is borrowed jewellery. Travel with the senior squad once and sit in a row behind the bench, close enough to smell the liniment, far enough to know you are not there yet. Pay is better. Pressure is worse. Every performance is an audition with no script. The gaffer says you are in the shop window. You hope the glass is not locked.""",
    """Level seven. Lower league professional. A contract you can show your family. Wages that cover rent if you are careful. Fans who know your name and your miss from last week. Media is a local paper and a forum that hates you creatively. You play twice a week and your body keeps score. Pre-season is punishment designed as bonding. You move house for minutes on the pitch. Agents appear like weather. Some help. Some sell stories. You learn that professional does not mean safe. It means accountable.""",
    """Level eight. Championship grind. Stadiums big enough to swallow your old Sunday league pitch whole. Travel on coaches with your name on the seat. Opponents are faster, nastier, smarter. The table is a spreadsheet that follows you home. Sell a bad game and social media does not sleep. Medical staff are real. Recovery is scheduled. You earn more than your parents did at your age and that creates a new kind of pressure. You are not allowed to be ordinary on Saturday. Ordinary gets loaned out.""",
    """Level nine. Top flight bench. You walk past cameras that do not know your name yet. Training ground coffee tastes the same as everywhere else. Match day you suit up at two in the afternoon and wait. Warm up in a zone the broadcast never shows. The whistle blows and you calculate inches of space. One touch can be a headline. One mistake can be a meme by half time. Pay is life-changing. Minutes are rationed. You learn patience is a skill with teeth.""",
    """Level ten. Starter in the top league. Noise hits you in the chest before the ball moves. Every pass is reviewed by millions who never miss a meal for sport. Sponsors own your sleeves. Your calendar is not yours. Performance data lands on a tablet before you shower. Win and you are a product. Lose and you are a problem. The money is real. So is the loneliness. Friends treat you like a bank with jokes. You are living the dream people shout about. Sometimes it feels like work in a loud room.""",
    """Level eleven. European nights. Travel that eats days. Security lines, hotel lobbies, pitch walk the night before under lights that make the grass look fake. Opponents you grew up watching on a screen. Anthem in a tunnel you once drew in school. Subbed on at seventy minutes with the score tight and the whole continent listening without knowing your postcode. This level is not only skill. It is sleep, discipline, and the ability to look small in a giant stadium and still choose courage.""",
    """Level twelve. National camp call-up. Not a tournament montage. A badge on a training top that changes how staff speak to you. Media training before you touch a ball. Teammates you fought all season now share a cafeteria. You compete for a squad number with friends. Miss the cut and fly home economy with strangers reading the headline over your shoulder. Make it and discover the nation argument is louder than any away end. Pride and pressure share a room. You represent more than your club now. You represent every level you climbed past.""",
    """So where are you stuck. Park myth. Sunday mud. Semi-pro limbo. Academy PDF. Bench sweat. Championship spreadsheet. Top-league minutes. European tunnel. National camp nerves. The levels are not a ladder you climb once. People fall, restart, change position, change country, change mind. Football pays some people in money and everyone else in stories. Tell me which level you are on right now, and which one you thought would feel different when you got there. That is the receipt. Every level POV.""",
]

# Extra prose per rank so Edge TTS lands near fourteen minutes (roughly twelve thousand five hundred chars).
_CHAPTER_EXTRAS = [
    """The ladder in your head has no save button. You can delete the game app and still feel the levels when you walk past a park and hear a ball thump a fence. That sound is level one calling. This video is the map. Not to fame. To the texture of each step: what your week looks like, what your body feels like, what your phone says about you at night.""",
    """You know the kid who only shoots from halfway because the clip would look good. Park level punishes that. Here the keeper is someone's older brother and he will remember. You learn shape without a whiteboard. You learn hunger without a nutritionist. You learn that the best player on the pitch might work a shift tomorrow morning and still be the fastest because life made him economical with effort.""",
    """Sunday league has politics that would embarrass a parliament. Who starts is who drove. Who plays striker is who brought the balls. You will play in rain that cancels everything else in town except this fixture because pride is stupid and beautiful. You tape ankles with tape that lost its glue in someone's bag. You celebrate a goal like it mattered because for one afternoon it genuinely does.""",
    """Regional football teaches geography. You learn towns you never visited except to lose in. You learn that a two-hour drive each way is normal if you still believe. The stands are mostly family and one person with a horn. You start checking weather apps like a farmer. You start knowing which pitches tilt and which ones swallow the ball in mud. The game gets faster and the mistakes get punished by strangers who will forget you by Monday.""",
    """Semi-pro is where dreams learn paperwork. You sign forms that mention insurance. You meet a kit man who cares more about sock tape than you do. You play in front of three hundred people and it feels like three thousand because you can hear individuals. The gaffer shouts instructions you already know. You nod anyway. Respect is currency when the wage is small. You tell coworkers you have a match Saturday and they say cool without understanding that cool is your second job.""",
    """Academy life is a clock in every room. Curfew. Meal time. Video time. Bed time. You share a room with someone who snores and someone who cries quietly after a bad session. Coaches praise with adjectives that mean nothing until they stop using them on you. You learn that being good at school keeps you on the pitch. You learn that being bad at school gets you sent home even if you scored in a friendly. The building smells like disinfectant and ambition.""",
    """Reserves is the hallway between worlds. You eat with seniors and sit with kids. You train hard enough to impress and careful enough not to injure a star. Match day you watch the stadium fill from a window that does not appear on television. You get twenty minutes in a cup tie and your legs feel like they belong to someone else. The crowd roar leaks through concrete. You understand that proximity is not arrival. You go home and replay one pass that worked.""",
    """Lower-league professional is the first time football pays rent and also takes your weekends forever. You meet fans who know your birthday. You meet fans who know your miss from October. Local radio calls you by nickname without asking. You learn recovery is not optional. Ice becomes furniture. You sign autographs for kids and remember being that kid. You fear a knock that lasts three weeks because three weeks is a career at this wage. You still would not trade the shirt.""",
    """Championship football is a season that never stops talking. Promotion money haunts every match. Relegation fear sits in the seat next to you on the bus. Stadiums hold noise like weather. You play twice in four days and your hamstrings file complaints. The gaffer rotates and you learn new instructions like new passwords. Journalists ask questions that sound simple and are traps. You answer carefully. You sleep with the table open on your phone. You tell yourself you love the grind. Sometimes that is true.""",
    """The bench in the top flight is a job with a view. You watch the game you would change if you could. You count warm-up minutes like money. The substitute board is a guillotine and a lottery. You clap when required. You stretch when required. You pray the gaffer looks at you and not the other sub. Your family watches on television and texts love you cannot answer until full time. You learn that ready is not a feeling. Ready is a decision you make in thirty seconds.""",
    """Starting in the top league turns your name into a search term. Every touch is a sentence. Every run is evidence. You meet players you once had on a poster. You discover they are human and tired. Sponsors want smiles. Fans want miracles. Managers want consistency. Your body wants sleep. You rent a quiet house and still hear whistles in the walls. You earn more than you imagined and spend it on normal things that feel unreal. You win and strangers claim they always believed. You lose and strangers claim they knew.""",
    """European nights rewrite your calendar. You fly back at dawn and train at noon. You play a match where one mistake is a highlight reel for the wrong reasons. The tunnel smells like grass and nerves. You line up near someone you watched on a laptop. The anthem is not background music. It is a weight. Subbed on, you touch the ball once and the stadium reacts like you moved a planet. You sleep on the plane and dream of level one mud. You wake and the schedule says again.""",
    """National camp is identity with paperwork. You sing anthems in a room before you earn the right on grass. Media training teaches you how to say nothing kindly. Teammates become rivals for a shirt number. You share a table with a player who broke your leg two seasons ago. You nod. Professional. Cut from the squad and you ride home reading comments from people who never kicked a ball in rain. Selected and you discover the nation watches differently than your club. Pride is heavy. You carry it anyway.""",
    """Levels are not medals. They are weeks. Mud weeks. Bus weeks. Contract weeks. Bench weeks. Night-flight weeks. You can be on two levels at once in your head while your feet are only on one. That is why the ladder lies. Tell me the level you are actually living, not the one you post. Tell me which step surprised you with how ordinary it felt once you arrived.""",
]


def _full_chapters() -> list[str]:
    return [f"{body} {extra}" for body, extra in zip(CHAPTERS, _CHAPTER_EXTRAS, strict=True)]

# Six beats per chapter (84 total at 14 minutes).
_BEAT_TEMPLATES: list[list[tuple[str, str]]] = [
    [
        ("hook-counting", "You wake counting levels, not cards.", f"Kit in bed staring at ceiling, LEVEL counter floating, hook energy. {STYLE}"),
        ("not-fifa", "Not FIFA. Not a game ladder.", f"Red X over a video game rank screen, Kit unimpressed, mouth closed. {STYLE}"),
        ("real-mud", "Real mud, real rent, real scouts.", f"Kit boots with mud, rent bill icon, scout silhouette with clipboard. {STYLE}"),
        ("sixty-thousand", "Sixty thousand strangers later.", f"Tiny park pitch morphing into huge stadium crowd, POV from Kit. {STYLE}"),
        ("backpack-goals", "Park goals made of backpacks.", f"Two hoodies as goalposts, backpacks, evening park. {STYLE}"),
        ("stay-hook", "Stay for every level.", f"Kit pointing forward on pitch, STAY text, cream paper. {STYLE}"),
    ],
    [
        ("level-one", "Level one: park kickabout.", f"Title card LEVEL 1, Kit dribbling in park. {STYLE}"),
        ("jumper-nets", "Jumpers for goalposts, no nets.", f"Jumpers on grass, no net, dog nearby. {STYLE}"),
        ("wet-ball", "Heavy wet ball, cheap boots.", f"Kit kicking heavy wet ball, scuffed boots. {STYLE}"),
        ("show-up", "Currency: show up tomorrow.", f"Calendar with tomorrow circled, Kit tying boots. {STYLE}"),
        ("scout-myth", "The scout myth starts here.", f"Empty park bench with MYTH stamp, no scouts. {STYLE}"),
        ("not-yet", "They are not watching. Not yet.", f"Kit alone practicing, empty sidelines. {STYLE}"),
    ],
    [
        ("level-two", "Level two: Sunday league.", f"Title LEVEL 2, muddy pitch, Kit in mixed kit. {STYLE}"),
        ("subs-bag", "Subs collected in a freezer bag.", f"Freezer bag with coins, volunteer collecting. {STYLE}"),
        ("deep-heat", "Dressing room: paint and Deep Heat.", f"Tiny changing room, Deep Heat tin, Kit sitting. {STYLE}"),
        ("thirty-minutes", "Thirty minutes if you are lucky.", f"Sub board showing 30 MIN, Kit waiting. {STYLE}"),
        ("cracked-mug", "Tea in a cracked mug.", f"Winners tea mug cracked handle, steam. {STYLE}"),
        ("bus-schedule", "Commitment has a bus schedule.", f"Minibus timetable, Kit checking phone. {STYLE}"),
    ],
    [
        ("level-three", "Level three: county step.", f"Title LEVEL 3, regional badge generic, Kit on coach. {STYLE}"),
        ("minibus", "Travel on a minibus.", f"Kit on minibus back seat, kit bag. {STYLE}"),
        ("almost-kit", "Kit that almost matches.", f"Two similar but mismatched shirts side by side. {STYLE}"),
        ("vertical-film", "Parent films vertically.", f"Phone vertical filming match, Kit playing. {STYLE}"),
        ("pathway-word", "The word pathway appears.", f"PATHWAY stamp on clipboard, petrol receipt. {STYLE}"),
        ("excuses-stop", "Excuses stop working.", f"Kit running in rain, NO EXCUSES text. {STYLE}"),
    ],
    [
        ("level-four", "Level four: semi-pro.", f"Title LEVEL 4, semi-pro contract paper. {STYLE}"),
        ("not-quite-contract", "A contract that is not quite.", f"Thin contract page, Kit signing cautiously. {STYLE}"),
        ("warehouse-job", "Not enough to quit the warehouse.", f"Kit in warehouse vest next to boots. {STYLE}"),
        ("floodlights", "Training if floodlights work.", f"Pitch under flickering floodlight, Kit training. {STYLE}"),
        ("six-years", "Pretending for six years.", f"Calendar six years crossed, same semi-pro badge. {STYLE}"),
        ("gaffer-stops", "One bad month, gaffer stops calling.", f"Phone with missed calls fading, Kit worried. {STYLE}"),
    ],
    [
        ("level-five", "Level five: academy invite.", f"Title LEVEL 5, academy building generic. {STYLE}"),
        ("shared-digs", "Shared digs, cafeteria rules.", f"Kit in dorm room, cafeteria tray rules sign. {STYLE}"),
        ("gps-vest", "GPS vests graph your lungs.", f"Kit wearing GPS vest, heart graph overlay. {STYLE}"),
        ("one-of-thirty", "One of thirty who believe.", f"Thirty silhouettes, one highlighted Kit. {STYLE}"),
        ("release-pdf", "Release day is a PDF.", f"Laptop PDF RELEASE DAY, Kit stiff expression. {STYLE}"),
        ("entry-ticket", "Talent is the entry ticket.", f"Ticket stub labeled TALENT, not PRIZE. {STYLE}"),
    ],
    [
        ("level-six", "Level six: reserves.", f"Title LEVEL 6, empty stand stadium. {STYLE}"),
        ("empty-stands", "Echo for applause.", f"Kit playing in empty stand, echo lines. {STYLE}"),
        ("match-ball", "Match ball like borrowed jewellery.", f"Kit holding match ball carefully. {STYLE}"),
        ("behind-bench", "Behind the bench, not there yet.", f"Kit seated behind first-team bench. {STYLE}"),
        ("shop-window", "In the shop window.", f"Shop window mannequin with kit, metaphor. {STYLE}"),
        ("audition", "Every game an audition.", f"Spotlight on Kit on pitch, AUDITION stamp. {STYLE}"),
    ],
    [
        ("level-seven", "Level seven: lower league pro.", f"Title LEVEL 7, contract handshake. {STYLE}"),
        ("family-contract", "Contract you can show family.", f"Kit showing contract to family silhouettes. {STYLE}"),
        ("rent-math", "Wages cover rent if careful.", f"Rent bill balanced on wages slip. {STYLE}"),
        ("local-forum", "Local forum hates creatively.", f"Laptop forum posts, Kit ignoring. {STYLE}"),
        ("body-score", "Your body keeps score.", f"Kit ice bath, body map aches. {STYLE}"),
        ("accountable", "Professional means accountable.", f"Kit facing media mic silhouette, accountable. {STYLE}"),
    ],
    [
        ("level-eight", "Level eight: Championship grind.", f"Title LEVEL 8, big stadium exterior. {STYLE}"),
        ("swallow-pitch", "Stadium swallows Sunday pitch.", f"Size comparison Sunday pitch inside stadium. {STYLE}"),
        ("named-seat", "Coach with your name on seat.", f"Bus seat NAME TAG Kit, night travel. {STYLE}"),
        ("table-home", "Table follows you home.", f"League table on kitchen wall at home. {STYLE}"),
        ("loan-threat", "Ordinary gets loaned out.", f"LOAN arrow pointing away from Kit. {STYLE}"),
        ("not-allowed-ordinary", "Not allowed to be ordinary.", f"Kit under spotlight Saturday, no ordinary. {STYLE}"),
    ],
    [
        ("level-nine", "Level nine: top-flight bench.", f"Title LEVEL 9, tunnel suits. {STYLE}"),
        ("unknown-cameras", "Cameras do not know your name.", f"Cameras pointed past Kit in tunnel. {STYLE}"),
        ("two-pm-suit", "Suit up at two p.m.", f"Clock 2 PM, Kit in suit with kit bag. {STYLE}"),
        ("hidden-warmup", "Warm up where broadcast never shows.", f"Kit warming up off-camera zone. {STYLE}"),
        ("inches-space", "Calculate inches of space.", f"Top-down pitch inches between defenders. {STYLE}"),
        ("minutes-rationed", "Minutes are rationed.", f"Stopwatch MINUTES RATIONED, Kit waiting. {STYLE}"),
    ],
    [
        ("level-ten", "Level ten: top-league starter.", f"Title LEVEL 10, stadium roar. {STYLE}"),
        ("noise-chest", "Noise hits your chest.", f"Kit hand on chest, sound waves, crowd. {STYLE}"),
        ("millions-review", "Millions review every pass.", f"Tablet replay with view count, Kit. {STYLE}"),
        ("sponsor-sleeves", "Sponsors own your sleeves.", f"Kit shirt sleeve logos generic. {STYLE}"),
        ("loud-room-work", "Dream feels like work in loud room.", f"Kit exhausted in loud stadium tunnel. {STYLE}"),
        ("loneliness-money", "Money real, loneliness real.", f"Kit alone in luxury apartment, city lights. {STYLE}"),
    ],
    [
        ("level-eleven", "Level eleven: European nights.", f"Title LEVEL 11, UCL-style tunnel generic no logos. {STYLE}"),
        ("pitch-walk", "Pitch walk under fake-looking lights.", f"Kit walking pitch at night, bright lights. {STYLE}"),
        ("childhood-screen", "Opponents you watched on screen.", f"Kid Kit watching TV, now facing opponent silhouette. {STYLE}"),
        ("anthem-tunnel", "Anthem in the tunnel.", f"Kit in tunnel, anthem moment, no flags. {STYLE}"),
        ("seventy-minutes", "Subbed on at seventy minutes.", f"Board 70 MIN, Kit ready to enter. {STYLE}"),
        ("choose-courage", "Choose courage in giant stadium.", f"Kit small in huge stadium, stepping forward. {STYLE}"),
    ],
    [
        ("level-twelve", "Level twelve: national camp.", f"Title LEVEL 12, training camp badge generic. {STYLE}"),
        ("badge-changes-talk", "Badge changes how staff speak.", f"Kit with national training top, staff formal. {STYLE}"),
        ("media-training", "Media training before ball.", f"Kit at media training desk, microphones. {STYLE}"),
        ("economy-flight", "Miss cut, fly home economy.", f"Kit on plane economy, headline on seat screen. {STYLE}"),
        ("nation-argument", "Nation argument louder than away end.", f"Social chatter cloud over Kit head. {STYLE}"),
        ("every-level-climbed", "Represent every level you climbed.", f"Kit shadow showing ladder of levels behind. {STYLE}"),
    ],
    [
        ("where-stuck", "Where are you stuck.", f"Kit facing ladder of levels, WHERE ARE YOU stamp. {STYLE}"),
        ("fall-restart", "People fall, restart, change.", f"Kit helping teammate up, restart arrow. {STYLE}"),
        ("paid-stories", "Football pays in money or stories.", f"Split path MONEY vs STORIES, Kit between. {STYLE}"),
        ("comment-which", "Which level are you on.", f"Comment bubble WHICH LEVEL, Kit to camera POV. {STYLE}"),
        ("thought-different", "Thought it would feel different.", f"Kit at top looking back at park level. {STYLE}"),
        ("every-level-receipt", "Every level POV receipt.", f"Title card EVERY LEVEL POV, Kit thumbs up, mouth closed. {STYLE}"),
    ],
]


def _build_rows() -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for chapter_index, templates in enumerate(_BEAT_TEMPLATES, start=1):
        for beat_index, (slug, covers, prompt) in enumerate(templates, start=1):
            rows.append((f"r{chapter_index:02d}-{slug}", covers, prompt))
    return rows


def main() -> None:
    need = pov_beat_count(TARGET_SECONDS)
    beats = _build_rows()
    if len(beats) != need:
        raise SystemExit(f"Expected {need} beats, got {len(beats)}")

    draft = DraftScript(
        title="Your Life at Every Level of Football",
        description=(
            "From park kickabout to European nights — your life at every rank of football, "
            "cartoon POV, one level at a time."
        ),
        tags=(
            "football",
            "soccer",
            "pov",
            "every level",
            "cartoon",
            "rank",
            "sunday league",
            "champions league",
            "story",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in _full_chapters()
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="YOU START HERE",
    )
    scenario = build_pov_scenario(
        draft,
        topic="Your Life at Every Level of Football",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-pov.json"
    named = PROJECT_ROOT / "senaryo-pov-football-levels.json"
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
    print("brand", scenario.youtube.brand_id)
    print("hook", scenario.youtube.thumbnail_hook)
    print("tsv", tsv)


if __name__ == "__main__":
    main()

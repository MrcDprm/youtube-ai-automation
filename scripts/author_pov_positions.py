"""Author Every Level POV ep4: Your Life as Every Position on a Football Pitch."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, pov_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_pov_scenario, write_scenario
from scripts.pov_pacing import EPISODE_CHAPTER_ENERGY, beat_covers

TERMS = ("cartoon pov illustration", "football rank cartoon")
TARGET_SECONDS = 840.0
MINUTES = 14
PROJECT_ID = "your-life-as-every-position-on-a-football-pit-14dk-20260902"
EPISODE_KEY = "positions"
VOICE = "en-US-GuyNeural"
RATE = "+1%"
ZOOM = 1.16
SCENE_GAP = 0.28

STYLE = (
    "Bold cartoon POV, thick ink outlines, flat fills of pitch green, stadium amber, cream paper, "
    "tomato red accents, slight paper grain, non-photorealistic, illustrated, first-person football "
    "climb story, not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, "
    "no photoreal faces, no real club crests, no national flags as identity, no child closeups. "
    "Recurring protagonist Kit: young adult, green hoodie or generic kit, short dark hair, mouth closed."
)

CHAPTERS = [
    """You do not live one role on a pitch. You live a ladder of roles, and each rung rewrites what bravery looks like. This is your life as every position on a football pitch, from the last line to the last touch. The gap between them is not a tactics board. It is loneliness, noise, blame, and where your body belongs when the ball moves. By the end you will know why the keeper talks to the post and the striker talks to the net. Stay. Position one is not glory. Position one is gloves in the rain and nobody clapping when you save what they forgot to see.""",
    """Position one. Goalkeeper. You stand where mistakes become headlines and saves become expected. The box is yours until it is not. You organize defenders who ignore you until the ball is in the air. You shout into wind that steals your words. Your hands are your résumé. One spill and the whole pitch thinks you cracked. You train alone while outfield players joke about standing still. You dive on frozen ground because someone has to. You watch the game from the best seat and the worst jury. You learn patience that looks like laziness from the stands. You learn that clean sheets are team trophies worn by one name.""",
    """Position two. Center-back. You are the adult in a room of adrenaline. You solve problems with shoulders, timing, and calm when a striker smells blood. You win headers that nobody counts unless you lose one. You cover for full-backs who forgot their job because the winger looked fast on television. You communicate in short words because panic spreads faster than passes. You take yellow cards like invoices for someone else's mistake. You are not allowed to be tired in public. You learn that bravery here is stepping forward when every instinct says step back.""",
    """Position three. Full-back. You are a winger who came home late and got put on defense duty forever. You run two games in one: shut the line, then become an extra attacker when the coach points. Your lungs burn while the center-back tells you to stay simple. You cross into traffic and get judged on one connection. You mark players who are faster on paper and win anyway because the touchline is a wall. You spend half the match with your back to each goal. You learn that modern football punishes full-backs who only defend and also punishes full-backs who only attack.""",
    """Position four. Defensive midfielder. You are the screen between chaos and structure. You break passes that would have looked beautiful on highlights if you had arrived one second late. You tackle, recover, tackle again, and rarely score. Fans clap the forward who ran into space you cleaned five minutes earlier. You read the game like sheet music and play the note nobody hears. You take fouls to stop counters and accept the card like rent. You learn that being important and being celebrated are not the same currency on a Saturday.""",
    """Position five. Box-to-box midfielder. You are the player GPS thinks is lying. You appear in both boxes in one half and still get asked why you were not somewhere else. You run until your legs feel borrowed. You join attacks because the coach said arrive, then sprint back because the coach said never leave us open. You score a screamer once a month and cover three mistakes per week. Teammates love you because you do the work they avoid. Opponents hate you because you never fully disappear. You learn that box-to-box is a personality test with shin guards.""",
    """Position six. Attacking midfielder. Number ten energy even when the shirt says something else. You live in the pocket where space opens for half a second and disappears if you breathe wrong. You are expected to see passes that do not exist yet and make them look obvious after they land. You take the ball in traffic and turn like the crowd is a suggestion. You get kicked because stopping you is cheaper than marking you honestly. You miss one chance and the stadium remembers. You learn that playmakers are judged on magic, not on mileage.""",
    """Position seven. Winger. Touchline merchant. You beat a man, cut in, cross, repeat until the full-back hates sunlight. Your best weapon is space that only exists if you believe in it. You track back because the gaffer said so and because you know the counter will kill you personally. You take on one-v-ones like exams you cannot retake. You deliver balls into boxes where strikers miss and you still get half the blame. You are fast until the pitch is heavy, then you are clever or you are dead. You learn that width is not decoration. It is how you stretch a defense until someone snaps.""",
    """Position eight. Inverted winger. You start wide and end up central because your strong foot has opinions. Defenders think they know where you are going until you cut inside and the whole shape tilts. You shoot from angles coaches once banned and now call progressive. You occupy the half-space like a tenant who refuses to leave. Full-backs do not know whether to follow you inside or protect the line you abandoned. You create goals and also take them because someone has to. You learn that inverted is not a trick. It is a different kind of loneliness on the flank.""",
    """Position nine. Second striker. You are the shadow striker, the link, the player who makes the number nine look like a genius. You drop, you spin, you arrive late in the box when everyone watches the ball. You do not always score but you always connect. You press from an angle that looks lazy until it isn't. You speak both languages: striker hunger and midfielder patience. Coaches love you because you solve problems without instructions. Fans sometimes forget your name because your work is the pass before the pass. You learn that being unselfish is a skill with a tax bill.""",
    """Position ten. Target striker. Number nine. The box is your office and every cross is a meeting you cannot miss. You hold up balls with your back to goal while midfielders pretend they are close enough to help. You win aerial duels that look like wrestling and smell like grass. You finish with one touch because two touches is a luxury you were never sold. You get marked by two center-backs and still expected to score anyway. You take elbows like weather. You learn that target nines are not just tall. They are stubborn in ways statistics rarely capture.""",
    """Position eleven. False nine. You drop deep and the center-backs do not know whether to follow or hold the line. You are a striker who refuses to stay where strikers belong. You pull defenders into midfield and open lanes for wingers who thank you with a wave. You score less than a classic nine but the team scores more because you rearrange the room. You need intelligence, touch, and the confidence to disappear from the box on purpose. You learn that false nine is not a cheat code. It is a trade: your goals for their structure.""",
    """Position twelve. Hybrid roles. Modern football does not always give you one name. You are a winger who defends like a full-back. A full-back who finishes like a winger. A midfielder who drops into defense because the shape changed in real time. You watch heat maps that look like abstract art and realize the position on the team sheet was a suggestion. You train multiple jobs because substitutes are expensive and versatility is currency. You get instructions through earpieces and hand signals. You learn that the pitch is not eleven fixed jobs. It is eleven people solving a moving problem.""",
    """So which position owns you. Gloves and silence. Shoulders and headers. Touchline sprints. The screen in front of defense. Box-to-box lungs. Number ten pockets. Wide crosses. Inverted cuts. Second-striker links. Target nine battles. False nine drops. Hybrid shapes that change every week. Tell me which role you play on Sunday and which role you wish you played when the camera was on. Tell me if you thought one position would fix your football and did not. That is the receipt. Rank Run POV.""",
]

_REHOOKS = [
    "One shirt. Eleven jobs. The pitch is lying if it says you only have one role.",
    "Gloves save what nobody claps. Welcome to invisible glory.",
    "Headers win wars. Credit loses them.",
    "Touchline sprint. Attack. Defend. Lungs on fire.",
    "Break the pass nobody sees. Janitor with a view.",
    "GPS thinks you are lying. You are not.",
    "Half-second pocket. Magic or miss — no middle.",
    "Beat your man. Overhit the cross. Repeat until hate.",
    "Cut inside. The whole pitch tilts.",
    "Link play. Your name stays off the photo.",
    "One touch. Elbows included. No refund.",
    "Drop deep. Defenders panic. Your goals disappear.",
    "Hybrid week. Three jobs. One shirt.",
    "Comment your Sunday role. Be honest.",
]

_CHAPTER_EXTRAS = [
    """Position stories sell the striker and hide the keeper. This episode is the whole pitch made personal: blame, credit, and the version of you that appears when the ball arrives elsewhere.""",
    """Goalkeepers learn early that applause is conditional. One save is duty. One mistake is a documentary. The role teaches you to love the game in quiet rooms.""",
    """Center-backs inherit panic and return calm. You are the last adult before the adult in goal. Headers are not highlights until you lose one.""",
    """Full-backs live in the corridor between styles. Attack too much and you are reckless. Defend too much and you are obsolete. The touchline is your contract.""",
    """Defensive mids are the game's janitors with better views. You sweep what would have gone viral if you had been late.""",
    """Box-to-box is mileage with meaning. You are everywhere, which means you are also nowhere when someone needs a scapegoat.""",
    """The ten sees the pass before the pass exists. That gift comes with a tax: one miss and the crowd thinks you vanished.""",
    """Wingers sell hope to the touchline. One good cross erases three lost duels until the next lost duel.""",
    """Inverted wingers bend the pitch without moving the lines. Defenders hate you because you refuse to stay where they studied.""",
    """Second strikers connect rooms. Your goal tally will lie about your importance forever.""",
    """Target nines carry contact like currency. The box is not glamorous. It is elbows, timing, and one touch.""",
    """False nines trade personal numbers for team shape. You score less and matter more, which is a hard sell at dinner.""",
    """Hybrid roles are the receipt that football changed. One shirt, three jobs, zero patience.""",
    """Positions are weeks, not labels. Tell me yours honestly. Sunday role counts.""",
]

_CHAPTER_EXTRAS_B = [
    """You will meet players who looked wrong on paper and right on grass. The pitch punishes labels faster than coaches do.""",
    """Your first clean sheet feels like a secret because nobody chants for the keeper at the café afterward.""",
    """You once cleared a ball off the line and the striker got credit for the miss. Center-back math is cruel.""",
    """You overlap, cross, sprint back, and still hear keep it simple from the bench like simplicity is free.""",
    """You foul once to kill a counter and accept the yellow like rent. The DM receipt is always paid in cards.""",
    """You cover more ground than anyone and still get asked why you were not on the back post. Box-to-box irony.""",
    """You thread a ball through three legs and the assist chart says second pass. Playmaker erasure is normal.""",
    """You beat your man twice and overhit the cross. The touchline remembers the cross, not the beats.""",
    """You cut inside, shoot, score, and the pundit says predictable. Inverted life is never fully credited.""",
    """You set up the goal and the striker takes the photo. Second-striker fame is always one room away.""",
    """You win a header duel and land in mud that matches your kit. Target nine glamour is a myth sold to forwards.""",
    """You drop deep, spin, and release a winger who scores. The false nine goal count will never tell that story.""",
    """You played winger Tuesday and wing-back Saturday and nobody updated the program. Hybrid football is real life.""",
    """Comment your position. Be honest. Nobody starts as a complete player.""",
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
        ("not-one-role", "You do not live one role.", f"Kit on pitch split into position zones NOT ONE ROLE. {STYLE}"),
        ("ladder-roles", "A ladder of roles.", f"Position ladder Kit climbing from goal to striker. {STYLE}"),
        ("bravery-rewrites", "Each rung rewrites bravery.", f"BRAVERY stamp changing per zone Kit POV. {STYLE}"),
        ("keeper-post", "Keeper talks to the post.", f"Kit as keeper whispering to goalpost gloves on. {STYLE}"),
        ("striker-net", "Striker talks to the net.", f"Kit as striker staring at net one touch. {STYLE}"),
        ("stay-pitch", "Stay for every position.", f"Kit pointing across full pitch STAY text. {STYLE}"),
    ],
    [
        ("position-one-gk", "Position one: goalkeeper.", f"Title POSITION 1 GOALKEEPER Kit in gloves. {STYLE}"),
        ("box-yours", "The box is yours until not.", f"Penalty box YOURS stamp Kit hands up. {STYLE}"),
        ("shout-wind", "Instructions stolen by wind.", f"Kit shouting arrows stolen by wind. {STYLE}"),
        ("hands-resume", "Hands are your résumé.", f"Gloved hands RESUME stamp Kit diving. {STYLE}"),
        ("train-alone", "Train alone, stand still jokes.", f"Kit solo training cones outfielders joking STILL. {STYLE}"),
        ("clean-sheet", "Clean sheets, one name.", f"Clean sheet trophy one name GOALKEEPER. {STYLE}"),
    ],
    [
        ("position-two-cb", "Position two: center-back.", f"Title POSITION 2 CENTER-BACK Kit shoulders square. {STYLE}"),
        ("adult-room", "Adult in adrenaline room.", f"Kit calm amid chaos ADULT IN ROOM. {STYLE}"),
        ("headers-count", "Headers nobody counts.", f"Kit winning header invisible stat counter. {STYLE}"),
        ("cover-fullback", "Cover for full-backs.", f"Kit sprinting to cover wandering full-back. {STYLE}"),
        ("yellow-invoice", "Yellow cards like invoices.", f"Yellow card INVOICE for others mistake Kit. {STYLE}"),
        ("step-forward", "Step forward when instinct says back.", f"Kit stepping forward BRAVERY arrow. {STYLE}"),
    ],
    [
        ("position-three-fb", "Position three: full-back.", f"Title POSITION 3 FULL-BACK Kit on touchline. {STYLE}"),
        ("two-games", "Two games in one.", f"Split DEFEND and ATTACK Kit running both. {STYLE}"),
        ("lungs-burn", "Lungs burn, stay simple.", f"Kit gasping STAY SIMPLE from bench. {STYLE}"),
        ("cross-traffic", "Cross into traffic.", f"Kit crossing into crowded box judged. {STYLE}"),
        ("touchline-wall", "Touchline is a wall.", f"Kit using touchline as wall vs winger. {STYLE}"),
        ("back-both-goals", "Back to both goals.", f"Kit spinning back to defend and attack goals. {STYLE}"),
    ],
    [
        ("position-four-dm", "Position four: defensive mid.", f"Title POSITION 4 DEFENSIVE MID Kit screening. {STYLE}"),
        ("screen-chaos", "Screen between chaos and structure.", f"Chaos arrow blocked by Kit SCREEN. {STYLE}"),
        ("break-passes", "Break passes nobody sees.", f"Kit intercept invisible highlight pass broken. {STYLE}"),
        ("forward-claps", "Forward gets claps for your space.", f"Forward celebrated space Kit cleaned earlier. {STYLE}"),
        ("foul-rent", "Fouls to stop counters like rent.", f"Kit tactical foul CARD LIKE RENT. {STYLE}"),
        ("two-languages", "Speak to backs and wingers.", f"Kit two speech bubbles CB language winger language. {STYLE}"),
    ],
    [
        ("position-five-b2b", "Position five: box-to-box.", f"Title POSITION 5 BOX-TO-BOX Kit mid-pitch sprint. {STYLE}"),
        ("gps-lying", "GPS thinks you are lying.", f"Heat trail both boxes GPS LIAR Kit. {STYLE}"),
        ("both-boxes", "Both boxes in one half.", f"Kit appearing in both penalty boxes same half. {STYLE}"),
        ("screamer-cover", "Screamer monthly, cover weekly.", f"Kit long shot plus three recovery tackles. {STYLE}"),
        ("work-avoided", "Do work teammates avoid.", f"Kit doing arrows teammates skipped. {STYLE}"),
        ("personality-test", "Personality test with shin guards.", f"BOX-TO-BOX personality test Kit exhausted. {STYLE}"),
    ],
    [
        ("position-six-am", "Position six: attacking mid.", f"Title POSITION 6 NUMBER TEN Kit in pocket. {STYLE}"),
        ("half-second-space", "Space for half a second.", f"Pocket space opening closing Kit turning. {STYLE}"),
        ("passes-not-exist", "See passes that do not exist yet.", f"Kit vision dotted pass lines future. {STYLE}"),
        ("kicked-stopping", "Get kicked because stopping you is cheap.", f"Kit fouled CHEAPER THAN HONEST MARKING. {STYLE}"),
        ("four-chances-one-goal", "Four chances, one headline.", f"Four chance icons one GOAL headline stolen. {STYLE}"),
        ("judged-magic", "Judged on magic not mileage.", f"MAGIC vs MILEAGE scales Kit ten. {STYLE}"),
    ],
    [
        ("position-seven-w", "Position seven: winger.", f"Title POSITION 7 WINGER Kit touchline. {STYLE}"),
        ("beat-cut-cross", "Beat, cut, cross, repeat.", f"Kit sequence beat cut cross loop. {STYLE}"),
        ("space-belief", "Space exists if you believe.", f"Kit believing into touchline space. {STYLE}"),
        ("track-back", "Track back or counter kills you.", f"Kit sprinting back counter arrow personal. {STYLE}"),
        ("one-v-one-exam", "One-v-ones like exams.", f"Kit 1v1 EXAM NO RETAKE stamp. {STYLE}"),
        ("width-snaps", "Width until defense snaps.", f"Defense stretched SNAP Kit wide. {STYLE}"),
    ],
    [
        ("position-eight-iw", "Position eight: inverted winger.", f"Title POSITION 8 INVERTED WINGER Kit cutting in. {STYLE}"),
        ("start-wide-end-central", "Start wide, end central.", f"Kit path wide to central strong foot. {STYLE}"),
        ("shape-tilts", "Whole shape tilts when you cut.", f"Defense shape tilting Kit cutting inside. {STYLE}"),
        ("half-space-tenant", "Half-space tenant.", f"Kit in half-space TENANT REFUSES LEAVE. {STYLE}"),
        ("progressive-angle", "Shoot from once-banned angles.", f"Kit shooting progressive angle coach flip. {STYLE}"),
        ("flank-loneliness", "Different loneliness on the flank.", f"Kit alone on flank INVERTED LONELINESS. {STYLE}"),
    ],
    [
        ("position-nine-ss", "Position nine: second striker.", f"Title POSITION 9 SECOND STRIKER Kit linking. {STYLE}"),
        ("shadow-striker", "Shadow striker, link player.", f"Kit shadow behind number nine LINK. {STYLE}"),
        ("pass-before-pass", "Work is pass before pass.", f"Two-pass chain only second visible Kit. {STYLE}"),
        ("drop-spin-arrive", "Drop, spin, arrive late.", f"Kit drop spin late box arrival. {STYLE}"),
        ("two-languages-hunger", "Striker hunger, mid patience.", f"Kit two modes HUNGER and PATIENCE. {STYLE}"),
        ("unselfish-tax", "Unselfish skill with tax bill.", f"Assist credit tax bill Kit smiling. {STYLE}"),
    ],
    [
        ("position-ten-9", "Position ten: target striker.", f"Title POSITION 10 TARGET NINE Kit in box. {STYLE}"),
        ("box-office", "Box is your office.", f"Kit in box OFFICE stamp meetings crosses. {STYLE}"),
        ("back-to-goal", "Hold up with back to goal.", f"Kit back to goal shielding midfield far. {STYLE}"),
        ("aerial-wrestling", "Aerial duels like wrestling.", f"Kit header duel wrestling mud. {STYLE}"),
        ("one-touch-luxury", "One touch because two is luxury.", f"Kit one-touch finish TWO TOUCH LUXURY X. {STYLE}"),
        ("two-markers", "Marked by two, expected to score.", f"Two CBs on Kit still expected GOAL. {STYLE}"),
    ],
    [
        ("position-eleven-f9", "Position eleven: false nine.", f"Title POSITION 11 FALSE NINE Kit dropping deep. {STYLE}"),
        ("drop-defenders", "Drop and center-backs freeze.", f"Kit dropping CBs follow or hold dilemma. {STYLE}"),
        ("refuse-stay", "Refuse to stay where nines belong.", f"Kit leaving box on purpose REFUSE STAY. {STYLE}"),
        ("open-lanes", "Pull defenders, open lanes.", f"Defenders pulled winger lane open Kit. {STYLE}"),
        ("less-goals-more-team", "Score less, team scores more.", f"Personal goals down team goals up chart. {STYLE}"),
        ("trade-structure", "Trade your goals for their structure.", f"Kit trading goal icon for shape icon. {STYLE}"),
    ],
    [
        ("position-twelve-hybrid", "Position twelve: hybrid roles.", f"Title POSITION 12 HYBRID Kit multi-role. {STYLE}"),
        ("no-one-name", "Modern football, no one name.", f"Kit shirt with three role labels. {STYLE}"),
        ("heat-map-art", "Heat maps like abstract art.", f"Chaotic heat map Kit abstract art. {STYLE}"),
        ("sheet-suggestion", "Team sheet was a suggestion.", f"Team sheet SUGGESTION stamp shape changed. {STYLE}"),
        ("versatility-currency", "Versatility is currency.", f"Kit juggling winger full-back mid icons. {STYLE}"),
        ("moving-problem", "Eleven people, moving problem.", f"Eleven kits solving moving puzzle pitch. {STYLE}"),
    ],
    [
        ("which-position", "Which position owns you.", f"Kit facing pitch WHICH POSITION stamp. {STYLE}"),
        ("gloves-to-hybrid", "Gloves to hybrid arc.", f"Arc goalkeeper gloves to hybrid shape Kit. {STYLE}"),
        ("sunday-vs-camera", "Sunday role vs camera role.", f"Split SUNDAY ROLE vs CAMERA ROLE Kit. {STYLE}"),
        ("one-role-myth", "One position will not fix you.", f"ONE POSITION FIX MYTH crossed out Kit. {STYLE}"),
        ("comment-position", "Tell me your position.", f"Comment bubble YOUR POSITION Kit POV. {STYLE}"),
        ("every-level-receipt", "Every level POV receipt.", f"EVERY LEVEL POV title Kit mouth closed. {STYLE}"),
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
        title="Your Life as Every Position on a Football Pitch",
        description=(
            "From goalkeeper gloves to false nine drops — your life in every position on the pitch, "
            "cartoon POV, not a tactics lecture."
        ),
        tags=(
            "football positions",
            "goalkeeper",
            "striker",
            "winger",
            "midfielder",
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
        thumbnail_hook="NOT ONE ROLE",
    )
    scenario = build_pov_scenario(
        draft,
        topic="Your Life as Every Position on a Football Pitch",
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
    named = PROJECT_ROOT / "senaryo-pov-positions.json"
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

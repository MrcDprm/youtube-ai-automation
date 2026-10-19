"""Author Every Level POV ep6: Your Life as a Substitute on the Bench."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, pov_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_pov_scenario, write_scenario
from scripts.pov_pacing import EPISODE_CHAPTER_ENERGY, beat_covers

TERMS = ("cartoon pov illustration", "football substitute cartoon")
TARGET_SECONDS = 840.0
MINUTES = 14
PROJECT_ID = "your-life-as-a-substitute-on-the-bench-14dk-20260905"
EPISODE_KEY = "bench-substitute"
VOICE = "en-US-GuyNeural"
RATE = "+2%"
ZOOM = 1.17
SCENE_GAP = 0.25

STYLE = (
    "Bold cartoon POV, thick ink outlines, flat fills of pitch green, stadium amber, cream paper, "
    "tomato red accents, slight paper grain, non-photorealistic, illustrated, first-person football "
    "substitute story, not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, "
    "no photoreal faces, no real club crests, no national flags as identity, no child closeups. "
    "Recurring protagonist Kit: young adult, green hoodie or generic kit, short dark hair, mouth closed."
)

CHAPTERS = [
    """Some players climb a ladder. You climb a bench — and this is your life as a substitute, from a name missing off the team sheet to the player a whole stadium screams for when the game is dying. Not the starting eleven story. Not the highlight-reel hat-trick story. The other one — the one about warm-up bibs, unused numbers, and the specific ache of watching a match you trained all week for from a plastic seat. By the end you will know why impact sub can feel like a compliment and a cage in the same sentence, and why some players spend a career learning to be brilliant in fifteen minutes. Rank one is not even that. Rank one is not being picked at all.""",
    """Rank two. The eighteen. Matchday. Your name is finally on the team sheet, but three lines down from where you wanted it, under a heading nobody puts on a poster: substitutes. You go through the same warm-up as everyone else — sprints, passes, a shot that clips the bar — and then you sit. The bench is colder than the dugout looks on television. You clap goals you wish you scored. You chew gum like it is a job. Ninety minutes pass and your shirt stays as clean as it was in the tunnel. Someone calls that professional. You call it Tuesday.""",
    """Rank three. The eighty-fifth minute. The manager finally says your name, and it does not feel like an opportunity — it feels like an errand. Go and see the game out. Waste a corner in the corner flag. You sprint on with five minutes to make an impression that a whole week of training could not buy you. The ball barely reaches you twice. The final whistle goes and a stranger online writes that you looked lively, which is the kindest insult in football. You learn fast that garbage time is still time, and some careers are built entirely out of other people's leftovers.""",
    """Rank four. The cameo that counts. Seventy-eighth minute, one-nil down, and the manager finally trusts you with more than an errand. You take a touch, drop a shoulder, and the net moves before the crowd finishes reacting to you even entering the pitch. Suddenly the same fans who forgot your name are chanting a nickname you never gave yourself. The headline calls you a super sub. The dressing room calls you lucky. You call it the first proof that fifteen minutes can be worth more than someone else's ninety, if you use every single one of them.""",
    """Rank five. The chant starts before you even move. One-nil down at home, seventy minutes gone, and the crowd turns toward the bench and starts singing your name before the manager has made a decision. It is the strangest kind of power — being wanted more sitting down than most players are wanted playing. You stand up to warm up and the noise doubles. You are not even on the pitch yet and you have already changed the mood of a stadium. That is the day you understand impact substitute is not a consolation prize. It is a specific, rare job, and you are starting to be good at it.""",
    """Rank six. Trust arrives in minutes, not words. The manager stops waiting until the seventy-eighth minute and starts bringing you on in the sixty-fifth, then the sixtieth, like he is quietly admitting the plan changed because of you. Teammates start looking for you differently in the warm-up area, like you are a weapon being loaded rather than a substitute being prepared. You still are not starting. But you are no longer an emergency option — you are a decision the manager makes on purpose, early, because the game might need you before it is desperate.""",
    """Rank seven. A new name arrives in the squad list, expensive and specific, and everyone in the building suddenly discusses your role using the word cover. You watch a player unpack a locker two down from yours who plays your exact position and reads your exact scouting report. Coaches say healthy competition. You hear something closer to a countdown. The label that made you famous — super sub — starts to feel like a ceiling someone built without asking you. You are excellent at fifteen minutes. Now you have to prove you were only ever fifteen minutes because nobody had given you ninety.""",
    """Rank eight. The cup team sheet spells your name in the starting eleven for the first time all season, in a competition some fans call second string and you call oxygen. Rotation policy, the manager says, protecting his words like they might disappoint you. You do not care what the reason is called. You get ninety minutes to remember what a full match feels like in your legs by the sixtieth instead of the first. You are tired in a way that feels like relief. For one Wednesday night, you are not an impact substitute. You are simply a footballer who started.""",
    """Rank nine. The cup start becomes a cup performance nobody expected, and by full time the post-match graphics have your face on them instead of a supporting role in someone else's highlight package. A pundit says the word finally on live television, like your career has been an unopened letter. Your phone fills with messages from people who did not text you after the super-sub goals. It is strange to be praised for ninety minutes the same week you were only trusted with a cup tie because a rotation policy needed a name. You take it anyway. Praise rarely checks its own timing.""",
    """Rank ten. Saturday morning, a teammate pulls up in the warm-up clutching a hamstring, and your entire week turns inside out in the time it takes a physio to jog over. Emergency starter. The manager grabs your arm in the tunnel and says three sentences that used to take him a whole season to say to you. You walk out for kickoff with your heart somewhere near your collarbone, in a league match, in the actual best team you have belonged to, because someone else's body failed at the worst possible moment for them and the best possible moment for you. Football rarely apologizes for how opportunities arrive.""",
    """Rank eleven. Prove-it week becomes prove-it fortnight becomes, quietly, prove-it month. You start Saturday, then the following Saturday, then a midweek game nobody expected you to still be involved in. Journalists stop asking if you can start and start asking if you can start every week, which is a different, heavier question. Your body learns a new rhythm — recovery, prehab, ice, sleep — the maintenance schedule of a starter instead of the sprint-and-wait schedule of a substitute. You are not fully believed yet. But you are no longer a surprise, and in football, stopping being a surprise is its own kind of promotion.""",
    """Rank twelve. The fixture list gives you the derby, ninety minutes, a stadium at a volume you have only ever heard from a bench. No sixty-fifth-minute rescue mission this time — kickoff to final whistle, your name read out first instead of read out as a substitution. You feel every ache of a full match differently when it is earned from minute one, not inherited from someone else's tired legs. You make a mistake in the first half and have to survive it for eighty more minutes instead of ten. That, more than any goal, is what convinces you: you can carry a game, not just finish one.""",
    """Rank thirteen. The team sheet stops surprising anyone, including you. Your name sits inside the strongest eleven the manager can pick, not the emergency eleven he picks when he runs out of choices. The same chant that used to greet you jogging on from the bench now greets you walking out of the tunnel at kickoff, and it sounds different from this side of it — earned instead of urgent. Somewhere a younger player is warming up in your old spot, watching how you move, the way you once watched the starters ahead of you. You do not remember the exact day you stopped being the impact sub. You just noticed, one Saturday, that nobody called you that anymore.""",
    """Rank fourteen. Eighty-second minute, three-one up, and the manager finally takes you off — not because you failed, but because the game is won and a young substitute deserves the same door you were once given. You walk to the bench you used to live on and, for the first time, sit on it as a favor instead of a sentence. You lean over and tell the kid warming up exactly what nobody told you: it is not garbage time, it is your time, use every second of it. He nods like you nodded once, not really believing you yet. So tell me honestly — have you ever been the eighteen, the eighty-fifth minute, or the chant from the bench before anyone let you play? That is the whole ladder. Rank Run POV.""",
]

_REHOOKS = [
    "Some players never even get a plastic seat. You get the seat and want more.",
    "Clean shirt, ninety minutes, professional patience with a name.",
    "Garbage time is still time. Leftovers still feed a career.",
    "Fifteen minutes, one touch, a nickname you never asked for.",
    "Standing up is already a headline before you touch the ball.",
    "Trust now arrives ten minutes earlier than it used to.",
    "A new name in the squad list rewrites your job description.",
    "Second string to some. Oxygen to you.",
    "Finally, said live, like an unopened letter.",
    "Someone else's hamstring becomes your best Saturday.",
    "Stop being a surprise. That is the real promotion.",
    "No rescue mission. Kickoff to final whistle, all yours.",
    "The chant moved from the bench to the tunnel.",
    "The favor, not the sentence. Full circle on a plastic seat.",
]

_CHAPTER_EXTRAS = [
    """This is the ladder nobody draws on a wall chart. Every rank on it still has a shirt number and a heartbeat.""",
    """The dugout looks warm on television. It rarely is.""",
    """Leftover minutes still show up on a highlight reel somewhere. Careers are built out of stranger things.""",
    """A super sub label is earned in seconds and remembered in headlines for years.""",
    """Momentum can start in a crowd's throat before it starts at your feet.""",
    """Minutes are the only currency a manager cannot fake giving you.""",
    """Competition does not knock. It just unpacks a locker near yours.""",
    """A rotation policy is often just a manager's polite word for chance.""",
    """Praise rarely checks whether you were ready for it.""",
    """Opportunity in football is rarely fair. It is simply available.""",
    """A prove-it week becomes a prove-it identity if you survive it twice.""",
    """A full ninety changes how a mistake feels in your legs.""",
    """Nobody announces the day you stop being a substitute. You just notice the silence around the word.""",
    """The bench remembers everyone who ever sat on it, including the version of you that is gone now.""",
]

_CHAPTER_EXTRAS_B = [
    """You know the exact seat number on that bench. You have counted the studs on it more than the goals in the match.""",
    """You learn to retie your boots twice, just to have something to do with your hands.""",
    """You keep the matchball tag from that cameo anyway. Nobody has to know why.""",
    """You save the video for the day you doubt yourself again. You already know that day is coming.""",
    """You mouth the words back at the crowd once, just once, before you catch yourself.""",
    """You stop packing your bag like you might not be needed. Small habits change first.""",
    """You start double-checking your own numbers against his. Old habits from the bench die slow.""",
    """You iron your own boots the night before, a ritual you never needed as a substitute.""",
    """You screenshot the clip before it disappears into someone else's algorithm.""",
    """You warm up twice as fast as usual and still feel late.""",
    """You stop flinching when a journalist says your name into a microphone.""",
    """You replay the mistake in your head longer than you replay anything you did well.""",
    """You catch yourself teaching a younger sub the same trick a senior player once taught you.""",
    """You remember every kind word said to you on that bench, and you say a few back before you leave it.""",
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
        ("bench-ladder-title", "Bench to starter.", f"Title BENCH TO STARTER Kit climbing a stadium bench like a ladder. {STYLE}"),
        ("not-picked", "Name missing off team sheet.", f"Team sheet on wall, Kit's name missing, Kit looking down list. {STYLE}"),
        ("plastic-seat-ache", "Alone on the bench.", f"Kit alone on empty plastic bench seat, stadium lights above. {STYLE}"),
        ("warmup-bib", "Unused warm-up bib.", f"Kit holding an unused orange warm-up bib, staring at pitch. {STYLE}"),
        ("impact-sub-cage", "Compliment and a cage.", f"Word IMPACT SUB half compliment half cage bars around Kit. {STYLE}"),
        ("rank-one-not-picked", "Rank 1: not picked.", f"Title RANK 1 NOT PICKED Kit outside locked dressing room door. {STYLE}"),
    ],
    [
        ("rank-two-eighteen", "Rank 2: the eighteen.", f"Title RANK 2 THE EIGHTEEN team sheet with Kit's name under SUBSTITUTES heading. {STYLE}"),
        ("same-warmup-sprints", "Same warm-up as everyone.", f"Kit doing warmup sprints alone on sideline before kickoff. {STYLE}"),
        ("bench-colder-tv", "Colder than on TV.", f"Kit shivering on real bench vs warm TV bench graphic. {STYLE}"),
        ("clap-goals-envy", "Clapping envied goals.", f"Kit clapping politely while teammates celebrate a goal. {STYLE}"),
        ("clean-shirt-90", "Shirt stays clean.", f"Clock showing 90 minutes, Kit's shirt still spotless. {STYLE}"),
        ("professional-tuesday", "Professional, or Tuesday.", f"Kit shrugging PROFESSIONAL vs TUESDAY caption bubble. {STYLE}"),
    ],
    [
        ("rank-three-85", "Rank 3: 85th minute.", f"Title RANK 3 THE 85TH MINUTE Kit sprinting onto pitch late. {STYLE}"),
        ("go-see-it-out", "Go see it out.", f"Manager pointing GO SEE IT OUT instruction to Kit. {STYLE}"),
        ("waste-corner", "Waste a corner.", f"Kit jogging ball to corner flag wasting time. {STYLE}"),
        ("ball-twice", "Ball reaches you twice.", f"Stat card BALL TOUCHES 2 next to Kit on pitch. {STYLE}"),
        ("looked-lively", "Looked lively.", f"Phone comment LOOKED LIVELY Kit reading with flat expression. {STYLE}"),
        ("leftovers-career", "Careers built on leftovers.", f"Kit holding a tray of leftover minutes like food scraps, football motif. {STYLE}"),
    ],
    [
        ("rank-four-cameo-counts", "Rank 4: cameo that counts.", f"Title RANK 4 THE CAMEO THAT COUNTS Kit entering pitch 78th minute board. {STYLE}"),
        ("touch-shoulder-drop", "Touch, drop the shoulder.", f"Kit dropping shoulder past defender, ball at feet. {STYLE}"),
        ("net-moves", "The net moves.", f"Ball hitting back of net, crowd rising, Kit mid-celebration. {STYLE}"),
        ("nickname-chant", "A nickname you never chose.", f"Crowd banner with nickname Kit never chose. {STYLE}"),
        ("super-sub-headline", "Super sub headline.", f"Newspaper headline SUPER SUB Kit photo. {STYLE}"),
        ("lucky-dressing-room", "Dressing room says lucky.", f"Teammates saying LUCKY speech bubble Kit half-smiling. {STYLE}"),
    ],
    [
        ("rank-five-chant-starts", "Rank 5: the chant starts.", f"Title RANK 5 THE CHANT STARTS Kit hearing crowd turn toward bench. {STYLE}"),
        ("crowd-sings-name", "Crowd sings your name first.", f"Crowd banner singing Kit's name before substitution board raised. {STYLE}"),
        ("stand-to-warmup", "Noise doubles when you stand.", f"Kit standing up to warm up, noise doubling behind him. {STYLE}"),
        ("power-sitting-down", "Power while sitting down.", f"Kit seated on bench glowing like a spotlight, POWER text. {STYLE}"),
        ("not-consolation-prize", "Not a consolation prize.", f"Trophy shaped like a bench labeled NOT A CONSOLATION PRIZE. {STYLE}"),
        ("rare-job-title", "A rare specific job.", f"Business card style card RARE JOB: IMPACT SUB Kit holding it. {STYLE}"),
    ],
    [
        ("rank-six-trust-minutes", "Rank 6: trust in minutes.", f"Title RANK 6 TRUST IN MINUTES clock showing 65 replacing 78. {STYLE}"),
        ("earlier-sub-board", "Brought on earlier.", f"Substitution board showing earlier minute number, Kit ready. {STYLE}"),
        ("teammates-look-differently", "Teammates look differently.", f"Teammates pointing at Kit in warmup area like loading a weapon. {STYLE}"),
        ("weapon-not-emergency", "Weapon, not emergency.", f"Kit glowing like a loaded weapon icon vs dusty emergency exit sign. {STYLE}"),
        ("decision-on-purpose", "A decision made on purpose.", f"Manager notebook circling Kit's name on purpose, early plan. {STYLE}"),
        ("before-desperate", "Before the game is desperate.", f"Clock BEFORE DESPERATE label, Kit calm on bench. {STYLE}"),
    ],
    [
        ("rank-seven-new-name", "Rank 7: the new name.", f"Title RANK 7 THE NEW NAME squad list with unfamiliar name added. {STYLE}"),
        ("locker-two-down", "Locker two down from yours.", f"New player's locker two down from Kit's, same position kit hanging. {STYLE}"),
        ("scouting-report-mirror", "The same scouting report.", f"Two scouting reports side by side identical to Kit's. {STYLE}"),
        ("healthy-competition-word", "Healthy competition.", f"Coach saying HEALTHY COMPETITION speech bubble, Kit uneasy. {STYLE}"),
        ("ceiling-built-without-you", "A ceiling built without you.", f"Kit reaching up hitting invisible ceiling labeled SUPER SUB. {STYLE}"),
        ("prove-more-than-15", "Prove you're more than 15.", f"Kit holding sign PROVE I AM MORE THAN 15 MINUTES. {STYLE}"),
    ],
    [
        ("rank-eight-cup-start", "Rank 8: the cup start.", f"Title RANK 8 THE CUP START team sheet with Kit in starting eleven. {STYLE}"),
        ("rotation-policy-words", "Rotation policy, he says.", f"Manager careful ROTATION POLICY speech bubble to press. {STYLE}"),
        ("full-90-legs", "A full 90 in your legs.", f"Kit legs tired at 60th minute instead of first, sensation lines. {STYLE}"),
        ("tired-relief", "Tired feels like relief.", f"Kit smiling exhausted, TIRED = RELIEF caption. {STYLE}"),
        ("wednesday-night-oxygen", "Oxygen on a Wednesday.", f"Floodlit midweek stadium, OXYGEN word glowing over pitch. {STYLE}"),
        ("simply-a-footballer", "Simply a footballer.", f"Kit standing tall plain jersey no label, SIMPLY A FOOTBALLER. {STYLE}"),
    ],
    [
        ("rank-nine-cup-performance", "Rank 9: the performance.", f"Title RANK 9 THE PERFORMANCE post-match graphic with Kit's face. {STYLE}"),
        ("pundit-finally-word", "Pundit says finally.", f"TV pundit desk saying word FINALLY, Kit on screen. {STYLE}"),
        ("unopened-letter", "An unopened letter.", f"Kit holding an envelope labeled CAREER, finally opened. {STYLE}"),
        ("phone-fills-messages", "Phone fills with messages.", f"Kit's phone overflowing with new congratulation messages. {STYLE}"),
        ("strange-timing-praise", "Strange timing for praise.", f"Calendar page ROTATION POLICY next to trophy PRAISE, confused Kit. {STYLE}"),
        ("praise-no-schedule", "Praise checks no schedule.", f"Kit shrugging PRAISE DOES NOT CHECK TIMING caption. {STYLE}"),
    ],
    [
        ("rank-ten-emergency-start", "Rank 10: emergency start.", f"Title RANK 10 THE EMERGENCY START teammate holding hamstring on pitch. {STYLE}"),
        ("physio-jogs-over", "Physio jogs over.", f"Physio running onto pitch, Kit warming up urgently on sideline. {STYLE}"),
        ("tunnel-three-sentences", "Three sentences in the tunnel.", f"Manager gripping Kit's arm in tunnel, speech bubble three short lines. {STYLE}"),
        ("heart-near-collarbone", "Heart near your collarbone.", f"Kit walking out for kickoff, heart icon glowing near collarbone. {STYLE}"),
        ("best-team-belonged", "Best team you've belonged to.", f"Kit in strongest ever lineup graphic, proud nervous face. {STYLE}"),
        ("opportunity-no-apology", "Opportunity apologizes to no one.", f"Broken hourglass shaped like a leg, OPPORTUNITY text. {STYLE}"),
    ],
    [
        ("rank-eleven-prove-it-month", "Rank 11: prove-it month.", f"Title RANK 11 PROVE IT MONTH calendar with repeated Saturday starts marked. {STYLE}"),
        ("journalists-heavier-question", "A heavier question now.", f"Reporter microphone asking EVERY WEEK question, Kit thinking. {STYLE}"),
        ("recovery-routine-icons", "A starter's recovery routine.", f"Ice bath, sleep, prehab icons around Kit, new starter routine. {STYLE}"),
        ("sprint-and-wait-old", "The old sprint-and-wait.", f"Faded old routine icon SPRINT AND WAIT crossed out. {STYLE}"),
        ("not-fully-believed-yet", "Not fully believed yet.", f"Kit walking past skeptical fan faces, doubt speech bubbles. {STYLE}"),
        ("stop-being-surprise", "No longer a surprise.", f"Newspaper headline NO LONGER A SURPRISE Kit calm confident pose. {STYLE}"),
    ],
    [
        ("rank-twelve-derby-90", "Rank 12: the derby, 90.", f"Title RANK 12 THE DERBY fixture board showing rival club generic crest. {STYLE}"),
        ("name-read-first", "Your name read out first.", f"Stadium announcer board reading Kit's name first in starting lineup. {STYLE}"),
        ("stadium-max-volume", "Stadium at full volume.", f"Packed stadium roaring, sound wave lines, Kit walking out. {STYLE}"),
        ("full-match-ache-earned", "An ache that is earned.", f"Kit's legs aching differently, EARNED label glowing. {STYLE}"),
        ("first-half-mistake", "A first-half mistake.", f"Kit making a mistake, ball slipping past, worried face. {STYLE}"),
        ("survive-eighty-more", "Survive eighty more.", f"Clock ticking 80 minutes remaining, Kit determined resolve pose. {STYLE}"),
    ],
    [
        ("rank-thirteen-nailed-on", "Rank 13: nailed on.", f"Title RANK 13 NAILED ON team sheet with Kit permanently in strongest XI. {STYLE}"),
        ("emergency-vs-strongest", "Strongest, not emergency.", f"Two lineup cards EMERGENCY ELEVEN crossed out, STRONGEST ELEVEN circled. {STYLE}"),
        ("chant-in-tunnel-now", "The chant, now in the tunnel.", f"Kit walking out of tunnel at kickoff to same old chant, now earned. {STYLE}"),
        ("younger-sub-watching", "A younger sub is watching.", f"Young substitute warming up watching Kit's movement closely. {STYLE}"),
        ("watched-starters-mirror", "You once watched the starters.", f"Kit remembering himself once watching starters, mirror flashback. {STYLE}"),
        ("nobody-calls-that-anymore", "Nobody calls you that now.", f"Speech bubble label IMPACT SUB fading away from Kit. {STYLE}"),
    ],
    [
        ("rank-fourteen-full-circle", "Rank 14: full circle.", f"Title RANK 14 FULL CIRCLE clock showing 82nd minute, score 3-1. {STYLE}"),
        ("subbed-off-favor", "Subbed off as a favor.", f"Manager waving Kit off pitch kindly, not urgently, calm smile. {STYLE}"),
        ("sit-as-favor", "Sit as a favor now.", f"Kit sitting on old bench now smiling, FAVOR not SENTENCE caption. {STYLE}"),
        ("tell-the-kid", "Tell the kid the truth.", f"Kit leaning over talking to young sub warming up, advice speech bubble. {STYLE}"),
        ("kid-nods-unsure", "The kid nods, unsure.", f"Young substitute nodding, not fully believing, mirrored Kit memory. {STYLE}"),
        ("comment-hook-ladder", "Which rank were you?", f"Kit pointing at viewer LADDER graphic with comment bubble EVERY LEVEL POV end card. {STYLE}"),
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
        title="Your Life as a Substitute on the Bench",
        description=(
            "The eighteen, the 85th-minute cameo, the super-sub chant, and the long climb to "
            "becoming a starter — your life as a football substitute, cartoon POV."
        ),
        tags=(
            "substitute",
            "impact substitute",
            "super sub",
            "football sub",
            "bench player",
            "football",
            "soccer",
            "pov",
            "cartoon",
            "every level",
            "rank run",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in _full_chapters()
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="BENCH TO STARTER",
    )
    scenario = build_pov_scenario(
        draft,
        topic="Your Life as a Substitute on the Bench",
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
    named = PROJECT_ROOT / "senaryo-pov-bench-substitute.json"
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

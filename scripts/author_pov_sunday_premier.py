"""Author Every Level POV ep3: Your Life from Sunday League to the Premier League."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, pov_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_pov_scenario, write_scenario
from scripts.pov_pacing import EPISODE_CHAPTER_ENERGY, beat_covers

TERMS = ("cartoon pov illustration", "football rank cartoon")
TARGET_SECONDS = 840.0
MINUTES = 14
PROJECT_ID = "your-life-from-sunday-league-to-the-premier-l-14dk-20260902"
EPISODE_KEY = "sunday-premier"
VOICE = "en-US-GuyNeural"
RATE = "+4%"
ZOOM = 1.18
SCENE_GAP = 0.25

STYLE = (
    "Bold cartoon POV, thick ink outlines, flat fills of pitch green, stadium amber, cream paper, "
    "tomato red accents, slight paper grain, non-photorealistic, illustrated, first-person football "
    "climb story, not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, "
    "no photoreal faces, no real club crests, no national flags as identity, no child closeups. "
    "Recurring protagonist Kit: young adult, green hoodie or generic kit, short dark hair, mouth closed."
)

CHAPTERS = [
    """You do not teleport from Sunday mud to Premier League lights. You climb rungs that creak. Each rung has a wage, a pitch, a bus, and a version of you that thinks the next rung will finally feel like the movies. This is your life from Sunday league to the Premier League, and the gap between rung one and rung ten is not talent alone. It is paperwork, rent, injuries, and the slow rewrite of what normal looks like. By the end you will know what changes when subs are collected in a freezer bag and when they are direct-deposited before you wake. Stay. Rung one is not a highlight. Rung one is collecting fifty pence in the rain.""",
    """Rung one. Sunday league. The pitch is a field that was a field yesterday. Someone marks lines with spray paint that washes away by Wednesday. You pay your sub in coins. The manager is also the treasurer. Win and you celebrate with pints you cannot afford twice. Lose and you fix the net because nobody else will. Boots cost more than your wage, which is zero. You work Monday somewhere that does not care you scored. You tell coworkers you have a match and they nod like you said you have a hobby. It is a hobby that hurts. You learn hunger without a nutritionist. You learn pride without a crowd.""",
    """Rung two. Regional step. Travel in a car you share fuel for. Kit almost matches. Opponents know your name from last season's grudge. You get twenty quid petrol money if the treasurer remembered. You still have a day job. You still tape ankles yourself. The pitch might have a stand with twelve people and one dog. You start dreaming in spreadsheets: if I get seen, if I get signed, if I stop being late to night shift because of extra time. The football is faster. The excuses die younger. You are not professional. You are visible on a muddy Tuesday.""",
    """Rung three. Semi-pro. A contract that fits on one page. Wages enough to notice on a payslip, not enough to quit the warehouse. Training twice a week under lights that buzz. Physio is a student with tape and good intentions. You meet players who were academy kids and fell through the floor. You meet players who never went and built legs like tree trunks. Everyone says this is a stepping stone. Some have been stepping for six years. You learn the cruel math: one bad month and the gaffer stops calling. You learn to smile in team photos like the stone is solid.""",
    """Rung four. Full-time lower tier. First time football pays rent if you are careful. Contract you can show your family without laughing. Fans who know your miss from October. Media is a local paper and a forum that hates creatively. You move closer to the ground because travel was killing you. Your apartment is small and honest. You buy boots without checking the bank twice. You still eat pasta before matches because habits survive upgrades. You fear a three-week injury like a recession. Professional now means accountable, not safe.""",
    """Rung five. League Two money. Wage bands you are not allowed to discuss at dinner. Car that is not embarrassing. Agent emails begin. You sign autographs without feeling like a fraud. Training ground has a gym that works. Medical staff exist on matchdays. You play in front of thousands some weeks, hundreds others. The table follows you home on a phone screen. Promotion talk is real money talk. Relegation talk is real fear talk. You start measuring life in windows: two-year deal, one-year option, release clause you finally understand.""",
    """Rung six. League One step up. Salary jumps enough to help family without shouting about it. Apartment with a second room you use for boots and ice packs. Teammates drive better cars and pretend they do not notice the gap. You eat better because the club feeds you on schedule. Recovery is scheduled, not hoped for. Opponents are faster, nastier, smarter. You are not allowed to be ordinary on Saturday. Ordinary gets loaned out. You learn that the rung above is visible from here like a lit window across the street.""",
    """Rung seven. Championship grind. Money that changes what rent means. Stadiums swallow your old Sunday pitch whole. Travel on coaches with your name on the seat. The table is a spreadsheet that follows you into bed. Sell a bad game and social media does not sleep. You earn more than your parents did at your age and that creates a new pressure you cannot explain at home. Friends treat you like a bank with jokes. You are living a life that looks like success on paper and feels like exams every week.""",
    """Promotion night. Playoff final or automatic spot, the rung does not care which story you prefer. Wembley or a Tuesday away, the bus is quiet in a different way. Win and the bank account changes tier before the summer ends. Lose and you pretend the season was still progress. You watch teammates cry in towels that look too small for adults. You learn that one ninety-minute door can upgrade every rung below overnight. Sunday league feels like another person's diary entry.""",
    """Rung eight. Premier League threshold. Even the bench money rewrites your calendar. Medical team, performance staff, security at home you did not ask for. You suit up hours before kickoff. Minutes are rationed. One touch can be a headline. One mistake can be a meme by half time. Teammates earn sums you do not say aloud. You share a dressing room with people who bought houses before twenty-five. You rent and tell yourself patience. The rung is real. The gap inside the rung is also real.""",
    """Rung nine. Premier League starter. Noise hits your chest before the ball moves. Sponsors on your sleeves. Calendar is not yours. Performance data on a tablet before you shower. Win and you are a product. Lose and you are a problem. House deposit becomes possible. Family asks for tickets they do not understand are contracts. You rent quiet because silence is expensive at the top. You are the climb people will use as a montage. You remember Sunday mud when you tie laces in a tunnel that smells like money.""",
    """Rung ten is not a number. It is maintenance. Agents, image rights, tax conversations, transfer windows that feel like job interviews in public. Teammates come and go by plane. You learn that the Premier League pays some people like CEOs and others like managers, same dressing room, same badge, different lives. Pay gaps sit three lockers away. You do not complain out loud. You notice the car park. You notice who flies private and who flies economy next day. The rung did not erase the ladder. It magnified every rung below.""",
    """What the montage skips. Moves every year. Friends left in cities you only visit for fixtures. Relationships strained by schedules written in July. Injuries that downgrade you one rung overnight. Loans that feel like exile. The phone call that says we are going in a different direction. You can climb fast and fall faster. Sunday league taught you to love the game without money. The Premier League teaches you to protect the game because money attached itself like a shadow.""",
    """So which rung are you on. Coins in a freezer bag. Petrol money in an envelope. First payslip. First contract your mum frames. Championship spreadsheet. Premier League bench. Starter tunnel. Tell me where the climb still feels like Sunday morning. Tell me which rung you thought would fix everything and did not. That is the receipt. Rank Run POV.""",
]

_REHOOKS = [
    "Mud first. Lights later. The ladder lies about how clean the top looks.",
    "Freezer bag subs. Cracked handle tea. Pride is optional here.",
    "Bumpy pitch justice. The bus schedule is your contract.",
    "Petrol IOU football. Monday always waits.",
    "First payslip shock. Not enough to quit. Enough to hope.",
    "Framed contract. Mum cries. You still fear Tuesday training.",
    "Spreadsheet pressure. Promotion money haunts every pass.",
    "Premier bench view. Minutes cost more than money here.",
    "Tunnel starter. Noise hits before the ball moves.",
    "Lifestyle jump. Same anxiety. Better kitchen.",
    "Agents like weather. Some help. Some sell storms.",
    "Old mates text when you score. Silence when you don't.",
    "Sunday morning in your head while Premier lights flash.",
    "Comment your rung. The real one — not the highlight.",
]

_CHAPTER_EXTRAS = [
    """Climb stories sell the top rung and hide the middle years. The middle is where most careers live and die. This episode is the middle made visible: wages as numbers, pitches as characters, buses as timelines.""",
    """Sunday league is where you learn the ball is not fair. It does not care about your shift tomorrow. You play anyway because the rung above is a story you tell yourself at half time.""",
    """Regional football is geography with grudges. You lose in towns you cannot spell and remember forever. Petrol money is not income. It is hope with mileage.""",
    """Semi-pro is the limbo rung. Enough money to believe. Not enough to stop being afraid. The warehouse still knows your name on Monday.""",
    """Full-time lower tier is the first time football pays rent and still owns your weekends forever. Small apartment, big relief. You stop calling it a hobby out loud.""",
    """League Two is when agents appear like weather. Contracts get language you need explained. Promotion is not glory yet. It is arithmetic.""",
    """League One is a raise that feels like oxygen. You still share dressing room jokes with players on half your wage. Awkwardness becomes normal.""",
    """Championship money changes what you order without looking at the menu. It does not change the table following you home. Fear scales up with income.""",
    """Promotion is a door, not a gradient. One night can rewrite the ladder below. You stand in a tunnel that is not the Champions League tunnel but feels like a visa stamp.""",
    """Premier League bench is a job with a view. Pay changes life. Minutes stay rationed. You learn to be ready in thirty seconds because the board is a guillotine.""",
    """Starting in the top flight turns your name into a search term. You can afford silence. You cannot afford ordinary Saturdays.""",
    """Inside the Premier League, pay gaps are not abstract. They are parking spaces, holidays, and who pays the bill without thinking. Same tunnel, different tax bracket.""",
    """The montage skips loans, injuries, and the year you almost quit. Real climbs include backward steps. Sunday league still lives in your touch sometimes.""",
    """Rungs are weeks, not medals. Tell me yours honestly. Mud rung counts.""",
]

_CHAPTER_EXTRAS_B = [
    """You will meet players who jumped two rungs on talent and fell one on discipline. The ladder punishes shortcuts.""",
    """Your boss at the day job will ask if you are still doing that football thing. One day the question stops. You miss the simplicity of it.""",
    """Treasurer forgets petrol money once and the whole car goes silent. Small humiliations teach teams faster than tactics.""",
    """Semi-pro photos look professional until you zoom in on the pitch lines. Context is everything on the climb.""",
    """First framed contract on a mum's wall weighs more than the paper. You cry in the car after signing and hate yourself for crying.""",
    """League Two promotion bonus rumors spread faster than truth. You learn to nod and say nothing.""",
    """Better car, same anxiety. The rung upgrades hardware, not nerves.""",
    """Promotion bonus pays for one summer of feeling safe. Then August reminds you the ladder continues.""",
    """Championship bus has your name on the seat. Sunday league had no seats. Progress is petty and beautiful.""",
    """Premier League dressing room coffee tastes the same as semi-pro. Progress is not always sensory.""",
    """You buy your parents dinner and pretend it is normal. It is not normal. It is the climb paying backward.""",
    """Teammate flies private, you fly economy next day. You laugh together because the badge is shared and the bank is not.""",
    """Loan to a smaller club feels like exile and education at once. You either return sharper or broken.""",
    """Comment your rung. Be honest. Nobody starts in the tunnel.""",
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
        ("no-teleport", "You do not teleport from mud to lights.", f"Kit between muddy pitch and bright stadium split screen. {STYLE}"),
        ("rungs-creak", "Rungs that creak.", f"Wooden ladder rungs creaking, Kit climbing cartoon. {STYLE}"),
        ("wage-pitch-bus", "Each rung: wage, pitch, bus.", f"Three icons WAGE PITCH BUS on ladder, Kit pointing. {STYLE}"),
        ("fifty-pence", "Rung one: fifty pence in rain.", f"Coins in rain freezer bag, SUNDAY LEAGUE stamp. {STYLE}"),
        ("subs-bag-pl", "Freezer bag to direct deposit.", f"Freezer bag morphing to bank deposit slip. {STYLE}"),
        ("stay-climb", "Stay for the climb.", f"Kit pointing up ladder STAY text. {STYLE}"),
    ],
    [
        ("rung-one", "Rung one: Sunday league.", f"Title RUNG 1 muddy pitch Kit playing. {STYLE}"),
        ("spray-lines", "Lines with spray paint.", f"Spray paint lines washing away, muddy field. {STYLE}"),
        ("coins-sub", "Pay sub in coins.", f"Kit handing coins SUBS jar, rain. {STYLE}"),
        ("zero-wage", "Wage is zero.", f"Pay slip ZERO, boots expensive beside it. {STYLE}"),
        ("day-job", "Monday job does not care.", f"Kit in work vest with boots in bag Monday. {STYLE}"),
        ("hobby-hurts", "Hobby that hurts.", f"Kit icing ankle HOBBY HURTS stamp. {STYLE}"),
    ],
    [
        ("rung-two", "Rung two: regional step.", f"Title RUNG 2 Kit in almost-matching kit. {STYLE}"),
        ("share-fuel", "Share fuel for the car.", f"Kit splitting petrol money with teammate. {STYLE}"),
        ("twenty-quid", "Twenty quid petrol if remembered.", f"Envelope 20 QUID PETROL maybe. {STYLE}"),
        ("twelve-fans", "Stand with twelve people and a dog.", f"Tiny stand 12 FANS dog silhouette. {STYLE}"),
        ("night-shift", "Late to night shift after extra time.", f"Clock night shift vs extra time conflict. {STYLE}"),
        ("muddy-tuesday", "Visible on a muddy Tuesday.", f"Kit playing muddy Tuesday SCOUT MYTH empty. {STYLE}"),
    ],
    [
        ("rung-three", "Rung three: semi-pro.", f"Title RUNG 3 one-page contract Kit signing. {STYLE}"),
        ("warehouse", "Not enough to quit warehouse.", f"Kit warehouse vest and football boots split. {STYLE}"),
        ("buzz-lights", "Training under buzzing lights.", f"Flickering floodlights Kit training. {STYLE}"),
        ("six-years", "Stepping stone for six years.", f"Calendar six years STEPPING STONE. {STYLE}"),
        ("gaffer-stops", "One bad month, gaffer stops.", f"Phone missed calls fading Kit worried. {STYLE}"),
        ("solid-stone", "Smile like stone is solid.", f"Kit team photo smile stiff. {STYLE}"),
    ],
    [
        ("rung-four", "Rung four: full-time lower tier.", f"Title RUNG 4 contract handshake family. {STYLE}"),
        ("pays-rent", "Football pays rent if careful.", f"Rent bill checkmark wages cover Kit relieved. {STYLE}"),
        ("small-flat", "Small honest apartment.", f"Kit small flat boots by door humble. {STYLE}"),
        ("october-miss", "Fans remember October miss.", f"Forum post OCTOBER MISS Kit shrugging. {STYLE}"),
        ("three-week-injury", "Three-week injury like recession.", f"Injury calendar 3 WEEKS recession metaphor. {STYLE}"),
        ("accountable", "Professional means accountable.", f"ACCOUNTABLE stamp Kit standing tall. {STYLE}"),
    ],
    [
        ("rung-five", "Rung five: League Two.", f"Title RUNG 5 League Two generic badge shape. {STYLE}"),
        ("wage-band", "Wage bands not discussed.", f"Sealed envelope WAGE BAND shhh. {STYLE}"),
        ("car-not-embarrassing", "Car that is not embarrassing.", f"Kit modest car not flashy ok. {STYLE}"),
        ("agent-emails", "Agent emails begin.", f"Laptop agent email inbox Kit reading. {STYLE}"),
        ("promotion-talk", "Promotion talk is money talk.", f"PROMOTION MONEY arrows table talk. {STYLE}"),
        ("two-year-deal", "Two-year deal windows.", f"Contract 2 YEAR OPTION release clause icons. {STYLE}"),
    ],
    [
        ("rung-six", "Rung six: League One.", f"Title RUNG 6 salary jump Kit new flat. {STYLE}"),
        ("second-room", "Second room for boots and ice.", f"Flat second room boots ice packs. {STYLE}"),
        ("car-gap", "Teammates better cars pretend not.", f"Car park modest vs nice cars Kit neutral. {STYLE}"),
        ("club-feeds", "Club feeds you on schedule.", f"Team cafeteria schedule Kit eating on time. {STYLE}"),
        ("lit-window", "Top rung visible like lit window.", f"Lit window across street CHAMPIONSHIP glow. {STYLE}"),
        ("loan-threat", "Ordinary gets loaned out.", f"LOAN arrow Kit warning ordinary. {STYLE}"),
    ],
    [
        ("rung-seven", "Rung seven: Championship.", f"Title RUNG 7 big stadium Kit bus. {STYLE}"),
        ("rent-changes", "Money changes what rent means.", f"Better apartment key RENT UPGRADE. {STYLE}"),
        ("named-seat", "Coach seat with your name.", f"Bus seat NAME TAG Kit night travel. {STYLE}"),
        ("table-in-bed", "Table follows you to bed.", f"Phone league table in bed Kit awake. {STYLE}"),
        ("bank-jokes", "Friends treat you like bank jokes.", f"Friends laughing MONEY jokes Kit awkward smile. {STYLE}"),
        ("exams-weekly", "Success on paper, exams weekly.", f"Report card EXAMS EVERY SATURDAY. {STYLE}"),
    ],
    [
        ("promotion-night", "Promotion night: one door.", f"Title PROMOTION NIGHT Wembley-style arch generic no logos. {STYLE}"),
        ("playoff-final", "Playoff final or automatic spot.", f"Two paths PLAYOFF or AUTO PROMOTION Kit between. {STYLE}"),
        ("quiet-bus", "Bus quiet in a different way.", f"Team bus silent tension Kit staring window. {STYLE}"),
        ("towels-cry", "Teammates cry in small towels.", f"Towels over faces adults crying promotion. {STYLE}"),
        ("ninety-minutes", "One ninety-minute door upgrades all.", f"Door 90 MINUTES UPGRADE ladder below. {STYLE}"),
        ("diary-entry", "Sunday league feels like diary.", f"Old diary SUNDAY LEAGUE distant memory. {STYLE}"),
    ],
    [
        ("rung-eight", "Rung eight: Premier League threshold.", f"Title RUNG 8 tunnel suit Kit bench area. {STYLE}"),
        ("bench-money", "Even bench money rewrites calendar.", f"Calendar rewritten PREMIER LEAGUE PAY. {STYLE}"),
        ("minutes-rationed", "Minutes rationed.", f"Stopwatch MINUTES RATIONED Kit waiting. {STYLE}"),
        ("locker-gap", "Pay gap three lockers away.", f"Three lockers PAY GAP different cars implied. {STYLE}"),
        ("houses-before-25", "Teammates houses before twenty-five.", f"House icons young age Kit renting still. {STYLE}"),
        ("gap-inside", "Gap inside the rung is real.", f"Same tunnel DIFFERENT BANK Kit noticing. {STYLE}"),
    ],
    [
        ("rung-nine", "Rung nine: Premier League starter.", f"Title RUNG 9 Kit starter stadium roar. {STYLE}"),
        ("noise-chest", "Noise hits chest first.", f"Kit hand chest sound waves crowd. {STYLE}"),
        ("sponsor-sleeves", "Sponsors on sleeves.", f"Generic sleeve logos Kit playing. {STYLE}"),
        ("house-deposit", "House deposit becomes possible.", f"House deposit document POSSIBLE stamp. {STYLE}"),
        ("ticket-requests", "Family asks for tickets.", f"Family text TICKETS PLEASE Kit overwhelmed. {STYLE}"),
        ("remember-mud", "Remember Sunday mud in tunnel.", f"Flashback mud to tunnel Kit tying laces. {STYLE}"),
    ],
    [
        ("rung-ten", "Rung ten is maintenance.", f"Title RUNG 10 MAINTENANCE Kit agent meeting. {STYLE}"),
        ("image-rights", "Agents, image rights, tax talk.", f"Documents IMAGE RIGHTS TAX Kit signing. {STYLE}"),
        ("car-park", "Notice the car park.", f"Car park luxury vs normal Kit walking through. {STYLE}"),
        ("fly-private", "Some fly private, some economy.", f"Split plane PRIVATE vs ECONOMY same badge. {STYLE}"),
        ("same-badge", "Same badge, different lives.", f"Same shirt different wallets three players. {STYLE}"),
        ("magnified-ladder", "Premier League magnifies ladder below.", f"Magnifying glass on ladder below Kit top. {STYLE}"),
    ],
    [
        ("montage-skips", "Montage skips moves and injuries.", f"Montage reel with red X moves injuries loans. {STYLE}"),
        ("different-direction", "Different direction phone call.", f"Phone call DIFFERENT DIRECTION Kit stunned. {STYLE}"),
        ("fall-faster", "Climb fast, fall faster.", f"Ladder up arrow down arrow Kit between. {STYLE}"),
        ("love-without-money", "Sunday taught love without money.", f"Kid Kit park joy no money icon. {STYLE}"),
        ("shadow-money", "Money attached like shadow.", f"Kit shadow shaped like money bag. {STYLE}"),
        ("almost-quit", "Year you almost quit.", f"Calendar ALMOST QUIT crossed out kept going. {STYLE}"),
    ],
    [
        ("which-rung", "Which rung are you on.", f"Kit facing ladder WHICH RUNG stamp. {STYLE}"),
        ("coins-to-deposit", "Coins to direct deposit arc.", f"Arc coins freezer bag to bank deposit. {STYLE}"),
        ("mum-frames", "Contract mum frames.", f"Mum silhouette frame contract wall Kit smile. {STYLE}"),
        ("sunday-morning", "Climb still feels like Sunday.", f"Kit Sunday morning coffee muddy boots memory. {STYLE}"),
        ("comment-rung", "Tell me your rung.", f"Comment bubble YOUR RUNG Kit POV. {STYLE}"),
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
        title="Your Life from Sunday League to the Premier League",
        description=(
            "From fifty-pence subs in the rain to Premier League wages — your life on every "
            "rung of the climb, cartoon POV."
        ),
        tags=(
            "sunday league",
            "premier league",
            "football",
            "soccer",
            "pov",
            "climb",
            "cartoon",
            "every level",
            "wages",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in _full_chapters()
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="MUD TO LIGHTS",
    )
    scenario = build_pov_scenario(
        draft,
        topic="Your Life from Sunday League to the Premier League",
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
    named = PROJECT_ROOT / "senaryo-pov-sunday-premier.json"
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

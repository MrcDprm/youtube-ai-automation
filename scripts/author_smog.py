"""Author Drawn Anyway episode 16: Great Smog of London, nineteen fifty two."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 600.0
MINUTES = 9
VOICE = "en-AU-WilliamNeural"
RATE = "+4%"

CHAPTERS = [
    """A city once cancelled an opera because the fog walked indoors and ate the stage. That is not a metaphor, and it is not a gothic cartoon you invented after a trivia night about pea soup. From Friday the fifth of December to Tuesday the ninth of December nineteen fifty two, London sat under a yellow-black mix of smoke and fog so thick that on Sunday visibility was filed down to a foot, and in back streets to about a metre. At Sadler's Wells, on the evening of Monday the eighth, La Traviata was abandoned after the first act because the house could not see the singers. Buses and cars stalled. The Underground still ran. Keep that picture. Then put a red X on the corpse-reel joke. The leftover is not that London invented weather. The leftover is that the good hard coal had been sent abroad to pay wartime debts, and what burned in the grates was nutty slack, a cheap sulphurous stuff, while an anticyclone sat on the city like a lid and refused to let the chimneys have a sky.""",
    """Start with why a pea-souper was supposed to be ordinary. London had been arguing with its own smoke since at least the thirteenth century. John Evelyn published Fumifugium in sixteen sixty one, a book about the inconvenience of the air and smoke of London, which is a sentence three hundred years older than this week and still not a punchline. Londoners knew pea-soupers. This one was denser and longer. A cold snap had people stoking more coal than usual. Better anthracite tended to be exported. Domestic fuel was often nutty slack, low grade, high sulphur, more sulphur dioxide in the plume. Coal-fired stations sat in the Greater London ring: Battersea, Bankside, Fulham, Greenwich, West Ham, Kingston upon Thames. The Met Office later listed, for each smoggy day, on the order of a thousand tonnes of smoke particles, one hundred forty tonnes of hydrochloric acid, fourteen tonnes of fluorine compounds, three hundred seventy tonnes of sulphur dioxide that might become eight hundred tonnes of sulphuric acid. At Battersea, flue-gas washing cooled the exhaust so it did not rise. It slumped. Diesel buses were replacing electric trams, which is a sentence about exhaust you can put on a depot, not a conspiracy. The official idea, if anyone had written one, was: this is weather, and then it will lift, because it always had, and the city had a nickname for it already.""",
    """On the fourth of December an anticyclone settled over a windless London. Cool stagnant air sat under a warmer lid. That is a temperature inversion, a sandwich, not a ghost. Smoke from homes and works, tarry soot, vehicle exhaust, sulphur dioxide, mixed into a persistent smog. The tarry particles gave the mix its greenish-yellow, the pea-soup nickname. No significant wind. The stuff accumulated. E. T. Wilkins, of the Department of Scientific and Industrial Research, later the named officer in charge of atmospheric pollution, said fog, white mist, or grimy smog covered many parts of the British Isles, and in London and the Thames Valley covered upwards of a thousand square miles. It was in London that the effects were greatest. There was initially no panic, because London was famous for fog. Driving became difficult, then sometimes impossible. Public transport other than the Underground halted. Ambulances were strained. Indoor concerts and film screens went dim. Outdoor sport was cancelled. At night, incandescent street bulbs did not punch through. Fluorescent lamps that could were not yet common. Chemists sold smog masks to whoever could buy them, which is a retail sentence standing in for a fuel sentence. A mask is what you sell when you will not move the coal.""",
    """Indoor is the leftover that photographs as a joke and is not one. The smog seeped into halls. Sadler's Wells lost La Traviata after act one. That is a logistics receipt: if the audience cannot see the stage, the opera is a weather instrument. At the Smithfield Show, an agricultural fair, livestock were the first named casualties in the papers: an Aberdeen Angus died, twelve other cattle had to be put down, sixty needed major veterinary treatment, about a hundred more needed minor attention. Do not draw that as a slaughter reel. File it as a showground that was not built for acid air. Walking became shuffling for kerbs. People abandoned cars. Crime in the streets was reported up, which is a newspaper sentence, not a thesis. The week ending the sixth of December, weekly deaths in London were running about the winter average, about nine hundred forty five. The next week they went to two thousand four hundred eighty four. The week after, still high, one thousand five hundred twenty three. There was no influenza epidemic that could carry those numbers. That is Wilkins's later point, and a Commons point. It is not a giggle you get to spend on a tally, and it is not a week you get to file as a long weekend of atmosphere. The singers went home. The tube kept its timetable. The grate kept its slack.""",
    """Here is the leftover that is not a body. Government medical reports in the weeks after estimated up to four thousand dead as a direct result, and about one hundred thousand made ill, especially the very young, the elderly, and people who already had lung or heart trouble. Do not draw those people. In February nineteen fifty three, Labour MP Marcus Lipton told the Commons the fog had caused six thousand deaths and that twenty five thousand more had claimed sickness benefits in London in that period. Wilkins plotted deaths from December through March against the previous winter and found about eight thousand extra beyond the first four thousand, twelve thousand in total. A nineteen ninety influenza story was offered for the later months. Later work, including Bell, Davis, and Fletcher in two thousand four, put the total around twelve thousand, three to four times the first official figure, close to Wilkins. File both numbers. The four thousand is what the government first wrote. The twelve thousand is what the chart kept adding. A city can file a fog as weather while a mortality curve files it as fuel.""",
    """Rehook, because the internet likes a killer fog and a Netflix episode that makes the hospitals a riot. The Crown used the week. Critics said the weather was fair and the politics and the hospital chaos were turned up. File the warning. Harold Macmillan, Minister of Housing and Local Government, later prime minister, was not racing to a new Act. In a memorandum dated the eighteenth of November nineteen fifty three he listed masks and warning signals as things that could look busy, better stoves and smokeless coal as longer studies, and wrote that we cannot do very much, but we can seem to be very busy, and that is half the battle nowadays. He was not satisfied that further general legislation was needed at present. Broad economic considerations, he told the House, would be foolish to disregard. Ian Macleod, Minister of Health, was quoted in the Evening Standard protesting that anyone would think fog had only started in London since he became a minister. That is a ministry defending a calendar. It is not a chemistry lesson.""",
    """Pressure from the press, doctors, the London County Council, and MPs forced a committee. Sir Hugh Beaver chaired the Committee on Air Pollution, appointed in the summer of nineteen fifty three. Beaver was an administrator, not a lifelong smoke scientist. The interim report came in December nineteen fifty three, in plain language, focused on fuel combustion. It said the domestic fire was the biggest single smoke producer, twice as much smoke per coal as industry, lower to the ground. The final report, November nineteen fifty four, offered a plan: smoke control, cleaner fuel, zones. The City of London Various Powers Act nineteen fifty four came first in the Square Mile. The Clean Air Act nineteen fifty six, later extended in nineteen sixty eight, let authorities set smoke control areas, push coke and gas fires, offer money to swap open coal. Central heating was still rare in most homes until the late sixties. Progress was slow enough that another smog sat down in early December nineteen sixty two. A law is not a wind. A zone is not a lid lifting itself. Householders were offered money to swap the open fire, which is a grant standing next to a habit, and habits do not read White Papers on the day they are printed. The Act could name a smoke control area. It could not, on day one, unexport the hard coal that had already left the dock.""",
    """None of this is a hymn to pea soup as folklore, and none of it is a cartoon of Londoners as fools who should have known better than to light a grate in December. They had a cold snap. They had the coal they were sold. They had stations whose washers put the plume back in the street. They had buses on diesel where trams had been electric. They had an inversion that turned five days into a lid. The chemistry is sulphur plus water droplets plus no wind. The logistics is which coal leaves the country, which coal stays in the grate, which flue is cooled until it cannot rise, which minister would rather issue masks than move a fuel market. You are allowed to laugh at an opera that lost its stage. You are not required to laugh at four thousand, or twelve thousand, or at a showground vet list. A pea-souper is a nickname. Nutty slack is a specification. Macmillan's busy is a memo. Wilkins's chart is a remainder.""",
    """So who won. Not the anticyclone. Not the nickname. Not the first press line that this was just weather. The Underground won a week of being the transport that still existed. Sadler's Wells won a cancelled second act, which is a terrible trophy and a perfect receipt. Wilkins won a chart that would not stay at four thousand. Beaver won a committee that named the domestic fire. The Clean Air Act won a four-year delay and then a set of zones. Nutty slack won the grate. Hard coal won the export dock. If you need a moral, skip never live in London. Take this: a lid is a terrible neighbour for a cheap sulphurous fire, and a mask is a terrible instrument for a fuel policy. The next time someone tells you the Great Smog was only fog, ask which coal was at home, and whether the singers could see the pit. Would you have kept burning slack, or would you have kept the hard coal in the grate. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no corpse closeups, no dead cattle, no blood, not mud-green archive night, "
    "not After Hours File dark. Fog shown as a candy yellow-cream pea-soup blob, chimneys, an opera stage, "
    "coal piles, a tube train, a law book, not violence and not bodies. "
    "Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("stage-vanished", "The fog walked indoors and ate the stage.", f"Cartoon title beat: an opera stage vanishing into yellow-cream pea-soup fog, cream paper, candy colors, not dark archive. {STYLE}"),
    ("not-trivia", "Not a gothic pea-soup trivia gag.", f"Ink shaking his head at a TRIVIA FOG stamp with a red X, mouth closed. {STYLE}"),
    ("december-1952", "Friday 5 to Tuesday 9 December 1952, London.", f"A calendar 5-9 DEC 1952, a simple map LONDON, no flag. {STYLE}"),
    ("foot-of-sight", "Sunday: visibility filed down to a foot.", f"A ruler 1 FOOT beside a street lamp in candy yellow fog, no people dying. {STYLE}"),
    ("sadlers-wells", "Sadler's Wells, Monday 8th: La Traviata stopped after act one.", f"A theatre marquee SADLER'S WELLS, TRAVIATA, ABANDONED AFTER ACT 1. {STYLE}"),
    ("tube-ran", "Buses stalled. The Underground still ran.", f"A cartoon tube train TUBE STILL RAN, buses parked above. {STYLE}"),
    ("x-on-corpse-joke", "Put a red X on the corpse-reel joke.", f"A CORPSE REEL stamp with a giant red X. No bodies drawn. {STYLE}"),
    ("nutty-slack", "Good hard coal exported. Homes burned nutty slack.", f"Two coal piles HARD EXPORT vs NUTTY SLACK HOME. {STYLE}"),
    ("evelyn-1661", "John Evelyn, Fumifugium, 1661. Smoke is an old argument.", f"An old book FUMIFUGIUM 1661, a tiny chimney. {STYLE}"),
    ("pea-souper", "London knew pea-soupers. This one was denser and longer.", f"A soup tin PEA-SOUPER, a stamp THIS ONE WORSE. {STYLE}"),
    ("cold-snap", "A cold snap. More coal in the grates.", f"A thermometer low, extra coal scuttles, no people suffering. {STYLE}"),
    ("stations-ring", "Battersea, Bankside, Fulham, Greenwich, West Ham, Kingston.", f"Six power-station nameplates in a ring, chimneys as simple candy stacks. {STYLE}"),
    ("met-office-tonnes", "Met Office: 1000 t smoke, 140 HCl, 370 SO2 a day.", f"A clipboard 1000 SMOKE 140 HCl 370 SO2, MET OFFICE. {STYLE}"),
    ("battersea-slump", "Battersea washers cooled the flue. Smoke slumped.", f"A chimney with a DOWN arrow SLUMP, not a disaster-porn plume. {STYLE}"),
    ("diesel-for-trams", "Diesel buses replacing electric trams.", f"A tram WITHDRAWN, a diesel bus NEW, no flags. {STYLE}"),
    ("official-weather", "Official idea: this is weather, and then it will lift.", f"A clipboard PLAN: WEATHER THEN LIFT, a check mark. {STYLE}"),
    ("anticyclone-lid", "4 December: anticyclone, windless, a temperature inversion.", f"A weather sandwich COLD under WARM, LID stamp, 4 DEC. {STYLE}"),
    ("wilkins-miles", "Wilkins: Thames Valley, upwards of 1000 square miles.", f"A nameplate E.T. WILKINS, a map blob 1000 SQ MI. {STYLE}"),
    ("no-panic-yet", "No panic at first. London was famous for fog.", f"A newspaper JUST FOG, a small question mark. {STYLE}"),
    ("transport-halt", "Surface transport halted. Ambulances strained.", f"Empty bus stops, a small ambulance icon, no crash gore. {STYLE}"),
    ("indoor-screens", "Concerts and film screens went dim indoors.", f"A cinema screen fading into yellow fog, empty seats. {STYLE}"),
    ("sport-off", "Outdoor sport cancelled.", f"A football pitch with a POSTPONED stamp in candy fog. {STYLE}"),
    ("incandescent-night", "Night bulbs did not punch through. Masks at chemists.", f"A weak lamp, a chemist sign SMOG MASKS, no suffering faces. {STYLE}"),
    ("traviata-act-one", "If the audience cannot see, the opera is weather.", f"Singers as tiny silhouettes lost in fog, STAGE EATEN, no photoreal faces. {STYLE}"),
    ("smithfield-report", "Smithfield Show: livestock in the papers. Do not draw slaughter.", f"Empty show-ring pens and a VET BAG, no dead animals. {STYLE}"),
    ("shuffle-kerbs", "Walking became shuffling for kerbs. Cars abandoned.", f"Empty cartoon cars, a kerb, candy fog, no people collapsing. {STYLE}"),
    ("week-nine-forty-five", "Week to 6 Dec: about 945 deaths, winter average.", f"A somber ledger 945 AVERAGE, no bodies. {STYLE}"),
    ("week-two-four-eight-four", "Next week: 2484. Then 1523. Not influenza carrying it.", f"A tally 2484 then 1523, NOT FLU stamp, respectful. {STYLE}"),
    ("four-thousand", "First government figure: up to 4000 dead, 100000 ill.", f"A somber government card 4000 and 100000, no corpses. {STYLE}"),
    ("lipton-1953", "Marcus Lipton, Feb 1953: 6000 dead, 25000 sickness claims.", f"A Commons nameplate MARCUS LIPTON, 6000 and 25000. {STYLE}"),
    ("twelve-thousand", "Wilkins's chart: about 8000 more, 12000 total.", f"A line chart 4000 then 12000, WILKINS, no bodies. {STYLE}"),
    ("bell-davis", "Bell, Davis, Fletcher 2004: around 12000, close to Wilkins.", f"A paper 2004, 12000, a stamp CLOSE TO WILKINS. {STYLE}"),
    ("file-both", "File both numbers. Four thousand is first. Twelve is the remainder.", f"Two folders 4000 FIRST and 12000 REMAINDER. {STYLE}"),
    ("crown-warning", "The Crown used the week. Politics and hospitals were turned up.", f"A TV card THE CROWN, a WARNING not LICENCE stamp. {STYLE}"),
    ("macmillan-busy", "Macmillan memo 18 Nov 1953: seem to be very busy.", f"A memo SEEM BUSY, nameplate HAROLD MACMILLAN, no portrait. {STYLE}"),
    ("no-new-act-yet", "He was not satisfied further general legislation was needed.", f"A bill stamped NOT NEEDED YET, 1953. {STYLE}"),
    ("macleod-fog", "Macleod: as if fog started when he became minister.", f"A nameplate IAN MACLEOD, calendar joke FOG SINCE ME, no portrait. {STYLE}"),
    ("beaver-chair", "Sir Hugh Beaver, Committee on Air Pollution, summer 1953.", f"A nameplate HUGH BEAVER, COMMITTEE, no portrait. {STYLE}"),
    ("domestic-fire", "Interim Dec 1953: the domestic fire, biggest single smoke.", f"A cartoon grate 2X SMOKE vs a factory, DOMESTIC. {STYLE}"),
    ("final-1954", "Final report November 1954: zones, cleaner fuel, a plan.", f"A report NOV 1954, stamps ZONES and CLEANER FUEL. {STYLE}"),
    ("city-act-1954", "City of London Various Powers Act 1954, the Square Mile first.", f"A Square Mile map, ACT 1954, no flag. {STYLE}"),
    ("clean-air-1956", "Clean Air Act 1956, extended 1968. Smoke control areas.", f"A law book CLEAN AIR 1956, 1968 tag. {STYLE}"),
    ("coke-and-grants", "Coke, gas fires, money to swap the open coal.", f"A grant envelope, a coke scuttle replacing a coal grate. {STYLE}"),
    ("sixty-two-again", "Another smog, early December 1962. A law is not a wind.", f"A calendar DEC 1962, AGAIN stamp, candy fog, no bodies. {STYLE}"),
    ("not-folklore", "Not a hymn to pea soup as folklore.", f"Ink peeling a FOLKLORE sticker off a soup tin, mouth closed. {STYLE}"),
    ("slack-is-spec", "A pea-souper is a nickname. Nutty slack is a specification.", f"A nickname tag vs a SPEC sheet NUTTY SLACK. {STYLE}"),
    ("lid-plus-fuel", "Lid plus cheap sulphur fire. Mask vs fuel policy.", f"A weather lid over a grate, a tiny mask with a red X as a fix. {STYLE}"),
    ("masks-not-policy", "A mask is a terrible instrument for a fuel policy.", f"A chemist mask vs a coal barge, the barge labeled POLICY. {STYLE}"),
    ("who-won", "Not the nickname. Tube. Wilkins. Beaver. The Act, late.", f"A tube, a chart, a committee stamp, a law book beating a soup tin. {STYLE}"),
    ("hard-coal-dock", "Hard coal won the export dock. Slack won the grate.", f"A dock HARD COAL vs a home grate SLACK. {STYLE}"),
    ("four-year-delay", "The Clean Air Act won a four-year delay, then zones.", f"A clock 1952 to 1956, then ZONES. {STYLE}"),
    ("which-coal", "Ask which coal was at home, and whether the singers could see.", f"A coal scuttle vs a tiny opera glass, question mark. {STYLE}"),
    ("comment-hook", "Would you have kept burning slack. Tell me in the comments.", f"Ink pointing at the viewer, mouth closed, a tiny grate and a tiny stage. {STYLE}"),
    ("receipt", "A lid, a cheap fire, a cancelled second act. Drawn anyway.", f"A receipt card LID + SLACK = NO ACT TWO, Ink with marker, mouth closed. {STYLE}"),
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
        title="The Fog That Shut the City",
        description=(
            "London, December nineteen fifty two. Nutty slack, a lid of weather, "
            "and an opera that lost its stage."
        ),
        tags=(
            "history",
            "great smog",
            "london",
            "1952",
            "clean air act",
            "cartoon",
            "true story",
            "logistics",
            "pea souper",
            "funny",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="THE STAGE VANISHED",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Fog That Shut the City",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-smog.json"
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

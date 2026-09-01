"""Author episode 13: you stop for a color because a cop's arm became a lamp."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you will sit at a red light with nobody coming. Two in the morning, an empty intersection, a lamp the color of stop hanging over a street that is not arguing with you. You will wait. You will not think of it as a political act. It will feel like traffic doing its job. Here is the part that should bother you. There is no physics in that red. Red does not grab your bumper. Red is a schedule wearing a color, and you treat the color as a cop who never gets tired. For most of the history of corners, a person stood in the mud and decided who got to move. So why do you obey a lamp when the street is empty? Because London tried a gas semaphore that burst, because a policeman in Salt Lake City built a wooden box of red and green, because Cleveland wired a corner in nineteen fourteen and taught a city that a color could replace an arm. That is the whole plot. Your wait is not caution. It is a leftover salute. You still sit. The sit is flattered. That is its job. The empty street did not vote. A lamp did, and then a grid that taught your foot the brake until the brake started calling itself sense. Sense is a word a corner invented so an empty road would still feel like law.""",
    """Start with the older corner, because the lamp stole a whistle and then sold it back as glass. Before cars, a crossing was a negotiation: horses, carts, people on foot, a shout if you were lucky. Then the automobile arrived like a rumor with a horn, and the rumor did not know how to take turns. Cities hired men to stand in the intersection and become a hinge. A hinge with a whistle and a pair of lungs. The job was weather. Rain, soot, a horse that did not agree, a driver who thought money was a turn signal. If your empty red still feels like manners, notice that manners used to have a pulse. A pulse can get tired. A pulse can play favorites. A pulse can be bribed with a nod. The lamp cannot. That is the sales pitch and also the theft. We took discretion, which is a human word, and we put it in a lens. A lens does not know your face. A lens only knows whose turn the clock thinks it is. If you still wave thanks at a green, that wave is a letter to a person who is not there.""",
    """Named corners, because a myth of one inventor is how a lamp gets a halo it did not earn. In eighteen sixty eight, at Bridge Street in Westminster, a railway engineer named J. P. Knight put up a gas-lit semaphore, a railroad idea forced onto a city street. At night it burned gas. In eighteen sixty nine the lamps burst and the officer running it was badly hurt. London went back to men in the road. In nineteen twelve, in Salt Lake City, a policeman named Lester Wire built a wooden box with red and green, a homemade argument against chaos. On the fifth of August, nineteen fourteen, Cleveland switched on an electric traffic signal at Euclid Avenue and East One Hundred Fifth, a design by James Hoge for the American Traffic Signal Company. In nineteen twenty, in Detroit, William Potts added yellow and made a four-way that could talk to four directions at once. In nineteen twenty three Garrett Morgan patented a T-shaped three-position signal and sold the rights to a giant. He did not invent waiting. He patented a cleaner way to say wait, go, and stop being a rumor. The rumor is still in the pole. A pole is a biography that forgot most of its names and kept the color.""",
    """Watch the cop leave the box, because a vertical city of cars needed a hinge that did not sleep. Once the color held, intersections multiplied like a rash of plus signs. The officer's arm became a legend parents told, then a costume, then a photograph in a museum of jobs. I am not giving you a list of firsts. I am pointing at the swap. We took a person who could see a hearse coming and wave it through, and we replaced that seeing with a cycle. A cycle is fair in the way a vending machine is fair. It does not know a funeral. It does not know a kid in the crosswalk who started late. It knows green. Green is a permission slip printed in light. If your city still posts an officer at a parade, that officer is a fossil of judgment. Judgment is expensive. A pole is cheap. Cheap is how a grid stays in the century without hiring a choir of lungs. A choir would at least see a hearse. A pole just waits for the next green and calls the waiting fairness.""",
    """This is the rehook. You think red is a fact, the way gravity is a fact. Red is a policy. In an empty intersection at two in the morning the policy is still on, because the alternative is trusting you, and the city learned not to. Timed corridors, green waves, a sequence that loves a car more than a walker: the lamp is not neutral. It is a budget of seconds. I am not calling you a coward for waiting. I am un-naturing the sit. The sit is Knight's burst lamp wearing a modern lens. The burst said fire is a bad night shift. The lens said color can be law. Law is a feeling when nobody is coming. If you roll through anyway, that is not you inventing physics. That is you admitting the only hurry that counts is the one the camera will not fine. A camera is a cop who learned to sit in a box and never blink. Never blinking is how a policy stays employed after midnight.""",
    """Watch the lock travel. Highways got on-ramps that meter you like a faucet. School zones learned to flash. Pedestrian countdowns turned waiting into a sport with a score. A yellow that used to mean caution became a dare you measure in bumper lengths. Cities sold synchronized greens as a gift to commuters and a shrug to anyone on foot. You still perform the little rituals: stop line, look both ways even when the lamp is green, apologize with a wave when you creep. The rituals are how obedience stays polite. A polite wait is still a wait. If your left-turn arrow still feels like a blessing, notice it is a queue that learned to point. The ground is optional only if the color says so. Optional ground is a city that bet your morning on a timing plan you will never read. Never reading is the modern contract. The contract is hanging over the asphalt as if hanging were free. Hanging is the fee. The fee is a red you treat like weather.""",
    """This is you, already, in the middle of the story. A Tuesday, a red, a street so empty it looks like a drawing. You sit with the radio and stare at the lamp because rolling would feel like a crime with no victim, which is the most modern crime there is. None of this makes you obedient by nature. It makes you a person born after a burst gas lamp and after Cleveland's corner and after yellow learned to be a maybe and after a cop's arm moved into a pole. You can feel both in the same red: relief that you do not have to argue with a horn, and a tiny insult that an empty world still owns your minute. The relief is real. The insult is the salute failing for a second. You paid for a quieter corner with a trust you cannot negotiate. The trust is cheerful. Cheerful is how a schedule stays in the century without looking like a schedule. The lamp still has a color. The color still feels like a person. A person used to have a whistle. Your whistle is the click of the box changing its mind. The click is cheerful. Cheerful is how a missing cop stays in the century without looking missing.""",
    """A city is a pile of permissions with buildings attached. That sentence is rude and almost fair. Take the lamps away and the corner becomes a shouting match nobody wins, or a cop on every plus sign until the payroll breaks. Fire trucks, buses, a person with a cane: the cycle is a diagram of who is allowed to go next, written by someone you will not meet. You still wait. The wait is a vote for a hinge that was sold as safety. I am not telling you to blow the light as a personality. I am telling you the personality was always the swap: a man in the mud, a burst lamp, a wooden box, a wired corner, a yellow maybe. The crowd is still in the intersection. The crowd is you and three other cars treating a color as a treaty. The treaty cannot see a funeral. The timer can, if a human overrode it, which is a sentence maintenance logs are not supposed to hide. A log is a promise in a cabinet you will never open. The cabinet is the real corner. The corner is a costume. Costume is how a plus sign stays in a Tuesday without looking like a dare. The dare is still under the red. The red is still a permission slip you never signed.""",
    """So what did we trade? We traded a corner that had to be argued in real time for a corner that could be timed, fined, and forgotten. That timing is real help: fewer horns, a child who gets a walk signal, an ambulance that can pre-empt the cycle. Help can be a miracle and still be a lamp. We also gained a myth that red is nature, that green is a right, that an empty wait is proof you are good. Good is a word the grid uses. We kept the cop and called it a color. We kept the whistle and called it a countdown. Both can be true and still not be a reason to forget the lamp is a policy that learned manners. Deals can be rewritten. Some already were, quietly, when walk signals got longer and when a flashing yellow meant think. Think is slower than a brake. A brake is a truce you sit in. A truce is not a street that learned to be empty and still kind. Kind would be a different grid. The grid we kept is a pile of people who agreed not to argue with glass.""",
    """This is you. You will put your foot on the pedal. The red will still be there. You will feel nothing, which is the victory. Look at the lamp. That is not the sky and it is not a cop. That is a gas semaphore that burst, a wooden box in Salt Lake, a Cleveland corner in nineteen fourteen, a Detroit yellow, a patent that cleaned up a rumor, a pole that replaced a pair of lungs, and a color that still owns an empty street so you will keep treating glass as law. You are allowed to wait. You are allowed to hate the minute and still sit. Just stop calling the red natural, or inevitable, or proof that you are cautious. Tonight, when nobody is coming, look at it like a leftover salute to an arm that left the box. The salute is cheerful. The empty street is the point. Go when it lets you. Know which color you are still obeying. The wait is cheerful. Cheerful is how a lamp stays in the intersection without looking like a person you used to have to tip.""",
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, five-second cadence)."""
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("empty-red", "You sit at a red light with nobody coming.", "Stickman in a car at a red light, empty street, MS Paint, white background."),
    ("two-am", "Two in the morning. An empty intersection.", "Night clock 2:00, empty crossroads, red lamp, MS Paint."),
    ("lamp-stop", "A lamp the color of stop hanging over the street.", "Hanging red lamp over a simple street, MS Paint."),
    ("you-wait", "You will wait. The street is not arguing.", "Waiting stickman, silent empty road, MS Paint."),
    ("not-political", "You will not think of it as a political act.", "Red light labeled NOT POLITICS, shrugging stickman, MS Paint."),
    ("traffic-job", "It feels like traffic doing its job.", "Smiling traffic lamp, stickman waiting, MS Paint."),
    ("no-physics", "There is no physics in that red.", "Red lamp, PHYSICS with red X, MS Paint."),
    ("no-bumper", "Red does not grab your bumper.", "Red light not grabbing a bumper, MS Paint."),
    ("schedule-color", "Red is a schedule wearing a color.", "Schedule paper wearing a red circle, MS Paint."),
    ("cop-never-tired", "You treat the color as a cop who never gets tired.", "Red lamp in a cop hat, never-tired badge, MS Paint."),
    ("person-mud", "A person stood in the mud and decided who moved.", "Stick cop in mud directing carts, MS Paint."),
    ("why-empty", "Why obey a lamp when the street is empty?", "Empty street, questioning stickman, red lamp, MS Paint."),
    ("london-burst", "London tried a gas semaphore that burst.", "Old gas semaphore lamp bursting, 1868, MS Paint."),
    ("wire-box", "A policeman in Salt Lake built a wooden box of red and green.", "Wooden box red/green, stick cop, MS Paint."),
    ("cleveland-arm", "Cleveland wired a corner. A color replaced an arm.", "Color lamp replacing a cop's arm, 1914, MS Paint."),
    ("not-caution", "Your wait is not caution. It is a leftover salute.", "Wait as a salute to a missing cop, MS Paint."),
    ("empty-no-vote", "The empty street did not vote. A lamp did.", "Lamp ballot beating an empty street, MS Paint."),
    ("brake-sense", "A grid taught your foot the brake until it called itself sense.", "Foot on brake labeled SENSE, MS Paint."),
    ("older-corner", "Start with the older corner.", "Old muddy crossroads, no lamp, MS Paint."),
    ("stole-whistle", "The lamp stole a whistle and sold it back as glass.", "Lamp stealing a whistle, GLASS tag, MS Paint."),
    ("horses-carts", "A crossing was horses, carts, people, a shout.", "Horses carts pedestrians shouting, MS Paint."),
    ("car-rumor", "The automobile arrived like a rumor with a horn.", "Early car with a huge horn, MS Paint."),
    ("no-turns", "The rumor did not know how to take turns.", "Cars overlapping, no turns, MS Paint."),
    ("hired-hinge", "Cities hired men to stand in the intersection and become a hinge.", "Stick cop as a hinge between streets, MS Paint."),
    ("whistle-lungs", "A hinge with a whistle and a pair of lungs.", "Whistle and lungs on a cop stickman, MS Paint."),
    ("job-weather", "The job was weather. Rain, soot, a horse that did not agree.", "Wet cop, soot, stubborn horse, MS Paint."),
    ("money-signal", "A driver who thought money was a turn signal.", "Money waved as a turn signal, MS Paint."),
    ("manners-pulse", "Manners used to have a pulse.", "Manners with a heartbeat, MS Paint."),
    ("pulse-tired", "A pulse can get tired. A pulse can play favorites.", "Tired cop, favorite car waved through, MS Paint."),
    ("pulse-bribed", "A pulse can be bribed with a nod.", "Nod as a bribe, cop winking, MS Paint."),
    ("lamp-cannot", "The lamp cannot. That is the sales pitch and the theft.", "Lamp with NO BRIBE sign, MS Paint."),
    ("discretion-lens", "We put discretion in a lens.", "DISCRETION going into a lamp lens, MS Paint."),
    ("lens-no-face", "A lens does not know your face. It knows the clock's turn.", "Lens ignoring a face, watching a clock, MS Paint."),
    ("named-corners", "Named corners. A myth of one inventor is a halo.", "Halo on a lamp, myth sticker, MS Paint."),
    ("knight-1868", "Eighteen sixty eight, Bridge Street, Westminster, J. P. Knight.", "Gas semaphore, BRIDGE ST 1868, MS Paint."),
    ("railroad-idea", "A railroad idea forced onto a city street.", "Railroad signal standing on a city corner, MS Paint."),
    ("burst-hurt", "Eighteen sixty nine: the lamps burst. The officer was hurt.", "Burst lamp, bandaged stick cop, 1869, MS Paint."),
    ("back-to-men", "London went back to men in the road.", "London street, cop back in the road, MS Paint."),
    ("lester-wire", "Nineteen twelve, Salt Lake City, Lester Wire, wooden box.", "Wooden traffic box 1912, SALT LAKE, MS Paint."),
    ("cleveland-1914", "Fifth of August, nineteen fourteen, Cleveland switches on.", "Cleveland corner lamp turning on, 1914, MS Paint."),
    ("euclid", "Euclid Avenue and East One Hundred Fifth.", "Street signs EUCLID and E 105, lamp, MS Paint."),
    ("james-hoge", "James Hoge, American Traffic Signal Company.", "Simple company box, designer stickman HOGE, MS Paint."),
    ("potts-yellow", "Nineteen twenty Detroit: William Potts adds yellow.", "Four-way lamp, yellow added, 1920, MS Paint."),
    ("morgan-1923", "Nineteen twenty three: Garrett Morgan patents a T-signal.", "T-shaped signal, patent paper 1923, MS Paint."),
    ("sold-rights", "He sold the rights to a giant. He did not invent waiting.", "Patent sold, WAIT already existing, MS Paint."),
    ("cleaner-wait", "A cleaner way to say wait, go, and stop being a rumor.", "WAIT GO STOP as clean labels, MS Paint."),
    ("rumor-pole", "The rumor is still in the pole.", "Rumor cloud inside a traffic pole, MS Paint."),
    ("cop-leaves", "Watch the cop leave the box.", "Cop walking out of a traffic box, MS Paint."),
    ("plus-rash", "Intersections multiplied like a rash of plus signs.", "Many plus-sign corners, MS Paint."),
    ("arm-legend", "The officer's arm became a legend, then a costume.", "Cop arm as a legend then a costume, MS Paint."),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", "FIRSTS list with red X, SWAP arrow, MS Paint."),
    ("hearse-wave", "A person who could see a hearse and wave it through.", "Cop waving a simple hearse, MS Paint."),
    ("replaced-cycle", "We replaced that seeing with a cycle.", "Seeing eye replaced by a cycle arrow, MS Paint."),
    ("vending-fair", "A cycle is fair like a vending machine is fair.", "Lamp as a vending slot, FAIR, MS Paint."),
    ("no-funeral", "It does not know a funeral. It does not know a late kid.", "Funeral and late kid ignored by lamp, MS Paint."),
    ("green-slip", "It knows green. Green is a permission slip in light.", "Green light as a permission slip, MS Paint."),
    ("parade-fossil", "An officer at a parade is a fossil of judgment.", "Parade cop with FOSSIL tag, MS Paint."),
    ("judgment-expensive", "Judgment is expensive. A pole is cheap.", "Price tags: cop vs pole, MS Paint."),
    ("no-choir-lungs", "A grid without a choir of lungs.", "Empty cop hats, city grid, MS Paint."),
    ("rehook-fact", "Rehook: you think red is a fact like gravity.", "Red lamp vs gravity apple, stickman, MS Paint."),
    ("red-policy", "Red is a policy.", "Red lamp stamped POLICY, MS Paint."),
    ("policy-on", "At two in the morning the policy is still on.", "2am empty corner, policy switch ON, MS Paint."),
    ("not-trust-you", "The alternative is trusting you. The city learned not to.", "TRUST YOU with red X, city, MS Paint."),
    ("green-wave", "Timed corridors, green waves that love a car.", "Green wave arrows for cars, MS Paint."),
    ("shrug-walker", "A shrug to anyone on foot.", "Walker shrugged at by a lamp, MS Paint."),
    ("not-neutral", "The lamp is not neutral. It is a budget of seconds.", "Lamp holding a seconds budget, MS Paint."),
    ("un-nature-sit", "Not calling you a coward. Un-naturing the sit.", "NATURE sticker peeling off a sitting car, MS Paint."),
    ("burst-wearing-lens", "The sit is the burst lamp wearing a modern lens.", "Old burst lamp inside a modern lens, MS Paint."),
    ("color-law", "The lens said color can be law.", "Color circle stamped LAW, MS Paint."),
    ("roll-anyway", "If you roll through, that is not inventing physics.", "Car rolling, PHYSICS with red X, MS Paint."),
    ("camera-fine", "The hurry that counts is the one the camera will not fine.", "Camera vs rolling car, FINE, MS Paint."),
    ("camera-cop", "A camera is a cop who learned to sit in a box and never blink.", "Camera in a cop hat, unblinking, MS Paint."),
    ("lock-travel", "Watch the lock travel.", "Traffic lock walking onto a highway, MS Paint."),
    ("ramp-faucet", "On-ramps that meter you like a faucet.", "Ramp as a faucet dripping cars, MS Paint."),
    ("school-flash", "School zones learned to flash.", "School zone lamp flashing, MS Paint."),
    ("countdown-sport", "Pedestrian countdowns turned waiting into a sport.", "Countdown numbers as a scoreboard, MS Paint."),
    ("yellow-dare", "Yellow became a dare measured in bumper lengths.", "Yellow light, bumper measuring tape, MS Paint."),
    ("sync-gift", "Synchronized greens as a gift to commuters.", "Gift box of green lights for cars, MS Paint."),
    ("stop-line", "Stop line. Look both ways even when green.", "Stop line, stickman looking both ways, MS Paint."),
    ("creep-wave", "Apologize with a wave when you creep.", "Creeping car, little wave, MS Paint."),
    ("polite-wait", "Rituals are how obedience stays polite.", "Obedience in a polite hat, MS Paint."),
    ("left-arrow", "A left-turn arrow is a queue that learned to point.", "Left arrow as a pointing queue, MS Paint."),
    ("color-says", "The ground is optional only if the color says so.", "Ground switch locked by a color lamp, MS Paint."),
    ("unread-timing", "A timing plan you will never read.", "Unread TIMING clipboard, MS Paint."),
    ("this-is-you", "This is you. A Tuesday. A red. A street like a drawing.", "Stickman Tuesday car, empty drawn street, red, MS Paint."),
    ("radio-stare", "You sit with the radio and stare at the lamp.", "Stickman, radio, staring at red lamp, MS Paint."),
    ("not-nature-obey", "None of this makes you obedient by nature.", "OBEDIENT NATURE sticker with red X, MS Paint."),
    ("born-after", "Born after a burst lamp, Cleveland, yellow maybe, cop into a pole.", "Timeline: burst, Cleveland, yellow, pole, MS Paint."),
    ("relief-horn", "Relief that you do not have to argue with a horn.", "Horn with a truce flag, MS Paint."),
    ("insult-minute", "A tiny insult that an empty world still owns your minute.", "Empty world holding a minute, insulted stickman, MS Paint."),
    ("salute-fail", "The insult is the salute failing for a second.", "Broken salute, MS Paint."),
    ("quieter-corner", "You paid for a quieter corner with a trust you cannot negotiate.", "Quiet corner for sale, unopened trust, MS Paint."),
    ("cheerful-schedule", "Cheerful is how a schedule stays without looking like a schedule.", "Schedule in a cheerful costume, MS Paint."),
    ("color-person", "The color still feels like a person.", "Red circle with a stick face, MS Paint."),
    ("pile-permissions", "A city is a pile of permissions with buildings attached.", "Permission slips stacked into buildings, MS Paint."),
    ("shouting-match", "Take the lamps away and the corner is a shouting match.", "Corner of shouting cars, no lamps, MS Paint."),
    ("payroll-breaks", "Or a cop on every plus sign until the payroll breaks.", "Too many cops, broken payroll, MS Paint."),
    ("who-next", "Fire truck, bus, cane: a diagram of who goes next.", "Diagram: truck bus cane, MS Paint."),
    ("wait-vote", "The wait is a vote for a hinge sold as safety.", "Wait voting HINGE, safety poster, MS Paint."),
    ("not-blow", "Not telling you to blow the light as a personality.", "Personality hat on a red light with red X, MS Paint."),
    ("swap-personality", "The personality was the swap: mud, burst, box, wire, yellow.", "Five icons of the swap, MS Paint."),
    ("three-cars", "You and three other cars treating a color as a treaty.", "Four cars, color treaty paper, MS Paint."),
    ("treaty-blind", "The treaty cannot see a funeral.", "Treaty paper with closed eyes, MS Paint."),
    ("human-override", "The timer can, if a human overrode it.", "Human hand overriding a timer, MS Paint."),
    ("cabinet-corner", "A log in a cabinet you will never open. The real corner.", "Locked cabinet labeled LOG, MS Paint."),
    ("costume-plus", "Costume is how a plus sign stays in a Tuesday.", "Plus-sign corner in a costume, MS Paint."),
    ("trade-argued", "We traded a corner argued in real time for a timed fined forgotten one.", "Argued corner vs timed fined corner, MS Paint."),
    ("timing-helps", "Fewer horns, a walk signal, an ambulance that can pre-empt.", "Walk signal, ambulance getting green, MS Paint."),
    ("miracle-lamp", "Help can be a miracle and still be a lamp.", "Halo on a traffic lamp, MS Paint."),
    ("red-nature-myth", "A myth that red is nature, that green is a right.", "RED=NATURE myth, GREEN=RIGHT, MS Paint."),
    ("empty-wait-good", "A myth that an empty wait proves you are good.", "GOOD star for waiting at empty red, MS Paint."),
    ("grid-word", "Good is a word the grid uses.", "Grid holding the word GOOD, MS Paint."),
    ("cop-called-color", "We kept the cop and called it a color.", "Cop renamed COLOR, MS Paint."),
    ("whistle-countdown", "We kept the whistle and called it a countdown.", "Whistle renamed 9 8 7, MS Paint."),
    ("policy-manners", "The lamp is a policy that learned manners.", "Policy lamp in a tuxedo, MS Paint."),
    ("walk-longer", "Walk signals got longer. Flashing yellow meant think.", "Longer WALK, flashing yellow THINK, MS Paint."),
    ("think-slower", "Think is slower than a brake. A brake is a truce you sit in.", "THINK turtle vs brake, MS Paint."),
    ("empty-kind", "A truce is not a street that learned to be empty and still kind.", "Empty kind street vs truce, MS Paint."),
    ("foot-pedal", "You put your foot on the pedal. The red will still be there.", "Callback: foot on pedal, red lamp, MS Paint."),
    ("feel-nothing", "You will feel nothing, which is the victory.", "Blank calm face at a red light, MS Paint."),
    ("look-lamp", "Look at the lamp. Not the sky and not a cop.", "Lamp between red-X sky and red-X cop, MS Paint."),
    ("burst-box-cleveland", "Gas semaphore. Wooden box. Cleveland nineteen fourteen.", "Three icons: gas, wood box, 1914 lamp, MS Paint."),
    ("yellow-patent-pole", "Detroit yellow. A patent. A pole that replaced lungs.", "Yellow, patent, pole vs lungs, MS Paint."),
    ("glass-as-law", "A color that owns an empty street so glass stays law.", "Glass lamp stamped LAW over empty street, MS Paint."),
    ("allowed-wait", "You are allowed to wait. Allowed to hate the minute and still sit.", "Waiting stickman, hate-the-minute cloud, MS Paint."),
    ("not-natural", "Stop calling the red natural.", "RED NATURAL sticker with red X, MS Paint."),
    ("not-cautious-proof", "Not proof that you are cautious.", "CAUTIOUS stamp with red X, MS Paint."),
    ("leftover-arm", "A leftover salute to an arm that left the box.", "Salute to an empty cop box, MS Paint."),
    ("empty-is-point", "The salute is cheerful. The empty street is the point.", "Cheerful salute, empty street, MS Paint."),
    ("know-color", "Go when it lets you. Know which color you are still obeying.", "Stickman going on green, color labeled which, MS Paint."),
    ("wait-cheerful", "The wait is cheerful. Cheerful is how a lamp stays without looking like a person to tip.", "Smiling wait, lamp, TIP jar with red X, MS Paint."),
    ("final-callback", "Empty red. London. Cleveland. Your foot.", "Final callback: empty red, two place labels, stickman foot, MS Paint."),
]


def _beats() -> list[tuple[str, str, str]]:
    """Stamp each row with a five-second mmss slug prefix."""
    if len(_ROWS) != paint_beat_count(660.0):
        raise SystemExit(f"need {paint_beat_count(660.0)} beats, got {len(_ROWS)}")
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
        title="Why You Stop for a Color",
        description=(
            "An empty red light feels like caution. It is a leftover salute. "
            "A gas semaphore burst in London, Cleveland wired a corner in "
            "nineteen fourteen, a cop's arm moved into a pole. You still wait."
        ),
        tags=(
            "traffic",
            "signal",
            "history",
            "city",
            "why",
            "red",
            "green",
            "intersection",
            "wait",
            "cop",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="EMPTY RED?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why You Stop for a Color",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-traffic.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))
    print("accent", scenario.subtitles.accent_color, "rate", scenario.tts.rate)
    print("hook", scenario.youtube.thumbnail_hook)


if __name__ == "__main__":
    main()

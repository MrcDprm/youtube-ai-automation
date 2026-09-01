"""Author episode: you open a booklet and treat a border as obvious."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."

CHAPTERS = [
    """Tonight you will open a small booklet and treat a border as obvious. Your thumb will find a photo page as if the airport grew a permission slip because airports do permission slips. Here is the part that should bother you. The first travelers did not agree. Many of them crossed a river with a local letter, a merchant seal, or nothing but a face the guard had seen before. So why does your pocket wear a passport as if the booklet were physics? Because medieval kings already issued safe conducts when roads needed paperwork, because Louis the Fourteenth asked subjects to carry identity papers when cities needed to count who belonged, because the League of Nations standardized the booklet format in nineteen twenty when trains made borders loud, and because states learned that a stamped page is easier to inspect than a memory. That is the whole plot. Your crossing is not freedom by nature. It is a leftover letter that learned to look official. You still present. The presentation is flattered. That is its job. The river did not vote. A clerk did, and then a booklet that taught your hand the stamp until the stamp started calling itself sense. Sense is a word a border invented so a line would still feel like law when the letter was gone.""",
    """Start with the letter, because the passport stole a safe conduct and then sold it back as cardboard. Before photography, before machine-readable zones, before a booklet could host a chip that beeps, crossing a line was a negotiation with a guard you could not schedule. Early travelers carried. Early hosts vouched. Some routes offered nothing but reputation and the social contract that your name matched your face. When booklets arrived, they were honest and suspicious. A page that says bearer may pass is a letter wearing a cover. It does not say the line is real until everyone agrees to treat ink as a gate. If your passport still feels like the only adult option, notice that the adult option started as royal paperwork dragged onto a route that was not a checkpoint. The route did not offer a photo booth. The face still wanted recognition until recognition got tired of being the only system. The face was not a miracle. It was logistics.""",
    """Named corners, because a myth of one inventor is how a booklet gets a halo it did not earn. The passport is not a single eureka moment you can pin on one hero with a plaque. It is a layer cake of safe conducts, identity counts, and a stamped page that behaved nicely when you needed to move a crowd through a booth. In fourteen fourteen, King Henry the Fifth of England issued safe conducts for subjects traveling abroad. In seventeenth century France, Louis the Fourteenth's regime pushed subjects to carry papers that proved who they were. After the First World War, the League of Nations convened in nineteen twenty to agree on a standard passport format so trains would not stall at every redrawn border. If you still treat the booklet as sacred cardboard, file the conference separately from the queue. Your page is a League complaint wearing a century of stamps.""",
    """Watch the letter leave the court, because a horizontal world of trains needed a slip that did not require a king at every crossing. Early border tricks were honest and exhausting. Explain your business. Wait for a seal. Hope the guard remembers your cousin. Repeat. A standardized booklet is a small insult to anonymity with a large gift to the queue. The photo repeats. The number flexes. The stamp says proceed here without asking the traveler to retell a biography at every line. I am not giving you a list of firsts. I am pointing at the swap. We took a face that said trust me and we replaced it with a page that said read this ink. Read is easier to teach in a manual. Read is easier to scan in a booth. Read is easier to repeat when the line speeds up. The line is the real inventor. The line does not care about your nostalgia for an unmarked road. The line cares about booklets that fit and travelers who stay inside the procedure.""",
    """This is the rehook. You think the passport is a fact, the way a door is a fact. The passport is a policy. In a modern terminal the policy is already on, because the alternative is trusting every crossing to a guard's memory and every queue to a story that must be retold before the plane boards. Memory is honest. Booklets are scalable. Scalable is how an identity escapes the local letter and becomes something a state can own in numbers. I am not calling you clumsy for liking a stamp. I am un-naturing the page. The page is a safe conduct wearing a laminate. The laminate said ink can be law. Law is a feeling when your hand finds a booklet without remembering when it learned it. If you have ever crossed somewhere that wanted a paper you did not pack, you know the passport is not physics. It is a compromise that won a bureaucratic vote. A vote is not a river. A vote is a spreadsheet with cardboard and a stamp catalog.""",
    """Watch the stamp travel. Mass bureaucracy did not invent borders. It inventoried the answer. When the same crossing had to repeat across a continent, the booklet became the unit you could print, bind, inspect, and replace without translating a vouching ritual for every guard. Biometric chips, visa pages, e-gates: decades later the booklet could scan and glow, a useful chapter about fibers and databases, not the origin story of the letter itself. Do not make tonight a speech about who deserves to move. Make it about the object: cardboard, photo, stamp, repeat. A catalog is a quiet referendum. If your carry-on has a passport and your history book has a local letter, that gap is not evolution. It is inventory. Inventory is how the past loses a fight without filing a complaint.""",
    """This is you, already, in the middle of the story. A Tuesday, a departure hall, a booklet you have opened a thousand times without thanking a League conference. You present a page because boarding would feel impossible without a stamp, which is the most modern impossibility there is. None of this makes you bureaucratic by nature. It makes you a person born after the nineteen twenty format and after photos learned lamination and after a chip learned to beep at a gate. You can feel both in the same motion: relief that you do not have to retell your life at every booth, and a tiny insult that a royal letter won a pocket slot. The relief is real. The insult is the unmarked road failing for a second in your imagination. You paid for a faster queue with a document you never voted on. The document is cheerful. Cheerful is how a booklet stays in the century without looking like a letter.""",
    """A border is a pile of compromises with a booklet attached. That sentence is rude and almost fair. Take the passport away and the terminal becomes a workshop puzzle nobody wins, or a biography retold at every line until the flight leaves. Photo rules, stamp geometry, binding time, replacement fees: the page is a diagram of how to cross without sending the whole human into the memory story, written by clerks you will not meet. You still present. The presentation is a vote for a slip that was sold as obvious. I am not telling you to hunt for an unmarked road as a personality. I am telling you the personality was always the swap: a local letter, a royal safe conduct, a French identity count, a League format, a laminate that forgot your cousin. The crowd is still in the hall. The crowd is you and a departure board treating paper as a treaty. So what did we trade? We traded a face that told the truth about recognition for a page that could be printed, stamped, and forgotten. That tooling is real help: fewer stories, a guard who keeps a line moving, a crossing you can make with a pocket. Help can be a miracle and still be a part number. We also gained a myth that the passport is nature and the booklet is the only adult crossing. We kept the letter and called it a passport. We kept the road and called it history. Both can be true and still not be a reason to forget the booklet is a policy that learned manners.""",
    """This is you. You will walk to the gate. The booklet will still be there. You will feel nothing, which is the victory. Look at the stamp. That is not the sky and it is not a single hero clerk. That is a local letter, a medieval safe conduct, a French identity paper habit, the League of Nations in nineteen twenty, a laminate that replaced a cousin's memory, a brief later chapter about chips if you must, and a page that still owns your departure hall so you will keep treating cardboard as law. You are allowed to present. You are allowed to hate the queue and still fly. Just stop calling the passport natural, or inevitable, or proof that you are modern. Tonight, when the officer flips a page, look at it like a leftover salute to a letter that left the court. The salute is cheerful. The cardboard is the point. Go when the stamp lets you. Know which booklet you are still obeying.""",
]


def _stamp(index: int) -> str:
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("open-booklet", "Tonight you open a small booklet and treat a border as obvious.", f"Stickman opening booklet BORDER OBVIOUS, {PAINT}"),
    ("thumb-photo", "Your thumb finds a photo page as if the airport grew a permission slip.", f"Thumb on photo page AIRPORT PERMISSION SLIP, {PAINT}"),
    ("airports-slips", "Because airports do permission slips.", f"Airport sprouting permission slip like fruit, {PAINT}"),
    ("first-no-agree", "The first travelers did not agree.", f"Early traveler shaking head at passport, {PAINT}"),
    ("river-letter", "Many crossed with a local letter, a merchant seal, or a face the guard knew.", f"River crossing letter seal face guard, {PAINT}"),
    ("why-pocket-passport", "Why does your pocket wear a passport as if the booklet were physics?", f"Passport stamped PHYSICS question mark, {PAINT}"),
    ("safe-conducts", "Medieval kings issued safe conducts when roads needed paperwork.", f"Medieval king SAFE CONDUCT document, {PAINT}"),
    ("louis-xiv", "Louis the Fourteenth asked subjects to carry identity papers.", f"Louis XIV IDENTITY PAPERS label, {PAINT}"),
    ("league-1920", "The League of Nations standardized the booklet format in nineteen twenty.", f"League of Nations 1920 PASSPORT FORMAT, {PAINT}"),
    ("stamped-page", "States learned a stamped page is easier to inspect than a memory.", f"Stamped page vs MEMORY red X, {PAINT}"),
    ("not-freedom-nature", "Your crossing is not freedom by nature.", f"FREEDOM BY NATURE stamp red X on booklet, {PAINT}"),
    ("letter-official", "A leftover letter that learned to look official.", f"Letter morphing into official booklet, {PAINT}"),
    ("present-flattered", "The presentation is flattered. That is its job.", f"Smiling passport FLATTERED badge, {PAINT}"),
    ("river-no-vote", "The river did not vote. A clerk did.", f"River NO VOTE clerk raising hand, {PAINT}"),
    ("stamp-sense", "The stamp taught your hand until it called itself sense.", f"Hand word SENSE after stamp, {PAINT}"),
    ("start-letter", "Start with the letter.", f"Letter labeled START, {PAINT}"),
    ("passport-stole", "The passport stole a safe conduct and sold it back as cardboard.", f"Safe conduct stolen by cardboard passport, {PAINT}"),
    ("before-photo", "Before photography, before machine-readable zones, before a chip that beeps.", f"Timeline before photo MRZ chip, {PAINT}"),
    ("guard-negotiation", "Crossing was a negotiation with a guard you could not schedule.", f"Traveler negotiating with guard, {PAINT}"),
    ("carry-vouch", "Early travelers carried. Early hosts vouched.", f"Traveler carrying host vouching, {PAINT}"),
    ("reputation-contract", "Some routes offered reputation and the contract your name matched your face.", f"REPUTATION name matches face contract, {PAINT}"),
    ("booklet-suspicious", "When booklets arrived, they were honest and suspicious.", f"Booklet HONEST SUSPICIOUS labels, {PAINT}"),
    ("bearer-pass", "A page that says bearer may pass is a letter wearing a cover.", f"BEARER MAY PASS letter wearing cover, {PAINT}"),
    ("ink-gate", "The line is real until everyone agrees to treat ink as a gate.", f"INK AS GATE agreement stamp, {PAINT}"),
    ("royal-paperwork", "Royal paperwork dragged onto a route not a checkpoint.", f"Royal papers on road NOT CHECKPOINT, {PAINT}"),
    ("face-recognition", "The face still wanted recognition until recognition got tired.", f"Face speech bubble WANT RECOGNITION, {PAINT}"),
    ("face-tired", "Recognition got tired of being the only system.", f"Tired recognition ONLY SYSTEM label, {PAINT}"),
    ("not-miracle", "The face was not a miracle. It was logistics.", f"LOGISTICS stamp on face not miracle, {PAINT}"),
    ("named-corners", "Named corners. One inventor is a halo the booklet did not earn.", f"Halo on passport MYTH sticker, {PAINT}"),
    ("not-one-hero", "The passport is not one eureka moment on a plaque.", f"Hero plaque red X many layers, {PAINT}"),
    ("layer-cake", "Safe conducts, identity counts, stamped page in a crowd.", f"Layer cake safe conduct identity stamp, {PAINT}"),
    ("henry-v-1414", "Fourteen fourteen, King Henry the Fifth issued safe conducts.", f"Henry V 1414 SAFE CONDUCT stamp, {PAINT}"),
    ("france-papers", "Seventeenth century France pushed papers that proved who you were.", f"France 1600s WHO YOU ARE papers, {PAINT}"),
    ("wwi-borders", "After the First World War, borders got loud with trains.", f"Train loud BORDERS after war, {PAINT}"),
    ("league-format", "League of Nations nineteen twenty agreed on standard passport format.", f"League 1920 STANDARD FORMAT handshake, {PAINT}"),
    ("conference-queue", "File the conference separately from the queue.", f"Conference vs QUEUE separate files, {PAINT}"),
    ("league-complaint", "Your page is a League complaint wearing a century of stamps.", f"League complaint wearing stamp century coat, {PAINT}"),
    ("letter-leaves-court", "Watch the letter leave the court.", f"Letter walking away from court, {PAINT}"),
    ("trains-slip", "A world of trains needed a slip without a king at every crossing.", f"Train world slip no king every crossing, {PAINT}"),
    ("explain-seal-hope", "Explain your business. Wait for a seal. Hope the guard remembers. Repeat.", f"Three panel EXPLAIN SEAL HOPE REPEAT, {PAINT}"),
    ("small-insult", "A standardized booklet is a small insult to anonymity.", f"Passport insulting anonymity cloud, {PAINT}"),
    ("photo-repeats", "The photo repeats. The number flexes.", f"Photo repeating number flexing, {PAINT}"),
    ("stamp-proceed", "The stamp says proceed here without retelling a biography.", f"PROCEED HERE stamp no biography, {PAINT}"),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", f"FIRSTS red X SWAP arrow, {PAINT}"),
    ("face-trust", "We took a face that said trust me.", f"Face speech bubble TRUST ME, {PAINT}"),
    ("page-read", "We replaced it with a page that said read this ink.", f"Page READ THIS INK arrow, {PAINT}"),
    ("read-manual", "Read is easier to teach in a manual.", f"Manual teaching READ checkmark, {PAINT}"),
    ("read-booth", "Read is easier to scan in a booth.", f"Booth scanner READ checkmark, {PAINT}"),
    ("line-inventor", "The line is the real inventor.", f"Border line labeled REAL INVENTOR, {PAINT}"),
    ("unmarked-road", "The line does not care about nostalgia for an unmarked road.", f"Unmarked road nostalgia red X, {PAINT}"),
    ("rehook-fact", "You think the passport is a fact, the way a door is a fact.", f"Passport vs door both labeled FACT, {PAINT}"),
    ("passport-policy", "The passport is a policy.", f"POLICY stamp on passport, {PAINT}"),
    ("guard-memory", "The alternative is trusting every crossing to a guard's memory.", f"Guard memory red X booklet wins, {PAINT}"),
    ("memory-honest", "Memory is honest. Booklets are scalable.", f"MEMORY honest BOOKLETS scalable scales, {PAINT}"),
    ("un-naturing", "I am un-naturing the page.", f"Page NATURAL stamp peeling off, {PAINT}"),
    ("conduct-laminate", "The page is a safe conduct wearing a laminate.", f"Safe conduct wearing LAMINATE costume, {PAINT}"),
    ("ink-law", "The laminate said ink can be law.", f"Laminate INK IS LAW stamp, {PAINT}"),
    ("no-paper-packed", "If you crossed somewhere that wanted a paper you did not pack.", f"Crossing wanted paper not packed scene, {PAINT}"),
    ("not-physics", "You know the passport is not physics.", f"PHYSICS stamp red X on passport, {PAINT}"),
    ("bureaucratic-vote", "A compromise that won a bureaucratic vote.", f"Bureaucracy voting for passport wins, {PAINT}"),
    ("spreadsheet-cardboard", "A vote is a spreadsheet with cardboard and a stamp catalog.", f"Spreadsheet cardboard stamp catalog, {PAINT}"),
    ("stamp-travel", "Watch the stamp travel.", f"Stamp traveling across booklet pages, {PAINT}"),
    ("inventoried-answer", "Mass bureaucracy inventoried the answer.", f"Office inventory passport stacks shelf, {PAINT}"),
    ("print-bind-inspect", "Print, bind, inspect, replace without a vouching ritual.", f"PRINT BIND INSPECT REPLACE conveyor, {PAINT}"),
    ("chip-chapter", "Biometric chips, visa pages, e-gates: a later chapter.", f"Chip visa egate LATER CHAPTER, {PAINT}"),
    ("no-deserve-speech", "Do not make tonight a speech about who deserves to move.", f"WHO DESERVES speech red X, {PAINT}"),
    ("object-cardboard", "Make it about the object: cardboard, photo, stamp, repeat.", f"CARDBOARD PHOTO STAMP REPEAT icons, {PAINT}"),
    ("catalog-referendum", "A catalog is a quiet referendum.", f"Quiet catalog REFERENDUM whisper, {PAINT}"),
    ("carryon-vs-letter", "Your carry-on has a passport and your history book has a local letter.", f"Passport vs local letter gap, {PAINT}"),
    ("inventory-fight", "Inventory is how the past loses a fight without filing a complaint.", f"Past losing fight INVENTORY filing cabinet, {PAINT}"),
    ("this-is-you", "This is you, already, in the middle of the story.", f"Stickman labeled THIS IS YOU departure hall, {PAINT}"),
    ("tuesday-present", "A Tuesday, a departure hall, a booklet without thanking a League conference.", f"Tuesday hall booklet no thank you, {PAINT}"),
    ("present-page", "You present a page because boarding would feel impossible without a stamp.", f"Present page IMPOSSIBLE without stamp, {PAINT}"),
    ("modern-impossibility", "The most modern impossibility there is.", f"MODERN IMPOSSIBILITY stamp on gate, {PAINT}"),
    ("after-1920", "Born after the nineteen twenty format.", f"Timeline after 1920 passport format, {PAINT}"),
    ("lamination-chip", "After photos learned lamination and a chip learned to beep.", f"Photo lamination chip beeping, {PAINT}"),
    ("relief-insult", "Relief you do not retell your life, insult a royal letter won.", f"Relief checkmark insult royal letter wins, {PAINT}"),
    ("road-imagination", "The unmarked road failing in your imagination.", f"Ghost unmarked road failing imagination, {PAINT}"),
    ("never-voted", "You paid for a faster queue with a document you never voted on.", f"Faster queue NEVER VOTED stamp, {PAINT}"),
    ("cheerful-booklet", "Cheerful is how a booklet stays without looking like a letter.", f"Smiling booklet letter costume hidden, {PAINT}"),
    ("compromises-border", "A border is a pile of compromises with a booklet attached.", f"Border pile COMPROMISES booklet bolted, {PAINT}"),
    ("take-passport-away", "Take the passport away and the terminal becomes a workshop puzzle.", f"Terminal puzzle nobody wins no passport, {PAINT}"),
    ("photo-stamp-rules", "Photo rules, stamp geometry, binding time, replacement fees.", f"PHOTO RULES STAMP GEOMETRY FEES labels, {PAINT}"),
    ("diagram-cross", "The page is a diagram of how to cross without the memory story.", f"Page diagram CROSS without memory story, {PAINT}"),
    ("present-vote", "The presentation is a vote for a slip sold as obvious.", f"Presentation voting SLIP OBVIOUS, {PAINT}"),
    ("personality-swap", "The personality was always the swap.", f"SWAP arrow local letter to booklet, {PAINT}"),
    ("local-letter", "A local letter, a royal safe conduct.", f"Local letter and safe conduct icons, {PAINT}"),
    ("french-count", "A French identity count, a League format.", f"French count League format icons, {PAINT}"),
    ("laminate-cousin", "A laminate that forgot your cousin.", f"Laminate forgetting cousin ghost, {PAINT}"),
    ("treaty-crowd", "You and a departure board treating paper as a treaty.", f"Departure board paper TREATY handshake, {PAINT}"),
    ("what-we-traded", "We traded a face that told the truth about recognition.", f"Face truth RECOGNITION traded away, {PAINT}"),
    ("printed-stamped", "For a page that could be printed, stamped, and forgotten.", f"Printed stamped forgotten page on line, {PAINT}"),
    ("real-help", "Real help: fewer stories, a line moving, a crossing from a pocket.", f"Fewer stories line moving POCKET crossing, {PAINT}"),
    ("miracle-part-number", "Help can be a miracle and still be a part number.", f"MIRACLE and PART NUMBER both true, {PAINT}"),
    ("myth-nature", "A myth that the passport is nature and the booklet is the only adult crossing.", f"MYTH NATURE ADULT CROSSING stamps, {PAINT}"),
    ("letter-passport", "We kept the letter and called it a passport.", f"Letter wearing PASSPORT name tag, {PAINT}"),
    ("road-history", "We kept the road and called it history.", f"Road labeled HISTORY museum, {PAINT}"),
    ("policy-manners", "The booklet is a policy that learned manners.", f"Policy passport in polite bow tie, {PAINT}"),
    ("seal-era", "There was an era when the royal seal was the whole sermon.", f"Royal seal preaching WHOLE SERMON label, {PAINT}"),
    ("border-separate", "A border line arrived as a separate homework assignment.", f"Border line SEPARATE HOMEWORK label, {PAINT}"),
    ("flip-sound", "The page flip is a contract your ears learned to trust.", f"Page flip sound CONTRACT ears trust, {PAINT}"),
    ("cardboard-wear", "Cardboard wears, stamps fade, the procedure stays.", f"Worn cardboard faded stamp PROCEDURE stays, {PAINT}"),
    ("regulators-shelf", "Regulators did not invent the booklet. They shelved it.", f"Regulator placing passport on SHELF not invent, {PAINT}"),
    ("fleet-treaty", "A departure hall is a treaty written in identical booklets.", f"Identical passports TREATY label, {PAINT}"),
    ("hand-memory", "Your hand remembers a booklet you never chose.", f"Hand with booklet MEMORY ghost, {PAINT}"),
    ("letter-ghost", "The local letter is still a ghost in every pocket.", f"Local letter ghost in pocket, {PAINT}"),
    ("cardboard-cheerful", "Cardboard is cheerful. Cheerful is how policy wears a page.", f"Cheerful cardboard page POLICY costume, {PAINT}"),
    ("present-before-gate", "You present before you gate as if gating required permission.", f"Present then GATE PERMISSION stamp, {PAINT}"),
    ("layout-cardboard", "A pile of people who agreed not to argue with cardboard.", f"People nodding at cardboard no argue, {PAINT}"),
    ("walk-gate", "You will walk to the gate. The booklet will still be there.", f"Callback walking gate booklet in hand, {PAINT}"),
    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at stamp, {PAINT}"),
    ("look-stamp", "Look at the stamp. Not the sky and not a single hero clerk.", f"Stamp between red X sky and red X hero, {PAINT}"),
    ("named-stack", "Local letter, safe conduct, French papers, League nineteen twenty, laminate.", f"Stack icons letter conduct France league laminate, {PAINT}"),
    ("page-law", "A page that owns your departure hall so cardboard stays law.", f"Departure hall page stamped LAW, {PAINT}"),
    ("allowed-present", "You are allowed to present. Allowed to hate the queue and still fly.", f"Present ok hate queue still flying, {PAINT}"),
    ("not-natural", "Stop calling the passport natural.", f"NATURAL stamp red X on passport, {PAINT}"),
    ("not-inevitable", "Not inevitable. Not proof you are modern.", f"INEVITABLE MODERN stamps red X, {PAINT}"),
    ("leftover-letter", "A leftover salute to a letter that left the court.", f"Salute to letter leaving court, {PAINT}"),
    ("cardboard-point", "The salute is cheerful. The cardboard is the point.", f"Cheerful salute on cardboard passport, {PAINT}"),
    ("know-booklet", "Go when the stamp lets you. Know which booklet you are still obeying.", f"Stickman at gate passport labeled which booklet, {PAINT}"),
    ("glance-cheerful", "Cheerful is how a booklet stays without looking like a letter.", f"Smiling booklet letter ghost hidden, {PAINT}"),
    ("train-redrawn", "Trains made borders loud when maps kept getting redrawn.", f"Train loud borders maps redrawn, {PAINT}"),
    ("merchant-seal", "A merchant seal was a handshake you could carry in a pocket.", f"Merchant seal POCKET HANDSHAKE label, {PAINT}"),
    ("checkpoint-invented", "The checkpoint was invented after the line needed counting.", f"Checkpoint invented after LINE NEEDS COUNT, {PAINT}"),
    ("photo-booth", "The photo booth is a machine that turns a face into paperwork.", f"Photo booth FACE TO PAPERWORK machine, {PAINT}"),
    ("booth-speed", "A booth is a machine for turning ink into speed.", f"Booth machine INK TO SPEED, {PAINT}"),
    ("binding-thread", "Thread and glue are the quiet parliament of a passport.", f"Thread glue QUIET PARLIAMENT passport, {PAINT}"),
    ("cousin-memory", "The guard remembered your cousin until the stamp replaced memory.", f"Cousin MEMORY replaced by stamp, {PAINT}"),
    ("gate-beep", "The gate beeps because the booklet learned electronics.", f"Gate beeping booklet learned electronics, {PAINT}"),
    ("visa-extra", "A visa page is homework the booklet forgot to do at home.", f"Visa page HOMEWORK NOT DONE AT HOME, {PAINT}"),
    ("queue-physics", "The queue is not physics. It is paperwork with chairs.", f"QUEUE stamp red X paperwork with chairs, {PAINT}"),
    ("final-callback", "A letter. A conference. Your booklet.", f"Final callback letter CONFERENCE YOUR BOOKLET, {PAINT}"),
]


def _beats() -> list[tuple[str, str, str]]:
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
        title="Why a Booklet Lets You Cross a Line",
        description=(
            "Your passport feels obvious. Early travelers used local letters and safe conducts. "
            "The League of Nations standardized the booklet in nineteen twenty. "
            "The stamp is logistics."
        ),
        tags=(
            "passport",
            "border",
            "travel",
            "league of nations",
            "history",
            "why",
            "document",
            "identity",
            "safe conduct",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="PAPER LINE?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why a Booklet Lets You Cross a Line",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-passport.json"
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
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))
    print("accent", scenario.subtitles.accent_color, "rate", scenario.tts.rate)
    print("hook", scenario.youtube.thumbnail_hook)
    print("tsv", tsv)


if __name__ == "__main__":
    main()

"""Author episode: you hand a bill and treat a promise as obvious."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."

CHAPTERS = [
    """Tonight you will hand a rectangle of paper and treat a promise as obvious. Your fingers will find a portrait and a number as if the wallet grew a spell because wallets do spells. Here is the part that should bother you. The first markets did not agree. Many of them paid in metal you could weigh, salt you could lick, or grain you could carry until your back filed a complaint. So why does your pocket wear a bill as if the bill were physics? Because Song Dynasty merchants already printed jiaozi when copper coins were too heavy to haul, because London goldsmiths wrote receipts when vaults were safer than saddlebags, because the Bank of England learned to issue notes when a war needed credit faster than a mine could dig, and because factories learned that a standardized promise is easier to count than a room full of silver. That is the whole plot. Your spend is not value by nature. It is a leftover receipt that learned to circulate. You still pay. The payment is flattered. That is its job. The market did not vote. A clerk did, and then a note that taught your hand the rectangle until the rectangle started calling itself sense. Sense is a word a promise invented so a debt would still feel like law when the vault was gone.""",
    """Start with the weight, because the bill stole a receipt and then sold it back as cotton. Before printing presses, before central banks, before a wallet could host twenty denominations without hernia, buying a thing was a negotiation with mass you could not ignore. Early traders counted. Early buyers bit metal to test it. Some markets offered nothing but trust and the social contract that your coin was not shaved. When paper arrived, it was honest and suspicious. A note that says pay the bearer is a promise wearing ink. It does not say the promise is true until everyone agrees to pretend together. If your bill still feels like the only adult option, notice that the adult option started as warehouse paperwork dragged onto a street that was not a vault. The street did not offer a scale. The coin still wanted weighing. Weighing wanted a human arm until the human arm got tired of being the only cashier. The arm was not a miracle. It was logistics.""",
    """Named corners, because a myth of one inventor is how a rectangle gets a halo it did not earn. Jiaozi was not the only paper that looked at heavy copper and thought the joke was bad. It was an early loud example with a dynasty behind it. In the eleventh century, merchants in Sichuan traded printed notes backed by deposits because strings of cash were a back injury waiting to happen. The Song government eventually took over issuance around ten twenty three, which is the quiet way a crisis teaches a state what normal means. Across centuries and continents, goldsmiths in London wrote receipts for gold left in their vaults, and those receipts began to change hands without the gold moving, which is the other quiet way a vault teaches a city what speed means. The Bank of England, chartered in sixteen ninety four, joined the habit. If you still treat the bill as a single eureka moment, file the hero separately from the ink. Your rectangle is a Song merchant complaint wearing a century of cotton.""",
    """Watch the promise leave the vault, because a horizontal city of trade needed a slip that did not require a mule for every purchase. Early payment tricks were honest and exhausting. Carry the silver. Weigh the silver. Argue about the silver. Repeat. A transferable note is a small insult to mass with a large gift to the counter. The paper flexes across hands. The signature repeats. The seal says trust here without asking the buyer to melt a coin before every loaf. I am not giving you a list of firsts. I am pointing at the swap. We took a vault that said come back with weight and we replaced it with a note that said believe this ink. Believe is easier to teach in a market. Believe is easier to print in a run. Believe is easier to repeat when the line speeds up. The line is the real inventor. The line does not care about your nostalgia for a purse full of metal. The line cares about notes that fit and traders who stay inside the agreement.""",
    """This is the rehook. You think the bill is a fact, the way a door is a fact. The bill is a policy. In a modern city the policy is already on, because the alternative is trusting every buyer to carry bullion to a grocery line and every seller to weigh it before the ice cream melts. Metal is honest. Notes are scalable. Scalable is how a promise escapes the strongroom and becomes something a city can own in numbers. I am not calling you clumsy for liking a rectangle. I am un-naturing the portrait. The portrait is a receipt wearing a denomination. The denomination said trust can be law. Law is a feeling when your hand finds a bill without remembering when it learned it. If you have ever paid somewhere that wanted exact change because cards were down, you know the note is not physics. It is a compromise that won a production vote. A vote is not a coin. A vote is a spreadsheet with cotton and a serial number catalog.""",
    """Watch the ink travel. Mass production did not invent trade. It inventoried the answer. When the same purchase had to repeat across a city, the note became the unit you could print, serial, ship, and replace without translating a weighing ritual for every stall. Central banks, reserve ratios, anti-counterfeit threads: decades later the paper could glow under a lamp, a useful chapter about fibers and enforcement, not the origin story of the promise itself. Do not make tonight a lecture about shadowy cabals. Make it about the object: cotton, ink, signature, repeat. A catalog is a quiet referendum. If your wallet has a bill and your history book has a scale, that gap is not evolution. It is inventory. Inventory is how the past loses a fight without filing a complaint.""",
    """This is you, already, in the middle of the story. A Tuesday, a counter, a handoff you have performed a thousand times without thanking a Song merchant. You reach for paper because leaving would feel awkward without a rectangle, which is the most modern impossibility there is. None of this makes you gullible by nature. It makes you a person born after jiaozi and after goldsmith receipts and after a central bank learned to host denominations that multiply. You can feel both in the same motion: relief that you do not have to weigh metal before every coffee, and a tiny insult that a warehouse note won a wallet slot. The relief is real. The insult is the coin purse failing for a second in your imagination. You paid for speed with a promise you never voted on. The promise is cheerful. Cheerful is how a bill stays in the century without looking like a receipt.""",
    """A market is a pile of compromises with a promise attached. That sentence is rude and almost fair. Take the bill away and the checkout becomes a workshop puzzle nobody wins, or a scale on every counter until the queue breaks. Signatures, serial numbers, printing plates, replacement notes: the rectangle is a diagram of how to trade without moving the whole vault, written by clerks you will not meet. You still pay. The payment is a vote for a slip that was sold as obvious. I am not telling you to hunt for a coin purse as a personality. I am telling you the personality was always the swap: heavy copper, a Sichuan jiaozi, a London goldsmith receipt, a Bank of England charter, a central bank plate, a thread that forgot your scale. The crowd is still at the counter. The crowd is you and a city treating paper as a treaty. So what did we trade? We traded weight that told the truth about value for a note that could be printed, numbered, and forgotten. That tooling is real help: fewer mules, a seller who keeps a line moving, a purchase you can make with a pocket. Help can be a miracle and still be a part number. We also gained a myth that the bill is nature and the rectangle is the only adult pay. We kept the receipt and called it money. We kept the coin and called it history. Both can be true and still not be a reason to forget the bill is a policy that learned manners.""",
    """This is you. You will walk to the register. The rectangle will still be there. You will feel nothing, which is the victory. Look at the portrait. That is not the sky and it is not a single hero inventor. That is heavy copper, a Song jiaozi around ten twenty three, a London goldsmith vault receipt, the Bank of England in sixteen ninety four, a printing plate that replaced a scale, a brief later chapter about glowing threads if you must, and a promise that still owns your checkout so you will keep treating ink as law. You are allowed to pay. You are allowed to hate inflation and still buy lunch. Just stop calling the bill natural, or inevitable, or proof that you are modern. Tonight, when the clerk takes the note, look at it like a leftover salute to a vault that stayed shut. The salute is cheerful. The cotton is the point. Go when the promise lets you. Know which receipt you are still obeying.""",
]


def _stamp(index: int) -> str:
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


_ROWS: list[tuple[str, str, str]] = [
    ("hand-bill", "Tonight you hand a rectangle of paper and treat a promise as obvious.", f"Stickman handing paper bill PROMISE OBVIOUS, {PAINT}"),
    ("fingers-portrait", "Your fingers find a portrait and a number as if the wallet grew a spell.", f"Fingers on bill portrait WALLET SPELL label, {PAINT}"),
    ("wallets-spells", "Because wallets do spells.", f"Wallet sprouting spell like fruit, {PAINT}"),
    ("first-no-agree", "The first markets did not agree.", f"Early trader shaking head at paper, {PAINT}"),
    ("metal-salt-grain", "Many paid in metal you could weigh, salt you could lick, or grain you could carry.", f"Metal salt grain payment options, {PAINT}"),
    ("why-pocket-bill", "Why does your pocket wear a bill as if the bill were physics?", f"Bill stamped PHYSICS with question mark, {PAINT}"),
    ("song-jiaozi", "Song Dynasty merchants printed jiaozi when copper coins were too heavy.", f"JIAOZI label heavy copper coins, {PAINT}"),
    ("goldsmith-receipts", "London goldsmiths wrote receipts when vaults were safer than saddlebags.", f"Goldsmith vault receipt safer than saddlebag, {PAINT}"),
    ("bank-england", "The Bank of England learned to issue notes when war needed credit faster than a mine.", f"Bank of England 1694 notes war credit, {PAINT}"),
    ("standard-promise", "Factories learned a standardized promise is easier to count than a room of silver.", f"Standard notes vs room of silver easier, {PAINT}"),
    ("not-value-nature", "Your spend is not value by nature.", f"VALUE BY NATURE stamp red X on bill, {PAINT}"),
    ("receipt-circulate", "A leftover receipt that learned to circulate.", f"Receipt morphing into circulating bill, {PAINT}"),
    ("payment-flattered", "The payment is flattered. That is its job.", f"Smiling bill FLATTERED badge, {PAINT}"),
    ("market-no-vote", "The market did not vote. A clerk did.", f"Market NO VOTE clerk raising hand, {PAINT}"),
    ("rectangle-sense", "The rectangle taught your hand until it called itself sense.", f"Hand word SENSE after rectangle, {PAINT}"),
    ("start-weight", "Start with the weight.", f"Scale weight labeled START, {PAINT}"),
    ("bill-stole-receipt", "The bill stole a receipt and sold it back as cotton.", f"Receipt stolen by cotton bill, {PAINT}"),
    ("before-presses", "Before printing presses, before central banks, before twenty denominations.", f"Timeline before press central bank denominations, {PAINT}"),
    ("mass-negotiation", "Buying was a negotiation with mass you could not ignore.", f"Buyer negotiating with heavy MASS, {PAINT}"),
    ("count-bite", "Early traders counted. Early buyers bit metal to test it.", f"Counting coins biting metal test, {PAINT}"),
    ("trust-coin", "Some markets offered trust and the social contract your coin was not shaved.", f"TRUST coin not shaved contract, {PAINT}"),
    ("paper-suspicious", "When paper arrived, it was honest and suspicious.", f"Paper HONEST SUSPICIOUS labels, {PAINT}"),
    ("pay-bearer", "A note that says pay the bearer is a promise wearing ink.", f"PAY BEARER promise wearing ink coat, {PAINT}"),
    ("pretend-together", "The promise is true until everyone agrees to pretend together.", f"People agreeing PRETEND TOGETHER, {PAINT}"),
    ("warehouse-paperwork", "Warehouse paperwork dragged onto a street not a vault.", f"Warehouse papers on street NOT VAULT, {PAINT}"),
    ("coin-wanted-weighing", "The coin still wanted weighing.", f"Coin speech bubble WANT WEIGHING, {PAINT}"),
    ("arm-tired", "Weighing wanted a human arm until the arm got tired of being the only cashier.", f"Tired arm ONLY CASHIER label, {PAINT}"),
    ("not-miracle", "The arm was not a miracle. It was logistics.", f"LOGISTICS stamp on arm not miracle, {PAINT}"),
    ("named-corners", "Named corners. One inventor is a halo the rectangle did not earn.", f"Halo on bill MYTH sticker, {PAINT}"),
    ("not-only-paper", "Jiaozi was not the only paper that looked at heavy copper.", f"Many papers one loud JIAOZI, {PAINT}"),
    ("dynasty-behind", "An early loud example with a dynasty behind it.", f"Loud example DYNASTY BEHIND label, {PAINT}"),
    ("eleventh-sichuan", "Eleventh century, merchants in Sichuan traded printed notes.", f"Sichuan 11th century printed notes, {PAINT}"),
    ("strings-cash", "Strings of cash were a back injury waiting to happen.", f"Heavy string of coins BACK INJURY label, {PAINT}"),
    ("song-1023", "The Song government took over issuance around ten twenty three.", f"Calendar 1023 SONG ISSUANCE stamp, {PAINT}"),
    ("crisis-teaches", "The quiet way a crisis teaches a state what normal means.", f"Crisis teaching state NORMAL arrow, {PAINT}"),
    ("london-goldsmith", "Goldsmiths in London wrote receipts for gold in vaults.", f"London goldsmith vault receipt, {PAINT}"),
    ("receipts-change-hands", "Receipts changed hands without the gold moving.", f"Receipt changing hands gold stays vault, {PAINT}"),
    ("vault-teaches-speed", "The quiet way a vault teaches a city what speed means.", f"Vault teaching city SPEED label, {PAINT}"),
    ("bank-charter", "Bank of England chartered in sixteen ninety four joined the habit.", f"Bank of England 1694 CHARTER stamp, {PAINT}"),
    ("song-complaint", "Your rectangle is a Song merchant complaint wearing a century of cotton.", f"Song merchant complaint wearing cotton century coat, {PAINT}"),
    ("promise-leaves-vault", "Watch the promise leave the vault.", f"Promise walking away from vault, {PAINT}"),
    ("trade-no-mule", "A city of trade needed a slip without a mule for every purchase.", f"Slip safe vs mule every purchase red X, {PAINT}"),
    ("carry-weigh-argue", "Carry the silver. Weigh the silver. Argue. Repeat.", f"Three panel CARRY WEIGH ARGUE REPEAT, {PAINT}"),
    ("small-insult", "A transferable note is a small insult to mass.", f"Note insulting heavy mass cloud, {PAINT}"),
    ("paper-flexes", "The paper flexes across hands. The signature repeats.", f"Bill flexing across many hands signature, {PAINT}"),
    ("seal-trust", "The seal says trust here without melting a coin before every loaf.", f"Seal TRUST HERE no melting coin, {PAINT}"),
    ("not-firsts", "Not a list of firsts. Pointing at the swap.", f"FIRSTS red X SWAP arrow, {PAINT}"),
    ("vault-come-back", "We took a vault that said come back with weight.", f"Vault speech bubble COME BACK WITH WEIGHT, {PAINT}"),
    ("note-believe", "We replaced it with a note that said believe this ink.", f"Note BELIEVE THIS INK arrow, {PAINT}"),
    ("believe-market", "Believe is easier to teach in a market.", f"Market teaching BELIEVE checkmark, {PAINT}"),
    ("believe-print", "Believe is easier to print in a run.", f"Printing press BELIEVE in run, {PAINT}"),
    ("line-inventor", "The line is the real inventor.", f"Factory line labeled REAL INVENTOR, {PAINT}"),
    ("nostalgia-metal", "The line does not care about nostalgia for a purse full of metal.", f"Metal purse nostalgia red X, {PAINT}"),
    ("rehook-fact", "You think the bill is a fact, the way a door is a fact.", f"Bill vs door both labeled FACT, {PAINT}"),
    ("bill-policy", "The bill is a policy.", f"POLICY stamp on bill, {PAINT}"),
    ("bullion-grocery", "The alternative is carrying bullion to a grocery line.", f"Bullion in grocery line red X note wins, {PAINT}"),
    ("metal-honest", "Metal is honest. Notes are scalable.", f"METAL honest NOTES scalable scales, {PAINT}"),
    ("un-naturing", "I am un-naturing the portrait.", f"Portrait NATURAL stamp peeling off, {PAINT}"),
    ("receipt-denomination", "The portrait is a receipt wearing a denomination.", f"Receipt wearing DENOMINATION costume, {PAINT}"),
    ("trust-law", "The denomination said trust can be law.", f"Denomination TRUST IS LAW stamp, {PAINT}"),
    ("cards-down", "If you paid somewhere that wanted exact change because cards were down.", f"Exact change needed cards down scene, {PAINT}"),
    ("not-physics", "You know the note is not physics.", f"PHYSICS stamp red X on note, {PAINT}"),
    ("production-vote", "A compromise that won a production vote.", f"Production line voting for note wins, {PAINT}"),
    ("spreadsheet-cotton", "A vote is a spreadsheet with cotton and a serial catalog.", f"Spreadsheet cotton serial catalog, {PAINT}"),
    ("ink-travel", "Watch the ink travel.", f"Ink traveling across printing frame, {PAINT}"),
    ("inventoried-answer", "Mass production inventoried the answer.", f"Factory inventory note stacks shelf, {PAINT}"),
    ("print-serial-ship", "Print, serial, ship, replace without a weighing ritual.", f"PRINT SERIAL SHIP REPLACE conveyor, {PAINT}"),
    ("central-bank-chapter", "Central banks, reserve ratios, anti-counterfeit threads: a later chapter.", f"Central bank threads LATER CHAPTER, {PAINT}"),
    ("object-cotton", "Make it about the object: cotton, ink, signature, repeat.", f"COTTON INK SIGNATURE REPEAT icons, {PAINT}"),
    ("no-cabal", "Do not make tonight a lecture about shadowy cabals.", f"SHADOWY CABAL stamp red X, {PAINT}"),
    ("catalog-referendum", "A catalog is a quiet referendum.", f"Quiet catalog REFERENDUM whisper, {PAINT}"),
    ("wallet-vs-scale", "Your wallet has a bill and your history book has a scale.", f"Wallet bill vs history scale gap, {PAINT}"),
    ("inventory-fight", "Inventory is how the past loses a fight without filing a complaint.", f"Past losing fight INVENTORY filing cabinet, {PAINT}"),
    ("this-is-you", "This is you, already, in the middle of the story.", f"Stickman labeled THIS IS YOU at counter, {PAINT}"),
    ("tuesday-handoff", "A Tuesday, a counter, a handoff without thanking a Song merchant.", f"Tuesday counter handoff no thank you, {PAINT}"),
    ("reach-paper", "You reach for paper because leaving would feel awkward without a rectangle.", f"Hand reaching bill AWKWARD without paper, {PAINT}"),
    ("modern-impossibility", "The most modern impossibility there is.", f"MODERN IMPOSSIBILITY stamp on checkout, {PAINT}"),
    ("after-jiaozi", "Born after jiaozi and after goldsmith receipts.", f"Timeline after jiaozi goldsmith receipt, {PAINT}"),
    ("denominations-multiply", "After a central bank learned to host denominations that multiply.", f"Central bank denominations multiplying, {PAINT}"),
    ("relief-insult", "Relief you do not weigh metal, insult a warehouse note won.", f"Relief checkmark insult warehouse note wins, {PAINT}"),
    ("coin-purse-imagination", "The coin purse failing in your imagination.", f"Ghost coin purse failing imagination, {PAINT}"),
    ("never-voted", "You paid for speed with a promise you never voted on.", f"Speed receipt NEVER VOTED stamp, {PAINT}"),
    ("cheerful-bill", "Cheerful is how a bill stays without looking like a receipt.", f"Smiling bill receipt costume hidden, {PAINT}"),
    ("compromises-promise", "A market is a pile of compromises with a promise attached.", f"Market pile COMPROMISES promise bolted, {PAINT}"),
    ("take-bill-away", "Take the bill away and checkout becomes a workshop puzzle.", f"Checkout puzzle nobody wins no bill, {PAINT}"),
    ("signatures-serials", "Signatures, serial numbers, printing plates, replacement notes.", f"SIGNATURES SERIALS PLATES REPLACEMENT labels, {PAINT}"),
    ("diagram-trade", "The rectangle is a diagram of how to trade without moving the vault.", f"Bill diagram TRADE without moving vault, {PAINT}"),
    ("pay-vote", "The payment is a vote for a slip sold as obvious.", f"Payment voting SLIP OBVIOUS, {PAINT}"),
    ("personality-swap", "The personality was always the swap.", f"SWAP arrow heavy copper to paper, {PAINT}"),
    ("heavy-copper", "Heavy copper, a Sichuan jiaozi.", f"Heavy copper and Sichuan jiaozi icons, {PAINT}"),
    ("london-receipt", "A London goldsmith receipt.", f"London goldsmith receipt icon, {PAINT}"),
    ("bank-charter-line", "A Bank of England charter, a central bank plate.", f"Charter and printing plate icons, {PAINT}"),
    ("thread-forgot-scale", "A thread that forgot your scale.", f"Security thread forgetting scale ghost, {PAINT}"),
    ("treaty-crowd", "You and a city treating paper as a treaty.", f"City crowd paper TREATY handshake, {PAINT}"),
    ("what-we-traded", "We traded weight that told the truth about value.", f"Weight truth VALUE traded away, {PAINT}"),
    ("printed-numbered", "For a note that could be printed, numbered, and forgotten.", f"Printed numbered forgotten note on line, {PAINT}"),
    ("real-help", "Real help: fewer mules, a line moving, a pocket purchase.", f"Fewer mules line moving POCKET purchase, {PAINT}"),
    ("miracle-part-number", "Help can be a miracle and still be a part number.", f"MIRACLE and PART NUMBER both true, {PAINT}"),
    ("myth-nature", "A myth that the bill is nature and the rectangle is the only adult pay.", f"MYTH NATURE ADULT PAY stamps, {PAINT}"),
    ("receipt-money", "We kept the receipt and called it money.", f"Receipt wearing MONEY name tag, {PAINT}"),
    ("coin-history", "We kept the coin and called it history.", f"Coin labeled HISTORY museum, {PAINT}"),
    ("policy-manners", "The bill is a policy that learned manners.", f"Policy bill in polite bow tie, {PAINT}"),
    ("coin-era", "There was an era when the coin was the whole sermon.", f"Coin preaching WHOLE SERMON label, {PAINT}"),
    ("deposit-backing", "Early notes promised a deposit somewhere specific.", f"Note arrow DEPOSIT SOMEWHERE SPECIFIC, {PAINT}"),
    ("counterfeit-fear", "Counterfeit fear is the shadow of a promise that travels.", f"Counterfeit shadow following traveling note, {PAINT}"),
    ("note-separate", "Paper notes arrived as a separate homework assignment.", f"Paper note SEPARATE HOMEWORK label, {PAINT}"),
    ("fold-sound", "The crinkle sound is a contract your ears learned to trust.", f"Bill crinkle sound CONTRACT ears trust, {PAINT}"),
    ("weighing-queue", "A scale on every counter until the queue breaks.", f"Scale on every counter QUEUE BREAKS, {PAINT}"),
    ("bearer-promise", "Pay the bearer is a sentence that outsources trust.", f"PAY BEARER outsources TRUST label, {PAINT}"),
    ("ink-dry", "Ink dries, plates wear, the agreement stays.", f"Drying ink worn plate AGREEMENT stays, {PAINT}"),
    ("vault-shut", "The vault stayed shut so the street could move.", f"Shut vault street moving arrow, {PAINT}"),
    ("cotton-fray", "Cotton frays, plates swap, the promise stays.", f"Frayed cotton new plate same PROMISE, {PAINT}"),
    ("regulators-shelf", "Regulators did not invent the promise. They shelved it.", f"Regulator placing note on SHELF not invent, {PAINT}"),
    ("city-treaty", "A city checkout is a treaty written in identical portraits.", f"Identical bill portraits TREATY label, {PAINT}"),
    ("hand-memory", "Your hand remembers a rectangle you never chose.", f"Hand with rectangle MEMORY ghost, {PAINT}"),
    ("coin-ghost", "The coin purse is still a ghost in every wallet.", f"Coin purse ghost in modern wallet, {PAINT}"),
    ("cotton-cheerful", "Cotton is cheerful. Cheerful is how policy wears fabric.", f"Cheerful cotton fabric POLICY costume, {PAINT}"),
    ("pay-before-leave", "You pay before you leave as if leave required permission.", f"Pay then LEAVE PERMISSION stamp, {PAINT}"),
    ("layout-cotton", "A pile of people who agreed not to argue with cotton.", f"People nodding at cotton no argue, {PAINT}"),
    ("hands-counter", "You walk to the register. The rectangle will still be there.", f"Callback walking register bill in hand, {PAINT}"),
    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at payment, {PAINT}"),
    ("look-portrait", "Look at the portrait. Not the sky and not a single hero.", f"Portrait between red X sky and red X hero, {PAINT}"),
    ("named-stack", "Heavy copper, Song jiaozi, London receipt, Bank of England, printing plate.", f"Stack icons copper jiaozi receipt bank plate, {PAINT}"),
    ("promise-law", "A promise that owns your checkout so cotton stays law.", f"Checkout promise stamped LAW, {PAINT}"),
    ("allowed-pay", "You are allowed to pay. Allowed to hate inflation and still buy lunch.", f"Pay ok hate inflation still lunch, {PAINT}"),
    ("not-natural", "Stop calling the bill natural.", f"NATURAL stamp red X on bill, {PAINT}"),
    ("not-inevitable", "Not inevitable. Not proof you are modern.", f"INEVITABLE MODERN stamps red X, {PAINT}"),
    ("leftover-vault", "A leftover salute to a vault that stayed shut.", f"Salute to vault staying shut, {PAINT}"),
    ("cotton-point", "The salute is cheerful. The cotton is the point.", f"Cheerful salute on cotton bill, {PAINT}"),
    ("know-receipt", "Go when the promise lets you. Know which receipt you are still obeying.", f"Stickman paying bill labeled which receipt, {PAINT}"),
    ("glance-cheerful", "Cheerful is how a bill stays without looking like a receipt.", f"Smiling bill receipt ghost hidden, {PAINT}"),
    ("final-callback", "A scale. Sichuan. Your rectangle.", f"Final callback scale Sichuan YOUR RECTANGLE, {PAINT}"),
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
        title="Why a Bill Is a Promise",
        description=(
            "Your paper bill feels like money. Early markets used weighed metal. "
            "Song Dynasty jiaozi and London goldsmith receipts became circulating promises. "
            "The rectangle is logistics."
        ),
        tags=(
            "paper money",
            "jiaozi",
            "history",
            "bank of england",
            "goldsmith",
            "why",
            "economics",
            "promise",
            "currency",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="PAPER PROMISE?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why a Bill Is a Promise",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        use_zenn=False,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-bill.json"
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

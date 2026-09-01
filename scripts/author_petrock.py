"""Author Drawn Anyway episode 20: Pet Rock, nineteen seventy five."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 630.0
MINUTES = 9
VOICE = "en-US-GuyNeural"
RATE = "+2%"

CHAPTERS = [
    """A cardboard crate once sold a rock as if it needed to breathe. That is not a metaphor, and it is not a cartoon you invented after a trivia night about the seventies being stupid. In nineteen seventy five, a freelance copywriter in Los Gatos, California, put a smooth pebble from Rosarito, Baja California, into a miniature pet carrier with a handle, wood-shaving bedding, and fourteen air holes, plus a booklet titled The Care and Training of Your Pet Rock. The store price landed at three dollars and ninety five cents. Keep that picture. Then put a red X on the joke that Americans were so bored they bought gravel. The leftover is not that a pebble has a personality. The leftover is that the die-cut box, the straw, and the thirty six pages were the product, and the rock was the free sample that tagged along. A hole in cardboard is a costume for lungs. A handle is a costume for a leash. A training manual is a costume for a sale. File those three before you file the stone.""",
    """Start with why a joke in a bar was supposed to stay a joke. Gary Ross Dahl was a broke advertising copywriter in Los Gatos. In April nineteen seventy five, at a local bar, his friends complained about real pets: soiled carpets, chewed shoes, the whole unpaid job of keeping an animal alive. Dahl said he had a pet rock. They laughed. The official plan, if anyone had written one on a cocktail napkin, was going to work as a gag and then die at last call. Instead Dahl barely slept. He wrote the manual first. He founded Rock Bottom Productions and recruited two colleagues as investors: George Coakley and John Heagerty, of Coakley Heagerty Companies Limited. He went to a builder's supply store in San Jose and, in the usual retelling, picked the most expensive rock in the place, a Rosarita Beach stone, a rounded gray pebble that sold for a penny. Mexican beach stones by the countless trillions sit on beaches for free. A penny is already a costume. A company name is a costume. A bar joke that writes a thirty two to thirty six page manual before it has a warehouse is not a bar joke anymore. It is inventory looking for a crate.""",
    """File the crate, because the crate is the whole trick. Designer Pat Welch developed a cardboard box that imitated a pet carrier: handle, fourteen air holes, wood-shaving bedding, graphics that said this was an animal that needed air. Dahl later said the biggest expense was the die-cutting and manufacture of those boxes. The rocks cost a penny. The shavings were nearly free. Early manuals were piggybacked onto other printing jobs he was already running for clients, then cut and trimmed. That is logistics wearing a joke. Newsweek later called the whole scheme one of the most ridiculously successful marketing schemes ever. File the adjective. Do not spend it as a sneer at the buyers. Melanie DiLeo, a Midwest department-store buyer for Associated Merchandising Corporation, was at the San Francisco summer trade show that introduced it. Her prototype was one of a few made available to major buyers before production. She said she had a gut feeling. The Pet Rock made you laugh. You could spend about five dollars and still laugh. The economy, she said, was not in great shape. This was a novelty meant to sell in the fall and up to Christmas. That is a season, not a personality test.""",
    """Here is the leftover Dahl spent decades repeating and the internet still files as gravel. In a two thousand six interview with the Jacksonville Review, he said he was not selling rocks. Who in their right mind, he asked, would pay good money for a plain beach pebble available by the countless trillions absolutely free. The product never was about selling rocks. He was selling books. The Care and Training of Your Pet Rock, a three-inch by four-inch, thirty six page spoof of a dog training manual, was the product, not the rock which happened to tag along with it. That important bit, he said, had been overlooked, misunderstood, or ignored. The manual treats the pebble as a dog. Play dead is the easy trick: take it to the training area, give the command, and if it is like most rocks it will not have to be told more than once. It goes stiff. Rocks enjoy the trick so much they practice when you are not looking. There is a fake disease called Rock Bottom. There is no known cure. Get a new Pet Rock. Copyright nineteen seventy five, Rock Bottom Productions. A booklet that tells you not to turn a rock loose because the world is already overcrowded with discarded rocks is not geology. It is packaging with a punchline stapled in.""",
    """The debut was the San Francisco Gift Fair in August, at a starting price of two dollars. Retailers swarmed. Neiman Marcus and Bloomingdale's put the novelty on shelves. Dahl set retail at three dollars and ninety five cents and began shipping the early supplies on the first of October. In the month before Christmas he was delivering more than ten thousand rocks a day. Estimates for the season sit at about one point three to one point five million kits. The Strong museum files more than one million by Christmas. The Boston Globe later filed more than two tons of rock. Wikipedia's round count is nearly one point five million at just under four dollars, about ninety five cents profit on each unit. File the range. Do not invent a nicer round number. People magazine, nineteen seventy five, quoted him: people are so damn bored, tired of all their problems, this takes them on a fantasy trip, you might say we have packaged a sense of humor. He appeared on The Tonight Show twice. He later said, in a two thousand eleven interview, that he had one phone to each ear, and taught his P.R. guy to impersonate him so the calls could be answered twice. That is a warehouse problem wearing a talk-show jacket.""",
    """Rehook, because the internet likes a stupid seventies and a moral about consumer sheep. Put a red X on that sermon. A ventilated crate is not a personality. A penny pebble is not a census of American intelligence. The official idea was a perfect pet that would not need to be fed, walked, bathed, groomed, or forgiven, and would not die, become sick, or be disobedient. The street idea was a gag gift you could put on a desk before Christmas. Both can be true without turning the checkout line into a roast. Three quarters of the nation's newspapers ran something, in the Strong museum's retelling, and Newsweek ran a story. Copycats arrived because you cannot patent a rock. The brand could be copyrighted. The geology could not. By February nineteen seventy six the kits were discounted. The fad lasted about six months. A Bicentennial Pet Rock the following year found the joke already spent. A Sand Breeding Kit did not become a second million. T-shirts and shampoo did not either. A joke that ships ten thousand units a day is still a joke. A joke that needs a die-cutter is a factory.""",
    """File the hangover with names, not with a cartoon of greed as a personality. In the late nineteen seventies Coakley and Heagerty sued. They had put up money to get production going. A court found in their favor. Dahl wrote a six-figure check. John Heagerty said they would have liked to have continued a relationship with Gary, but money has a divisive element to it. Gary got rich quick and then he wanted more than he deserved. File the quote as a quote. Do not pick a hero. Dahl used proceeds to design and build a pub in Los Gatos named Carrie Nation's, after the temperance campaigner who smashed saloons with a hatchet, bricks, and rocks. He bought a house later filed at about five thousand two hundred square feet in that same town. He stayed in advertising, published Advertising for Dummies in two thousand one, and died on the twenty third of March two thousand fifteen in Jacksonville, Oregon, of chronic obstructive pulmonary disease, at seventy eight. His wife Marguerite confirmed it. Super Impulse later bought rights in twenty twenty two. A film studio licensed a googly-eyed rock as a tie-in. None of that is the nineteen seventy five receipt. The nineteen seventy five receipt is a crate with air holes, a penny stone, and a booklet that got to the printer first.""",
    """None of this is a hymn to a gullible checkout, and none of it is a cartoon of shoppers as fools who should have known better than to pay four dollars for a stone. They had a recession hangover. They had Watergate in the rear-view. They had a copywriter who wrote the manual first and a designer who put lungs on cardboard. You are allowed to laugh at play dead, and at fourteen holes so a pebble can breathe, and at a disease called Rock Bottom with no known cure. You are not required to laugh at DiLeo buying for Midwest stores because a five-dollar laugh was scarce, or at a freelance copywriter who piggybacked booklets onto client print jobs because he did not have a toy factory. A penny is a costume for a beach. A handle is a costume for a gift. Ninety five cents is a margin. One point five million is a press count on cardboard. The official idea was: this will read as the perfect pet. The street idea was: wrap the joke so tightly the rock is optional.""",
    """So who won. Not the pebble. Not geology. Not the Bicentennial encore. Welch won a crate people still photograph. Dahl won a millionaire season, two Tonight Show bookings, a bar named after a woman who threw rocks at bars, and a six-figure invoice from the men who floated the first run. Coakley and Heagerty won a court. Newsweek won a sentence about a ridiculous scheme. DiLeo won a prototype that later sat at The Strong, in a case titled What Were They Thinking. The die-cutter won the biggest line item. If you need a moral, skip never buy a novelty. Take this: a rock is a terrible product, and a box that pretends it needs air is a terribly honest one. The next time someone tells you nineteen seventy five bought gravel, ask whether they mean the pebble or the manual, and whether the air holes were a joke or the whole sale. Would you have paid three dollars and ninety five cents for a Rosarito stone, or only for the crate it came in. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no cruelty, not mud-green archive night, not After Hours File dark. "
    "Pet Rock shown as a candy cardboard pet-carrier crate, a cute gray pebble, a tiny manual, "
    "a gift-fair booth, not cruelty, not a roast of buyers. Recurring mascot Ink may cameo: mustard jacket, "
    "ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("air-holes", "A cardboard crate sold a rock as if it needed to breathe.", f"A candy cardboard pet-carrier crate with 14 round AIR HOLES, a cute gray pebble inside, cream paper. {STYLE}"),
    ("not-trivia", "Not a stupid-seventies trivia gag.", f"Ink shaking his head at a STUPID 70S stamp with a red X, mouth closed. {STYLE}"),
    ("dahl-1975", "1975, freelance copywriter, Los Gatos, California.", f"A nameplate GARY DAHL, tags 1975 and LOS GATOS, no portrait. {STYLE}"),
    ("rosarito-pebble", "A smooth pebble from Rosarito, Baja California.", f"A cute rounded gray pebble labeled ROSARITO, a tiny BAJA pin, no flag as joke. {STYLE}"),
    ("crate-kit", "Handle, wood shavings, fourteen air holes, plus a booklet.", f"An exploded kit: HANDLE, SHAVINGS, 14 HOLES, BOOKLET, pebble. {STYLE}"),
    ("three-ninety-five", "Store price: $3.95.", f"A price tag $3.95 on a tiny crate. {STYLE}"),
    ("x-on-gravel", "Put a red X on they-bought-gravel.", f"A THEY BOUGHT GRAVEL stamp with a giant red X. {STYLE}"),
    ("box-was-product", "Leftover: the box and the pages were the product. The rock tagged along.", f"Three cards BOX, 36 PAGES, ROCK = FREE SAMPLE. {STYLE}"),
    ("bar-april", "April 1975, a Los Gatos bar. Friends complained about pets.", f"A candy bar booth APRIL 1975, a tiny SOILED CARPET and CHEWED SHOE, not cruel. {STYLE}"),
    ("i-have-a-rock", "Dahl said he had a pet rock. They laughed.", f"A speech bubble I HAVE A PET ROCK over a pebble on a bar stool. {STYLE}"),
    ("rock-bottom-co", "He founded Rock Bottom Productions.", f"A company sign ROCK BOTTOM PRODUCTIONS. {STYLE}"),
    ("investors", "Investors: George Coakley and John Heagerty.", f"Two nameplates COAKLEY and HEAGERTY, tag INVESTORS, no portraits. {STYLE}"),
    ("san-jose-penny", "Builder's supply, San Jose: a Rosarita Beach stone for a penny.", f"A supply-bin pebble, tags SAN JOSE and 1 CENT. {STYLE}"),
    ("free-on-beach", "Beach stones by the trillions sit free. A penny is already a costume.", f"A beach of cute pebbles FREE, one pebble wearing a 1 CENT costume tag. {STYLE}"),
    ("pat-welch", "Designer Pat Welch: a cardboard pet carrier.", f"A nameplate PAT WELCH beside a tiny crate blueprint. No portrait. {STYLE}"),
    ("fourteen-holes", "Handle, fourteen air holes, wood-shaving bedding, graphics.", f"A crate diagram HANDLE, 14 HOLES, SHAVINGS. {STYLE}"),
    ("die-cut-cost", "Biggest expense: die-cutting the boxes. Rocks a penny. Shavings nearly free.", f"A ledger BOX DIE-CUT $$, ROCK 1c, SHAVINGS ~0. {STYLE}"),
    ("print-piggyback", "Early manuals piggybacked on other client print jobs, then trimmed.", f"A print stack CLIENT JOBS with a tiny MANUAL riding along. {STYLE}"),
    ("newsweek-scheme", "Newsweek: one of the most ridiculously successful marketing schemes ever.", f"A magazine clip NEWSWEEK, RIDICULOUSLY SUCCESSFUL, file stamp. {STYLE}"),
    ("dileo-gut", "Melanie DiLeo, AMC buyer, gut feeling at the San Francisco show.", f"A buyer badge MELANIE DILEO AMC, GUT FEELING, no portrait. {STYLE}"),
    ("five-dollar-laugh", "You could spend about $5 and still laugh. Economy not great. Fall to Christmas.", f"A $5 laugh tag, a calendar FALL to CHRISTMAS. {STYLE}"),
    ("selling-books", "2006: I was not selling rocks. I was selling books.", f"A scale BOOK vs ROCK, the book side down, 2006 tag. {STYLE}"),
    ("three-by-four", "A 3 by 4 inch, 36-page spoof of a dog training manual.", f"A tiny booklet 3x4 IN, 36 PAGES, DOG MANUAL SPOOF. {STYLE}"),
    ("play-dead", "Play dead: if it is like most rocks it will not be told twice.", f"A pebble labeled PLAY DEAD, a tiny command bubble, cute not grim. {STYLE}"),
    ("rock-bottom-bug", "Fake disease: Rock Bottom. No known cure. Get a new Pet Rock.", f"A cartoon thermometer ROCK BOTTOM, stamp NO CURE, a replacement crate. {STYLE}"),
    ("copyright-rbp", "Copyright 1975, Rock Bottom Productions.", f"A copyright bug 1975 ROCK BOTTOM PRODUCTIONS. {STYLE}"),
    ("gift-fair", "San Francisco Gift Fair, August, starting price $2.", f"A gift-fair booth SF AUG 1975, tag $2. {STYLE}"),
    ("neiman-bloomies", "Neiman Marcus and Bloomingdale's put it on shelves.", f"Two fancy store awnings NEIMAN MARCUS and BLOOMINGDALE'S, tiny crates. No flags. {STYLE}"),
    ("oct-1-ship", "Retail $3.95. Early supplies shipped 1 October.", f"A shipping crate OCT 1, $3.95. {STYLE}"),
    ("ten-thousand", "Month before Christmas: more than 10,000 rocks a day.", f"A conveyor of tiny crates 10000 A DAY. {STYLE}"),
    ("one-point-five", "Season estimate: about 1.3 to 1.5 million kits.", f"A tally 1.3-1.5 MILLION KITS. {STYLE}"),
    ("two-tons", "Boston Globe later: more than 2 tons of rock.", f"A scale 2 TONS, a cute pebble pile. {STYLE}"),
    ("ninety-five-margin", "About 95 cents profit on each unit.", f"A margin badge 95 CENTS. {STYLE}"),
    ("people-quote", "People 1975: we have packaged a sense of humor.", f"A People-style clip PACKAGED A SENSE OF HUMOR, 1975. {STYLE}"),
    ("tonight-twice", "The Tonight Show twice. One phone to each ear.", f"Two talk-show chairs TONIGHT x2, two candy phones. No photoreal host. {STYLE}"),
    ("pr-impersonate", "He taught his P.R. guy to impersonate him so calls could be answered twice.", f"Two identical nameplates DAHL, one tagged P.R. STAND-IN. {STYLE}"),
    ("rehook-sheep", "Rehook: put a red X on the consumer-sheep sermon.", f"Ink peeling a SHEEP stamp off a checkout, mouth closed. {STYLE}"),
    ("perfect-pet", "Official idea: a pet that would not need feeding, walking, or forgiving.", f"A checklist NO FOOD NO WALK NO DIE, a smiling pebble. {STYLE}"),
    ("gag-desk", "Street idea: a gag gift on a desk before Christmas.", f"An office desk with a tiny crate under a bow. {STYLE}"),
    ("cannot-patent", "You cannot patent a rock. Copycats arrived.", f"A PATENT stamp with a red X on a pebble, COPYCAT crates behind. {STYLE}"),
    ("feb-discount", "By February 1976 the kits were discounted. Fad about six months.", f"A calendar FEB 1976, SALE sticker, 6 MONTHS tag. {STYLE}"),
    ("bicentennial-flop", "A Bicentennial Pet Rock the next year found the joke already spent.", f"A 1976 crate with a tiny fizzle, JOKE SPENT. No flag as the joke. {STYLE}"),
    ("sand-kit", "A Sand Breeding Kit did not become a second million.", f"A novelty box SAND BREEDING KIT with a small DID NOT tag. {STYLE}"),
    ("lawsuit", "Late 1970s: Coakley and Heagerty sued. Court for the investors.", f"A court folder COAKLEY HEAGERTY v DAHL. {STYLE}"),
    ("six-figure", "Dahl wrote a six-figure check.", f"A giant check SIX FIGURES. {STYLE}"),
    ("heagerty-money", "Heagerty: money has a divisive element to it.", f"A quote card MONEY HAS A DIVISIVE ELEMENT. {STYLE}"),
    ("carrie-nations", "A Los Gatos pub named Carrie Nation's, after a woman who smashed saloons with rocks.", f"A pub sign CARRIE NATION'S, a cartoon hatchet and a pebble, not gore. {STYLE}"),
    ("house-sqft", "A house later filed at about 5,200 square feet.", f"A candy house 5200 SQ FT. {STYLE}"),
    ("dummies-2015", "Advertising for Dummies 2001. Died 23 March 2015, Jacksonville, Oregon, age 78.", f"A book 2001, a calendar 23 MAR 2015, age 78, no gravestone gore. {STYLE}"),
    ("not-fools", "Not a cartoon of shoppers as fools for a four-dollar stone.", f"Ink peeling a FOOLS sticker off a BUYERS sign, mouth closed. {STYLE}"),
    ("die-cutter-won", "The die-cutter won the biggest line item. The crate is the receipt.", f"A die-cutter trophy BIGGEST LINE ITEM, a crate as a receipt. {STYLE}"),
    ("pebble-or-manual", "Ask whether they mean the pebble or the manual, and whether the air holes were the sale.", f"Split: a pebble vs a booklet vs a crate of AIR HOLES, a question mark. {STYLE}"),
    ("three-ninety-or-crate", "Would you have paid $3.95 for a Rosarito stone, or only for the crate.", f"Split price tag $3.95: PEBBLE vs CRATE, a question mark. {STYLE}"),
    ("receipt", "A box sold a rock. Drawn anyway.", f"A receipt card BOX vs ROCK, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Rock People Paid to Own",
        description=(
            "Pet Rock, nineteen seventy five. A Los Gatos copywriter, a crate with air holes, "
            "and a manual that was the product."
        ),
        tags=(
            "history",
            "pet rock",
            "1975",
            "gary dahl",
            "cartoon",
            "true story",
            "packaging",
            "funny",
            "logistics",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="THEY SOLD THE BOX",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Rock People Paid to Own",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-petrock.json"
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

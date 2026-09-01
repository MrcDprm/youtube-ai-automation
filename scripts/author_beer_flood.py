"""Author Drawn Anyway episode 2: London Beer Flood, Meux, eighteen fourteen."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 630.0
MINUTES = 9
VOICE = "en-GB-ThomasNeural"
RATE = "+2%"

CHAPTERS = [
    """London once flooded a neighborhood with beer. That is not a pub joke and it is not a cartoon you saw on a phone. On the seventeenth of October eighteen fourteen, at Meux and Company's Horse Shoe Brewery, where Tottenham Court Road met Oxford Street, a storehouse clerk named George Crick watched a seven hundred pound iron hoop slip off a twenty two foot wooden vat. The vat held three thousand five hundred fifty five barrels of porter, ten months old, filled to within four inches of the top. Hoops slipped two or three times a year. Crick was not alarmed. His supervisor said no harm whatever would ensue. Crick was told to write a note to Mister Young, a partner, so someone could fix it later. He was still holding that note, standing on a platform thirty feet from the vat, when the vessel burst as completely as if a quart pot had been turned up on a table. Keep that picture. A hoop. A shrug. A note. A wall two and a half bricks thick. Everything after this is just that picture getting wetter, louder, and more expensive than anyone in the storehouse had budgeted for.""",
    """Start with why anyone built a wooden tank the size of a small house and then trusted it with iron belts. In eighteen nine, Sir Henry Meux bought the Horse Shoe Brewery at that busy junction. His father, Sir Richard Meux, had already shown off at the Griffin Brewery on Liquor Pond Street, later Clerkenwell Road, with a vat that could hold twenty thousand barrels. Henry copied the brag. He raised a vessel twenty two feet tall, rated for about eighteen thousand barrels, bound with some eighty tons of iron hoops. Meux brewed only porter, the dark working beer of London, left for months to mature, sometimes a year for the best. In the twelve months to July eighteen twelve the firm turned out over one hundred two thousand barrels. At the rear of the Horse Shoe ran New Street, a cul-de-sac onto Dyott Street, inside the St Giles rookery: eight acres of cheap rooms stacked against the brewery's back wall. The official idea was scale. The unofficial idea was that a hoop which had always been put back would always be put back. The rookery did not get a vote on either idea.""",
    """Porter was not a novelty drink. It was the capital's daily dark pint, mixed to taste from older stock and fresh, which is why a ten month vat of entire sat in the storehouse waiting to be blended. Huge wood was how you stored that kind of money without a thousand little barrels eating the floor. The Horse Shoe sat on low, poorly drained ground. Beer that escaped would not politely run to the Thames. It would sit. It would fill cellars that people lived in. Richard Kirkland later called St Giles a slum always on the verge of collapse. Thomas Beames, writing decades after, called it a rendezvous the respectable liked to insult. You do not need the insult. You need the map: a giant tank, a two-and-a-half-brick wall, and a street of rooms that had nowhere to put a fifteen foot wave. If this already sounds like a bad idea written in iron, you are paying attention. The porter was real. The hoops were real. The plan assumed the vat would keep being a vat. Plans that assume a wooden cylinder will remain a cylinder should be stored with the other fiction.""",
    """About half past four in the afternoon, Crick saw the band go. Seven hundred pounds of iron, the smallest of twenty two hoops, about three feet from the bottom. He told his boss. He wrote the note. An hour later he was still on that platform, note in hand, when the vat let go with no warning. The rush knocked the stopcock off a neighbouring vessel. That one dumped too. Several hogsheads smashed and joined the flood. How much porter? One paper said one hundred twenty eight thousand imperial gallons. Another said three hundred twenty three thousand. That gap is the joke and the paperwork. The force took out the rear wall, twenty five feet high. Some bricks went up and landed on roofs in Great Russell Street. A wave of porter about fifteen feet high went into New Street, wrecked two houses, and badly damaged two others. The land was flat. Drainage was a rumour. Beer ran into inhabited cellars. Inside the brewery, everyone lived. Three workmen were pulled from rubble. The superintendent and others went to Middlesex Hospital. The people who did not brew the porter took the deaths. Eight. Named later on an inquest list. Not a montage. A number that would not fit on a hoop.""",
    """Here is the part the internet likes to get drunk on, and here is the part the newspapers actually printed. Later stories claimed hundreds scooped beer from the gutter, a city-wide party, even a death from drinking the flood. Martyn Cornell, who reads the beer files for a living, checked the papers of eighteen fourteen. They did not report a carnival. They reported a crowd that behaved. The popular press of that week was not shy about insulting the Irish poor of St Giles. If a riot of drinkers had been there to smear, it would have been on the page. What the papers did describe was desolation equal to fire or earthquake, and then a smaller, uglier industry: watchmen at the brewery charging spectators to view the wreck of the vats. Several hundred paid. Mourners who had died in a cellar were given another wake at The Ship on Bainbridge Street. Other families laid out their dead in a yard. The public came, stared, and put money in a hat for funerals. That is not a party. That is a city turning a burst tank into a ticket and a collection plate. Keep both. The myth is louder. The receipts are meaner.""",
    """Two days later, on the nineteenth of October, the coroner for Middlesex, George Hodgson, sat at the St Giles workhouse. He read eight names. He walked the jurors to the brewery and the bodies, then took evidence. George Crick went first. He had seen the hoop, the note, the burst. His own brother was among the injured at Middlesex Hospital. Crick said hoops failed three or four times a year without previous disaster. Richard Hawse, landlord of the Tavistock Arms in Great Russell Street, spoke: a servant washing pots in the pub yard had been killed when the brewery wall came down. Other witnesses filled the hour. The jury did not linger. They returned, without hesitation, that the eight had lost their lives casually, accidentally, and by misfortune. In the language of the room that meant an act of God. An act of God is a legal shrug wearing a hymn. It meant Meux and Company did not have to pay compensation to the families. The hoop had been a known habit. The note had been the procedure. Procedure plus God is how a brewery walks out of a workhouse still a brewery.""",
    """Money is where the vat becomes a spreadsheet. The lost porter, the smashed buildings, the replacement vessel: about twenty three thousand pounds, a sum that could have sunk the firm. Meux petitioned Parliament in private and recovered about seven thousand two hundred fifty pounds from His Majesty's Excise, tax already paid on beer that no longer existed. The rebate is the punchline wearing a wig. The street got misfortune. The company got a refund on the inventory. The Horse Shoe went back to work. Across the industry, the giant wooden maturation tank started to look like a bad bet; lined vessels took the job later. In nineteen twenty one Meux left the site for Nine Elms in Wandsworth, a brewery they had bought in nineteen fourteen. The Horse Shoe came down. The Dominion Theatre was built where the vats had stood. Meux and Company went into liquidation in nineteen sixty one. If you want a moral about alcohol, skip it. Take this: a storage decision can outlive the people it floods, and a tax office can be kinder than a coroner.""",
    """So who learned. Not the hoop. Hoops had been slipping for years, which is why Crick wrote a note instead of shouting. Not the wall. Two and a half bricks are a number, not a promise. The rookery learned first and paid in a list of eight. The trade learned slowly, the way trades do, by replacing wood with something that fails differently. London learned a story it still tells as a novelty: the day beer became a wave. Cornell's warning still applies. Do not add a drunken chorus the papers did not print. Do not turn the inquest into a joke about God being a shareholder. Do laugh, if you laugh, at the note. A clerk did the correct small thing while standing thirty feet from a cylinder that was about to become a street. That is logistics. Logistics is funnier than a myth and crueller than a cartoon, which is why the cartoon has to stay on the hoop, the wall, the ticket to see the wreck, and the excise stamp that said: the beer still counts, even when it is in New Street.""",
    """The leftover fact is a theatre. You can walk past the Dominion and never know a twenty two foot vat used to ferment behind that block, or that New Street is gone from the map the way cul-de-sacs get eaten. The Horse Shoe is a name on old prints. George Crick is a witness in a workhouse transcript. Mister Young is the man who was supposed to get a note. Eight people are a verdict that rhymes with misfortune. If you need a question, here it is, and it is not about whether beer is funny. Would you have written the note and gone back to the platform. A hoop that always slipped. A supervisor who promised no harm. A partner's name on a scrap of paper. A wall that was two and a half bricks thick facing a street that had nowhere for a wave to go. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags, "
    "no photoreal faces, no drowning people, no corpses. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("beer-flood", "London once flooded a neighborhood with beer.", f"Cartoon title beat: a huge wooden vat tipping dark porter into tiny London streets, cream paper. {STYLE}"),
    ("not-a-joke", "Not a pub joke. Not a phone cartoon.", f"Ink the mascot shaking his head at a pint glass wearing a joke sticker, mouth closed. {STYLE}"),
    ("october-date", "Seventeenth of October, eighteen fourteen.", f"Cartoon calendar October seventeen 1814, brewery chimney behind. {STYLE}"),
    ("horse-shoe", "Meux Horse Shoe Brewery, Tottenham Court Road.", f"Simple cartoon brewery labeled HORSE SHOE at a busy street junction, no flags. {STYLE}"),
    ("crick-clerk", "Clerk George Crick watched a hoop slip.", f"Cartoon clerk on a high platform staring at a giant vat, tiny note in hand. {STYLE}"),
    ("seven-hundred", "A seven hundred pound iron hoop.", f"A huge cartoon iron ring falling off a wooden vat, motion lines, no people crushed. {STYLE}"),
    ("twenty-two-feet", "A twenty two foot wooden vat.", f"Tiny clerk beside a towering wooden cylinder bound in iron, cream paper. {STYLE}"),
    ("three-five-five-five", "Three thousand five hundred fifty five barrels inside.", f"Giant cartoon number 3555 on a barrel stamp, porter brown. {STYLE}"),
    ("four-inches", "Filled to within four inches of the top.", f"Cutaway vat almost full of dark porter, tiny air gap at the rim. {STYLE}"),
    ("not-alarmed", "Hoops slipped every year. Crick was not alarmed.", f"Ink shrugging next to a hoop on the floor labeled USUAL, mouth closed. {STYLE}"),
    ("no-harm", "His supervisor said no harm whatever would ensue.", f"Cartoon stamp NO HARM on a clipboard, vat looming behind. {STYLE}"),
    ("note-young", "Write a note to Mister Young. Fix it later.", f"Cartoon letter addressed to Mr Young, quill, vat in the background. {STYLE}"),
    ("quart-pot", "The vat burst like a quart pot turned on a table.", f"Wooden vat emptying like a mug knocked over, dark porter arc, no people. {STYLE}"),
    ("henry-buys", "Eighteen nine: Henry Meux bought the Horse Shoe.", f"Cartoon deed and oversized key labeled HORSE SHOE, no portrait. {STYLE}"),
    ("griffin-brag", "Father Richard's Griffin vat held twenty thousand barrels.", f"Even bigger cartoon vat labeled GRIFFIN, tiny people pointing, no flags. {STYLE}"),
    ("eighty-tons", "Eighty tons of iron hoops on Henry's vat.", f"Stack of cartoon iron rings, a scale groaning, cream paper. {STYLE}"),
    ("only-porter", "Meux brewed only porter, London's dark working beer.", f"Row of simple dark mugs, PORTER banner, no drunk faces. {STYLE}"),
    ("one-oh-two-k", "Over one hundred two thousand barrels in a year.", f"Cartoon ledger totaling 102493, proud rubber stamp. {STYLE}"),
    ("new-street", "New Street, a cul-de-sac onto Dyott Street.", f"Simple map: brewery block, dead-end New Street, rookery roofs. {STYLE}"),
    ("st-giles", "The St Giles rookery sat against the back wall.", f"Crowded cartoon rooftops tight against a brewery wall, no misery porn. {STYLE}"),
    ("scale-idea", "The official idea was scale. The hoop would be put back.", f"Split image: giant vat trophy versus a hoop being hammered on. {STYLE}"),
    ("blend-stock", "Ten month entire waited to be blended to taste.", f"Two cartoon taps, OLD and FRESH, mixing into a mug. {STYLE}"),
    ("low-ground", "The Horse Shoe sat on low, poorly drained ground.", f"Cartoon brewery in a shallow dish, rain arrows with nowhere to go. {STYLE}"),
    ("cellars-lived", "Escaped beer would fill cellars people lived in.", f"Cutaway of stacked rooms and cellar icons, beer as brown arrows, no bodies. {STYLE}"),
    ("four-thirty", "Half past four: Crick saw the band go.", f"Cartoon clock at four thirty, hoop mid-fall, clerk pointing. {STYLE}"),
    ("smallest-hoop", "Smallest of twenty two hoops, three feet from the bottom.", f"Vat diagram with the lowest small hoop highlighted, simple arrows. {STYLE}"),
    ("hour-later", "An hour later he still held the note.", f"Hourglass and the same letter, vat looking the same, false calm. {STYLE}"),
    ("stopcock", "The rush knocked a neighbouring stopcock off.", f"Second vat's tap flying off, two streams of porter meeting. {STYLE}"),
    ("gallon-gap", "One hundred twenty eight thousand, or three hundred twenty three.", f"Two cartoon clipboards arguing with different gallon numbers. {STYLE}"),
    ("back-wall", "The rear wall, twenty five feet, two and a half bricks, went.", f"Cartoon brick wall bursting outward, bricks as simple rectangles, no people. {STYLE}"),
    ("russell-roofs", "Bricks landed on Great Russell Street roofs.", f"Cartoon bricks on rooftops, chimney pots, no injuries shown. {STYLE}"),
    ("fifteen-foot", "A fifteen foot wave of porter entered New Street.", f"Stylized dark-brown wave between tiny houses, not photoreal, no drowning. {STYLE}"),
    ("two-houses", "Two houses wrecked, two more badly damaged.", f"Four cartoon houses: two collapsed as simple shapes, two cracked. {STYLE}"),
    ("eight-on-paper", "Eight people died. The brewery counted survivors.", f"A form with the number 8, and a brewery door marked ALL ALIVE, no corpses. {STYLE}"),
    ("hospital-cart", "Injured brewery men went to Middlesex Hospital.", f"Cartoon hospital cart, bandaged workers sitting up, not grim. {STYLE}"),
    ("myth-party", "Later stories sold a city-wide beer party.", f"A carnival poster stamped MYTH with a big red X. {STYLE}"),
    ("cornell-papers", "Cornell checked the papers. No carnival.", f"Ink reading stacked 1814 newspapers, mouth closed, X on a party hat. {STYLE}"),
    ("well-behaved", "The papers said the crowd behaved.", f"Cartoon crowd behind a rope, headline WELL BEHAVED, no riot. {STYLE}"),
    ("watchmen-fee", "Watchmen charged to view the wrecked vats.", f"Ticket booth at the brewery ruins, TICKET TO SEE THE VAT. {STYLE}"),
    ("hundreds-paid", "Several hundred spectators paid.", f"Line of cartoon coins into a hat beside a broken vat. {STYLE}"),
    ("ship-wake", "Another wake was held at The Ship, Bainbridge Street.", f"Simple pub sign THE SHIP, respectful interior, no child closeup. {STYLE}"),
    ("funeral-hat", "The public put money in a hat for funerals.", f"Cartoon collection hat labeled FUNERALS, coins, cream paper. {STYLE}"),
    ("workhouse", "Nineteenth of October: inquest at St Giles workhouse.", f"Cartoon workhouse room, coroner desk, calendar October 19. {STYLE}"),
    ("hodgson", "Coroner George Hodgson walked the jurors to the site.", f"Cartoon jury in a line touring a broken vat, no bodies shown. {STYLE}"),
    ("crick-witness", "Crick testified. His brother was in hospital.", f"Crick at a witness chair, tiny hospital window in the corner. {STYLE}"),
    ("three-four-year", "Hoops failed three or four times a year, he said.", f"Cartoon year-wheel with four hoop icons popping off. {STYLE}"),
    ("hawse-pub", "Landlord Hawse: the Tavistock Arms wall came down.", f"Cartoon pub Tavistock Arms, one wall as dashed outline, yard tubs. {STYLE}"),
    ("misfortune", "Verdict: casually, accidentally, and by misfortune.", f"Giant rubber stamp MISFORTUNE on an inquest paper. {STYLE}"),
    ("act-of-god", "In that room, misfortune meant an act of God.", f"Legal scroll labeled ACT OF GOD beside a tiny hoop. {STYLE}"),
    ("no-payout", "Meux did not have to pay the families.", f"Empty envelope COMPENSATION with a red X. {STYLE}"),
    ("twenty-three-k", "The disaster cost about twenty three thousand pounds.", f"Cartoon invoice totaling 23000, vat, wall, beer icons. {STYLE}"),
    ("excise-back", "Parliament and Excise returned about seven thousand two hundred fifty.", f"Tax rebate stamp 7250 on a beer barrel that no longer exists. {STYLE}"),
    ("wood-retired", "Giant wooden vats started to look like a bad bet.", f"Wooden vat with a RETIRED tag, newer lined tank beside it. {STYLE}"),
    ("dominion", "The Dominion Theatre now stands where the vats stood. Would you have written the note. Tell me in the comments.", f"Ink the mascot pointing at a cartoon theatre on the old brewery footprint, mouth closed, cream paper. {STYLE}"),
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
        title="The Day a Town Flooded With Beer",
        description=(
            "Horse Shoe Brewery, eighteen fourteen. A hoop slipped, a clerk wrote a note, "
            "and porter took the back wall. The inquest called it misfortune. The tax office "
            "called it a rebate."
        ),
        tags=(
            "history",
            "london",
            "beer",
            "cartoon",
            "true story",
            "1814",
            "brewery",
            "porter",
            "meux",
            "funny",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="VAT BURST",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Day a Town Flooded With Beer",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_font_size=50,
        subtitle_position_ratio=0.82,
        subtitle_color="#F5D76E",
        subtitle_accent="#C45C26",
        subtitle_stroke="#3D1F0A",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-beer.json"
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
    print("voice", scenario.tts.voice, "rate", scenario.tts.rate, "cat", scenario.youtube.category_id)
    print("brand", scenario.youtube.brand_id, "hook", scenario.youtube.thumbnail_hook)
    print("subs", scenario.subtitles.color, scenario.subtitles.font_size)
    print("tsv", tsv)


if __name__ == "__main__":
    main()

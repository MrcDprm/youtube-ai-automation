"""Author episode 11: you pay before the letter leaves, because a stamp flipped the debt."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you will press a stamp onto an envelope, or you will tap a tracking number that appears like a receipt from a god who works in logistics. The corner will stick. A tiny portrait will mean the debt is already paid. You will not think of it as a political act. It will feel like postage doing its job. Here is the part that should bother you. For most of the history of letters, the person who received the mail paid. The sender could write for almost nothing. The recipient could refuse the knock, and the letter died on the doorstep like an unpaid bill. So why do you pay before the letter leaves the house? Because a British schoolmaster decided the old rates were a tax on distance and on the poor, and then a black square with a queen's face taught the world to prepay. That is the whole plot. Your stamp is not a decoration. It is a receipt that flipped who owes whom. You still lick the corner, or you don't, because the glue learned manners. The corner is flattered. That is its job. The doorstep did not vote. A reform pamphlet did, and then a post office that taught your hand the stick until the stick started calling itself sending.""",
    """Start with the older letter, because the stamp stole a knock and then sold it back as a sticker. Before prepaid postage, a letter was a bet. Distance cost money. A note from London to Scotland could cost a laborer's day. Clerks counted sheets and miles like a taxi that never turned the meter off. The person at the far end paid, which sounds fair until you notice the trap: anyone could send you a letter you did not want, and you still owed the post for the privilege of finding out. People refused. They peeked at the address through a window and shook their head. Lovers invented codes on the envelope so the beloved could read the outside and send the postman away unpaid, which is romance wearing a loophole. The government hated the loophole. The poor hated the bill. If your spam folder still feels like an insult, notice that spam used to knock, and the knock used to cost. Cost is how a door learned to be a filter. The stamp deleted the filter and called the deletion progress. Progress never had to stand on the mat with a coin in its hand.""",
    """Rowland Hill was a schoolmaster and a pamphleteer, not a prophet of your tracking app. In eighteen thirty seven he published Post Office Reform, a paper that said the real cost of a letter was not the miles. It was the clerks arguing about miles. Uniform cheap postage, paid in advance, would make the arguing stop. In eighteen forty Britain launched the Uniform Penny Post: one penny to send a half-ounce letter anywhere in the country. On the sixth of May, eighteen forty, the Penny Black went on sale, a rectangle of Queen Victoria in profile, the world's first adhesive postage stamp. It was not cute. It was a machine for saying this debt is settled at the counter, not at the door. Hill wanted volume. Volume is what happens when the poor can write to the poor without bankrupting the far end. If your stamp still feels like a tiny flag of the nation, notice that the nation first needed a tiny receipt. The receipt learned a face so you would not lose it in a drawer of plain paper.""",
    """Watch the old world fight the sticker, because a sticker that works is an insult to a profession. The Mulready envelope, a decorated prepaid wrapper sold beside the Penny Black, was mocked into a joke in weeks. People wanted the little black square, not an allegory of Britannia. Clerks who had lived on complicated rates had to learn a simpler till. Forgers noticed a queen is easier to copy than a clerk's mood. Perforations arrived later, in the eighteen fifties, so you could tear a stamp without scissors, which is a tiny kindness and also a tiny admission that the stamp had become a habit. The United States issued its first general stamps in eighteen forty seven, Franklin and Washington doing the same job in a different accent. I am not asking you to collect. I am pointing at the swap. We took a knock that could be refused, turned it into a prepaid square, then taught every country the square. The square is how a reform travels. Travel is a word that never has to stand on a doorstep waiting to be paid.""",
    """This is the rehook. You think a stamp is proof the letter is important, the way a wax seal was proof. Importance was never the point. Cash-up-front was the point. Email later deleted the square and kept the volume, which is how you know the volume was the product. A tracking number is a Penny Black that learned to ping. A postage-due stamp is a fossil of the old world, a little confession that someone still tried to send unpaid. I am not nostalgic for refusing the postman as a lifestyle. I am trying to un-nature the lick. The lick is not love of the queen. The lick is Hill's argument winning in your saliva. Even a QR code on a shipping label is the same argument wearing a barcode: the sender paid, the door does not get to negotiate. Negotiation is slow. Prepaid is how a lock stays on the envelope without looking like a lock.""",
    """Watch the lock travel. Colonies copied the penny idea because empires love a uniform till. Airmail printed little planes and charged extra for the sky. Registered mail sold anxiety as a signature. The post office became a place you trusted with money orders and gossip and the state's right to open what it feared. A stamp can be propaganda: a dead president, a bird, a war bond. It can also be a quiet census of who is allowed to write. If your package still feels like a private act, notice the public machine under it: rates, weight, a face that means paid. Junk mail is the old unwanted letter that learned to prepay itself, which is a cruel joke Hill did not write and we still receive. The joke is allowed. The prepaid spam is the plot. A plot can be rewritten. A catalog would prefer you not notice that rewrite is possible, because an unpaid knock at least had the dignity of being refuseable.""",
    """This is you, already, in the middle of the story. A birthday card with a stamp you bought in a strip of twenty. A return label that is really a prepaid apology. A wedding invitation whose RSVP is an email because stamps got expensive and attention got cheap. None of this makes you a Victorian. It makes you a person born after Hill's pamphlet and after Victoria's profile and after a post office that decided the doorstep was a bad place to collect a tax. You can feel both in the same envelope: relief that your friend will not be billed for your handwriting, and a small flatness, a square that used to be a negotiation. The relief is real. The flatness is the receipt. You paid for the knock in advance so the knock could become a slot in a door. The slot does not argue. Slots are how a reform stays in the century without looking like a reform.""",
    """Amazon is a post office that learned to smile. A courier is a postman with a rating. You still perform Hill's trick every time you check out: the sender pays, the door does not get a veto, volume is the business. That is not an insult. It is a family resemblance. The tracking map on your phone is a clerk who finally stopped arguing about miles in public and started arguing in a server. I am not telling you to mail a letter as a personality. I am telling you the personality was always the till. If sending still feels free, that is email talking, and email is postage that lost its square and kept the spam. The spam is honest. Honest is a word the Penny Black never needed, because the black square had already confessed: someone paid. Someone always pays. The question was only which side of the door. You already know which side you stand on when you tap buy. The tap is a Penny Black with no queen left to look at.""",
    """So what did we trade? We traded a world where a letter could be refused for a world where a letter is assumed welcome because the square says so. That assumption is real help: a soldier's note, a job offer, a bill you actually needed, a grandmother who could finally afford to write twice. Help can be a miracle and still be a till. We also gained a myth that postage is a tax on paper, that stamps are cute, that junk mail is weather. Weather is a word the prepaid use. We kept the knock and called it a slot. We kept the clerk and called it a tracking page. Both can be true and still not be a reason to forget the door used to have a vote. Deals can be rewritten. Some already were, quietly, when email made the square optional and the volume infinite. Infinite volume is a treaty with no doorstep. Treaties need more than glue. Glue is a truce you lick. A truce is not a post that learned to ask.""",
    """This is you. You will pick up the stamp. The corner will still stick. You will feel nothing, which is the victory. Put your thumb on the queen, or on the flag, or on the barcode that replaced her. That is not the sky and it is not a conversation. That is a schoolmaster's pamphlet, a penny post, a black square in eighteen forty, a mocked envelope that lost to a sticker, a clerk who stopped arguing miles, a door that lost its veto, and a tracking number that still collects at the counter. You are allowed to love the mail. You are allowed to text instead and feel modern for an evening. Just stop calling the prepaid square natural, or inevitable, or proof that sending is free. Tonight, when the corner sticks, look at it like a receipt from a doorstep that used to say no. The receipt is cheerful. The doorstep is the point. Send if you want. Know which debt you are still paying. The stick is cheerful. Cheerful is how a flipped debt stays on an envelope without looking like a tax.""",
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, five-second cadence)."""
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


# (slug, covers, prompt) — 132 unique stills, one every five seconds of target runtime.
_ROWS: list[tuple[str, str, str]] = [
    ("stamp-press", "You press a stamp onto an envelope.", "Stickman pressing a stamp on an envelope, MS Paint, white background."),
    ("tracking-god", "A tracking number appears like a receipt from a logistics god.", "Phone with tracking number, tiny halo, MS Paint."),
    ("corner-sticks", "The corner will stick. A tiny portrait means the debt is paid.", "Stamp corner sticking, tiny portrait, PAID, MS Paint."),
    ("not-political", "You will not think of it as a political act.", "Envelope labeled NOT POLITICS, stickman shrugging, MS Paint."),
    ("postage-job", "It feels like postage doing its job.", "Mailbox smiling, stickman posting, MS Paint."),
    ("receiver-paid", "The person who received the mail paid.", "Recipient stickman paying a postman, sender waving free, MS Paint."),
    ("write-free", "The sender could write for almost nothing.", "Sender writing cheap, empty coin purse far away, MS Paint."),
    ("refuse-knock", "The recipient could refuse the knock. The letter died on the doorstep.", "Door refusing a letter, letter dying on steps, MS Paint."),
    ("why-prepay", "Why do you pay before the letter leaves the house?", "House, letter leaving, money at the door vs stamp, MS Paint."),
    ("schoolmaster", "A British schoolmaster. A black square with a queen's face.", "Stick schoolmaster, black stamp with queen doodle, MS Paint."),
    ("receipt-flip", "Your stamp is a receipt that flipped who owes whom.", "Stamp receipt flipping a debt arrow, MS Paint."),
    ("lick-manners", "You lick the corner, or you don't. The glue learned manners.", "Tongue vs self-stick stamp, glue in a tuxedo, MS Paint."),
    ("corner-flattered", "The corner is flattered. That is its job.", "Smiling stamp corner, MS Paint."),
    ("pamphlet-voted", "The doorstep did not vote. A reform pamphlet did.", "Pamphlet ballot beating a doorstep, MS Paint."),
    ("older-letter", "Start with the older letter.", "Old sealed letter, no stamp, stickman, MS Paint."),
    ("stole-knock", "The stamp stole a knock and sold it back as a sticker.", "Stamp stealing a door knocker, STICKER tag, MS Paint."),
    ("letter-bet", "A letter was a bet. Distance cost money.", "Letter on a betting table, mileage coins, MS Paint."),
    ("london-scotland", "London to Scotland could cost a laborer's day.", "Map London-Scotland, wage envelope emptied, MS Paint."),
    ("taxi-meter", "Clerks counted sheets and miles like a taxi meter that never stopped.", "Clerk taxi meter on a letter, MS Paint."),
    ("far-end-pays", "The person at the far end paid.", "Far-end stickman handing coins to a postman, MS Paint."),
    ("unwanted-debt", "Anyone could send a letter you did not want. You still owed.", "Unwanted letter, bill attached, sad recipient, MS Paint."),
    ("people-refused", "People refused. They peeked at the address and shook their head.", "Window peek at envelope, head shake, MS Paint."),
    ("lovers-code", "Lovers coded the envelope so the beloved could send the postman away unpaid.", "Coded marks on envelope, lover waving postman off, MS Paint."),
    ("romance-loophole", "Romance wearing a loophole.", "Heart using a loophole in a fence, MS Paint."),
    ("gov-hated", "The government hated the loophole. The poor hated the bill.", "Crown vs loophole, poor stickman vs bill, MS Paint."),
    ("spam-knocked", "Spam used to knock, and the knock used to cost.", "Spam letter knocking, coin on the door, MS Paint."),
    ("door-filter", "Cost is how a door learned to be a filter.", "Door with a FILTER slot, coins, MS Paint."),
    ("stamp-deleted", "The stamp deleted the filter and called it progress.", "Stamp covering FILTER, trophy PROGRESS, MS Paint."),
    ("hill-1837", "Rowland Hill, schoolmaster, eighteen thirty seven, Post Office Reform.", "Stick Hill, pamphlet 1837, MS Paint."),
    ("not-tracking", "Not a prophet of your tracking app.", "Hill vs a phone tracking map with red X prophet hat, MS Paint."),
    ("cost-not-miles", "The real cost was not the miles. It was clerks arguing about miles.", "Clerks arguing over a map, ignored road, MS Paint."),
    ("uniform-cheap", "Uniform cheap postage, paid in advance, would stop the arguing.", "One penny coin stopping a clerk fight, MS Paint."),
    ("penny-post", "Eighteen forty: Uniform Penny Post. One penny, half-ounce, anywhere.", "Penny, letter, map of Britain, 1840, MS Paint."),
    ("may-sixth", "Sixth of May, eighteen forty: the Penny Black goes on sale.", "Calendar May 6, black stamp for sale, MS Paint."),
    ("victoria-profile", "Queen Victoria in profile. First adhesive postage stamp.", "Black rectangle queen profile stamp, MS Paint."),
    ("not-cute", "It was not cute. It was a machine for settled debt.", "Stamp machine labeled SETTLED, not a bow, MS Paint."),
    ("counter-not-door", "Settled at the counter, not at the door.", "Post counter PAID vs door with empty hand, MS Paint."),
    ("hill-volume", "Hill wanted volume. The poor writing to the poor.", "Many cheap letters between small houses, MS Paint."),
    ("tiny-flag", "A stamp feels like a tiny flag. It was a tiny receipt.", "Stamp as flag vs stamp as receipt, MS Paint."),
    ("face-so-kept", "The receipt learned a face so you would not lose it.", "Plain paper vs faced stamp in a drawer, MS Paint."),
    ("world-fights", "Watch the old world fight the sticker.", "Old clerks vs a stamp sticker, MS Paint."),
    ("sticker-insult", "A sticker that works is an insult to a profession.", "Stamp insulting a clerk hat, MS Paint."),
    ("mulready", "The Mulready envelope: decorated prepaid wrapper, mocked in weeks.", "Fancy MULREADY envelope, laughing stick people, MS Paint."),
    ("want-square", "People wanted the little black square, not Britannia allegory.", "Black square beating a Britannia drawing, MS Paint."),
    ("simpler-till", "Clerks on complicated rates had to learn a simpler till.", "Complex rate chart vs one-penny till, MS Paint."),
    ("forgers", "Forgers noticed a queen is easier to copy than a clerk's mood.", "Forger copying a queen stamp, clerk mood uncopied, MS Paint."),
    ("perforations", "Eighteen fifties: perforations so you could tear without scissors.", "Stamp sheet with holes, no scissors, 1850s, MS Paint."),
    ("habit-admission", "A tiny admission that the stamp had become a habit.", "Stamp as a habit badge, MS Paint."),
    ("us-1847", "United States, eighteen forty seven: Franklin and Washington stamps.", "Two US stamps Franklin Washington 1847, MS Paint."),
    ("different-accent", "The same job in a different accent.", "British stamp and US stamp shaking hands, MS Paint."),
    ("not-collect", "Not asking you to collect. Pointing at the swap.", "Collector album with red X, SWAP arrow, MS Paint."),
    ("refusable-to-square", "A knock that could be refused became a prepaid square.", "Refused knock becoming a prepaid square, MS Paint."),
    ("every-country", "Then every country learned the square.", "Globe covered in tiny stamps, MS Paint."),
    ("reform-travels", "The square is how a reform travels.", "Stamp with little legs walking, REFORM, MS Paint."),
    ("no-doorstep-wait", "Travel never has to stand on a doorstep waiting to be paid.", "Traveling stamp skipping a waiting doorstep, MS Paint."),
    ("rehook-important", "Rehook: you think a stamp proves the letter is important.", "Stamp as IMPORTANCE badge, stickman, MS Paint."),
    ("wax-seal", "The way a wax seal was proof.", "Wax seal vs stamp, MS Paint."),
    ("cash-up-front", "Importance was never the point. Cash-up-front was.", "Cash on a counter beating a wax seal, MS Paint."),
    ("email-volume", "Email deleted the square and kept the volume.", "Email eating a stamp, volume graph up, MS Paint."),
    ("volume-product", "Volume was the product.", "Product box labeled VOLUME, letters pouring, MS Paint."),
    ("tracking-penny", "A tracking number is a Penny Black that learned to ping.", "Penny Black with a ping radar, MS Paint."),
    ("postage-due", "Postage-due is a fossil of someone sending unpaid.", "POSTAGE DUE stamp fossil, MS Paint."),
    ("not-refuse-lifestyle", "Not nostalgic for refusing the postman as a lifestyle.", "Refusing postman with lifestyle red X, MS Paint."),
    ("un-nature-lick", "Trying to un-nature the lick.", "Nature sticker peeling off a licked stamp, MS Paint."),
    ("saliva-argument", "The lick is Hill's argument winning in your saliva.", "Hill pamphlet in a saliva drop, MS Paint."),
    ("qr-same", "A QR shipping label is the same argument wearing a barcode.", "QR label with a tiny stamp ghost, MS Paint."),
    ("door-no-negotiate", "The sender paid. The door does not negotiate.", "Door with a mute button, paid stamp, MS Paint."),
    ("prepaid-lock", "Prepaid is a lock on the envelope that does not look like a lock.", "Envelope lock disguised as a stamp, MS Paint."),
    ("colonies-copy", "Colonies copied the penny idea. Empires love a uniform till.", "Empire map, same penny till everywhere, MS Paint."),
    ("airmail-sky", "Airmail printed little planes and charged extra for the sky.", "Stamp with a tiny plane, extra coins, MS Paint."),
    ("registered-anxiety", "Registered mail sold anxiety as a signature.", "Registered letter, anxious signature, MS Paint."),
    ("money-orders", "The post office took money orders, gossip, and the state's fear.", "Post office: money, gossip, opened letter, MS Paint."),
    ("propaganda-face", "A stamp can be propaganda: dead president, bird, war bond.", "Three stamps: president, bird, war bond, MS Paint."),
    ("who-may-write", "A quiet census of who is allowed to write.", "Stamp as a census checklist of writers, MS Paint."),
    ("private-public", "A package feels private. A public machine is under it.", "Package with a public machine underneath, MS Paint."),
    ("junk-prepay", "Junk mail is the unwanted letter that learned to prepay itself.", "Junk mail wearing a stamp, cruel smile, MS Paint."),
    ("hill-didnt", "A joke Hill did not write and we still receive.", "Hill shaking head at junk mail, MS Paint."),
    ("prepaid-spam-plot", "The prepaid spam is the plot.", "Spam stamped PAID, labeled PLOT, MS Paint."),
    ("refuseable-dignity", "An unpaid knock at least could be refused.", "Unpaid knock with a dignity hat, MS Paint."),
    ("this-is-you", "This is you. A birthday card with a stamp from a strip of twenty.", "Stickman birthday card, stamp strip of 20, MS Paint."),
    ("return-label", "A return label that is a prepaid apology.", "Return label saying SORRY, prepaid, MS Paint."),
    ("wedding-email", "A wedding RSVP by email because stamps got expensive.", "Wedding invite vs email RSVP, pricey stamp, MS Paint."),
    ("not-victorian", "None of this makes you a Victorian.", "Modern stickman, Victorian hat with red X, MS Paint."),
    ("born-after-hill", "Born after Hill's pamphlet and Victoria's profile.", "Baby stickman, pamphlet, queen profile, MS Paint."),
    ("bad-tax-door", "A post office that decided the doorstep was a bad place to collect a tax.", "Doorstep BAD TAX, post office pointing away, MS Paint."),
    ("friend-not-billed", "Relief that your friend will not be billed for your handwriting.", "Friend not paying, handwriting letter, relieved, MS Paint."),
    ("flat-square", "A small flatness: a square that used to be a negotiation.", "Flat stamp square, old negotiation table faded, MS Paint."),
    ("paid-the-knock", "You paid for the knock in advance so it could become a slot.", "Knock becoming a mail slot, MS Paint."),
    ("slot-no-argue", "The slot does not argue.", "Silent mail slot, MS Paint."),
    ("reform-costume", "Slots are how a reform stays without looking like a reform.", "Mail slot in a disguise costume, MS Paint."),
    ("amazon-smile", "Amazon is a post office that learned to smile.", "Smiling box company hat on a post office, MS Paint."),
    ("courier-rating", "A courier is a postman with a rating.", "Postman with a five-star rating, MS Paint."),
    ("checkout-hill", "You perform Hill's trick at checkout: sender pays, door has no veto.", "Checkout, Hill ghost, door with no veto, MS Paint."),
    ("family-face", "Not an insult. A family resemblance.", "A postage stamp and a shipping box as cousins, MS Paint."),
    ("tracking-clerk", "The tracking map is a clerk who stopped arguing miles in public.", "Clerk inside a phone map, MS Paint."),
    ("till-personality", "The personality was always the till.", "Personality mask on a cash till, MS Paint."),
    ("email-free", "If sending feels free, that is email talking.", "Email speaking, FREE, MS Paint."),
    ("lost-square", "Email is postage that lost its square and kept the spam.", "Email with missing stamp hole, spam leftover, MS Paint."),
    ("spam-honest", "The spam is honest. Someone always pays.", "Honest spam pointing at a payer, MS Paint."),
    ("which-side", "The question was only which side of the door.", "Door, payer on sender side vs recipient side, MS Paint."),
    ("trade-refuse", "We traded a refuseable letter for a letter assumed welcome.", "Refused letter swapped for WELCOME stamp, MS Paint."),
    ("square-says-so", "Assumed welcome because the square says so.", "Stamp saying WELCOME, MS Paint."),
    ("soldier-note", "Help: a soldier's note, a job offer, a grandmother writing twice.", "Soldier letter, job envelope, grandmother two stamps, MS Paint."),
    ("miracle-till", "Help can be a miracle and still be a till.", "Halo on a cash till, MS Paint."),
    ("tax-on-paper", "A myth that postage is a tax on paper, that stamps are cute.", "CUTE stamp vs TAX ON PAPER, MS Paint."),
    ("junk-weather", "A myth that junk mail is weather.", "Junk mail as a weather cloud, MS Paint."),
    ("prepaid-weather", "Weather is a word the prepaid use.", "Prepaid stickman holding WEATHER, MS Paint."),
    ("knock-called-slot", "We kept the knock and called it a slot.", "Knock renamed SLOT, MS Paint."),
    ("clerk-called-page", "We kept the clerk and called it a tracking page.", "Clerk renamed TRACKING PAGE, MS Paint."),
    ("door-had-vote", "The door used to have a vote.", "Door in a voting booth, MS Paint."),
    ("email-optional", "Email made the square optional and the volume infinite.", "Optional stamp, infinite letters, MS Paint."),
    ("no-doorstep-treaty", "Infinite volume is a treaty with no doorstep.", "Treaty paper, missing doorstep, MS Paint."),
    ("glue-truce", "Glue is a truce you lick. Not a post that learned to ask.", "Licked glue truce vs asking postman, MS Paint."),
    ("pick-up-stamp", "You pick up the stamp. The corner will still stick.", "Callback: stickman lifting a stamp, corner sticky, MS Paint."),
    ("feel-nothing", "You will feel nothing, which is the victory.", "Blank calm face, sticking stamp, MS Paint."),
    ("thumb-queen", "Put your thumb on the queen, or the flag, or the barcode.", "Giant thumb on stamp queen then barcode, MS Paint."),
    ("not-conversation", "Not the sky and not a conversation.", "Stamp between red-X sky and red-X talk bubble, MS Paint."),
    ("pamphlet-penny", "A schoolmaster's pamphlet, a penny post, a black square.", "Pamphlet, penny, black square, MS Paint."),
    ("mocked-envelope", "A mocked envelope that lost to a sticker.", "Mulready losing to a stamp sticker, MS Paint."),
    ("clerk-stopped", "A clerk who stopped arguing miles.", "Tired clerk, quiet map, MS Paint."),
    ("door-lost-veto", "A door that lost its veto.", "Door VETO stamped cancelled, MS Paint."),
    ("tracking-counter", "A tracking number that still collects at the counter.", "Tracking number at a post counter, MS Paint."),
    ("love-the-mail", "You are allowed to love the mail.", "Happy stickman with letters, MS Paint."),
    ("text-instead", "You are allowed to text instead and feel modern.", "Stickman texting, smug, stamp unused, MS Paint."),
    ("not-natural", "Stop calling the prepaid square natural.", "Stamp NATURAL sticker with red X, MS Paint."),
    ("sending-not-free", "Not proof that sending is free.", "FREE stamp with red X, MS Paint."),
    ("receipt-no", "When the corner sticks, a receipt from a doorstep that used to say no.", "Sticky stamp, doorstep saying NO faded, MS Paint."),
    ("cheerful-receipt", "The receipt is cheerful. The doorstep is the point.", "Cheerful receipt, doorstep silhouette, MS Paint."),
    ("know-debt", "Send if you want. Know which debt you are still paying.", "Stickman sending, stamp labeled which debt, MS Paint."),
    ("thumb-barcode", "The barcode replaced her face. The till did not.", "Barcode stamp vs queen face, till still there, MS Paint."),
    ("stick-cheerful", "The stick is cheerful. Cheerful is how a flipped debt stays.", "Smiling sticky stamp, flipped debt arrow, MS Paint."),
    ("slot-callback", "The mail slot. Hill. Victoria. Your thumb.", "Final callback: mail slot, three tiny labels, stickman thumb, MS Paint."),
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
        title="Why You Pay Before the Letter Leaves",
        description=(
            "A stamp feels like a decoration. It is a receipt that flipped the debt. "
            "Recipient-paid mail, Rowland Hill, the Penny Black, a door that lost its veto. "
            "Tracking is just a clerk in your phone."
        ),
        tags=(
            "stamp",
            "mail",
            "postage",
            "history",
            "penny-black",
            "hill",
            "why",
            "letters",
            "post",
            "tracking",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="PAY FIRST?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why You Pay Before the Letter Leaves",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-stamp.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print(out)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))
    print("accent", scenario.subtitles.accent_color, "stroke", scenario.subtitles.stroke_width)
    print("rate", scenario.tts.rate)
    print("hook", scenario.youtube.thumbnail_hook)


if __name__ == "__main__":
    main()

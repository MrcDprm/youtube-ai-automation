"""Author episode 8: the keyboard order is a typewriter fossil, then write senaryo-paint.json."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you will type a message with two thumbs. You will not think about the order of the letters. Q, W, E, R, T, Y. The top row looks like a word that got drunk and fell over. It feels like weather. Here is the part that should bother you. That order was cut for a machine whose metal arms jammed if neighboring keys fired too fast, in Milwaukee, in the eighteen seventies. Your phone has no arms. It has glass, a dictionary, and a little gray bar that guesses the next word as if guessing could forgive the layout. So why do you still type as if a hammer might tangle with its neighbor? Because a keyboard that won a sales floor never had to win a fair race, and then offices trained millions of fingers until switching felt like a personality change. That is the whole plot. Your keyboard is not a map of English. It is a fossil of a typewriter that needed to look clever in a shop window, and then the shop window became the world. You still tap the fossil. The fossil is flattered. That is its job.""",
    """Start with the older writing, because the keyboard stole the alphabet and then scrambled it like that was literacy. For most of history, making a letter meant a hand, a chisel, a brush, or a compositor picking bits of metal from a case. The alphabet had an order you sang as a child. Early writing machines sometimes tried to honor that song. Keys in neat rows of A B C. It looked honest. It was also slow, and the typebars, those little metal fingers that slap ink onto paper, liked to collide when common English pairs sat next to each other like neighbors who share a wall. Christopher Latham Sholes was a Milwaukee newspaper man and tinkerer, not a prophet of your thumbs. In the late eighteen sixties he and his partners kept rearranging a wooden prototype so the gadget would type without tying itself in knots. They were not optimizing your poetry. They were trying to sell a machine that did not embarrass itself in the first ten seconds. The alphabet was a suggestion. The jam was a boss. If a letter pair made the arms kiss, the letter pair lost, even if English needed it every other word.""",
    """The machine left the workshop the way a lot of American gadgets left the workshop: it got bought by people who already knew how to make metal behave. In eighteen seventy three, E. Remington and Sons, the gun makers, took on Sholes's design. The Remington Number One went to market looking like a sewing machine that had decided to become a clerk. Early models typed only capital letters. The Remington Number Two, a few years later, added a shift key, which is a polite way of saying the alphabet now had an upstairs. The popular story says QWERTY spread the most common letter pairs so the typebars would not kiss. That is part of the weather. Another part is colder and funnier. The top row can spell TYPE WRITER. A salesman could hammer the product name without hunting. If your layout still feels like nature, notice that nature arranged a billboard. I am not saying a demo trick is the only parent. I am saying the child does not remember which parent paid for dinner, and you are eating with both of them every time you log into email. The shop window won.""",
    """Hunt-and-peck does not lock a nation. Muscle memory does. For years a typewriter was a hunt. Two fingers, eyes on the keys, the machine as a piano you refused to learn. Then offices wanted speed as a job, not as a hobby. In eighteen eighty eight, in Cincinnati, Frank McGurrin, who typed without looking, raced Louis Taub, who hunted. McGurrin won, and the win traveled as a rumor with a stopwatch. Touch typing turned the layout into a labor skill. Schools drilled it. Secretarial colleges sold it. Home keys grew little bumps so your index fingers could find F and J without a glance, which is a tiny kindness and also a tiny tattoo. Once your rent depended on where those letters lived, the letters became geography, not preference. You can argue about a better map in a journal. You cannot argue with a thousand people who will be slower for six months on purpose. The keyboard stopped being a device. It became a dialect of the hands. Dialects do not hold referendums. They hold jobs.""",
    """Other maps existed, which is how you know this one was a choice. In nineteen thirty six, August Dvorak and William Dealey patented a simplified keyboard that put frequent English letters on the home row, the row where your resting fingers already live. Vowels under the left hand. Common consonants under the right. It looks, if you squint, like someone finally asked English what it wanted. The United States Navy ran tests in the nineteen forties that made Dvorak look like a miracle diet for fingers. Later readers poked holes: messy methods, a designer too close to the classroom, a government study by Earle Strong in the nineteen fifties that said retraining typists was not worth the lost weeks. I am not crowning a winner in a typing Olympics. I am pointing at the trap. Even a kinder layout has to climb a mountain of already-trained hands. The mountain is the product. The patent is a postcard from the other side.""",
    """This is the rehook. You think QWERTY survived because it is good enough, the way a river survives because water is wet. Your phone has no typebars. Nothing jams. In the years of the number pad, T nine tried a different logic: three letters on a key, a dictionary to guess which word you meant. Then a slab of glass put a typewriter on your thumbs because the installed base was not the hardware. The installed base was you. In nineteen eighty five the economic historian Paul David published a famous paper that used QWERTY as a parable of lock-in: a standard can win early, then sit on the throne because switching is expensive, not because the throne is wise. Other economists later argued he oversold the tragedy, that QWERTY is not clearly a lemon. Fine. The parable still fits your pocket. The glass did not choose English. The glass chose your habits, and then sold you a gray bar to apologize for the choice. An apology is not a redesign. It is a nurse for a fossil that still has to go to work.""",
    """Watch the lock travel. France got A ZERTY. German-speaking rooms got Q WERT Z. The Z and the W swapped like neighbors who could not agree on a fence, and then a century of schoolchildren treated the fence as geology. Colemak and other modern layouts live on the internet the way rare birds live in a preserve: loved, documented, and statistically not how you buy a laptop at an airport. You can remap a machine in an evening. You cannot remap a job interview, a library catalog, a hospital terminal, a cousin's laptop at Thanksgiving. Compatibility is a kindness. It is also a velvet rope. The rope says everyone can sit down. The rope also says no one gets to stand up and rearrange the chairs. When autocorrect saves you, it is not proving QWERTY is smart. It is proving the fossil needed a nurse, and the nurse is now a product with a cute animation. Cute is how a lock stays in the room.""",
    """This is you, already, in the middle of the story. Ten-finger typing was a desk sport. Two-thumb typing is a walk sport. The layout designed, maybe, to keep metal arms from kissing is now being stabbed by two blunt instruments that never heard of Milwaukee. The mismatch should have been a redesign meeting. Instead it became a billion tiny corrections: swipe, suggest, the little bubble that thinks you meant their, not there. None of that makes you bad at language. It makes you a person born after Remington and after secretarial college and after a phone company decided that a familiar wrong map beats an unfamiliar right one. You can feel both in the same sentence: relief that the gray bar caught the typo, and a tiny shame that your hands still live in eighteen seventy eight. The shame is unearned. The date is not. If the keys feel inevitable, that is the training talking.""",
    """So what did we trade? We traded a chance, at every new machine, to ask English for a better home row, for a continuity that lets you sit at a stranger's keyboard and still be a person. That continuity is real. It is how offices, libraries, and your uncle's clunky laptop stay in the same country. We also gained a myth that the alphabet wanted this, that QWERTY is a puzzle you are supposed to be proud of solving, like a rite. The rite is a job skill wearing a nursery song. We kept the sales-row accident and called it literacy. We kept the jam-avoidance rumor and called it science. Both rumors can be partly true and still not be a reason to carve the same scar into glass. Deals can be rewritten. Some already were, quietly, when phones added swipe and prediction and called it magic. Magic is a keyboard that never quite has to confess. Confession would look like a blank home row and a week of feeling stupid on purpose. Markets hate that week.""",
    """This is you. You will pick up the phone. The letters will still sit in that drunk-row order. You will feel nothing, which is the victory. Put your thumb on Q. That is not the sky and it is not the alphabet you sang. That is a Milwaukee prototype, a Remington shop, a top row that could type the product name, a Cincinnati contest, a nineteen thirty six patent that lost to muscle, a nineteen eighty five parable about lock-in, and a slab of glass with no hammers that still flinches like a hammer might come back. You are allowed to keep QWERTY. You are allowed to learn another layout in a fit of spite. Just stop calling the order natural, or inevitable, or proof that you are bad at keyboards. Tonight, when the keys light up, look at them like a typewriter that shed its arms and kept its grin. The grin is cheerful. The arms are the point. Type if you want. Know which machine you are still feeding.""",
]

BEATS: list[tuple[str, str, str]] = [
    (
        "0000-thumbs-phone",
        "You type a message with two thumbs and do not think about the letter order.",
        "Round-head stickman two thumbs on a simple phone keyboard, MS Paint, white background.",
    ),
    (
        "0008-qwerty-row",
        "Q W E R T Y. The top row looks like a drunk word.",
        "Giant wobbly keys Q W E R T Y in a row, stickman staring, MS Paint.",
    ),
    (
        "0016-feels-weather",
        "The order feels like weather.",
        "Keyboard under a smiling sun and a cloud, as if the layout were climate, MS Paint.",
    ),
    (
        "0024-milwaukee-jams",
        "Cut for a machine whose metal arms jammed in Milwaukee in the eighteen seventies.",
        "Old typewriter with tangled metal arms, tiny Milwaukee label, eighteen seventies, MS Paint.",
    ),
    (
        "0032-phone-no-arms",
        "Your phone has no arms. Glass, a dictionary, a gray guess bar.",
        "Phone with a gray suggestion bar, no typewriter arms, confused stickman, MS Paint.",
    ),
    (
        "0042-sales-floor",
        "A keyboard that won a sales floor never had to win a fair race.",
        "Shop window typewriter trophy beating a racing typewriter, MS Paint.",
    ),
    (
        "0052-fossil-window",
        "Your keyboard is a fossil of a typewriter that looked clever in a shop window.",
        "Fossil keyboard in a shop window, stickman tapping it, MS Paint.",
    ),
    (
        "0108-old-writing",
        "Older writing: hand, chisel, compositor picking metal type.",
        "Stick compositor picking letter blocks from a case, quill nearby, MS Paint.",
    ),
    (
        "0122-abc-keys",
        "Early machines tried honest A B C rows.",
        "Keyboard labeled A B C in neat rows, honest smile, MS Paint.",
    ),
    (
        "0136-typebars-kiss",
        "Typebars collided when common English pairs sat next door.",
        "Two metal typebars kissing and jamming, letter pair next door, MS Paint.",
    ),
    (
        "0150-sholes",
        "Christopher Latham Sholes, Milwaukee newspaper man, rearranging a wooden prototype.",
        "Stick inventor at a wooden keyboard prototype, name SHOLES, MS Paint.",
    ),
    (
        "0206-jam-was-boss",
        "The alphabet was a suggestion. The jam was a boss.",
        "Alphabet hat in a suggestion box, a boss labeled JAM, MS Paint.",
    ),
    (
        "0222-remington-1873",
        "Eighteen seventy three: Remington the gun makers take the design.",
        "Gun factory handing a typewriter a name tag REMINGTON 1873, MS Paint.",
    ),
    (
        "0238-number-one",
        "Remington Number One looked like a sewing machine that became a clerk.",
        "Sewing-machine-shaped typewriter with a clerk hat, MS Paint.",
    ),
    (
        "0254-shift-upstairs",
        "Number Two added a shift key. The alphabet got an upstairs.",
        "Keyboard house with SHIFT stairs to capital letters upstairs, MS Paint.",
    ),
    (
        "0312-type-writer-row",
        "The top row can spell TYPE WRITER. A salesman demo.",
        "Top-row keys lighting up TYPE WRITER, salesman stickman pointing, MS Paint.",
    ),
    (
        "0328-billboard-nature",
        "If the layout feels like nature, notice nature arranged a billboard.",
        "Tree growing a TYPE WRITER billboard instead of leaves, MS Paint.",
    ),
    (
        "0344-hunt-peck",
        "For years typing was a hunt. Two fingers, eyes on the keys.",
        "Stickman pecking two keys, eyes glued to the keyboard, MS Paint.",
    ),
    (
        "0400-mcgurrin-1888",
        "Eighteen eighty eight Cincinnati: McGurrin touch-types, beats Taub.",
        "Typing race, blindfold typist vs hunter, banner CINCINNATI 1888, MS Paint.",
    ),
    (
        "0416-home-bumps",
        "Home keys grew bumps so fingers could find F and J.",
        "F and J keys with little bumps, two index fingers landing, MS Paint.",
    ),
    (
        "0432-dialect-jobs",
        "The keyboard became a dialect of the hands. Dialects hold jobs.",
        "Hands speaking a dialect into a job office, keyboard mouth, MS Paint.",
    ),
    (
        "0448-dvorak-1936",
        "Nineteen thirty six: Dvorak and Dealey patent a home-row English layout.",
        "Patent paper DVORAK 1936, home row full of common letters, MS Paint.",
    ),
    (
        "0506-navy-tests",
        "Navy tests in the nineteen forties made Dvorak look like a miracle.",
        "Navy hat, stopwatch, Dvorak keyboard glowing, MS Paint.",
    ),
    (
        "0522-strong-study",
        "Earle Strong in the nineteen fifties: retraining was not worth the weeks.",
        "Government stamp NOT WORTH IT, tired retraining class, MS Paint.",
    ),
    (
        "0538-mountain-hands",
        "A kinder layout still has to climb a mountain of trained hands.",
        "Dvorak postcard at the foot of a mountain made of hands, MS Paint.",
    ),
    (
        "0554-phone-no-jam",
        "Rehook: your phone has no typebars. Nothing jams.",
        "Phone next to a typewriter, typewriter jammed, phone shrugging, MS Paint.",
    ),
    (
        "0610-t-nine",
        "T nine put three letters on a number key and guessed.",
        "Old number pad with ABC on 2, dictionary guessing a word, MS Paint.",
    ),
    (
        "0626-paul-david",
        "Nineteen eighty five: Paul David uses QWERTY as a lock-in parable.",
        "Book labeled LOCK-IN 1985, throne with a QWERTY crown, MS Paint.",
    ),
    (
        "0642-gray-bar-nurse",
        "The glass chose your habits, then sold a gray bar to apologize.",
        "Phone gray bar saying SORRY, nursing a fossil keyboard, MS Paint.",
    ),
    (
        "0658-azerty-qwertz",
        "France got AZERTY. German rooms got QWERTZ. Local fences as geology.",
        "Two maps, AZERTY and QWERTZ, a fence between Z and W, MS Paint.",
    ),
    (
        "0716-airport-laptop",
        "You cannot remap a hospital terminal or a cousin's laptop at Thanksgiving.",
        "Stickman at Thanksgiving with a cousin laptop, remap with a red X, MS Paint.",
    ),
    (
        "0732-velvet-rope",
        "Compatibility is a kindness and a velvet rope.",
        "Velvet rope around chairs that are all the same keyboard, MS Paint.",
    ),
    (
        "0748-thumbs-vs-ten",
        "Ten-finger desk sport. Two-thumb walk sport. Same map.",
        "Split: ten fingers at a desk vs two thumbs walking, same QWERTY, MS Paint.",
    ),
    (
        "0806-autocorrect-bubble",
        "Swipe, suggest, a bubble that thinks you meant their not there.",
        "Typo bubble fixing THEIR, stickman thumbs, MS Paint.",
    ),
    (
        "0822-shame-1878",
        "Tiny shame that your hands still live in eighteen seventy eight.",
        "Calendar 1878 taped to a modern phone, blushing stickman, MS Paint.",
    ),
    (
        "0838-stranger-keyboard",
        "Continuity lets you sit at a stranger's keyboard and still be a person.",
        "Stickman sitting at a stranger's laptop, still able to type, MS Paint.",
    ),
    (
        "0854-magic-confess",
        "Swipe and prediction called magic. Magic is a keyboard that never confesses.",
        "Magic hat on a keyboard, a locked confession diary, MS Paint.",
    ),
    (
        "0920-thumb-on-q",
        "You pick up the phone. Put your thumb on Q.",
        "Callback: stickman thumb pressing a giant Q key on a phone, MS Paint.",
    ),
    (
        "0940-not-the-alphabet",
        "Not the sky, not the alphabet you sang. Milwaukee, Remington, the sales row.",
        "Q key exploding into tiny icons: workshop, gun factory, TYPE WRITER row, MS Paint.",
    ),
    (
        "1030-grin-no-arms",
        "A typewriter that shed its arms and kept its grin. Type. Know the machine.",
        "Smiling typewriter with no arms, stickman typing on glass, MS Paint.",
    ),
]


def main() -> None:
    draft = DraftScript(
        title="Why Your Keyboard Is In The Wrong Order",
        description=(
            "QWERTY feels like the alphabet. It was a Milwaukee typewriter layout. "
            "Remington, a sales-row trick, a Cincinnati typing race, Dvorak in "
            "nineteen thirty six, lock-in on glass with no hammers. Your phone still "
            "types like eighteen seventy eight."
        ),
        tags=(
            "keyboard",
            "qwerty",
            "typewriter",
            "history",
            "tech",
            "machine",
            "why",
            "layout",
            "phone",
            "typing",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in BEATS
        ),
        thumbnail_hook="WRONG KEYS?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Your Keyboard Is In The Wrong Order",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 24, tzinfo=UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-qwerty.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print(out)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))


if __name__ == "__main__":
    main()

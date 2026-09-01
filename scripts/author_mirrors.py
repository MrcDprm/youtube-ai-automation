"""Author episode 4: cheap glass invented your face, then write senaryo-paint.json."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you are going to walk into a bathroom and check your face. You will not think of it as an event. You will tilt your head. You will hunt a hair. You will decide if you look like a person who can leave the house. The glass will agree or it will not, and you will obey it. Here is the part that should bother you. For most of human history, that check did not exist. You had a face the way you have a back. Other people saw it. You did not. You lived inside a head you could not inspect, and that was not a philosophy. It was physics. A still pond gave you a wobble. A polished bronze disk gave the rich a brown ghost. Ordinary people went to the grave having never once seen themselves the way you will see yourself before breakfast. So why does a cheap rectangle on a wall get to tell you who you are? Because glass got cheap. That is the whole plot. Your self-consciousness is a manufacturing story, and the factory is still running every time you flip on the bathroom light. The habit feels as old as washing. It is not. It is younger than a lot of the houses still standing on your street.""",
    """Start with what a face was before glass. You knew your hands. You knew your feet if you sat down. Your face was a rumor you wore. Family told you that you had your father's mouth. Enemies told you that you looked tired. A lover told you that you were beautiful, which is a sentence you could not fact-check against anything except more sentences. Painters and coins reserved likeness for kings. The rest of us were descriptions walking around. In some places you could stoop over black water and meet a shaken version of yourself, then lose it when the wind arrived. Archaeologists have found polished obsidian from places like Catalhoyuk, six thousand years back, little dark mirrors for people who could get them. Bronze and silver disks followed for people who could pay. These were not bathrooms. They were objects you took out, angled toward a window, and put away. A face was a visit, not a habit. You did not have a relationship with your outline. You had errands.""",
    """Venice turned the visit into a treasure. On the island of Murano, glassmakers learned to back glass with tin and mercury and make a reflection that was bright enough to feel like a second room. The Republic treated the recipe like a weapon. Craftsmen were paid well and watched closely. Stories from the fifteen hundreds say a glassmaker who took the secret abroad could be hunted. Whether every tale is tidy or not, the policy is clear in the surviving rules. A good mirror was not a grooming tool. It was state property wearing the costume of furniture. Ambassadors wrote home about Venetian glass as if they were describing a navy. If you have ever paid too much for a thing that only shows you yourself, you are in an old tradition. The difference is that those buyers were buying a monopoly measured in months of wages, and you are buying a checkout item next to soap. Same hunger. Different receipt.""",
    """France got tired of importing that monopoly. In the sixteen sixties, Jean-Baptiste Colbert, the minister who treated the French economy like a machine to be tuned, wanted mirrors made at home so the silver would stop leaving the country. Venetian workers were lured, bribed, or smuggled toward Paris. The royal manufactory that became Saint-Gobain started pouring French glass in sheets big enough to intimidate a visitor. Then Louis the Fourteenth lined a hall at Versailles with them. The Hall of Mirrors is easy to file under pretty. Do not. It is a flex. A corridor of faces repeating, light bouncing, visitors seeing themselves among the king. You were not meant to feel cozy. You were meant to feel small and multiplied. The most powerful room in Europe was, among other things, a bathroom scaled up into a threat. Reflection had become politics you could walk through, and the walk was the point. If a king spends a fortune so you can watch yourself shrink, the fortune is not about grooming. It is about who owns the image of a face in a room.""",
    """Then chemistry ruined the exclusivity, which is the kindest thing chemistry has done for your ego and the cruelest. In eighteen thirty five, Justus von Liebig published a way to deposit silver on glass without the worst of the old mercury craft. The laboratory details matter less than the shop price. Across the later eighteen hundreds, silvered mirrors climbed down the class ladder one room at a time. Shop windows. Wardrobes. Hotel lobbies. A washstand in a rented room. For the first time, a clerk and a mill worker could own a daily face. Churches had warned about vanity for centuries, usually while the priest had better access to glass than the pew. Now vanity had hardware in the house. You did not need a court invitation to be accused by your own outline. The moral panic arrived late, as moral panics do. The glass was already over the sink, doing its job without a sermon.""",
    """This is the rehook. You think you have always known what you look like. You have not. Your great-great-grandparents, if they were ordinary, might have had one decent mirror in the house, shared among six people, or none at all. They knew their face from other people's flinches and compliments, from a wedding daguerreotype if they were lucky, from a barber's chair with someone else's mirror. A face was social. It happened between people. Cheap glass pulled the face inward. You started rehearsing alone. You started correcting the mouth before anyone else arrived. That is a new kind of loneliness. It feels like hygiene. It is also a rehearsal for an audience that is not in the room. The first person you perform for, every morning, is a sheet of silvered silica that does not love you, cannot flinch, and cannot look away. That is a terrible director. You still take notes.""",
    """Photography finished what the cheap mirror started, then the phone finished photography. A painting used to be a rumor with talent and a rich patron. A photograph was a rumor with a machine and a wait. Now you carry a front camera that is a pocket Versailles you can open on a bus. You do not just check. You archive. You compare Tuesday's face to Thursday's as if a face were a stock price. You learn the angle that lies in your favor and call it your good side, which is a sentence no medieval farmer needed. People invent a self in the glass, then invent a second self for the lens, then wonder which one is the real punishment. None of this makes you vain in some eternal biblical sense. It makes you a person born after Liebig, after cheap film, after the little lens above the screen. The species did not evolve to curate a face. The species evolved to have one, and to let other people deal with it while you dealt with weather. The archive in your pocket is the newest room in that Hall of Mirrors, and it follows you to the grocery line.""",
    """Notice what the glass does to judgment. Before a clear daily mirror, ugly and handsome were mostly other people's problems. You could be cruel about a stranger in the market and still be vague about yourself, which is a kind of mercy you did not know you had. After the glass, you become the stranger. You score the chin. You invent a symmetry that nature did not owe you. Later centuries will sell you a return to a face you saw in bad lighting. Makeup becomes less of a festival paint and more of a correction layer you apply so the glass will stop arguing. I am not scolding the paint. I am pointing at the new job. The mirror hired you as the manager of a surface. Managers look for defects. That is what they are for. A pond never asked you to optimize. A phone camera never stops asking, and it keeps a file.""",
    """So what did we trade? We traded mystery for maintenance. We traded the chance to be surprised by a portrait for the chance to be disappointed before we lock the door. We also gained something honest. A boil is easier to treat if you can see it. A smile you practice can be a kindness in a hard week. Blindness to your own face was not a spiritual achievement. It was a materials limit, like not having a window. The trick, same as always, is pretending the new object is nature. It is not. It is Murano secrecy, a French hallway built to humble diplomats, a German chemist, a factory that silvered glass until a farmer's child could own a rectangle and take it personally. Your face as a daily project is younger than the steam engine and older than the selfie. That is a narrow window in the species. You are living in it like it was always the human condition, which is how every new object wins.""",
    """This is you. You will lean toward the glass. You will decide you look tired, or fine, or like someone who should try again. The verdict will feel personal, the way a grade feels personal when the test was written by a stranger. It is industrial. Put your hand on the cheap rectangle. That is not your soul looking back. That is silver and glass repeating photons, the same trick a Venetian wanted to kill a man over, the same trick a king used to humble a diplomat, the same trick Liebig made boring enough for a rental bathroom. You are allowed to comb your hair. You are allowed to like a day. Just stop letting a checkout-aisle invention write your character in permanent ink. Tonight, when you check, look once for dirt and once for history. The face in there is new. The hunger to manage it is newer. The bathroom is a museum that still has the water running, and you are the exhibit that keeps coming back.""",
]

BEATS: list[tuple[str, str, str]] = [
    (
        "0000-bathroom-check",
        "You walk into a bathroom and check your face.",
        "Round-head stickman at a bathroom sink leaning toward a rectangle mirror, MS Paint, white background.",
    ),
    (
        "0008-obey-glass",
        "The glass will agree or not, and you will obey it.",
        "Mirror with a simple face, stickman nodding yes, MS Paint.",
    ),
    (
        "0016-no-check",
        "For most of history that check did not exist.",
        "Empty wall where a mirror should be, confused stickman, red X, MS Paint.",
    ),
    (
        "0024-face-like-back",
        "You had a face the way you have a back.",
        "Stickman trying to see his own back and face, both impossible, MS Paint.",
    ),
    (
        "0032-never-saw",
        "Ordinary people never saw themselves the way you will before breakfast.",
        "Breakfast table, no mirror, stickman shrugging, MS Paint.",
    ),
    (
        "0042-glass-got-cheap",
        "Your self-consciousness is a manufacturing story.",
        "Factory making rectangles of glass, tiny FACE labels, MS Paint.",
    ),
    (
        "0052-face-was-rumor",
        "Your face was a rumor you wore.",
        "Stickman with speech bubbles from others: TIRED, FATHER MOUTH, MS Paint.",
    ),
    (
        "0108-cannot-factcheck",
        "A lover said you were beautiful. You could not fact-check.",
        "Two stickmen, a heart, a question mark on the listener, MS Paint.",
    ),
    (
        "0122-kings-coins",
        "Likeness was for kings on coins and paintings.",
        "Coin with a crown stick-face, ordinary stickman with no portrait, MS Paint.",
    ),
    (
        "0136-pond-wobble",
        "A still pond gave you a shaken version, then the wind took it.",
        "Stickman over a blue puddle, wobble lines, a wind puff, MS Paint.",
    ),
    (
        "0150-obsidian",
        "Polished obsidian at Catalhoyuk, six thousand years back.",
        "Black shiny disk, crude hut, label CATALHOYUK, 6000 YEARS, MS Paint.",
    ),
    (
        "0204-bronze-ghost",
        "Bronze disks gave the rich a brown ghost. A face was a visit.",
        "Rich stickman angling a bronze circle toward a window, then putting it away, MS Paint.",
    ),
    (
        "0220-murano",
        "Murano glassmakers made a reflection like a second room.",
        "Island labeled MURANO, bright mirror, a second tiny room inside it, MS Paint.",
    ),
    (
        "0236-state-secret",
        "Venice treated the recipe like a weapon.",
        "Locked recipe book, lion seal, glassmaker stickman watched by guards, MS Paint.",
    ),
    (
        "0252-hunted",
        "A glassmaker who took the secret abroad could be hunted.",
        "Stickman with a mirror running, arrows, stamp SECRET, MS Paint.",
    ),
    (
        "0310-monopoly-furniture",
        "A good mirror was state property wearing furniture costume.",
        "Fancy mirror with a crown and a price tag MONOPOLY, MS Paint.",
    ),
    (
        "0326-colbert",
        "Colbert wanted French mirrors. Venetian workers were lured.",
        "Minister stickman, bag of coins, glassmakers walking toward a French flag doodle, MS Paint.",
    ),
    (
        "0342-saint-gobain",
        "Saint-Gobain started pouring French glass.",
        "Glass factory labeled SAINT-GOBAIN, sheets of glass, MS Paint.",
    ),
    (
        "0358-versailles",
        "Louis the Fourteenth lined a hall at Versailles with mirrors.",
        "Long hallway of rectangle mirrors, tiny crown stickman, label VERSAILLES, MS Paint.",
    ),
    (
        "0416-flex",
        "The Hall of Mirrors is a flex, not cozy.",
        "Tiny visitor stickman dwarfed by repeating reflections, MS Paint.",
    ),
    (
        "0432-politics-walk",
        "Reflection had become politics you could walk through.",
        "Stick diplomats walking a mirrored hall, looking small, MS Paint.",
    ),
    (
        "0448-liebig",
        "Eighteen thirty five: Liebig silvered glass. The price fell.",
        "Chemist stickman, silver pour on glass, label LIEBIG 1835, MS Paint.",
    ),
    (
        "0506-class-ladder",
        "Mirrors climbed down to shops, wardrobes, rented washstands.",
        "Shop window, wardrobe, hotel sink, each with a cheap mirror, MS Paint.",
    ),
    (
        "0522-vanity-hardware",
        "Vanity now had hardware in the house.",
        "Sermon stickman pointing, a mirror already over a sink, MS Paint.",
    ),
    (
        "0538-always-known-x",
        "You think you have always known what you look like. You have not.",
        "Stickman pointing at his reflection, big red X on ALWAYS, MS Paint.",
    ),
    (
        "0554-social-face",
        "A face was social. It happened between people.",
        "Three stickmen looking at one face, no mirror, MS Paint.",
    ),
    (
        "0610-rehearse-alone",
        "Cheap glass pulled the face inward. You rehearse alone.",
        "Stickman practicing a smile at a mirror, empty room, MS Paint.",
    ),
    (
        "0626-silver-silica",
        "The first audience is a sheet of silvered silica that cannot look away.",
        "Mirror labeled SILICA staring, stickman performing, MS Paint.",
    ),
    (
        "0642-front-camera",
        "The phone is a pocket Versailles.",
        "Stickman holding a phone, tiny Hall of Mirrors inside the screen, MS Paint.",
    ),
    (
        "0658-archive-face",
        "You archive Tuesday's face and compare it to Thursday.",
        "Two phone pictures of a stick-face labeled TUE and THU, MS Paint.",
    ),
    (
        "0716-not-evolved",
        "The species did not evolve to curate a face.",
        "Timeline ape to stickman, a red X over a selfie, MS Paint.",
    ),
    (
        "0732-you-are-stranger",
        "After the glass, you become the stranger you judge.",
        "Stickman pointing at his mirror-self like a stranger, MS Paint.",
    ),
    (
        "0748-manager-surface",
        "The mirror hired you as manager of a surface.",
        "Stickman in a tiny manager tie inspecting a face clipboard, MS Paint.",
    ),
    (
        "0804-pond-never-asked",
        "A pond never asked you to optimize.",
        "Peaceful puddle vs a phone camera with a demand bubble FIX, MS Paint.",
    ),
    (
        "0822-mystery-maintenance",
        "We traded mystery for maintenance.",
        "Mystery box crossed out, a wrench on a face, MS Paint.",
    ),
    (
        "0840-narrow-window",
        "Daily face-as-project is younger than the steam engine.",
        "Steam engine, then a mirror, then a selfie, a narrow bracket labeled YOU ARE HERE, MS Paint.",
    ),
    (
        "0920-lean-verdict",
        "You lean in and the verdict feels personal. It is industrial.",
        "Bathroom stickman, factory stamp INDUSTRIAL on the mirror, MS Paint.",
    ),
    (
        "0940-hand-on-glass",
        "Put your hand on the cheap rectangle. Photons, not a soul.",
        "Stick hand on a mirror, dotted light arrows bouncing, label PHOTONS, MS Paint.",
    ),
    (
        "1005-checkout-character",
        "Do not let a checkout-aisle invention write your character.",
        "Store checkout, cheap mirror in a cart, stickman walking away, MS Paint.",
    ),
    (
        "1030-bathroom-museum",
        "Look once for dirt and once for history. The bathroom is a museum.",
        "Callback: same bathroom mirror, tiny museum labels MURANO LIEBIG, water still running, MS Paint.",
    ),
]


def main() -> None:
    draft = DraftScript(
        title="Why Cheap Glass Invented Your Face",
        description=(
            "You check the bathroom mirror like it is nature. Most humans never saw "
            "their own face clearly. Murano secrecy, Versailles, Liebig's cheap silvering. "
            "Self-consciousness is a manufacturing story."
        ),
        tags=(
            "mirrors",
            "history",
            "glass",
            "venice",
            "versailles",
            "self image",
            "psychology",
            "why",
            "face",
            "liebig",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in BEATS
        ),
        thumbnail_hook="YOUR FACE?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Cheap Glass Invented Your Face",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 23, tzinfo=UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-mirrors.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print(out)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))


if __name__ == "__main__":
    main()

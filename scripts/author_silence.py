"""Author episode 10: quiet used to be a room, then a product with a battery."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you will put on a pair of over-ear headphones and the bus will die. Not the engine. The people. The hiss of the door. The kid's video with no headphones of its own. You will press a cup of plastic over each ear and the city will become a movie with the sound turned down, which will feel like a small personal miracle and not like a purchase. Here is the part that should bother you. Silence used to be the default setting of a room. It did not come with a charging cable. It did not require a brand. It did not cost three hundred dollars to make a train bearable. So why does quiet now feel like a luxury good you wear on your head? Because factories learned to shout, cities learned to never stop, and then a professor on an airplane decided the only polite response was to invent a machine that argues with the air. That is the whole plot. Your headphones are not peace. They are a refund. You still tap the earcup. The earcup is flattered. That is its job. The mill did not vote. A catalog did, and then a commute that taught your hands the seal until the seal started calling itself calm.""",
    """Start with the older quiet, because the headphone stole a room and then sold it back as a feature. Before mills, the loud things had names you could point at: a storm, a dog, a bell, a market day. Night was still mostly dark and mostly not a factory. A village was not silent like a studio. It was quiet like a place that ran out of reasons to bang. Then steam arrived, and steam does not know how to whisper. A Lancashire mill in the eighteen hundreds was a room of belts and iron that ate conversations for lunch. Workers learned to lip-read. They went home with a ringing that did not belong to any bird. The ringing was not a vibe. It was an injury that learned to commute. If your open office still feels a bit much, notice that a bit much used to be a mill floor, and the mill floor did not offer a noise-cancel button. It offered cotton and a wage. The wage did not include your ears. The ears were a donation you did not remember signing. Progress counted looms. It did not count the leftover ring.""",
    """Cities turned the mill inside out and called it progress. In nineteen hundred six, in New York, Julia Barnett Rice, a physician with money and a low tolerance for tugboat horns, founded the Society for the Suppression of Unnecessary Noise. That name is a joke until you live next to a river of boats that honk as if honking were a personality. She went after children's hospitals being kept awake by steam whistles. She got quiet zones. She got ordinances. She was not a monk. She was a person who noticed that noise is a thing the powerful can dump on the less powerful and then call it commerce. The elevated train did not ask your bedroom for consent. The factory whistle did not RSVP. If your leaf blower still feels like a neighbor's right, Rice would like a word. The word is unnecessary. Unnecessary is a moral category wearing a civic hat. A civic hat is slower than a product page, which is why the product page won the century and the hat had to settle for a quiet zone around a hospital that still had to sleep.""",
    """Watch silence become etiquette, because etiquette is how a class teaches its volume. A library is a room that decided thinking is a group project that requires nobody to speak. That is a beautiful deal and also a velvet rope. If you grew up in a loud kitchen, the library can feel like a test you were not told about. Open-plan offices later reversed the deal: thinking would now happen in a warehouse of other people's calls, and if you hated it you were not a team player. The team did not vote. The furniture did. Cubicle walls got shorter. Headphones got bigger. The headset at your desk is a portable library carrel you bought because the building refused to be one. I am not nostalgic for shushing librarians as a police force. I am pointing at the swap. We took a shared quiet, turned it into a personality, then sold the personality as foam and a wireless chip. Personality is a word that never has to sit in the food-court office. The food-court office just sends you a calendar invite labeled focus time, which is a joke the walls tell with a straight face.""",
    """This is the rehook. You think silence is empty, the way a blank page is empty. In nineteen fifty two, at the Maverick Concert Hall in Woodstock, New York, John Cage premiered four minutes and thirty-three seconds of a pianist not playing. The piece is a prank until you sit in it. You hear chairs. You hear rain. You hear yourself. Cage had already sat in an anechoic chamber, a room built to eat echoes, and he still heard his nervous system, a high tone and a low tone, blood and nerves refusing to be mute. I am not assigning you homework in experimental music. I am trying to un-nature the earcup. The quiet you buy is not the absence of the world. It is a filter with a logo. Even a room later advertised as the quietest on earth, a tourist attraction for nothing in Minneapolis, still gives you your body as a radio. Your headphones cannot fire your blood. They can only argue with the bus. Argument is not peace. Argument is a product that needs a battery, and a battery is a tiny admission that the room lost.""",
    """Amar Gopal Bose was an MIT professor who liked music and hated the way airplanes sounded. On a transatlantic flight in nineteen seventy eight, he put on the airline headphones and the engine came through like a roommate who never leaves. He started sketching a headset that would listen to the noise and play its opposite, a little war in the ear canal. By nineteen eighty nine, Bose was selling active noise control to pilots. The consumer version arrived later, wrapped in silver and the promise that your commute could be a studio. The science is real. The marketing is a lullaby. Anti-noise is a clever trick of physics. Selling it as peace is a clever trick of a catalog. If your quiet-comfort still feels like self-care, notice that self-care is often a patch you wear so the city does not have to lower its voice. The patch is allowed. The city is the plot. A plot can be rewritten. A catalog would prefer you not notice the rewrite is possible, because a quieter street does not need a sequel of earcups.""",
    """Watch the lock travel. First-class cabins sell quiet as a seat. Quiet cars on trains draw a chalk line through courtesy and then argue about phone calls like theology. Hotels sell soundproof the way they sell thread count, a number that means please do not hear the other guests living. Leaf blowers, motorcycle packs, night construction, the scooter with a speaker: the street learned to be a loudspeaker, and then the store learned to sell you earmuffs with a battery. Airports sell silence in a bottle of foam. Schools send home notes about noise-sensitive kids as if the building's air system were weather. You can buy a better filter. You cannot buy a quieter block without politics. Politics is slower than two-day shipping. Two-day shipping is how a lock stays in the room. The lock looks like self-respect. Self-respect is allowed. Just notice it is also a subscription to not hearing the neighbors the city declined to regulate, which is a polite way of saying your ears became the zoning board.""",
    """This is you, already, in the middle of the story. Two cups on your ears on a Tuesday. An open office that sounds like a food court. A video you watch at one in the morning with the volume down and the cancel up, which is a funny way to be alone in a building full of other alones. None of this makes you fragile. It makes you a person born after the mill and after the elevated train and after a professor on a plane decided the air should lose an argument. You can feel both in the same commute: relief that the toddler speaker died, and a small shame that peace required a product. The shame is unearned. The product is not free. If the quiet feels like your personality, that is the catalog talking. The catalog is cheerful. Cheerful is how a mill stays in the century without looking like a mill. You still commute through it. The commute is flattered. That is its job, and the job is to make the roar feel like your private weather instead of a public decision.""",
    """So what did we trade? We traded a chance, at every new street, to treat noise as pollution the way we treat smoke, for a gadget that lets the smoke continue. That gadget is real help for a night-shift worker, a student in a thin-walled apartment, a parent who needs ten minutes that are not a kitchen. Help can be a miracle and still be a receipt. We also gained a myth that quiet is a luxury personality, that expensive earcups are taste, that people who complain about leaf blowers are difficult. Difficult is a word the noisy use. We kept the mill in the city and called it vibrancy. We kept the airplane in the living room and called it a laptop. Both can be true and still not be a reason to carve the same roar into every block. Deals can be rewritten. Some already were, quietly, when a hospital got a quiet zone and a train got a quiet car. Quiet cars are tiny treaties. Treaties need more than foam. Foam is a truce you wear. A truce is not a street that learned manners.""",
    """This is you. You will pick up the headphones. The cups will still seal. You will feel nothing, which is the victory. Put your thumb on the earcup. That is not the sky and it is not a forest. That is a mill that learned to be a city, a physician who hated tugboat horns, a pianist who refused to play, a professor on a plane, a catalog that sold you the argument with the air, and a street that never had to lower its voice because you lowered yours first. You are allowed to love the quiet. You are allowed to take the cups off and hear the bus like a documentary. Just stop calling the silence natural, or inevitable, or proof that you are too sensitive for the century. Tonight, when the world dies in your ears, look at it like a refund for a city that overcharged you in sound. The refund is cheerful. The city is the point. Listen if you want. Know which machine you are still wearing. The seal is cheerful. Cheerful is how a refund stays on your head without looking like a mill.""",
]


def _stamp(index: int) -> str:
    """Return mmss for still number ``index`` (0-based, five-second cadence)."""
    seconds = index * 5
    return f"{seconds // 60:02d}{seconds % 60:02d}"


# (slug, covers, prompt) — 132 unique stills, one every five seconds of target runtime.
_ROWS: list[tuple[str, str, str]] = [
    ("headphones-on", "You put on over-ear headphones and the bus dies.", "Stickman putting huge over-ear headphones on a bus, MS Paint, white background."),
    ("people-hiss", "Not the engine. The people. The hiss of the door.", "Bus door hiss, stick passengers, sound X, MS Paint."),
    ("kids-video", "A kid's video with no headphones of its own.", "Child stickman phone blasting, annoyed neighbors, MS Paint."),
    ("plastic-cups", "You press a cup of plastic over each ear.", "Giant plastic ear cups sealing on a round head, MS Paint."),
    ("movie-muted", "The city becomes a movie with the sound turned down.", "City skyline with a MUTE slider, stickman watching, MS Paint."),
    ("default-room", "Silence used to be the default setting of a room.", "Empty quiet room, DEFAULT sticker, MS Paint."),
    ("no-cable", "It did not come with a charging cable.", "Silence with a red X on a charging cable, MS Paint."),
    ("three-hundred", "It did not cost three hundred dollars to make a train bearable.", "Headphones price 300, train, MS Paint."),
    ("luxury-head", "Why does quiet feel like a luxury good on your head?", "Headphones wearing a luxury crown, stickman, MS Paint."),
    ("factories-shout", "Factories learned to shout. Cities learned to never stop.", "Shouting factory, never-sleeping city, MS Paint."),
    ("professor-plane", "A professor on an airplane invented a machine that argues with air.", "Stick professor on a plane, headset vs air, MS Paint."),
    ("not-peace", "Your headphones are not peace. They are a refund.", "Headphones labeled REFUND not PEACE, MS Paint."),
    ("tap-cup", "You tap the earcup. The earcup is flattered.", "Finger tapping a smiling earcup, MS Paint."),
    ("older-quiet", "Start with the older quiet.", "Village path, no factories, stickman listening, MS Paint."),
    ("stole-room", "The headphone stole a room and sold it back as a feature.", "Headphones stealing a room, FEATURE tag, MS Paint."),
    ("storm-dog-bell", "Loud things had names: a storm, a dog, a bell, a market.", "Storm, dog, bell, market stall, four icons, MS Paint."),
    ("night-not-factory", "Night was mostly dark and mostly not a factory.", "Moon over a dark village, factory far and tiny, MS Paint."),
    ("village-quiet", "A village was quiet like a place that ran out of reasons to bang.", "Village with a resting hammer, MS Paint."),
    ("steam-whisper", "Steam arrived. Steam does not know how to whisper.", "Steam engine shouting, whisper X, MS Paint."),
    ("lancashire-mill", "A Lancashire mill of belts and iron ate conversations.", "Mill belts, iron, speech bubbles eaten, LANCASHIRE, MS Paint."),
    ("lip-read", "Workers learned to lip-read.", "Two mill workers reading lips, noisy gears, MS Paint."),
    ("ringing-home", "They went home with a ringing that belonged to no bird.", "Stickman in bed, ringing ears, bird with red X, MS Paint."),
    ("injury-commute", "The ringing was an injury that learned to commute.", "Ear injury riding a train, MS Paint."),
    ("open-office", "Your open office feels a bit much.", "Open office of talking stick people, overwhelmed one, MS Paint."),
    ("mill-no-button", "The mill floor had no noise-cancel button.", "Mill with a missing CANCEL button, MS Paint."),
    ("cotton-wage", "It offered cotton and a wage. Not your ears.", "Cotton bale and wage envelope, ears left behind, MS Paint."),
    ("progress-looms", "Progress counted looms. Not the leftover ring.", "Tally of looms, ignored ringing ear, MS Paint."),
    ("city-inside-out", "Cities turned the mill inside out and called it progress.", "City wearing a mill as a coat labeled PROGRESS, MS Paint."),
    ("rice-1906", "Nineteen hundred six, New York: Julia Barnett Rice.", "Stick physician RICE, New York skyline 1906, MS Paint."),
    ("tugboat-horns", "A low tolerance for tugboat horns.", "Tugboat blasting a horn, Rice covering ears, MS Paint."),
    ("society-noise", "Society for the Suppression of Unnecessary Noise.", "Banner SOCIETY UNNECESSARY NOISE, MS Paint."),
    ("joke-until", "The name is a joke until you live next to honking boats.", "Apartment next to honking boats, not laughing, MS Paint."),
    ("hospital-whistles", "Children's hospitals kept awake by steam whistles.", "Hospital kids awake, steam whistle, MS Paint."),
    ("quiet-zones", "She got quiet zones. She got ordinances.", "Map with QUIET ZONE, ordinance paper, MS Paint."),
    ("not-a-monk", "She was not a monk. She noticed dumped noise.", "Rice not a monk, noise dumped on small houses, MS Paint."),
    ("commerce-dump", "The powerful dump noise and call it commerce.", "Factory dumping sound on poor street, COMMERCE, MS Paint."),
    ("el-train", "The elevated train did not ask your bedroom for consent.", "El train outside a bedroom, no consent form, MS Paint."),
    ("whistle-rsvp", "The factory whistle did not RSVP.", "Whistle ignoring an RSVP card, MS Paint."),
    ("leaf-blower", "If your leaf blower feels like a neighbor's right.", "Leaf blower vs neighbor stickman, RIGHT?, MS Paint."),
    ("unnecessary-word", "Rice's word is unnecessary.", "Big word UNNECESSARY, Rice pointing, MS Paint."),
    ("product-page-won", "The product page won the century. The hat got a hospital zone.", "Product page trophy, tiny hospital quiet zone, MS Paint."),
    ("etiquette-volume", "Silence became etiquette. A class teaching its volume.", "Etiquette book shushing a loud kitchen, MS Paint."),
    ("library-deal", "A library decided thinking requires nobody to speak.", "Library stick figures silent, thinking bubbles, MS Paint."),
    ("velvet-rope", "A beautiful deal and a velvet rope.", "Library door with a velvet rope, MS Paint."),
    ("loud-kitchen", "A loud kitchen makes the library feel like a secret test.", "Loud kitchen vs library TEST, kid stickman, MS Paint."),
    ("open-plan-reverse", "Open-plan offices reversed the deal.", "Warehouse office of calls, no walls, MS Paint."),
    ("team-player", "If you hated it you were not a team player.", "TEAM PLAYER stamp on a headphone hater, MS Paint."),
    ("furniture-voted", "The team did not vote. The furniture did.", "Desks voting, people not voting, MS Paint."),
    ("short-cubicles", "Cubicle walls got shorter. Headphones got bigger.", "Short cubicle, huge headphones, MS Paint."),
    ("portable-carrel", "A headset is a portable library carrel the building refused.", "Headphones as a tiny carrel, refused building, MS Paint."),
    ("not-shush-police", "Not nostalgic for shushing librarians as police.", "Librarian whistle with red X, MS Paint."),
    ("the-swap", "We took shared quiet and sold it as foam.", "Shared quiet room becoming foam earcups, MS Paint."),
    ("wireless-chip", "Personality as foam and a wireless chip.", "Foam + chip labeled PERSONALITY, MS Paint."),
    ("rehook-empty", "Rehook: you think silence is empty like a blank page.", "Blank page vs headphones, stickman, MS Paint."),
    ("cage-1952", "Nineteen fifty two, Woodstock: John Cage, Maverick Hall.", "Concert hall MAVERICK, CAGE 1952, pianist, MS Paint."),
    ("four-33", "Four minutes thirty-three seconds of not playing.", "Piano, timer 4:33, pianist not touching keys, MS Paint."),
    ("prank-until", "A prank until you sit in it.", "Audience stickman hearing chairs and rain, MS Paint."),
    ("hear-chairs", "You hear chairs. You hear rain. You hear yourself.", "Chairs, rain, tiny self-radio, MS Paint."),
    ("anechoic", "Cage in an anechoic chamber that eats echoes.", "Box room eating echo waves, Cage sitting, MS Paint."),
    ("blood-nerves", "He still heard blood and nerves, high tone and low.", "Body as radio, high and low waves, MS Paint."),
    ("un-nature-cup", "Trying to un-nature the earcup.", "Nature sticker peeling off a headphone cup, MS Paint."),
    ("filter-logo", "The quiet you buy is a filter with a logo.", "Filter headphones with a brand scribble, MS Paint."),
    ("quietest-room", "A quietest-on-earth room in Minneapolis still plays your body.", "Tourist room MINNEAPOLIS, body radio, MS Paint."),
    ("cannot-fire-blood", "Headphones cannot fire your blood. They argue with the bus.", "Headphones vs bus, blood still beating, MS Paint."),
    ("argument-battery", "Argument is a product that needs a battery.", "Headphones plugged into a battery, ARGUMENT, MS Paint."),
    ("room-lost", "A battery is an admission that the room lost.", "Sad room vs winning battery, MS Paint."),
    ("bose-mit", "Amar Gopal Bose, MIT professor, hated airplane sound.", "Stick professor BOSE, MIT, airplane noise, MS Paint."),
    ("flight-1978", "Transatlantic flight, nineteen seventy eight, airline headphones fail.", "Airplane 1978, leaky airline headset, MS Paint."),
    ("roommate-engine", "The engine came through like a roommate who never leaves.", "Engine as a roommate on the plane, MS Paint."),
    ("sketch-opposite", "He sketched a headset that plays the opposite of noise.", "Sketch: noise wave vs opposite wave in an ear, MS Paint."),
    ("war-canal", "A little war in the ear canal.", "Tiny war inside an ear canal, MS Paint."),
    ("pilots-1989", "Nineteen eighty nine: active noise control for pilots.", "Pilot headset 1989, ANR, MS Paint."),
    ("consumer-silver", "Later, a silver consumer version. Commute as studio.", "Silver headphones, commute labeled STUDIO, MS Paint."),
    ("science-real", "The science is real. The marketing is a lullaby.", "Lab flask vs lullaby catalog, MS Paint."),
    ("anti-noise-trick", "Anti-noise is a physics trick. Peace is a catalog trick.", "Physics medal vs catalog PEACE, MS Paint."),
    ("self-care-patch", "Self-care is a patch so the city need not lower its voice.", "Bandage headphones on a shouting city, MS Paint."),
    ("patch-allowed", "The patch is allowed. The city is the plot.", "OK stamp on patch, city labeled PLOT, MS Paint."),
    ("quieter-street", "A quieter street does not need a sequel of earcups.", "Quiet street, sequels of headphones cancelled, MS Paint."),
    ("first-class-quiet", "First-class cabins sell quiet as a seat.", "First-class seat labeled QUIET, expensive, MS Paint."),
    ("quiet-car", "Quiet cars on trains: a chalk line through courtesy.", "Train car QUIET, chalk line, phone argument, MS Paint."),
    ("phone-theology", "They argue about phone calls like theology.", "Two stickmen arguing phones vs theology book, MS Paint."),
    ("hotel-soundproof", "Hotels sell soundproof like thread count.", "Hotel bed, SOUNDPROOF 400, MS Paint."),
    ("other-guests", "A number that means please do not hear the other guests.", "Thin wall, other guest living, please-X, MS Paint."),
    ("leaf-moto-night", "Leaf blowers, motorcycles, night construction, scooter speakers.", "Four noisy street icons, MS Paint."),
    ("street-speaker", "The street learned to be a loudspeaker.", "Street shaped like a speaker, MS Paint."),
    ("store-earmuffs", "The store sells earmuffs with a battery.", "Store shelf of battery earmuffs, MS Paint."),
    ("airport-foam", "Airports sell silence in a bottle of foam.", "Airport shop, foam earplugs bottle SILENCE, MS Paint."),
    ("school-note", "Schools send notes as if HVAC were weather.", "School note NOISE-SENSITIVE, HVAC cloud, MS Paint."),
    ("buy-filter", "You can buy a better filter. Not a quieter block.", "Shopping bag FILTER vs unsold quiet block, MS Paint."),
    ("politics-slow", "Politics is slower than two-day shipping.", "Turtle politics vs fast shipping box, MS Paint."),
    ("ears-zoning", "Your ears became the zoning board.", "Ear wearing a zoning-board badge, MS Paint."),
    ("this-is-you", "This is you. Two cups on your ears on a Tuesday.", "Stickman Tuesday headphones on a commute, MS Paint."),
    ("food-court-office", "An open office that sounds like a food court.", "Office desks plus food-court noise, MS Paint."),
    ("one-am-video", "One in the morning, volume down, cancel up.", "1 AM stickman, video, cancel ON, MS Paint."),
    ("building-alones", "Alone in a building full of other alones.", "Apartment windows, each with headphones, MS Paint."),
    ("not-fragile", "None of this makes you fragile. Born after the mill.", "Not-fragile sticker, mill and modern commute, MS Paint."),
    ("air-lost", "A professor decided the air should lose an argument.", "Air losing a debate to a headset, MS Paint."),
    ("toddler-relief", "Relief that the toddler speaker died.", "Toddler speaker X, relieved stickman, MS Paint."),
    ("shame-product", "A small shame that peace required a product.", "Tiny shame cloud over store headphones, MS Paint."),
    ("shame-unearned", "The shame is unearned. The product is not free.", "Shame in a trash, price tag still on cups, MS Paint."),
    ("catalog-talking", "If quiet feels like personality, the catalog is talking.", "Catalog speaking through headphones, MS Paint."),
    ("mill-costume", "Cheerful is how a mill stays without looking like a mill.", "Mill in a cheerful costume, MS Paint."),
    ("private-weather", "The roar feels like your private weather.", "Personal weather cloud of noise around one head, MS Paint."),
    ("trade-smoke", "We traded treating noise like smoke for a gadget.", "Smoke pollution vs noise, gadget instead of law, MS Paint."),
    ("gadget-helps", "The gadget helps a night-shift worker and a thin wall.", "Night worker and thin apartment, headphones helping, MS Paint."),
    ("ten-minutes", "A parent who needs ten minutes that are not a kitchen.", "Parent with timer 10 MIN, kitchen X, headphones, MS Paint."),
    ("miracle-receipt", "Help can be a miracle and still be a receipt.", "Miracle halo on a receipt, MS Paint."),
    ("luxury-myth", "A myth that quiet is a luxury personality.", "Luxury personality badge on earcups, MS Paint."),
    ("taste-cups", "Expensive earcups as taste.", "Wine-taste pose with headphones, MS Paint."),
    ("difficult-word", "Complain about leaf blowers and you are difficult.", "Leaf blower calling a neighbor DIFFICULT, MS Paint."),
    ("noisy-word", "Difficult is a word the noisy use.", "Noisy stickman holding the word DIFFICULT, MS Paint."),
    ("vibrancy-mill", "We kept the mill in the city and called it vibrancy.", "City mill labeled VIBRANCY, MS Paint."),
    ("laptop-airplane", "We kept the airplane in the living room and called it a laptop.", "Laptop with airplane wings in a living room, MS Paint."),
    ("roar-every-block", "Not a reason to carve the same roar into every block.", "Every city block carved with ROAR, MS Paint."),
    ("hospital-treaty", "A hospital quiet zone and a train quiet car are treaties.", "Hospital and quiet car shaking hands, TREATY, MS Paint."),
    ("foam-truce", "Foam is a truce you wear. Not a street with manners.", "Foam earplug truce vs polite street, MS Paint."),
    ("pick-up-cups", "You pick up the headphones. The cups will still seal.", "Callback: stickman lifting headphones, seal starting, MS Paint."),
    ("feel-nothing", "You will feel nothing, which is the victory.", "Blank calm face, sealed cups, MS Paint."),
    ("thumb-cup", "Put your thumb on the earcup.", "Giant thumb on an earcup, MS Paint."),
    ("not-forest", "Not the sky and not a forest.", "Headphones between red-X sky and red-X forest, MS Paint."),
    ("mill-city", "A mill that learned to be a city.", "Mill morphing into a skyline, MS Paint."),
    ("physician-horns", "A physician who hated tugboat horns.", "Rice vs tugboat horn, MS Paint."),
    ("pianist-refused", "A pianist who refused to play.", "Pianist hands in lap, 4:33, MS Paint."),
    ("professor-air", "A professor on a plane. A catalog selling the argument.", "Plane professor plus catalog ARGUE WITH AIR, MS Paint."),
    ("street-never", "A street that never lowered its voice because you lowered yours.", "Shouting street, quiet headphone person, MS Paint."),
    ("love-quiet", "You are allowed to love the quiet.", "Happy stickman in genuine quiet, MS Paint."),
    ("cups-off", "You are allowed to take the cups off and hear the bus.", "Headphones off, bus documentary, MS Paint."),
    ("not-natural", "Stop calling the silence natural.", "Headphones with NATURAL sticker and a red X, MS Paint."),
    ("too-sensitive", "Not proof you are too sensitive for the century.", "SENSITIVE stamp with red X, century calendar, MS Paint."),
    ("world-dies", "When the world dies in your ears, look at it like a refund.", "City dying inside earcups, REFUND, MS Paint."),
    ("city-is-point", "The refund is cheerful. The city is the point.", "Cheerful refund, city silhouette, MS Paint."),
    ("machine-wearing", "Know which machine you are still wearing.", "Stickman wearing a machine labeled which mill, MS Paint."),
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
        title="Why Quiet Got Expensive",
        description=(
            "Headphones feel like peace. They are a refund. Mills, Julia Rice, "
            "Cage's four minutes, Bose on a plane, a city that sold you the argument "
            "with the air. Quiet used to be a room."
        ),
        tags=(
            "silence",
            "headphones",
            "noise",
            "quiet",
            "history",
            "bose",
            "cage",
            "why",
            "commute",
            "luxury",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="BUY SILENCE?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Quiet Got Expensive",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 24, tzinfo=UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-silence.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print(out)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))
    print("accent", scenario.subtitles.accent_color, "stroke", scenario.subtitles.stroke_width)
    print("rate", scenario.tts.rate)


if __name__ == "__main__":
    main()

"""Author episode: you open a map and treat north as up."""



from __future__ import annotations



from datetime import UTC, datetime



from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT, paint_beat_count

from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat

from modules.scenario_builder import build_paint_scenario, write_scenario



TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS



PAINT = "MS Paint, white background, wobbly black outlines, round-head stickman, flat colors, 16:9. Keep all text and titles in the middle 75% of frame, not flush to top edge."



CHAPTERS = [

    """Tonight you will open a map and treat north as up, the way you treat a ceiling as above your head. Your thumb will spin the page and the labels will still expect the top edge to be north as if gravity had opinions about cartography. Here is the part that should bother you. The planet did not grow a ribbon that says this way is up. Your eyes did not evolve to read latitude as a ladder. A compass needle does not point at the word north on a legend. It points at magnetic north, a wandering pole the map politely hides behind a tidy arrow. So why does your screen wear north at the top as if north were physics? Because Chinese engineers learned to magnetize iron for navigation, because Islamic and European sailors copied the needle habit along trade routes, because Claudius Ptolemy drew a grid in the second century of the common era that later printers treated like a template, because Gerardus Mercator published a projection in fifteen sixty nine that made a rectangle feel like the world, and because mass printing and maritime empires exported one convenient orientation until a phone default felt like weather. That is the whole plot. Your north-up habit is not a mountain. It is a cartographic souvenir that learned to look like a law, and you obey it every commute as if the law had opinions about your thumb. The law does. The law is flattered. That is its job. The globe did not vote. A printer did, and then a convention that taught your screen the grid until the grid started calling itself sense. Sense is a word a compass rose invented so a leftover would still feel like truth when the parchment was gone.""",

    """Start with the needle, because the map stole a magnet and then sold it back as a frame. Long before Mercator, before atlases, before a satellite could laugh at your sense of up, humans already knew iron could point. Han dynasty China left early references to south-pointing spoons and lodestone. By the Song dynasty, navigators were using magnetized needles floating on water or hanging on silk. The needle does not read your moral compass. It aligns with Earth's magnetic field, which is tilted and drifting and rude about staying put. Geographic north, the top of the axis the planet spins around, and magnetic north, the place your pocket compass chases, are cousins who disagree. If your map still feels like it belongs to the pole star, notice that the star is a ceiling light and the map is a flat lie you agreed to enjoy. Flat is useful when you need a harbor, a tax boundary, and a school classroom to agree on where the river went without waiting for a globe to roll off the desk. The Earth keeps direction like a slow spin. The north-up grid keeps direction like a poster that forgot it was curved. You can love both and still admit only one of them is wearing your phone's default skin.""",

    """Named corners, because a myth of one culture is how an arrow gets a halo it did not earn. North at the top is not a single eureka moment you can pin on one hero with a plaque. It is a layer cake of ritual, astronomy, printing, and whichever edge of the paper was easiest to hold while the ink dried. Claudius Ptolemy compiled the Geography in the second century of the common era, a star manual for the ground that placed north toward the top of many reconstructions later scholars made from his coordinates. Medieval European mappa mundi often put east at the top because Jerusalem mattered more than a pole. Islamic cartographer Muhammad al-Idrisi finished the Tabula Rogeriana for Roger the Second of Sicily in eleven fifty four with south at the top, a perfectly sensible choice when your patron sits in the north of the sheet. Chinese maps sometimes placed south at the top because the emperor faced south toward his realm. If you still treat north-up as sacred direction, file the paperwork separately from the physics. North did not fall out of a mountain. It fell out of workshops that needed a repeatable edge, then exported the habit along routes and copied tables until the habit felt like gravity. Your screen is a convention wearing English and wearing a rotation lock.""",

    """Watch north leave the needle, because a flat rectangle needed a spine that did not require a globe in every pocket. Early portolan charts cared about coastlines and rhumb lines, not a moral top. Sailors wanted bearings that repeated. Printers wanted a sheet that stacked in a shop. Classroom walls wanted a rectangle that fit above a chalkboard. Putting north up is a layout decision the way putting a title at the top of a page is a layout decision. It is not evil. It is not universal. It is convenient once your fleet, your publisher, and your atlas customer all learned the same handshake. When Gerardus Mercator published his world projection in fifteen sixty nine, he was solving a practical problem for navigation: how to represent constant compass bearings as straight lines on a flat chart. The projection stretched the poles into a joke you still forgive because rectangles ship well. The punchline is not that one Flemish engraver invented your commute. The punchline is that a navigable rectangle and a printing press agreed on an edge, and the edge stayed because retraining millions of thumbs is expensive. Expensive is how a leftover stays in the century without looking like a leftover.""",

    """This is the rehook. You think north-up is a fact, the way gravity is a fact. North-up is a policy. In a modern app the policy is already on, because the alternative is trusting every user to rotate a map until their personal sense of up matches their chair, their car, and their teacher's chalkboard from nineteen ninety eight. Globes are honest. Flat defaults are scalable. Scalable is how an orientation escapes the scriptorium and becomes something a city can teach in numbers. I am not calling you clumsy for liking a fixed top. I am un-naturing the arrow. The arrow is a printer's margin wearing a compass rose. The rose said rotation can be law. Law is a feeling when your eyes find north without remembering when they learned it. If you have ever used a paper map on a windy trail and fought the crease because the trail went sideways on the page, congratulations. You have met the policy hiding inside the legend. The relief of a locked north is real. The relief is also a truce you never signed. A truce is not a planet that voted. A truce is a spreadsheet with margins.""",

    """Mass production did not invent direction. It inventoried it. When the same atlas plate had to repeat across editions, north-up became the part you could source, print, ship, and hang without translating a different sacred edge for every classroom wall. British Admiralty charts, Ordnance Survey sheets, school atlases in the twentieth century: the stack is boring on purpose. Boring is how a convention wins without a parade. Aviation maps and maritime charts kept rhumb-line logic while classrooms kept poster logic. Satellites later photographed the planet without asking permission from a compass rose, yet the jpeg still arrives north-up because the viewer software inherited the poster. A catalog is a quiet referendum. If your phone map has a locked top and your history book has a south-up Islamic world map, that gap is not evolution. It is inventory. Inventory is how the past wins a fight without filing a complaint. The past is cheerful. Cheerful is how a north arrow stays in the corner without looking like a printer holding a clipboard.""",

    """This is you, already, in the middle of the story. A Tuesday, a blue dot, a screen you rotate with your wrist and watch snap back to north-up as if the app were correcting your personality. You stare at the arrow because turning left would feel impossible without a fixed top, which is the most modern impossibility there is. None of this makes you geographical by nature. It makes you a person born after Mercator posters and after classroom walls became real estate and after a rectangle learned to host pinch-zoom, traffic, and a little triangle that re-centers you when you panic. You can feel both in the same glance: relief that you do not have to negotiate up with every stranger at a bus stop, and a tiny insult that a printer's margin outlasted the parchment. The relief is real. The insult is the south-up map failing for a second in your imagination. You paid for a shared world with an edge you never voted on. The edge is cheerful. Cheerful is how a default stays in the century without looking like a convention. The screen still has an arrow. The arrow still feels like a pole. A pole used to be a spin axis you never saw. Your axis is the rotation lock on a rectangle that forgot the globe. The lock is cheerful. Cheerful is how a cartographic habit stays on a phone without looking like a workshop.""",

    """A map is a pile of compromises with corners attached. That sentence is rude and almost fair. Take north-up away and the classroom becomes a workshop puzzle nobody wins, or a different sacred edge on every sheet until the compass rose breaks. Coastlines, tax lines, bearings, poster frames: the orientation is a diagram of how to agree without spinning the room, written by scribes and engravers you will not meet. You still open. The open is a vote for a margin that was sold as obvious. I am not telling you to hunt for an eleventh-century south-up atlas as a personality. I am telling you the personality was always the swap: a lodestone needle, a Ptolemaic grid, an Islamic south-up table, a medieval east-up pilgrimage map, a Mercator rectangle, an Admiralty plate, a classroom poster, a GPS view that re-locks your thumb. The crowd is still on the screen. The crowd is you and a rideshare fleet treating an arrow as a treaty. The treaty cannot see a globe. The globe can, if you pick it up, which is a sentence app defaults are not supposed to hide. A default is a promise in a settings menu you will never open. The menu is the real map edge. The edge is a costume. Costume is how a north arrow stays on a Tuesday without looking like a printer. The printer is still under the triangle. The triangle is still a permission slip you never signed. So what did we trade? We traded a sphere for a rectangle that survives pockets. We traded local sacred edges for a poster pulse atlases can love. We gained a shared top that lets a pilot, a teacher, and a navigation app agree on where left is without spinning the room. That is not nothing. A kid who knows north is up on the wall is living inside an administrative outcome, not a personality trait of the planet. The trick is pretending the arrow is nature. It is not. It is lodestone habit, a Ptolemaic reconstruction, a Mercator stretch, a plate on a press, a classroom nail, and a phone default you never changed. Deals can be rewritten. Some already were, quietly, when apps added rotate-with-heading and called it a feature as if features were not history with a toggle switch.""",

    """This is you. You will open the map again. North will still be at the top. You will feel nothing, which is the victory. Look at the arrow. That is not the spin axis and it is not a mountain. That is a magnetized needle, a Ptolemaic grid habit, an Islamic south-up table you rarely see, a Mercator rectangle, an Admiralty sheet, a classroom poster, and a GPS view that still owns your thumb so you will keep treating north as law. You are allowed to open. You are allowed to hate rotating and still navigate. Just stop calling north-up natural, or inevitable, or proof that you are modern. Tonight, when the little triangle snaps you back to top, look at it like a leftover salute to a printer's margin that left the shop. The salute is cheerful. The arrow is the point. Go when the grid lets you. Know which edge you are still obeying. The glance is cheerful. Cheerful is how a map stays on the screen without looking like a scribe you never met.""",

]





def _stamp(index: int) -> str:

    """Return mmss for still number ``index`` (0-based, five-second cadence)."""

    seconds = index * 5

    return f"{seconds // 60:02d}{seconds % 60:02d}"





_ROWS: list[tuple[str, str, str]] = [

    ("open-map", "Tonight you open a map and treat north as up.", f"Stickman opening phone map, NORTH UP obvious, {PAINT}"),

    ("ceiling-above", "The way you treat a ceiling as above your head.", f"Ceiling ABOVE HEAD arrow, map same habit, {PAINT}"),

    ("spin-labels", "You spin the page and labels still expect top is north.", f"Rotating map but NORTH stays top, {PAINT}"),

    ("gravity-cartography", "As if gravity had opinions about cartography.", f"Gravity cartoon giving cartography opinion, {PAINT}"),

    ("no-ribbon", "The planet did not grow a ribbon saying this way is up.", f"Earth with red X ribbon THIS WAY UP, {PAINT}"),

    ("eyes-no-ladder", "Your eyes did not evolve to read latitude as a ladder.", f"Eyes vs latitude ladder red X, {PAINT}"),

    ("needle-not-word", "A compass needle does not point at the word north on a legend.", f"Needle ignoring word NORTH on legend, {PAINT}"),

    ("magnetic-north", "It points at magnetic north, a wandering pole.", f"Needle pointing MAGNETIC NORTH wandering, {PAINT}"),

    ("why-north-top", "Why does your screen wear north at the top as if north were physics?", f"Screen with NORTH TOP PHYSICS costume, {PAINT}"),

    ("chinese-magnetize", "Chinese engineers learned to magnetize iron for navigation.", f"Ancient Chinese lodestone needle label, {PAINT}"),

    ("sailors-copied", "Islamic and European sailors copied the needle along trade routes.", f"Trade route copying compass needle, {PAINT}"),

    ("ptolemy-grid", "Claudius Ptolemy drew a grid in the second century.", f"Ptolemy grid GEOGRAPHY label, {PAINT}"),

    ("mercator-1569", "Gerardus Mercator published a projection in fifteen sixty nine.", f"Mercator 1569 rectangle world map generic, {PAINT}"),

    ("printing-export", "Mass printing exported one orientation until a phone default felt like weather.", f"Printing press exporting NORTH UP arrows, {PAINT}"),

    ("not-mountain", "Your north-up habit is not a mountain.", f"MOUNTAIN red X, north habit wins, {PAINT}"),

    ("cartographic-souvenir", "A cartographic souvenir that learned to look like a law.", f"Souvenir tag CARTOGRAPHY wearing LAW mask, {PAINT}"),

    ("law-flattered", "The law is flattered. That is its job.", f"Smiling compass rose FLATTERED badge, {PAINT}"),

    ("globe-no-vote", "The globe did not vote. A printer did.", f"Globe NO VOTE, printer raising hand, {PAINT}"),

    ("grid-sense", "The grid taught your screen until it called itself sense.", f"Screen word SENSE after grid arrows, {PAINT}"),

    ("start-needle", "Start with the needle.", f"Compass needle labeled START, {PAINT}"),

    ("map-stole-magnet", "The map stole a magnet and sold it back as a frame.", f"Magnet stolen by map FRAME, {PAINT}"),

    ("before-mercator", "Long before Mercator, before atlases, before satellites.", f"Timeline before Mercator atlases satellites, {PAINT}"),

    ("iron-could-point", "Humans already knew iron could point.", f"Iron bar pointing like compass, {PAINT}"),

    ("han-spoons", "Han dynasty China left references to south-pointing spoons.", f"South-pointing spoon HAN label, {PAINT}"),

    ("song-needles", "Song dynasty navigators used magnetized needles on water or silk.", f"Needle floating water silk SONG, {PAINT}"),

    ("magnetic-field", "The needle aligns with Earth's magnetic field.", f"Needle aligned to magnetic field lines, {PAINT}"),

    ("geo-vs-magnetic", "Geographic north and magnetic north are cousins who disagree.", f"Two cousins GEO NORTH vs MAG NORTH arguing, {PAINT}"),

    ("pole-star-ceiling", "The pole star is a ceiling light; the map is a flat lie.", f"Pole star as ceiling light, flat map lie, {PAINT}"),

    ("flat-useful", "Flat is useful when harbor, tax boundary, and classroom agree.", f"Harbor tax classroom agreeing on flat map, {PAINT}"),

    ("earth-spin", "The Earth keeps direction like a slow spin.", f"Earth spinning slow direction arrow, {PAINT}"),

    ("poster-curved", "North-up grid keeps direction like a poster that forgot it was curved.", f"Flat poster forgot CURVED red reminder, {PAINT}"),

    ("named-corners", "Named corners. One culture is a halo the arrow did not earn.", f"Halo on north arrow MYTH sticker, {PAINT}"),

    ("not-one-hero", "North at the top is not one eureka moment on a plaque.", f"Single hero plaque red X many layers, {PAINT}"),

    ("layer-cake", "A layer cake of ritual, astronomy, printing, and paper edges.", f"Layer cake ritual astronomy printing paper, {PAINT}"),

    ("ptolemy-geography", "Ptolemy compiled Geography in the second century.", f"Ptolemy GEOGRAPHY book north top many maps, {PAINT}"),

    ("medieval-east", "Medieval mappa mundi often put east at the top.", f"Mappa mundi EAST AT TOP Jerusalem, {PAINT}"),

    ("al-idrisi-south", "Al-Idrisi finished Tabula Rogeriana in eleven fifty four with south at the top.", f"Al-Idrisi map SOUTH AT TOP 1154, {PAINT}"),

    ("chinese-south-up", "Chinese maps sometimes placed south at the top.", f"Chinese map south top emperor faces south, {PAINT}"),

    ("not-sacred", "North-up is not sacred direction.", f"SACRED DIRECTION stamp red X, {PAINT}"),

    ("repeatable-edge", "Workshops needed a repeatable edge.", f"Workshop stamping repeatable edge on maps, {PAINT}"),

    ("convention-english", "Your screen is a convention wearing English and a rotation lock.", f"Screen wearing ENGLISH ROTATION LOCK, {PAINT}"),

    ("north-leaves-needle", "Watch north leave the needle.", f"Word NORTH walking away from needle, {PAINT}"),

    ("rectangle-spine", "A flat rectangle needed a spine without a globe in every pocket.", f"Rectangle spine no globe in pocket, {PAINT}"),

    ("portolan-coast", "Portolan charts cared about coastlines and rhumb lines.", f"Portolan chart coast rhumb lines, {PAINT}"),

    ("sailors-bearings", "Sailors wanted bearings that repeated.", f"Sailor happy repeating bearings, {PAINT}"),

    ("printers-stack", "Printers wanted a sheet that stacked in a shop.", f"Printer stacking identical map sheets, {PAINT}"),

    ("classroom-chalk", "Classroom walls wanted a rectangle above a chalkboard.", f"Map rectangle above chalkboard, {PAINT}"),

    ("layout-decision", "Putting north up is a layout decision.", f"LAYOUT DECISION stamp on north arrow, {PAINT}"),

    ("not-universal", "It is not universal.", f"UNIVERSAL stamp red X, {PAINT}"),

    ("same-handshake", "Fleet, publisher, and atlas customer learned the same handshake.", f"Three figures handshake NORTH UP, {PAINT}"),

    ("mercator-problem", "Mercator solved navigation: constant bearings as straight lines.", f"Mercator straight rhumb line on flat chart, {PAINT}"),

    ("poles-stretched", "The projection stretched the poles into a joke you forgive.", f"Stretched poles joke but rectangle ships, {PAINT}"),

    ("navigable-rectangle", "A navigable rectangle and a printing press agreed on an edge.", f"Rectangle and press agreeing on top edge, {PAINT}"),

    ("retrain-thumbs", "Retraining millions of thumbs is expensive.", f"Millions of thumbs dollar signs expensive, {PAINT}"),

    ("rehook-fact", "Rehook: you think north-up is a fact like gravity.", f"North-up vs gravity both labeled FACT, {PAINT}"),

    ("north-policy", "North-up is a policy.", f"North arrow stamped POLICY, {PAINT}"),

    ("personal-up", "Alternative: every user negotiates up with their chair and car.", f"Chaos everyone picks own UP red X, {PAINT}"),

    ("globes-honest", "Globes are honest.", f"Globe labeled HONEST, {PAINT}"),

    ("defaults-scalable", "Flat defaults are scalable.", f"Flat map defaults multiplying SCALABLE, {PAINT}"),

    ("city-teaches", "Scalable is how orientation escapes the scriptorium.", f"Scriptorium to city classroom arrows, {PAINT}"),

    ("un-nature-arrow", "Not calling you clumsy. Un-naturing the arrow.", f"NATURE sticker peeling off north arrow, {PAINT}"),

    ("printer-margin", "The arrow is a printer's margin wearing a compass rose.", f"Printer margin wearing compass rose costume, {PAINT}"),

    ("rotation-law", "The rose said rotation can be law.", f"Compass rose ROTATION LAW stamp, {PAINT}"),

    ("windy-trail", "Paper map on a windy trail, trail goes sideways on the page.", f"Hiker fighting creased sideways trail map, {PAINT}"),

    ("locked-north", "The relief of a locked north is real.", f"Relief sigh locked north arrow, {PAINT}"),

    ("spreadsheet-margins", "A truce is a spreadsheet with margins.", f"Spreadsheet with margin arrows truce, {PAINT}"),

    ("mass-inventoried", "Mass production inventoried direction.", f"INVENT DIRECTION red X INVENTORIED check, {PAINT}"),

    ("atlas-plate", "The same atlas plate had to repeat across editions.", f"Atlas plate repeating north-up editions, {PAINT}"),

    ("admiralty-ordnance", "Admiralty charts, Ordnance Survey, school atlases.", f"Stack Admiralty Ordnance school atlas generic, {PAINT}"),

    ("boring-on-purpose", "The stack is boring on purpose.", f"BORING ON PURPOSE stamp on chart stack, {PAINT}"),

    ("satellite-jpeg", "Satellites photographed the planet; the jpeg still arrives north-up.", f"Satellite photo jpeg forced NORTH UP, {PAINT}"),

    ("quiet-referendum", "A catalog is a quiet referendum.", f"Catalog voting booth QUIET REFERENDUM, {PAINT}"),

    ("phone-vs-history", "Phone map locked top, history book south-up Islamic map.", f"Phone north-up vs book south-up gap, {PAINT}"),

    ("inventory-fight", "That gap is inventory.", f"Inventory shelf beating alternate orientations, {PAINT}"),

    ("this-is-you", "This is you. A Tuesday. A blue dot.", f"Stickman Tuesday blue dot on map, {PAINT}"),

    ("snap-back", "You rotate the screen and it snaps back to north-up.", f"Phone rotating then snapping NORTH UP, {PAINT}"),

    ("turn-left", "Turning left feels impossible without a fixed top.", f"Driver needs fixed top to turn left, {PAINT}"),

    ("modern-impossibility", "The most modern impossibility there is.", f"MODERN IMPOSSIBILITY cloud over map, {PAINT}"),

    ("not-geographical", "None of this makes you geographical by nature.", f"GEOGRAPHICAL NATURE stamp red X, {PAINT}"),

    ("born-after-posters", "Born after Mercator posters and classroom walls.", f"Timeline Mercator poster classroom wall, {PAINT}"),

    ("pinch-zoom", "A rectangle learned pinch-zoom, traffic, re-center triangle.", f"Map with pinch zoom traffic triangle, {PAINT}"),

    ("relief-no-negotiate", "Relief you do not negotiate up with strangers.", f"Happy stickman no negotiate UP with strangers, {PAINT}"),

    ("insult-printer", "A tiny insult that a printer's margin outlasted parchment.", f"Printer margin beating parchment insult cloud, {PAINT}"),

    ("never-voted", "You paid for a shared world with an edge you never voted on.", f"Receipt map edge never voted, {PAINT}"),

    ("cheerful-edge", "Cheerful is how a default stays without looking like a convention.", f"Smiling north arrow disguise, {PAINT}"),

    ("compromises-corners", "A map is compromises with corners attached.", f"Compromise stack with map corners, {PAINT}"),

    ("take-north-away", "Take north-up away and the classroom becomes a puzzle.", f"Classroom puzzle no north-up, {PAINT}"),

    ("diagram-agree", "Orientation is how to agree without spinning the room.", f"Room not spinning everyone agrees on map, {PAINT}"),

    ("watch-vote", "The open is a vote for a margin sold as obvious.", f"Opening map voting OBVIOUS margin, {PAINT}"),

    ("swap-personality", "The swap: needle, Ptolemy, south-up table, east-up map, Mercator, poster, GPS.", f"Six icons needle Ptolemy south east Mercator GPS, {PAINT}"),

    ("crowd-screen", "The crowd is still on the screen.", f"Many stickmen on one phone map, {PAINT}"),

    ("arrow-treaty", "You and a rideshare fleet treating an arrow as a treaty.", f"Rideshare cars arrow treaty paper, {PAINT}"),

    ("treaty-blind", "The treaty cannot see a globe.", f"Treaty blindfold globe behind, {PAINT}"),

    ("settings-menu", "A default is a promise in a settings menu you never open.", f"Settings menu promise never opened, {PAINT}"),

    ("printer-under", "The printer is still under the triangle.", f"Printer ghost under GPS triangle, {PAINT}"),

    ("what-trade", "So what did we trade?", f"Trade scale sphere vs rectangle, {PAINT}"),

    ("sphere-rectangle", "We traded a sphere for a rectangle that survives pockets.", f"Globe shrinking into pocket rectangle, {PAINT}"),

    ("shared-top", "We gained a shared top pilots teachers and apps agree on.", f"Pilot teacher app agreeing on top arrow, {PAINT}"),

    ("kid-wall", "A kid who knows north is up lives inside an administrative outcome.", f"Kid pointing at wall north administrative outcome, {PAINT}"),

    ("arrow-not-nature", "The trick is pretending the arrow is nature.", f"NATURE stamp red X on arrow, {PAINT}"),

    ("lodestone-habit", "Lodestone habit, Ptolemaic grid, Mercator stretch, press plate, phone default.", f"Stack lodestone Ptolemy Mercator press phone, {PAINT}"),

    ("rotate-heading", "Apps added rotate-with-heading and called it a feature.", f"Feature toggle ROTATE WITH HEADING, {PAINT}"),

    ("rhumb-lines", "Rhumb lines wanted a flat chart that lied politely.", f"Rhumb lines on flat chart polite lie, {PAINT}"),

    ("magnetic-drift", "Magnetic north drifts; maps pretend the arrow is loyal.", f"Magnetic north drifting arrow pretending loyal, {PAINT}"),

    ("jerusalem-east", "East-at-top maps put pilgrimage above pole logic.", f"Jerusalem east top pilgrimage over pole, {PAINT}"),

    ("emperor-south", "South-at-top maps put the throne at the top of the page.", f"Emperor throne top south-up map, {PAINT}"),

    ("atlas-customer", "Atlas customers learned one edge and stopped asking.", f"Atlas customer stopped asking other edges, {PAINT}"),

    ("chart-room", "Chart rooms wanted bearings, not philosophy.", f"Chart room BEARINGS not PHILOSOPHY sign, {PAINT}"),

    ("poster-nail", "A classroom nail is a quiet referendum.", f"Map nailed to wall QUIET REFERENDUM, {PAINT}"),

    ("blue-dot-you", "The blue dot is you pretending the world has a handle.", f"Blue dot YOU handle on map, {PAINT}"),

    ("recenter-panic", "The re-center triangle saves you from your own rotation.", f"Re-center triangle saving panicked stickman, {PAINT}"),

    ("heading-mode", "Heading mode is history with a toggle switch.", f"Heading mode toggle HISTORY SWITCH, {PAINT}"),

    ("flat-lie-useful", "The flat lie is useful. Useful is how lies stay.", f"Flat map lie labeled USEFUL stays, {PAINT}"),

    ("margin-won", "The margin won because spheres do not fit in pockets.", f"Sphere too big for pocket margin wins, {PAINT}"),

    ("compass-rose-costume", "The compass rose is a costume for a printer's habit.", f"Compass rose printer costume, {PAINT}"),

    ("thumb-treaty", "Your thumb signed a treaty with a triangle.", f"Thumb signing treaty with map triangle, {PAINT}"),

    ("spin-axis-hidden", "The spin axis stays hidden behind a cheerful arrow.", f"Spin axis hidden behind smiling arrow, {PAINT}"),

    ("legend-handshake", "The legend is a handshake you learned in school.", f"Map legend SCHOOL HANDSHAKE label, {PAINT}"),

    ("plate-repeat", "A repeated plate teaches a city what up means.", f"Printing plate repeating UP lesson to city, {PAINT}"),

    ("open-again", "You will open the map again. North will still be at the top.", f"Callback opening map north top again, {PAINT}"),

    ("feel-nothing", "You will feel nothing, which is the victory.", f"Blank calm face victory at map, {PAINT}"),

    ("look-arrow", "Look at the arrow. Not the spin axis and not a mountain.", f"Arrow between red X spin axis and red X mountain, {PAINT}"),

    ("named-stack", "Needle, Ptolemy, south-up table, Mercator, Admiralty, poster, GPS.", f"Stack icons needle Ptolemy Mercator poster GPS, {PAINT}"),

    ("arrow-law", "GPS still owns your thumb so north stays law.", f"Thumb on phone north stamped LAW, {PAINT}"),

    ("allowed-open", "You are allowed to open and hate rotating and still navigate.", f"Open ok hate rotate still navigating, {PAINT}"),

    ("not-natural", "Stop calling north-up natural.", f"NATURAL stamp red X on north-up, {PAINT}"),

    ("not-inevitable", "Not inevitable. Not proof you are modern.", f"INEVITABLE MODERN stamps red X, {PAINT}"),

    ("leftover-margin", "A leftover salute to a printer's margin that left the shop.", f"Salute to printer margin leaving shop, {PAINT}"),

    ("arrow-point", "The salute is cheerful. The arrow is the point.", f"Cheerful salute on north arrow, {PAINT}"),

    ("know-edge", "Go when the grid lets you. Know which edge you are still obeying.", f"Stickman driving map edge labeled which, {PAINT}"),

    ("glance-cheerful", "Cheerful is how a map stays without looking like a scribe.", f"Smiling map scribe ghost hidden, {PAINT}"),

    ("final-callback", "Needle. Rectangle. Your thumb.", f"Final callback needle rectangle label your thumb, {PAINT}"),

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

        title="Why North Won the Map",

        description=(

            "North at the top feels obvious. Compasses point to magnetic north. "

            "Ptolemy, al-Idrisi, and Mercator shaped cartographic habits. "

            "Printing and phone defaults made one orientation feel like law."

        ),

        tags=(

            "maps",

            "north",

            "compass",

            "cartography",

            "mercator",

            "ptolemy",

            "history",

            "why",

            "navigation",

            "geography",

        ),

        scenes=tuple(

            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS

        ),

        visual_beats=tuple(

            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)

            for slug, covers, prompt in beats

        ),

        thumbnail_hook="NORTH UP?",

    )

    scenario = build_paint_scenario(

        draft,

        topic="Why North Won the Map",

        language="en",

        voice="en-US-GuyNeural",

        tts_rate="-8%",

        minutes=11,

        target_seconds=660.0,

        use_zenn=False,

        now=datetime.now(UTC),

    )

    out = PROJECT_ROOT / "senaryo-paint.json"

    named = PROJECT_ROOT / "senaryo-paint-north.json"

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



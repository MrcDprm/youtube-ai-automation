"""Author Drawn Anyway episode 29: Vasa, Stockholm, sixteen twenty eight."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 630.0
MINUTES = 9
VOICE = "en-AU-WilliamNeural"
RATE = "+4%"

CHAPTERS = [
    """Sweden's most expensive new warship sailed about thirteen hundred metres and then parked itself on the harbour floor. That is not a metaphor, and it is not a cartoon you invented after a trivia night about a king who bolted on an extra deck at the last minute. On the tenth of August sixteen twenty eight, Captain Söfring Hansson took Vasa out of Stockholm toward the naval station at Älvsnabben. A light southwest breeze. Four sails. Gunports open to fire a salute. She heeled, righted, then a stronger gust at Tegelviken put the lower ports under. Water on the lower gundeck. Thirty two metres down, about one hundred twenty metres from shore. Upper masts still stuck out of the water. Nearby boats pulled people off while hundreds watched from the shore, including foreign ambassadors. Wikipedia files about thirty people lost. File that once. Do not draw it. Keep that split: they already knew she rolled, and they sailed her anyway. Then put a red X on the joke that Gustavus Adolphus snuck a second deck onto a finished hull. The leftover is not a cartoon king. The leftover is a lurch test they stopped because they were afraid she would capsize at the quay.""",
    """Start with why a two-deck gun platform was supposed to be the truth. January sixteen twenty five: Henrik Hybertsson, called Master Henrik, and Arendt de Groote signed to build four ships. Keel in late February or early March sixteen twenty six at Skeppsgården, the navy yard in Stockholm. The king wanted heavier ships as gun platforms, not just boarding barges, because the war with Poland-Lithuania needed broadsides. On the fifth of August sixteen twenty six he ordered seventy two twenty-four-pounders, too many for one deck. That order came less than five months after the keel, early enough for two decks to be in the design. The French Galion du Guise, the model Arendt named, already had two. Laser surveys in two thousand seven to eleven found no mid-build stretch, no spliced extra length. Wikipedia: no evidence she was substantially modified after the keel. Hybertsson was already ill, handed the yard to Hein Jacobsson by summer sixteen twenty six, dead in spring sixteen twenty seven around launch. The king visited the yard in January sixteen twenty eight and was not in Stockholm for the maiden voyage. Jacobsson later said he widened her about one foot five inches, forty three centimetres, and could not go further because the hull was too far along. The official idea was: more guns, a high stern, and a letter from Poland that says sail now.""",
    """File the summer test, because thirty men running is not a vibe. Captain Söfring Hansson called Vice Admiral Klas Fleming to the ship at the royal palace quay. Thirty men ran back and forth across the upper deck. She rolled alarmingly. Fleming stopped them after three trips, afraid she would sink at the quay. Ship's master Göran Mattson later testified Fleming wished the king were home. Gustavus Adolphus was in Poland, sending impatient letters to get her to sea. Vasa Museum: sixty nine metres long, more than fifty from keel to mast truck, over twelve hundred tonnes, ten sails, sixty four cannons, one hundred twenty tonnes of ballast, hundreds of sculptures. Wikipedia files a beam of eleven point seven metres, a draft of four point eight, a displacement of about twelve hundred ten tonnes, forty eight of those guns as twenty-four-pounders, a broadside of about five hundred eighty eight pounds. Complement on paper: about one hundred forty five sailors and three hundred soldiers. Not all were aboard for the maiden trip. She carried too much weight high. Ballast could not fix it without a redesign. Upper gunports were even sized for smaller twelve-pounders, then they loaded twenty-four-pounders on both decks anyway, fifty six of them planned, eight of seventy two guns still undelivered when she sailed. Founder Medardus Gessus cast a lot of that bronze. A top-heavy stick with the windows open.""",
    """Here is the leftover the internet files as a last-minute extra floor. Tenth of August, warped along the eastern waterfront past the palace, then four sails east. First gust off Södermalm: sheets cast off, she slowly righted. Second gust at Tegelviken: lower ports under, water in, hold, gone in minutes. In sight of the yard that built her. Hundreds, maybe thousands, on the shore, including ambassadors. The Council wrote the king the next day. It took over two weeks to reach him. He answered: imprudence and negligence, punish the guilty. Inquest at the Royal Palace, fifth of September, Privy Council and Admiralty, Admiral of the Realm Carl Carlsson Gyllenhielm in the room. Crew swore the guns were secured and they were sober. Jacobsson: built as Henrik directed, as the king approved, and he had already asked to widen her more. Arendt when asked why she sank: only God knows. No one punished. Blame parked on a dead designer. Äpplet, the sister, got about a metre more beam, completed sixteen twenty nine, and actually worked. That is the leftover of a hull that was already a letter: the next one was wider.""",
    """The prescription took three hundred thirty three years. Within three days someone signed a contract to raise her. It failed. English engineer Ian Bulmer righted her and stuck her harder in the mud. Sixteen sixty three to sixty five, Albrecht von Treileben and Andreas Peckell took almost all the bronze guns with a diving bell, ripped deck planks, sold guns abroad. Nineteen twenty: the Olschanski brothers asked to blow wrecks for black-oak furniture. Authorities said no. Twenty fifth of August nineteen fifty six, Anders Franzén's coring probe brought up a waterlogged oak plug off Beckholmen. Divers Per Edvin Fälting and Sven Persson went down. Navy in. Tunnels under the hull, cables, Neptune pontoons. Twentieth of August nineteen fifty nine, first move in three hundred thirty one years, then eighteen underwater lifts toward Kastellholmen. Twenty fourth of April nineteen sixty one, in front of the world, the timbers broke the surface. PEG spray from sixty two to seventy nine. New museum, fifteenth of June nineteen ninety. Wikipedia: more than forty five million visitors by early twenty twenty five. About ninety eight percent of the original structure. Four thousand bolts swapped by twenty eighteen. The leftover of a thirteen hundred metre voyage is a building that still has to keep the humidity honest.""",
    """Rehook, because the internet likes a story that a king is a clown who bolted on a party deck. Put a red X on that sermon. A two-deck order in August sixteen twenty six is not a personality. Ignoring a quay that almost capsized is logistics, not a sitcom. Fleming had the political problem: the king was not home and the letters said sail. Hansson had the sailing problem: ports open for a salute on a ship that already failed a running test. Hybertsson had the dead problem: he could not answer a court. File all three. Do not invent a secret extra deck the lasers would have seen. Do not invent sabotage. Do not invent a last-minute personality who ruined a perfect one-deck ship. The leftover is uglier and smaller: a centre of gravity too high, a gust in a gap in the bluffs, open ports on purpose, and a meeting that blamed a man who had been dead a year.""",
    """File what the next hull actually did. Four more two-deck ships after Vasa: Äpplet, Kronan, Scepter, Göta Ark. Privy Council cancelled later orders after the king died at Lützen in sixteen thirty two. Kronan and Scepter served as flagships into the sixteen sixties. Äpplet, completed sixteen twenty nine, about a metre wider, found in December twenty twenty one off Vaxholm. Same idea, more belly. Vasa Museum: experts at the inquest already said too little belly, not enough hull for the upper works. They named the proportion in sixteen twenty eight. They built the proportion into the sister in sixteen twenty nine. That is not time travel. That is a yard that could add forty three centimetres once and a metre the next time. Conservation is still a hold temperature: PEG, a climate plant after the two thousand yellow spots on the oak, four thousand iron bolts swapped for stainless by twenty eighteen, eight tonnes lighter. A museum is a costume for a test they ran and then scheduled a salute.""",
    """None of this is a hymn to a perfect navy, and none of it is a cartoon of thirty running men as clowns. They had a war in the Baltic. They had ten ships lost in a storm off Riga in sixteen twenty five, which is why the four-ship contract existed. They had a king who understood guns and sent measurements from camp. You are allowed to laugh at a flagship that needed a museum more than a battle, and at a diving bell that harvested the bronze, and at a furniture permit that almost turned her into chairs. You are not required to laugh at thirty names on a harbour floor, or at divers cutting clay tunnels in the dark, or at a widow of a designer who became the file's leftover villain. The official idea was: sail her to Älvsnabben and join the fleet. The street idea was: they added a deck and God shrugged. The leftover idea is: thirty men had already shown the roll, the ports were open on purpose, and the next ship was simply wider.""",
    """So who won. Not the thirteen hundred metres. Not the extra-deck meme. Fleming won a stopped test and a sailing order. Hansson won an inquest and no sentence. Hybertsson won the blame by being dead. Äpplet won a metre. Franzén won a core of oak. Fälting won a dive. The furniture brothers won a no. Treileben won bronze. Stockholm won a museum that outdrew the voyage. If you need a moral, skip kings are dumb. Take this: a last-minute deck is a terrible whole story, and a three-trip lurch test is a terrible honest one. The next time someone tells you Vasa sank because a king bolted on extra guns at the dock, ask when the seventy two twenty-four-pounders were ordered, and whether thirty men had already run across that deck. Would you have waited for the king, or sailed with the ports shut. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no drowning, no cruelty, not mud-green archive night, "
    "not After Hours File dark. Vasa shown as a candy warship, a harbour stick, a running-test, "
    "open gunports, a museum hall, not photoreal royal portraits, not a battle gore board. "
    "Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, oversized black marker, "
    "mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("1300-metres", "Sweden's new warship sailed about 1,300 metres, then sat on the harbour floor.", f"A candy warship 1300 M from a dock, then a harbour-floor tag. Cream paper. {STYLE}"),
    ("not-trivia", "Not a last-minute extra-deck trivia gag.", f"Ink shaking his head at an EXTRA DECK stamp with a red X, mouth closed. {STYLE}"),
    ("aug-10", "10 August 1628, Captain Söfring Hansson, toward Älvsnabben.", f"A date 10 AUG 1628, nameplate HANSSON. No portrait. {STYLE}"),
    ("four-sails", "Light southwest breeze. Four sails. Gunports open for a salute.", f"Four candy sails, open ports, tag SALUTE. {STYLE}"),
    ("tegelviken", "A gust at Tegelviken put the lower ports under.", f"A gust arrow TEGELVIKEN, water at lower ports. Not drowning. {STYLE}"),
    ("32-metres", "32 metres down, about 120 metres from shore.", f"A depth ruler 32 M, shore 120 M. {STYLE}"),
    ("x-extra-deck", "Put a red X on the joke that the king bolted on a second deck at the last minute.", f"A LAST-MINUTE DECK stamp with a giant red X. {STYLE}"),
    ("lurch-leftover", "Leftover: a lurch test they stopped because she might capsize at the quay.", f"Thirty tiny candy figures mid-run, STOP stamp. {STYLE}"),
    ("contract-1625", "January 1625: Hybertsson and de Groote, four ships.", f"A contract 1625, two nameplates. {STYLE}"),
    ("keel-1626", "Keel late winter 1626, Skeppsgården, Stockholm.", f"A keel tag 1626, yard SKEPPSGARDEN. {STYLE}"),
    ("72-guns", "5 August 1626: king ordered 72 twenty-four-pounders, too many for one deck.", f"A gun-order card 72 x 24 LB, date 5 AUG 1626. {STYLE}"),
    ("early-enough", "That order came under five months after the keel. Two decks could be in the design.", f"A calendar UNDER 5 MONTHS, TWO DECKS IN DESIGN. {STYLE}"),
    ("no-splice", "Laser surveys 2007-11: no mid-build stretch, no spliced extra length.", f"A laser ruler NO SPLICE. {STYLE}"),
    ("henrik-dies", "Hybertsson ill, Jacobsson by summer 1626, dead spring 1627 around launch.", f"A handoff tag HENRIK to HEIN, date 1627. {STYLE}"),
    ("43-cm", "Jacobsson widened her about 1 ft 5 in, 43 cm. Could not go further.", f"A width arrow +43 CM, STOP. {STYLE}"),
    ("official-sail", "Official idea: more guns, a high stern, letters that say sail now.", f"A letter SAIL NOW, a high candy stern. {STYLE}"),
    ("thirty-run", "Thirty men ran across the upper deck. She rolled alarmingly.", f"A deck with running arrows, ROLL tag. {STYLE}"),
    ("three-trips", "Fleming stopped them after three trips, afraid she would sink at the quay.", f"A stop-hand 3 TRIPS, tag QUAY. {STYLE}"),
    ("wished-king", "Mattson: Fleming wished the king were home. King was in Poland, writing sail.", f"A letter from POLAND, empty chair KING. No portrait. {STYLE}"),
    ("museum-spec", "69 m long, 50 m+ tall, 1,200+ tonnes, 64 cannons, 120 tonnes ballast.", f"A spec card 69 M / 64 GUNS / 120 T BALLAST. {STYLE}"),
    ("top-heavy", "Too much weight high. More ballast could not fix it without a redesign.", f"A top-heavy candy ship, ballast too low. {STYLE}"),
    ("ports-12", "Upper ports sized for 12-pounders, then 24-pounders on both decks.", f"Two port sizes 12 vs 24. {STYLE}"),
    ("eight-missing", "Eight of 72 guns still undelivered when she sailed.", f"An empty carriage 8 MISSING. {STYLE}"),
    ("righted-once", "First gust: sheets off, she slowly righted.", f"A heel then a RIGHTING arrow. {STYLE}"),
    ("second-gust", "Second gust: lower ports under, water in, hold, gone.", f"Ports under a wave line, tag GONE. Not drowning people. {STYLE}"),
    ("in-sight", "In sight of the yard that built her. Hundreds on the shore.", f"A yard still visible, a crowd of tiny silhouettes. {STYLE}"),
    ("king-letter", "Council wrote next day. Two weeks to Poland. King: punish the guilty.", f"A delayed letter PUNISH. {STYLE}"),
    ("sept-5", "Inquest 5 September 1628, Royal Palace. Gyllenhielm in the room.", f"A folder INQUEST 5 SEP, nameplate GYLLENHIELM. {STYLE}"),
    ("sober-guns", "Crew: guns secured, crew sober. Nobody took the blame.", f"Two stamps SOBER and GUNS FAST. {STYLE}"),
    ("god-knows", "Arendt: Only God knows. No one punished. Blame on a dead designer.", f"A quote ONLY GOD KNOWS, a closed file. {STYLE}"),
    ("applet-metre", "Sister Äpplet: about a metre more beam, completed 1629, actually worked.", f"Two hulls VASA vs APPLET +1 M. {STYLE}"),
    ("found-2021", "Äpplet's wreck found December 2021.", f"A find tag APPLET 2021. {STYLE}"),
    ("three-days", "Within three days a contract to raise her. It failed.", f"A raise-contract, stamp FAILED. {STYLE}"),
    ("bulmer-mud", "Ian Bulmer righted her and stuck her harder in the mud.", f"A ship more stuck, tag BULMER. {STYLE}"),
    ("diving-bell", "1663-65: Treileben and Peckell, diving bell, almost all the bronze guns.", f"A diving bell, bronze guns up. {STYLE}"),
    ("x-clowns", "Rehook: red X on the clown-king extra-deck sermon.", f"Ink peeling an EXTRA DECK KING sticker, mouth closed. {STYLE}"),
    ("no-furniture", "1920: brothers asked to blast wrecks for furniture. Authorities said no.", f"A furniture chair with a red X, date 1920. {STYLE}"),
    ("franzen-1956", "25 August 1956: Franzén's corer, oak off Beckholmen.", f"A core of oak, date 25 AUG 1956. {STYLE}"),
    ("24-apr-61", "24 April 1961: timbers broke the surface. 333 years.", f"A calendar 24 APR 1961, tag 333 YEARS. {STYLE}"),
    ("peg-spray", "PEG spray 1962 to 1979. New museum 15 June 1990.", f"Spray nozzles PEG, museum tag 1990. {STYLE}"),
    ("45-million", "More than 45 million visitors by early 2025. About 98% original.", f"A tally 45M VISITORS, 98 PERCENT. {STYLE}"),
    ("too-little-belly", "Inquest experts: too little belly, not enough hull for the upper works.", f"A hull cross-section LITTLE BELLY. {STYLE}"),
    ("four-after", "After Vasa: Äpplet, Kronan, Scepter, Göta Ark. Two served as flagships.", f"Four ship tags, two stamped FLAGSHIP. {STYLE}"),
    ("bolts-2018", "By 2018: 4,000 bolts swapped, eight tonnes lighter.", f"A bolt tally 4000, minus 8 T. {STYLE}"),
    ("humidity", "A museum still has to keep the humidity honest.", f"A humidity gauge HONEST. {STYLE}"),
    ("who-won-test", "Not the 1,300 metres. The three-trip test won a warning they filed as sail anyway.", f"A warning bell vs a SAIL stamp. {STYLE}"),
    ("wider-won", "Äpplet won a metre. Franzén won a core of oak.", f"A metre trophy and an oak core trophy. {STYLE}"),
    ("furniture-no", "The furniture brothers won a no. Stockholm won a museum.", f"A no-permit vs a museum ticket. {STYLE}"),
    ("ask-the-order", "Ask when the 72 twenty-four-pounders were ordered.", f"A question mark over 5 AUG 1626. {STYLE}"),
    ("ask-the-run", "Ask whether thirty men had already run.", f"A question mark over 30 runners. {STYLE}"),
    ("wait-or-ports", "Would you have waited for the king, or sailed with the ports shut.", f"Split: a wait chair vs shut ports, a question mark. {STYLE}"),
    ("lurch-honest", "A last-minute deck is a terrible whole story. A three-trip lurch is a terrible honest one.", f"A fake extra deck vs a running test. {STYLE}"),
    ("centre-g", "The leftover: a centre of gravity and a gust in a gap.", f"A CG dot and a gust in a cliff gap. {STYLE}"),
    ("receipt", "Thirty men had already shown the roll. Drawn anyway.", f"A receipt card TEST vs SALUTE, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Warship That Sank in Harbor",
        description=(
            "Sixteen twenty eight. Thirteen hundred metres, a three-trip lurch test, "
            "and a salute fired through ports they should have shut."
        ),
        tags=(
            "history",
            "1628",
            "vasa",
            "sweden",
            "ship",
            "cartoon",
            "true story",
            "logistics",
            "museum",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="1300 METRES",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Warship That Sank in Harbor",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-vasa.json"
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

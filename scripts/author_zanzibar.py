"""Author Drawn Anyway episode 9: Anglo-Zanzibar War, eighteen ninety six."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 600.0
MINUTES = 9
VOICE = "en-GB-ThomasNeural"
RATE = "+2%"

CHAPTERS = [
    """A war once ended before a kettle would have boiled. That is not a metaphor, and it is not a cartoon you invented after a trivia night. On Thursday the twenty seventh of August eighteen ninety six, in Zanzibar Town, on Unguja in the Indian Ocean, British ships opened fire at nine oh two in the morning, local mean time. The shooting is usually said to have stopped around nine forty. That is thirty eight minutes if you start the clock at nine oh two and stop it when the palace guns go quiet. Some logs say nine thirty five. Some say nine forty five. Guinness later filed it as the shortest war on record. Keep that picture. A wooden palace on a waterfront. An ultimatum with a breakfast deadline. A royal yacht that was a copy of a British frigate. Everything after this is just that picture hiring a stopwatch. This is not a victory lap.""",
    """Start with why a palace thought a morning would be enough. Two days earlier, at eleven forty in the morning East Africa time on the twenty fifth, Sultan Hamad bin Thuwaini died suddenly. He had been the pro-British sultan since eighteen ninety three. His twenty nine year old nephew Khalid bin Barghash moved into the palace complex without waiting for the British consul. A rumor said poison. Treat that as a rumor some people liked, not a verdict. The paper that actually mattered was older. On the fourteenth of June eighteen ninety, Zanzibar had become a British protectorate. A candidate for the throne was supposed to get the consul's permission. Khalid did not. London preferred Hamoud bin Mohammed, who would sit quieter. Consul Basil Cave and First Minister Lloyd Mathews, a former Royal Navy lieutenant already running the sultan's cabinet, told Khalid to think carefully. He had already been talked down from a similar grab three years earlier by Rennell Rodd. This time he stayed.""",
    """By nightfall on the twenty fifth, Palace Square held about two thousand eight hundred men under Captain Saleh of the bodyguard. Most were civilians. About seven hundred askaris came over to Khalid. The artillery facing the harbour was a mixed souvenir drawer: Maxim guns, a Gatling, a seventeenth-century bronze cannon, and two twelve-pounders that had been a gift from Kaiser Wilhelm the Second. The navy was one wooden sloop, His Highness's Ship Glasgow, a royal yacht built in eighteen seventy eight to look like the British frigate Glasgow, which had once impressed a previous sultan and then failed to impress this one, so she mostly sat at anchor. Mathews and Cave landed one hundred fifty sailors and marines from Philomel and Thrush, plus nine hundred Zanzibari askaris under Lieutenant Arthur Raikes at the customs house. Cave telegraphed Lord Salisbury: if peaceful attempts fail, may we fire on the palace from the men-of-war. The other consuls were told not to recognise Khalid. The American consul, Richard Dorsey Mohun, would not even answer a letter about the accession.""",
    """The twenty sixth is logistics, not glory. Cruiser Racoon arrived at ten. Flagship Saint George steamed in at two with Rear-Admiral Harry Rawson. Salisbury's reply authorised whatever measures they could actually finish. Do not start what you cannot complete. That sentence is the whole imperial method in one cable. Rawson sent the ultimatum: haul down the banner and leave the palace by nine in the morning on the twenty seventh, or the ships would open fire. Merchant boats were cleared. Consul Mohun wrote that the night was appallingly silent, no drums, no babies, which is a line you can keep without turning it into a horror reel. At eight on the twenty seventh Khalid asked to parley. Cave said only the ultimatum terms. At eight thirty a messenger said they had no intention of hauling anything down and did not believe the British would fire. Cave said they did not want to, and would. At eight fifty five Rawson signalled prepare for action.""",
    """Nine o'clock. Mathews ordered the bombardment. At nine oh two, Racoon, Thrush, and Sparrow fired together. Thrush's first shot knocked over a twelve-pounder. The palace, the attached harem Beit al-Hukm, and the ceremonial House of Wonders sat in a timber line on the sea front, linked by covered bridges. It was not a fortress. It was a government that had been built to look at the water. About three thousand people were inside, including servants. High explosive into wood is not a fair contest, and it is not a joke. Roughly five hundred Zanzibari men and women were killed or wounded, many in the fire. It is not known how many were fighters. One British petty officer on Thrush was badly hurt and later recovered. At nine oh five the obsolete Glasgow fired her nine-pounders and a Gatling that had been a present from Queen Victoria at Saint George. Return fire holed her. The crew were taken off in launches. She settled in the shallow harbour with masts still up. Shelling is usually said to have ceased around nine forty, after about five hundred shells, four thousand one hundred machine-gun rounds, and a thousand rifle rounds.""",
    """Here is the leftover fact, and it is not who was braver. The duration is a filing dispute. Start at the order at nine, or at the first gun at nine oh two. Stop at nine thirty five, when Saint George's log has a cease-fire, or nine forty on Thrush, nine forty one on Racoon, nine forty five on Philomel and Sparrow. Thirty eight minutes is the number that won the trivia card. Forty and forty five are in the same morning. A war that short is still a war if you were in the wooden building. It is also a timetable enforced by ships that had already been parked for the purpose. Khalid reached the German consulate. Consul Albrecht von Rechenberg would not hand him over. On the second of October, SMS Seeadler put a boat to the garden gate at high tide so Khalid never stepped onto Zanzibar soil as a prisoner. He went to Dar es Salaam. The British later caught him in nineteen sixteen and sent him to the Seychelles and Saint Helena. He died in Mombasa in nineteen twenty seven.""",
    """Rehook, because the internet likes a cute record. Shortest war is a caption. The invoice is different. Supporters of Khalid were billed about three hundred thousand rupees for the shells and the looting. Hamoud was installed that afternoon with the powers of a letterhead. Months later, with British prompting, he abolished slavery in all its forms. Emancipation still meant showing up at an office. In ten years only about seventeen thousand of an estimated sixty thousand enslaved people in eighteen ninety one had been processed. The House of Wonders, almost unhurt, became a secretariat. In eighteen ninety seven they added a clocktower where a lighthouse had been. Glasgow's masts stuck out of the harbour until she was broken up in nineteen twelve. A clock on a palace and a wreck you could still see from shore. That is the souvenir, not a medal.""",
    """None of this is a hymn to gunboats, and none of it is a cartoon of Khalid as a fool who should have known better than to own a wooden house. The treaty of eighteen ninety already said who approved sultans. The ultimatum printed a time. The palace was timber. The yacht was a prestige copy that had sat at anchor for years. When the hour came, the hour did the work. You can call that the shortest war. You can also call it a deadline with artillery attached. The chemistry is high explosive plus wood plus a harbour. The logistics is who owns the morning. Cave asked London for permission. Salisbury said yes, if you can finish it. They finished it before a long meeting would have found its chairs.""",
    """So who won. Not the bronze cannon. Not the yacht named after someone else's frigate. Not the trivia card, though the trivia card will outlive the customs shed fire. Rawson won a knighthood and later a governorship in New South Wales. Cave won a Companion of the Bath. Mathews kept the keys. Hamoud won a throne that was already a desk. Khalid won a boat ride from a garden. If you need a moral, skip empire is efficient. Take this: a stopwatch is a terrible instrument for a succession treaty, and a succession treaty is a terrible instrument for a wooden palace. The next time someone tells you the shortest war, ask which logbook, nine oh two or nine, nine forty or nine forty five. Would you have waited for nine. A breakfast ultimatum, five ships, thirty eight disputed minutes. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no cheering empire, no child victims. Recurring mascot Ink may cameo: "
    "mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("kettle-clock", "A war ended before a kettle would have boiled.", f"Cartoon title beat: a huge kettle next to a harbour clock, tiny wooden palace, cream paper. No flags. {STYLE}"),
    ("not-trivia", "Not a metaphor. Not a trivia-night cartoon.", f"Ink shaking his head at a TRIVIA stamp with a red X, mouth closed. {STYLE}"),
    ("august-twenty-seven", "August 27, 1896, Zanzibar Town, Unguja.", f"Calendar August 27 1896, an island in a simple ocean, no flags. {STYLE}"),
    ("nine-oh-two", "Ships opened fire at 9:02 local mean time.", f"A harbour clock 9:02, three toy gunboats, no explosion gore. {STYLE}"),
    ("nine-forty", "Shooting usually stopped around 9:40. About 38 minutes.", f"A stopwatch 38 MIN between 9:02 and 9:40. {STYLE}"),
    ("logbooks-disagree", "Some logs say 9:35. Some say 9:45.", f"Three ship logbooks with three slightly different end times. {STYLE}"),
    ("guinness-card", "Guinness later filed the shortest war on record.", f"A trivia card SHORTEST WAR, a wooden palace shrinking behind it. {STYLE}"),
    ("not-a-lap", "A wooden palace, a breakfast deadline. Not a victory lap.", f"A NO LAP stamp over a medal. Ink nodding, mouth closed. {STYLE}"),
    ("hamad-dies", "August 25, 11:40: Sultan Hamad bin Thuwaini died suddenly.", f"A clock 11:40, a vacant sultan's chair, respectful not gory. {STYLE}"),
    ("khalid-moves-in", "Nephew Khalid bin Barghash moved in without the consul.", f"A palace door, a 29 label, a CONSUL permission slip unused. {STYLE}"),
    ("poison-rumor", "A rumor said poison. Treat it as a rumor.", f"A bottle stamped RUMOR not VERDICT. {STYLE}"),
    ("june-1890", "June 14, 1890: protectorate. Consul must approve the sultan.", f"A treaty paper 14 JUN 1890, CONSUL checkbox empty. {STYLE}"),
    ("prefer-hamoud", "London preferred Hamoud bin Mohammed.", f"Two nameplates, a finger ticking HAMOUD. No portraits. {STYLE}"),
    ("cave-mathews", "Basil Cave and Lloyd Mathews told Khalid to think carefully.", f"Two hats CONSUL and FIRST MINISTER, a THINK stamp. {STYLE}"),
    ("rodd-three-years", "Rennell Rodd had talked him down three years earlier.", f"A calendar skipping 1893 to 1896, SAME GRAB tag. {STYLE}"),
    ("palace-square", "By nightfall: about 2,800 in Palace Square.", f"A square of simple hats, 2800, night lanterns, not a battle mural. {STYLE}"),
    ("souvenir-guns", "Maxims, a Gatling, a 17th-century bronze, Kaiser's 12-pounders.", f"A mixed drawer of toy guns labeled GIFTS, no gore. {STYLE}"),
    ("glasgow-yacht", "The navy: wooden yacht Glasgow, a copy of a British frigate.", f"A fancy yacht at anchor looking like a copy, mostly idle. {STYLE}"),
    ("raikes-customs", "Raikes' askaris at the customs house. 150 sailors landed.", f"A customs shed and a small landing party, no flags as joke. {STYLE}"),
    ("salisbury-cable", "Cave to Salisbury: may we fire if peace fails.", f"A telegraph tape MAY WE FIRE, waiting. {STYLE}"),
    ("mohun-no-reply", "US consul Mohun would not even reply about the accession.", f"A sealed letter RETURN TO SENDER, US CONSUL desk. {STYLE}"),
    ("racoon-st-george", "26th: Racoon at 10:00. St George at 14:00 with Rawson.", f"Two toy cruisers arriving, clocks 10:00 and 2:00. {STYLE}"),
    ("finish-it", "Salisbury: do not start what you cannot complete.", f"A cable FINISH IT, not a glory poster. {STYLE}"),
    ("nine-am-ultimatum", "Ultimatum: leave by 9:00 on the 27th, or the ships fire.", f"An ultimatum paper with a 9:00 breakfast clock. {STYLE}"),
    ("silent-night", "Mohun: the night was appallingly silent. No drums.", f"A quiet town, a silent drum, moon, not horror. {STYLE}"),
    ("eight-o-clock", "8:00: Khalid asked to parley. Cave said only the terms.", f"A messenger and a closed TERMS folder. {STYLE}"),
    ("eight-thirty", "8:30: we will not haul down. We do not believe you will fire.", f"Two speech bubbles: WON'T / WILL. No flags. {STYLE}"),
    ("eight-fifty-five", "8:55: Rawson signalled prepare for action.", f"A signal hoist PREPARE, clock 8:55. {STYLE}"),
    ("mathews-orders", "9:00: Mathews ordered the bombardment.", f"A clock hitting 9:00, an ORDER stamp. {STYLE}"),
    ("three-ships", "9:02: Racoon, Thrush, Sparrow fired together.", f"Three named toy ships, simultaneous puffs, no gore. {STYLE}"),
    ("first-shot", "Thrush's first shot knocked over a 12-pounder.", f"A toy cannon tipping, FIRST SHOT, not bloody. {STYLE}"),
    ("timber-line", "Palace, harem, House of Wonders: a timber line on the water.", f"Three wooden buildings in a row, HOUSE OF WONDERS label, bridges. {STYLE}"),
    ("not-a-fortress", "It was not a fortress. It was built to look at the water.", f"A palace labeled VIEW not FORT. {STYLE}"),
    ("five-hundred", "About 500 killed or wounded. One British sailor hurt.", f"A somber tally 500 and 1, respectful clipboard, no corpses. {STYLE}"),
    ("glasgow-fires", "9:05: yacht Glasgow fired nine-pounders at St George.", f"A small yacht puffing at a big cruiser, 9:05. {STYLE}"),
    ("masts-up", "She settled in shallow water, masts still up.", f"Harbour water, three masts sticking up, not a graveyard. {STYLE}"),
    ("ammo-count", "About 500 shells, 4,100 machine-gun rounds, 1,000 rifle.", f"Three ammo boxes with those numbers. {STYLE}"),
    ("filing-dispute", "The leftover fact is a filing dispute, not bravery.", f"A FILE stamp over a medal with a red X. {STYLE}"),
    ("which-start", "Start at 9:00 order, or 9:02 first gun.", f"Two clocks 9:00 vs 9:02, START? {STYLE}"),
    ("which-stop", "Stop at 9:35, 9:40, 9:41, or 9:45 depending on the log.", f"Four log corners, four end times. {STYLE}"),
    ("german-gate", "Khalid to the German consulate. Rechenberg would not hand him over.", f"A consulate garden gate, POLITICAL PRISONER tag. No flags as joke. {STYLE}"),
    ("seeadler", "October 2: SMS Seeadler boat to the garden at high tide.", f"A boat at a garden gate, high-tide mark, 2 OCT. {STYLE}"),
    ("mombasa-1927", "Caught in 1916, exile, died Mombasa 1927.", f"A long timeline 1896 to 1927, MOMBASA at the end. {STYLE}"),
    ("rupee-bill", "Supporters billed about 300,000 rupees for the shells.", f"An invoice 300000 RUPEES, SHELLS as a line item. {STYLE}"),
    ("hamoud-afternoon", "Hamoud installed that afternoon, powers of a letterhead.", f"A throne that is actually a desk, LETTERHEAD. {STYLE}"),
    ("slow-office", "Abolition still meant an office visit. 17,293 in ten years.", f"An office window queue, 17293 / 60000. Respectful. {STYLE}"),
    ("clocktower", "1897: a clocktower on the House of Wonders, replacing a lighthouse.", f"A palace getting a CLOCK instead of a lighthouse. {STYLE}"),
    ("masts-1912", "Glasgow's masts visible until scrap in 1912.", f"Harbour masts, calendar 1912 SCRAP. {STYLE}"),
    ("not-a-hymn", "Not a hymn to gunboats. Not a cartoon of a fool.", f"Ink crossing out a HYMN sheet, mouth closed. {STYLE}"),
    ("who-owns-morning", "The logistics is who owns the morning.", f"A sunrise stamped PROPERTY OF THE DEADLINE. {STYLE}"),
    ("chairs-unfound", "They finished before a long meeting would have found its chairs.", f"Empty meeting chairs vs a 38 MIN stamp. {STYLE}"),
    ("trivia-outlives", "The trivia card will outlive the customs-shed fire.", f"A trivia card larger than a tiny fire brigade, not gory. {STYLE}"),
    ("which-logbook", "Ask which logbook: 9:02 or 9:00, 9:40 or 9:45.", f"Ink holding two logbooks, mouth closed. {STYLE}"),
    ("comment-hook", "Would you have waited for nine. Tell me in the comments.", f"Ink pointing at the viewer, a breakfast clock at 8:59, mouth closed. {STYLE}"),
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
        title="The War That Lasted Thirty Eight Minutes",
        description=(
            "Zanzibar, eighteen ninety six. A breakfast ultimatum, a wooden palace, "
            "and logbooks that still argue about nine forty."
        ),
        tags=(
            "history",
            "zanzibar",
            "shortest war",
            "cartoon",
            "true story",
            "1896",
            "clock",
            "indian ocean",
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
        thumbnail_hook="CHECK THE CLOCK",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The War That Lasted Thirty Eight Minutes",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-zanzibar.json"
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
    print("tsv", tsv)


if __name__ == "__main__":
    main()

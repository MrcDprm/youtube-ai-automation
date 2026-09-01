"""Author Drawn Anyway episode 24: New Coke, nineteen eighty five."""

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
    """On the twenty third of April nineteen eighty five, Coca-Cola locked the old formula in an Atlanta bank vault and told the world it would never be used again. That is not a metaphor, and it is not a cartoon you invented after a trivia night about the dumbest soda in America. Roberto Goizueta, the chairman, called the new flavor smoother, rounder, bolder, more harmonious. Donald Keough said he had never been as confident about a decision. They had run about one hundred ninety thousand blind taste tests in the United States and Canada. The sweeter sip beat the old Coke, and it beat Pepsi. Keep that score. Then put a red X on the joke that the company was too stupid to count. The leftover is not a conspiracy. The leftover is a sip that won a test, and a can people already had in the fridge.""",
    """Start with why a new formula was supposed to be the sure plan. After the war, Coca-Cola had about sixty percent of the cola market. By nineteen eighty three that number was under twenty four, Pepsi eating supermarket space, Coke holding vending machines and fast food, especially McDonald's. Pepsi's Challenge, from the mid nineteen seventies, put two unmarked cups in a mall and let the sweeter sip win on camera. Internal tests at Coke got the same leftover. Goizueta had told the company in nineteen eighty there would be no sacred cows, including how the drinks were made. Diet Coke in nineteen eighty two had already shown a sweeter path. Sergio Zyman and Brian Dyson ran a secret job called Project Kansas, named for a photo of Kansas journalist William Allen White drinking a Coke that hung on office walls. Management rejected selling the new flavor beside the old one. Bottlers were already sore about Diet Coke and syrup prices. Goizueta wanted New Coke or no Coke, and he wanted the word New on the can. The official idea was: the sip is the product, so change the sip.""",
    """File the numbers, because the vault does not start as a tantrum. Time magazine filed more than one hundred ninety thousand consumers, twenty five cities, nineteen eighty one to eighty four. The new flavor beat the old by fifty five to forty five. When people were told what they were tasting, sixty one to thirty nine. Against Pepsi, a trade source gave as much as fifty six to forty four. Later write-ups round the whole program toward two hundred thousand. File the range. A marketing case later noted that of those testers, only about thirty or forty thousand actually tasted the formula that shipped. Most were not told a yes meant the old can would vanish. About ten to twelve percent in focus groups got angry at the thought of a replacement and said they might stop. The company downplayed them. Robert Woodruff, who had built the international brand, died in March at ninety five, a month before launch. Goizueta said he had Woodruff's blessing. Friends inside doubted the old man understood. Production of the original ended later that week. Gold tops on leftover cans. Yellow stickers on multi-packs. Lincoln Center, April twenty third: Goizueta would not admit taste tests had led the change. He called it one of the easiest decisions they had ever made. Pepsi had already fed reporters questions. Roger Enrico took a full page in the New York Times and gave Pepsi people the twenty sixth off. The other guy just blinked.""",
    """Here is the leftover the internet files as America losing its mind over soda. Early numbers looked like the research. Sales in launch cities up about eight percent. Most regular drinkers kept buying. Three quarters said they would buy it again. Then the hotline. Wikipedia files over forty thousand calls and letters. UPI, by the tenth of June, one thousand five hundred a day, most of them unhappy, versus about four hundred before. History later cites five thousand a day, then eight thousand. File the range. Do not invent a nicer round number. A psychiatrist hired to listen said some callers sounded like a death in the family. Gay Mullins in Seattle formed Old Cola Drinkers of America on the twenty eighth of May, tens of thousands of calls, a lawsuit a judge dismissed. In informal blinds, Mullins could not always pick the old can, or preferred the new one. File that too. Johnny Carson and David Letterman made it a week of jokes. Ads were booed on a scoreboard in Houston. International bottlers in Monaco did not want to sell it. Zyman heard the same doubt from relatives in Mexico. By mid-June the summer lift was flattening. On the twenty third of June, bottlers told Atlanta they were tired of being the face of the change. The twenty still suing over syrup used the formula in court. If the new can was just a sweeter cousin of Diet Coke, the unique-syrup argument got thinner. Talks moved from if to when.""",
    """Seventy nine days. On the eleventh of July, the same executives announced the original was coming back as Coca-Cola Classic. Peter Jennings broke into General Hospital. Senator David Pryor called it a meaningful moment in United States history. The hotline took thirty one thousand six hundred calls in two days. Keough said all the time and money and skill in the research could not measure the attachment. He also answered the conspiracy: some cynics would say they planned the whole thing; the truth is they were not that dumb and not that smart. Snopes later filed the planned-ploy story as false. File it as a rumor. Do not spend it as a plot. Mullins got the first case of Classic, then complained it made him sick, blaming high-fructose corn syrup, and said the syrup had dulled his taste, which is how he had preferred New Coke in tests. Some tongues said the first Classic batches were not the spring formula. In a few regions that was logistics: bottlers who had not already switched were now using corn syrup instead of cane. Most already had. The leftover in the can was not always the leftover in the vault.""",
    """Rehook, because the internet likes a fake panic and a moral about sheep who cannot handle change. Put a red X on that sermon. A sip test is not a personality. A hotline is not a census of American intelligence. Malcolm Gladwell later sat with food researchers who blamed the test itself. Carol Dollard, who had worked product development at Pepsi, told him a sip test and a home-use test can give you the exact opposite. A sweeter sip wins a mouthful and loses a fridge. Coke never asked the survey the only question that mattered: how would you feel if this replaced the one you already buy. Sensation transference, a Cheskin leftover from the nineteen forties: people taste the red can and the script as much as the liquid. Darrel Rhea later said the mistake was attributing the share loss entirely to the product. Pepsi had been building a youth brand since the sixties. The sip was a costume for a generation Pepsi had already named. The vault was a costume for a formula they still had.""",
    """File what the two cans actually did. By the end of nineteen eighty five, Classic was outselling New Coke and Pepsi. New Coke dwindled toward a three percent share, still decent in Los Angeles. A later analysis credited Cherry Coke, launched almost at the same time, more than the comeback myth. File that too. McDonald's switched fountains back to the original almost immediately. No one was fired. Goizueta said he never regretted the change, threw a tenth anniversary for New Coke in nineteen ninety five, and drank it until he died in ninety seven. Zyman later wrote that it infuriated the public, cost a ton, lasted about seventy seven days in his count, and still reattached people to the brand. Wikipedia's clock is seventy nine. File the two days. In nineteen ninety the leftover can became Coke Two in Spokane, a Pepsi town, rose, then fell, and died as a line in two thousand two. Classic kept the word Classic on the label into two thousand nine. In twenty nineteen they poured a limited run for a Netflix show set in nineteen eighty five, about five hundred thousand cans, and the website fell over from orders.""",
    """None of this is a hymn to a sacred soda, and none of it is a cartoon of shoppers as children. They had a sip cup. They had a vault. They had a hundred ninety thousand check marks that never asked about replacement. You are allowed to laugh at a chairman calling the easiest decision in the building, and at a full-page victory ad from the other cola, and at a Senate floor treating a can as history. You are not required to laugh at a hotline that sounded like grief, or at bottlers getting frozen out at dinner, or at a sip that was honest as far as a sip goes. The official idea was: New Coke or no Coke. The street idea was: they ruined the real thing. The leftover idea is: they still had the formula, and the test had measured a mouthful, not a habit.""",
    """So who won. Not the vault lock in April. Not the conspiracy that they planned the riot. Goizueta won a sip that beat Pepsi in a cup. Keough won a sentence about not being that dumb and not that smart. Mullins won a protest group and a first case, then a complaint about corn syrup. Enrico won a holiday and almost no permanent converts. Classic won the supermarket by Christmas. The sip won the test and lost the fridge. If you need a moral, skip never change anything. Take this: a taste test is a terrible whole story, and a formula you already own is a terrible honest one. The next time someone tells you New Coke proves people are irrational, ask whether the survey asked about deletion, and whether the winning sip was ever drunk by the can. Would you have killed the old formula for a two-ounce cup, or kept both on the shelf. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no cruelty, not mud-green archive night, not After Hours File dark. "
    "New Coke shown as candy red cans labeled NEW and CLASSIC, a sip cup, a bank vault, a fridge, "
    "not photoreal logos, not a flag protest, not pouring soda as cruelty. Recurring mascot Ink "
    "may cameo: mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("vault-lock", "23 April 1985: old formula locked in an Atlanta vault, never again.", f"A candy bank vault, tag ATLANTA, a formula card 7X LOCKED. Cream paper. {STYLE}"),
    ("not-trivia", "Not a dumbest-soda trivia gag.", f"Ink shaking his head at a DUMBEST SODA stamp with a red X, mouth closed. {STYLE}"),
    ("goizueta-words", "Goizueta: smoother, rounder, bolder, more harmonious.", f"A quote card SMOOTHER ROUNDER BOLDER, nameplate GOIZUETA. No portrait. {STYLE}"),
    ("keough-confident", "Keough: never been as confident about a decision.", f"A badge NEVER MORE CONFIDENT, nameplate KEOUGH. {STYLE}"),
    ("190k-sips", "About 190,000 blind taste tests, U.S. and Canada.", f"A tally 190000 BLIND SIPS, tiny cups. {STYLE}"),
    ("sip-beat-pepsi", "The sweeter sip beat old Coke, and it beat Pepsi.", f"A scoreboard SIP WINS vs OLD and PEPSI. {STYLE}"),
    ("x-too-stupid", "Put a red X on the company-was-too-stupid-to-count joke.", f"A TOO STUPID TO COUNT stamp with a giant red X. {STYLE}"),
    ("leftover-fridge", "Leftover: a sip that won a test, a can already in the fridge.", f"A tiny sip cup vs a fridge full of cans. {STYLE}"),
    ("sixty-to-24", "After the war ~60% cola share. By 1983 under 24%.", f"A falling bar 60% to UNDER 24%, year 1983. {STYLE}"),
    ("pepsi-challenge", "Pepsi Challenge, mid-1970s: two unmarked cups, sweeter sip on camera.", f"Two unmarked cups, a camera, tag PEPSI CHALLENGE. {STYLE}"),
    ("no-sacred-cows", "Goizueta 1980: no sacred cows, including how drinks were made.", f"A NO SACRED COWS stamp, year 1980. {STYLE}"),
    ("diet-coke-82", "Diet Coke 1982 already showed a sweeter path.", f"A can DIET 1982 beside a sweeter-path arrow. {STYLE}"),
    ("project-kansas", "Zyman and Dyson: Project Kansas, named for a photo of William Allen White.", f"A folder PROJECT KANSAS, a framed photo of a man with a soda. Not photoreal. {STYLE}"),
    ("not-beside", "Management rejected selling new beside old. Bottlers sore about Diet Coke.", f"A rejected shelf NEW + OLD with a red X, bottler clipboard. {STYLE}"),
    ("new-or-no", "Goizueta: New Coke or no Coke. The word NEW on the can.", f"Two doors NEW COKE and NO COKE, a can tagged NEW. {STYLE}"),
    ("official-sip", "Official idea: the sip is the product, so change the sip.", f"A giant sip cup labeled THE PRODUCT. {STYLE}"),
    ("time-55-45", "Time: 190,000 testers, 25 cities. New beat old 55 to 45.", f"A magazine card TIME, 55-45 NEW vs OLD. {STYLE}"),
    ("told-61-39", "When told what they were tasting: 61 to 39.", f"A reveal card TOLD YOU, 61-39. {STYLE}"),
    ("vs-pepsi-56", "Against Pepsi, a trade source: as much as 56 to 44.", f"A trade slip 56-44 vs PEPSI. {STYLE}"),
    ("30-40-thousand", "Only about 30 or 40 thousand tasted the formula that shipped.", f"A funnel 190K down to 30-40K FINAL FORMULA. {STYLE}"),
    ("not-told-vanish", "Most were not told a yes meant the old can would vanish.", f"A survey clipboard with VANISH? left blank. {STYLE}"),
    ("ten-percent-angry", "About 10-12% in focus groups angry at replacement. Downplayed.", f"A small angry 10-12% slice, stamp DOWNPLAYED. Cute not cruel. {STYLE}"),
    ("woodruff-march", "Woodruff died March 1985, age 95, a month before launch.", f"A calendar MAR 1985, nameplate WOODRUFF 95. No portrait. {STYLE}"),
    ("gold-tops", "Original production ended that week. Gold tops on leftover cans.", f"Cans with gold lids, tag OLD CAN NEW SODA. {STYLE}"),
    ("lincoln-easiest", "Lincoln Center: Goizueta called it one of the easiest decisions.", f"A stage card LINCOLN CENTER, EASIEST DECISION. {STYLE}"),
    ("enrico-blinked", "Enrico: full-page Times ad. Pepsi holiday April 26. The other guy blinked.", f"A newspaper THE OTHER GUY BLINKED, date 26 APR. {STYLE}"),
    ("eight-percent", "Early launch-city sales up about 8%. Three quarters would buy again.", f"A chart +8%, badge 3/4 BUY AGAIN. {STYLE}"),
    ("hotline-range", "Hotline: file 1,500 a day, or 5,000, or 8,000. Forty thousand letters in one count.", f"A phone 800-GET-COKE, ledger FILE THE RANGE. {STYLE}"),
    ("psychiatrist", "A psychiatrist listening said some callers sounded like a death in the family.", f"A headset and a small grief-note, not gore, not a funeral. {STYLE}"),
    ("mullins-may28", "Gay Mullins, Seattle, Old Cola Drinkers, 28 May. Lawsuit dismissed.", f"A protest sign OLD COLA DRINKERS, date 28 MAY, gavel DISMISSED. {STYLE}"),
    ("mullins-blind", "In informal blinds Mullins could not always pick the old can.", f"Three cups, Mullins nameplate, tag COULD NOT TELL. {STYLE}"),
    ("scoreboard-boo", "Ads booed on a Houston scoreboard. Jokes on late night.", f"A stadium scoreboard NEW COKE with BOO. Cute not grim. {STYLE}"),
    ("monaco-no", "International bottlers in Monaco did not want to sell it.", f"A map pin MONACO, stamp NOT INTERESTED. No flags. {STYLE}"),
    ("june-23-bottlers", "23 June: bottlers told Atlanta they were tired of being the face.", f"A meeting table ATLANTA 23 JUN, tired bottler hats. {STYLE}"),
    ("if-to-when", "Talks moved from if to when.", f"A toggle IF flipped to WHEN. {STYLE}"),
    ("july-11", "11 July, 79 days: original returns as Coca-Cola Classic.", f"A calendar 11 JUL, 79 DAYS, can CLASSIC. {STYLE}"),
    ("jennings-bulletin", "Peter Jennings broke into General Hospital. Pryor: a meaningful moment.", f"A TV bulletin INTERRUPT, nameplate JENNINGS, Senate gavel PRYOR. {STYLE}"),
    ("31600-calls", "Hotline: 31,600 calls in two days after the return.", f"A call counter 31600 IN 2 DAYS. {STYLE}"),
    ("not-dumb-smart", "Keough: we are not that dumb, and we are not that smart.", f"A quote card NOT THAT DUMB NOT THAT SMART. {STYLE}"),
    ("snopes-false", "The planned-ploy story: later filed false. Rumor, not a plot.", f"A conspiracy stamp with a red X, tag RUMOR. {STYLE}"),
    ("hfcs-leftover", "Classic in some regions used corn syrup, not cane. Leftover in the can was not always the vault.", f"Two sweetener cards CANE vs CORN SYRUP. {STYLE}"),
    ("x-sheep", "Rehook: red X on the sermon that shoppers were sheep.", f"Ink peeling a SHEEP stamp, mouth closed. {STYLE}"),
    ("sip-vs-home", "Dollard: a sip test and a home-use test can give the exact opposite.", f"A sip cup vs a home fridge, OPPOSITE arrows. {STYLE}"),
    ("never-asked", "They never asked: how would you feel if this replaced the one you buy.", f"A survey with one blank line IF THIS REPLACES IT. {STYLE}"),
    ("red-can-taste", "Sensation transference: people taste the red can and the script.", f"A red can with a thought-bubble TASTING THE LABEL. {STYLE}"),
    ("classic-wins", "By end of 1985 Classic outsold New Coke and Pepsi.", f"A podium CLASSIC first, NEW and PEPSI behind. {STYLE}"),
    ("three-percent", "New Coke toward a 3% share. Cherry Coke launched almost at the same time.", f"A tiny 3% slice, a can CHERRY 1985. {STYLE}"),
    ("no-one-fired", "No one fired. Goizueta never regretted it. Tenth anniversary 1995.", f"A party hat 10 YR 1995, stamp NOBODY FIRED. {STYLE}"),
    ("coke-ii", "1990: Coke II in Spokane. Died as a line in 2002.", f"A map pin SPOKANE 1990, tombstone 2002 as a product end, not gore. {STYLE}"),
    ("netflix-cans", "2019: limited run, about 500,000 cans. The website fell over.", f"A crate 500000 CANS 2019, a crashed website bar. {STYLE}"),
    ("who-won-fridge", "The sip won the test and lost the fridge.", f"A sip cup trophy vs a winning fridge. {STYLE}"),
    ("ask-deletion", "Ask whether the survey asked about deletion, and whether the sip was drunk by the can.", f"A question mark over a survey and a two-ounce cup. {STYLE}"),
    ("kill-or-keep", "Would you have killed the old formula for a two-ounce cup, or kept both.", f"Split: a vault lock vs two cans on a shelf, a question mark. {STYLE}"),
    ("receipt", "They still had the formula. Drawn anyway.", f"A receipt card SIP vs HABIT, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Soda That Tried to Replace Itself",
        description=(
            "Nineteen eighty five. A hundred ninety thousand sips, a vault, "
            "and a formula they already had."
        ),
        tags=(
            "history",
            "1985",
            "new coke",
            "coca-cola",
            "marketing",
            "cartoon",
            "true story",
            "logistics",
            "taste test",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="THE SIP WAS WRONG",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Soda That Tried to Replace Itself",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-newcoke.json"
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

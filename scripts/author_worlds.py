"""Author Drawn Anyway episode 17: War of the Worlds radio, nineteen thirty eight."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PROJECT_ROOT, drawn_beat_count
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_drawn_scenario, write_scenario

TERMS = ("cartoon illustration", "storytime cartoon")
BEAT_SECONDS = 540.0
TARGET_SECONDS = 600.0
MINUTES = 9
VOICE = "en-AU-WilliamNeural"
RATE = "+4%"

CHAPTERS = [
    """A radio play once made the front page by sounding like the news. That is not a metaphor, and it is not a cartoon you invented after a trivia night about Martians in New Jersey. On Sunday the thirtieth of October nineteen thirty eight, at eight in the evening Eastern time, The Mercury Theatre on the Air went live from the Columbia Broadcasting Building at four hundred eighty five Madison Avenue, New York, over the CBS Radio Network. It was the seventeenth episode. Orson Welles was twenty three. He directed and narrated. Howard Koch had adapted H. G. Wells's eighteen ninety eight novel. The landing was moved to Grovers Mill, an unincorporated village in West Windsor, New Jersey. Keep that picture. Then put a red X on the nationwide stampede. The leftover is not that Mars arrived. The leftover is that the next morning's papers needed a panic, and a ratings service named Hooper had already telephoned five thousand households that night: two percent were on the play, and nobody said they were listening to the news.""",
    """Start with why a Halloween play was supposed to be ordinary. Mercury was a sustaining show, which means no sponsor and almost no commercial breaks, a small loyal audience against NBC's Chase and Sanborn Hour with Edgar Bergen and Charlie McCarthy in the same slot. John Houseman produced. Paul Stewart was associate producer. Davidson Taylor sat for CBS. Koch was assigned the Wells novel on the twenty fourth of October, with Sunday already on the calendar. He had just come off Hell on Ice, Seventeen, and Around the World in Eighty Days. On the night of the twenty fifth he rang Houseman in what Houseman later called deep distress: the book would not sit as radio. His secretary Anne Froelick agreed. Houseman's fallback was an abandoned Lorna Doone. He told Koch to keep going. They wrote through the night. Stewart recorded an acetate without music. Welles, busy rehearsing Danton's Death, heard it at the St. Regis and called it dull, and asked for more news flashes. CBS legal then said the script was too credible, and demanded about twenty eight phrasing changes: Hotel Biltmore became a nonexistent Park Plaza, Columbia Broadcasting Building became Broadcasting Building, Princeton University Observatory became Princeton Observatory. The New York Times had already listed it as a play. The official plan was going to work: it is fiction, it is in the paper, it is Halloween, and four announcements on the network will say so.""",
    """The hour opens with a paraphrase of Wells, then a weather report, then dance music by Ramon Raquello and his orchestra from a hotel ballroom that did not exist under that name. Bulletins cut in: gas explosions on Mars, then a cylinder on a farm at Grovers Mill. Frank Readick played reporter Carl Phillips. He had gone to the record library and played Herbert Morrison's Hindenburg report until the panic in the voice was a craft, not an accident. Bernard Herrmann's orchestra had to sound like a dance band. Welles wanted the music to sit for unbearably long stretches. The emergency fill was a solo piano, Debussy and Chopin, which Houseman later called the neatest trick of the show. From the first mention of meteorites to the fall of New York, Houseman wrote, the broadcasting time was less than forty minutes. Then Dan Seymour broke in: you are listening to a CBS presentation of Orson Welles and the Mercury Theatre on the Air. There were four such announcements: beginning, before the middle break, after it, and at the end. The middle break ran about ten minutes late to protect the drama. After the play, Welles compared the night to dressing up in a sheet and jumping out of a bush and saying boo. He said they annihilated the world before your very ears and utterly destroyed CBS, and that both institutions were still open for business. If your doorbell rings and nobody is there, that was no Martian. It is Halloween.""",
    """Here is the leftover that photographs as a riot and is not one. At about eight thirty two, Houseman saw Taylor leave the studio for a phone, then come back pale as death with an order to interrupt and announce fiction. The rooftop reporter, Ray Collins, was already choking on the black smoke over Manhattan, and the first scheduled break was under a minute away. It ran as planned. Stefan Schnabel sat in the anteroom and watched police trickle in, then more, a struggle of uniforms, page boys, and executives trying to keep the show on. During the sign-off the phone rang. Houseman picked up a furious man who said he was mayor of a Midwestern town where mobs were in the streets. Houseman hung up. Paul White, head of CBS News, found a switchboard that could take only a fraction of the calls, and Welles saying he was through, washed up. White wrote explanations to put on the air. The cast left by a rear door. Welles went to an all-night rehearsal of Danton's Death. Shortly after midnight, at Broadway and Forty Second, the Times building zipper read ORSON WELLES CAUSES PANIC. Houseman later wrote that when they were finally released, life was going on as usual in the streets of New York. Ben Gross, radio editor of the Daily News, wrote in nineteen fifty four that the streets were nearly deserted as he walked to the studio for the end of the program.""",
    """File the numbers without turning them into a stampede. That night the C. E. Hooper company telephoned five thousand households. Two percent said they were listening to the radio play. None said a news broadcast. About ninety eight percent were on something else, most likely Chase and Sanborn, or the set was off. Some CBS affiliates, including Boston's WEEI, had preempted Mercury for local commercials, which shrinks the map further. Hadley Cantril, a Princeton psychologist, published The Invasion from Mars in nineteen forty. He put the audience around six million, of whom one point seven million took it as news, and one point two million were frightened or disturbed. Jefferson Pooley and Michael J. Socolow later called the method flawed: the estimate sat more than twice any other measure, the interviews came after the headlines, and frightened is not the same word as panicked. A. Brad Schwartz read some two thousand letters to Welles and the FCC. About twenty seven percent came from frightened listeners or people who said they saw a panic. Schwartz's later count of people panicked enough to flee outside, in a country of about one hundred thirty million, is filed by some historians as fewer than fifty. File the disagreement. Do not pick the cartoon million because it sounds like a better story. Newark hospitals logged no shock admissions that night. No verified suicide attaches to the broadcast. Calling a newspaper to ask if Mars is real is a check. It is not a mob.""",
    """Rehook, because the internet likes a nation in the streets and a boy genius who fooled America. Within three weeks the papers had published at least twelve thousand five hundred articles about the night. The story fell off the front pages in a few days, which is a circulation curve, not a body count. It was late Sunday in the Eastern time zone. Many city rooms were thin. Coverage ran as Associated Press roundups from bureaus, anecdotal, which reads like everywhere at once. Radio had taken advertising money from print through the Depression. Editor and Publisher warned that the nation faced incomplete news over a medium that had yet to prove it could do the news job. That is a trade paper defending a dock, not a sociology paper. Pooley and Socolow, writing in Slate on the seventy fifth anniversary, put it plainly: the supposed panic was so tiny as to be practically immeasurable on the night, and the papers seized a chance to tell advertisers and regulators that radio management was not to be trusted. W. Joseph Campbell and Robert E. Bartholomew later joined the same consensus: not nationwide. The Twin City Sentinel joked that Charlie McCarthy had saved the United States from death by hysteria, because most sets were on Bergen. A joke can be a receipt. A roundup is not a census.""",
    """The morning after, the thirty first of October, Welles was called to a press conference on about three hours of sleep. He said the technique was not original and not even new, and that he had anticipated nothing unusual. Asked why American cities were in the script, he said Wells had used real cities in Europe. He said he was terribly sorry now. The FCC did not punish CBS or Welles, and kept the complaints out of license renewals. Iowa senator Clyde L. Herring talked of a bill to review programs before they aired. It was never introduced. Campbell Soup then put money under the show, and Mercury became The Campbell Playhouse. That is a sponsor walking in after a headline, which is logistics wearing a halo. Koch had been paid fifty dollars a week, then sixty, and Houseman had given him the rights to scripts in lieu of a real salary. Welles later fought Cantril's book for listing Koch as sole author. H. G. Wells met Orson Welles once, in late October nineteen forty, in San Antonio, on KTSA with Charles C. Shaw. The novelist asked whether there had been such a panic, or whether it was Halloween fun. A Munich speech on the eighth of November nineteen thirty eight used the American story as a caption about democracy. File the speech. Do not let it steal the switchboard.""",
    """None of this is a hymn to a gullible country, and none of it is a cartoon of listeners as fools who should have known better than to own a radio in nineteen thirty eight. They had had a month of Munich on the set, boot by boot, as Frank Brady later wrote. Paul White thought the fright, where it existed, sat on that suspense. The Radio Project found that less than a third of the frightened understood the invaders as Martians; many heard Germans, or a disaster. Concrete, Washington, lost power and phones that night at a cement-plant substation, a coincidence that still rode the wire as proof. Jack Paar, on WGAR in Cleveland, told callers the world was not ending. Some accused him of covering it up. That is a rumor colliding with a drama, not a census of the Republic. You are allowed to laugh at a dance band that was a plot device, and at a piano that sat too long. You are not required to laugh at a Trenton switchboard, or at a person who dialed the paper because the bulletin sounded like the Hindenburg. A news flash is a costume. Four disclaimers are a receipt. Twelve thousand five hundred articles are a press run. Two percent is a rating.""",
    """So who won. Not Mars. Not a nationwide stampede. Not the later caption that everybody switched over from Charlie McCarthy and missed the open. The papers won a week of panic copy and a sermon about radio. Hooper won two percent and a quiet night in most living rooms. Welles won a reputation as a trickster, then a sponsor, then the long shadow of the zipper in Times Square. Koch won a script he had not wanted on Tuesday. CBS won an FCC that did not punish, and a legal department that had already made them change twenty eight names. Grovers Mill won a later marker on a story about a farm that was a sound effect. If you need a moral, skip never trust radio. Take this: a headline is a terrible instrument for measuring a living room, and a living room is a terrible census when the city editor is home on Sunday. The next time someone tells you America ran into the street because Mars landed in New Jersey, ask whether they mean the broadcast or the morning edition, and whether Hooper's two percent was in the room. Would you have believed the bulletin, or would you have checked the newspaper listings first. Tell me in the comments. That is the receipt. Drawn anyway.""",
]

STYLE = (
    "Bold cartoon storytime, thick ink outlines, flat candy fills of mustard, ink-blue, "
    "cream paper and tomato red, slight paper grain, non-photorealistic, illustrated, "
    "not a photo, no live-action, no realism, no stickman, no MS Paint, no gore, no flags as identity, "
    "no photoreal faces, no corpses, no alien gore, no heat-ray burns, no blood, not mud-green archive night, "
    "not After Hours File dark. Broadcast shown as a candy radio, a newspaper stack, a tiny dance band, "
    "a farm cylinder as a cartoon prop, a switchboard, a Times zipper, not violence and not stampedes. "
    "Recurring mascot Ink may cameo: mustard jacket, ink-blue hair, oversized black marker, mouth closed, readable silhouette."
)

_ROWS: list[tuple[str, str, str]] = [
    ("front-page-play", "A radio play made the front page by sounding like news.", f"Cartoon title beat: a giant newspaper FRONT PAGE over a tiny candy radio, cream paper, hook energy. No stampede. {STYLE}"),
    ("not-trivia", "Not a Martians-in-New-Jersey trivia gag.", f"Ink shaking his head at a TRIVIA MARS stamp with a red X, mouth closed. {STYLE}"),
    ("oct-30-1938", "Sunday 30 October 1938, 8 pm Eastern.", f"A calendar 30 OCT 1938 and a round clock 8:00 ET, no flag. {STYLE}"),
    ("madison-485", "Columbia Broadcasting Building, 485 Madison Avenue.", f"A building plaque 485 MADISON, CBS RADIO, cream paper. {STYLE}"),
    ("mercury-17", "Mercury Theatre on the Air, episode 17.", f"A radio-show card MERCURY THEATRE EPISODE 17. {STYLE}"),
    ("welles-23", "Orson Welles, 23, directed and narrated.", f"A nameplate ORSON WELLES, tag 23, DIRECTOR, no portrait. {STYLE}"),
    ("koch-wells", "Howard Koch adapted H. G. Wells, 1898.", f"Two books: H.G. WELLS 1898 and KOCH RADIO SCRIPT. {STYLE}"),
    ("grovers-mill", "Landing moved to Grovers Mill, West Windsor, New Jersey.", f"A simple map GROVERS MILL NJ, a tiny farm, no flags. {STYLE}"),
    ("x-on-stampede", "Put a red X on the nationwide stampede.", f"A STAMPEDE stamp with a giant red X. Empty street. {STYLE}"),
    ("hooper-two", "Hooper: 2 percent on the play. Nobody said news.", f"A ratings badge HOOPER 2 PERCENT, a NEWS stamp with a zero. {STYLE}"),
    ("sustaining", "Sustaining show: no sponsor, almost no ad breaks.", f"A radio log SUSTAINING, NO SPONSOR, tiny empty ad slot. {STYLE}"),
    ("chase-sanborn", "Same slot as NBC Chase and Sanborn, Bergen, McCarthy.", f"Two dials CBS MERCURY vs NBC CHASE AND SANBORN, bigger NBC. {STYLE}"),
    ("houseman-stewart", "John Houseman produced. Paul Stewart associate.", f"Two nameplates HOUSEMAN PRODUCER and STEWART ASSOCIATE, no portraits. {STYLE}"),
    ("koch-oct24", "Koch assigned the novel on 24 October.", f"A calendar 24 OCT, assignment slip WAR OF THE WORLDS. {STYLE}"),
    ("lorna-doone", "Fallback was abandoned Lorna Doone. Keep going.", f"A script LORNA DOONE with a red X, WELLS script on top. {STYLE}"),
    ("all-nighter", "Koch, Houseman, Froelick wrote through the night.", f"Three nameplates KOCH HOUSEMAN FROELICK, coffee and paper stacks. {STYLE}"),
    ("dull-acetate", "Welles at the St. Regis called the acetate dull. More flashes.", f"A disc ACETATE, a stamp MORE NEWS FLASHES. {STYLE}"),
    ("twenty-eight", "CBS legal: too credible. About 28 phrasing changes.", f"A legal stamp TOO CREDIBLE, tally 28 CHANGES. {STYLE}"),
    ("biltmore-plaza", "Hotel Biltmore became a nonexistent Park Plaza.", f"A hotel sign BILTMORE crossed out, PARK PLAZA invented. {STYLE}"),
    ("nyt-listing", "The New York Times listed it as a play.", f"A listings clip NYT TONIGHT PLAY WAR OF THE WORLDS. {STYLE}"),
    ("official-plan", "Official plan: fiction, four announcements, Halloween.", f"A clipboard PLAN: FICTION, 4 ANNOUNCEMENTS, HALLOWEEN. {STYLE}"),
    ("ramon-raquello", "Dance music: Ramon Raquello and his orchestra.", f"A tiny candy dance band RAMON RAQUELLO, hotel ballroom sign. {STYLE}"),
    ("cylinder-farm", "Bulletins: gas on Mars, then a cylinder on a farm.", f"A cartoon farm with a candy metal cylinder prop, not gore. {STYLE}"),
    ("readick-hindenburg", "Frank Readick played Carl Phillips off the Hindenburg record.", f"A nameplate FRANK READICK, a disc HINDENBURG, mic, no crash gore. {STYLE}"),
    ("herrmann-piano", "Herrmann's band as dance music. Solo piano fill, Debussy, Chopin.", f"An orchestra pit plus a lonely piano DEBUSSY CHOPIN. {STYLE}"),
    ("forty-minutes", "Meteorites to the fall of New York: under 40 minutes.", f"A stopwatch UNDER 40 MIN, a tiny skyline as a radio prop. {STYLE}"),
    ("four-announcements", "Four network announcements that it was a dramatization.", f"Four stamps ANNOUNCEMENT 1 2 3 4, FICTION. {STYLE}"),
    ("boo-sheet", "Welles: a sheet, a bush, boo. Both institutions still open.", f"A cartoon sheet labeled BOO, a sign CBS STILL OPEN. No ghost gore. {STYLE}"),
    ("eight-thirty-two", "8:32, Taylor pale, ordered to interrupt. Break was a minute away.", f"A clock 8:32, nameplate DAVIDSON TAYLOR, phone, PALE stamp. {STYLE}"),
    ("police-anteroom", "Police in the anteroom. Executives kept the show on.", f"Cartoon cops and PAGE BOYS at a studio door, comic scramble, not violence. {STYLE}"),
    ("white-board", "Paul White: switchboard a sea of light. Welles: I'm through.", f"A giant switchboard ALL LIGHTS, nameplate PAUL WHITE, tag I'M THROUGH. {STYLE}"),
    ("times-zipper", "Times zipper after midnight: ORSON WELLES CAUSES PANIC.", f"A building zipper ORSON WELLES CAUSES PANIC, cream paper, no mob. {STYLE}"),
    ("deserted-streets", "Houseman and Ben Gross: New York streets ordinary, nearly deserted.", f"An empty candy NYC street ORDINARY, NO MOB stamp. {STYLE}"),
    ("five-thousand", "Hooper telephoned 5,000 households that night.", f"A survey clipboard 5000 HOUSEHOLDS, HOOPER. {STYLE}"),
    ("ninety-eight", "About 98 percent were elsewhere, or the set was off.", f"A pie 2 PERCENT vs 98 PERCENT ELSEWHERE. {STYLE}"),
    ("weei-preempt", "Boston WEEI preempted Mercury for local commercials.", f"A station plate WEEI BOSTON, LOCAL ADS over MERCURY. {STYLE}"),
    ("cantril-six", "Cantril 1940: about 6 million heard it. File the method.", f"A book INVASION FROM MARS 1940, 6 MILLION with a question mark. {STYLE}"),
    ("frightened-not", "Frightened is not the same word as panicked.", f"Two word cards FRIGHTENED and PANICKED, a red unequal sign. {STYLE}"),
    ("schwartz-letters", "About 2,000 letters. About 27 percent frightened or saw panic.", f"A letter stack 2000, slice 27 PERCENT, SCHWARTZ. {STYLE}"),
    ("fewer-fifty", "Some later counts: fewer than 50 fled outside. File the disagreement.", f"A tiny tally FEWER THAN 50 vs a huge MYTH million with a red X. {STYLE}"),
    ("no-hospital", "Newark hospitals: no shock admissions that night.", f"A hospital clip NEWARK, SHOCK ADMISSIONS 0. {STYLE}"),
    ("rehook-streets", "Rehook: the internet likes a nation in the streets.", f"Ink peeling a NATION IN STREETS sticker off a map, mouth closed. {STYLE}"),
    ("twelve-five", "At least 12,500 articles in three weeks.", f"A press pile 12500 ARTICLES, 3 WEEKS, circulation curve. {STYLE}"),
    ("ap-roundup", "Thin Sunday city rooms. AP anecdotal bureau roundups.", f"An AP ROUNDUP card, many tiny bureau pins, ANECDOTAL stamp. {STYLE}"),
    ("ads-depression", "Radio had taken Depression advertising from print.", f"A money arrow ADS from NEWSPAPER stack to RADIO set. {STYLE}"),
    ("editor-publisher", "Editor and Publisher: radio had yet to prove the news job.", f"A trade-journal cover EDITOR AND PUBLISHER, RADIO NEWS warning. {STYLE}"),
    ("pooley-socolow", "Pooley and Socolow: panic practically immeasurable that night.", f"A Slate-style card POOLEY SOCOLOW, TINY PANIC. {STYLE}"),
    ("charlie-saved", "Twin City Sentinel: Charlie McCarthy saved the United States.", f"A joke headline CHARLIE MCCARTHY SAVED AMERICA, a dummy on a radio. No flags. {STYLE}"),
    ("fcc-no-punish", "FCC did not punish CBS or Welles.", f"A gavel FCC, stamp NO PUNISHMENT. {STYLE}"),
    ("campbell-playhouse", "Campbell Soup sponsored. Mercury became The Campbell Playhouse.", f"A soup can CAMPBELL beside a show card CAMPBELL PLAYHOUSE. {STYLE}"),
    ("wells-1940", "H. G. Wells, San Antonio 1940: was it Halloween fun.", f"Two nameplates H.G. WELLS and ORSON WELLES, KTSA 1940, HALLOWEEN FUN. No portraits. {STYLE}"),
    ("not-fools", "Not a cartoon of listeners as fools.", f"Ink peeling a FOOLS sticker off a RADIO LISTENERS sign, mouth closed. {STYLE}"),
    ("listings-or-bulletin", "Would you have believed the bulletin, or checked the listings.", f"Split: a NEWS FLASH mic vs a NYT LISTINGS clip, a question mark. {STYLE}"),
    ("receipt", "A headline is a terrible census. Two percent. Drawn anyway.", f"A receipt card HEADLINE vs HOOPER 2 PERCENT, Ink holding the marker, mouth closed. {STYLE}"),
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
        title="The Broadcast That Sounded Too Real",
        description=(
            "Mercury Theatre, October nineteen thirty eight. A Halloween play, "
            "a Hooper two percent, and a newspaper panic."
        ),
        tags=(
            "history",
            "war of the worlds",
            "1938",
            "orson welles",
            "radio",
            "cartoon",
            "true story",
            "mercury theatre",
            "cbs",
            "funny",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in beats
        ),
        thumbnail_hook="THE PAPERS WROTE IT",
    )
    scenario = build_drawn_scenario(
        draft,
        topic="The Broadcast That Sounded Too Real",
        language="en",
        minutes=MINUTES,
        target_seconds=TARGET_SECONDS,
        voice=VOICE,
        tts_rate=RATE,
        subtitle_color="#FFFFFF",
        now=datetime.now(UTC),
    )
    out = PROJECT_ROOT / "senaryo-drawn.json"
    named = PROJECT_ROOT / "senaryo-drawn-worlds.json"
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

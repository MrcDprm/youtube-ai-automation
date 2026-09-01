"""Author episode 5: the clerk invented your last name, then write senaryo-paint.json."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT
from modules.interfaces import DraftScene, DraftScript, DraftVisualBeat
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you are going to fill a box that says last name. You will not hesitate. The letters will arrive in your fingers the way your address does, as if they grew there. A bank wants it. A website wants it. A nurse with a clipboard wants it before she looks at your face. Here is the part that should bother you. For most of human history, that box did not exist. You had a name people shouted across a field. You had a father's name, a trade, a hill you lived under. You did not have a hereditary filing code that followed your grandchildren into a database and then into an ad. So why does a clerk's blank get to decide which family you belong to on paper? Because states needed to count you, tax you, conscript you, and find you again next year. That is the whole plot. Your last name is not a soul. It is a column. And you have been treating the column like blood, which is a compliment the column did not earn and a burden your relatives now share without voting on it.""",
    """Start with what a name was when the village was the whole map. Everyone knew which John you meant. John the miller. John by the oak. John's son, until that son got his own nickname and the old pointer went stale. The extra word was a pointer, not an heirloom. It could change if you moved, if you married, if you took a new job, if the village already had two millers and needed a joke to tell them apart. In many languages the second word was a sentence: son of, from, of the red hair. Iceland still works this way for a lot of people. A child is not born into a frozen family brand. The child is born as someone's child, which is a relationship, not a logo. You cannot put a relationship in a dropdown menu without flattening it, so the modern form pretends the logo was always there and that the flattening is just how humans come. It is not. It is how clerks come.""",
    """England is a useful mess because the paperwork survived and you can watch the stickiness happen. After the Norman conquest, elites already liked extra names that sounded like land. Ordinary people picked them up slowly, over centuries, not on a Tuesday with a press release. By the thirteen hundreds, tax lists and court rolls are stuffed with bynames that are starting to stick to sons even when the son does a different job. The poll taxes of thirteen seventy seven and thirteen eighty one needed heads you could write twice. If the same man is John Smith this year and John of the Green next year, the collector loses a coin and a night of sleep. Heredity is convenient for the collector. Once a word sticks to a household, the household becomes a line item. Smith stops meaning the man at the anvil and starts meaning his children's children, including the ones who never touched a hammer. That is how a job becomes a ghost that lives in your inbox and on the back of your debit card.""",
    """Other places did it as an order, not a drift. In seventeen eighty seven, Emperor Joseph the Second required Jews in much of the Habsburg lands to take fixed family names the state could file. Before that, many communities used patronymics and sacred names that did not fit a Christian clerk's ledger or his idea of a household. The edict was sold as order, modernity, neat streets of ink. It was also a leash. When a government tells you what your family is called, it is not discovering your essence. It is building an index it can search without asking your neighbors. Similar waves hit other empires in the same centuries. Civil registration under Napoleon wanted births, deaths, and marriages in a book a stranger could audit in a different town. The book does not care if your grandmother had three village names and a nickname that made people kind. The book wants one string that does not wander when the auditor arrives.""",
    """In nineteen thirty four, Turkey passed the Surname Law. Everyone had to pick a hereditary last name and write it where a clerk could read it. Mustafa Kemal took Ataturk. Ordinary people took words that sounded proud, or rural, or safe, or whatever a local official would stamp before closing time. Some names were banned for being too foreign, too religious, too tribal, too much like a title. That is not a fun fact for a quiz night. That is the state walking into the kitchen and saying the way you introduce yourself at a door is now a national project. If you have relatives who still tell the story of the afternoon the family chose a word, you are hearing the invention happen in living memory, not in a mist. Most English speakers think surnames are as old as caves. They are not. Some of the ones in use tonight are as old as a radio and a government circular.""",
    """This is the rehook. You think your last name is who you are. It is who you are to a form. The form came first in the places that needed armies and taxes and a way to punish the man who was not in the room. China had hereditary clan names for a very long time, which is a different tool, older and thicker, and it still served counting and kinship and office. The point is not that every culture waited for Europe to invent paper. The point is that a fixed family label is a technology. It solves a problem the village did not have and the empire did. Who is this man when he is not standing in front of you? The answer used to be: ask his neighbor. The answer became: look at the line. You are still living in the line. You type it into a box as if the box were a confession. It is a census with better typography. The confession feeling is a special effect. The special effect works because you learned it in school, on a form, before you learned where the word came from.""",
    """Listen to what the words still confess if you stop treating them as perfume. Baker, Cook, Wright, Taylor. Hill, Brooks, Ford. Johnson, Andersen, bin something, Mac something, O-apostrophe something. The language did not hide the filing system. It tattooed the old pointer onto the new brand. Then the brand forgot the pointer and started a fan club. You meet a Miller who cannot mill and a King who cannot rule and a Bishop who does not go to church, and nobody finds this strange, which is how you know the spell worked. The name outlived the fact, which is the definition of bureaucracy winning a century quietly. A clerk needed a handle that would still work after the anvil rusted. The handle became an identity you will defend in an argument, print on a cake, and teach a child to spell before they can explain what a state is or why the cake needed a second word.""",
    """Notice the feelings the box produces, because the feelings are the product now. Pride. Shame. A story about ancestors who may not have shared the word, or who were given it by a man with a list. People change names to escape a father, to enter a marriage, to stop being searchable, to sound like they belong in a new country, to make a child's school list less of a fight. That pain is real. The object causing it is still a column. Search engines made the column louder and cheaper to abuse. Your last name is now a query. Strangers can assemble a version of you from the string a tax man wanted for a reason that had nothing to do with your personality. Passport, credit check, school list, the email that is your name plus a number because someone else got there first. You are not imagining the weight. You are just mistaken about the age of the weight. It is heavy because it is useful to institutions, not because the universe assigned it in a ceremony with candles.""",
    """So what did we trade? We traded being known in a place for being findable in a system. We traded nicknames that could heal or sting and then fade for a string that follows you to a grave and then into genealogy websites that will sell you a crest that is almost certainly a lie. We also gained something that is not nothing. Inheritance is easier to argue when the names match enough for a judge. A letter can find a widow. A vaccine record can find a child who moved. A war crime can find a perpetrator, which is a use of the index that should make you pause before you call all paperwork a joke and all clerks a waste. The trick is pretending the index is nature. It is not. It is poll taxes, imperial edicts, a surname law, a dropdown menu designed in an office you will never visit. Family is older than the last name. The last name is how family got invited into the ledger and then could not leave.""",
    """This is you. You will type the box. You will feel like you are telling the truth about your blood. You are telling the clerk's truth, which is a thinner thing, and it still opens doors, still books a flight, still lets a hospital find the right chart. Put your finger on the letters. That is not your blood looking back. That is a handle invented so a stranger could find you next April when the list is due. You are allowed to love the sound. You are allowed to keep it, change it, hyphenate it, refuse the father's word, invent a kinder one. Just stop confusing the handle with the people who answer when you call. Tonight, when the form asks for last name as if it were asking for your soul, look at the blank the way you would look at a stamp. Someone needed a column. You learned to live inside it. The box is still empty until you agree. You will agree. That is fine. Know what you are agreeing to, and then write it like a person who has read the fine print. The stamp is waiting. The column is hungry. You still get to decide how much of yourself you pour into the ink.""",
]

BEATS: list[tuple[str, str, str]] = [
    (
        "0000-last-name-box",
        "You fill a box that says last name.",
        "Round-head stickman filling a form with a huge box labeled LAST NAME, MS Paint, white background.",
    ),
    (
        "0008-clipboard",
        "A nurse with a clipboard wants it before she looks at your face.",
        "Stick nurse, clipboard covering a stick patient's face, MS Paint.",
    ),
    (
        "0016-no-box",
        "For most of history that box did not exist.",
        "Empty form with the last-name box crossed out, confused stickman, MS Paint.",
    ),
    (
        "0024-shouted-name",
        "You had a name people shouted across a field.",
        "Two stickmen in a field, a speech bubble with a first name only, MS Paint.",
    ),
    (
        "0032-not-soul",
        "Your last name is not a soul. It is a column.",
        "A soul doodle with a red X, a spreadsheet column labeled NAME, MS Paint.",
    ),
    (
        "0042-column-like-blood",
        "You have been treating the column like blood.",
        "Spreadsheet dripping a red drop into a family tree, MS Paint.",
    ),
    (
        "0052-which-john",
        "Everyone knew which John you meant.",
        "Three stick Johns with labels MILLER, OAK, SON, MS Paint.",
    ),
    (
        "0106-pointer-not-heirloom",
        "The extra word was a pointer, not an heirloom.",
        "A pointing arrow vs a fancy trophy, stickman choosing the arrow, MS Paint.",
    ),
    (
        "0120-could-change",
        "It could change if you moved or took a new job.",
        "Stickman walking, name tags swapping MILLER to HILL, MS Paint.",
    ),
    (
        "0134-iceland",
        "Iceland still names children as someone's child, not a logo.",
        "Simple map labeled ICELAND, a child stickman tagged SON OF, MS Paint.",
    ),
    (
        "0148-dropdown",
        "You cannot put a relationship in a dropdown menu.",
        "A website dropdown eating a family hug, error face, MS Paint.",
    ),
    (
        "0204-norman-elites",
        "After the Norman conquest, elites already liked extra names.",
        "Crown stickman with a long name banner, peasant with one word, MS Paint.",
    ),
    (
        "0220-tax-lists",
        "By the thirteen hundreds, tax lists stuffed with bynames.",
        "Long scroll of names, a tax collector stickman, 1300s, MS Paint.",
    ),
    (
        "0236-poll-tax",
        "Poll taxes needed heads you could write twice.",
        "Two years, same stickman, two different name tags, collector crying, MS Paint.",
    ),
    (
        "0252-smith-ghost",
        "Smith becomes a ghost for children who never touched a hammer.",
        "Stick child at a laptop labeled SMITH, rusty hammer far away, MS Paint.",
    ),
    (
        "0310-joseph-second",
        "Seventeen eighty seven: Joseph the Second orders fixed Jewish family names.",
        "Emperor stickman, edict 1787, families receiving name stamps, MS Paint.",
    ),
    (
        "0328-leash-index",
        "When a government names your family, it is building an index.",
        "Giant card index, families as file cards on a leash, MS Paint.",
    ),
    (
        "0344-napoleon-book",
        "Napoleon's civil books wanted one string that does not wander.",
        "Big registration book, Napoleon hat stickman, wandering names with a red X, MS Paint.",
    ),
    (
        "0402-turkey-1934",
        "Nineteen thirty four: Turkey's Surname Law. Everyone picks a last name.",
        "Calendar 1934, stamp SURNAME LAW, stick family choosing a word, MS Paint.",
    ),
    (
        "0420-ataturk",
        "Mustafa Kemal took Ataturk. Ordinary people took what an official would stamp.",
        "Official stickman with a stamp, family holding name cards, MS Paint.",
    ),
    (
        "0436-banned-words",
        "Some names were banned for being too foreign or too tribal.",
        "Name cards with forbidden red circles, MS Paint.",
    ),
    (
        "0452-living-memory",
        "Some families still remember the afternoon they chose the word.",
        "Old and young stickmen at a table choosing letters, MS Paint.",
    ),
    (
        "0510-form-first",
        "Your last name is who you are to a form. The form came first.",
        "A giant form standing in front of a tiny stickman, MS Paint.",
    ),
    (
        "0526-china-clans",
        "China had hereditary clan names for a very long time, a different older technology.",
        "Simple clan banner and a counting stick official, label CHINA, MS Paint.",
    ),
    (
        "0542-ask-neighbor",
        "Who is this man? Ask his neighbor. Then: look at the line.",
        "Two panels: asking a neighbor, then pointing at a list, MS Paint.",
    ),
    (
        "0558-box-is-census",
        "You type it as if the box were a mirror. It is a census.",
        "Form box vs a census taker with a tally, MS Paint.",
    ),
    (
        "0614-name-confesses",
        "Baker, Hill, Johnson. The words still confess the old pointer.",
        "Three stickmen labeled BAKER HILL JOHNSON with tiny icons loaf hill son, MS Paint.",
    ),
    (
        "0630-miller-cannot",
        "A Miller who cannot mill. Bureaucracy winning.",
        "Stickman labeled MILLER at a desk, mill with a red X, MS Paint.",
    ),
    (
        "0646-cake-and-child",
        "You print it on a cake and teach a child to spell it.",
        "Birthday cake with a long last name, child stickman copying letters, MS Paint.",
    ),
    (
        "0702-pride-shame",
        "The box produces pride, shame, escape, belonging.",
        "Form box radiating four emoji-like doodles: crown, cloud, door, flag, MS Paint.",
    ),
    (
        "0718-search-query",
        "Your last name is now a query.",
        "Search bar eating a last name, stranger stickmen assembling a file, MS Paint.",
    ),
    (
        "0734-email-number",
        "Your email is your name plus a number because someone else got there first.",
        "Email address with a 14 at the end, two stickmen arguing, MS Paint.",
    ),
    (
        "0750-weight-is-useful",
        "It is heavy because it is useful to institutions.",
        "Last-name rock labeled USEFUL, government building sitting on it, MS Paint.",
    ),
    (
        "0810-findable",
        "We traded being known in a place for being findable in a system.",
        "Village handshake vs a barcode on a stickman, MS Paint.",
    ),
    (
        "0826-genealogy-web",
        "The string follows you into genealogy websites.",
        "Grave and a website family tree sharing the same label, MS Paint.",
    ),
    (
        "0842-index-not-joke",
        "A letter can find a widow. The index is not only a joke.",
        "Envelope reaching a stick widow, a small pause face, MS Paint.",
    ),
    (
        "0900-family-older",
        "Family is older than the last name. The last name invited family into the ledger.",
        "Hug labeled FAMILY, arrow into a ledger book, MS Paint.",
    ),
    (
        "0920-type-the-box",
        "You type the box and feel like you are telling the truth.",
        "Stickman typing LAST NAME, a thought bubble TRUTH with a tiny question mark, MS Paint.",
    ),
    (
        "1000-handle-not-blood",
        "Put your finger on the letters. That is a handle, not blood.",
        "Finger on form letters, blood drop with a red X, handle tag, MS Paint.",
    ),
    (
        "1030-stamp-callback",
        "Look at the blank like a stamp. Someone needed a column.",
        "Callback: the same LAST NAME box, a clerk stamp, empty until agreed, MS Paint.",
    ),
]


def main() -> None:
    draft = DraftScript(
        title="Why Your Last Name Was Invented By A Clerk",
        description=(
            "You type last name like it is blood. It is a column. Village nicknames, "
            "English poll taxes, Joseph the Second, Turkey's nineteen thirty four Surname Law. "
            "Family is older than the form."
        ),
        tags=(
            "surname",
            "last name",
            "history",
            "census",
            "identity",
            "names",
            "family",
            "why",
            "bureaucracy",
            "clerk",
        ),
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=tuple(
            DraftVisualBeat(slug=slug, prompt=prompt, covers=covers)
            for slug, covers, prompt in BEATS
        ),
        thumbnail_hook="LAST NAME?",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Your Last Name Was Invented By A Clerk",
        language="en",
        voice="en-US-GuyNeural",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 23, tzinfo=UTC),
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    named = PROJECT_ROOT / "senaryo-paint-surnames.json"
    write_scenario(scenario, out)
    write_scenario(scenario, named)
    print(scenario.project_id)
    print(out)
    print("chapters", len(scenario.scenes), "beats", len(scenario.video.visual_beats))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))


if __name__ == "__main__":
    main()

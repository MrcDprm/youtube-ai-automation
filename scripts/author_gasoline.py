"""Author Badly Drawn Why: Why Your Car Still Drinks Dead Plants (Zenn path)."""

from __future__ import annotations

from datetime import UTC, datetime

from config.constants import PAINT_PLACEHOLDER_SEARCH_TERMS, PROJECT_ROOT
from modules.interfaces import DraftScene, DraftScript
from modules.scenario_builder import build_paint_scenario, write_scenario

TERMS = PAINT_PLACEHOLDER_SEARCH_TERMS

CHAPTERS = [
    """Tonight you will stand at a pump and watch a number climb. The hose is cold. The smell is familiar enough that your brain files it under normal. You will not think about what you are buying. You will think about the price, the card, the click when the handle locks. Here is the part that should bother you. The liquid in that hose is mostly ancient sunlight trapped inside dead things that sank to the bottom of a sea before your species learned to stand upright. Kerosene lamps. A waste pit. A river that caught fire because a refinery needed somewhere to put the part nobody wanted. Then a German engineer built a reliable four-stroke engine, and a Michigan factory learned to stamp cars like cans, and the trash became the main product. Your tank is not futuristic. It is a nineteenth-century leftover with a credit card reader glued on. You still pump it. The pump is cheerful. That is its job.""",
    """Start with the lamp, because the car came second and the trash came first. In eighteen fifty-nine, Edwin Drake drilled near Titusville in Pennsylvania and proved you could pull crude oil out of the ground on purpose. Refiners did not want crude oil because it was pretty. They wanted what you could distill out of it for light. Kerosene replaced whale oil in lamps. Whale oil was expensive, morally awkward, and smelled like a lawsuit. Kerosene was a product with a receipt. Gasoline, the lighter volatile fraction that came off the same still, was the nuisance. It evaporated. It stank. It caught fire if you looked at it wrong. Refinery men called it essence, then gasoline, and treated it like a leak with ambition. Some burned it in pits to get rid of it. Some let it run into creeks. Chronicles from the early oil fields describe ground around refineries soaked in the stuff and barrels of unwanted spirit floating away. The industry’s star product was illumination. The car was not a customer yet. The customer was a wick.""",
    """Named dates, because a myth of inevitability is how a waste product gets a halo. In eighteen seventy-six, Nikolaus Otto patented a practical four-stroke internal combustion engine in Germany. The engine did not care about your feelings. It cared about a fuel that vaporized fast and burned in a controlled bang. Gasoline was already sitting in refinery yards being treated like a raccoon in the kitchen. In eighteen eighty-six, Karl Benz received a patent for a motor car powered by gasoline. In the United States, Charles and Frank Duryea built an early gasoline automobile in eighteen ninety-three. John Froelich made a gasoline tractor in eighteen ninety-two. These were curiosities, not a grid. Horses still made sense. Trains still made sense. Lamp oil still paid the bills. What changed was not a single inventor moment. It was volume. More engines, more cars, more demand for the fraction refiners used to throw away. Market incentives, which is a polite phrase for we finally found a buyer for the trash.""",
    """Watch kerosene lose the argument, because electric light did not kill the night. It killed the receipt. Thomas Edison’s practical electric lighting spread through cities in the eighteen eighties and eighteen nineties. Kerosene lamps did not vanish overnight, but the growth curve for lamp fuel stopped being the whole story. Refineries that had been built around light now had tanks of light nobody needed as much and tanks of vapor nobody had enough buyers for. The U.S. Energy Information Administration’s history of gasoline notes that early refiners discarded gasoline when distilling for kerosene and only later treated it as valuable once automobiles existed. By nineteen sixteen, gasoline production in the United States surpassed kerosene production. That is not a footnote. That is the pivot. The main product became the by-product. The by-product became the reason we paved the continent. If your pump feels permanent, notice it is younger than the light it replaced.""",
    """This is the rehook. You think gasoline is transportation the way gravity is gravity. It is a packaging decision from an era that wanted lamps. Crude oil is a soup of hydrocarbons. A refinery is a sorting machine. Different boiling points become different products. Gasoline sits in the light, volatile end of the sort. Diesel sits heavier. Bitumen sits heavier still and becomes road. Your car runs on the fraction that used to be the one refiners could not wait to evict. Octane ratings, tetraethyl lead, catalytic crackers, all of that is later engineering to make the trash behave in millions of cylinders. I am not giving you a chemistry lecture. I am pointing at the category error. You call it fuel. The nineteenth century called it nuisance. Both can be true in the same hose.""",
    """Ford is where the leftover stops being funny and starts being infrastructure. In nineteen eight, the Ford Motor Company began selling the Model T. Mass production at Highland Park turned the automobile from a rich person’s toy into a middle-class appliance. More cars meant more gasoline burned, which meant more crude pulled, which meant more refineries tuned to favor the light fractions. Service stations spread. Pipelines spread. The map learned to follow the tank. None of this required you to understand geology. It required you to want to go farther than a horse on a Tuesday. The tank became a habit. Habits feel like nature when they are old enough. Your habit is barely more than a century old wearing a hundred-million-year-old ingredient list.""",
    """This is you, already, in the middle of the story. You drive or you do not, but you live inside the world the fraction built. Asphalt is another petroleum sort. Plastics are another. The pump is the most honest interface because it shows you the swap in one handle. You pay for dead plants compressed by time, refined by heat, moved by pipe, stored in an underground tank, metered in gallons. The meter is calm. The calm is how a legacy product stays in the century without introducing itself. You can feel both in the same smell: convenience, and the faint absurdity that the valuable part started as the part they burned in pits. Convenience wins. It usually does. The win is not proof the story is elegant.""",
    """A city is a pile of combustion permissions with buildings attached. That sentence is rude and almost fair. Take gasoline away and the grocery truck stops, the ambulance changes math, the suburb becomes a thought experiment. The fuel is entangled. That entanglement is why the leftover survived every obituary. Electric cars are not a plot twist in this essay. They are the next sorting decision. The point is narrower. You were told the pump was progress in liquid form. Often it was waste that found a market. Waste can be useful and still be waste in origin. Refineries still crack heavy molecules to make more light ones because the light ones are what the grid drinks. The grid is you, and the hose, and the number climbing while you stare at your phone.""",
    """So what did we keep? We kept a nineteenth-century sorting outcome and painted it green with marketing when marketing arrived. We kept a fuel that won because engines multiplied faster than lamp wicks. We kept underground tanks, spill law, octane wars, lead that fixed knocking and caused a different problem, unleaded, reformulated, ethanol blends, all of it layered on top of the same ancient plankton brew. The layers are real fixes. The brew is still old. Tonight when you smell the handle, that smell is not the future. It is a refinery answer to a lamp-age question that the car hijacked. You are allowed to need the tank. You are allowed to want something cleaner and still pull in. Just stop calling the liquid inevitable, or pure progress, or unrelated to the part they used to dump in the creek. Look at the pump like a museum label that forgot to mention it started as trash. The label is cheerful. The trash is the point. Drive when you must. Know what century your tank is still paying rent to.""",
]

DESCRIPTION = (
    "You pump a familiar liquid and call it normal. Gasoline began as the unwanted, "
    "volatile fraction from kerosene refining—burned, dumped, and ignored until Otto’s "
    "engine and Ford’s Model T turned waste into infrastructure. This is why your tank "
    "still drinks dead plants."
)

TAGS = (
    "gasoline",
    "petroleum",
    "kerosene",
    "Ford Model T",
    "history",
    "cars",
    "refining",
    "energy",
    "why essay",
    "badly drawn why",
)


def main() -> None:
    draft = DraftScript(
        title="Why Your Car Still Drinks Dead Plants",
        description=DESCRIPTION,
        tags=TAGS,
        scenes=tuple(
            DraftScene(narration=chapter.strip(), search_terms=TERMS) for chapter in CHAPTERS
        ),
        visual_beats=(),
        thumbnail_hook="DEAD PLANTS",
    )
    scenario = build_paint_scenario(
        draft,
        topic="Why Your Car Still Drinks Dead Plants",
        language="en",
        voice="en-US-GuyNeural",
        tts_rate="-8%",
        minutes=11,
        target_seconds=660.0,
        now=datetime(2026, 8, 28, tzinfo=UTC),
        use_zenn=True,
    )
    out = PROJECT_ROOT / "senaryo-paint.json"
    write_scenario(scenario, out)
    print(scenario.project_id)
    print(out)
    print("zenn", scenario.video.is_zenn)
    print("chapters", len(scenario.scenes))
    print("chars", sum(len(scene.narration) for scene in scenario.scenes))


if __name__ == "__main__":
    main()

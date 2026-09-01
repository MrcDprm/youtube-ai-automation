---
name: after-hours-file
description: Produce a full After Hours File YouTube package — one researched closed-file mystery, illustrated night stills, slow TTS, thumbnail, Studio pack. Use only when brands/active.json id is after-hours-file.
---

# After Hours File — full package

The operator never draws, never narrates, never writes title/description/thumbnail. They only upload the MP4, the JPEG, and paste Studio text.

Do not wait for a second prompt to start stills or TTS.

Active brand must be `after-hours-file` in `brands/active.json`. Do not make a Badly Drawn Why episode.

## Pipeline (every video)

1. Write the English spoken file yourself (~9–11 minutes, mid-roll floor 8). One case. Ollama is optional sketch only; do not ship a thin draft.
2. Split into 8–10 chapters for TTS. Invent unique visual beats at **one still every ~10 seconds** (`slug`, `covers`, `prompt`) — **about 60** for a 10-minute file (`file_beat_count(600) == 60`), not 132 stickman cuts.
3. Write the scenario with `build_file_scenario` / `senaryo-file.json`. Voice `en-GB-RyanNeural`, rate `-12%`. If that voice is missing, `en-GB-ThomasNeural` at the same rate.
4. Generate 16:9 illustrated night stills (ChatGPT Image 2) into `output/storyboard/<project_id>/` as `NN-slug.png` plus `thumbnail.png` (dark cover, pale 3–5 word hook, **not** yellow, not the full title).
5. `python main.py run --scenario senaryo-file.json --no-upload`
6. Deliver `output/final/<id>.mp4`, `output/thumbnails/<id>.jpg`, `output/studio/<id>/STUDIO.txt`.

Target narration about 8500–9500 characters. Confirm duration 9–11 minutes ±45 seconds.

## Essay shape

One closed file. Named witness, place, year. Cold open in the location at night, not in "you". Open loop by ~0:50: the file did not close. Separate claim from evidence. Do not declare a ghost. Do not mock the witness. Close on what the folder still cannot answer. Spell years and big numbers as words. No "welcome back", "in this video", or subscribe ask.

Do not clone Bedtime Stories titles, characters, or their exact cases-as-packaged. Do not remake Badly Drawn Why object-history essays.

## Drawings

16:9, painterly night illustration, mud-green / charcoal / weak yellow lamp. Fog, empty room, map, folder, distant silhouette, one story / one palette. Slow Ken Burns.

Never: MS Paint stickman, light-blue torso, yellow thumbnail hook, photoreal portraits of real people, national flags, gore, graphic harm to children.

GenerateImage `aspect_ratio` 16:9. Images land in Cursor `assets/`. Copy **only** TSV-matching beat names into the project storyboard folder. After still 01 exists, use it as `reference_image_paths`. Copy `thumbnail.png` into the new project folder immediately.

## Never

- YouTube API upload
- Pexels on these stills
- Asking the operator to draw, narrate, or write title/description/thumbnail
- Using `senaryo-paint.json` or GuyNeural for this brand

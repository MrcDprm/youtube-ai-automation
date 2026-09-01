---
name: badly-drawn-why
description: Produce a full Badly Drawn Why YouTube package — English essay, timestamps, MS Paint stills, TTS, thumbnail, Studio pack. One episode per «yeni video», then stop. Use only when brands/active.json id is badly-drawn-why.
---

# Badly Drawn Why — full package

The operator never draws, never narrates, never writes title/description/thumbnail. They only upload the MP4, the JPEG, and paste Studio text.

Do not wait for a second prompt to start stills or TTS. Do wait for the next «yeni video» before starting another episode.

Active brand must be `badly-drawn-why` in `brands/active.json`. Do not make Drawn Anyway or After Hours File.

## One episode, then stop

«yeni video» (or an equivalent produce request) means **one** episode from the next unshipped topic in `scenarios/topics-paint.json`. Skip any entry whose `guidance` starts with `SHIPPED`. Do not remake those. Do not skip ahead.

After the three delivery files exist: mark that topic `SHIPPED YYYYMMDD`, hand the paths to the operator in Turkish, **then stop**. Do not start the next topic. Do not chain.

## Promise

English **why essay**. Second person. One object, habit, or system — including **cars** and **historical objects/systems**. Stickman. Named facts. Humor at the leftover logistics, not at a person or a group. Not a textbook recap. Not a closed-file ghost story. Not a Drawn Anyway one-true-event cartoon. Not Oversimplified.

## Research and harm

Research from named sources. Do not invent quotes, dates, or kill counts. Spell years and big numbers as words.

Humor lands on the **system or object**, never on a person, nationality, religion, disability, illness, or the injured. No gore, corpses, child-victim closeups, crash closeups, drowning, or national flags as the joke. No medical or legal advice. No hate. YouTube altered/synthetic: yes.

## Pipeline (every video)

1. Author the English spoken essay yourself (~11 minutes). Ollama `generate --format paint` is an optional sketch only; rewrite until it holds a viewer.
2. Split into chapters for TTS. Add **~132 visual beats** (one every five seconds) with MS Paint prompts.
3. Generate **132 sixteen-by-nine MS Paint stills** plus `thumbnail.png` into `output/storyboard/<project_id>/`. Name them `NN-mmss-slug.png` to match `visual_beats`.
4. Write the paint scenario (`build_paint_scenario` / `senaryo-paint.json`, `use_zenn=False`). Voice `en-US-GuyNeural`, rate `-8%`. Set `thumbnail_hook` (yellow 2–4 words). Never Ink. Never `senaryo-drawn.json`.
5. `python main.py run --scenario senaryo-paint.json --no-upload` — Ken Burns stills, standard ASS captions.
6. Deliver `output/final/<id>.mp4`, `output/thumbnails/<id>.jpg`, `output/studio/<id>/STUDIO.txt`.

## Essay shape

Cold open in `you` (0:00–0:20). Open loop by 0:50. Named people/places/numbers. Rehook ~3:15. "This is you" ~6:30–9:00. Close the loop. Callback to the opening image. Spell years and big numbers as words. No subscribe ask in the hook. No "welcome back" / "in this video".

## Drawings

White background, beginner MS Paint, wobbly thick black outlines, round-head stickman, flat colors, no 3D, no realistic humans, no anime, 16:9. No candy-mascot Ink. No photoreal logos. Keep titles and labels in the **middle 75%** of the frame (not flush to the top edge) so Ken Burns zoom does not clip text.

## Never

- YouTube API upload
- Pexels on paint
- Copying another channel's exact titles
- Asking the operator to draw, narrate, or write title/description/thumbnail
- Mixing Drawn Anyway cartoon stills or After Hours File night stills into this package
- Starting the next topic after a ship unless the operator asked for another video

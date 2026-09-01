---
name: drawn-anyway
description: Produce a full Drawn Anyway YouTube package — one researched true story, cartoon mascot, punchy English, thumbnail, Studio pack. One episode per «yeni video», then stop. Use only when brands/active.json id is drawn-anyway.
---

# Drawn Anyway — full package

The operator never draws, never narrates, never writes title/description/thumbnail. They only upload the MP4, the JPEG, and paste Studio text.

Do not wait for a second prompt to start stills, clips, or TTS. Do wait for the next «yeni video» before starting another episode.

Active brand must be `drawn-anyway` in `brands/active.json`. Do not make Badly Drawn Why or After Hours File.

Read `brands/drawn-anyway-lock.json` for the locked mascot STYLE. Higgsfield voice ids in that file are leftover; do not spend credits unless the operator explicitly tops up.

## One episode, then stop

«yeni video» (or an equivalent produce request) means **one** episode from the next unshipped topic in `scenarios/topics-drawn.json`. Skip any entry whose `guidance` starts with `SHIPPED`. Do not remake those. Do not skip ahead.

After the three delivery files exist and duration is inside 8:00–11:00: mark that topic `SHIPPED YYYYMMDD`, hand the paths to the operator in Turkish, **then stop**. Do not start the next topic. Do not chain.

## Promise

One true event. Cartooned. Punchline. A question in the last twenty seconds for comments. Not a textbook recap. Not a closed-file ghost story. Not a stickman "why object" essay.

## Pipeline (every video)

1. Research the event from named sources. Do not invent quotes, dates, or kill counts. Spell years and big numbers as words. No "welcome back", "in this video", or subscribe ask.
2. Write spoken chapters that land **8:00–11:00** of Edge TTS (mid-roll floor is 8:00). Aim the middle of the band, about 9–10 minutes. **N stills ≈ minutes × 6** at a 10-second cadence (48 at 8:00, up to **66** at 11:00).
3. Group chapters into Studio timestamps (about one chapter per minute).
4. Write `build_drawn_scenario` / `senaryo-drawn.json`. Stamp Drawn Anyway on the scenario. Default Edge voice is `en-AU-WilliamNeural` at `+4%`, fallback `en-US-GuyNeural`. **Voice, rate, subtitle font size, and caption colour may change per episode.** Never `en-GB-RyanNeural`. Never stickman. Never Pexels.
5. Produce pictures that match the locked mascot STYLE (see lock file). Never MS Paint stickman. Never mud-green archive night.
6. Higgsfield explainer only if the operator has paid credits and asks. Otherwise ship cartoon stills + Ken Burns + Edge TTS the same day.
7. Thumbnail: bold cartoon, 3–4 word hook, not AHF-dark, not the full title.
8. Deliver `output/final/<id>.mp4`, `output/thumbnails/<id>.jpg`, `output/studio/<id>/STUDIO.txt`. Same three files as Badly Drawn Why. Do not invent a new upload or schedule workflow.

Confirm duration is **inside 8:00–11:00**. If TTS lands under 8:00, lengthen chapters and re-run (do not ship 7:xx). Then stop.

## Higgsfield explainer (when credits allow)

Gemini Omni Flash is about **24–30 credits per 10-second clip**. An 8-minute film is **48 clips ≈ 1,150–1,450 credits**, plus ~0.6 credit per `seed_audio` take and 2 credits for a style-key refresh.

Only take this path when `higgsfield account status` shows enough credits for **N clips + N takes + assemble** and the operator asked for it. Workspace must already be selected.

1. Attach the locked style-key image (job id in the lock file) to every clip.
2. Generate **N** `seed_audio` takes with locked voice **Fraser** (`voice_type=preset`, id in the lock file). One line per block. No stage directions.
3. Generate **N** `gemini_omni` (or cheaper `kling3_0_turbo` if Omni is unaffordable) 16:9 clips. Clip audio is ambience only — no dialogue, no lip-sync, mouth closed on the mascot.
4. Assemble with `explainer_video` if that job type exists; otherwise concatenate in order (sandbox or local ffmpeg), 10 seconds per block.
5. Copy the MP4 into `output/final/`. Write Studio chapters at 0:00, 1:00, …

Do not auto-pick a new mascot. Operator already delegated the Ink lock.

## Credit shortfall (same-day ship)

If credits are below the Omni floor, or the operator said zero Higgsfield spend:

1. Generate 16:9 cartoon stills (ChatGPT Image 2 or Nano Banana) into `output/storyboard/<project_id>/` as `NN-slug.png` plus `thumbnail.png`. Same prompt quality as always. After still 01 exists, use it as `reference_image_paths`.
2. **One unique still per 10-second beat.** Never hold or reuse a drawing across two beats. Cadence stays the same; do not pad runtime by stretching one image.
3. Generate in parallel batches of **6–8** (not 4) to save wall-clock time. If a 429 hits, drop to 4 and continue. Copy **only** TSV-matching beat names into the storyboard folder — never the whole Cursor `assets/` directory.
4. `python main.py run --scenario senaryo-drawn.json --no-upload`. Ken Burns workers are 8; keep encode `preset` medium and the same CRF. Do not switch to `veryfast` to save minutes.

This is still Drawn Anyway: punchy picture changes, stronger Ken Burns (`zoom` 1.16). It is not After Hours File.

## Captions

One fill colour per episode. Do **not** set `accent_color` (it alternates every cue and is hard to watch). `numeral_display` is on: TTS may still say "nineteen seventy"; the burn-in should show `1970`, `45 feet`, `8 tons`. Leave small prose counts as words (`three men`).

## Essay shape

Cold open on the stupid true detail, not "you". Named people, place, year by ~0:40. Open loop: the official plan was going to work. Rehook ~3:00. Punchline is logistics, not cruelty. Close on the leftover fact plus a comment question.

Never: gore, photoreal portraits, national flags as the joke, child-victim closeups, cloning Oversimplified / TheOdd1sOut titles, Bedtime Stories packaging, or Badly Drawn Why object history.

## Drawings

16:9, bold cartoon storytime, thick ink outlines, flat candy fills (mustard, ink-blue, cream paper, tomato red), paper grain. Recurring mascot **Ink**: mustard jacket, ink-blue hair, oversized marker, mouth closed, readable silhouette.

Never: stickman, light-blue torso, photoreal faces, flags as identity, gore, graphic harm.

## Never

- YouTube API upload
- Pexels on these stills
- Asking the operator to draw, narrate, or write title/description/thumbnail
- Using `senaryo-paint.json`, `senaryo-file.json`, or RyanNeural for this brand
- Mixing a new "delivery system" into the package; hand off the same three files every time
- Starting the next topic after a ship unless the operator asked for another video

---
name: every-level-pov
description: Produce a full Every Level POV YouTube package — evergreen football/sport rank progression, cartoon Kit protagonist, thumbnail, Studio pack. One episode per «yeni video», then stop. Use only when brands/active.json id is every-level-pov.
---

# Every Level POV — full package

The operator never draws, never narrates, never writes title/description/thumbnail. They only upload the MP4, the JPEG, and paste Studio text.

Do not wait for a second prompt to start stills, clips, or TTS. Do wait for the next «yeni video» before starting another episode.

Active brand must be `every-level-pov` in `brands/active.json`. Do not make Badly Drawn Why, After Hours File, or Drawn Anyway.

Read `brands/every-level-pov-lock.json` for the locked protagonist **Kit** STYLE. Read `brands/every-level-pov-channel.json` for channel copy. Channel assets live in `brands/assets/every-level-pov/`.

## One episode, then stop

«yeni video» means **one** episode from the next unshipped topic in `scenarios/topics-pov.json`. Skip `SHIPPED` entries. Do not skip ahead.

After the three delivery files exist and duration is **inside 12:00–26:00** (pilot aim ~14:00): mark the topic `SHIPPED YYYYMMDD`, hand paths in Turkish, **then stop**.

## Promise

First-person rank progression. Cartoon POV. Each level gets environment, money pressure, and one vivid detail. Close with a comment question. Not a true-crime story. Not stickman essay. Not World Cup-only branding — evergreen football and sport.

## Pipeline (every video)

1. Research ranks from real football structure (Sunday league, academy, reserves, leagues, Champions League). No invented transfer fees as fact; use plausible ranges and label uncertainty. Spell years as words in TTS. No "welcome back", subscribe ask, or "in this video".
2. Write **12–17 rank chapters** landing **12:00–26:00** Edge TTS. Pilot default **14:00**. **N stills = minutes × 6** at 10-second cadence (72 at 12:00, 84 at 14:00, up to **156** at 26:00).
3. Studio chapters ≈ one rank per timestamp.
4. `build_pov_scenario` → `senaryo-pov.json`. Voice `en-US-GuyNeural` at `+2%`, fallback `en-US-ChristopherNeural`. Never RyanNeural. Never stickman. Never Pexels.
5. Stills: Kit POV cartoon, 16:9, reference `brands/every-level-pov-kit.png` after beat 01 exists.
6. Thumbnail: Kit + **red** 3–4 word hook (not full title).
7. Deliver `output/final/<id>.mp4`, `output/thumbnails/<id>.jpg`, `output/studio/<id>/STUDIO.txt`.

If TTS **under 12:00**, lengthen ranks and re-run. Do not ship short.

## Stills workflow

1. Run or extend `scripts/author_pov_*.py` → `senaryo-pov.json` + `output/storyboard/<id>/beats.tsv`
2. Generate 16:9 stills into `output/storyboard/<project_id>/` as `NN-slug.png` + `thumbnail.png`
3. **One unique still per 10-second beat.** After still 01, pass Kit reference on every call.
4. Parallel batches of **6–8**; on 429 drop to 4.
5. `python scripts/sync_paint_stills.py --scenario senaryo-pov.json` (or copy matching beats to `output/clips/`)
6. `python main.py run --scenario senaryo-pov.json --no-upload`

Ken Burns zoom **1.16**. `preset` medium. Do not use `veryfast`.

## Captions

White fill, dark stroke. Do **not** set `accent_color`. `numeral_display` on for scores, fees, capacities in captions.

## Script shape

Cold open hook in second person. Rank 1 = lowest (park kickabout). Each rank: where you play, what you earn, what breaks you, one sensory detail. Rehook mid-video. Final rank = highest in the episode topic. Close: "Which level are you stuck at?" style comment hook.

Never: gore, photoreal faces, national flags as identity, racist crowd scenes, child exploitation, World Cup as channel name.

## Drawings

Kit: young adult, green hoodie, thick ink outlines, mouth closed, readable silhouette. Pitch green, stadium amber, cream paper, tomato red accents. First-person POV hands/feet in frame when useful.

Never: Ink mascot, MS Paint stickman, After Hours File dark archive, photoreal, Pexels.

## Never

- YouTube API upload
- Mixing brands in one episode
- Asking the operator to draw, narrate, or write Studio fields
- Chaining a second topic after ship unless asked

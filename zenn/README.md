# Zenn (free sidecar)

Stick-cut renderer for Badly Drawn Why: Edge TTS word timings → ~2s programmatic beats → ffmpeg assembly.

Claude’s Remotion / ElevenLabs stack is not used. Speech timings come from the existing
Edge TTS `WordBoundary` stream (`modules.tts.EdgeTTSEngine` → `WordCue`).

## Free stack

| Step | Tool |
| --- | --- |
| Voice | Edge TTS (`en-US-GuyNeural` or whatever the scenario already uses) |
| Beats | `zenn.segmentation.cues_to_beats` on real word timestamps |
| Pose / background | `zenn/config/pose-rules.json` keywords, then optional callable fallback |
| Frames | Pillow compose (`zenn/visuals`) + bundled SVG assets |
| Encode | `MoviePyEditor.build_zenn_story` — ffmpeg hold clips + karaoke ASS |
| Thumbnail | `zenn/render/thumbnail.py` — black field, yellow hook |

No paid image API, no voice cloning, no photoreal faces.

## Beat window

From `zenn/config/style.json`:

- Minimum hold **1.0s** (no flicker). A trailing clip shorter than this is merged into the previous beat.
- Target **2.2s**.
- Maximum **4.0s**, except a single word whose own duration already exceeds 4s (documented in tests).

Cuts prefer sentence endings (`.!?…`), otherwise the target duration.

## Visual assets

- **12 poses** — `visuals/assets/poses/*.svg` (standing, running, scared, …)
- **6 backgrounds** — `visuals/assets/backgrounds/*.svg` (garage, road, factory, office, old_city, cave)
- Palette: black `#000000`, white `#FFFFFF`, accent `#FFD600`

Regenerate SVG files: `python zenn/visuals/svg_assets.py`

## Pipeline hook

When `video.story_visual.zenn_enabled` is true (default for new Badly Drawn Why scenarios from
`build_paint_scenario`), `VideoPipeline` skips MS Paint still fetch and calls `_stage_zenn_assemble`.

Legacy 132 ChatGPT stills remain available with `use_zenn=False` in the author script.

## Python

```python
from modules.interfaces import WordCue
from zenn.segmentation import cues_to_beats

beats = cues_to_beats(word_cues)
```

Each `Beat` has `start_ms`, `end_ms`, `text`, `visual_prompt`, `pose_tag`, `bg_tag`.

```bash
.venv/Scripts/python.exe -m pytest tests/test_zenn_segmentation.py tests/test_zenn_phase2.py
```

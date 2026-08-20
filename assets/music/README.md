# Background music

Drop a licensed audio file here and point `video.background_music.file` at it in
`senaryo.json`, then set `video.background_music.enabled` to `true`.

```json
"background_music": {
  "enabled": true,
  "file": "assets/music/ambient_loop.mp3",
  "volume": 0.08,
  "fade_in_seconds": 1.5,
  "fade_out_seconds": 2.5,
  "duck_to": 0.5
}
```

## How the mix works

The track is looped to the full video length, scaled to `volume`, faded in and out, and
**ducked** to `volume * duck_to` for every span where narration is playing. Ducking is a
deterministic gain envelope computed from the known scene timeline, not a sidechain
compressor, so the result is identical on every run.

Keep `volume` low. `0.08` means 8% amplitude, which sits under a voice track without
fighting it. Anything above `0.20` will bury the narration.

## Where to find free-to-use music

| Source | Notes |
| --- | --- |
| [YouTube Audio Library](https://studio.youtube.com/channel/UC/music) | Free for YouTube; check per-track attribution requirements |
| [Free Music Archive](https://freemusicarchive.org/) | Mixed licenses, filter by CC |
| [Incompetech](https://incompetech.com/music/royalty-free/) | CC BY, attribution required |
| [Pixabay Music](https://pixabay.com/music/) | Pixabay Content License |

## Licensing warning

Music is the single most common cause of Content ID claims and copyright strikes. A claim can
demonetize or block a video worldwide even when the pipeline itself did nothing wrong.

- Confirm the license permits use in monetized video **before** rendering.
- If the license requires attribution, put it in `youtube.description` yourself. The pipeline
  auto-appends stock **footage** credits, but it cannot know your music's terms.
- "Free to download" is not the same as "free to use in a monetized YouTube video".

Audio files are gitignored and never committed.

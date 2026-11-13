# Background gameplay

Long gameplay recordings for videos that set `video.background_video`. Git ignores everything in
this folder except this file: recordings are large, and they belong to whoever recorded them.

## GTA 5 Shorts

`python main.py generate --format gta` and `VIDEO_FORMAT=gta` read from `assets/background/gta5/`,
or from the folder `GTA_BACKGROUND_DIR` in `.env` names.

- Use footage you recorded yourself. Ten minutes or more per file gives every Short a stretch that
  no other Short has used.
- Driving, flying and walking through the city sit well behind captions. Leave out menus, loading
  screens and cutscenes.
- The game's own sound is muted in GTA Shorts, because the in-game radio plays licensed songs.
- mp4, mkv, mov, webm and m4v files are read. Horizontal footage works too: every frame is
  cropped to 9:16.

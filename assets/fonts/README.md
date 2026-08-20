# Fonts

MoviePy 2.x renders text with Pillow, which needs a **real font file path** — there is no
system-font-name lookup and no ImageMagick involved. Every burned-in subtitle and every
thumbnail title therefore requires a `.ttf` (or `.otf`) in this folder.

## Default font

The project default is **`Inter-Bold.ttf`**, referenced by:

- `DEFAULT_FONT` in `.env`
- `subtitles.font` in `senaryo.json`

## Getting it automatically (recommended)

```bash
python main.py doctor --fix
# or
make font
```

This downloads an SIL Open Font License font into this folder. It first tries the official
Inter release and extracts the static `Inter-Bold.ttf`; if that is unavailable it falls back to
`Anton-Regular.ttf`, a heavy condensed display face that works well for short-form captions.

## Getting it manually

Drop any `.ttf`/`.otf` here and point `subtitles.font` at it. Good free options:

| Font | License | Source |
| --- | --- | --- |
| Inter | SIL OFL 1.1 | <https://github.com/rsms/inter/releases> |
| Anton | SIL OFL 1.1 | <https://fonts.google.com/specimen/Anton> |
| Bebas Neue | SIL OFL 1.1 | <https://fonts.google.com/specimen/Bebas+Neue> |
| Montserrat | SIL OFL 1.1 | <https://fonts.google.com/specimen/Montserrat> |

## Resolution order

`utils.fs.resolve_font()` never crashes on a missing file. It tries, in order, and warns on
every fallback:

1. The exact path configured in the scenario.
2. The same filename inside `assets/fonts/`.
3. Any other `.ttf`/`.otf` already in `assets/fonts/`.
4. A platform font scan (Windows `C:\Windows\Fonts`, macOS `/System/Library/Fonts`,
   Linux `/usr/share/fonts`).

Only when all four fail does it raise `FontNotFoundError`.

## Licensing

Fonts are **not** committed to this repository. Check the license of whatever you drop here
before publishing videos that use it. All fonts listed above are OFL and safe for commercial
video use; the OFL only restricts selling the font files themselves.

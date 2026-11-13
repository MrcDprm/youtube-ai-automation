# Scenario queue

This folder is the daily production inbox. `python main.py daily` looks here before it
asks the script model for a new script.

```
scenarios/
├── topics.json          # subjects to generate from, in order
├── topics.example.json  # a copy you can restore
├── inbox/               # drop a finished senaryo.json here to skip generation for a day
├── processing/          # claimed by a run that is currently rendering (gitignored)
├── done/                # successfully rendered (gitignored)
└── failed/              # render or generation failed; the topic is NOT consumed (gitignored)
```

## How a day is chosen

1. If a video already succeeded *today*, `daily` exits without doing anything (`--force` overrides).
2. Otherwise the oldest `inbox/*.json` wins. Dropping a file is how you override the model.
3. Otherwise the next unused topic in `topics.json` is generated, then rendered.
4. A missed day (the PC was off) produces **one** video the next time the command runs, never
   a burst of five. YouTube's default quota is about six uploads per day.

Uploading stays off unless you pass `--upload` or set `DAILY_UPLOAD=true` in `.env`. Generated
files are still `privacy_status: private`.

## Topic list format

A string:

```json
["Kahvenin dünyaya yayılışı"]
```

or an object, when a topic needs extra steering:

```json
{
  "topics": [
    {
      "topic": "Yapay zekanın kısa tarihi",
      "scenes": 10,
      "guidance": "Merak uyandırıcı, abartısız.",
      "language": "tr"
    }
  ]
}
```

Used topics are recorded in `.cache/scheduler/state.json`, not in this file, so you can edit
the list without losing history.

## GTA 5 Shorts

`topics-gta.json` holds checked GTA 5 facts for `generate --format gta` and for `daily` with
`VIDEO_FORMAT=gta`. Each entry carries a `fact`, which the script may only reword, and the
`sources` it was checked against:

```json
{
  "topic": "Fort Zancudo'ya izinsiz girmek",
  "fact": "Hikaye modunda üsse karadan izinsiz girer ve askerlere görünürsen hemen 4 yıldız aranma seviyesi alırsın.",
  "sources": [
    {"title": "Grand Theft Wiki: Fort Zancudo", "url": "https://www.grandtheftwiki.com/Fort_Zancudo"}
  ]
}
```

Add a fact only after two independent pages agree on it, and write its numbers as digits: a
script that uses a number the fact does not give is sent back for a rewrite. The sources are
copied into the scenario file for review and are never spoken or published.

`python main.py topics --gta` lists the facts with their numbers, and
`python main.py generate --format gta 3` writes the third one.

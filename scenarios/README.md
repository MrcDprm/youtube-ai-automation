# Scenario queue

This folder is the daily production inbox. `python main.py daily` looks here before it
asks Ollama for a new script.

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

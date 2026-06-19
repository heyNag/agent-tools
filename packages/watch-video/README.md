# watch-video

`watch-video` is a local video inspection package for agents. It turns a URL or
local video into a small bundle of evidence:

- metadata
- focused audio clip
- transcript JSON and Markdown
- optional frames
- a concise report

It is designed for local use by Claude, Codex, and similar tools. The package is
the source of truth for the skill, command prompts, helper scripts, and plugin
metadata.

## Requirements

```sh
brew install yt-dlp ffmpeg jq
```

Set `GROQ_API_KEY` for Whisper fallback:

```sh
export GROQ_API_KEY="..."
export GROQ_MODEL="whisper-large-v3-turbo"
```

## Quickstart

```sh
python3 scripts/watch.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --duration 30 \
  --frames \
  --frame-interval 5
```

Focused local examples:

```sh
python3 scripts/watch.py ./screen-recording.mov --start 00:15 --end 00:45 --frames
python3 scripts/watch.py "$URL" --transcriber none --frame-interval 10
```

Outputs are written under `.watch-video/runs/<run-id>/` by default.

## Files

```text
SKILL.md              # skill instructions for local agents
commands/             # command prompts
scripts/watch.py      # orchestration CLI
scripts/groq_transcribe.py
scripts/extract_frames.py
plugin/plugin.json
tests/
```

# agent-tools

Personal agent tooling for local skills, commands, plugins, and future MCP
servers.

This repository is intentionally practical and file-first. Local packages live
under `packages/` and are the source of truth for skills, commands, plugin
metadata, and helper scripts. MCP projects live under `mcp/` as deployable
server shapes that can be developed later without turning this repository into
an MCP gateway.

## Current Package

### watch-video

`watch-video` helps Claude, Codex, and other local agents inspect videos:

- YouTube and other `yt-dlp` supported URLs
- local videos and screen recordings
- tutorials, product demos, and UI bug videos
- native captions when available
- Groq Whisper fallback when captions are missing
- focused ranges with `--start`, `--end`, or `--duration`
- optional frame extraction with `ffmpeg`

## Requirements

On macOS:

```sh
brew install yt-dlp ffmpeg jq
```

Python 3.11+ is recommended. Node.js is only needed for the placeholder MCP
server under `mcp/watch-video`.

## Groq Setup

Set a Groq key in your shell or copy `.env.example` to `.env` and source it in
your preferred way:

```sh
export GROQ_API_KEY="..."
export GROQ_MODEL="whisper-large-v3-turbo"
```

The helper scripts never print the API key.

## Try a 30-second YouTube Scan

```sh
python3 packages/watch-video/scripts/watch.py \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --duration 30 \
  --frames \
  --frame-interval 5
```

The run artifacts are written under `.watch-video/runs/<run-id>/`, including
`metadata.json`, `audio.mp3`, transcript files, extracted frames, and
`report.md`.

## Install Locally

Install into Claude local folders:

```sh
./scripts/install-claude.sh
```

Install into Codex local folders:

```sh
./scripts/install-codex.sh
```

Install both:

```sh
./scripts/install-all.sh
```

These scripts are idempotent. The repo remains the source of truth; installed
files are copies for local agent runtimes.

## Groq Smoke Test

```sh
./scripts/test-groq.sh path/to/audio.mp3
```

This checks `GROQ_API_KEY`, calls Groq Whisper with
`whisper-large-v3-turbo` by default, and pretty prints with `jq` when available.

## Repo Structure

```text
packages/
  watch-video/
    SKILL.md              # local skill contract
    commands/             # agent command prompts
    scripts/              # Python helpers
    plugin/               # future Claude Code plugin metadata
    tests/                # Python tests

mcp/
  watch-video/
    src/index.ts          # minimal MCP server skeleton
    Dockerfile            # deployable later

scripts/
  install-claude.sh
  install-codex.sh
  install-all.sh
  test-groq.sh
```

## Future MCP Path

`mcp/watch-video` currently exposes a small `watch_video_status` tool. It is a
deployable placeholder for a future MCP server that can wrap the local
`watch-video` scripts. It is not a gateway and does not integrate video
processing yet.

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

## Quickstart

Install local dependencies on macOS:

```sh
brew install yt-dlp ffmpeg jq
```

Set a Groq key for Whisper fallback:

```sh
export GROQ_API_KEY="..."
export GROQ_MODEL="whisper-large-v3-turbo"
```

Run a 30-second YouTube scan. Quote URLs in zsh so `?` is not treated as a glob:

```sh
python3 packages/watch-video/scripts/watch.py \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --duration 30 \
  --frames \
  --frame-interval 5
```

Install into Claude and Codex:

```sh
./scripts/install-all.sh
```

The run artifacts are written under `.watch-video/runs/<run-id>/`, including
`metadata.json`, `audio.mp3`, transcript files, extracted frames, and
`report.md`.

The helper scripts never print the API key. CI does not require `GROQ_API_KEY`.

## Requirements

Python 3.11+ is recommended. Node.js is only needed for the placeholder MCP
server under `mcp/watch-video`.

## Install Locally

Preview the install without writing to local agent folders:

```sh
DRY_RUN=1 ./scripts/install-all.sh
```

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
files are copies for local agent runtimes. Installers only replace files or
directories marked as `agent-tools` managed; set `FORCE=1` only after inspecting
any existing unmanaged target.

## Groq Smoke Test

```sh
./scripts/test-groq.sh path/to/audio.mp3
```

This checks `GROQ_API_KEY`, calls Groq Whisper with
`whisper-large-v3-turbo` by default, and pretty prints with `jq` when available.

## Common Commands

```sh
make test
make install
make install-dry-run
make groq-test AUDIO=path/to/audio.mp3
make mcp-build
```

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

## Next Roadmap

- Better transcript/caption fallback and language selection.
- Prettier reports with clearer visual evidence tables.
- Real MCP tools for status, metadata inspection, and safe local job launching.
- Optional deployment to Railway later, once the MCP API surface is real.

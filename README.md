# agent-tools

`agent-tools` is a collection of agent tools, skills, commands, plugins, helper
scripts, and future MCP servers.

The current public tool is `watch-video`, a local video inspection package for
short clips, tutorials, demos, screen recordings, and UI bug videos.

## Install For Claude Code

```text
/plugin marketplace add heyNag/agent-tools
/plugin install watch-video@heynag-agent-tools
```

## Install For Codex Or Generic Skills

```sh
git clone https://github.com/heyNag/agent-tools.git
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/watch-video
cp -R agent-tools/codex/watch-video ~/.codex/skills/watch-video
```

## Local Development Install

```sh
./scripts/install-all.sh
```

## Requirements

```sh
brew install yt-dlp ffmpeg jq
```

Groq is optional but useful when captions are missing:

```sh
export GROQ_API_KEY="..."
export GROQ_MODEL="whisper-large-v3-turbo"
```

Default Groq model: `whisper-large-v3-turbo`.

## Quick Test

```sh
python3 packages/watch-video/scripts/watch.py \
  "https://www.youtube.com/watch?v=DTCyvo6cC54" \
  --duration 30 \
  --frames \
  --frame-interval 10 \
  --max-frames 4
```

## Repo Structure

```text
packages/             source of truth for tools
plugins/              Claude Code publishable plugins
codex/                Codex and generic skill packages
mcp/                  future deployable MCP servers
docs/                 project memory and agent orientation
scripts/              build, install, test, and helper scripts
.github/workflows/    CI
```

Future tools should follow this pattern:

- `packages/<name>/tool.json`
- `plugins/<name>` when the tool targets Claude Code
- `codex/<name>` when the tool targets Codex or generic skills
- `mcp/<name>` only when an MCP server is needed

There is no MCP gateway for now.

## Docs

Start with [docs/README.md](docs/README.md).

Future agents should read `docs/README.md`, `docs/architecture.md`, and
`docs/agent-guidelines.md` before making structural changes.

## Security

Do not commit real API keys, `.env.local`, `.watch-video/` artifacts, media
files, transcripts, frames, caches, or local build outputs. Keep CI no-secret and
free of live Groq/video/Claude requirements. See [docs/security.md](docs/security.md).

## Checks

```sh
make test
make syntax
make mcp-build
make build-packages
make verify-packages
```

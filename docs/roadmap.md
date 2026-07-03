# Roadmap

This roadmap is directional. It is not a commitment to overbuild the repo.

## Phase 1: Source-Only Skills

Maintain the current source-only package shape:

```text
packages/<name>
packages/<name>/skills/<name>
```

Keep `watch-video`, `codex-reset-credit`, `x-bookmarks`, and
`chatgpt-pro-review` easy to install in Claude Code, Codex, Cursor, Claude
Desktop custom skills, OpenCode, and optional Skillshare.

## Phase 2: Better Reports And Fallbacks

Mostly delivered: `watch-video` now probes captions before downloading,
collapses rolling-caption duplication, picks frames by scene change or
keyframe with near-duplicate removal and a detail dial, chunks Whisper audio
past the upload cap, pins transcript-cue frames, and stores Whisper keys once.
Remaining: richer visual report summaries and deeper caption-fallback
diagnostics.

## Phase 3: Richer Agent Ergonomics

Improve commands, install docs, target mapping, and troubleshooting. Keep local
installed copies downstream of package source.

## Phase 4: Real MCP Tools, If Needed

There is no MCP folder today. If a real agent workflow needs server-side tools,
add a focused `mcp/<name>` folder with actual tools, tests, and deployment docs.
For `watch-video`, possible future tools could include `video_info`,
`video_analyze`, `video_watch`, and `video_detail`.

## Phase 5: Optional Deployment

If useful, make a future `mcp/<name>` server deployable to Railway or a similar
platform. Deployment should build on an independent MCP folder shape, not on a
gateway.

## Phase 6: More Charms

Add more packages only when they have a clear local workflow or agent need. New
packages should follow `docs/adding-a-skill.md`.

## MCP Gateway Constraint

Do not add an MCP gateway, router, proxy, or shared MCP control plane unless the
user explicitly asks for it.

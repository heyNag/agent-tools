# Architecture

`agent-tools` is a public source-only workspace for agent skills, Claude Code
plugins, optional Skillshare discovery, and helper scripts.

## Repo Shape

```text
packages/             source packages and Claude Code plugin roots
.claude-plugin/       Claude Code marketplace catalog
skillshare-hub.json   optional Skillshare hub index
.dist/                ignored local build artifacts
scripts/              install, build, test, and release helpers
.github/workflows/    CI and manual skill release workflow
docs/                 orientation and project memory
```

There is no committed `generated/` directory.

## Packages

Current packages:

```text
packages/watch-video
packages/codex-reset-credit
packages/x-bookmarks
```

Each package is directly consumable as a Claude Code plugin source and contains
a portable skill folder:

```text
packages/<name>/skills/<name>
```

Package manifests live at:

```text
packages/<name>/tool.json
packages/<name>/.claude-plugin/plugin.json
```

## Distribution

Public install surfaces consume source paths:

```text
Claude Code       -> packages/<name>
Codex             -> packages/<name>/skills/<name>
OpenCode/generic  -> packages/<name>/skills/<name>
Skillshare hub    -> packages/<name>/skills/<name>
Claude Desktop    -> .dist/claude/custom-skills/<name> built locally
```

The root `.claude-plugin/marketplace.json` is generated from package manifests
and points to `./packages/<name>`. `skillshare-hub.json` is generated from
`tool.json`, `.claude-plugin/plugin.json`, and skill frontmatter, and points to
`packages/<name>/skills/<name>`.

Run:

```sh
make build-packages
make public-check
```

## MCP

There is no MCP server in the repo today. If a future skill needs real MCP
tools, add a focused `mcp/<name>` folder in that change and document how it is
deployed and tested.

Do not add an MCP gateway, router, proxy, or shared MCP control plane unless
explicitly requested.

There is also no global session-start bootstrap today. Current packages are
task/domain tools invoked by users, native skill discovery, or agent judgment.

## Source Of Truth

Edit source paths:

```text
packages/<name>/
scripts/
docs/
```

Installed copies, `.dist/` artifacts, local auth state, and run artifacts are
not source of truth.

# Architecture

`agent-tools` is a personal agent tooling workspace for local skills, commands,
plugins, helper scripts, and future MCP servers.

The current shape is intentionally small:

```text
packages/             local skills, commands, and Claude/Codex-facing packages
plugins/              generated Claude Code plugin packages, committed for public install
codex/                generated Codex/generic skill packages, committed for public install
mcp/                  deployable MCP server shapes, one folder per MCP server
scripts/              install, test, sync, and helper scripts
.github/workflows/    CI
docs/                 orientation and project memory
```

## Packages

`packages/` is for local agent-facing source of truth. Packages can include
skills, commands, plugin metadata, helper scripts, and tests.

The current package is:

```text
packages/watch-video
```

`packages/watch-video` owns the local `watch-video` skill, commands, plugin
metadata, Python scripts, and tests. Edit source files there first.

Each public package should declare its distribution targets in:

```text
packages/<name>/tool.json
```

For now, the only public package is `watch-video`.

## Public Distribution

`plugins/` and `codex/` are generated from `packages/`, but they are committed as
public install targets so users and agents do not need to understand the source
workspace layout.

```text
plugins/<name>        Claude Code plugin package
codex/<name>          Codex/generic skill package
```

Do not manually edit generated public outputs during normal development. Edit
`packages/<name>` first, then run:

```sh
make build-packages
make verify-packages
```

Future packages should follow the same manifest pattern:

- `packages/<name>/tool.json` declares `public`, `targets`, and whether an MCP
  placeholder exists.
- `plugins/<name>` exists only when the package targets Claude Code.
- `codex/<name>` exists only when the package targets Codex or generic skills.
- `mcp/<name>` exists only when the package needs an MCP server shape.

## MCP

`mcp/` is for deployable MCP server shapes. Each MCP server should live in its
own folder and be independently buildable and deployable later, ideally with its
own `Dockerfile`.

The current MCP placeholder is:

```text
mcp/watch-video
```

It is a minimal TypeScript MCP server skeleton. It currently exposes a status
tool only. It does not wrap video processing yet.

## No Gateway

There is no MCP gateway for now. Do not add a gateway, router, proxy, or shared
MCP control plane unless explicitly requested. Keep MCP folders independently
understandable and deployable.

## Source Of Truth

Repo source paths are authoritative:

- Edit packages under `packages/`.
- Regenerate public outputs under `plugins/` and `codex/` from packages.
- Edit MCP server source under `mcp/`.
- Edit install and test helpers under `scripts/`.
- Edit project memory under `docs/`.

Install scripts copy repo source into local Claude/Codex folders. Those installed
copies are runtime copies, not source of truth. Do not manually edit installed
copies and treat them as canonical. Change the repo source and rerun the install
script instead.

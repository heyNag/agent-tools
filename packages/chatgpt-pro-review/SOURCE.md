# Source Package

This directory is the source of truth and Claude Code plugin root for
`chatgpt-pro-review`.

Edit files here first:

- `skills/chatgpt-pro-review/SKILL.md`
- `skills/chatgpt-pro-review/agents/`
- `commands/`
- `.claude-plugin/plugin.json`
- `README.md`
- `SOURCE.md`
- `tests/`
- `tool.json`

After changing package source, run:

```sh
make build-packages
make public-check
```

Install targets consume source directly:

```text
Claude Code marketplace source  -> packages/chatgpt-pro-review
Codex skill source              -> packages/chatgpt-pro-review/skills/chatgpt-pro-review
Cursor plugin source            -> skills/chatgpt-pro-review symlink
OpenCode/generic skill source   -> packages/chatgpt-pro-review/skills/chatgpt-pro-review
Skillshare hub source           -> packages/chatgpt-pro-review/skills/chatgpt-pro-review
Claude Desktop local artifact   -> .dist/claude/custom-skills/chatgpt-pro-review
```

`.dist/` artifacts are local build outputs and must not be committed.

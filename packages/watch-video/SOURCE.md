# Source Package

This directory is the source of truth for `watch-video`.

Edit files here first:

- `SKILL.md`
- `README.md`
- `commands/`
- `plugin/plugin.json`
- `scripts/`
- `tests/`
- `tool.json`

After changing package source, run:

```sh
make build-packages
make verify-generated-clean
```

The public install copies under `plugins/watch-video` and `codex/watch-video`
are generated from this directory.

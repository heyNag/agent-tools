<!-- BEGIN GENERATED FROM SOURCE: packages/codex-reset-credit/README.md -->
<!-- Do not edit directly; edit the source path and run make rebuild-generated. -->
<!-- END GENERATED FROM SOURCE -->

# codex-reset-credit

`codex-reset-credit` is a read-only local skill for checking Codex reset-credit
status and local Codex rate-limit reset windows.

It can:

- call the live Codex/ChatGPT reset-credit endpoint using local Codex auth
- read local Codex session snapshots for rate-limit reset windows
- print a concise text report
- emit sanitized JSON with `--json`
- run local-only with `--no-live`

It must never print tokens, account IDs, raw auth file contents, or edit local
Codex files.

## Source And Generated Outputs

Source lives under:

```text
packages/codex-reset-credit
```

Public install targets are generated from that source into:

```text
generated/claude/plugins/codex-reset-credit
generated/codex/skills/codex-reset-credit
```

Edit source first, then run:

```sh
make rebuild-generated
make verify-generated-clean
```

## Usage

From this package directory:

```sh
python3 scripts/check_reset_credits.py
```

Useful options:

```sh
python3 scripts/check_reset_credits.py --json
python3 scripts/check_reset_credits.py --no-live
python3 scripts/check_reset_credits.py --thread-id <thread-id>
python3 scripts/check_reset_credits.py --session-file <absolute-path-to-rollout.jsonl>
python3 scripts/check_reset_credits.py --timezone UTC
```

## Evidence Boundary

- Reset-credit data comes from the live Codex/ChatGPT backend endpoint.
- Rate-limit windows come from local Codex session `token_count` events.
- Local session snapshots may be stale if Codex has not emitted recent usage
  events.

## Files

```text
SKILL.md                         # skill instructions for agents
scripts/check_reset_credits.py   # read-only helper CLI
commands/codex-reset-credit.md   # Claude command prompt
plugin/plugin.json               # Claude plugin metadata
tests/                           # offline helper tests
```

The helper was ported from Nag's local dotfiles skill at
`/Users/nag/.dotfiles/ai/skills/codex-reset-credit`.

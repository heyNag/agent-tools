#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PACKAGE="${1:-watch-video}"
SRC="$ROOT/packages/$PACKAGE"
PLUGIN="$ROOT/plugins/$PACKAGE"
CODEX="$ROOT/codex/$PACKAGE"

fail() {
  echo "error: $*" >&2
  exit 1
}

check_same_file() {
  local source_file="$1"
  local generated_file="$2"
  [[ -f "$source_file" ]] || fail "missing source file: ${source_file#$ROOT/}"
  [[ -f "$generated_file" ]] || fail "missing generated file: ${generated_file#$ROOT/}"
  if ! cmp -s "$source_file" "$generated_file"; then
    echo "mismatch: ${generated_file#$ROOT/} differs from ${source_file#$ROOT/}" >&2
    return 1
  fi
}

check_same_dir() {
  local source_dir="$1"
  local generated_dir="$2"
  [[ -d "$source_dir" ]] || return 0
  [[ -d "$generated_dir" ]] || fail "missing generated directory: ${generated_dir#$ROOT/}"
  python3 - "$ROOT" "$source_dir" "$generated_dir" <<'PY'
import filecmp
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
source_dir = pathlib.Path(sys.argv[2])
generated_dir = pathlib.Path(sys.argv[3])
ignored_dirs = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def files_under(directory: pathlib.Path) -> dict[str, pathlib.Path]:
    files: dict[str, pathlib.Path] = {}
    for path in directory.rglob("*"):
        if any(part in ignored_dirs for part in path.parts):
            continue
        if path.is_file():
            files[str(path.relative_to(directory))] = path
    return files


source_files = files_under(source_dir)
generated_files = files_under(generated_dir)
errors: list[str] = []

for rel in sorted(set(source_files) - set(generated_files)):
    errors.append(f"missing generated file: {generated_dir.relative_to(root) / rel}")
for rel in sorted(set(generated_files) - set(source_files)):
    errors.append(f"unexpected generated file: {generated_dir.relative_to(root) / rel}")
for rel in sorted(set(source_files) & set(generated_files)):
    if not filecmp.cmp(source_files[rel], generated_files[rel], shallow=False):
        errors.append(
            f"mismatch: {generated_dir.relative_to(root) / rel} differs from "
            f"{source_dir.relative_to(root) / rel}"
        )

if errors:
    for error in errors:
        print(error, file=sys.stderr)
    raise SystemExit(1)
PY
}

[[ -d "$SRC" ]] || fail "missing source package: packages/$PACKAGE"

status=0

check_same_file "$SRC/README.md" "$CODEX/README.md" || status=1
check_same_file "$SRC/SKILL.md" "$CODEX/SKILL.md" || status=1
check_same_dir "$SRC/scripts" "$CODEX/scripts" || status=1
[[ -f "$CODEX/GENERATED.md" ]] || {
  echo "missing generated marker: codex/$PACKAGE/GENERATED.md" >&2
  status=1
}

check_same_file "$SRC/README.md" "$PLUGIN/README.md" || status=1
check_same_file "$SRC/SKILL.md" "$PLUGIN/skills/$PACKAGE/SKILL.md" || status=1
check_same_file "$SRC/plugin/plugin.json" "$PLUGIN/.claude-plugin/plugin.json" || status=1
check_same_dir "$SRC/scripts" "$PLUGIN/skills/$PACKAGE/scripts" || status=1
check_same_dir "$SRC/commands" "$PLUGIN/commands" || status=1
[[ -f "$PLUGIN/GENERATED.md" ]] || {
  echo "missing generated marker: plugins/$PACKAGE/GENERATED.md" >&2
  status=1
}

if [[ "$status" -ne 0 ]]; then
  echo "generated outputs are out of sync; run make build-packages" >&2
  exit "$status"
fi

echo "generated outputs match packages/$PACKAGE"

#!/usr/bin/env bash
set -euo pipefail

PACKAGE="${1:-watch-video}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/packages/$PACKAGE"
TOOL_JSON="$SRC/tool.json"
OUT="$ROOT/plugins/$PACKAGE"

fail() {
  echo "error: $*" >&2
  exit 1
}

case "$PACKAGE" in
  ""|*[!A-Za-z0-9._-]*)
    fail "invalid package name: $PACKAGE"
    ;;
esac

json_public() {
  python3 - "$TOOL_JSON" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)
print("true" if data.get("public") is True else "false")
PY
}

json_has_target() {
  python3 - "$TOOL_JSON" "$1" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)
targets = data.get("targets") or []
print("true" if sys.argv[2] in targets else "false")
PY
}

copy_dir() {
  local source_dir="$1"
  local dest_dir="$2"
  mkdir -p "$dest_dir"
  cp -R "$source_dir"/. "$dest_dir"/
  find "$dest_dir" \( -name "__pycache__" -o -name ".pytest_cache" -o -name ".venv" -o -name "node_modules" -o -name "dist" \) -prune -exec rm -rf {} +
  find "$dest_dir" -name ".DS_Store" -delete
}

[[ -f "$TOOL_JSON" ]] || fail "missing package manifest: $TOOL_JSON"
[[ "$(json_public)" == "true" ]] || {
  echo "skip: $PACKAGE is not public"
  exit 0
}
[[ "$(json_has_target claude)" == "true" ]] || {
  echo "skip: $PACKAGE does not target claude"
  exit 0
}

[[ -f "$SRC/SKILL.md" ]] || fail "missing required file: $SRC/SKILL.md"
[[ -d "$SRC/scripts" ]] || fail "missing required directory: $SRC/scripts"
[[ -f "$SRC/plugin/plugin.json" ]] || fail "missing required file: $SRC/plugin/plugin.json"
[[ -f "$SRC/README.md" ]] || fail "missing required file: $SRC/README.md"
[[ -f "$ROOT/LICENSE" ]] || fail "missing required file: $ROOT/LICENSE"

rm -rf "$OUT"
mkdir -p "$OUT/.claude-plugin" "$OUT/skills/$PACKAGE"

cp "$SRC/SKILL.md" "$OUT/skills/$PACKAGE/SKILL.md"
copy_dir "$SRC/scripts" "$OUT/skills/$PACKAGE/scripts"

if [[ -d "$SRC/commands" ]]; then
  copy_dir "$SRC/commands" "$OUT/commands"
fi

cp "$SRC/plugin/plugin.json" "$OUT/.claude-plugin/plugin.json"
cp "$SRC/README.md" "$OUT/README.md"
cp "$ROOT/LICENSE" "$OUT/LICENSE"

echo "built Claude plugin: plugins/$PACKAGE"

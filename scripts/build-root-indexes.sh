#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail() {
  echo "error: $*" >&2
  exit 1
}

json_public() {
  python3 - "$1" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)
print("true" if data.get("public") is True else "false")
PY
}

reset_symlink_dir() {
  local dir="$1"
  mkdir -p "$dir"
  find "$dir" -mindepth 1 -maxdepth 1 -type l -delete
}

ensure_safe_index_dir() {
  local dir="$1"
  mkdir -p "$dir"
  local unsafe
  unsafe="$(find "$dir" -mindepth 1 -maxdepth 1 ! -type l ! -name "README.md" -print)"
  if [[ -n "$unsafe" ]]; then
    echo "$unsafe" >&2
    fail "${dir#$ROOT/} contains non-symlink entries; remove or move them before rebuilding indexes"
  fi
}

skill_index="$ROOT/skills"
command_index="$ROOT/commands"

ensure_safe_index_dir "$skill_index"
ensure_safe_index_dir "$command_index"
reset_symlink_dir "$skill_index"
reset_symlink_dir "$command_index"

shopt -s nullglob
for tool_json in "$ROOT"/packages/*/tool.json; do
  package="$(basename "$(dirname "$tool_json")")"
  package_dir="$ROOT/packages/$package"

  if [[ "$(json_public "$tool_json")" != "true" ]]; then
    continue
  fi

  skill_dir="$package_dir/skills/$package"
  [[ -f "$skill_dir/SKILL.md" ]] || fail "missing source skill: ${skill_dir#$ROOT/}/SKILL.md"
  ln -s "../packages/$package/skills/$package" "$skill_index/$package"

  if [[ -d "$package_dir/commands" ]]; then
    for command_file in "$package_dir"/commands/*.md; do
      [[ -f "$command_file" ]] || continue
      command_name="$(basename "$command_file")"
      if [[ -e "$command_index/$command_name" || -L "$command_index/$command_name" ]]; then
        fail "duplicate command name in root command index: $command_name"
      fi
      ln -s "../packages/$package/commands/$command_name" "$command_index/$command_name"
    done
  fi
done
shopt -u nullglob

echo "built root skill/command indexes: skills/ commands/"

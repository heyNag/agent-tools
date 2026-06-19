#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
package_dir="${repo_root}/packages/watch-video"
skill_target="${HOME}/.codex/skills/watch-video"

run() {
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    printf '[dry-run]'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

tmp_target="${skill_target}.tmp.$$"

run rm -rf "${tmp_target}"
run mkdir -p "${tmp_target}"
run cp "${package_dir}/SKILL.md" "${tmp_target}/SKILL.md"
run cp -R "${package_dir}/scripts" "${tmp_target}/scripts"
run rm -rf "${skill_target}"
run mv "${tmp_target}" "${skill_target}"

echo "Installed watch-video for Codex:"
echo "  skill: ${skill_target}"

#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
package_dir="${repo_root}/packages/watch-video"
skill_target="${HOME}/.claude/skills/watch-video"
commands_target="${HOME}/.claude/commands"

run() {
  if [[ "${DRY_RUN:-0}" == "1" ]]; then
    printf '[dry-run]'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

copy_skill() {
  local tmp_target
  tmp_target="${skill_target}.tmp.$$"

  run rm -rf "${tmp_target}"
  run mkdir -p "${tmp_target}"
  run cp "${package_dir}/SKILL.md" "${tmp_target}/SKILL.md"
  run cp -R "${package_dir}/scripts" "${tmp_target}/scripts"
  run rm -rf "${skill_target}"
  run mv "${tmp_target}" "${skill_target}"
}

copy_commands() {
  run mkdir -p "${commands_target}"
  for command_file in "${package_dir}"/commands/*.md; do
    run cp "${command_file}" "${commands_target}/$(basename "${command_file}")"
  done
}

copy_skill
copy_commands

echo "Installed watch-video for Claude:"
echo "  skill: ${skill_target}"
echo "  commands: ${commands_target}"

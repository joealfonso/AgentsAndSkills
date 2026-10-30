#!/usr/bin/env bash
# Draw skills and agents out of this repo without the plugin system.
#
#   scripts/skills.sh list                 show every skill and agent
#   scripts/skills.sh link <name>|all      symlink into ~/.claude/skills or ~/.claude/agents (edits here go live)
#   scripts/skills.sh unlink <name>|all    remove symlinks that point back into this repo
#   scripts/skills.sh zip <name>           build dist/<name>.zip for uploading to claude.ai (Settings > Capabilities > Skills)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_HOME="${CLAUDE_HOME:-$HOME/.claude}/skills"
AGENTS_HOME="${CLAUDE_HOME:-$HOME/.claude}/agents"
HOOKS_HOME="${CLAUDE_HOME:-$HOME/.claude}/hooks"
AGENT_HOOK="$ROOT/plugins/dev-team/hooks/agent_hook.py"

skill_dirs() { find "$ROOT/plugins" -path '*/skills/*/SKILL.md' -exec dirname {} \; | sort; }
agent_files() { find "$ROOT/plugins" -path '*/agents/*.md' | sort; }

find_item() {
  local name="$1"
  for d in $(skill_dirs); do [[ "$(basename "$d")" == "$name" ]] && { echo "skill $d"; return; }; done
  for f in $(agent_files); do [[ "$(basename "$f" .md)" == "$name" ]] && { echo "agent $f"; return; }; done
  echo "No skill or agent named '$name'. Try: scripts/skills.sh list" >&2; exit 1
}

link_one() {
  local kind="$1" path="$2" dest
  if [[ "$kind" == skill ]]; then mkdir -p "$SKILLS_HOME"; dest="$SKILLS_HOME/$(basename "$path")"
  else mkdir -p "$AGENTS_HOME"; dest="$AGENTS_HOME/$(basename "$path")"; fi
  if [[ -e "$dest" && ! -L "$dest" ]]; then echo "skip $dest (a real file is already there)"; return; fi
  ln -sfn "$path" "$dest"; echo "linked $dest"
  if [[ "$kind" == agent ]]; then  # the agents' frontmatter hook looks for it here
    mkdir -p "$HOOKS_HOME"; ln -sfn "$AGENT_HOOK" "$HOOKS_HOME/agent_hook.py"
  fi
}

unlink_one() {
  local kind="$1" path="$2" dest
  [[ "$kind" == skill ]] && dest="$SKILLS_HOME/$(basename "$path")" || dest="$AGENTS_HOME/$(basename "$path")"
  if [[ -L "$dest" && "$(readlink "$dest")" == "$ROOT"/* ]]; then rm "$dest"; echo "unlinked $dest"; fi
}

case "${1:-list}" in
  list)
    echo "Skills:"
    for d in $(skill_dirs); do
      plugin="$(basename "$(dirname "$(dirname "$d")")")"
      printf "  %-32s %s\n" "$(basename "$d")" "($plugin)"
    done
    echo "Agents:"
    for f in $(agent_files); do printf "  %s\n" "$(basename "$f" .md)"; done
    ;;
  link|unlink)
    [[ $# -ge 2 ]] || { echo "usage: $0 $1 <name>|all" >&2; exit 1; }
    fn="${1}_one"
    if [[ "$2" == all ]]; then
      for d in $(skill_dirs); do "$fn" skill "$d"; done
      for f in $(agent_files); do "$fn" agent "$f"; done
    else
      item="$(find_item "$2")"; read -r kind path <<<"$item"; "$fn" "$kind" "$path"
    fi
    ;;
  zip)
    [[ $# -ge 2 ]] || { echo "usage: $0 zip <skill-name>" >&2; exit 1; }
    item="$(find_item "$2")"; read -r kind path <<<"$item"
    [[ "$kind" == skill ]] || { echo "'$2' is an agent; only skills can be zipped" >&2; exit 1; }
    mkdir -p "$ROOT/dist"; rm -f "$ROOT/dist/$2.zip"
    (cd "$(dirname "$path")" && zip -qr "$ROOT/dist/$2.zip" "$2" -x '*.DS_Store')
    echo "built dist/$2.zip"
    ;;
  *) sed -n '2,8p' "$0"; exit 1 ;;
esac

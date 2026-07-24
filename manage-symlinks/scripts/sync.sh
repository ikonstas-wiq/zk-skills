#!/usr/bin/env bash
#
# sync.sh — link every skill in this repo into a skills search path.
#
# Source of truth: this repo (work-skills). Each top-level directory that
# contains a SKILL.md is symlinked into the Claude Code skills directory
# (~/.claude/skills) as <target>/<name> -> <repo>/<name>.
#
# Scope: ~/.claude/skills ONLY. This skill deliberately does not touch
# ~/.agents/skills, ~/.codex/skills, or any other search path.
#
# Safe by default: never clobbers a real directory/file that isn't ours —
# it warns and skips unless --force is given (which moves the conflict aside).
#
# Usage:
#   sync.sh [--dry-run] [--force] [--prune]
#
#   --dry-run      Show what would change; make no changes
#   --force        Move an aside a conflicting real path, then link
#   --prune        Remove stale symlinks in target that point into this repo
#                  but whose source skill no longer exists
#
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET="${HOME}/.claude/skills"   # fixed: Claude Code skills path only
DRY_RUN=0; FORCE=0; PRUNE=0

# Top-level directories that are NOT active skills. Templates now live inside a
# skill's own examples/ folder (not as top-level dirs), so this is empty; kept
# as a hook for any future scaffold that does sit at the top level.
EXCLUDE=( )

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --force) FORCE=1; shift ;;
    --prune) PRUNE=1; shift ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

is_excluded() { local n="$1"; [ ${#EXCLUDE[@]} -eq 0 ] && return 1; for e in "${EXCLUDE[@]}"; do [ "$n" = "$e" ] && return 0; done; return 1; }
run() { if [ "$DRY_RUN" = 1 ]; then echo "  DRY: $*"; else eval "$@"; fi; }

mkdir -p "$TARGET"
CONFLICT_DIR="/workspace/Temp/manage-symlinks-conflicts"

echo "repo:   $REPO"
echo "target: $TARGET"
[ "$DRY_RUN" = 1 ] && echo "(dry-run — no changes)"
echo

created=0; updated=0; ok=0; conflict=0; pruned=0

for dir in "$REPO"/*/; do
  name="$(basename "$dir")"
  [ -f "$dir/SKILL.md" ] || continue          # only real skills
  is_excluded "$name" && continue
  desired="$REPO/$name"
  link="$TARGET/$name"

  if [ -L "$link" ]; then
    current="$(readlink "$link")"
    if [ "$current" = "$desired" ]; then
      ok=$((ok+1)); continue
    fi
    echo "UPDATE  $name  (was -> $current)"
    run "rm '$link'"; run "ln -s '$desired' '$link'"; updated=$((updated+1))
  elif [ -e "$link" ]; then
    if [ "$FORCE" = 1 ]; then
      echo "CONFLICT(force) $name  — moving real path aside"
      run "mkdir -p '$CONFLICT_DIR'"; run "mv '$link' '$CONFLICT_DIR/$name'"
      run "ln -s '$desired' '$link'"; updated=$((updated+1))
    else
      echo "CONFLICT $name  — real path exists at $link; skipping (use --force)"
      conflict=$((conflict+1))
    fi
  else
    echo "CREATE  $name"
    run "ln -s '$desired' '$link'"; created=$((created+1))
  fi
done

if [ "$PRUNE" = 1 ]; then
  for link in "$TARGET"/*; do
    [ -L "$link" ] || continue
    tgt="$(readlink "$link")"
    case "$tgt" in
      "$REPO"/*) [ -e "$tgt" ] || { echo "PRUNE   $(basename "$link")  (dangling -> $tgt)"; run "rm '$link'"; pruned=$((pruned+1)); } ;;
    esac
  done
fi

echo
echo "summary: created=$created updated=$updated unchanged=$ok conflicts=$conflict pruned=$pruned"
[ "$conflict" -gt 0 ] && echo "note: $conflict conflict(s) left in place — inspect, then re-run with --force to replace."
exit 0

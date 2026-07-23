---
name: manage-symlinks
description: Link the skills in this repo (work-skills) into a Claude Code skills search path so they resolve as installed skills. Use after adding, renaming, or removing a skill here, or when setting up work-skills on a new machine/container. Repo-local — it only manages symlinks for skills that live in this repo.
---

# Manage work-skills symlinks

`work-skills` is the source of truth for the author's work skills. For Claude
Code to see them, each skill directory must appear in a skills search path
(default `~/.claude/skills`) as a symlink back to this repo. This skill keeps
those symlinks in sync.

One skill per top-level directory that contains a `SKILL.md`. Templates and
scaffolds (e.g. `write-guide.example`) are excluded — see `EXCLUDE` in the
script.

## When to use

- After adding a new skill, renaming one, or removing one from this repo.
- Setting up `work-skills` on a fresh container or machine.
- After the personal, gitignored `write-guide/` is created from
  `write-guide.example/` (so it gets linked too).

## Run it

```bash
bash scripts/sync.sh              # link everything into ~/.claude/skills
bash scripts/sync.sh --dry-run    # preview; make no changes
bash scripts/sync.sh --prune      # also remove stale links whose skill was deleted
bash scripts/sync.sh --force      # replace a conflicting real dir (moved aside to Temp)
bash scripts/sync.sh --target ~/.agents/skills   # link into a different search path
```

## Behaviour and safety

- **Idempotent.** A link already pointing at the right place is left untouched;
  a link pointing elsewhere is repointed; a missing link is created.
- **Non-destructive by default.** If a *real* directory or file (not a symlink)
  already occupies a target name, the script **warns and skips** it. Pass
  `--force` to move that path aside to `/workspace/Temp/manage-symlinks-conflicts/`
  and then link. This is what stops it from clobbering an unrelated skill.
- **Prune** only removes symlinks that point *into this repo* and whose source
  no longer exists. It never touches links owned by other repos, or alias links
  (e.g. `gws-slides-edit -> custom-gws-slides-edit`) that point within the
  target dir rather than into this repo.
- **Gitignored skills are linked too.** `write-guide/` is real on disk (just not
  committed), so it is linked like any other skill.

## Notes

- The renamed `write-guide` supersedes the old `zk-write-guide`. Anything that
  still references the old name (e.g. a global `CLAUDE.md` instruction, other
  skills' descriptions) should be updated, or given a compatibility alias
  symlink — this skill does not create name aliases automatically.
- Report what changed after a run (created / updated / pruned / conflicts).

---
name: skillify
description: Distil the current conversation into a new reusable Claude Code skill (SKILL.md). Invoke at the end of a session when a non-trivial workflow, recipe, or stance emerged that the user will reach for again. Assesses whether a skill is warranted before authoring, scopes via AskUserQuestion, and follows the user's existing conventions for naming, frontmatter, and structure.
argument-hint: "<optional: short description of the pattern to capture>"
---

# Skillify

Convert what just happened in this conversation into a Claude Code skill — a `SKILL.md` the user can rely on next time without re-deriving the pattern. Aim for one screen, accurate triggers, and honest "when NOT to use" boundaries.

## Step 0 — Assess: does this deserve a skill?

Skill creation has overhead and dilutes the auto-loaded skill index. Before authoring, the pattern must clear **all four** bars:

- **Reusability**: the user will reach for it across ≥2 distinct contexts. One-off scripts and answers to a single question do not qualify.
- **Non-trivial logic**: there are gotchas, sequencing, or conventions a future Claude would re-derive poorly without notes. Pure tool wrappers without insight do not qualify.
- **Stability**: the pattern is unlikely to churn weekly. Volatile APIs or in-flight investigations belong in memory, not skills.
- **Trigger clarity**: you can state, in one sentence, when a future Claude should auto-invoke this. Vague triggers ("about projects", "when coding") will misfire.

**Skip the skill — propose a better home — when any of these are true:**

| Signal | Better home |
|---|---|
| It's a single fact about the user, project, or system | auto-memory under `~/.claude/projects/-workspace/memory/` |
| It's a project-specific convention | that project's `CLAUDE.md` |
| It's a recurring schedule, not a procedure | `/schedule` |
| It extends or duplicates an existing skill | edit the existing skill instead |
| It's a tool wrapper with no judgement layer | leave it to the tool's own docs |

If skipping, tell the user briefly *why* and where the content should go instead. Stop here — do not author a low-value skill just because it was asked for.

## Step 1 — Scope via AskUserQuestion

Issue **one** `AskUserQuestion` call combining the questions below. Pre-fill the recommended option for each from what you observed; the user can override.

1. **Name** — kebab-case, following local conventions:
   - `zk-*` — personal voice or judgement (e.g. `zk-write-guide`)
   - `custom-gws-*` — Google Workspace extensions beyond the built-in `gws-*` skills
   - `acli-*` — Atlassian CLI wrappers
   - bare name — generic utilities (e.g. `slack`, `generate-feedback`)
2. **Location** — `~/.claude/skills/<name>/` (global, default) vs `<project>/.claude/skills/<name>/` (project-local, only when the pattern is clearly project-bound).
3. **Auto-invoke trigger** — one-line condition for the description's "Use when..." / "Auto-invoke when..." clause. Confirm the exact phrasing.
4. **Out of scope** — what should this skill explicitly *not* cover? Feeds the "When NOT to use" section.

Do not ask about file structure, frontmatter fields, or content — those are determined by the rules below.

## Step 2 — Author SKILL.md

**Frontmatter** — exactly these fields, no bloat:

```
---
name: <slug, must match folder name>
description: <one paragraph. State the capability, then "Use when..." / "Auto-invoke when..." with crisp criteria. This is the only thing future-Claude reads to decide whether to load the skill — accuracy of the trigger matters more than completeness of the body.>
argument-hint: "<optional: what to pass when invoked>"
---
```

**Body structure** — sections in this order:

1. **H1 title + one-line intent.**
2. **When to use / when NOT to use** — both sides, concrete examples. Reject-cases are as load-bearing as use-cases.
3. **The procedure or knowledge** — the substantive content. Code blocks for invocations; tables for response shapes; tight prose otherwise.
4. **Gotchas / notes for future-me** — non-obvious quirks, schema oddities, things that bit the user before. Often the highest-value section.
5. **See also** — companion skills, related memories, external docs.

**Writing rules**:

- One screen if possible. Tight beats thorough.
- Plain language; concrete examples over abstract description.
- No marketing tone, no emoji unless functional.
- Prefer inline content. Split into `references/` (data, long tables) or `scripts/` (executables) only when the SKILL.md would otherwise exceed ~200 lines.
- If the skill depends on other skills, declare them up front as "Companion skills" with a one-liner each — don't duplicate their logic.

## Step 3 — Write, register, hand off

1. Create the folder and write `SKILL.md` with `Write`. Save any referenced data/scripts into `references/` or `scripts/` subdirs.
2. Tell the user:
   - The path of the new skill.
   - That `/new-skill-checker <path>` runs the security/quality grading (Quantium Claude Skills Security Standard) — recommend running it before sharing or relying on the skill in org contexts.
   - Whether any auto-memory entry should be added (only if the skill needs routing context that isn't obvious from the description alone — e.g. "always invoke X skill when user asks Y").

Do not create a memory entry by default. Most skills are discoverable via the skill index alone.

## Quality bar

A skill is good when:
- A cold future-Claude reads only the frontmatter and knows whether to load it.
- The "when NOT to use" prevents the most obvious mis-fires.
- Captured gotchas save real time on the next invocation — not generic "be careful" advice.
- It composes with other skills rather than duplicating them.

A skill is bad when:
- The description is so broad it auto-loads on unrelated tasks.
- The body restates what tool docs already say.
- It encodes a one-off decision instead of a repeatable pattern.
- It adds a third way to do what two existing skills already handle.

## See also

- `/new-skill-checker` — post-authoring security and metadata grading.
- `~/.claude/skills/` — existing skills for style reference. `zk-write-guide` and `extract-zoom-transcripts` are good templates for prompt-only and procedural skills respectively.

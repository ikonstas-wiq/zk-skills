---
name: remove-ai-tells
description: "Catalogue of AI writing tells and the de-slop pass that removes them. Load at the START of any prose task for a human audience (emails, chat, docs, HTML reports, briefings, slides) so the tells are in view while drafting — and re-run the pass every time a prose artefact is edited or changed, before treating it as done."
---

# Remove AI Tells

Two behaviours, both mandatory:

1. **Up front.** When a task involves writing prose for a human, load this skill and read `references/TELLS.md` (what to remove) and `references/VOICE.md` (what to aim for) before you draft.
2. **On every edit.** Any time a prose artefact is written, edited, or changed, run the De-Slop Pass over the changed text before considering it finished. A material edit is a trigger — loop the pass again, every time.

Run the pass inline, in the model that invoked this skill, directly against the draft — no subagent orchestration by default. (Exception: for a very large standalone artefact, offload the mechanical sweep to a cheaper model and apply its findings yourself; brief it on the guardrails below so it doesn't flag deliberate phrasing.)

## The De-Slop Pass

1. **Sweep** the draft against `references/TELLS.md`. List every hit: category + offending quote.
2. **Fix minimally.** Rewrite only the flagged pattern; keep the author's meaning and phrasing. Roughen the edge, don't rewrite the paragraph. Never add facts while fixing.
3. **Loop.** Sweep again — fixes spawn fresh tells (a cut em dash becomes a tidy bow; a dropped buzzword becomes a hollow intensifier). Repeat until a pass finds nothing new. Two passes usually suffice; three is the ceiling.
4. **Delete-test the residue.** For each remaining adjective, intensifier, or qualifier: delete it. If the sentence means the same, cut it for real.
5. **Read-aloud spot-check** the opener, the closer, and one dense paragraph. If it sounds like a slide deck rather than something said to a colleague, rewrite it.

## Guardrails (the non-obvious calls)

- **Preserve strategic phrasing.** When the source states a position in deliberate words, lift them verbatim. Re-dictating the author's framing is the biggest source of rework — worse than any tell.
- **Never fabricate** to fill a gap — stats, URLs, names, list items. Flag the gap instead.
- **Structural bold and house-style em dashes stay.** The bold-overuse and em-dash rules target prose emphasis, not the typographic hierarchy of dense HTML/report sections. Respect the artefact's established house style.
- **Don't sand off the author's mess.** Fragments, asides, and uneven rhythm from the human source are voice. Only remove patterns the AI introduced.

## Reporting (only when reviewing someone else's draft, not silently fixing your own)

Report hits grouped by `references/TELLS.md` category, each with the quoted text and a concrete suggestion, ordered by impact. Hard bans (§1) are non-negotiable; constructions and lexical hits (§2–3) are rewrite-by-default; density items (§6) are judgment calls — note them, fix when over threshold. The author may overrule any judgment call.

## Files

- `references/TELLS.md` — the catalogue: lexical, rhetorical, structural, tonal, typographic tells, in six sections.
- `references/VOICE.md` — positive voice rules: what the finished prose should read like. Adapt to your house style.
- `README.md` — human-facing map of the skill and its references.

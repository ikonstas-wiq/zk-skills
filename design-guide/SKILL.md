---
name: design-guide
version: 1.0.0
description: "Lightweight design system for self-contained HTML artefacts — reports, briefings, prototypes. CSS design tokens (assets) plus two visual incarnations (Detailed dashboard, Exec editorial) across two brands (Quantium, wiq). Load this when building or restyling any single-file HTML for Quantium/wiq audiences, or when you need reusable design tokens for a prototype."
metadata:
  openclaw:
    category: "custom"
    domain: "design"
---

# design-guide

A lightweight, reusable design system for self-contained HTML artefacts (single-file
dashboards, reports, briefings, prototypes — inline CSS + JS, no build step). It
separates **assets** (design tokens + brand palettes) from **implementations** (how
those tokens are composed into a visual style), so the same token core serves polished
reports *and* future prototypes.

> Not to be confused with the team's broader industrial `design-system`. This is the
> personal, artefact-focused guide.

## The model

**A scheme = assets (tokens + palette) × implementation.** Two brands × two
implementations = **four schemes**, from a shared core rather than four monoliths.

```
ASSETS  (the reusable "what")                 IMPLEMENTATIONS (the "how")
  assets/primitives.css   scale + type + motion    implementations/detailed.css  dashboard
  assets/spectrum.css     9 data colours           implementations/exec.css      editorial
  assets/palette-quantium.css  Q Blue roles
  assets/palette-wiq.css       Berry roles
```

Three token tiers (borrowed from DTCG practice, but plain CSS — no compiler):

- **Primitive** — raw values (`--space-3: 12px`, `--q-blue: #3f69ae`). Never referenced by components directly.
- **Semantic** — role names components consume (`--accent`, `--surface`, `--heading`, `--radius-card`). Palettes and implementations *set* these.
- **Component** — the `.card` / `.doc-table` / `.top-nav` rules, referencing semantic tokens only.

Because every scheme uses the **same HTML class vocabulary**, switching scheme is a CSS
swap (plus the matching JS behaviour) — the markup never changes.

## How to build an artefact

1. **Pick a scheme** from the two axes (see selection guide below).
2. **Inline the recipe** — concatenate the token + implementation files into one
   `<style>` block. See [`presets/README.md`](presets/README.md) for the exact file
   order per scheme and the two JS behaviours.
3. **Load Roboto** (and **Inter** for Exec) from Google Fonts in `<head>`.
4. **Build with the class vocabulary** — reference semantic tokens, never hardcode hex,
   size, spacing, or radius in `style=""`.
5. **Run the Design Quality Review** (below) before delivering.

For a prototype that only needs tokens, inline `primitives.css` + a `palette-*.css` and
build your own components against the semantic roles.

## Choosing a scheme

| Axis | Options | Driven by |
|---|---|---|
| **Brand** (palette) | Quantium (Q Blue) · wiq (Berry) | The audience's org |
| **Register** (implementation) | Detailed · Exec | Purpose + reader |

- **Detailed** — dashboards, working briefings, multi-topic reports, anything data-dense or tab-navigated. Rounded, hover elevation, spectrum coding, one page visible at a time.
- **Exec** — POVs, essays, board/leadership reads, external thought-leadership. Warm paper, near-black ink, one restrained accent, sharp 3px, longform. Tabs double as scroll anchors (scroll down *or* click across).

| | Detailed (dashboard) | Exec (editorial) |
|---|---|---|
| Background | cool white `#f8f9fa` | warm paper `#f7f4ef` |
| Text | brand heading + Dark Grey body | ink `#1a1a1a` / `#3d3d3a` |
| Accent | brand + full 9-colour spectrum | **one** brand accent; spectrum for data only |
| Radius | 8–10px | 3px |
| Shadow / motion | hover shadows, fadeUp | none (print-like) |
| Layout | tabs, one page at a time | all sections stacked + scroll-spy tabs |
| Type | Roboto 300/400/500 | Inter display 600/700, larger body |

## Token reference

Tokens live in `assets/`. Key families (full values in the files):

- **Space** `--space-1..16` (4px base): 4·8·12·16·24·32·48·64
- **Radius** `--radius-sharp:3 · -sm:4 · -md:8 · -lg:10`
- **Type** `--text-h1:32 · -h2:22 · -title:16 · -lead:15 · -body:14 · -small:13 · -label:11 · -meta:10 · -pill:10`; weights `--weight-light:300 · -regular:400 · -medium:500 · -display`
- **Elevation** `--elev-0 · -card · -hover · -open`
- **Motion** `--motion-fast:150 · -standard:250 · -expand:450` + `--ease-out-expo`
- **Measure** `--container:1100 · -wide:1440 · --measure-longform:720`
- **Colour** neutrals + paper/ink primitives; the 9-colour `--q-*` spectrum; brand accent + status roles from the palette

Semantic roles components consume: `--accent · --accent-hover · --on-accent · --heading ·
--text · --text-muted · --bg · --surface · --surface-inset · --border-color ·
--radius-container/-card/-pill · --shadow-rest/-hover/-open · --table-head-bg/-fg ·
--table-row-alt · --{info,success,warning,danger}(-bg/-fg)`.

## Component vocabulary

Same classes across all schemes: `.top-nav` (`.top-nav-title`, `.top-nav-tab`,
`.top-nav-date`) · `.page` · `.container` · `h1` + `.tagline` · `.master-section`
(`.master-header`, `.master-color-bar`, `.master-heading-text`, `.master-title`,
`.master-subhead`, `.master-chevron`, `.master-body` → `.master-body-inner`) ·
`.info-table` / `.doc-table` / `.action-table` · `.tag` (`.tag-blue/-cyan/-green/-orange/-coral/-violet`)
· `.quote` · `.tip-card` / `.warning-card` · `.convo-card` / `.response-card` (`.prompt`)
with `.badge-num` · `.timeline-item` · `.callout-bar` (`.callout-label`, `.callout-text`)
· `.stats-row` (`.stat-number`, `.stat-label`) · `.card` / `.grid-card` · status
`.status-dot` / `.rag`.

**Accordion header:** always wrap title + subhead in `.master-heading-text` (its
`flex-direction: column` stacks them). Without the wrapper they render on one line —
the recurring squashed-subhead bug.

**Class-name collisions:** the circular index badge is `.badge-num`, never bare `.num`
— a bare `.num` also matches numeric table cells and silently reshapes them into pills.

## No decorative characters

Never use emoji, Unicode dingbats/pictographs, or HTML entities (`&check;`, `&#x2713;`,
`&#x26A0;`, arrows, stars) as visual elements — in headings, labels, badges, or status.
Instead: CSS coloured dots, colour bars, border-left accents; text labels ("Active",
"Up"); inline SVG chevrons for expand/collapse. Only standard punctuation
(hyphens, en-dashes, pipes) is acceptable as a symbol.

## Colour discipline

1. **Brand accent leads.** `--accent` (Q Blue / Berry) carries active states, stat
   numbers, callout borders, key accents — confidently present, not a grey-with-a-garnish.
2. **Spectrum is for data only.** The `--q-*` palette is for charts and domain coding,
   in the sacred 1–9 order (Blue, Cyan, Turquoise, Green, Yellow, Orange, Coral,
   Burgundy, Violet). Never as a general UI accent; never start with orange.
3. **Warm neutrals, warm hover.** Insets and hover use `--surface-inset` (chrome/paper),
   not cold grey. Never `--surface-inset` as a large page background.
4. **Every hex traces to a token.** No hardcoded hex in `style=""` — outside the `:root`
   token definitions there should be no raw hex.
5. **Exec restraint.** In Exec, one accent only for UI; no coloured card-bar grids.

## Restyling an existing HTML file

Choose the approach by file size — the goal is speed, not sequential chunk reads.

| Lines | Approach |
|---|---|
| < 300 | Read whole file, rewrite |
| 300–800 | Read in 2–3 **parallel** chunks, then targeted edits |
| 800–2000 | Read `<style>` block + scan inline patterns, then batch edits |
| 2000+ | Rewrite `<style>` + `replace_all` passes |

Never read 100 lines at a time in 15 sequential calls — that is the biggest source of
slowness. Rewrite the `<style>` block in one edit (80% of the work), then
`replace_all` systematic swaps for inline styles (run independent swaps in parallel).
Verify with a final scan for orphaned hex outside `:root`.

Common swaps: `#212121/#111/#000 → var(--heading)` · `#555 → var(--text)` ·
`#757575/#888/#9e9e9e → var(--text-muted)` · `#e0e0e0/#ccc → var(--border-color)` ·
`#f8f8f8/#fafafa → var(--bg)` · `font-weight:600/700/800 → var(--weight-medium)`
(Detailed) · `border-radius:12/16/20px → var(--radius-card)`.

## Design Quality Review

Before delivering, verify:

**Anti-slop** — sections vary (not all identical accordions; mix tables, cards, callouts,
timelines); accent is confidently present, not timid; no orange-as-primary; no chrome/paper
as a large page background; no emoji or stray Unicode icons; no orphaned inline hex;
cards vary (some colour-barred, some stats, some compact rows).

**Typography** — headings in `--weight-medium` (Detailed) / display weight (Exec), one
`h1` size and one `h2` size per page; body light and readable; labels uppercase 10–12px
with tracking; sentence case on headings.

**Colour** — every hex references a token; accent dominant; spectrum only in data, in
1–9 order; text is heading-ink for headings, body-ink for body, never pure `#000`.

**Structure** — Detailed: light shadows on hover only; subtle transitions; radius ≤10px.
Exec: no shadow, no motion, radius 3px. SVG chevrons; CSS dots for status. Every
`.master-title` + `.master-subhead` sits inside a `.master-heading-text` wrapper.

**Layout** — clear hierarchy; sections visually distinct; grids reflow on mobile; nav
scrolls horizontally; content within `--container` (or `--container-wide` for data-dense).

## Consumers

- **mds-to-html** loads this and selects a scheme from its intake.
- **q-html** / **wiq-html** are deprecated thin pointers to this guide (the two Detailed
  presets). Prefer design-guide directly.
- **distil-workshop** and future prototypes reference these tokens.

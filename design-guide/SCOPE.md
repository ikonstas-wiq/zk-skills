# design-guide — Scope

A lightweight, reusable design system for self-contained HTML artefacts (reports, briefings, prototypes). Splits **assets** (tokens + brand palettes) from **implementations** (Detailed vs Exec incarnations), so the same token core serves both polished reports and future prototypes.

Status: **scoped, awaiting go-ahead to build.** Nothing here is wired in yet.

---

## 1. Why

Two problems in the current setup:

1. **Tokens only exist for colour.** `q-html` and `wiq-html` define a full colour `:root`, but the type scale, spacing, radius, elevation and motion live in *prose tables*, not CSS variables. That is the root cause of the recurring polish failures mds-to-html fights by hand — "one card title at 14px, the next at 16px", "two tables at different cell sizes". You cannot hold a scale constant that isn't a variable.
2. **Only one axis is modelled: brand.** The skills capture *wiq (Berry) vs Quantium (Blue)*. The `/html-examples` reveal a second, orthogonal axis — **register**: the dashboard style the skills produce vs an *editorial "exec" style* (warm paper, near-black ink, one restrained accent, 3px radius, no shadow, longform). Nothing captures it today.

Two axes → **four schemes**. Rather than four monolithic stylesheets, we keep the conceptual separation: `scheme = palette (asset) × implementation`.

---

## 2. Architecture

```
work-skills/design-guide/
  SKILL.md                     — the guide: model, token reference, when-to-use, anti-slop rules
  assets/                      — THE REUSABLE "WHAT"
    primitives.css             — space · radius · type scale · weight · elevation · motion · measure
    spectrum.css               — the 9-colour data spectrum (brand-neutral, shared)
    palette-quantium.css       — semantic colour roles → Q Blue / Q Black / warm greys
    palette-wiq.css            — semantic colour roles → Berry / Charcoal
  implementations/             — THE "HOW" (incarnations)
    detailed.css               — dashboard: md/lg radius, hover elevation, transitions, spectrum, tabs/cards/accordions
    exec.css                   — editorial: 3px radius, paper bg, no shadow, single accent, longform measure
  presets/                     — zero-friction merges (agent pastes one :root block)
    quantium-detailed.css      (= today's q-html)
    wiq-detailed.css           (= today's wiq-html)
    quantium-exec.css          (NEW)
    wiq-exec.css               (NEW)
  components/                  — component CSS grouped by implementation (nav, card, table, accordion, callout, stats, timeline…)
```

**Layering (three tiers, borrowed from design-harness but no build step):**

- **Primitive** — raw scale values (`--space-3: 12px`, `--q-blue: #3f69ae`). Never used directly in components.
- **Semantic** — role names a component references (`--accent`, `--surface`, `--heading`, `--radius-container`). Palettes and implementations *set* these.
- **Component** — the actual `.card` / `.q-table` / `.top-nav` rules, referencing semantic tokens only.

**How a scheme composes:**

```
Assets:          primitives.css  +  spectrum.css  +  palette-{brand}.css
Implementation:  implementations/{detailed|exec}.css   (overrides structural semantics)
= Scheme:        one of the 4 presets
```

A prototype that just wants your tokens pulls `primitives.css + palette-quantium.css` and ignores everything else. That is the reusability you asked for.

---

## 3. Token inventory (the "beef up")

Colour tokens carry over from q-html/wiq-html unchanged. **New** token families:

### Space (`--space-*`) — 4px base, mirrors design-harness primitives
`1:4 · 2:8 · 3:12 · 4:16 · 6:24 · 8:32 · 12:48 · 16:64`
(card padding = 3, section body = 6, container padding = 12)

### Radius (`--radius-*`)
`sharp:3px` (exec) · `sm:4px` (pills/tags) · `md:8px` (cards) · `lg:10px` (containers, detailed)

### Type scale (`--text-*`) — the single biggest fix
| Token | Size | Weight | Use |
|---|---|---|---|
| `--text-h1` | 32px | 500 | page h1 |
| `--text-h2` | 22px | 500 | section h2 |
| `--text-title` | 16px | 500 | section + card titles (pick one, hold it) |
| `--text-lead` | 15px | 300 | tagline / lead paragraph |
| `--text-body` | 14px | 400 | body content |
| `--text-small` | 13px | 300 | card desc, table cells |
| `--text-label` | 11px | 500 | uppercase table headers, labels, meta |
| `--text-meta` | 10px | 500 | caption |
| `--text-pill` | 10px | 500 | tags |

Plus `--weight-light:300 · -regular:400 · -medium:500`, `--tracking-tight:-0.2px` (headings), `--tracking-label:0.06em` (uppercase), and line-heights `--lh-tight:1.2 / --lh-body:1.5`.

### Elevation (`--elev-*`)
`0:none` · `hover:0 2px 12px rgba(0,0,0,.04)` · `open:0 4px 20px rgba(0,0,0,.06)` · `card:0 2px 8px rgba(0,0,0,.04)`

### Motion (`--motion-*`)
`fast:150ms · standard:250ms · expand:450ms` + `--ease-out-expo: cubic-bezier(0.16,1,0.3,1)`

### Measure / layout
`--container:1100px · --container-wide:1440px · --measure-longform:720px` (exec reading width)

### Font
`--font-sans:'Roboto',system-ui,sans-serif` · `--font-display` (exec may swap to `'Inter'`, matching the editorial examples)

### Semantic colour roles (set by palette, consumed by components)
`--accent · --accent-hover · --on-accent · --heading · --text · --text-muted · --bg · --surface · --surface-inset · --border-color · --focus-ring` + status quads `--{info,success,warning,danger}` / `-bg` / `-fg`.

---

## 4. The four schemes

**Assets differ by brand; implementations differ by register.**

| | **Detailed** (dashboard) | **Exec** (editorial) |
|---|---|---|
| **Quantium** | Q Blue accent · full spectrum · white `#f8f9fa` bg · 8–10px radius · hover shadows · **tabbed** | Q Black ink on warm paper `#F7F4EF` · single Blue (or Cyan) accent · 3px radius · no shadow · **longform** |
| **wiq** | Berry accent · Berry table headers · no shadow · 8px radius · **tabbed** | Charcoal ink on paper · single Berry accent · 3px radius · longform |

Detailed = the two skills you already have (re-expressed on tokens, behaviour unchanged). Exec = new, derived from `cost-of-intelligence` / `ai-transformation-pov` / `enterprise-ai-inference`.

**Exec incarnation specifics (from the examples):**
- Backgrounds: warm paper `#F7F4EF` / near-white `#FAFAF9`; optional dark sidebar `#1C1C1E`.
- Ink: near-black `#1A1A1A` / `#3D3D3A`, not the Q-Black used on white.
- **One** accent only for UI; spectrum reserved strictly for data. No card grids of coloured bars.
- Radius `3px`; **no** shadows or transitions (print-like).
- Longform single column at `--measure-longform` (~720px), larger `--text-body` (16px), and **display weights relaxed to 600/700** for editorial headings (Detailed keeps the 300/400/500 restraint).

**Exec is structural, not just paint.** Detailed is tab-centric; Exec is longform. So design-guide ships an exec *layout pattern* (sectioned longform, optional sticky section-nav) alongside the exec palette — mds-to-html picks tabbed-vs-longform from the intake register.

---

## 5. Consumers & wiring

| Consumer | Change |
|---|---|
| **mds-to-html** | Step 1 "read q-html" → "read design-guide; select scheme from intake". Register/audience already collected in intake maps to scheme (exec audience → Exec; org → palette); explicit override allowed. Everything else in the skill is untouched. |
| **q-html / wiq-html** | Become thin pointers to design-guide's `*-detailed` presets (or keep as-is short-term; deprecate to avoid drift). |
| **distil-workshop** | Update its q/wiq-html reference to design-guide. |
| **future prototypes** | Pull `assets/primitives.css` + a palette. No report styling needed. |

Shared rules currently **duplicated** across q-html and wiq-html (no-emoji, anti-slop checklist, colour discipline, restyling strategy) move to design-guide once and are referenced, not copied.

---

## 6. What to build (proposed phasing)

- **Phase 1 (recommended this pass):** create `design-guide/` — `assets/` (primitives, spectrum, both palettes), both `implementations/`, the 4 `presets/`, and `SKILL.md`. Wire mds-to-html Step 1 to load it and select a scheme. Detailed presets reproduce today's q/wiq-html output exactly (no visual regression); Exec presets are the net-new capability.
- **Phase 2:** slim q-html / wiq-html to pointers; update distil-workshop.
- **Phase 3 (your call, separate):** delete personal `design-harness`.

---

## 7. Red-Team Notes

- **Risk — visual regression in existing reports.** Detailed presets must byte-for-byte reproduce current q/wiq-html rendering. *Mitigation:* build Detailed by lifting the existing component CSS verbatim, only swapping literals for tokens; diff a known report before/after.
- **Risk — "lightweight" scope creep into design-harness.** No CLI, no build, no DTCG-JSON generation — plain CSS files + a guide. If a build step ever appears, that's a signal we've overshot.
- **Gap — Exec longform vs mds-to-html's tab engine.** Exec needs a layout mode, not just colours; flagged in §4/§5. Decision needed: does Exec in mds-to-html render longform, or tabbed-with-exec-paint? *Recommendation: longform, since that's what the examples are and what "exec read" implies.*
- **Gap — font loading for Exec.** Editorial examples use Inter; adds a second Google Fonts family. Acceptable (still self-contained), but note it in the boilerplate.
- **Scope check — brand ambiguity.** mds-to-html today only knows Quantium. Adding wiq as a first-class palette means intake must capture *org* (already implied by audience). Low risk; the intake table already has the hook.
- **Simpler alternative considered:** four flat preset files, no asset/implementation split. Rejected per your preference — it duplicates the palette and scale four times and kills prototype reuse. The tiered split costs one extra concept for real reuse.

**Verdict:** No blocking issues. Two decisions to confirm before Phase 1 (below).

---

## 8. Decisions (resolved)

1. **Exec layout:** **tabs-as-anchors.** Keep the tab bar, but render all sections on one continuous page — the reader can *scroll down* through everything or *click across* to jump. Sticky tab bar scroll-spies the active section (IntersectionObserver). This is distinct from Detailed's show/hide-one-page behaviour.
2. **q/wiq-html fate:** **deprecate now** to thin pointers into design-guide. Goal is to re-test mds-to-html against the new dependency.

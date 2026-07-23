---
name: q-html
version: 1.0.0
description: "Quantium-branded HTML styling system for self-contained single-file dashboards, reports, and presentation artefacts."
metadata:
  openclaw:
    category: "custom"
    domain: "design"
---

# Quantium HTML Styling System

Use this skill when building self-contained HTML artefacts (dashboards, reports, briefing pages, interactive presentations) for Quantium audiences. These are single-file HTML documents with inline CSS + JS, no build step.

## Design DNA

The Quantium style uses **Blue as the primary accent** against **warm neutrals** — clean, analytical, confident. Key traits:

- **Q Blue `#3f69ae`** is the primary accent colour — used for headings, active states, key accents, stat numbers, table headers
- **Quantium Black `#000006`** for headings (nearly-black, not pure black)
- **Dark Grey `#4a4a4e`** for body text
- **Warm grey chrome** (`#ece8e4`) for inset backgrounds and hover states
- **Spectrum palette** for domain/category coding and data visualisation (in strict order)
- **Subtle shadows allowed** — light `box-shadow` on hover for interactive cards only
- **Smooth transitions allowed** — subtle transitions (0.15–0.3s) on interactive elements
- **Max 10px border-radius** on containers, 8px on cards, 4–6px on small elements
- **Font weight restraint** — 300 (light), 400 (regular), 500 (medium) only

## No Decorative Characters

**Never use HTML emoji, Unicode symbols, or decorative characters as visual elements.** This includes:

- No emoji (stars, checkmarks, warning signs, arrows, fire, etc.)
- No Unicode dingbats or pictographs as icons
- No `&bull;`, `&check;`, `&#x2713;`, `&#x26A0;`, `&#x2191;`, etc. used decoratively
- No emoji in headings, labels, badges, or status indicators

**Instead use:**
- CSS-only indicators: coloured dots (`width: 6px; height: 6px; border-radius: 50%`), colour bars, border-left accents
- Text labels: "Active", "Warning", "Up", "Down" — written as words
- SVG chevrons for expand/collapse (inline `<svg>`, not Unicode triangles)
- Colour coding via background/text colour to convey status

**The only acceptable text symbols** are standard punctuation: hyphens, en-dashes, pipes as separators.

## Boilerplate

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TITLE</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root {
    /* -- Primary palette -- */
    --q-black: #000006;
    --q-white: #ffffff;
    --q-chrome: #ece8e4;

    /* -- Surface palette -- */
    --bg: #f8f9fa;
    --surface: #ffffff;
    --chrome: #ece8e4;
    --light-grey: #f2f2f2;

    /* -- Text -- */
    --text-primary: #000006;
    --text-secondary: #4a4a4e;
    --text-tertiary: #93908e;

    /* -- Structural greys (warm) -- */
    --border: #c7c5c4;
    --border-light: #ece8e4;
    --warm-grey: #bcb5ac;
    --dark-warm-grey: #736e68;
    --dark-grey: #4a4a4e;

    /* -- Spectrum palette (for domain/category coding, in order) -- */
    --q-blue: #3f69ae;
    --q-cyan: #44b6c5;
    --q-turquoise: #44d5a3;
    --q-green: #80df7c;
    --q-yellow: #eacb79;
    --q-orange: #ef9c48;
    --q-coral: #ef6348;
    --q-burgundy: #c96478;
    --q-violet: #8f73be;

    /* -- Animation -- */
    --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Roboto', system-ui, sans-serif;
    font-weight: 400;
    background: var(--bg);
    color: var(--text-secondary);
    -webkit-font-smoothing: antialiased;
  }
</style>
</head>
<body>
  <!-- content -->
</body>
</html>
```

## Colour System

### Primary Palette (identity)

From Quantium's official brand guidelines. Blue is the hero accent; warm greys are the foundation.

| Token             | Hex       | Use                                    |
|-------------------|-----------|----------------------------------------|
| `--q-black`       | `#000006` | Headings, high-emphasis text (never pure `#000`) |
| `--q-white`       | `#ffffff` | Surfaces, cards, light backgrounds     |
| `--q-chrome`      | `#ece8e4` | Chrome backgrounds, hover states, insets |
| `--q-blue`        | `#3f69ae` | Primary accent — headings, active tabs, stat numbers, table headers, callout borders |

### Surface Layers

| Token              | Hex       | Use                                |
|--------------------|-----------|------------------------------------|
| `--bg`             | `#f8f9fa` | Page background                    |
| `--surface`        | `#ffffff` | Cards, panels, sections            |
| `--chrome`         | `#ece8e4` | Hover states, inset backgrounds, column headers |
| `--light-grey`     | `#f2f2f2` | Subtle neutral backgrounds         |

### Text Hierarchy

| Token              | Hex       | Use                                |
|--------------------|-----------|------------------------------------|
| `--text-primary`   | `#000006` | Headings, primary content (= Q Black) |
| `--text-secondary` | `#4a4a4e` | Body text, descriptions (= Dark Grey) |
| `--text-tertiary`  | `#93908e` | Labels, metadata, timestamps (= Grey) |

### Structural Greys (warm-toned)

| Token              | Hex       | Use                                |
|--------------------|-----------|------------------------------------|
| `--border`         | `#c7c5c4` | Standard borders                   |
| `--border-light`   | `#ece8e4` | Subtle dividers (= Chrome)         |
| `--warm-grey`      | `#bcb5ac` | Decorative bars, bullets, mid-tone accents |
| `--dark-warm-grey` | `#736e68` | Secondary labels with warmth       |
| `--dark-grey`      | `#4a4a4e` | Strong contrast elements           |

### Spectrum Palette (domain/category coding and data visualisation)

**CRITICAL**: Charts and visualisations MUST use the spectrum palette in this order. Adjacent colours for related concepts, distant for contrast. These are **not** for general UI elements (use Q Blue for that).

| #  | Token             | Hex       | Typical use                    |
|----|-------------------|-----------|--------------------------------|
| 1  | `--q-blue`        | `#3f69ae` | Primary accent AND first data series |
| 2  | `--q-cyan`        | `#44b6c5` | Connectors, secondary accents  |
| 3  | `--q-turquoise`   | `#44d5a3` | Success states, positive indicators |
| 4  | `--q-green`       | `#80df7c` | Growth, scale indicators       |
| 5  | `--q-yellow`      | `#eacb79` | Caution, pricing               |
| 6  | `--q-orange`      | `#ef9c48` | Action required (use sparingly) |
| 7  | `--q-coral`       | `#ef6348` | Urgency, alerts, negative      |
| 8  | `--q-burgundy`    | `#c96478` | Revenue, commercial            |
| 9  | `--q-violet`      | `#8f73be` | Support, capabilities          |

### Semantic Tags (pastel pill backgrounds)

```css
/* Status maturity */
.tag-scaled  { background: #e8f5f0; color: #2a6b55; }
.tag-mvp     { background: #e8f0f8; color: #3a5a8a; }
.tag-poc     { background: #f5f0e0; color: #6b5a2a; }
.tag-concept { background: var(--chrome); color: var(--dark-warm-grey); }

/* Value types */
.val-do-more     { background: #e8f5f0; color: #2a6b55; }
.val-do-less     { background: #e8f0f8; color: #3a5a8a; }
.val-consistency { background: #f5f0e0; color: #6b5a2a; }
.val-commercial  { background: #f5e8e8; color: #7a3a3a; }

/* RAG status */
.rag-green { background: #e8f5f0; color: #2a7a55; }
.rag-amber { background: #f5f0e0; color: #8a6a2a; }
.rag-red   { background: #f5e8e8; color: #8a2a2a; }
```

### When to use Q Blue vs Spectrum colours

| Element                    | Use Q Blue               | Use Spectrum               |
|----------------------------|--------------------------|----------------------------|
| Active tab indicator       | `--q-blue`               | --                         |
| Table header background    | `--q-blue` or `--chrome` | --                         |
| Stat/hero number           | `--q-blue`               | --                         |
| Heading accent             | `--q-blue`               | --                         |
| Callout/accent border-left | `--q-blue`               | --                         |
| Domain colour coding       | --                       | Matching `--q-*` colour    |
| Chart data series          | Start with `--q-blue`    | Remaining `--q-*` in order |
| Status indicators          | --                       | RAG colours or tags        |
| Filter pill (active)       | `--q-blue`               | --                         |
| Positive/negative values   | --                       | `--q-turquoise` / `--q-coral` |

### Colour usage hierarchy (in order of application)

1. **Primary palette first** — White surfaces, Q Black headings, Chrome accents
2. **Warm greys for structure** — borders, dividers, neutral UI elements
3. **Blue + Cyan as primary accents** — start with `--q-blue`, add `--q-cyan` for secondary
4. **Spectrum sparingly** — only when multiple colour distinctions are needed, in order

**Anti-patterns to avoid:**
- Starting with orange/warm spectrum colours as primary accent
- Using full spectrum when 2–3 colours would suffice
- Using Chrome as primary page background (too dark for large areas — use `--bg` or white)
- Using spectrum colours for non-data structural elements

## Typography

- **Font**: `'Roboto', system-ui, sans-serif`
- **Weights**: 300 (light — descriptions, body), 400 (regular — general text), 500 (medium — headings, labels)
- **Headings**: `h1` at 32px/500 in Q Black, `h2` at 22px/500, section titles at 15–16px/500
- **Taglines**: 15px/300 in text-secondary, `line-height: 1.5`
- **Body**: 13–14px/300 in text-secondary for descriptions, 14px/400 for content
- **Labels/Meta**: 10–12px/500, uppercase, letter-spacing 0.04–0.08em, text-tertiary
- **Letter-spacing**: `-0.2px` to `-0.3px` on headings for tightness
- **Sentence case** for all headings (not Title Case, not ALL CAPS)

## Component Patterns

### Navigation (sticky top bar)

```css
.top-nav {
  position: sticky; top: 0; z-index: 100;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; padding: 0 24px;
}
.top-nav-title {
  font-size: 18px; font-weight: 500;
  color: var(--text-primary); letter-spacing: -0.3px;
  padding-right: 24px; margin-right: 8px;
  border-right: 1px solid var(--border); white-space: nowrap;
}
.top-nav-tab {
  font-size: 13px; font-weight: 500;
  color: var(--text-tertiary); background: none; border: none;
  padding: 16px; cursor: pointer; position: relative;
  transition: color 0.2s;
}
.top-nav-tab:hover { color: var(--text-secondary); }
.top-nav-tab.active { color: var(--text-primary); }
.top-nav-tab.active::after {
  content: ''; position: absolute; bottom: 0; left: 8px; right: 8px;
  height: 2px; background: var(--q-blue); border-radius: 1px;
}
.top-nav-date { margin-left: auto; font-size: 12px; color: var(--text-tertiary); }
```

### Expandable Section (accordion)

```css
.section {
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  margin-bottom: 12px; overflow: hidden;
  transition: box-shadow 0.3s var(--ease-out-expo);
}
.section:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.04); }
.section.open { box-shadow: 0 4px 20px rgba(0,0,0,0.06); }

.section-header {
  display: flex; align-items: center; padding: 20px 24px; cursor: pointer;
  user-select: none; gap: 16px; transition: background 0.2s;
}
.section-header:hover { background: var(--chrome); }

.color-bar { width: 4px; height: 32px; border-radius: 2px; flex-shrink: 0; }
.section-name { font-size: 16px; font-weight: 500; letter-spacing: -0.2px; }
.section-summary { font-size: 13px; color: var(--text-tertiary); margin-top: 2px; font-weight: 300; }

/* Use inline SVG chevron, not Unicode */
.chevron {
  width: 20px; height: 20px; flex-shrink: 0;
  transition: transform 0.35s var(--ease-out-expo); color: var(--text-tertiary);
}
.section.open .chevron { transform: rotate(180deg); }

.section-body { max-height: 0; overflow: hidden; transition: max-height 0.45s var(--ease-out-expo); }
.section-body-inner { padding: 0 24px 24px 44px; }
```

### Card

```css
.card {
  background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
  padding: 12px 14px; transition: box-shadow 0.2s var(--ease-out-expo), border-color 0.2s;
}
.card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.04); border-color: var(--warm-grey); }
.card-title { font-size: 14px; font-weight: 500; letter-spacing: -0.2px; }
.card-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.5; font-weight: 300; }
.card-highlight { border-left: 3px solid var(--warm-grey); }
```

### Grid Card (colour-coded top bar)

```css
.grid-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
  padding: 18px 14px; position: relative; overflow: hidden;
  transition: all 0.2s var(--ease-out-expo);
}
.grid-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
}
.grid-card:hover { transform: translateY(-3px); box-shadow: 0 4px 16px rgba(0,0,0,0.06); }
```

### Tag (pill)

```css
.tag {
  font-size: 10px; font-weight: 500;
  padding: 2px 7px; border-radius: 4px;
  white-space: nowrap; letter-spacing: 0.02em;
}
```

### Band (full-width horizontal section with grid items)

```css
.band {
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  overflow: hidden; margin-bottom: 12px;
}
.band:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.04); }
.band-header {
  display: flex; align-items: center; padding: 18px 24px; gap: 14px;
  border-bottom: 1px solid var(--border);
}
.band-items {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
}
.band-item {
  padding: 14px 24px;
  border-bottom: 1px solid var(--chrome);
  border-right: 1px solid var(--chrome);
}
```

### Callout Bar (north star)

```css
.callout-bar {
  display: flex; align-items: center; gap: 12px; padding: 14px 20px;
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  margin-bottom: 16px; border-left: 3px solid var(--q-blue);
}
.callout-label {
  font-size: 10px; font-weight: 500; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--q-blue); flex-shrink: 0;
}
.callout-text { font-size: 13px; color: var(--text-secondary); font-style: italic; font-weight: 300; }
```

### Stats Row

```css
.stats-row {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 10px; padding: 24px;
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;
  text-align: center;
}
.stat-number { font-size: 40px; font-weight: 500; color: var(--q-blue); line-height: 1.1; }
.stat-label {
  font-size: 11px; color: var(--text-tertiary); margin-top: 4px;
  text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;
}
```

### Filter Bar

```css
.filter-bar { display: flex; align-items: center; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
.filter-bar-label {
  font-size: 12px; font-weight: 500; color: var(--text-tertiary);
  text-transform: uppercase; letter-spacing: 0.04em; margin-right: 4px;
}
.filter-btn {
  font-size: 12px; font-weight: 500;
  padding: 5px 14px; border-radius: 20px; cursor: pointer;
  border: 1px solid var(--border); background: var(--surface); color: var(--text-secondary);
  transition: all 0.15s ease;
}
.filter-btn:hover { border-color: var(--dark-warm-grey); color: var(--text-primary); }
.filter-btn.active { background: var(--q-blue); border-color: var(--q-blue); color: #fff; }
```

### Table

```css
.q-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.q-table th {
  font-size: 11px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em;
  color: var(--text-tertiary); text-align: left; padding: 10px 16px;
  border-bottom: 1px solid var(--border); background: var(--chrome); white-space: nowrap;
}
.q-table td {
  padding: 12px 16px; border-bottom: 1px solid var(--chrome);
  color: var(--text-secondary); vertical-align: top; font-weight: 300;
}
.q-table tbody tr:last-child td { border-bottom: none; }
.q-table tr:hover td { background: var(--chrome); }
```

Note: Quantium tables use **Chrome header with tertiary text** (not coloured header backgrounds). This differs from the wiq-html pattern. For data-heavy tables where the header needs more prominence, use `background: var(--q-blue); color: #fff;` on `th` instead.

### Columns (two-column layout)

```css
.columns { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px; }
.column {
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  overflow: hidden; transition: box-shadow 0.3s var(--ease-out-expo);
}
.column:hover { box-shadow: 0 2px 12px rgba(0,0,0,0.04); }
.column-header {
  display: flex; align-items: center; gap: 12px;
  padding: 18px 20px; border-bottom: 1px solid var(--border); background: var(--chrome);
}
.column-title { font-size: 15px; font-weight: 500; letter-spacing: -0.2px; }
.column-subtitle { font-size: 12px; color: var(--text-tertiary); margin-top: 2px; font-weight: 300; }
.column-body { padding: 12px 14px; display: flex; flex-direction: column; gap: 8px; }
```

### Controls

```css
.controls { display: flex; gap: 8px; margin-bottom: 20px; }
.ctrl-btn {
  font-size: 12px; font-weight: 500;
  padding: 6px 14px; border-radius: 6px; border: 1px solid var(--border);
  background: var(--surface); color: var(--text-secondary); cursor: pointer;
  transition: all 0.15s;
}
.ctrl-btn:hover { border-color: var(--dark-warm-grey); color: var(--text-primary); }
```

### Legend

```css
.legend {
  margin-top: 24px; padding: 16px 20px;
  background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
  display: flex; gap: 24px; flex-wrap: wrap; align-items: center;
}
.legend-title {
  font-size: 11px; font-weight: 500; letter-spacing: 0.06em;
  text-transform: uppercase; color: var(--text-tertiary);
}
.legend-label { font-size: 12px; color: var(--text-secondary); margin-left: 2px; font-weight: 300; }
```

## Status Indicators (no emoji)

Use CSS-only patterns for status:

```css
/* Coloured dot */
.status-dot {
  display: inline-block; width: 8px; height: 8px;
  border-radius: 50%; vertical-align: middle; margin-right: 6px;
}
.status-dot.green  { background: #2a7a55; }
.status-dot.amber  { background: #8a6a2a; }
.status-dot.red    { background: #8a2a2a; }

/* RAG with dot + label */
.rag {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px; font-weight: 500;
  padding: 2px 10px 2px 6px; border-radius: 4px; white-space: nowrap;
}
.rag-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.rag-green { background: #e8f5f0; color: #2a7a55; }
.rag-green .rag-dot { background: #2a7a55; }
.rag-amber { background: #f5f0e0; color: #8a6a2a; }
.rag-amber .rag-dot { background: #8a6a2a; }
.rag-red { background: #f5e8e8; color: #8a2a2a; }
.rag-red .rag-dot { background: #8a2a2a; }

/* Meta dots (small, inline with text) */
.meta-dot { width: 6px; height: 6px; border-radius: 50%; }

/* Inline SVG chevron for expand/collapse */
/* Use: <svg class="chevron" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z"/></svg> */
```

## Layout Patterns

- **Max-width container**: `max-width: 1100px; margin: 0 auto; padding: 48px 24px;`
- **Two-column grid**: `display: grid; grid-template-columns: 1fr 1fr; gap: 12px;`
- **Card grid (4-col)**: `display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;`
- **Three-column grid**: `grid-template-columns: repeat(3, 1fr); gap: 16px;`
- **Data-dense dashboards**: `max-width: 1440px`

### Responsive breakpoint

```css
@media (max-width: 1100px) {
  .card-grid { grid-template-columns: repeat(2, 1fr); }
  .columns   { grid-template-columns: 1fr; }
}
```

### Entrance animation (optional)

```css
@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }

.animated-section {
  opacity: 0; transform: translateY(12px);
  animation: fadeUp 0.5s var(--ease-out-expo) forwards;
}
```

## Conventions

1. **Single-file** — all CSS and JS inline, no external dependencies except Google Fonts
2. **CSS variables only** — never hardcode hex values in component styles; always reference tokens
3. **Q Blue as primary accent** — active states, stat numbers, callout borders, filter pills all use `--q-blue`
4. **Q Black for headings** — `--text-primary` is `#000006`, body text is `--text-secondary` (`#4a4a4e`)
5. **Colour-bar pattern** — use a `4px` wide vertical colour bar or `3px` top-edge bar for section identity
6. **Warm hover** — hover states use `background: var(--chrome)`, not cold grey
7. **Light shadow on hover only** — `box-shadow: 0 2px 12px rgba(0,0,0,0.04)` on interactive card hover; no shadow at rest on most elements
8. **Subtle transitions** — `transition: all 0.2s var(--ease-out-expo)` on interactive elements
9. **10px max border-radius** on containers/sections, 8px on cards, 4–6px on pills/tags
10. **No emoji or decorative Unicode** — use CSS dots, colour bars, and text labels instead
11. **Font imports** — always load Roboto from Google Fonts CDN via `<link>` in `<head>`
12. **Spectrum colours for data only** — `--q-*` palette is for domain coding and chart series (in order), not general UI. Use Q Blue for UI accents
13. **Spectrum order is sacred** — when using multiple spectrum colours, always follow the 1–9 order: Blue, Cyan, Turquoise, Green, Yellow, Orange, Coral, Burgundy, Violet
14. **Blue and Cyan first** — when only 1–2 accent colours are needed beyond structure, reach for `--q-blue` then `--q-cyan`

## Restyling Strategy (for existing HTML files)

When restyling an existing HTML file to this design system, **choose the right approach based on file size**. The goal is speed — avoid sequential chunk-by-chunk reading.

### Step 1: Assess the file

```
wc -l <file>    # line count
ls -lh <file>   # byte size
```

| File size         | Lines     | Approach                    |
|-------------------|-----------|-----------------------------|
| Small             | < 300     | Read whole file, rewrite    |
| Medium            | 300–800   | Read in 2–3 parallel chunks, then targeted edits |
| Large             | 800–2000  | Read `<style>` block + scan inline patterns, then batch edits |
| Very large        | 2000+     | Style-block rewrite + `replace_all` passes |

### Step 2: Read in parallel (not sequentially)

For medium/large files, split the file into parallel reads:

```
# Read lines 1-400, 400-800, 800-1200, 1200+ in ONE parallel call
Read(file, offset=1, limit=400)
Read(file, offset=400, limit=400)
Read(file, offset=800, limit=400)
Read(file, offset=1200, limit=400)
```

**Never** read 100 lines at a time in 15 sequential calls. That is the single biggest source of slowness.

### Step 3: Apply changes efficiently

**For the `<style>` block**: Identify start/end lines, read it, rewrite the entire block in one Edit call. This is where 80% of the restyling happens.

**For inline styles in HTML/JS**: Use targeted `Edit` calls with `replace_all: true` for systematic colour swaps:

```
Edit(file, old="#212121", new="var(--text-primary)", replace_all=true)
Edit(file, old="#757575", new="var(--text-tertiary)", replace_all=true)
```

Run independent `replace_all` edits in parallel where possible.

**For JS template literals**: These contain inline styles in backtick strings. The same `replace_all` approach works — CSS variable references work fine inside template literals since they're ultimately rendered as inline HTML.

### Step 4: Verify

After edits, do a final scan for orphaned hex values:
```
Grep(file, pattern="#[0-9a-fA-F]{3,6}", output_mode="content")
```

Any remaining hardcoded hex (outside of CSS variable definitions in `:root`) needs fixing.

### Common colour mappings

Keep a mental map of the most frequent swaps for this design system:

| Old hex / pattern              | New token                        |
|-------------------------------|----------------------------------|
| `#212121`, `#111`, `#000`     | `var(--text-primary)`            |
| `#37474f`, `#333`             | `var(--text-primary)`            |
| `#555`                        | `var(--text-secondary)`          |
| `#757575`, `#888`, `#9e9e9e`  | `var(--text-tertiary)`           |
| `#bdbdbd`                     | `var(--warm-grey)`               |
| `#e0e0e0`, `#ccc`             | `var(--border)`                  |
| `#f0f0f0`, `#f5f5f5`          | `var(--light-grey)` or `var(--border-light)` |
| `#fafafa`, `#f8f8f8`          | `var(--bg)` or `var(--light-grey)` |
| `font-weight:600/700/800`     | `font-weight: 500`               |
| `border-radius:12/16/20px`    | `border-radius: 8px` or `10px`  |

## Key Differences from wiq-html

| Aspect               | wiq-html                          | q-html                            |
|----------------------|-----------------------------------|-----------------------------------|
| Primary accent       | Berry `#913199`                   | Q Blue `#3f69ae`                  |
| Heading text colour  | Berry (Charcoal `#3a474e`)        | Q Black `#000006`                 |
| Body text colour     | Charcoal `#3a474e`                | Dark Grey `#4a4a4e`               |
| Shadows              | None                              | Light, on hover only              |
| Transitions          | None                              | Subtle (0.15–0.3s)                |
| Border-radius        | Max 8px                           | Max 10px containers, 8px cards    |
| Table headers        | Berry background, white text      | Chrome background, tertiary text (default) or Blue/white (data-heavy) |
| Active filter pill   | Berry fill                        | Q Blue fill                       |
| Entrance animation   | None                              | Optional fadeUp                   |

## Design Quality Review

After generating or restyling any Quantium HTML artefact, run this checklist before delivering.

### Anti-Slop Checklist

- **Generic structure**: Does every section look the same? Vary card sizes, use full-width bands alongside grid cards, mix callout bars with tables.
- **Timid colour usage**: Is Blue confined to tiny accents while everything else is grey? Blue should be confidently present — stat numbers, active states, callout borders, hero elements. It's the brand accent, not a garnish.
- **Orange overuse**: Is orange used as a primary accent? It's position 6 in spectrum — reach for Blue and Cyan first.
- **Chrome overload**: Is Chrome everywhere as background? It's too dark for large areas. Use `--bg` or white for page backgrounds.
- **Emoji/Unicode litter**: Any stray checkmarks, arrows, warning triangles, stars? Replace with CSS indicators or text labels.
- **Orphaned inline styles**: Are hex colours hardcoded in `style=""` attributes instead of referencing CSS variables?
- **Cookie-cutter cards**: Do all cards have identical structure? Vary — some with colour bars, some with stats, some as compact rows.

### Typography Quality

- [ ] Headings use Roboto 500 in Q Black — not default browser weight
- [ ] Body text is 300/400 weight in text-secondary — light and readable
- [ ] Labels/meta are uppercase, 10–12px, with letter-spacing, text-tertiary
- [ ] Sentence case on all headings (not Title Case)
- [ ] Consistent hierarchy — only one h1 size, one h2 size per page

### Colour Discipline

- [ ] Every hardcoded hex references a `--token` (search for `#` in style blocks)
- [ ] Q Blue is the dominant accent — not orange or other spectrum colours
- [ ] Spectrum colours only appear in domain coding, charts, or data vis
- [ ] Spectrum colours follow the 1–9 order when multiples are used
- [ ] Text is Q Black for headings, Dark Grey for body — never pure `#000`
- [ ] Tinted backgrounds use official tag colours, not arbitrary pastels

### Structural Quality

- [ ] Shadows are light and only on hover (not at rest, except open accordions)
- [ ] Transitions are subtle (0.15–0.3s), using `--ease-out-expo` or `ease`
- [ ] All `border-radius` values are 10px or below
- [ ] No emoji, Unicode symbols, or HTML entities used as icons
- [ ] SVG chevrons for expand/collapse, CSS dots for status indicators
- [ ] Tables use Chrome header (or Blue header for data-heavy tables)

### Spatial Composition

- [ ] Page has a clear visual hierarchy — hero/stats at top, detail below
- [ ] Sections are visually distinct — colour bars, border-left accents, or background changes
- [ ] Grid layouts break at 1100px for mobile
- [ ] Content doesn't exceed `max-width: 1100px` (or 1440px for data-dense dashboards)

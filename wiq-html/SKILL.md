---
name: wiq-html
version: 2.0.0
description: "wiq-branded HTML styling system for self-contained single-file dashboards, reports, and presentation artefacts."
metadata:
  openclaw:
    category: "custom"
    domain: "design"
---

# wiq HTML Styling System

Use this skill when building self-contained HTML artefacts (dashboards, reports, briefing pages, interactive presentations) for Quantium / wiqRetail audiences. These are single-file HTML documents with inline CSS + JS, no build step.

## Design DNA

The wiq style uses **Berry purple as the primary accent** against **warm neutrals** — clean, professional, never decorative. Key traits:

- **wiq Berry `#913199`** is the primary brand colour — used for headings, active states, key accents
- **Charcoal `#3a474e`** for all body text (never pure black)
- **Warm grey chrome** (`#ece8e4`) instead of cold greys
- **Spectrum palette** for domain/category coding (distinct from the brand palette)
- **No shadows** — rely on borders and background contrast for depth
- **No animations or transitions** for web content (reserve for presentations)
- **Max 8px border-radius** on all shapes
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
    /* ── Brand palette ── */
    --berry: #913199;
    --berry-50: #c898cc;
    --berry-20: #ead8ec;
    --berry-10: #f9f4f9;
    --charcoal: #3a474e;
    --ultramarine: #250e90;
    --ocean-blue: #66c5ff;
    --alice-blue: #ecf4ff;

    /* ── Surface palette ── */
    --bg: #f8f9fa;
    --surface: #ffffff;
    --chrome: #ece8e4;
    --light-grey: #f2f2f2;

    /* ── Text ── */
    --text-primary: #3a474e;
    --text-secondary: #4a4a4e;
    --text-tertiary: #93908e;

    /* ── Structural greys (warm) ── */
    --border: #c7c5c4;
    --border-light: #ece8e4;
    --warm-grey: #bcb5ac;
    --dark-warm-grey: #736e68;

    /* ── Spectrum palette (for domain/category coding) ── */
    --q-blue: #3f69ae;
    --q-cyan: #44b6c5;
    --q-turquoise: #44d5a3;
    --q-green: #80df7c;
    --q-yellow: #eacb79;
    --q-orange: #ef9c48;
    --q-coral: #ef6348;
    --q-burgundy: #c96478;
    --q-violet: #8f73be;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Roboto', system-ui, sans-serif;
    font-weight: 400;
    background: var(--bg);
    color: var(--text-primary);
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

### Brand Palette (primary identity)

These come directly from the wiq brand guidelines. Berry is the hero colour.

| Token             | Hex       | Use                                    |
|-------------------|-----------|----------------------------------------|
| `--berry`         | `#913199` | Primary accent — headings, active tabs, key accents, table headers |
| `--berry-50`      | `#c898cc` | Mid-tone — taglines, secondary accents |
| `--berry-20`      | `#ead8ec` | Light accent — selected states, highlights |
| `--berry-10`      | `#f9f4f9` | Tinted backgrounds — intro panels, callout boxes |
| `--charcoal`      | `#3a474e` | All body text (never use pure black)   |
| `--ultramarine`   | `#250e90` | Deep accent — gradient start, dark emphasis |
| `--ocean-blue`    | `#66c5ff` | Light blue accent — secondary data series |
| `--alice-blue`    | `#ecf4ff` | Very light blue — info backgrounds     |

### Surface Layers

| Token              | Hex       | Use                                |
|--------------------|-----------|------------------------------------|
| `--bg`             | `#f8f9fa` | Page background                    |
| `--surface`        | `#ffffff` | Cards, panels, sections            |
| `--chrome`         | `#ece8e4` | Hover states, inset backgrounds    |
| `--light-grey`     | `#f2f2f2` | Subtle neutral backgrounds         |

### Text Hierarchy

| Token              | Hex       | Use                                |
|--------------------|-----------|------------------------------------|
| `--text-primary`   | `#3a474e` | Headings, primary content (= Charcoal) |
| `--text-secondary` | `#4a4a4e` | Body text, descriptions            |
| `--text-tertiary`  | `#93908e` | Labels, metadata, timestamps       |

### Structural Greys (warm-toned)

| Token              | Hex       | Use                                |
|--------------------|-----------|------------------------------------|
| `--border`         | `#c7c5c4` | Standard borders                   |
| `--border-light`   | `#ece8e4` | Subtle dividers                    |
| `--warm-grey`      | `#bcb5ac` | Decorative bars, bullets           |
| `--dark-warm-grey` | `#736e68` | Secondary labels with warmth       |

### Spectrum Palette (domain/category coding)

Use for data visualisation, domain colour-coding, and multi-series charts. Ordered spectrally — adjacent colours for related concepts, distant for contrast. These are **not** for general UI elements (use Berry for that).

| Token             | Hex       | Typical use                    |
|-------------------|-----------|--------------------------------|
| `--q-blue`        | `#3f69ae` | Category management            |
| `--q-cyan`        | `#44b6c5` | Assortment, connectors         |
| `--q-turquoise`   | `#44d5a3` | Space/POG, success states      |
| `--q-green`       | `#80df7c` | Growth, scale indicators       |
| `--q-yellow`      | `#eacb79` | Pricing, caution               |
| `--q-orange`      | `#ef9c48` | Buying, action required        |
| `--q-coral`       | `#ef6348` | Promotions, urgency, alerts    |
| `--q-burgundy`    | `#c96478` | Commercial, revenue            |
| `--q-violet`      | `#8f73be` | Support, assets, capabilities  |

### Semantic Tags (pastel pill backgrounds)

```css
/* Status maturity */
.tag-scaled  { background: #e8f5f0; color: #2a6b55; }
.tag-mvp     { background: var(--alice-blue); color: #3a5a8a; }
.tag-poc     { background: #f5f0e0; color: #6b5a2a; }
.tag-concept { background: var(--chrome); color: var(--dark-warm-grey); }

/* RAG status */
.rag-green { background: #e8f5f0; color: #2a7a55; }
.rag-amber { background: #f5f0e0; color: #8a6a2a; }
.rag-red   { background: #f5e8e8; color: #8a2a2a; }
```

### When to use Berry vs Spectrum colours

| Element                    | Use Berry                | Use Spectrum               |
|----------------------------|--------------------------|----------------------------|
| Active tab indicator       | `--berry`                | --                         |
| Table header background    | `--berry`                | --                         |
| Heading colour             | `--berry`                | --                         |
| Callout/accent border-left | `--berry`                | --                         |
| Domain colour coding       | --                       | Matching `--q-*` colour    |
| Chart data series          | `--berry` for primary    | `--q-*` for additional     |
| Status indicators          | --                       | RAG colours or tags        |
| Filter pill (active)       | `--berry`                | --                         |

## Typography

- **Font**: `'Roboto', system-ui, sans-serif`
- **Weights**: 300 (light — descriptions, body), 400 (regular — general text), 500 (medium — headings, labels)
- **Headings**: `h1` at 32px/500 in Berry, `h2` at 22px/500 in Berry, section titles at 15–16px/500
- **Taglines**: 16px/400 in Berry 50%, italic
- **Body**: 13–14px/300 in Charcoal for descriptions, 14–16px/400 for content
- **Labels/Meta**: 10–12px/500, uppercase, letter-spacing 0.04–0.08em
- **Letter-spacing**: `-0.2px` to `-0.3px` on headings for tightness
- **Footnotes**: 8pt/300 in Charcoal

## Component Patterns

### Navigation (sticky top bar)

```css
.top-nav {
  position: sticky; top: 0; z-index: 100;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; padding: 0 24px;
}
.top-nav-tab {
  font-size: 13px; font-weight: 500;
  color: var(--text-tertiary); background: none; border: none;
  padding: 16px; cursor: pointer; position: relative;
}
.top-nav-tab.active { color: var(--text-primary); }
.top-nav-tab.active::after {
  content: ''; position: absolute; bottom: 0; left: 8px; right: 8px;
  height: 2px; background: var(--berry); border-radius: 1px;
}
```

### Floating pill nav (alternative — for slide-style pages)

```css
.nav {
  position: fixed; top: 16px; left: 50%; transform: translateX(-50%);
  background: var(--surface); padding: 5px; border-radius: 8px;
  z-index: 1000; display: flex; gap: 3px; border: 1px solid var(--border);
}
.nav button {
  padding: 10px 20px; border: none; background: transparent;
  color: var(--text-secondary); border-radius: 6px; cursor: pointer;
  font-size: 13px; font-weight: 500;
}
.nav button.active {
  background: var(--berry); color: white;
}
```

### Expandable Section (accordion)

```css
.section {
  background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
  margin-bottom: 12px; overflow: hidden;
}

.section-header {
  display: flex; align-items: center; padding: 20px 24px; cursor: pointer;
  user-select: none; gap: 16px;
}
.section-header:hover { background: var(--chrome); }

.color-bar { width: 4px; height: 32px; border-radius: 2px; flex-shrink: 0; }
.section-name { font-size: 16px; font-weight: 500; letter-spacing: -0.2px; }
.section-summary { font-size: 13px; color: var(--text-tertiary); margin-top: 2px; font-weight: 300; }

/* Use inline SVG chevron, not Unicode */
.chevron { width: 20px; height: 20px; flex-shrink: 0; color: var(--text-tertiary); }

.section-body { max-height: 0; overflow: hidden; }
.section-body-inner { padding: 0 24px 24px 44px; }
```

### Card

```css
.card {
  background: var(--bg); border: 1px solid var(--border); border-radius: 8px;
  padding: 12px 14px;
}
.card:hover { border-color: var(--warm-grey); }
.card-title { font-size: 14px; font-weight: 500; letter-spacing: -0.2px; }
.card-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.5; font-weight: 300; }
.card-highlight { border-left: 4px solid var(--berry); }
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
  background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
  overflow: hidden; margin-bottom: 12px;
}
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

### Callout Bar

```css
.callout-bar {
  display: flex; align-items: center; gap: 12px; padding: 14px 20px;
  background: var(--berry-10); border: 1px solid var(--border); border-radius: 8px;
  margin-bottom: 16px; border-left: 4px solid var(--berry);
}
.callout-label {
  font-size: 10px; font-weight: 500; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--berry); flex-shrink: 0;
}
.callout-text { font-size: 13px; color: var(--text-secondary); font-style: italic; font-weight: 300; }
```

### Data Grid Cards (colour-coded top bar)

```css
.grid-card {
  background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
  padding: 18px 14px; position: relative; overflow: hidden;
}
.grid-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
}
.grid-card:hover { border-color: var(--warm-grey); }
```

### Stats Row

```css
.stats-row {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 24px;
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px;
  text-align: center;
}
.stat-number { font-size: 40px; font-weight: 500; color: var(--berry); line-height: 1.1; }
.stat-label {
  font-size: 11px; color: var(--text-tertiary); margin-top: 4px;
  text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500;
}
```

### Filter Bar

```css
.filter-bar { display: flex; align-items: center; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
.filter-btn {
  font-size: 12px; font-weight: 500;
  padding: 5px 14px; border-radius: 20px; cursor: pointer;
  border: 1px solid var(--border); background: var(--surface); color: var(--text-secondary);
}
.filter-btn:hover { border-color: var(--dark-warm-grey); color: var(--text-primary); }
.filter-btn.active { background: var(--berry); border-color: var(--berry); color: #fff; }
```

### Table

```css
.wiq-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.wiq-table th {
  font-size: 11px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.04em;
  color: #fff; text-align: left; padding: 10px 16px;
  background: var(--berry); border-bottom: 1px solid var(--border);
}
.wiq-table td {
  padding: 12px 16px; border-bottom: 1px solid var(--chrome);
  color: var(--text-secondary); vertical-align: top; font-weight: 300;
}
.wiq-table tr:nth-child(even) td { background: var(--berry-10); }
.wiq-table tr:hover td { background: var(--chrome); }
```

### Takeaway Box

```css
.takeaway {
  background: var(--berry); color: #fff; border-radius: 8px;
  padding: 16px 20px; margin-top: 20px;
  font-size: 14px; font-weight: 400; line-height: 1.5;
}
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

/* Text-only status label */
.status-label {
  font-size: 11px; font-weight: 500; text-transform: uppercase;
  letter-spacing: 0.04em;
}

/* Inline SVG chevron for expand/collapse */
.chevron-svg {
  width: 16px; height: 16px; fill: none;
  stroke: currentColor; stroke-width: 2; stroke-linecap: round;
}
/* Use: <svg class="chevron-svg" viewBox="0 0 16 16"><polyline points="4 6 8 10 12 6"/></svg> */
```

## Layout Patterns

- **Max-width container**: `max-width: 1100px; margin: 0 auto; padding: 48px 24px;`
- **Two-column grid**: `display: grid; grid-template-columns: 1fr 1fr; gap: 12px;`
- **Card grid**: `display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;` (collapse to 2-col below 1100px)
- **Three-column grid**: `grid-template-columns: repeat(3, 1fr); gap: 16px;`

### Responsive breakpoint

```css
@media (max-width: 1100px) {
  .card-grid { grid-template-columns: repeat(2, 1fr); }
  .columns   { grid-template-columns: 1fr; }
}
```

## Conventions

1. **Single-file** — all CSS and JS inline, no external dependencies except Google Fonts
2. **CSS variables only** — never hardcode hex values in component styles; always reference tokens
3. **Berry as primary accent** — headings, active states, table headers, callout borders all use `--berry`
4. **Charcoal text** — `--text-primary` is `#3a474e`, never use pure black
5. **Colour-bar pattern** — use a `4px solid var(--berry)` left border or `3px` top-edge bar for section identity
6. **Warm hover** — hover states use `background: var(--chrome)`, not grey
7. **No box-shadow** — use border contrast and background layering for depth instead
8. **No animations or transitions** — content appears immediately; accordion expand/collapse may use `max-height` toggle via JS but no CSS transitions
9. **8px max border-radius** — all rounded corners cap at `border-radius: 8px`
10. **No emoji or decorative Unicode** — use CSS dots, colour bars, and text labels instead. See the "No Decorative Characters" section above
11. **Font imports** — always load Roboto from Google Fonts CDN via `<link>` in `<head>`
12. **Spectrum colours for data only** — `--q-*` palette is for domain coding and chart series, not general UI. Use Berry for UI accents

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
Edit(file, old="box-shadow:0 1px 4px rgba(0,0,0,.08)", new="border: 1px solid var(--border)", replace_all=true)
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
| `#212121`, `#111`, `#000`     | `var(--text-primary)` / `var(--charcoal)` |
| `#37474f`, `#333`             | `var(--text-primary)`            |
| `#555`, `#4a4a4e`             | `var(--text-secondary)`          |
| `#757575`, `#888`, `#9e9e9e`  | `var(--text-tertiary)`           |
| `#bdbdbd`                     | `var(--warm-grey)`               |
| `#e0e0e0`, `#ccc`             | `var(--border)`                  |
| `#f0f0f0`, `#f5f5f5`          | `var(--light-grey)` or `var(--border-light)` |
| `#fafafa`, `#f8f8f8`          | `var(--bg)` or `var(--light-grey)` |
| `font-weight:600/700/800`     | `font-weight: 500`               |
| `box-shadow:...`              | Remove (use border instead)      |
| `transition:...`              | Remove                           |
| `border-radius:12/16/20px`    | `border-radius: 8px`            |

## Design Quality Review

After generating or restyling any wiq HTML artefact, run this checklist before delivering. The goal is intentional, polished output — not generic AI-generated markup.

### Anti-Slop Checklist

Scan the output for these common signs of low-quality generated HTML:

- **Generic structure**: Does every section look the same? Vary card sizes, use full-width bands alongside grid cards, mix callout bars with tables. Monotonous repetition signals auto-generation.
- **Timid colour usage**: Is Berry confined to tiny accents while everything else is grey? Berry should be confidently present — table headers, active states, callout borders, key stat numbers. It's the brand colour, not a garnish.
- **Emoji/Unicode litter**: Any stray checkmarks, arrows, warning triangles, stars, or decorative symbols? Replace with CSS indicators or text labels. Every single one.
- **Meaningless whitespace**: Is the page either crammed or drowning in padding? Each spacing decision should be intentional — tighter within related items, more generous between sections.
- **Orphaned inline styles**: Are hex colours hardcoded in `style=""` attributes instead of referencing CSS variables? Every colour should trace back to a `--token`.
- **Cookie-cutter cards**: Do all cards have identical structure? Real dashboards vary — some cards have colour bars, some have stats, some are compact rows. Match the component to the content.

### Typography Quality

- [ ] Headings use Roboto 500 in Berry — not default browser weight, not black
- [ ] Body text is 300 weight in Charcoal — light and readable, not heavy
- [ ] Labels/meta are uppercase, 10–12px, with letter-spacing
- [ ] No font size below 11px except footnotes (8pt)
- [ ] Consistent hierarchy — only one h1 size, one h2 size per page

### Colour Discipline

- [ ] Every hardcoded hex in CSS references a `--token` (search for `#` in style blocks)
- [ ] Berry is the dominant accent — not `--q-blue` or any spectrum colour
- [ ] Spectrum colours only appear in domain coding, charts, or data vis
- [ ] Text is Charcoal (`#3a474e`), never `#000`, `#111`, or `#212121`
- [ ] Tinted backgrounds use official Berry tints (`--berry-10`, `--berry-20`), not arbitrary pastels

### Structural Quality

- [ ] No `box-shadow` anywhere — depth comes from borders and background layering
- [ ] No CSS `transition` or `animation` properties (except accordion `max-height` via JS)
- [ ] All `border-radius` values are 8px or below
- [ ] No emoji, Unicode symbols, or HTML entities used as icons
- [ ] SVG chevrons for expand/collapse, CSS dots for status indicators
- [ ] Tables use Berry header with white text, alternating Berry-10 rows

### Spatial Composition

- [ ] Page has a clear visual hierarchy — hero/stats at top, detail below
- [ ] Sections are visually distinct — use colour bars, border-left accents, or background changes to separate areas
- [ ] Grid layouts break at 1100px for mobile
- [ ] Content doesn't exceed `max-width: 1100px` (or 1440px for data-dense dashboards)

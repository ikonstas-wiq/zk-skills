---
name: mds-to-html
description: "Convert multiple markdown topic files into a single self-contained Quantium-branded HTML report with one tab per file. Use when asked to present research, briefings, or multi-topic notes as a polished tabbed HTML page."
argument-hint: "<directory or file list to convert, plus optional output path>"
---

# Markdown Files to Tabbed HTML

Convert a collection of markdown files (or a single long markdown with clear sections) into a self-contained, Quantium-branded HTML page with one tab per topic/file. No information loss — every detail from the source files appears in the output.

## When to Use

- User has multiple `.md` files covering related topics and wants a single polished output
- User has a long markdown document with clear `## Section` breaks that should become tabs
- User asks to "make this into an HTML report", "present these as tabs", or "format these nicely"
- After research that produced multiple markdown files, to consolidate into a readable briefing

## Step 0: Establish Intake (audience drives everything)

Before building, resolve these five inputs. Infer them from the request where stated; only ask if genuinely ambiguous — a wrong guess on audience changes confidentiality, framing, and how much you cut:

| Input | Options | What it controls |
|-------|---------|------------------|
| **Audience** | Just me / internal team / external partner / named individuals | Confidentiality, framing, content fidelity |
| **Shareable?** | Personal working doc vs shareable artefact | Whether the confidentiality + framing rules below are enforced |
| **Register** | Fact-based / minimal-sell (default) vs persuasive | How hard the Tone Gate bites |
| **Size ceiling** | Tab count or "N-page" cap, if any | The curate-vs-density tradeoff (see Content Fidelity) |
| **Anonymisation** | Name people/orgs freely vs strip all names | Framing rules |
| **Voice treatment** | Preserve source (default) / neutral edit / write in authored voice | Whether the optional `write-guide` slot is loaded (see Tone Gate) |
| **Brand** | Quantium (Q Blue) / wiq (Berry) | Which `design-guide` palette |
| **Format** | Detailed (dashboard, tabbed) / Exec (editorial, longform) | Which `design-guide` implementation + which JS behaviour |

Default assumption when unstated: **shareable, fact-based, curated, preserve source voice, Quantium + Detailed.** These settings have caused the least rework. Derive Format from audience/purpose — an exec/leadership/external POV read leans **Exec**; a working or data-dense briefing leans **Detailed**. State your inferred intake (including brand + format = the `design-guide` scheme) in one line before building, so it can be corrected early rather than after the first version.

## Content Fidelity: Lossless vs Curated (depends on audience)

The right level of completeness depends on the intake:

- **Personal / working briefing → lossless.** Every fact, quote, number, table row, and bullet from the source MUST appear. The HTML is a presentation layer, not a summary. If the source says "£700m–£1bn" the HTML says "£700m–£1bn"; 27 source rows → 27 HTML rows. Use accordions/tabs to show everything, not to hide things behind fewer sections.
- **Shareable / exec artefact → curate hard.** Lead with the headline, keep only what the audience needs, and cut low-value sections ruthlessly — information loss is expected and wanted here. Honour any size ceiling from intake (e.g. "2-3 tabs", "two-page"). A reader who won't open an 8-section deck needs the 4 that matter.

**Never fabricate to fill space.** Only include facts present in the source. Do not invent URLs, stats, product names, or list items that aren't in the markdown — when a detail is missing, flag it as a gap rather than inventing one. (Hallucinated repo links and phantom items are a recurring failure here.)

## Prose Readability

Long unbroken prose paragraphs are hard to scan on screen. When a section runs to dense prose, lighten it without losing content:

- **Light keyword bolding, not overkill.** Bold the one or two phrases per paragraph that carry the point (a role, a number, the key claim) so the eye can land. Do not bold whole sentences or every line — that reads as AI emphasis-crutch (see remove-ai-tells §6). Roughly one bold phrase per 2–3 sentences is plenty.
- **Mix prose with bullets.** When a sentence is secretly a list ("do A; do B; treating C as…"), break it into a short lead-in line plus bullets. A run of 3–4 accumulated items, skills, or "double down on" actions almost always reads better as bullets than as a semicolon-chained sentence.
- **Keep a prose anchor.** Lead each section with 1–2 sentences of real prose before any bullets — bullets alone lose the narrative. The pattern is *prose sets up the point → bullets carry the list → optional prose closes it.*
- **Vary rhythm.** Don't convert everything to bullets either; alternate short paragraphs, the occasional bulleted list, and a one-line callout. Uniform anything (all prose or all bullets) is the tell.

This is the default for personal/working briefings with substantial prose. For terse or already-list-shaped sources, leave them be.

## UI Consistency: type sizes & component styling

Inconsistent sizing across similar objects is the most common polish failure — two tables at different cell sizes, one card title at 14px and the next at 16px, a tagline larger on one tab than another. Pin the scale once and reuse it; never re-size an instance with an inline `style="font-size:…"`. If two things are the same kind of object, they share one class and render identically.

Use `design-guide`'s tokens — don't invent sizes. The type scale, spacing, radius,
elevation and motion are all CSS variables (`--text-*`, `--space-*`, `--radius-*`), so
consistency is enforced by *referencing the token*, never by re-typing a value. Hold
these constant across every tab (all sourced from `design-guide/assets/primitives.css`):

| Object | Token |
|--------|-------|
| Page `h1` | `--text-h1` (32/500) |
| Section `h2` | `--text-h2` (22/500) |
| Section + card titles | `--text-title` (16/500) — pick one, hold it |
| Tagline / lead paragraph | `--text-lead` (15/300) |
| Body, card description, table cells | `--text-small` (13/300) or `--text-body` (14/400) — pick one, hold it |
| Table headers, labels, meta | `--text-label` (11/500, uppercase) |
| Tag pills | `--text-pill` (10/500) |

Same rule for spacing: same component → same `--space-*` token (cards `--space-3`, section
bodies `--space-6`, container padding `--space-12`). Don't let one card breathe while its
neighbour is cramped. Before delivery, grep the output for inline `font-size`/`padding`/hex
in `style=""` — any hit is a consistency leak; move it onto the shared class/token.

## Critical Rule: Confidentiality of Meeting Transcripts

If any source markdown was derived from a meeting transcript, treat the transcript content as **confidential** when producing a shareable HTML report. Information from transcripts is *usable* — facts, decisions, positions, and themes can inform the output — but it must be rendered in a way that is **non-identifying and non-incriminating**.

Apply these rules whenever transcript-sourced content is included:

1. **No verbatim quotes attributed to a named person.** A line like `Olivier: "I think this is a waste of money"` must not appear, even if the source markdown contains it. Paraphrase to a neutral, third-person statement of the position.
2. **No attribution of opinions, scepticism, frustration, or political stance to a named individual.** Phrases like "Sotiri was sceptical of the brief", "Pete pushed back on Ro", "X feels bad about Y" must be reframed. Use neutral framings: "concerns were raised about…", "the team debated whether…", "an open question remains around…".
3. **Strip out side-channel commentary** — DM excerpts, post-meeting reflections, 1:1 frustrations, off-the-record asides. These are background context for the author, not content for a sharable artefact.
4. **Personnel / HR / leave / health details** — never include in a shared report (e.g. "X is out on carer's leave"), even if relevant to scheduling. Refer instead to capacity / timing in neutral terms if needed.
5. **Decisions and outcomes are sharable; the path to them is not.** "The team decided to broaden ADS scope to include bespoke engagements" is fine. "Pete had to push Ro for sign-off after weeks of ambiguity" is not.
6. **When in doubt, abstract up one level.** If a transcript names a specific stakeholder pushing a specific view, generalise to "stakeholder feedback indicated…" or "an emerging view across the team…".

The litmus test: **if this HTML ended up forwarded to one of the people quoted in the source transcripts, would they recognise themselves being characterised in a way they didn't sign off on?** If yes, rewrite.

This rule applies to *shareable* outputs (the default assumption for this skill). If the user explicitly states the output is for personal use only and will not be shared, the rule can be relaxed — but always confirm before doing so.

## Framing (shareable outputs)

The source markdown is the author's draft. Preserve its *meaning and phrasing*, but apply these framing rules before rendering. These are the corrections most often made by hand after the first version — bake them in so they don't have to be:

1. **"Partner", not "client".** Default to "partner". "Built with partners", not "delivered for clients" or "agents we run".
2. **Don't name third-party organisations** unless the source clearly intends them named for this audience. Generalise to a role/category — "a global recruiter", not the named company.
3. **Strip internal individuals and internal conflict** from shareable outputs. No "X pushed back on Y", no naming who disagreed. Relabel a named person's prototype/work to a neutral category. Decisions and outcomes are shareable; the politics behind them are not.
4. **Calibrate confidence down — don't overstate.** Prefer "Example" over "Live" unless verified; "Version 1 in use" over "Initial version"; "cloud flexible" over "cloud agnostic". Avoid absolute or aspirational claims the author would soften.
5. **Preserve the author's strategic phrasing — do not smooth or paraphrase it.** When the source states framing in specific words, lift them verbatim. Resist "improving" headlines or restating positions in your own words; that phrasing is deliberate, and re-dictating it is the single biggest source of rework on this skill.
6. **Plain-English headings, not AI-structured labels.** "What we are delivering", not "TWO OUTCOMES". Avoid ALL-CAPS abstractions and tidy taxonomic labels the author wouldn't write.
7. **Attribute provenance.** Name the origin of third-party tools/frameworks where it sets context (e.g. "Google's agents-cli").
8. **No internal working titles in the header.** Strip codenames and working labels (e.g. a trailing "— Framing") from the page header.

## Tone Gate (apply to the source markdown before converting)

This skill renders whatever prose it is given, so slop in the source ends up in a shareable artefact. **Load both writing skills as upfront context before the first content pass — not as a final lint.** They are independent siblings; neither invokes the other, so this skill loads each explicitly:

- **`remove-ai-tells`** (`../remove-ai-tells/SKILL.md`) — *always*. The canonical catalogue of AI writing tells (meta-tails, buzzwords, fill words, negated contrasts, em-dash density, bow sentences, the lot); it defines the De-Slop Pass: sweep, fix minimally, loop until a pass finds nothing new, delete-test the residue.
- **`write-guide`** (`../write-guide/SKILL.md`) — *optional*, the voice layer. Load it when the intake calls for an authored voice (details under the Voice-treatment bullet below).

Run the De-Slop Pass on the source markdown before converting. Skill-specific calibration:

- For the default **fact-based / minimal-sell** register, apply the full catalogue; for an explicitly persuasive register, the tonal rules soften but the hard bans (emoji, meta-tails, fabrication, and the near-zero exclamation default) still hold.
- **Dense-deck exception** (also stated in remove-ai-tells guardrails): bold subheadings inside dense sections are structure, not emphasis crutches — keep the typographic hierarchy.
- **Voice treatment (optional).** This skill looks for a sibling `write-guide` skill (`../write-guide/SKILL.md`) — an interchangeable, user-supplied voice profile (gitignored; swap in your own, or run with none). If it exists *and* the intake calls for an authored voice (personal essays, external comms), load it and its `references/AUDIENCE.md` and apply it to the source markdown *before* converting. If it is absent, skip voice treatment and rely on `remove-ai-tells` alone. Do not blanket-apply a personal voice to dense factual decks — take only its voice guidance; the tells catalogue always comes from `remove-ai-tells`.

**Second `remove-ai-tells` loop — the microcopy this skill writes itself.** The pass above cleans the *source* prose. But this skill authors new text that was never in the source and never went through the gate: taglines, section summaries, accordion titles, tab labels, callout labels, and connective phrasing. That generated microcopy is exactly where fresh tells reappear — catchy section labels, "TWO OUTCOMES"-style taxonomy, bow-tie taglines, meta-tails. Run the De-Slop Pass once more on the rendered prose before delivery, focused on the copy you wrote rather than the copy you carried over.

## Process

### Step 1: Read the design-guide skill and select a scheme

Load the `design-guide` skill first (`../design-guide/SKILL.md`) for the full design
system — token tiers, the four schemes, component vocabulary, and shared rules. All
output must conform to it.

From the intake, resolve the **scheme** = brand × format:

- **Brand** → palette: Quantium (`palette-quantium.css`) or wiq (`palette-wiq.css`).
- **Format** → implementation: Detailed (`detailed.css`) or Exec (`exec.css`).

Then inline the recipe for that scheme (see `design-guide/presets/README.md` for the
exact file order and the matching JS behaviour):

- **Detailed** — `primitives + spectrum + palette-{brand} + detailed.css`, with the
  `showPage` JS (one page visible at a time).
- **Exec** — `primitives + spectrum + palette-{brand} + exec.css`, with the
  tabs-as-anchors JS (all pages stacked; scroll down *or* click a tab to jump;
  scroll-spy highlights the active tab). Load **Inter** as well as Roboto.

The HTML class vocabulary is identical across schemes — build once, the scheme is a CSS +
JS-behaviour choice, not a markup change.

### Step 2: Read all source files

Read all markdown files in the target directory (or the specified files). Note:
- Each file becomes one tab
- The filename or top-level heading becomes the tab label
- Keep tab labels short (2-3 words max) for the nav bar

### Step 3: Analyse content and plan tabs

For each file, identify:
- **Tab name**: derived from filename or `# heading` (shorten to 2-3 words)
- **Page header**: `h1` + tagline from the file's opening context
- **Content blocks**: map each section to the right component type (see mapping below)
- **Key quotes**: any `> blockquote` content becomes a `.quote` block
- **Tables**: any markdown tables become styled `.info-table` or `.doc-table`
- **Lists**: bullet points become content within expandable `.master-section` accordions

### Step 4: Map content to components

Use the richest component that fits the content. Do not default everything to plain paragraphs.

| Markdown pattern | HTML component |
|-----------------|----------------|
| Key-value pairs, metadata | `.info-table` (two-column table, label + value) |
| Long sections with sub-points | `.master-section` expandable accordion with `.master-color-bar` |
| Blockquotes | `.quote` block (blue left border, italic) |
| Warning/caution content | `.warning-card` (orange border, amber background) |
| Positive findings / recommendations | `.tip-card` (green border, mint background) |
| Numbered action items / conversation starters | `.convo-card` with `.badge-num` circle badge (never bare `.num`) |
| Status items (done/pending/check) | `.action-table` with coloured status spans |
| Data tables | `.doc-table` (full-width, styled headers) |
| Tags / labels / categories | `.tag` pills (`.tag-blue`, `.tag-green`, `.tag-orange`, `.tag-violet`, `.tag-coral`, `.tag-cyan`) |
| Timeline / chronological events | `.timeline-item` with dot indicators |
| Items with severity/priority (risks, blind spots) | Custom card with `.badge-num` badge and coloured left border |
| "If X, then Y" response pairs | `.response-card` with `.prompt` header |

### Step 5: Build the HTML

Structure:

```
<!DOCTYPE html>
<html>
<head>
  - Meta, title, Google Fonts link (Roboto 300;400;500 — plus Inter 300;400;500;600;700 for Exec)
  - Full <style> block = the design-guide scheme recipe inlined (primitives + spectrum + palette + implementation)
</head>
<body>
  - <nav class="top-nav"> with title + tab buttons + date
  - One <div id="page-{id}" class="page"> per tab
    - Each contains <div class="container"> with content
  - <script> with showPage() and toggleMaster() functions
</body>
</html>
```

### Step 6: Apply design rules

These are non-negotiable:

1. **Load `design-guide` first** and follow its tokens, colour system, typography, and component patterns exactly for the selected scheme
2. **No emoji or Unicode decorative characters** — use CSS dots, colour bars, SVG chevrons
3. **Content fidelity per intake** — for personal/working briefings, no information loss (every fact, quote, table row, and bullet appears; 12 source bullets → 12 HTML bullets; 27 rows → 27 rows). For shareable/exec artefacts, curate to the audience and honour the size ceiling (see Content Fidelity above). Never fabricate to fill space.
4. **Vary the components** — do not make every section an identical accordion. Mix tables, cards, quotes, timelines, tip/warning cards. Each tab should feel distinct.
5. **First tab's first section open by default** (preference, not mandate) — set `class="master-section open"` and `style="max-height: none;"` on the body. If the intake or user prefers everything collapsed, render all sections closed instead.
6. **Assign spectrum colours to sections** — use `--q-blue`, `--q-cyan`, `--q-turquoise`, `--q-orange`, `--q-coral`, `--q-violet` for `.master-color-bar` elements, in order, cycling through the spectrum
7. **Tab nav scrolls horizontally** on mobile — add `overflow-x: auto` to `.top-nav`
8. **Date in nav** — include a date stamp (from source files or current date) right-aligned in the nav
9. **Page headers** — each tab gets an `h1` and a `.tagline` subtitle. The tagline/intro paragraph must span the same content width as the body below it. Do NOT cap it with a narrow `max-width` (e.g. `max-width: 760px`) while the tables and cards beneath run to the full container width — that leaves the intro looking oddly narrow against the content. Let the `.tagline` and any `.provenance`/lead paragraph inherit the container width (typically `max-width: 1040px` on `.container`); only constrain line length globally if the whole page uses a narrower measure.
10. **Entrance animations** — sections use `fadeUp` animation with staggered delays
11. **Density vs curation depends on audience** — for personal briefings, favour density: include more content in fewer clicks, use accordions to organise not gatekeep. For shareable/exec artefacts, favour curation: lead with the headline, fewer sections, cut what the audience won't read. Let the intake decide, not a blanket preference.

### Step 7: Build carefully by hand — no browser pass

The Playwright visual-spacing pass is **disabled for now** (it reliably hangs in this environment on browser install / `file:` blocking). Build the HTML carefully by hand against the component patterns above and deliver — no screenshot loop. If a visual pass is ever re-enabled, keep it to spacing and alignment only, never a redesign.

Guard against class-name collisions: never reuse a class name for two different components (e.g. a circular `.num` badge and a `.num` numeric table cell). A bare `.num` selector matches every element with that class, so a badge style silently reshapes every table cell into pills and collapses the layout. Scope such helpers (`.badge-num`, `td.num`) or give them distinct names.

## Tab Naming

Keep tab names to 2-3 words. If the markdown filename is `03-linkedin-posts-and-voice.md`, the tab name is "Voice & Posts". If the heading is "## Suggested Questions for the Catch-Up", the tab name is "Questions".

## Accordion / Tile Header (avoid the squashed-subhead bug)

Recurring bug: tile title and subhead render on one line (`Today's process (as-is)Manual, inbox-driven`). Cause: the subhead is a direct flex child of `.master-header`, so it sits beside the title. Fix: always wrap title + subhead in a `.master-heading-text` column — that wrapper's `flex-direction: column` is what stacks them.

```html
<div class="master-header" onclick="toggleMaster(this)">
  <span class="master-color-bar" style="background: var(--q-blue);"></span>
  <div class="master-heading-text">                          <!-- wrapper is mandatory, even with no subhead -->
    <span class="master-title">Today's process (as-is)</span>
    <span class="master-subhead">Manual, inbox-driven</span> <!-- drop this line if no subhead -->
  </div>
  <svg class="master-chevron" ...>...</svg>
</div>
```
```css
.master-header { display: flex; align-items: center; gap: 14px; }
.master-heading-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }  /* NEVER a row */
```

## Expand/Collapse JavaScript

Include the JS behaviour matching the selected scheme (both are in
`design-guide/presets/README.md`). **Detailed** uses `showPage` (one page visible at a
time) + `toggleMaster`, shown below. **Exec** instead uses the tabs-as-anchors behaviour
(all pages stacked; `showPage` smooth-scrolls to a section; an IntersectionObserver
scroll-spies the active tab) plus the same `toggleMaster` — copy that variant from the
presets README.

For Detailed, always include this JS at the bottom:

```javascript
function showPage(page, btn) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.top-nav-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('page-' + page).classList.add('active');
  btn.classList.add('active');
  window.scrollTo(0, 0);
  document.getElementById('page-' + page).querySelectorAll('.master-section').forEach((s, i) => {
    s.style.animation = 'none'; s.offsetHeight; s.style.animation = '';
    s.style.animationDelay = (0.1 + i * 0.08) + 's';
  });
}

function toggleMaster(header) {
  const section = header.closest('.master-section');
  const body = section.querySelector('.master-body');
  if (section.classList.contains('open')) {
    body.style.maxHeight = '0';
    section.classList.remove('open');
  } else {
    section.classList.add('open');
    body.style.maxHeight = body.scrollHeight + 'px';
    setTimeout(() => { if (section.classList.contains('open')) body.style.maxHeight = 'none'; }, 500);
  }
}
```

## Output

- Write the HTML file to the same directory as the source files, or to the user's specified path
- Filename: derive from the collection topic (e.g. `meeting-prep.html`, `research-brief.html`)
- If the source markdown files should be kept, keep them. If the user asked to "convert" them, keep both
- Report the output path and tab count when done

## Quality Checks

Before delivering, verify:
- [ ] Intake stated up front (audience, shareable?, register, size ceiling, anonymisation)
- [ ] Framing rules applied: "partner" not "client"; no un-cleared org or individual names; confidence calibrated; author's phrasing preserved verbatim
- [ ] Tone Gate run on source: `remove-ai-tells` De-Slop Pass completed (looped until a sweep found nothing new)
- [ ] Second De-Slop loop run on the microcopy this skill authored (taglines, summaries, tab/callout labels)
- [ ] Type scale consistent — one size per role across all tabs; no inline `font-size`/`padding` overrides
- [ ] Spacing pass NOT run automatically — only if the user explicitly asked for a visual check (and then over local HTTP, not `file://`)
- [ ] No class-name collisions — no class reused for two different components (e.g. `.num` badge vs `.num` table cell)
- [ ] No fabricated facts, URLs, or list items — every detail traces to the source
- [ ] For shareable outputs, size ceiling honoured and low-value sections cut
- [ ] Every source file has a corresponding tab
- [ ] No content was dropped — spot-check a few specific facts from each source file
- [ ] Tabs are in logical order (not necessarily alphabetical — use narrative flow)
- [ ] First tab provides context/overview if one exists
- [ ] All accordions expand/collapse correctly (JS is included)
- [ ] Every tile/accordion title and its subhead render on separate lines — none squashed onto one line (grep `master-subhead`; each must sit inside a `master-heading-text` wrapper)
- [ ] No hardcoded hex colours outside `:root` definitions
- [ ] No emoji or Unicode decorative characters anywhere
- [ ] Mobile-friendly: nav scrolls, content reflows

---
name: gws-slides-edit
description: "Google Slides: Edit presentations while preserving template formatting. Covers editing existing slides, creating new slides from template layouts, and duplicating slides."
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
---

# Edit Google Slides (Template-Safe)

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules.

## Core Principles

1. **Never create slides or shapes from scratch.** Always use existing layouts, placeholders, and elements as the foundation. This preserves the wiq template formatting (fonts, colours, backgrounds, footers).

2. **Think "copy-paste", not "build from scratch".** When a mock/draft slide exists, always **duplicate it first** (`duplicateObject`), then edit the copy. This is how a human would do it — copy the slide, then refine. Never try to recreate a slide's elements (images, shapes, text boxes) individually on a new blank slide. The API cannot copy embedded images between slides, but `duplicateObject` preserves everything.

3. **Always left-align or centre-align text.** Never use justified alignment — it spreads words out and looks bad on slides. When inserting text into placeholders, set `alignment: "START"` (left) or `"CENTER"`. Never `"JUSTIFIED"`.

4. **Everything must be human-editable.** After AI generation, every visible element on the slide must be clickable and editable by a human in the Google Slides UI. Layout-level decorative shapes (coloured bars, background rectangles) are NOT editable — they're locked to the layout. If you need a custom content zone (takeaway box, callout, footer), create it as a slide-level shape using `createShape`, not by populating a layout placeholder. If a layout has a decorative shape you don't need, hide it by setting its fill alpha to 0, then create a slide-level replacement.

5. **Use native bullets, not literal bullet characters.** Never insert `•`, `–`, or `-` as text characters for bullets. Use `createParagraphBullets` instead. Literal bullet characters break when text styles are updated (font, colour, size changes apply to the character itself). Native bullets are paragraph-level formatting that stays consistent.

## Template Library

This skill directory (`~/.claude/skills/gws-slides-edit/`) contains brand and validation reference files:

| File | What it covers |
|------|---------------|
| `brand.md` | Colour palette (Berry `#913199`, Charcoal `#3a474e`, etc.), Roboto typography rules, layout constraints |
| `catalog.md` | 12 categories of slide templates with source deck IDs, slide numbers, density/audience tags |
| `sources.md` | Source presentation IDs for the Master Template, Accelerator, Offsite, and Check-in decks |
| `validation.md` | Post-generation checklist: no-fly zones, text overlap, EMU math, font compliance |

### Master Template Deck (191 slides, 84 templates, 14 categories)
**https://docs.google.com/presentation/d/1TEJSnDcIpqN5do9pXKGVihtkG-EzpV8cEku4n-TGFfY/edit**
- **ID**: `1TEJSnDcIpqN5do9pXKGVihtkG-EzpV8cEku4n-TGFfY`
- Full template index: `/workspace/ai-slides/outputs/template_index.json`
- Per-category indexes with thumbnails: `/workspace/ai-slides/outputs/{category}/`
- For the complete template catalog and data model, read the `slides-shared` skill.

### Original wiq Brand Template (87 slides)
**https://docs.google.com/presentation/d/1WYgs-05ctkrCkzd9HHWrp6HWpIGgHo24hUXy48gWkLY**

Key wiq layouts (IDs vary per deck — always `get` the presentation first to find the correct IDs):
- `01.Blank` — Empty slide with wiq footer
- `05.Section Waves` / `06.Section Vector` — Section dividers
- `08.Content` — Standard content slide (Title + Body + Subtitle placeholders)
- `09.Subtitle, Content` — Content with subtitle
- `16.Two Columns` / `18.Three Columns` — Multi-column layouts
- `22.Statement Waves` / `23.Statement Vector` — Statement/quote slides

### AI Slide Pipeline (for full deck generation)

For building complete decks from a brief, use the `slides-*` skill chain instead of this skill:

| Skill | Purpose |
|-------|---------|
| `slides-shared` | Template index, data model, brand summary, visual QA patterns |
| `slides-plan` | Brief → deck outline with template picks |
| `slides-generate` | Copy master deck → prune → populate text → visual QA |
| `slides-polish` | Design iteration: inspect → diagnose → fix → verify loop |

Read `slides-shared` first. It references this skill (`gws-slides-edit`) for brand.md and validation.md.

### Brand Rules (from `brand.md`)
- **Font**: Roboto only (Light, Normal, Medium). No other fonts.
- **Body text**: Charcoal `#3a474e` — NEVER black `#000000`
- **White text**: Only on dark backgrounds (Berry, Charcoal, Ultramarine)
- **Shapes**: Rounded rectangles only — no sharp corners
- **Alignment**: Left (`START`) or centre (`CENTER`) — NEVER justified
- **Single body size per slide**: Don't mix body text sizes (headlines/footnotes excluded)
- **Emphasis**: Bold or Roboto Medium. For stronger: bold + Berry colour. No underlines or italics for emphasis.

### Programmatic Builds (full decks from scratch)
For building entire decks programmatically (not editing existing slides), a reference implementation exists at:
`~/.claude/skills/gws-slides-edit/build-commercial-ai-deck.py` (1124 lines)

This provides:
- EMU helpers: `inches(n) = n * 914400`, `pt(n) = n * 12700`
- Brand colour constants (BERRY, CHARCOAL, ULTRAMARINE, etc.)
- Helper functions: `create_shape()`, `text_style()`, `para_style()`, `build_textbox()`
- 12 slide builder functions as reference patterns

Use this script as reference ONLY when building a full new deck. For editing existing decks, always use the duplicate-and-edit patterns below.

## Step 0: Always Read the Presentation First

Before any edit, fetch the presentation structure to discover masters, layouts, slides, and element IDs:

```bash
gws slides presentations get --params '{"presentationId": "PRESENTATION_ID"}'
```

Parse this to find:
- **Layout IDs** — from `layouts[].objectId` and `layouts[].layoutProperties.displayName`
- **Slide IDs** — from `slides[].objectId`
- **Element IDs** — from `slides[].pageElements[].objectId`
- **Placeholder types** — from `pageElements[].shape.placeholder.type` (TITLE, BODY, SUBTITLE)

For detailed element info on a specific slide:

```bash
gws slides presentations pages get --params '{"presentationId": "PRESENTATION_ID", "pageObjectId": "SLIDE_ID"}'
```

## Pattern 1: Edit Existing Slide Text

Use `replaceAllText` scoped to a specific slide. This swaps text content while preserving all formatting.

```bash
gws slides presentations batchUpdate --params '{"presentationId": "PRESENTATION_ID"}' --json '{
  "requests": [
    {
      "replaceAllText": {
        "containsText": {"text": "Old text here", "matchCase": true},
        "replaceText": "New text here",
        "pageObjectIds": ["SLIDE_OBJECT_ID"]
      }
    }
  ]
}'
```

**Key points:**
- Always scope with `pageObjectIds` to avoid unintended changes on other slides
- `matchCase: true` prevents accidental matches
- For surgical edits to a specific element, use `deleteText` + `insertText` instead:

```bash
gws slides presentations batchUpdate --params '{"presentationId": "PRESENTATION_ID"}' --json '{
  "requests": [
    {
      "deleteText": {
        "objectId": "ELEMENT_ID",
        "textRange": {"type": "ALL"}
      }
    },
    {
      "insertText": {
        "objectId": "ELEMENT_ID",
        "text": "New content goes here",
        "insertionIndex": 0
      }
    }
  ]
}'
```

Inserted text inherits the style of the surrounding text / placeholder defaults.

## Pattern 2: New Slide from Template Layout

Create a slide using a layout already in the deck's master. The new slide inherits all template formatting.

```bash
gws slides presentations batchUpdate --params '{"presentationId": "PRESENTATION_ID"}' --json '{
  "requests": [
    {
      "createSlide": {
        "objectId": "my_new_slide_id",
        "insertionIndex": 5,
        "slideLayoutReference": {
          "layoutId": "LAYOUT_OBJECT_ID"
        }
      }
    }
  ]
}'
```

Then fetch the new slide to discover its placeholder element IDs:

```bash
gws slides presentations pages get --params '{"presentationId": "PRESENTATION_ID", "pageObjectId": "my_new_slide_id"}'
```

Then insert text into the placeholders:

```bash
gws slides presentations batchUpdate --params '{"presentationId": "PRESENTATION_ID"}' --json '{
  "requests": [
    {
      "insertText": {
        "objectId": "TITLE_PLACEHOLDER_ID",
        "text": "Slide Title",
        "insertionIndex": 0
      }
    },
    {
      "insertText": {
        "objectId": "BODY_PLACEHOLDER_ID",
        "text": "Body content here",
        "insertionIndex": 0
      }
    }
  ]
}'
```

**Key points:**
- `layoutId` must reference a layout already in the target deck's masters — check with `get` first
- `insertionIndex` is the zero-based slide position
- `objectId` is optional but useful for referencing the slide immediately after creation

## Pattern 3: Duplicate an Existing Slide (PREFERRED)

**This should be your default approach.** Think like a human: copy the slide, then edit the copy. This is the safest and most complete method — it preserves all shapes, images, formatting, and positioning that cannot be recreated via the API.

```bash
gws slides presentations batchUpdate --params '{"presentationId": "PRESENTATION_ID"}' --json '{
  "requests": [
    {
      "duplicateObject": {
        "objectId": "SOURCE_SLIDE_ID"
      }
    }
  ]
}'
```

The response returns the new slide ID in `replies[0].duplicateObject.objectId`. The duplicate is placed immediately after the source. Then use Pattern 1 to edit text on the copy.

**When to use this:**
- Slides with custom shapes, diagrams, or images beyond simple placeholders
- When you need a near-identical slide with only text changes
- When the visual layout is complex and would be impossible to recreate from a layout alone

## What to AVOID

| Don't | Why | Do instead |
|-------|-----|------------|
| `presentations.create` | Makes a blank deck with no template | Copy the template via Drive API, then edit |
| `createShape` with manual styling | Loses template fonts, colours, positioning | Use placeholders from layouts, or `duplicateObject` on existing shapes |
| `updateTextStyle` with colour/font overrides | Fights the template; creates visual inconsistency | Let text inherit from the placeholder/layout |
| `updateShapeProperties` with background colours | Overrides template theming | Only use for shapes you've intentionally designed |
| `createImage` to copy images between slides | Embedded image URLs are internal and not publicly accessible — `createImage` will fail | `duplicateObject` the entire source slide, then edit the copy |
| Justified text alignment | Spreads words out, looks bad on slides | Always use `START` (left) or `CENTER` alignment |
| Recreating elements individually on a new slide | Slow, lossy, and the API can't copy embedded images | Duplicate the source slide first, then edit |
| Literal bullet characters (`•`, `–`, `-`) | Break when text styles are updated — font/colour/size changes apply to the character | Use `createParagraphBullets` with `BULLET_DISC_CIRCLE_SQUARE` preset |
| Populating layout decorative shapes with content | Users can't click or edit layout elements in the slide view | Create slide-level shapes with `createShape`; hide layout shapes by setting fill alpha to 0 |

## Verification

### Visual check (thumbnail)

```bash
gws slides presentations pages getThumbnail --params '{"presentationId": "PRESENTATION_ID", "pageObjectId": "SLIDE_ID"}'
```

Returns a URL to a rendered PNG. Download and review to confirm formatting is preserved.

### Text extraction check

```bash
gws slides presentations get --params '{"presentationId": "PRESENTATION_ID"}' \
  | python3 ~/.claude/skills/gws-slides-edit/extract-slides-text.py
```

### Full validation checklist

For important/final slides, run through `this skill directory (`~/.claude/skills/gws-slides-edit/`)validation.md`:
- No-fly zone compliance
- Text overlap prevention (bounding box math)
- Typography: Roboto only, Charcoal body text, single size per slide
- Shape validation: rounded rectangles, palette colours only
- EMU gotchas: 1 inch = 914400 EMU, auto-fit disabled, reverse-order insertText

## Cross-Deck Template Copying

The Slides API has no cross-presentation "copy slide" operation. If the target deck doesn't have wiq layouts in its master:

1. **Option A:** Copy the wiq template via Drive API (`gws drive files copy`), then edit the copy
2. **Option B:** In Google Slides UI, use "Import Slides" from the template to bring layouts across
3. **Option C:** Duplicate an existing well-formatted slide within the deck and edit from there

## See Also

- `gws-slides` — Base Slides API reference (raw CLI)
- `gws-drive` — For copying/creating presentations from templates
- `slides-shared` — Full template index (191 slides), data model, brand summary
- `slides-plan` / `slides-generate` / `slides-polish` — AI deck generation pipeline
- `~/.claude/skills/gws-slides-edit/brand.md` — Full colour palette and typography rules
- `~/.claude/skills/gws-slides-edit/validation.md` — Post-generation QA checklist
- `~/.claude/skills/gws-slides-edit/build-commercial-ai-deck.py` — Reference implementation for programmatic full-deck builds
- `~/.claude/skills/gws-slides-edit/extract-slides-text.py` — Text extraction utility for verification
- Master Template (191 slides): `1TEJSnDcIpqN5do9pXKGVihtkG-EzpV8cEku4n-TGFfY`
- Original wiq Template (87 slides): `1WYgs-05ctkrCkzd9HHWrp6HWpIGgHo24hUXy48gWkLY`

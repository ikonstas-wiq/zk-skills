# Slide Generation Validation Checklist

Run through this checklist for EVERY slide generated via the Slides API. The most common issues are text overlap and no-fly zone violations.

## Pre-Generation

- [ ] Read `brand.md` — confirm you have the correct colour hex codes and font sizes
- [ ] Identify which catalog template you're using from `catalog.md`
- [ ] If replicating a source slide, fetch the raw JSON to get exact element positions:
  ```bash
  gws slides presentations get --params '{"presentationId": "ID"}' --format json \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d['slides'][INDEX], indent=2))"
  ```

## Layout Validation

### No-Fly Zone
- [ ] All content elements are within the safe area (check slide guides)
- [ ] Only footnotes (8pt Roboto Light) may appear in the margin zone, and sparingly
- [ ] Logo/branding elements are in their designated positions only

### Text Overlap Prevention
- [ ] **Calculate bounding boxes**: For every text element, verify that `transform.translateX + size.width` does not exceed the slide width (10in / 914400 EMU per inch)
- [ ] **Vertical stacking**: Verify that `transform.translateY + size.height` of element N is less than `transform.translateY` of element N+1
- [ ] **No overlapping shapes**: Check that no two elements occupy the same coordinate space
- [ ] **Table cells**: Verify column widths sum to table width and row heights accommodate text at the specified font size
- [ ] **Headline position is fixed**: Headlines must stay at the designated Y position regardless of content length (1 or 2 lines)

### Spacing
- [ ] Text padding inside shapes: 0.05in (0.13cm) on all sides
- [ ] Sufficient whitespace between elements (minimum 0.15in gap)
- [ ] Content does not shift up when headline is single-line

## Typography Validation

- [ ] **Font**: All text uses Roboto (Light, Normal, or Medium only)
- [ ] **Text colour**: Body text is Charcoal `#3a474e` — NOT black `#000000`
- [ ] **White text**: Only used on dark backgrounds (Berry, Charcoal, Ultramarine)
- [ ] **Font sizes**: Match the spec in `brand.md` (headline 22pt, subtitle 12pt, body min 8pt, footnotes 8pt)
- [ ] **Single body size per slide**: No mixed body text sizes on the same slide
- [ ] **Emphasis**: Bold or Roboto Medium for emphasis. Berry colour for strong emphasis. No underlines, no italics for emphasis.

## Shape & Visual Validation

- [ ] **Rounded rectangles only**: No sharp-cornered boxes. Use `ROUND_RECTANGLE` shape type.
- [ ] **Colours from palette**: Every fill, stroke, and text colour matches a value in `brand.md`
- [ ] **No yellow sticky notes left**: Remove any `#f3ea5d` elements before finalising

## Content Validation

- [ ] **Headlines**: Complete sentence, ideally 1 line, max 2 lines
- [ ] **Slide density matches tag**: Light slides have 1-3 elements, heavy slides use tables/charts
- [ ] **Consistent terminology**: Use wiq brand terms (wiqLABS, wiqRetail, etc.)

## Post-Generation Verification

After creating a slide via `batchUpdate`, verify it rendered correctly:

```bash
# Re-fetch and extract text to confirm content placed correctly
gws slides presentations get --params '{"presentationId": "ID"}' --format json \
  | python3 scripts/extract-slides-text.py
```

- [ ] All intended text appears in the extraction
- [ ] No text is truncated or missing
- [ ] Slide count matches expected

## Common Pitfalls

1. **EMU calculations**: Google Slides uses EMUs (English Metric Units). 1 inch = 914400 EMU. Always calculate positions in EMU.
2. **Text auto-fit**: Set `autofit.autofitType` to `NONE` and manually size text boxes. Auto-fit can shrink text unpredictably.
3. **Overlapping insertText requests**: When populating a slide, insert text in reverse order (last element first) to avoid index shifting.
4. **Missing paragraph styles**: Always set `paragraphStyle.alignment` and `textStyle` explicitly — don't rely on defaults.
5. **Table column widths**: Explicitly set each column width. Default distribution rarely matches the design intent.

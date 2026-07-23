# Source Presentations

These are the Google Slides presentations in the `slide-templates/inputs` Drive folder (`1DzvJ7Jz9rIopuMS6Tjx6yDq8yWnR_yJJ`) used to build this template library.

## Master Template

| Name | ID | Slides | Notes |
|------|----|--------|-------|
| wiq Presentation Template | `1WYgs-05ctkrCkzd9HHWrp6HWpIGgHo24hUXy48gWkLY` | 87 | Brand guide, starter slides, icons, graphics |

### Master Template Structure
- Slides 1-3: Title, index, feedback
- Slides 4-9: Title/section variations (image overlays)
- Slides 10-11: Section dividers
- Slides 12-13: Acknowledgement of Country (AU/NZ)
- Slides 14-29: Content layouts (subtitle, takeaway, picture, columns, statement/question)
- Slides 30-33: **Appendix 1** — Colour palette + formatting guidelines
- Slides 34-49: **Appendix 2** — Starter slides (Agenda, From>To, Horizons, Chevron, Gantt, 2x2, Exec Summary, etc.)
- Slides 50-73: **Appendix 3** — Icon library (20+ categories)
- Slides 74-83: **Appendix 4** — Graphics/image resources
- Slides 84-87: **Appendix 5** — "Our Role" mission slides

## Example Packs

| Name | ID | Slides | Type |
|------|----|--------|------|
| Retail Accelerator Hub — Commercial AI Overview | `1Somws2irVcdLfxGpjWrmtO4nQwRjlXa3YoxRS9Bq_Fw` | 8 | Product overview |
| wiqRetail F27 Strategy Offsite (submissions) | `1P09avANwwMgV12EcFhJg87sbQboJGJeVaGOoecMMWsA` | 78 | Strategy offsite |
| wiq Domain Monthly Check-in — wiqLABS | `1mE1oIYmgc6qtRAcWFh9FiPcVG_9ZFCdUkYJVCzXHkxc` | 68 | Monthly check-in |

## Extracting Slide Content

```bash
# Extract text from any presentation
gws slides presentations get --params '{"presentationId": "ID"}' --format json \
  | python3 ~/.claude/skills/gws-slides-edit/extract-slides-text.py

# Get raw JSON for a specific slide's layout/positioning
gws slides presentations get --params '{"presentationId": "ID"}' --format json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d['slides'][SLIDE_INDEX], indent=2))"
```

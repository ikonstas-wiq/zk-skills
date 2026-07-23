---
name: custom-gws-docs-format
version: 1.0.0
description: "Google Docs: Format a document with rich text, headings, bullets, tables, and links via batchUpdate."
metadata:
  openclaw:
    category: "custom"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-docs"]
---

# Format a Google Doc

> **PREREQUISITE:** Load `gws-docs` and `gws-shared` skills first.

Convert markdown or structured content into a richly formatted Google Doc using the `documents.batchUpdate` API. This skill covers headings, bold/italic, bullets, numbered lists, tables, hyperlinks, and paragraph spacing.

## Core Workflow

### 1. Create or clear a document

```bash
# Create new
gws docs documents create --json '{"title": "My Document"}'

# Clear existing content (get endIndex first via documents.get, then delete range)
gws docs documents batchUpdate --params '{"documentId": "DOC_ID"}' \
  --json '{"requests": [{"deleteContentRange": {"range": {"startIndex": 1, "endIndex": END_INDEX_MINUS_1}}}]}'
```

### 2. Insert text

All content is inserted via `insertText` requests. Build requests sequentially, tracking the current insertion index (starts at 1). Every text segment must end with `\n`.

```json
{"insertText": {"location": {"index": 1}, "text": "My Heading\n"}}
```

### 3. Apply formatting

After inserting text, apply formatting to the range using the start/end indices.

#### Headings

```json
{"updateParagraphStyle": {
  "range": {"startIndex": START, "endIndex": END},
  "paragraphStyle": {"namedStyleType": "HEADING_1"},
  "fields": "namedStyleType"
}}
```

Valid styles: `HEADING_1`, `HEADING_2`, `HEADING_3`, `HEADING_4`, `TITLE`, `SUBTITLE`, `NORMAL_TEXT`

#### Bold / Italic

```json
{"updateTextStyle": {
  "range": {"startIndex": START, "endIndex": END},
  "textStyle": {"bold": true},
  "fields": "bold"
}}
```

Combine fields: `"fields": "bold,italic"` with `{"bold": true, "italic": true}`

#### Bullet Lists

```json
{"createParagraphBullets": {
  "range": {"startIndex": START, "endIndex": END},
  "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"
}}
```

Presets: `BULLET_DISC_CIRCLE_SQUARE`, `BULLET_DIAMOND_DISC_SQUARE`, `BULLET_CHECKBOX`

#### Numbered Lists

```json
{"createParagraphBullets": {
  "range": {"startIndex": START, "endIndex": END},
  "bulletPreset": "NUMBERED_DECIMAL_ALPHA_ROMAN"
}}
```

Presets: `NUMBERED_DECIMAL_ALPHA_ROMAN`, `NUMBERED_DECIMAL_NESTED`

#### Hyperlinks

```json
{"updateTextStyle": {
  "range": {"startIndex": START, "endIndex": END},
  "textStyle": {"link": {"url": "https://example.com"}},
  "fields": "link"
}}
```

#### Paragraph Spacing

```json
{"updateParagraphStyle": {
  "range": {"startIndex": START, "endIndex": END},
  "paragraphStyle": {
    "spaceAbove": {"magnitude": 6, "unit": "PT"},
    "spaceBelow": {"magnitude": 6, "unit": "PT"}
  },
  "fields": "spaceAbove,spaceBelow"
}}
```

### 4. Insert a table

```json
{"insertTable": {
  "rows": 3,
  "columns": 4,
  "location": {"index": INSERT_INDEX}
}}
```

After inserting, re-read the document with `documents.get` to find the cell indices, then insert text into each cell using `insertText` at the cell's content start index.

## Building Requests Programmatically

For large documents, use a Python script to convert markdown into batchUpdate requests:

```python
import json, re

requests = []
idx = 1  # insertion index starts at 1

def add_text(text, style=None, bold_prefix=None):
    """Insert text and optionally apply heading style and bold prefix."""
    global idx
    full = text + '\n'
    requests.append({"insertText": {"location": {"index": idx}, "text": full}})

    if style:
        requests.append({"updateParagraphStyle": {
            "range": {"startIndex": idx, "endIndex": idx + len(full)},
            "paragraphStyle": {"namedStyleType": style},
            "fields": "namedStyleType"
        }})

    if bold_prefix:
        end = idx + len(bold_prefix)
        requests.append({"updateTextStyle": {
            "range": {"startIndex": idx, "endIndex": end},
            "textStyle": {"bold": True},
            "fields": "bold"
        }})

    idx += len(full)

# Example usage
add_text("Document Title", style="HEADING_1")
add_text("Section One", style="HEADING_2")
add_text("Attendees: Alice, Bob, Charlie", bold_prefix="Attendees:")
add_text("This is a normal paragraph.")

# Write to file and submit
with open('/tmp/requests.json', 'w') as f:
    json.dump({"requests": requests}, f)
```

Then submit:

```bash
gws docs documents batchUpdate \
  --params '{"documentId": "DOC_ID"}' \
  --json "$(cat /tmp/requests.json)"
```

## Key Rules

1. **Track the index.** Every character (including `\n`) advances the index by 1. Off-by-one errors break the whole batch.
2. **Insert before formatting.** Text must exist before you can style it — `insertText` first, then `updateParagraphStyle` / `updateTextStyle`.
3. **`fields` is required.** Every update request needs a `fields` parameter specifying which properties to apply. Omitting it causes a 400 error.
4. **Batch atomically.** If any request in a batch is invalid, the entire batch fails. Validate index math carefully.
5. **Clean markdown before inserting.** Strip `**`, `*`, `#`, `[]()` syntax — apply formatting via API requests instead of embedding markdown characters.
6. **Re-read after structural changes.** After inserting tables or deleting content, indices shift. Call `documents.get` to get updated indices before further formatting.
7. **Bold sub-headings in paragraphs.** For patterns like `"Attendees: Alice, Bob"`, insert as plain text, then apply bold to just the label portion using its character range.

## Finding Text Positions in an Existing Doc

To format text in an existing document, map content to indices:

```bash
gws docs documents get --params '{"documentId": "DOC_ID"}' | python3 -c "
import json, sys
doc = json.load(sys.stdin)
for el in doc['body']['content']:
    if 'paragraph' in el:
        text = ''.join(e['textRun']['content'] for e in el['paragraph'].get('elements', []) if 'textRun' in e)
        print(f'{el[\"startIndex\"]:5d}-{el[\"endIndex\"]:5d} {text[:120].strip()}')
"
```

## See Also

- [gws-docs](../gws-docs/SKILL.md) — Core docs API (create, get, batchUpdate)
- [gws-docs-write](../gws-docs-write/SKILL.md) — Simple plain text append

---
name: custom-gws-gmail-format
version: 1.0.0
description: "Gmail: Build and send/draft well-formatted HTML emails with correct encoding via the raw API."
metadata:
  openclaw:
    category: "custom"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-gmail"]
---

# Format a Gmail email (send or draft)

> **PREREQUISITE:** Load `gws-gmail` and `gws-shared` skills first.

Use this skill whenever composing an email that needs formatting (bullets, bold, structure) or when creating drafts/sending via the Gmail API. It avoids common encoding pitfalls.

## Encoding Rules

1. **ASCII-only subjects.** Never use em dashes, curly quotes, or other non-ASCII in the `Subject:` header. Replace:
   - `—` (em dash) with `-` (hyphen)
   - `–` (en dash) with `-`
   - `'` `'` (curly single quotes) with `'`
   - `"` `"` (curly double quotes) with `"`
2. **Always set `Content-Type: text/html; charset=utf-8`** for formatted emails.
3. **Always set `MIME-Version: 1.0`** header.
4. **Base64-encode with URL-safe alphabet** (`base64.urlsafe_b64encode`), decode to ASCII string for the `raw` field.
5. **Use `\r\n` line endings** between headers, and a blank `\r\n` before the body.

## HTML Body Template

Use clean, inline-styled HTML. Gmail strips `<style>` blocks, so inline styles only.

```html
<div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
  <p>Hi Name,</p>

  <p>Paragraph text here.</p>

  <ol>
    <li><b>Bold label</b> - description text.</li>
    <li><b>Bold label</b> - description text.</li>
  </ol>

  <ul>
    <li>Unordered bullet point.</li>
  </ul>

  <p>Closing paragraph.</p>

  <p>Thanks,<br>Zac</p>
</div>
```

### Formatting elements

| Element | HTML |
|---------|------|
| Numbered list | `<ol><li>...</li></ol>` |
| Bullet list | `<ul><li>...</li></ul>` |
| Bold | `<b>text</b>` |
| Italic | `<i>text</i>` |
| Link | `<a href="URL">text</a>` |
| Line break | `<br>` |
| Paragraph | `<p>text</p>` |
| Heading | `<h3 style="margin: 16px 0 8px 0;">text</h3>` |

### Escaping

Escape `&` as `&amp;` in body text (e.g. `B&R` becomes `B&amp;R`).

## Building the raw message (Python)

Always use a Python script to build the payload. Never try to inline base64 in shell.

```python
import base64, json

headers = (
    "To: recipient@example.com\r\n"
    "Subject: ASCII-safe subject line\r\n"
    "MIME-Version: 1.0\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    "\r\n"
)

body = """<div style="font-family: Arial, sans-serif; font-size: 14px;">
<p>Email body here.</p>
</div>"""

raw = base64.urlsafe_b64encode((headers + body).encode("utf-8")).decode("ascii")
payload = json.dumps({"message": {"raw": raw}})

with open("/tmp/gmail_payload.json", "w") as f:
    f.write(payload)
```

## Creating a draft

```bash
# Step 1: build payload with Python (above)
python3 /tmp/build_email.py

# Step 2: create draft
gws gmail users drafts create \
  --params '{"userId": "me"}' \
  --json "$(cat /tmp/gmail_payload.json)"
```

## Updating a draft

```bash
gws gmail users drafts update \
  --params '{"userId": "me", "id": "DRAFT_ID"}' \
  --json "$(cat /tmp/gmail_payload.json)"
```

## Sending directly

```bash
# Payload for send uses the same raw format but top-level key is "raw" not "message"
python3 -c "
import base64, json
# ... build msg as above ...
raw = base64.urlsafe_b64encode(msg.encode('utf-8')).decode('ascii')
payload = json.dumps({'raw': raw})
with open('/tmp/gmail_payload.json', 'w') as f:
    f.write(payload)
"

gws gmail users messages send \
  --params '{"userId": "me"}' \
  --json "$(cat /tmp/gmail_payload.json)"
```

## Adding CC / BCC

Add headers before the blank line:

```
Cc: person1@example.com, person2@example.com
Bcc: hidden@example.com
```

## Key Rules

1. **Always use Python to build payloads.** Never pipe `gws` output through `python3 -c` in a single shell command - the pipe breaks permission matching. Write to a temp file, then pass to `gws` separately.
2. **ASCII subjects only.** Non-ASCII in subjects causes mojibake (`a]"` instead of `-`).
3. **HTML for any formatting.** Plain text emails cannot have bullets, bold, etc. Use `text/html` whenever formatting is needed.
4. **Inline styles only.** Gmail strips `<head>` and `<style>` blocks.
5. **Escape ampersands.** `&` in body text must be `&amp;`.
6. **Confirm before sending.** Always show the user the draft content and get confirmation before calling `messages.send`.

## See Also

- [gws-gmail-send](../gws-gmail-send/SKILL.md) - Simple plain text send
- [gws-gmail](../gws-gmail/SKILL.md) - Full Gmail API
- [gws-shared](../gws-shared/SKILL.md) - Auth and global flags

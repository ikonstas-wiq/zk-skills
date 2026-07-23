---
name: custom-gws-chat
version: 1.0.0
description: "Google Chat: Find a group chat by participants and download message attachments (images/files)."
metadata:
  openclaw:
    category: "custom"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-chat"]
---

# Google Chat — find-by-participants and attachment download

> **PREREQUISITE:** Load `gws-chat` and `gws-shared` skills first.

Two recipes the base `gws-chat` skill doesn't cover, both discovered the hard way.

## Recipe 1 — Find a group chat by participants

`spaces.list` doesn't filter by member; you have to triangulate.

```bash
# 1. List GROUP_CHAT/SPACE the caller is in, sorted by lastActiveTime (newest first).
gws chat spaces list \
  --params '{"pageSize": 100, "filter": "spaceType = \"SPACE\" OR spaceType = \"GROUP_CHAT\""}' \
  --format json
```

Narrow by:
- `spaceType: "GROUP_CHAT"` for unnamed 3–8 person chats; `spaceType: "SPACE"` for named rooms.
- `membershipCount.joinedDirectHumanUserCount` — **includes the caller**. A "you + 3 others" chat shows `3` if the API excludes you, but in practice it usually includes you. Check both counts.
- `lastActiveTime` — useful when the user gives a date window (e.g. "Friday into today").

```bash
# 2. For each candidate space, list members.
gws chat spaces members list \
  --params '{"parent": "spaces/<SPACE_ID>", "pageSize": 50}' --format json
```

```bash
# 3. Resolve user IDs to names. NOTE: people.people.get returns mostly-empty
# records for users not in the caller's Contacts — emails come through for
# domain users but displayNames often don't.
gws people people get \
  --params '{"resourceName": "people/<USER_ID>", "personFields": "names,emailAddresses"}' \
  --format json
```

**Fallback when names don't resolve:** peek at a few messages and read sender context from the text itself ("Hi Ro, Zac. I'm just with Michelle…" usually tells you who's who faster than the People API).

```bash
# Date-filtered message peek
gws chat spaces messages list \
  --params '{"parent": "spaces/<SPACE_ID>", "pageSize": 30, "filter": "create_time > \"2026-05-08T00:00:00Z\"", "orderBy": "createTime desc"}' \
  --format json
```

Filter syntax uses `create_time` (snake_case) with RFC3339 timestamps. `orderBy` accepts `createTime asc|desc`.

## Recipe 2 — Download message attachments

Three gotchas, all of which produce unhelpful errors:

### Gotcha 1 — wrong `resourceName`

The download endpoint **does not accept** the human-readable attachment path:

```
spaces/<SPACE_ID>/messages/<MSG_ID>/attachments/<ATTACHMENT_ID>   ← REJECTED
```

It wants the base64 blob from `attachmentDataRef.resourceName`:

```
ClxzcGFjZXMvQUFRQXpBR0w4cTQvbWVzc2FnZXMvbTVkWkd1Rzh5Um8u…       ← USE THIS
```

You get this from the `messages.list` response — every attachment has both fields. Read `attachment[].attachmentDataRef.resourceName`, not `attachment[].name`.

### Gotcha 2 — `alt=media` is required

```bash
gws chat media download \
  --params '{"resourceName": "<BASE64_BLOB>", "alt": "media"}' \
  -o image.png
```

Without `"alt": "media"` the API returns `Invalid value for query parameter 'alt'. It must be set to "media"`.

### Gotcha 3 — `-o` must resolve inside cwd

`-o /workspace/Temp/foo.png` is rejected from another working directory with `resolves to ... which is outside the current directory`. `cd` to the target dir first:

```bash
cd /workspace/Temp/terminology_chat && gws chat media download \
  --params '{"resourceName": "<BASE64_BLOB>", "alt": "media"}' \
  -o img1.png
```

## End-to-end: bulk download all attachments from a chat window

```bash
# 1. Capture messages with attachments to JSON.
gws chat spaces messages list \
  --params '{"parent": "spaces/<SPACE_ID>", "pageSize": 100, "filter": "create_time > \"2026-05-08T00:00:00Z\""}' \
  --format json > /tmp/chat.json

# 2. Extract attachmentDataRef.resourceName + contentName pairs.
jq -r '.messages[]? | .attachment[]? | "\(.attachmentDataRef.resourceName)\t\(.contentName)"' /tmp/chat.json

# 3. Loop and download. Run from the destination directory.
mkdir -p /workspace/Temp/chat_attachments && cd /workspace/Temp/chat_attachments
i=0
jq -r '.messages[]? | .attachment[]? | .attachmentDataRef.resourceName' /tmp/chat.json | while read ref; do
  i=$((i+1))
  gws chat media download --params "{\"resourceName\": \"$ref\", \"alt\": \"media\"}" -o "attachment_${i}.png"
done
```

## Reading the downloaded images

PNG/JPG attachments can be opened directly with the Read tool — it renders them visually. No OCR step needed.

```
Read /workspace/Temp/chat_attachments/attachment_1.png
```

## Common pitfalls

| Symptom | Cause |
|---------|-------|
| `Invalid resource name: spaces/.../attachments/...` | Used human-readable path instead of base64 `attachmentDataRef.resourceName` |
| `Invalid value for query parameter 'alt'` | Missing `"alt": "media"` in `--params` |
| `--output ... resolves to ... outside the current directory` | `cd` to the destination dir before running, then use a relative `-o` filename |
| `people.people.get` returns only `etag` and `resourceName` | User isn't in caller's Contacts — fall back to reading sender attribution from message text |
| Membership count looks off by one | `joinedDirectHumanUserCount` semantics vary; cross-check by listing members |

---
name: slack
description: Efficient Slack connector usage — read, search, send, and draft messages. Auto-invoke whenever the user asks anything about Slack conversations, messages, or activity. Handles the critical channel_types gotcha, provides conversation ID shortcuts via metadata map, and optimises token usage.
---

# Slack: Efficient Connector Usage

Use this skill whenever the user asks to read, search, send, or draft Slack messages. Load it proactively — do not wait for the user to explicitly call `/slack`.

## Critical Rule: Always Set channel_types

`slack_search_public_and_private` defaults to **public channels only** despite its name. Every search call MUST include:

```
channel_types="public_channel,private_channel,mpim,im"
```

Without this, 80%+ of messages are invisible (all DMs, group DMs, private channels missing).

## Connector Access & Retry — do NOT declare Slack "broken"

Slack is the **claude.ai Slack MCP connector**, exposed as `mcp__claude_ai_Slack__*`
tools — **not** a CLI, not an env var, not a token you set. There is no `slack`
binary and no `SLACK_TOKEN` to find. If you (or a sub-agent) "can't find Slack",
it's almost always because the tool schemas aren't loaded yet, not because the
connector is down.

**Before ever concluding Slack is unavailable, do all of this:**

1. **Load the tools.** They are deferred — fetch the schemas with ToolSearch
   first:
   `ToolSearch("select:mcp__claude_ai_Slack__slack_search_public_and_private,mcp__claude_ai_Slack__slack_read_channel,mcp__claude_ai_Slack__slack_search_users")`
   Only after this are the tools callable. (Sub-agents must do this themselves —
   tool schemas do not inherit from the parent.)
2. **Health-check with a cheap real call**, e.g.
   `slack_search_users(query="me", response_format="concise")` or a tiny
   `slack_read_channel(channel_id="<known id from metadata_map>", limit=1,
   response_format="concise")`. A normal result = connector is up.
3. **Retry transient failures.** On a timeout / 5xx / empty-with-error, retry the
   **same** call up to 2–3 times (brief backoff) before giving up. A single empty
   or errored response is not proof Slack is down.
4. **Distinguish "no results" from "not working".** A `200` with zero messages
   means there genuinely is nothing in range — that is a valid result, **not** an
   outage. Report it as `searched: true, raw: 0`, never as "Slack unavailable".

Only after steps 1–3 still fail with connector/transport errors should you record
Slack as unreachable — and then say *"Slack connector returned errors after
retries"*, not *"Slack CLI/token not available"* (which is never the real cause).

## Conversation Shortcuts

Before searching by name, check `references/metadata_map.json` in this skill's directory. It maps conversation names, people, and group DMs to channel IDs.

**Resolution order:**
1. Read `metadata_map.json` — match on person name, channel name, or participant list
2. If no match, use `slack_search_channels` or `slack_search_users` to discover the ID
3. Once found, use `slack_read_channel` with the ID directly (far cheaper than searching)

**Examples:**
- "Check my DMs with Amy" → lookup "Amy Humburg" → `slack_read_channel(channel_id="D0675GQLH1C")`
- "Read the leadership trio" → match "Core platform/engineering leadership trio" → `slack_read_channel(channel_id="C02FARX9W0N")`
- "What's happening in ai-cos" → match "ai-cos" → `slack_read_channel(channel_id="C0AQUE4NLLF")`

**Group DM matching:**
Group DMs have no names in Slack. Match on participants or purpose. When the user says "the group with Saweng and Stef", scan participant lists for the best match.

## Reading Messages

### Direct read (preferred when you have an ID)

```python
slack_read_channel(
    channel_id="C02FARX9W0N",
    limit=20,
    response_format="concise"
)
# ~300-500 tokens — cheapest option
```

### With time range

```python
slack_read_channel(
    channel_id="C02FARX9W0N",
    oldest="1775000000",  # Unix timestamp
    latest="1776000000",
    limit=50,
    response_format="concise"
)
```

## Searching Messages

### Default search template

```python
slack_search_public_and_private(
    channel_types="public_channel,private_channel,mpim,im",  # ALWAYS
    query="your search here",
    limit=20,
    response_format="concise"
)
```

### Common search patterns

**Your recent activity:**
```
query="from:me after:2026-04-01"
```

**Topic in specific channel:**
```
query="budget in:nz-connected-buying from:me"
```

**Mentions of you:**
```
query="<@UMT19FMGU> after:2026-04-01"
```

**Threads only:**
```
query="is:thread from:me topic-keyword"
response_format="detailed"  # Need message_ts for slack_read_thread
```

**Files you shared:**
```
content_types="files"
query="from:me type:documents after:2026-01-01"
```

### Search modifiers

| Modifier | Example | Purpose |
|----------|---------|---------|
| `from:me` | Messages you sent | |
| `from:<@UID>` | Messages from specific user | |
| `in:channel-name` | Specific channel | |
| `is:thread` | Threaded messages | |
| `has:link` / `has:file` | Content filters | |
| `after:YYYY-MM-DD` | Date range start | |
| `before:YYYY-MM-DD` | Date range end | |

### Thread reading (two-step)

1. Search with `response_format="detailed"` to get `message_ts`
2. Read thread: `slack_read_thread(channel_id="...", message_ts="...")`

## Sending Messages

When sending messages on behalf of the user, ALWAYS load the `zk-write-guide` skill first for voice/tone.

```python
# Send to a channel
slack_send_message(
    channel_id="C02FARX9W0N",
    text="Message content here"
)

# Send to a person (use their DM ID from metadata map)
slack_send_message(
    channel_id="D0675GQLH1C",  # Amy Humburg DM
    text="Hey Amy, ..."
)
```

**Draft instead of send** — use when the user wants to review first:
```python
slack_send_message_draft(
    channel_id="C02FARX9W0N",
    text="Draft message content"
)
```

**Schedule a message:**
```python
slack_schedule_message(
    channel_id="C02FARX9W0N",
    text="Scheduled message",
    post_at="1776300000"  # Unix timestamp
)
```

**Safety rules for sending:**
- Always confirm with user before sending (never auto-send)
- For DMs, double-check you have the right person's ID
- Use drafts by default unless user explicitly says "send it"

## Token Budget Guide

| Use Case | Budget | Approach |
|----------|--------|----------|
| Quick check | 300-1,000 | Direct `read_channel` with known ID |
| Daily catch-up | 2,000-3,000 | 2-3 concise searches |
| Weekly summary | 5,000-8,000 | 3-5 concise + 1-2 detailed |
| Deep investigation | 8,000-15,000 | Concise scan + detailed + threads |

**Optimisation rules:**
1. **Start concise, go detailed selectively** — concise for scanning, detailed only for deep dives
2. **Direct read > search** when you have an ID (~300 tokens vs ~1,000)
3. **Combine filters** in one query instead of multiple searches
4. **Paginate sparingly** — 3-5 pages max unless specifically asked for more

## Response Format Selection

- **concise**: Initial exploration, scanning, known-channel reads. ~400-1,000 tokens/20 messages.
- **detailed**: Need full context, permalinks, or `message_ts` for threads. ~8,000-17,000 tokens/20 messages.

## Refreshing the Metadata Map

The metadata map may go stale as channels are created/renamed and people join/leave.

**To verify and refresh:**
1. Search recent activity: `from:me after:[30 days ago]` across all channel_types
2. Cross-reference channel IDs against the map
3. For new conversations, get IDs from search results (use `detailed` format)
4. For channels: `slack_search_channels(query="channel-name")`
5. For users: `slack_search_users(query="Person Name")`
6. Update `metadata_map.json` and set `last_updated` / `last_verified` dates

## When NOT to Use This Skill

- Creating Slack Canvases → use `slack_create_canvas` / `slack_read_canvas` / `slack_update_canvas` directly
- Non-Slack sources → use gws for Google, msgraph for Outlook, acli for Jira/Confluence

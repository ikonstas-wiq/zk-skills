---
name: generate-feedback
description: Generate constructive, evidence-based feedback for team members by analysing Slack conversations and meeting transcripts over a specified time period. Use when preparing periodic feedback reviews (typically 1, 2, or 4 weeks) for leaders, peers, direct reports and team members. Requires minimum 6 data points per person across multiple sources. Outputs separate markdown files per person with positive reinforcement and development opportunities aligned to their specific feedback areas.
---

# Team Feedback Generator

## Overview

Generate constructive, evidence-based feedback for team members by systematically analysing Slack conversations and meeting transcripts over a specified time period. Search for discussions about and with each person, validate sufficient data points exist (minimum 6), then synthesise feedback aligned to each person's specific development areas. Produces separate markdown files per person with positive reinforcement and constructive development opportunities.

## When to Use

Use this skill when:
- Preparing periodic feedback for direct reports or team members (typically 1, 2, or 4 weeks)
- Need evidence-based observations from multiple sources (meetings and Slack)
- Want structured feedback aligned to each person's specific development areas
- Require separate, well-organised feedback documents per person

Do not use when:
- Providing immediate, informal feedback after a single event
- Feedback is based solely on direct observation without digital footprint
- Formal performance reviews requiring HR templates or specific formats

## Companion Skills (load these proactively)

This skill delegates to five other global skills. Load them when the workflow reaches the relevant step — do not duplicate their logic here.

- **`slack`** — All Slack data collection. Provides the `channel_types` rule, conversation ID shortcuts via `metadata_map.json`, and search patterns. Replaces the older `connect-slack` skill.
- **`zk-write-guide`** — Tone and writing voice for the generated feedback prose. Load before writing the final per-person markdown so the feedback sounds like Zac, not generic AI.
- **`remove-ai-tells`** — Canonical catalogue of AI writing tells. Run its De-Slop Pass on each per-person markdown before delivery (sweep against the catalogue, fix minimally, loop until a pass finds nothing new).
- **`zk-leadership-guide`** — Leadership perspective and values context. Load to inform the framing of development opportunities (e.g. what "growth" looks like in Zac's leadership lens).
- **`mds-to-html`** — Final consolidation. Load at §7 to package all per-person markdown files into a single self-contained Quantium-branded HTML report with one tab per person.

## Invocation Parameters

When invoked, clarify the following if not provided:

**Time Period** (required): Retrospective period for evidence gathering.
- Common values: "1 week", "2 weeks", "4 weeks"
- Used to filter meeting transcripts and Slack messages
- If not provided, ask the user to specify

**Example invocations:**
- "Generate feedback for the last 2 weeks"
- "Create team feedback covering the past month"
- "I need feedback for my directs from the last week"

## Workflow

Follow this sequential workflow when invoked.

### Step 1: Validate Inputs

**Bundled reference files** (in `references/` directory):
1. `common-corrections.md` — Attribution rules and name disambiguation. **LOAD FIRST.**
2. `person_metadata.md` — List of people with feedback areas

**External paths:**
3. Meeting transcripts directory: `/workspace/meetings`
4. Feedback output root: `/workspace/ai-feedback`

**Companion skills** (load when relevant — see above):
- `slack`, `zk-write-guide`, `zk-leadership-guide`

Validation:
- Use the Read/Glob tools to check each reference file exists
- Verify `/workspace/meetings` contains YYYYMM subdirectories
- Confirm `/workspace/ai-feedback` exists (create if missing)

If any reference file is missing, report which one with its expected location and stop.

### Step 2: Determine Time Period

If the time period was not provided in the request, ask the user.

Calculate the date range:
- End date: today (or most recent available data)
- Start date: end date minus the specified period
- Convert to `YYYYMMDD` for directory filtering and `YYYY-MM-DD` for Slack date filters

Identify relevant meeting transcript directories:
- List subdirectories in `/workspace/meetings` matching `YYYYMM`
- Filter to those overlapping the date range
- Meeting files are named `YYYYMMDD_{MeetingName}.txt` or `.md`

### Step 3: Load Context and Attribution Rules

**CRITICAL: Load `references/common-corrections.md` FIRST** — before processing any evidence.

It contains:
- Attribution rules for multi-speaker meetings (only cite what people actually said)
- Forbidden language patterns ("leadership observed", "it was noted that")
- People requiring disambiguation (Charlotte Wilson vs Charlotte Middleton, Alex Jarnoux vs Alex Smyth)
- Project name corrections and context clues
- Softening framework for DISCUSSED evidence

**Person Metadata** (`references/person_metadata.md`):
- Parse the markdown table to extract per person: preferred name, first name, last name, role, feedback areas
- Build a lookup keyed by preferred name
- Cross-reference with `common-corrections.md` to flag people requiring disambiguation

### Step 3.5: Identify Recently Relevant Slack Channels

Before per-person Slack searches in §4.2, build a shortlist of channels from the `slack` skill's metadata map that are likely to contain feedback signal for the period.

**Source:** `~/.claude/skills/slack/references/metadata_map.json`. Read it once here so per-person searches can prefer reading channels directly (cheap) over brute-force searching (expensive).

**Process:**
1. Read `metadata_map.json` and scan the `channels`, `group_dms`, and `dms` blocks.
2. Match against the people in `person_metadata.md`:
   - **Direct match** — DMs and group DMs whose participant list contains one or more people being processed.
   - **Project match** — channels whose `name`, `topic`, or `purpose` references active workstreams from `person_metadata.md` feedback areas (e.g. "FinComm", "Connected Buying", "wiqLABS", "Stella", "CPI").
   - **Team match** — channels covering teams the people belong to (engineering, leadership, delivery, design).
3. Filter to channels likely active in the date range. The metadata map's `last_verified` date and any per-channel activity hints are the cheapest signal; `slack_read_channel` with the period's `oldest`/`latest` confirms.
4. Build a per-person shortlist: a small set of channel IDs to read directly in §4.2 before falling back to keyword search.

**Output of this step:** a working set of channel IDs grouped by person (or "all", for cross-team channels like `#wiqlabs-general`). Carry this into §4.2.

If the metadata map is missing or stale (older than 30 days), note it and proceed with keyword search only — do not block.

### Step 4: Process Each Person

For each person in `person_metadata.md`, run the following sub-workflow.

#### 4.1: Search Meeting Transcripts and Classify Evidence

**Distinguish two types of evidence — they are handled very differently in §4.4.**

**Type 1 — DIRECT PARTICIPATION:** person was present AND spoke.
- Their direct quotes, questions, proposals, decisions (lines marked `PersonName:`)
- Observable behaviours in meetings they attended

**Type 2 — DISCUSSED ABOUT:** person was discussed but not present (or didn't speak on the topic).
- Others assessing their performance, challenges, or development needs
- Leadership conversations about them
- Second-hand observations

**Classification process:**
1. Check the meeting participants list to determine if the person attended
2. If they attended, search for their direct statements (`PersonName:` lines)
3. Separately identify discussions ABOUT them by other participants
4. Tag each piece of evidence as `DIRECT` or `DISCUSSED`

**Search approach — name variations:**
- First name only ("Stef", "Stefan")
- Last name only ("Raovic")
- Full name ("Stefan Raovic", "Stef Raovic")
- Possessive ("Stefan's", "Stef's")

**Person disambiguation** (critical for similar names):
- Always check `common-corrections.md` first
- Use role/context clues to verify: "Charlotte" + FinComm/SOP context → Charlotte Wilson; "Alex" + FinComm/Melbourne → Alex Smyth
- When uncertain, check role and project context before attributing

**Search scope:** only files in `YYYYMM` directories within the date range. Search file contents, not just filenames. Each meeting file with mentions = 1 data point.

**For each piece of evidence, capture:** meeting date, topic, surrounding context, whether DIRECT or DISCUSSED.

#### 4.2: Search Slack Conversations

**Use the global `slack` skill for all Slack work.** Do not implement Slack search logic here — load the skill and follow its procedures.

The `slack` skill handles:
- The critical `channel_types="public_channel,private_channel,mpim,im"` rule (without it, ~80% of messages are invisible)
- Conversation ID shortcuts via its `metadata_map.json`
- Thread reading and search patterns
- Token-efficient response formats

**For each person, work in this order:**

1. **Read shortlisted channels** from §3.5 first — `slack_read_channel` against the channel IDs already identified as relevant (DMs, group DMs, project channels). This is the cheapest, highest-signal source.
2. **Their activity** — messages from the person, constrained to the feedback period:
   ```
   from:<person> after:YYYY-MM-DD before:YYYY-MM-DD
   ```
3. **Discussions about them** — name mentions in conversations during the period (only if §1 and §2 leave gaps).

Then read full thread context for any substantive thread (use `slack_read_thread` per the `slack` skill).

**Counting:** each distinct Slack thread = 1 data point. Do not double-count individual messages within the same thread.

**Capture:** message content, channel/DM, date, and whether the person was a participant (DIRECT) or being discussed (DISCUSSED).

#### 4.3: Validate Data Points

Total = (meeting files with mentions) + (distinct Slack threads).

**Threshold: 6.**

- If `< 6`: skip feedback generation, note in summary as "insufficient data" with the count.
- If `>= 6`: proceed.

#### 4.4: Analyse Against Feedback Areas Using Evidence Classification

Review all evidence in the context of this person's specific feedback areas. **Apply different analysis approaches based on evidence type.**

##### Handling DIRECT evidence

Use for direct, specific feedback about observable behaviours — concrete examples of what they said, proposed, or decided. Can be more direct in development feedback because it's based on their actual actions.

Phrasing patterns:
- "You demonstrated X when you..."
- "Your approach to Y showed..."
- "In discussions, you proposed..."
- "Your questions about Z revealed..."

##### Handling DISCUSSED evidence — EXTREME CARE

This evidence requires careful handling to avoid revealing leadership discussions or creating perception of "talking behind their back."

**For positive reinforcement:** can use freely. Frame as direct observations: "You've shown strength in X" (not "others noted you're strong at X").

**For development opportunities:** must heavily soften. Never use language suggesting this came from leadership discussion. Frame as growth opportunities and potential, not criticisms.

**Transformation example:**

❌ TOO DIRECT (reveals discussion about them):
> "You treat stakeholder statements as gospel rather than forming independent opinion. You say yes to everything and don't question requirements respectfully."

✅ APPROPRIATELY SOFTENED:
> "There may be an opportunity to further develop your product instinct around questioning requirements. As you move into product leadership roles, building the confidence to probe stakeholder requests — asking whether they align with strategic direction and represent optimal use of capacity — will strengthen your effectiveness. This isn't about being oppositional, but rather developing independent judgment about what should versus could be built."

**Language for DISCUSSED development feedback:**

Use:
- "There may be an opportunity to..."
- "Consider whether..."
- "As you develop X, strengthening Y could..."
- "Building capability in Z would..."
- "Further development of..."

Avoid:
- "You need to..." / "You must..."
- "The problem is..." / "You're not..."
- Anything that sounds like criticism or judgment

**The trust test:** would the person feel supported in their development, or feel criticized/exposed if they read this? If the latter, soften further.

See `references/common-corrections.md` for the full softening framework with worked examples.

##### Self-feedback exemption (Zac entry only)

If the person being processed is **Zac Konstas himself** (the `Myself` row in `person_metadata.md`), the curation rules above do **not** apply. Zac is reading his own feedback — there is no third-party trust risk. For the Zac entry only:
- Do not soften DISCUSSED evidence
- Do not strip attribution
- Be direct, specific, and unfiltered
- Still mark genuinely sensitive items `[TO REVIEW]` if they involve other named individuals' confidentiality

For everyone else, full curation per the rules above.

#### 4.5: Generate Feedback Content

Before writing the prose, **load the `zk-write-guide` skill** so the voice matches Zac's authentic style, and the **`remove-ai-tells` skill** for the De-Slop Pass to run on each finished draft. Optionally load `zk-leadership-guide` for framing of development opportunities.

Structure for each person:

**Positive Reinforcement** (minimum 2 points):
- Can use BOTH direct and discussed evidence
- Specific, evidence-based observations
- Reference the behaviour/outcome without revealing exact sources
- Connect to a feedback area from their metadata
- Genuine and substantive

**Development Opportunities** (minimum 1 point):
- **Heavily prefer DIRECT evidence** where possible
- For DISCUSSED evidence, apply the softening rules in §4.4
- Constructive, actionable, framed as growth potential
- Connect to a feedback area
- **Test:** does this risk revealing leadership discussions? If yes, soften further or discard

**Critical language rules:**
- NEVER use "leadership observed", "leadership noted", "it was observed", "feedback indicated", "others have noted", "the team noticed", "colleagues mentioned"
- ALWAYS use direct framing: "There's an opportunity", "Consider whether", "As you develop"
- Frame DISCUSSED evidence as developmental suggestions, not performance critiques

**Risky feedback handling:**
- For sensitive situations, personal matters, or anything that could identify other individuals inappropriately: include the feedback but flag with **[TO REVIEW]** for manual review before delivery
- Especially flag anything derived from leadership discussions about the person

#### 4.6: Reflect on Feedback Area Validity and Emerging Themes

After the evidence has been mapped to the existing feedback areas, step back and assess two things explicitly. **This section is for Zac's review, not for the person.** Its purpose is to keep `person_metadata.md` honest and current — feedback areas drift out of date as roles, scope and people grow.

**Question 1: Are the existing feedback areas still the right ones?**

For each of the person's listed feedback areas, classify it:

- **Still valid** — the area is still load-bearing; evidence shows it remains a genuine development edge.
- **Graduated** — the person has demonstrably grown past it; the area no longer reflects where the leverage is.
- **Superseded by role/scope change** — the role or context has shifted, so the area no longer applies as written.
- **Needs rephrasing** — the underlying intent is right, but the wording no longer fits how the person operates today; suggest a better phrasing.

Cite one or two pieces of evidence that support each classification.

**Question 2: Are there new themes emerging that aren't covered by the existing areas?**

Scan the cross-cutting observations and the unaligned evidence captured during §4.1 and §4.2. Surface any theme that:

- Recurs across multiple meetings, channels, or weeks
- Reflects a scope or role change since the feedback areas were last set
- Names a strength the person is developing organically that deserves an explicit area
- Names a blocker or edge the person has not been coached on yet

For each emerging theme, propose a concrete one-line feedback area phrased in the same style as the existing ones in `person_metadata.md`. Include the evidence base.

**Output:** capture the reflection as a "Feedback Areas Reflection" section in the per-person markdown (template in §5). Keep it concise — a few bullets per category is enough.

**Self-feedback (Zac):** apply the same reflection to your own feedback areas. Be especially honest about whether any have graduated.

### Step 5: Generate Output Files

**Output directory:** `/workspace/ai-feedback/feedback/YYYYMM/` (YYYYMM = month of generation). Create if missing.

**File naming:** `{YYYYMMDD}_{person}_feedback.md` (lowercase). Example: `20260503_stef_feedback.md`.

**File format:**

```markdown
# Feedback for {Full Name}
**Role:** {Role from metadata}
**Period:** {Start Date} to {End Date}
**Generated:** {Generation Date}

---

## Positive Reinforcement

### {Feedback Area 1}
{Specific observation with evidence-based context}

### {Feedback Area 2}
{Specific observation with evidence-based context}

[Additional positive points as warranted]

---

## Development Opportunities

### {Feedback Area}
{Constructive observation — softened if from DISCUSSED evidence (except for self-feedback)}

[Additional development points as warranted]

---

## Feedback Areas Reflection
*For Zac's review only — not delivered to the person.*

### Existing areas
- **{Area 1 verbatim}** — {Still valid / Graduated / Superseded / Needs rephrasing}. {One-line rationale with evidence.}
- **{Area 2 verbatim}** — {classification}. {rationale}
- **{Area 3 verbatim}** — {classification}. {rationale}

### Emerging themes worth considering
- **{Proposed new area, phrased in the same style as existing ones}** — {what the evidence shows, why it might be worth adding.}
- [Additional emerging themes as warranted, or "None identified this period."]

---

## Data Summary
- **Total data points analysed:** {count}
- **Meeting transcripts:** {count}
- **Slack conversations:** {count}
```

### Step 6: Generate Summary Document

After processing all people, create `_feedback_summary.md` in the same output directory:

```markdown
# Team Feedback Summary
**Period:** {Start Date} to {End Date}
**Generated:** {Generation Date}

---

## Overview
- **People processed:** {count}
- **Feedback generated:** {count}
- **Insufficient data:** {count}

---

## Generated Feedback Files

{List of people with feedback generated, linked to their files}

---

## Insufficient Data

{List of people skipped due to insufficient data points, with counts}

---

## Notes

{Any relevant observations about the generation run}
```

### Step 7: Consolidate into a Single HTML Report

After all per-person markdown files and `_feedback_summary.md` are written, package them into one tabbed HTML report.

**Invoke the `mds-to-html` skill** with the output directory as the argument:

```
/mds-to-html /workspace/ai-feedback/feedback/YYYYMM/
```

`mds-to-html` will:
- Use `_feedback_summary.md` as the Overview tab (people roster, sensitivity flags, sources/voice/process callouts).
- Create one tab per `{YYYYMMDD}_{person}_feedback.md` file, tab-labelled by preferred name.
- Render each feedback area as an expandable accordion with spectrum colour bars.
- Preserve all source content verbatim — quotes, dates, evidence references, data summaries.
- Output a single self-contained HTML at `<dir>/team-feedback.html`.

**Tab order:** Overview first, then Zac's self-feedback (if present), then the rest of the people roughly in the order they appear in `person_metadata.md`.

**Special handling:**
- Where a person's feedback contains verbatim quotes (e.g. Harrison's dad jokes), prefer rendering as numbered `convo-card` entries with date/source attribution.
- Recognition moments (promotions, awards) become `callout-bar` elements at the top of the relevant tab.
- The Overview tab should foreground the sensitivity flags as expandable accordions, with Charlotte/upward-feedback/self-feedback flags opened by default if any exist.
- The "Feedback Areas Reflection" section should render as its own collapsed master-section near the bottom of each tab, visually distinct (e.g. violet `--q-violet` colour bar) so it reads as a meta-review for Zac rather than as feedback for the person. Include the "for Zac's review only" note in the section header.

Report the final HTML path back to the user alongside the markdown summary.

## Feedback Guidelines

### Evidence Classification and Handling (recap)

**DIRECT PARTICIPATION** — person was present and spoke. Handle with direct, specific, observation-based feedback.

**DISCUSSED ABOUT** — others discussed the person without them present. Heavily soften, generalise, and frame as developmental opportunities. Protect confidentiality of leadership conversations.

**Risk:** if feedback reveals leadership discussed someone behind their back, it damages trust and signals a political environment. Self-feedback (Zac) is exempt — see §4.4.

### Constructive and Direct

- Be honest about observations
- Frame development as growth potential, not deficiencies
- Direct language with professional respect
- Avoid sugar-coating *and* harshness
- Direct evidence supports direct feedback; discussed evidence requires gentler framing

### Evidence-Based Without Revealing Sources

- Reference behaviours and outcomes from the evidence
- Do not cite specific meeting names, dates, or channel names
- Do not identify other people by name in the feedback
- Use general framing: "In team discussions..." not "In Monday standup with Stefan..."
- Convert leadership discussion → developmental framing (see softening framework in `common-corrections.md`)

### Attribution Language

**FORBIDDEN** (reveals third-party discussion):
- "Leadership observed/noted/identified/discussed..."
- "It was observed that..."
- "Feedback indicated..."
- "Others have noted..."
- "The team noticed..."
- "Colleagues mentioned..."

**APPROVED** (direct observation):
- "There's an opportunity to..."
- "Consider whether..."
- "In discussions, you..." (only if they were actually present)
- "The pattern noted is..." (if genuinely observable)
- "As you develop X, strengthening Y could..."
- "Building capability in Z would..."
- "You've demonstrated X" / "The challenge is Y"

### Differentiated Redaction Rules

**Positive reinforcement:**
- Can be more specific about situations and context
- More latitude to describe what went well
- Use both direct and discussed evidence freely
- Focus on observable outcomes and impacts

**Development opportunities:**
- Strongly prefer DIRECT evidence
- For DISCUSSED evidence: avoid language that could embarrass or expose, frame constructively, remove all traces of third-party discussion, generalise if specific enough to identify exact sources, apply the softening framework

### Risky Feedback Handling

Mark `[TO REVIEW]` when feedback involves:
- Sensitive interpersonal dynamics
- Performance issues that might be contentious
- Situations that could identify specific individuals inappropriately
- Personal matters beyond professional development
- Anything that crosses a professional boundary
- ANY DISCUSSED-derived development feedback that feels harsh or exposing

### Alignment to Feedback Areas

Each piece of feedback must connect to one of the person's specific feedback areas in `person_metadata.md`. If an observation doesn't align, consider whether it's relevant.

### Authenticity (use `zk-write-guide`)

- Load the `zk-write-guide` skill before writing the final prose
- Run the `remove-ai-tells` De-Slop Pass on each per-person file before delivery — loop until a sweep finds nothing new
- Avoid corporate buzzwords and clichés
- Match Zac's leadership style: direct, pragmatic, outcome-focused
- Maintain a supportive developmental tone even when addressing gaps

## Examples of Evidence Handling

### Example 1: Direct Participation (can be direct)

**Evidence:** In sprint planning, Charlotte facilitated workshop discussion and took on SOP translation work.

**Feedback (appropriate):**
> "Your willingness to take on challenging facilitation responsibilities for the workshops shows growing ownership mindset. When assigned the SOP translation experiment, you moved forward with time-boxed experimentation rather than getting paralysed by uncertainty."

### Example 2: Discussed About (must soften)

**Evidence (leadership meeting):** "Michelle said Charlotte doesn't critically question requirements, just says yes to everything stakeholders ask for."

❌ **TOO DIRECT** (reveals discussion):
> "You treat stakeholder statements as gospel rather than forming independent opinion. You say yes to everything and don't question requirements."

✅ **APPROPRIATELY SOFTENED:**
> "As you develop product leadership capability, there's an opportunity to strengthen your critical questioning of requirements. Building the confidence to respectfully probe stakeholder requests — asking whether they align with strategic direction and represent optimal use of limited capacity — would enhance your effectiveness in product roles. This isn't about being oppositional, but rather developing independent judgment about priorities and trade-offs."

### Example 3: Mixed Evidence (blend carefully)

**Direct:** Charlotte attended a meeting about stakeholder engagement strategy.
**Discussed:** Michelle discussed Charlotte's pattern of attending meetings where Ben is already present.

❌ **TOO REVEALING:**
> "You attended a meeting with Carly Richards for an hour despite being advised not to go because Ben was there, showing poor judgment about stakeholder positioning."

✅ **APPROPRIATELY HANDLED:**
> "There's an opportunity to be more strategic about stakeholder engagement. As you build product ownership, developing judgment about which meetings require your presence versus where colleagues already represent wiqLABS effectively would help you invest deeply in your core priorities. Consider partnering more closely with leadership on stakeholder coordination to ensure your time creates maximum impact."

## Resources

### Companion skills (loaded at runtime, not bundled)

- **`slack`** — Slack data collection. Provides `channel_types` rule, conversation ID map, thread handling. Load before §3.5 to read `metadata_map.json`, then again at §4.2 for per-person searches.
- **`zk-write-guide`** — Writing voice. Load before §4.5 prose generation.
- **`zk-leadership-guide`** — Leadership perspective for development framing. Optional, useful at §4.5.
- **`mds-to-html`** — HTML consolidation. Load at §7 to package the per-person markdown into a single tabbed Quantium-branded HTML report.

### Bundled reference files (`references/`)

#### `common-corrections.md`
Critical attribution rules and disambiguation guidance. **Load FIRST in §3** before processing any evidence. Contains: attribution rules for multi-speaker meetings, forbidden language patterns, Charlotte/Alex disambiguation, project name corrections, the softening framework with worked examples.

#### `person_metadata.md`
Markdown table defining who to generate feedback for. Columns: Person (preferred name), First Name, Last Name, Role, Feedback Areas (`<br>`-separated bulleted list). Loaded at the start of §3 to determine the iteration set and feedback areas.

### External paths (must exist on the host)

- **Meeting transcripts:** `/workspace/meetings`
  - `YYYYMM/` subdirectories
  - Files: `YYYYMMDD_{MeetingName}.txt` or `.md`
- **Feedback output:** `/workspace/ai-feedback`
  - Skill creates `feedback/YYYYMM/` as needed

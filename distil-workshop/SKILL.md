---
name: distil-workshop
description: Unpack a workshop, strategy day, or offsite from its meeting folder (transcripts, whiteboards, prep docs, slides) into topic markdown files and a consolidated tabbed HTML debrief via mds-to-html. Use when asked to "unpack the day", distil a workshop, or turn a multi-session meeting folder into a leadership debrief.
argument-hint: "<meeting folder path> [supplementary doc links]"
---

# Distil Workshop

Turn a workshop or strategy day's raw materials into a set of topic markdown files plus a consolidated, tabbed HTML debrief. The skill orchestrates; the heavy lifting (confidentiality, tone, components) lives in `mds-to-html`, `remove-ai-tells`, `zk-write-guide` and `design-guide` (the token + component design system that replaced `q-html`/`wiq-html`) — defer to them, do not duplicate their rules here.

## Principle: ask before churning

Do NOT assume and start processing. After the source inventory (Step 1), pause and confirm intake with the user via `AskUserQuestion` (Step 2) before reading transcripts in depth or writing anything. A wrong guess on audience, scope, or missing sources wastes the whole run.

## Step 1: Inventory the meeting folder

The folder is usually under `/workspace/Meetings/<yyyymm>/<yyyymmdd>/<slug>/` (translate pasted Mac paths: `/Users/isaack/Projects/` → `/workspace/`). Per session subfolder, meet-agent typically leaves `transcript.txt`, `summary.md`, `analysis.md` (frontmatter has participants, topics, quality warnings). Also look for:

- `whiteboards/` or image files (photos of post-it boards, flipcharts)
- An `outputs/` directory (create if missing — topic mds and the HTML go here)
- Any PDFs, slides, or docs already in the folder

List what was found and what seems missing (e.g. "morning session has a transcript, afternoon doesn't").

## Step 2: Intake questions (blocking — use AskUserQuestion)

Ask before processing. Cover, in one or two rounds:

1. **Supplementary sources**: are there slides, prep docs (Google Docs links), Slack threads, or whiteboard photos not in the folder? For prep docs, confirm their role — usually supplementary context and fact validation, not assumed discussion content.
2. **Audience and shareability**: who reads the debrief (the people in the room? wider team? execs?), which drives the confidentiality and curation rules in `mds-to-html`.
3. **Tab structure**: propose a tab list (overview → 3-5 topic tabs → decisions/next steps; 5-7 max) derived from the summaries' topics, and let the user adjust before writing.
4. **Anything to emphasise or exclude** (sensitive announcements, names, politics).

## Step 3: Gather and validate sources

- **Transcripts**: read in full (paginate large ones). Meet-agent `summary.md`/`analysis.md` give the skeleton; the transcript gives the substance and phrasing.
- **Whiteboard photos**: photos are often rotated — straighten before reading (`magick <f> -rotate 90 rot90_<f>`), Read the rotated copies, extract every note, then delete the rotated temp files.
- **Google Docs prep files**: fetch via `gws` (load `gws-shared` first). Gotcha: `gws docs documents get` takes the ID inside params, not as a flag: `--params '{"documentId": "<id>", "includeTabsContent": true}'`. Extract per-tab text with a small Python pass over the JSON.
- **Names — never trust the transcript.** Meet-agent invents or mangles names (e.g. "Alec Noble" for Alex Jarnoux). Pull the day's calendar invite (`gws calendar events list` with `calendarId`, `timeMin`/`timeMax`, `singleEvents`) and treat accepted attendees as ground truth. Flag transcript participants who are not on the invite rather than guessing; transcripts may also use a generic speaker label (e.g. "Fuel Tank") that is not a person. Check `memory/` for known name mappings.
- **Dates**: anchor on the calendar invite / prep doc date, not transcript header dates (recordings are often stamped a day off).

## Step 4: Write the topic mds

Load `zk-write-guide` and `remove-ai-tells` before drafting. Write one md per agreed tab into `<meeting-folder>/outputs/`, numbered for order (`01-overview.md`, ...). Conventions that worked:

- **Overview tab**: when/where/facilitator/attendees (invite-verified), structure of the day (one line per segment), the headline alignments (often a closing pulse-check playback in the transcript), and what happens next.
- **A whiteboard tab** (if an exercise like Continue/Start/Stop ran): full extraction grouped by theme, enriched with the discussion around each cluster — lossless on the notes themselves.
- **Decisions/next steps tab**: decisions, an actions table with owners, and open questions deliberately left for follow-up.
- Apply transcript confidentiality from `mds-to-html` even at the md stage: decisions shareable, attributed criticism/politics not, sensitive engagements neutralised.
- Run the De-Slop Pass on the mds before converting.

## Step 5: Consolidate

Invoke `/mds-to-html` on the outputs directory, stating the intake (audience, shareable, register, tab count) confirmed in Step 2. The HTML lands in the same `outputs/` directory.

## Step 6: Report and iterate

Report the outputs (md list + HTML path + tab count) and the key findings as a TLDR. Expect correction rounds (names, owners, formatting) — apply each correction to BOTH the md and the HTML so they stay in sync, and save durable corrections (e.g. name mappings) to memory.

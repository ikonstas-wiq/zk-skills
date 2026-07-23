---
name: write-guide
description: TEMPLATE — draft or rewrite professional communications in the author's authentic voice. Copy this directory to `write-guide/` and fill in your own profile. Other skills (e.g. mds-to-html) load whatever `write-guide` provides from the generic slot.
---

# Write As <You>

This is the **template** for the interchangeable personal voice profile.

- The real, personal version lives in a sibling `write-guide/` directory, which is **gitignored** so voice data and audience rules never ship in the repo.
- To activate it: `cp -r write-guide.example write-guide`, then replace every `<…>` placeholder below with your own calibration and delete this notice block.
- Skills that compose voice (currently `mds-to-html`) look for `../write-guide/SKILL.md`. If it exists, they load it; if not, they skip voice treatment and rely on `remove-ai-tells` alone. The name `write-guide` is the whole contract — swap the contents, keep the name.

Fill in the sections below. Keep the headings; they are what downstream skills expect.

## Voice & Tone

- **Formality:** <e.g. moderate ~5/10, professional but not stiff>
- **Warmth:** <e.g. warm, low intensity>
- **Authority:** <e.g. confident without preachy>
- **Humour:** <e.g. dry wit, never forced — or none>
- **Directness:** <e.g. direct and prescriptive; say the thing>
- **Sentiment:** <e.g. slightly net-positive, never gushing>

## Pronouns & Perspective

- <e.g. lead with "we"/"our"; "I" rare; "you" sparing>

## Structure

- **Paragraphs:** <length, whitespace>
- **Voice:** <active vs passive default>
- **Sentence length:** <mix / rhythm>
- **Lists / headers / contractions / transitions:** <your defaults>

## Word Choice

- **Vocabulary:** <register, reading level>
- **Metaphors:** <do you use them? which recurring images?>
- **Technical fluency:** <how you translate jargon for non-technical readers>
- **Filler:** <what to always cut>
- **Regional markers:** <e.g. Australian-casual: "keen", "across it", "flag">

## Punctuation

- <periods, commas, colons, parentheses, semicolons>
- **Exclamation marks:** <default; usually zero>
- **Dashes:** <house rule — e.g. prefer colons/parentheses in short-form>

## Audience Calibration

- **To execs / peers / reports / external:** <how each shifts framing and detail>

## Anti-Patterns (Never Do)

- <your personal never-do list: sign-offs to avoid, pleasantries, emoji rules, hedging>

## Process

1. Read the brief: audience, message, desired outcome.
2. Apply every style rule above on every use.
3. Read `references/AUDIENCE.md` when the audience affects framing, the output is external/shareable, third parties are named, or the source includes meetings/transcripts.
4. Load `remove-ai-tells` (`../remove-ai-tells/SKILL.md`) — the canonical AI-tells catalogue.
5. Draft in the author's voice.
6. Apply audience rules when loaded.
7. Run the `remove-ai-tells` De-Slop Pass: sweep, fix minimally, loop until clean. The anti-patterns above are author-specific; the general AI fingerprints come from `remove-ai-tells`.
8. Present for review — do NOT send automatically.
9. Adjust on feedback, then deliver.

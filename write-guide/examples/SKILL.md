---
name: write-guide
description: TEMPLATE — draft or rewrite professional communications in the author's authentic voice. Once populated, this lives at write-guide/SKILL.md. Other skills (e.g. mds-to-html) load whatever `write-guide` provides from the generic slot.
---

# Write As <You>

<!--
HOW WE POPULATED THIS (for an Agent calibrating the real write-guide profile).
This records the method used to fill the real profile so it can be rebuilt for a new author.

1. Assemble a corpus of the author's OWN writing — prefer things they wrote unedited and sent themselves:
   sent Gmail/Outlook (gws/msgraph), their Slack messages ("from:me"), authored docs and PR descriptions.
   Skip co-authored, templated, or forwarded content — it is not their voice.
2. Confirm identity, pronouns, and the audiences they write to WITH the author — never infer from a name.
3. Fill each heading from OBSERVED patterns, not aspirations: derive formality/warmth/authority from tone;
   set punctuation rules by counting real habits (e.g. em-dash frequency, exclamation marks ~ zero,
   Australian-casual markers like "keen"/"across it"/"flag"); build the anti-patterns list from tics
   they consistently avoid.
4. Where the corpus is thin or a signal is ambiguous, ASK the author rather than guessing — voice errors
   are immediately obvious to them and cheap to correct up front.
5. Replace every <…> placeholder, delete this comment and the "activate it" block below, keep the headings
   (downstream skills expect them), and save to ../SKILL.md — i.e. write-guide/SKILL.md, one level up from
   this examples/ folder (gitignored — never commit).
-->

This is the **template** for the interchangeable personal voice profile.

- **Where this lives once populated:** `write-guide/SKILL.md` — one level up, in the root of this skill folder. (The companion `examples/AUDIENCE.md` goes to `write-guide/references/AUDIENCE.md`.)
- The real, personal versions are **gitignored** so voice data and audience rules never ship in the repo; only this `examples/` folder is committed.
- To activate, from the `write-guide/` folder: `cp examples/SKILL.md SKILL.md` and `cp examples/AUDIENCE.md references/AUDIENCE.md`, then replace every `<…>` placeholder with your own calibration and delete this notice block.
- Skills that compose voice (currently `mds-to-html`) look for `write-guide/SKILL.md`. If it exists, they load it; if not, they skip voice treatment and rely on `remove-ai-tells` alone. The name `write-guide` is the whole contract — swap the contents, keep the name.

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
4. Draft in the author's voice.
5. Apply audience rules when loaded.
6. Present for review — do NOT send automatically.
7. Adjust on feedback, then deliver.

This skill owns voice only. Removing AI tells is a separate concern handled by the `remove-ai-tells` skill, which surfaces on its own for prose tasks — this skill does not invoke it.

# Remove AI Tells

This directory contains an Agent Skill for detecting and removing patterns that make prose read as AI-generated.

## Pieces

- `SKILL.md` is the agent workflow. It explains when to load the references and how to run the De-Slop Pass.
- `references/TELLS.md` is the portable, voice-neutral detection catalogue. Put general AI-writing patterns here.
- `references/VOICE.md` is the portable positive-writing baseline. Put broadly reusable guidance about what good prose should sound like here.

## Personal writing styles

Keep personal voice and audience preferences in a separate skill. Compose that skill with `remove-ai-tells`: use the personal skill while drafting, then run the De-Slop Pass as the final prose-quality gate.

The `zk-write-guide` skill is one example. This separation keeps the tell catalogue and minimum positive baseline portable for any user.

Do not let a personal style override factual-integrity rules such as the ban on fabricated facts, links, names, or sources.

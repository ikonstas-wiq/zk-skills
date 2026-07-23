# AI Tells — The Catalogue

A reference catalogue of the lexical, rhetorical, structural, tonal, and typographic patterns that mark prose as AI-generated. This is the checklist the De-Slop Pass (see `../SKILL.md`) sweeps a draft against.

The catalogue is **voice-neutral** — it only lists what to remove. Positive voice rules (how the finished prose should read) live in `VOICE.md`; load that alongside this file when writing.

The examples below use neutral placeholder content. Where a rule shows a `before → after`, the "before" is the tell and the "after" is the fix. Quoted call-outs (e.g. *"…is catchy AI slop, remove it"*) are real editorial corrections, kept because they capture the instinct better than a paraphrase would.

## 1. Hard bans (zero tolerance)

- **Exclamation marks — default zero, sparingly for impact only.** At most one per piece, earned by genuine emphasis; never stacked, never for false enthusiasm, never in formal reports or HTML artefacts.
- **Emoji and decorative Unicode** (✅ → ★ 🚀) in emails, docs, reports, HTML artefacts. Chat/instant-message contexts only, sparingly. In HTML use CSS dots, colour bars, SVG — never glyphs.
- **Meta-explanatory tails.** Sentences that explain the doc's posture instead of doing the work: "Deliberately non-prescriptive — we haven't decided yet", "This is just a starting point", "Open to feedback", "Designed to spark discussion, not foreclose it". End at the substantive clause. Watch the shape: *[substantive clause]. [Adverb], we [haven't/aren't] Y.* — the second sentence is almost always cuttable.
- **Catchy slop labels and chatty interjections.** "The trap", "The kicker", "The throughline" / "The through line", "Spoiler:", "Here's the thing", "Here's where it gets interesting", "The result? Transformative." Verbatim call-out: *'"The trap" is catchy AI slop, remove it.'* These coined section labels manufacture a punchline the author never set up — use a plain heading or just state the point.
- **Invented taxonomy labels and ALL-CAPS abstractions.** "TWO OUTCOMES", "THE THREE PILLARS", tidy coined names for things the author never named, "a framework dubbed/named/aptly named X". Use plain-English headings the author would write: "What we are delivering". The subtler sibling: **single-word category jargon** ("archetype", "pattern", "vector", "modality", "axis", "lens") draped over a plain concept to lend intellectual weight — "the two enforcement archetypes worth weighing" → "the two general distribution methods worth noting". A one-word reach, not a coined name, but the same instinct; flatten to the plain noun.
- **Buzzwords and sell language.** leverage, synergy, circle back, move the needle, game-changing, game-changer, unlock, industrialise, seamless, best-in-class, cutting-edge, transformative, empower, facilitate, streamline, paradigm shift, "this changes everything", "this is huge". Replace with specific, active phrasing.
- **Fabricated polish.** Hallucinated repo links, attendee names, acronym expansions, phantom list items. Recurring failure — when a detail is missing, omit or flag it.

## 2. Constructions to rewrite on sight

- **Negated contrast / "it's not X, it's Y".** "This isn't about speed. It's about trust." The most diagnostic AI rhetorical fingerprint — it manufactures profundity by correcting a misconception nobody had. State the positive claim directly.
- **Trailing negation tail / ", not X".** A claim with the opposite tacked on for faux-emphasis: "Technical depth that is genuine, not borrowed", "deliberate, not accidental", "a capability to build, not a tax to tolerate", "built on the last, not swapped for it". The qualifier adds rhythm, not meaning — the positive already carries it. One such tail in a piece is fine; a string of them is a tell. Cut the ", not X" and let the claim stand: "genuine technical depth". Same family as the "X, not just Y" escalator ("own the story, not just the build").
- **Rhythmic triads / rule of three** when stacked or abstract: "how we work, what we build, and how we think". Concrete lists of three real things are fine; rhythm-for-rhythm's-sake is the tell.
- **Synonym cycling.** Restating one action or idea through a string of near-synonyms to manufacture rigour: "the agent reviews the draft, scores it, and suggests changes" (three dressings of one grade step). Distinct from the triads tell — that's rhythm, this is lexical variation as filler. Say the action once with the plain word, joined by "and": "the agent grades the draft and suggests changes". If the variants are genuinely different steps, name what differs; if they aren't, collapse them.
- **Perfect A/B mirror structures.** "One helps you X. The other helps you Y." Make comparisons asymmetric and conversational.
- **Tidy bow sentences.** A paragraph wrapped with a too-neat aphoristic closer ("The stuff a model can't do."). Let ideas end without a bow.
- **"From X to Y" false ranges.** "From startups to Fortune 500s" — implies coverage while saying nothing. Name the actual cases or cut.
- **"Whether you're A or B" fake inclusivity.** Almost always AI.
- **Rhetorical question stacks.** One question is an engagement tool; three is a TED talk.
- **Over-signposted transitions.** "And here's where it connects back to…", paragraph-opening "Furthermore / Moreover / Additionally" chains. Low transition density reads human — just move to the next idea.
- **Vapid evolution openers.** "As AI continues to evolve…", "In today's fast-paced world…", "In the digital age…".
- **Participial significance tails.** Main clause + ", marking a pivotal moment in…" / ", highlighting the importance of…". LLMs use these at several times human rate. Full stop instead.
- **Vague attribution.** "Experts agree", "studies show", "industry observers note". Name the source or drop the claim.
- **Both-sidesing.** "While critics argue X, proponents maintain Y; the truth lies somewhere in between." Take the position the author holds.
- **Literary clichés.** "Gradually, then all at once", "somewhere between the X and the Y". Pre-fab phrases signal AI-smoothness even when apt.
- **Elaborate copulas.** "serves as", "stands as a testament to", "represents a shift", "boasts". Usually just "is".
- **Flattening the author's charged phrasing.** Silently swapping a deliberate, value-laden word — or a narratively-charged heading — for a blander corporate-neutral equivalent. Words: "honest task" → "real task", "strong but noisy" → "strong, though inconsistent", "deliberate hedge" → "tactical hedge". Headings: "The intervention layer is the prize, and it wasn't on the plan" → "Natural-language deal interventions are ambitious and innovative". The guardrails (in `../SKILL.md`) say "preserve strategic phrasing" as a fix rule; this is the detectable tell. A heading is the author's framing of an idea, not a slot to fill with descriptors — lift evaluative words and headings verbatim.

## 3. Lexical watchlist (cut or replace)

**Most diagnostic (focal words — rare in human prose, spiked post-2022):**
delve, tapestry, underscore(s), pivotal, crucial, paramount, robust, seamless, leverage (verb), harness (verb), landscape (abstract), realm, testament, vibrant, multifaceted, nuanced (as decoration), foster, navigate (abstract), beacon, cornerstone, ecosystem (abstract), holistic, meticulous(ly), boast(s), elevate, supercharge, ever-evolving, journey (abstract), arc (as narrative decoration — "the margin arc", "the recovery arc", "the narrative arc"; name what moved and how instead: "margin climbed from 5.2% to 25.9%").

**Empty openers:** "It's important to note that", "It's worth mentioning", "At its core", "When it comes to X", "In the realm of", "Let's unpack".

**Throat-clearing:** "in order to" → "to"; "utilise" → "use"; "a number of" → a real count; "the fact that" → restructure; "It would be fair to say" → just say it.

**Hollow intensifiers/qualifiers:** really, very, quite, truly, genuinely (unless doing real work), actually, arguably, fundamentally, comprehensive, key (as filler), significant(ly) without a number.

**Hedge-and-fill verbs:** "helps to", "serves to", "plays a role in", "in many ways", "can be seen as".

**Filler action phrases:** "embark on a journey", "unlock the potential", "paving the way", "push the boundaries", "master the art of", "dive into the intricacies".

**Pseudo-analytical hedges:** "struggles to scale", "only as strong as X", "is a double-edged sword", "comes with trade-offs". Mechanism-sounding limitations that read as incisive but name nothing concrete — *what* breaks, *when*, or by how much. Example fixes: "Familiar, slow, struggles to scale with AI-generated output" → "Good practice, insufficient at this volume"; "Faster, but only as strong as the underlying assets and adoption" → "Faster, but needs steering to fit our house style". Replace with a concrete verdict about the situation at hand, not a generic scalability caveat.

**"name" / "named" as a verb meaning identify or call out.** "they name the growth areas honestly", "it names the risks", "naming the tension", "name the thing". Stilted in a way a human would not write — say what's actually meant: "calls out", "is honest about", "states plainly", "spells out", "flags", or just rephrase. Same family: "speak to" (meaning address), "give voice to", "surface" stacked as a verb. Example fix: "they lean on the strengths and name the growth areas honestly" → "they lean on the strengths and are honest about the growth areas".

**"failure mode" as a catch-all for "way this goes wrong".** "The failure mode here is over-engineering", "a common failure mode", "the failure mode of this approach". Borrowed engineering jargon LLMs reach for to sound rigorous about ordinary risks. Say the plain thing: "the risk here is", "this usually goes wrong when", "the danger is", or just describe what breaks. Keep it only in genuinely technical reliability contexts (FMEA, hardware, distributed systems) where it's the precise term.

**"the room" as a collective actor — and "in the room" as vague presence.** "where the room landed", "the room agreed", "the room moved toward", "support in the room", "the view that held in the room", "the room kept returning to". Also the attendee-idiom sibling: "who is in the room", "who's in the room", "everyone in the room", "get the right people in the room", "the people in the room" — reaching for "the room" to gesture at *who is involved* rather than naming them or saying it plainly ("who is on the thread", "who is on this", "who is across it"). Both variants are the same instinct: personifying or spatialising the meeting instead of naming who held a view or stating the point. Overused, it makes every paragraph sound like the same anonymous committee. Fix by naming the actor ("the security leads pushed for…"), stating the position directly ("training should gate access"), naming who is involved ("who is on the thread"), or attributing neutrally once ("the agreed direction was…"). Same instinct sits behind "framed around the three areas X set out" and other vague meta-framing of a discussion — say what was decided, not how the conversation was shaped. Family of the vague-attribution tell (§2).

**"the X can't see" — personifying a report, tool, or system as a seeing/blind agent.** "the weekly report can't see the one-off swing", "what the dashboard can't see", "the report is blind to margin", "invisible to the weekly cadence" stacked as a motif. The report does not have eyes; it reaches for a tidy vision metaphor to dramatise a scope gap. Say the plain mechanism: "the weekly report has no profit line, so the one-off swing never appears", "margin is out of the report's scope", "the dashboard doesn't track cost". Fine once; a recurring "can't see / blind to / invisible to" refrain across sections is the tell. Family of the object-personification instinct behind "the room" above.

The test for all of these: delete the word or phrase. If the sentence means the same, it was fill.

## 4. Structural tells

- **Prompt-restatement intro.** Opening by rephrasing the brief before answering it. Start with the substance.
- **"In conclusion" / "Final Thoughts" wrappers** on short pieces, and bow-tie endings that zoom back out to the intro's generic framing while adding nothing.
- **Bolded-lead-in bullet sprawl.** Every idea forced into bullets, each starting "**Keyword:** sentence restating the keyword". Use bullets only for genuinely list-shaped content.
- **Heading-per-paragraph** and Title Case In Every Heading. Use sentence case, fewer headings.
- **Section overload.** Verbatim reviewer reaction: *"8 is too many sections, I'm not even going to read it."* For exec / shareable artefacts: 4–6 top-level sections, curated hard.
- **Bolted-on procedural meta-sections.** Scaffolding the author never asked for, added to complete a facilitation-template archetype: "PRE-MEETING ASKS", "OUT OF SCOPE V1", "WHAT TO BRING" boxes. Verbatim reviewer reactions: *"Delete whole section and asks"*, *"Remove this, it doesn't add anything."* They read as thoroughness but carry no independent value once the body is clear. Omit unless explicitly requested.
- **Metronomic rhythm.** Uniform paragraph and sentence lengths throughout. Vary: short punchy sentences against longer ones, 2–3 sentence paragraphs, the key one-liner isolated with white space (don't bury the payoff mid-paragraph).
- **Dramatic fragmentation / stacked punchy fragments.** The opposite failure to metronomic uniformity: chopping into staccato one-clause fragments for false punch. "That's it. That's the whole thing.", "X. And Y. And Z.", "Not a demo. A product." A single fragment for emphasis is fine; stacked fragments and robotic symmetry (the same short shape three times running) are the tell. Restore complete sentences and let one fragment, if any, carry the weight. Same family as the negative-listing form ("Not X. Not Y. A Z.") — state Z directly.
- **Redundant beats.** A caveat or insight stated once, then re-litigated in every section. State it once up front and move on ("Label that at the front but don't keep referring to it everywhere").

## 5. Tonal tells

- **Relentless positivity / puffery.** Everything an opportunity, a breakthrough, "stands as a testament". Calibrate to neutral and factual.
- **Overstated maturity or confidence.** "Live" when it's an example; "cloud agnostic" when it's "cloud flexible". Calibrate claims down to what's verified.
- **Unsourced inference stated as fact.** Plausible extrapolations asserted as ground truth — a named person's activities ("X has been actively engaging on design-system thinking"), a tool's adoption state ("Live and in use"), or an asset's relative standing ("the most mature concrete asset in this space"). Distinct from fabricated polish (outright hallucination): this is *likely-but-unverified* worn as fact. Verbatim reviewer tells: *"Where did you get this information from?"* and *"Too opinionated, delete the bold bit."* The test — if a reader would ask "says who?", attribute it, hedge it, or cut it.
- **Defensive hedging.** Qualifying every statement to avoid being wrong ("often", "typically", "may", "generally") and defensive framing ("here's why it's taking so long"). Own positions; state caveats once, neutrally. **Double-negative softening** belongs here too: rewriting a blunt claim into a double negative that keeps the logic but drains the directness — "might not work" → "isn't guaranteed to work", "the fourth workstream" → "a potentially new workstream". Prefer the author's original blunt form.
- **Sycophancy and false enthusiasm.** "Great question", "exciting opportunities", "fascinating insights".
- **Safety boilerplate.** "It's important to approach this responsibly", "results may vary" — appended reflexively.
- **Abstraction without anchor.** Every abstract claim needs one concrete particular: "a workflow that took three hours now takes ten minutes" beats "significantly faster". Replace "much better" with the number.

## 6. Punctuation & typography — density is the tell, not presence

These are legitimate in skilled human writing; flag saturation, not existence:

| Pattern | Threshold |
|---------|-----------|
| Em dashes | Flag 4+ in a piece or 2+ in one paragraph. (Some house styles ban them outright in short-form email/chat — defer to `VOICE.md`.) |
| Tricolons / Oxford-comma triads | Fine occasionally; flag when every list has exactly three balanced items |
| Bold as emphasis | Flag bold on "key lines" in prose — let the words land. Structural bold (subheadings in dense decks) stays |
| Bullet lists | Fine for list-shaped content; flag prose forced into bullets |
| Transition adverbs | Fine singly; flag three consecutive paragraphs opening with one |
| Decorative asterisks/markers | Remove — *"it's tacky"* (verbatim). Use structure, not symbols |

---
name: wiq-html
version: 3.0.0
description: "DEPRECATED — wiq-branded HTML styling. Superseded by design-guide (scheme: wiq-detailed). Load design-guide instead."
metadata:
  openclaw:
    category: "custom"
    domain: "design"
---

# wiq-html — deprecated, use design-guide

This skill has been folded into **`design-guide`** (`../design-guide/SKILL.md`), which
now owns the token layer and component patterns for all HTML artefacts.

The old wiq look is the **`wiq-detailed`** scheme:

> assets/primitives.css + assets/spectrum.css + assets/palette-wiq.css + implementations/detailed.css

**What to do:** load `design-guide`, select the **wiq** palette + **Detailed**
implementation, and follow that guide. See `design-guide/presets/README.md` for the
concat recipe and the `showPage` JS behaviour.

Everything wiq-html previously documented — Berry accent, Charcoal text, warm neutrals,
the spectrum, typography, components (Berry table headers, Berry-10 row striping,
takeaway box), no-emoji rule, colour discipline, restyling strategy, and the quality
review — now lives in `design-guide` (as tokens for the wiq palette and the Detailed
implementation). Nothing is lost; it is tokenised and shared.

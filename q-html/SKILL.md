---
name: q-html
version: 2.0.0
description: "DEPRECATED — Quantium-branded HTML styling. Superseded by design-guide (scheme: quantium-detailed). Load design-guide instead."
metadata:
  openclaw:
    category: "custom"
    domain: "design"
---

# q-html — deprecated, use design-guide

This skill has been folded into **`design-guide`** (`../design-guide/SKILL.md`), which
now owns the token layer and component patterns for all HTML artefacts.

The old q-html look is the **`quantium-detailed`** scheme:

> assets/primitives.css + assets/spectrum.css + assets/palette-quantium.css + implementations/detailed.css

**What to do:** load `design-guide`, select the **Quantium** palette + **Detailed**
implementation, and follow that guide. See `design-guide/presets/README.md` for the
concat recipe and the `showPage` JS behaviour.

Everything q-html previously documented — Q Blue accent, warm neutrals, the 9-colour
spectrum, typography, components, no-emoji rule, colour discipline, restyling strategy,
and the quality review — now lives in `design-guide` (as tokens for the Quantium
palette and the Detailed implementation). Nothing is lost; it is tokenised and shared.

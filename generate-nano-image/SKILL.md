---
name: generate-nano-image
description: >
  Generate and iteratively edit images via Google's Nano Banana Pro
  (Gemini 3 Pro Image, gemini-3-pro-image-preview) on Vertex AI, using local
  gcloud Application Default Credentials (no API key). Handles dependency
  checks, an upfront Q&A, an API-first edit loop with vision-verified results,
  and a deterministic pixel-patch fallback for text the model won't fix.
  Use when the user wants to create an image, infographic, poster, or
  illustration from a prompt (optionally with reference images/docs), or
  refine an existing generated image. NOT for
  requests that name a different provider/tool (DALL·E, Imagen-only, Midjourney,
  Stable Diffusion, a local model), for photo editing of the user's own photos,
  or for diagram/chart generation better done in code.
argument-hint: "[a prompt, and/or paths to reference images or a brief doc]"
---

# generate-nano-image

Create and refine images with Nano Banana Pro on Vertex AI. API does the heavy
lifting; deterministic pixel-patches rescue small text fixes the model refuses.

## When to use / when NOT to use

**Use when:**
- "Generate an image of …", "make me a poster/infographic/icon …"
- The user has a detailed brief (a doc or long prompt) and/or reference images to condition on.
- Iterating on an image this skill produced ("flip the car", "fix that typo", "make the sky orange").

**Do NOT use when:**
- The user explicitly wants another generator (DALL·E, Midjourney, Stable Diffusion, raw Imagen) — defer to that.
- They want their *own* photographs edited (different tooling/expectations).
- The artefact is really a chart/diagram → generate it in code (matplotlib, mermaid, SVG), not a vision model.
- A non-interactive/headless/cron context — the edit loop needs the agent's vision at each step and cannot run unattended.

## Companion skills
- `remove-ai-tells` — if the image carries body copy you also drafted, de-slop the prose separately.

## Procedure

Scripts live in `scripts/` (bundled). Run everything from that dir with `uv run`
(ships a `uv.lock`, so it ignores the container's JFrog index). Replace `<SKILL>`
with this skill's directory.

### 0. Dependency check (do this first, once)
```bash
# ADC present? (no API key is used — Vertex signs with your gcloud ADC)
gcloud auth application-default print-access-token >/dev/null 2>&1 && echo "ADC OK" || echo "RUN: gcloud auth application-default login"
# Python deps resolve from the lock (first run installs the venv):
cd <SKILL>/scripts && uv run python -c "import google.genai, PIL, numpy; print('deps OK')"
```
If ADC is missing, tell the user to run `gcloud auth application-default login`
in this session via `! gcloud auth application-default login`.

### 1. Upfront Q&A (one AskUserQuestion)
Ask, pre-filling sensible defaults:
- **Output directory** — where images land (`--out-dir`). Default: a `./output/` near where they're working.
- **Max edit rounds** — guardrail cap on the interactive edit loop; stop and check in after N. Default 5.
- **Resolution / aspect ratio** — default **2K** (see latency gotcha; 4K times out). Aspect e.g. 16:9, 21:9, 1:1.
- **Reference inputs** — any images to condition on, and/or a doc/brief to fold into the prompt.

### 2. Initial generation
Read any brief doc(s) and concatenate into the prompt text. Pass reference images with repeated `--image`.
```bash
cd <SKILL>/scripts
uv run python generate.py \
  --out-dir "<OUT>" --aspect-ratio 21:9 --resolution 2K \
  --image ref1.png --image ref2.png \
  "$(cat brief.md)"
```
Run it in the **background** (renders take 2–3 min at 2K). Then **Read the saved PNG** and show/describe it.

### 3. Edit loop (API first — this is the default for almost everything)
Feed the current image back in; the prompt becomes edit instructions. Editing
**preserves everything you don't mention** far better than re-prompting from scratch.
```bash
uv run python generate.py --image <current>.png --out-dir "<OUT>" \
  --aspect-ratio 21:9 --resolution 2K "Make ONLY these changes … keep everything else identical."
```
After each edit you MUST **verify with vision**: crop the changed region and Read it
(`uv run python patch_helpers.py zoom <img> X0 Y0 X1 Y1 12 grid out.png`). The model
often *claims* it made a change while reproducing the original — do not trust its text.

Prompting reliability tiers (observed):
| Edit type | Reliability | Tactic |
|---|---|---|
| Recolour / relabel a distinct element | one-shot | normal instruction |
| Reorient / flip an object | needs blunt phrasing | say "flip 180° / mirror horizontally", not "turn it around" |
| Fix a single letter/word already in the image | **fails** | model reproduces the existing text → go to step 4 |

### 4. Deterministic pixel-patch — LAST RESORT only
Trigger only when an API edit can't land **and** the target is **text or a small
overlay on a near-flat background**. (Spatial edits, textured/photographic
backgrounds, and exotic fonts are out of reach — accept the API result or stop.)

Agent-driven loop (you read the crops and judge):
1. **Locate** — `zoom` to eyeball, then `vprof`/`hprof` for exact glyph x-spans and line y-spans.
2. **Sample** — `sample` the box for the local background (fill) and ink colour.
3. **Patch** — from a tiny inline script, call `patch_text(...)` (erase the old glyph(s) + halo, re-render centred lines in Liberation Sans Bold at the measured cap height). For a single-letter tweak that's nearly the same shape (e.g. C→G), adding a tiny stroke with `ImageDraw` beats redrawing.
4. **Verify** — `zoom` the result and Read it. Iterate coordinates until correct.
```bash
cd <SKILL>/scripts
uv run python patch_helpers.py zoom  img.png 2855 462 2965 538 12 grid /tmp/z.png   # inspect
uv run python patch_helpers.py vprof img.png 1380 1150 1525 1174                     # letter x-spans
uv run python patch_helpers.py sample img.png 1485 1150 1503 1174                    # bg + ink colour
# then a 3-line inline script: from patch_helpers import patch_text; patch_text(...)
```

## Gotchas / notes for future-me
- **Bake correct spelling into the FIRST prompt.** The editor locks onto whatever text is already in the image and will not correct a typo — every prompt-based attempt reproduces it (cost us 6 failed tries → pixel-patch). Cheaper to get it right up front.
- **4K reliably times out** (>7 min, no return). Default to **2K**; run generations in the background.
- **`gemini-3-pro-image-preview` is a preview id** that may change/404. Fallbacks: `gemini-2.5-flash-image` (standard Nano Banana, faster/cheaper) via `--model` or `MODEL_NAME`. Check the Vertex model garden if both fail.
- **JFrog 401**: solved by the committed `uv.lock`. If you edit deps, relock with `UV_EXTRA_INDEX_URL= uv lock`, else fresh resolution 401s.
- **Never re-run the model after a pixel-patch** — a fresh API edit regenerates the whole image and can revert/degrade your patches. Pixel-patches are terminal; do them last.
- **`patch_text` centring** uses `anchor="ms"` (horizontal centre, baseline y). Measure `center_x` from `vprof`, `baseline_y` from `hprof`.
- **Auth = ADC, no API key.** `GOOGLE_GENAI_USE_VERTEXAI` is implied via `vertexai=True`; project falls back to the ADC quota project if `GOOGLE_CLOUD_PROJECT` is unset; location defaults to `global` (correct for the Pro preview).

## See also
- `/new-skill-checker <path>` — security/quality grade before sharing.
- Vertex AI model garden — current image model ids.

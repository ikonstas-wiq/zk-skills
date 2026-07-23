---
name: html-to-pdf
version: 1.0.0
description: "Convert a self-contained HTML file to a well-formatted PDF using Playwright + Chromium."
metadata:
  openclaw:
    category: "custom"
    domain: "utility"
    requires:
      bins: ["node"]
---

# Convert HTML to PDF

Use this skill whenever the user asks to generate a PDF from an HTML file, or when you've built an HTML artefact that needs a PDF version.

## Prerequisites

Playwright must be installed globally with Chromium:

```bash
# Check if available
npx playwright --version

# Install if needed (one-time)
npm install -g playwright
npx playwright install chromium
```

The global install lives at `~/.npm-global/lib/node_modules/playwright`. You must set `NODE_PATH` when running Node scripts so it can find the module.

## Generating the PDF

Use this exact pattern. Do not use `puppeteer`, `wkhtmltopdf`, or other tools — Playwright + Chromium gives the best fidelity for styled HTML.

```bash
NODE_PATH=/home/node/.npm-global/lib/node_modules node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file:///absolute/path/to/input.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.pdf({
    path: '/absolute/path/to/output.pdf',
    format: 'A4',
    margin: { top: '24px', bottom: '24px', left: '24px', right: '24px' },
    printBackground: true
  });
  await browser.close();
  console.log('Done');
})();
"
```

### Key options

| Option | Default | Notes |
|--------|---------|-------|
| `format` | `'A4'` | Use `'Letter'` for US sizing |
| `margin` | `24px` all sides | Increase for documents with dense content near edges |
| `printBackground` | `true` | **Must be true** to render background colours, card fills, coloured bars |
| `waitUntil` | `'networkidle'` | Waits for web fonts (e.g., Google Fonts) to load |
| `waitForTimeout` | `1500` | Extra buffer for font rendering and CSS animations |

### Landscape mode

```javascript
await page.pdf({
  path: '/path/to/output.pdf',
  format: 'A4',
  landscape: true,
  margin: { top: '24px', bottom: '24px', left: '24px', right: '24px' },
  printBackground: true
});
```

## Validation

After generating the PDF, **always validate** by reading it back:

1. **Read the PDF** using the `Read` tool to visually inspect the output.
2. **Check for these common issues:**

| Issue | Cause | Fix |
|-------|-------|-----|
| Blank trailing page | Footer/source line pushed to new page by large margins | Reduce `margin-top` on the source element, or reduce section `margin-bottom` |
| Missing backgrounds | `printBackground: false` | Set `printBackground: true` |
| Broken fonts | Google Fonts not loaded | Increase `waitForTimeout` to `2000`+ or check `waitUntil: 'networkidle'` |
| Content cut off at edges | Margins too small for content width | Increase page margins or reduce `max-width` in CSS |
| Page breaks mid-card | No print CSS | Add `break-inside: avoid` to card/section elements in a `@media print` block |
| Animations visible as partial state | CSS animations freeze mid-transition | Add `@media print { * { animation: none !important; } }` |

3. **If the trailing page is blank**, tighten spacing and regenerate. Do not ship a PDF with a blank last page.

## HTML Best Practices for PDF Output

When building HTML that will become a PDF:

- Add `@media print` styles with `break-inside: avoid` on cards, tables, and sections
- Use `break-before: page` for intentional page breaks
- Keep `max-width` under `860px` for A4 with margins
- Avoid `position: fixed` or `position: sticky` — they don't translate to PDF
- CSS animations won't play in PDF — ensure the final state looks correct without animation
- Google Fonts work but need `waitUntil: 'networkidle'` to load

## Example: Full Workflow

```bash
# 1. Generate the PDF
NODE_PATH=/home/node/.npm-global/lib/node_modules node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file:///workspace/project/report.html', { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);
  await page.pdf({
    path: '/workspace/project/report.pdf',
    format: 'A4',
    margin: { top: '24px', bottom: '24px', left: '24px', right: '24px' },
    printBackground: true
  });
  await browser.close();
  console.log('Done');
})();
"

# 2. Validate — use Read tool on the PDF to check visually
# 3. Fix any issues (blank pages, missing styles) and regenerate
```

# Presets — scheme recipes

A **scheme = assets (tokens + palette) × implementation**. Rather than duplicate
four monolithic stylesheets, a preset is a *concatenation recipe*: inline these
files, in this order, into the single `<style>` block of the self-contained HTML.

Order matters — tokens first, implementation last (its `:root` overrides and rule
overrides must win the cascade):

| Scheme | Concatenate (in order) |
|---|---|
| **quantium-detailed** (= old q-html) | `primitives.css` + `spectrum.css` + `palette-quantium.css` + `detailed.css` |
| **wiq-detailed** (= old wiq-html) | `primitives.css` + `spectrum.css` + `palette-wiq.css` + `detailed.css` |
| **quantium-exec** | `primitives.css` + `spectrum.css` + `palette-quantium.css` + `exec.css` |
| **wiq-exec** | `primitives.css` + `spectrum.css` + `palette-wiq.css` + `exec.css` |

For prototypes that only need the design tokens (no report components), inline just
`primitives.css` + a `palette-*.css` and build your own components against the
semantic tokens (`--accent`, `--surface`, `--heading`, `--radius-card`, …).

Every scheme uses the **same HTML class vocabulary** (`.top-nav`, `.page`,
`.master-section`, `.doc-table`, `.tag`, `.callout-bar`, …), so switching scheme is
a CSS swap plus the matching JS behaviour below — the markup does not change.

---

## JavaScript behaviours

Pick one based on the implementation. Both are self-contained, no dependencies.

### Detailed — `showPage` (one page visible at a time)

```javascript
function showPage(page, btn) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.top-nav-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('page-' + page).classList.add('active');
  btn.classList.add('active');
  window.scrollTo(0, 0);
  document.getElementById('page-' + page).querySelectorAll('.master-section').forEach((s, i) => {
    s.style.animation = 'none'; s.offsetHeight; s.style.animation = '';
    s.style.animationDelay = (0.1 + i * 0.08) + 's';
  });
}

function toggleMaster(header) {
  const section = header.closest('.master-section');
  const body = section.querySelector('.master-body');
  if (section.classList.contains('open')) {
    body.style.maxHeight = '0';
    section.classList.remove('open');
  } else {
    section.classList.add('open');
    body.style.maxHeight = body.scrollHeight + 'px';
    setTimeout(() => { if (section.classList.contains('open')) body.style.maxHeight = 'none'; }, 500);
  }
}
```

### Exec — tabs-as-anchors (all pages stacked; scroll OR click; scroll-spy)

All `.page` blocks render at once. A tab click smooth-scrolls to its section; an
IntersectionObserver highlights the tab for whichever section is in view.

```javascript
// Click a tab -> jump to its section
function showPage(page, btn) {
  const target = document.getElementById('page-' + page);
  if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Scroll -> highlight the active tab (scroll-spy)
(function () {
  const tabById = {};
  document.querySelectorAll('.top-nav-tab').forEach(t => {
    const m = (t.getAttribute('onclick') || '').match(/showPage\(['"]([^'"]+)['"]/);
    if (m) tabById[m[1]] = t;
  });
  const spy = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const id = e.target.id.replace('page-', '');
      document.querySelectorAll('.top-nav-tab').forEach(t => t.classList.remove('active'));
      if (tabById[id]) tabById[id].classList.add('active');
    });
  }, { rootMargin: '-72px 0px -70% 0px', threshold: 0 });
  document.querySelectorAll('.page').forEach(p => spy.observe(p));
})();

// toggleMaster — same as Detailed above (accordions still expand/collapse)
```

The `toggleMaster` function is identical across both implementations — include it in
either scheme.

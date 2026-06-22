# CyberMate — Conversion Notes

This React/Vite project was checked against `cybermate.html` (the standalone
reference build). The two did **not** match — the original `src/` here was a
simple static "SOC dashboard" (Header, StatsBar, ThreatCard, LiveFeed,
AlertHistory) with mock data, while `cybermate.html` is a full multi-screen
experience: theme switcher → animated intro → operation menu → normal log
scan / brute‑force attack pipeline simulation (10 stages, canvas node graph)
→ full‑screen success pipeline. Visually and functionally they were
different products.

This project has been converted so it renders and behaves **exactly** like
`cybermate.html`, while still living inside the existing Vite + React
scaffold (so `npm install && npm run dev` keeps working).

## What changed

- **`src/cybermate-markup.html`** — the reference file's `<body>` content
  (theme selector, background canvas, all 5 screens), copied verbatim,
  byte‑for‑byte identical to the source HTML.
- **`src/cybermate-engine.js`** — the reference file's `<script>` logic
  (theme switching, particle backgrounds, intro sequence, the normal‑log
  scan simulation, the 10‑stage attack pipeline with the canvas node/packet
  animation, the success screen's 3D pipeline canvas), copied verbatim with
  **one** safety fix: the original intro animation was triggered by
  `addEventListener('load', …)`. Since this script is now mounted by React
  *after* the page has already loaded, that event would never fire again —
  so it now runs immediately if `document.readyState === 'complete'`, and
  falls back to the `load` listener otherwise. No other behavior was
  touched.
- **`src/App.css`** — replaced with the reference file's `<style>` block,
  verbatim (theme CSS variables, all screen/animation styles).
- **`src/App.jsx`** — now just mounts `cybermate-markup.html` (via
  `dangerouslySetInnerHTML`, so the inline `onclick="…"` handlers keep
  working exactly as in the original static file) and injects
  `cybermate-engine.js` as a real `<script>` tag once on load (a window
  flag guards against double‑injection from React StrictMode / HMR, since
  the engine starts animation loops that must only start once).
- **`src/main.jsx`** — dropped the unused `BrowserRouter` wrapper (the
  reference app has no routing).
- **`index.html`** — title aligned to match `cybermate.html` exactly
  (`CyberMate — Agentic SOC`). Fonts/meta/boot‑loader were already in place
  and needed no changes.
- **`src/components/_legacy_dashboard/`** — the old, now‑unused dashboard
  components (`Header.jsx`, `StatsBar.jsx`, `ThreatCard.jsx`, `LiveFeed.jsx`,
  `AlertHistory.jsx`, `PipelineView.jsx`) were moved here rather than
  deleted, in case anything from them is useful later. They are not
  imported by anything and have no effect on the build.
- **`src/api/client.js`** — left untouched. It wasn't wired into the old
  dashboard either; it's available if/when a real backend is connected.

## Verifying it

```bash
npm install
npm run dev
```

Open the dev URL — you should see the same theme switcher (top right),
the same animated "CYBERMATE" intro, the same operation menu, and the same
brute‑force pipeline simulation / normal log scan / success screens as
`cybermate.html`, pixel‑for‑pixel.

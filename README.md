# DeepSeek Research — Recursive Self-Improvement

An animated single-page site inspired by [Anthropic's recursive self-improvement essay](https://www.anthropic.com/institute/recursive-self-improvement), re-skinned for **DeepSeek** with the official DeepSeek whale mark.

## ✨ Highlights

- **Living hero** — a recursive cellular automaton that breeds cells outward and collapses them back into the DeepSeek whale, over and over, like the compounding AI loop it describes.
- **Scroll timeline** — the SVG grows lane by lane as you scroll; each node assembles a progressively finer pixel-art whale, ending in the "AI designing the AIs that design the AIs" loopback.
- **Official logo** — the DeepSeek whale mark extracted from deepseek.com is used in the header, hero, and footer.
- **PWA** — installable on any phone/desktop, works offline.

## 🚀 Open

Simply open `index.html` in a browser, or serve it:

```bash
python -m http.server 8000
# → http://localhost:8000
```

## 📱 PWA (installable / offline)

The site is a progressive web app:

- `manifest.webmanifest` — app name, theme, icons
- `sw.js` — service worker with offline caching
- `icon.svg` / `icon-192.png` / `icon-512.png` — app icons

On a phone: open the hosted URL → **Add to Home Screen** → launches fullscreen, works offline.

## 🔧 Rebuild

The site is generated from `build_page.py` (embeds the whale pixel art and logo path):

```bash
python build_page.py   # rewrites index.html
```

## 📄 License

Original essay and iconography belong to their respective owners. This is a fan/parody page for demonstration.

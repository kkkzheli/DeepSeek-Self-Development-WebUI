# DeepSeek-Self-Development-WebUI

An animated, single-page **fan-made replica** of [Anthropic's "When AI builds itself"](https://www.anthropic.com/institute/recursive-self-improvement) essay, re-skinned for **DeepSeek** with the official DeepSeek whale mark.

> **This is a local page for entertainment purposes only.** It provides visual effects only. It is **not** affiliated with, endorsed by, or related to DeepSeek or Anthropic in any way. All trademarks and copyrights belong to their respective owners. The essay text is adapted from Anthropic's original work for learning/entertainment purposes.

## ✨ Highlights

- **Living hero** — a recursive cellular automaton that breeds cells outward and collapses them back into the DeepSeek whale, over and over, like the compounding AI loop it describes.
- **Benchmark leaderboard** — SWE-bench Verified, GPQA Diamond, MMLU-Pro and more, toggleable between DeepSeek V4 Pro and V4 Flash (data sourced from official DeepSeek publications, with links).
- **Scroll timeline** — the SVG grows lane by lane as you scroll; each node assembles a progressively finer pixel-art whale, ending in the "AI designing the AIs that design the AIs" loopback.
- **Real-time adaptive layout** — the hero re-flows instantly when the viewport is squeezed by overlays or browser UI (no manual refresh needed).
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

The site is generated from `build_page.py` (embeds the whale pixel art, logo path, and all content):

```bash
python build_page.py   # rewrites index.html
```

## 📄 Copyright & Disclaimer

- This project is an **unofficial, fan-made** work. It is **not** affiliated with, endorsed by, or sponsored by **DeepSeek** or **Anthropic**.
- **DeepSeek**, the DeepSeek whale mark, and **Anthropic**, the Anthropic name and its essays, are trademarks or copyrighted works of their respective owners. All rights remain with their owners.
- The essay text and structure are adapted from Anthropic's original article for learning and entertainment only.
- The Anthropic variable fonts embedded in the page are property of Anthropic and are used here solely for personal, non-commercial, educational demonstration.
- Benchmark scores are quoted from official DeepSeek publications (model cards, technical report) and third-party evaluations; they are shown for display purposes and do not imply any official endorsement.
- No commercial use is intended. If you are a rights holder and want this removed, please open an issue.

## 🐳 Replica by

[kkkzheli](https://github.com/kkkzheli) — built with Claude Code.

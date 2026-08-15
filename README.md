<div align="center">

**English (US)** · [简体中文](#简体中文) · [繁體中文](#繁體中文)

</div>

# DeepSeek-Self-Development-WebUI

An animated, single-page **fan-made replica** of [Anthropic's "When AI builds itself"](https://www.anthropic.com/institute/recursive-self-improvement) essay, re-skinned for **DeepSeek** with the official DeepSeek whale mark.

> **This is a local page for entertainment purposes only.** It provides visual effects only. It is **not** affiliated with, endorsed by, or related to DeepSeek or Anthropic in any way. All trademarks and copyrights belong to their respective owners. The essay text is adapted from Anthropic's original work for learning/entertainment purposes.

## ✨ Highlights

- **Living hero** — a recursive cellular automaton that breeds cells outward and collapses them back into the DeepSeek whale, over and over, like the compounding AI loop it describes. Cursor proximity glows, click bursts particles, drag leaves a trail.
- **🌐 Trilingual** — switch 简体中文 / 繁體中文 / English (US) from the header dropdown at any time; the whole page (including benchmark notes and comparison footnotes) re-renders in place, and your choice is remembered across visits.
- **Benchmark leaderboard** — SWE-bench Verified, GPQA Diamond, MMLU-Pro and more, toggleable between DeepSeek V4 Pro and V4 Flash (data sourced from official DeepSeek publications, with links).
- **Flagship comparison** — every benchmark card ranks DeepSeek V4 Pro against the latest flagships (GPT-5.6 Sol, Claude Fable 5, Gemini 3.1 Pro, Grok 4.6, Qwen3.8-Max, Kimi K3, GLM-5.2, Mistral Large 3, Llama 4 Maverick), with source notes on each score (official model cards where published, otherwise third-party runs).
- **Scroll timeline** — the SVG grows lane by lane as you scroll; each node assembles a progressively finer pixel-art whale, ending in the "AI designing the AIs that design the AIs" loopback.
- **Real-time adaptive layout** — the hero re-flows instantly when the viewport is squeezed by overlays or browser UI (no manual refresh needed).
- **Single self-contained file** — all logos, fonts, icons and artwork are inlined as data URIs; `index.html` alone has zero network dependencies.
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

---

## 简体中文

# DeepSeek-Self-Development-WebUI

[Anthropic《When AI builds itself》](https://www.anthropic.com/institute/recursive-self-improvement) 的动画单页**粉丝复刻**，以 **DeepSeek** 官方鲸鱼标志重新皮肤。

> **本页面仅供本地娱乐。** 仅提供视觉展示。**与 DeepSeek 或 Anthropic 无任何关联、背书或关系**。所有商标与版权归各自权利人所有。文章文本改编自 Anthropic 原作，仅用于学习/娱乐。

## ✨ 亮点

- **灵动鲸鱼主视觉** — 递归元胞自动机不断向外繁殖细胞、再折叠回 DeepSeek 鲸鱼，循环往复，正如它描述的自我强化 AI 循环。光标靠近会发光，点击迸发粒子，拖拽留下轨迹。
- **🌐 三语切换** — 从顶部下拉菜单随时切换简体中文 / 繁體中文 / English (US)；整个页面（包括榜单注释与对比脚注）原地重新渲染，选择会在下次访问时记住。
- **基准测试榜单** — SWE-bench Verified、GPQA Diamond、MMLU-Pro 等，可在 DeepSeek V4 Pro 与 V4 Flash 之间切换（数据取自 DeepSeek 官方公开资料，附链接）。
- **旗舰对比** — 每个基准卡片将 DeepSeek V4 Pro 与最新旗舰（GPT-5.6 Sol、Claude Fable 5、Gemini 3.1 Pro、Grok 4.6、Qwen3.8-Max、Kimi K3、GLM-5.2、Mistral Large 3、Llama 4 Maverick）排名对比，每项分数附来源注（官方 model card 或第三方跑分）。
- **滚动时间线** — SVG 随滚动逐道生长；每个节点逐步组装更精细的像素鲸鱼，最终收束于「AI 设计设计 AI 的 AI」回环。
- **实时自适应布局** — 视口被覆盖层或浏览器 UI 挤压时，主视觉即时重排（无需手动刷新）。
- **单文件零依赖** — 所有 logo、字体、图标与图形均内联为 data URI；仅 `index.html` 一个文件，零网络依赖。
- **PWA** — 手机/桌面皆可安装，离线可用。

## 🚀 打开

直接用浏览器打开 `index.html`，或本地起服务：

```bash
python -m http.server 8000
# → http://localhost:8000
```

## 📱 PWA（可安装 / 离线）

本页是渐进式 Web 应用：

- `manifest.webmanifest` — 应用名、主题、图标
- `sw.js` — 离线缓存 Service Worker
- `icon.svg` / `icon-192.png` / `icon-512.png` — 应用图标

手机上：打开托管地址 → **添加到主屏幕** → 全屏启动，离线可用。

## 🔧 重新构建

页面由 `build_page.py` 生成（内嵌鲸鱼像素画、logo 路径与全部内容）：

```bash
python build_page.py   # 重写 index.html
```

## 📄 版权与免责声明

- 本项目是**非官方的粉丝作品**，与 **DeepSeek** 或 **Anthropic** 无任何关联、背书或赞助关系。
- **DeepSeek**、DeepSeek 鲸鱼标志，以及 **Anthropic** 名称与其文章，均为各自权利人的商标或版权作品，权利归其权利人所有。
- 文章文本与结构改编自 Anthropic 原文章，仅用于学习与娱乐。
- 页面内嵌的 Anthropic 可变字体属 Anthropic 所有，仅用于个人、非商业、教学演示。
- 榜单分数引自 DeepSeek 官方公开资料（model card、技术报告）与第三方评测，仅作展示，不代表任何官方背书。
- 无任何商业用途意图。如您是权利人并希望移除，请开 issue。

## 🐳 复刻者

[kkkzheli](https://github.com/kkkzheli) — 由 Claude Code 构建。

---

## 繁體中文

# DeepSeek-Self-Development-WebUI

[Anthropic《When AI builds itself》](https://www.anthropic.com/institute/recursive-self-improvement) 的動畫單頁**粉絲復刻**，以 **DeepSeek** 官方鯨魚標誌重新換膚。

> **本頁面僅供本機娛樂。** 僅提供視覺展示。**與 DeepSeek 或 Anthropic 無任何關聯、背書或關係**。所有商標與版權歸各權利人所有。文章文字改編自 Anthropic 原作，僅供學習／娛樂。

## ✨ 亮點

- **靈動鯨魚主視覺** — 遞迴元胞自動機不斷向外繁殖細胞、再摺疊回 DeepSeek 鯨魚，循環往復，正如它描述的自我強化 AI 循環。游標靠近會發光，點擊迸發粒子，拖曳留下軌跡。
- **🌐 三語切換** — 從頂部下拉選單隨時切換繁體中文 / 简体中文 / English (US)；整個頁面（含榜單註釋與對比腳註）原地重新渲染，選擇會在下次造訪時記住。
- **基準測試榜單** — SWE-bench Verified、GPQA Diamond、MMLU-Pro 等，可在 DeepSeek V4 Pro 與 V4 Flash 之間切換（資料取自 DeepSeek 官方公開資料，附連結）。
- **旗艦對比** — 每個基準卡片將 DeepSeek V4 Pro 與最新旗艦（GPT-5.6 Sol、Claude Fable 5、Gemini 3.1 Pro、Grok 4.6、Qwen3.8-Max、Kimi K3、GLM-5.2、Mistral Large 3、Llama 4 Maverick）排名對比，每項分數附來源註（官方 model card 或第三方跑分）。
- **捲動時間軸** — SVG 隨捲動逐道生長；每個節點逐步組裝更精細的像素鯨魚，最終收束於「AI 設計設計 AI 的 AI」迴圈。
- **即時自適應版面** — 視窗被覆蓋層或瀏覽器 UI 擠壓時，主視覺即時重排（無需手動重新整理）。
- **單檔案零依賴** — 所有 logo、字型、圖示與圖形均內嵌為 data URI；僅 `index.html` 一個檔案，零網路依賴。
- **PWA** — 手機／桌面皆可安裝，離線可用。

## 🚀 開啟

直接用瀏覽器開啟 `index.html`，或本機起服務：

```bash
python -m http.server 8000
# → http://localhost:8000
```

## 📱 PWA（可安裝／離線）

本頁是漸進式 Web 應用：

- `manifest.webmanifest` — 應用名稱、主題、圖示
- `sw.js` — 離線快取 Service Worker
- `icon.svg` / `icon-192.png` / `icon-512.png` — 應用圖示

手機上：開啟託管位址 → **加入主畫面** → 全螢幕啟動，離線可用。

## 🔧 重新建置

頁面由 `build_page.py` 產生（內嵌鯨魚像素畫、logo 路徑與全部內容）：

```bash
python build_page.py   # 重寫 index.html
```

## 📄 版權與免責聲明

- 本專案是**非官方的粉絲作品**，與 **DeepSeek** 或 **Anthropic** 無任何關聯、背書或贊助關係。
- **DeepSeek**、DeepSeek 鯨魚標誌，以及 **Anthropic** 名稱與其文章，均為各權利人的商標或版權作品，權利歸其權利人所有。
- 文章文字與結構改編自 Anthropic 原文章，僅供學習與娛樂。
- 頁面內嵌的 Anthropic 可變字型屬 Anthropic 所有，僅用於個人、非商業、教學示範。
- 榜單分數引自 DeepSeek 官方公開資料（model card、技術報告）與第三方評測，僅作展示，不代表任何官方背書。
- 無任何商業用途意圖。如您是權利人並希望移除，請開 issue。

## 🐳 復刻者

[kkkzheli](https://github.com/kkkzheli) — 由 Claude Code 建置。

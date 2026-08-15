<div align="center">

[English (US)](README.md) · [简体中文](README.zh-CN.md) · **繁體中文**

</div>

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

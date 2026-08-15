<div align="center">

[English (US)](README.md) · **简体中文** · [繁體中文](README.zh-TW.md)

</div>

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

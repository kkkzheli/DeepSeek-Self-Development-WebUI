# -*- coding: utf-8 -*-
"""Assemble the DeepSeek recursive self-improvement page from generated data."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'D:/ClaudeCode/deepseek-rsi/'
node_rects = json.load(open(BASE + 'node-rects-v2.json'))
whale = json.load(open(BASE + 'whale-hero.json'))
syms = json.load(open(BASE + 'symbols-ds.json'))
whale_path = json.load(open(BASE + 'whale-path.json'))['path']

whale_cells_js = json.dumps(whale['cells'])
whale_w, whale_h = whale['W'], whale['H']

# ---- Whale logo SVG (official compact glyph) ----
LOGO_SVG = (
    '<svg class="{cls}" viewBox="0 0 27 21" fill="none" xmlns="http://www.w3.org/2000/svg">\n'
    '  <path d="{path}" fill="currentColor"/>\n'
    '</svg>'
).format(cls='{cls}', path=whale_path)

def whale_logo(cls=''):
    return LOGO_SVG.format(cls=cls)

# ---- Timeline SVG ----
def build_timeline_svg():
    lanes_y = [103, 269, 435, 601, 767]
    durations = ['1.80s', '1.37s', '0.94s', '0.50s', '0.20s']
    # icons per lane: (label, icon_symbol)
    lane_icons = [
        [('person', 'icon-person'), ('computer', 'icon-computer')],
        [('person', 'icon-person'), ('computer', 'icon-computer'), ('chatbot', 'icon-chat')],
        [('person', 'icon-person'), ('computer', 'icon-computer'), ('chatbot', 'icon-chat'), ('agent', 'icon-agent')],
        [('person', 'icon-person'), ('computer', 'icon-computer'), ('chatbot', 'icon-chat'), ('agent', 'icon-agent')],
        [],
    ]
    defs = '<defs>' + ''.join(syms.values()) + '</defs>'

    parts = ['<svg class="flow-svg" viewBox="20 0 557 182" xmlns="http://www.w3.org/2000/svg">', defs]

    # Background lane divider lines
    for y in lanes_y:
        parts.append(f'<path d="M 20 {y+83} L 577 {y+83}" stroke="var(--border-subtle)" stroke-width="1" opacity="0.35" fill="none"/>')

    # Loopback shape (rounded pill at bottom, behind lanes 0-3)
    parts.append('''<path class="loop-shape" d="M 73 724 L 515 724 A 43 43 0 0 1 558 767 L 558 842.05 A 43 43 0 0 1 515 885.05 L 73 885.05 A 43 43 0 0 1 30 842.05 L 30 767 A 43 43 0 0 1 73 724 Z M 136 810 L 452 810 A 20 20 0 0 1 472 830 L 472 834.95 A 20 20 0 0 1 452 854.95 L 136 854.95 A 20 20 0 0 1 116 834.95 L 116 830 A 20 20 0 0 1 136 810 Z" fill="var(--color-slate-150)" fill-rule="evenodd" opacity="0"/>''')

    # 5 lane groups
    node_key = ['n1', 'n2', 'n3', 'n4', 'n5']
    for li, y in enumerate(lanes_y):
        parts.append(f'<g class="flow-lane-opacity lane-{li}" style="--flow-duration: {durations[li]}">')
        parts.append('<g fill="none">')
        if li == 0 or li == 4:
            dash = 448
            parts.append(f'<path class="fl-pending flow-line-base" d="M 73 {y} L 471 {y}" stroke="var(--border-subtle)" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="{dash} {dash}" stroke-dashoffset="{dash}"/>')
            parts.append(f'<path class="fl-pending flow-line-accent" d="M 73 {y} L 471 {y}" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="4 10" stroke-dashoffset="0"/>')
        else:
            dash1 = 185
            parts.append(f'<path class="fl-pending flow-line-base" d="M 73 {y} L 208 {y}" stroke="var(--border-subtle)" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="{dash1} {dash1}" stroke-dashoffset="{dash1}"/>')
            parts.append(f'<path class="fl-pending flow-line-accent" d="M 73 {y} L 208 {y}" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="4 10" stroke-dashoffset="0"/>')
            dash2 = 278
            parts.append(f'<path class="fl-pending flow-line-base" d="M 243 {y+2} L 471 {y+2}" stroke="var(--border-subtle)" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="{dash2} {dash2}" stroke-dashoffset="{dash2}"/>')
            parts.append(f'<path class="fl-pending flow-line-accent" d="M 243 {y-2} L 471 {y-2}" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="4 10" stroke-dashoffset="0"/>')
        parts.append('</g>')

        # Start icons
        if li < 4:
            for ii, (label, icon) in enumerate(lane_icons[li]):
                ix = 73 + ii * 80
                parts.append('<g class="start-icon">')
                parts.append(f'<g transform="translate({ix}, {y})">')
                parts.append(f'<g class="icon-pop"><g transform="translate(-23, -23)"><use href="#{icon}" width="46" height="46"/></g></g>')
                parts.append('</g>')
                parts.append(f'<text x="{ix}" y="{y+65}" text-anchor="middle" class="micro icon-label">{label}</text>')
                parts.append('</g>')

        # End node with whale pixels
        parts.append(f'<g class="node-end node-{li}">')
        parts.append(f'<circle cx="515" cy="{y}" r="32" fill="#fff" stroke="var(--border-subtle)" stroke-width="1.5"/>')
        parts.append(f'<g class="node-pop">')
        parts.append(node_rects[node_key[li]])
        parts.append('</g>')
        parts.append('</g>')
        parts.append('</g>')

    # Loopback arrow flowing along the bottom path (drawn after lanes so on top)
    parts.append('''<g class="loop-flow" opacity="0">
      <path class="loop-arrow" d="M 73 767 L 471 767" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="448 448" stroke-dashoffset="0"/>
    </g>''')
    parts.append('</svg>')
    return '\n'.join(parts)

TIMELINE_SVG = build_timeline_svg()

# ---- Hero whale mask (for canvas) ----
# The whale cells, normalized for canvas drawing. Keep as-is (60x45 grid).

# ============ FULL PAGE ============
PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="description" content="DeepSeek Research — Our progress toward recursive self-improvement">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#ffffff">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="DeepSeek Research">
<title>DeepSeek Research — Recursive Self-Improvement</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
:root {
  --ds-blue-900: #1a2f6e;
  --ds-blue-800: #28397f;
  --ds-blue-700: #2f4c8f;
  --ds-blue-600: #4d6bfe;
  --ds-blue-500: #3964fe;
  --ds-blue-450: #5686fe;
  --ds-blue-400: #9db5ff;
  --ds-blue-300: #b7c8fe;
  --ds-blue-200: #d3e2ff;
  --ds-blue-100: #e4edfd;
  --ds-blue-50:  #edf3fe;
  --ds-neutral-1000: #0f1115;
  --ds-neutral-700:  #61666b;
  --ds-neutral-600:  #81858c;
  --ds-neutral-400:  #adb2b8;
  --ds-neutral-200:  #e1e5ee;
  --ds-neutral-100:  #ebeef2;
  --ds-neutral-75:   #f1f3f5;
  --ds-neutral-50:   #f9fafb;
  --ds-neutral-00:   #ffffff;
  --color-slate-150: #e8ebf0;

  --text-primary:    var(--ds-neutral-1000);
  --text-secondary:  var(--ds-neutral-700);
  --text-tertiary:   var(--ds-neutral-600);
  --bg-page:         var(--ds-neutral-00);
  --bg-surface:      var(--ds-neutral-75);
  --border-subtle:   var(--ds-neutral-200);
  --border-default:  var(--ds-neutral-100);
  --accent:          var(--ds-blue-600);
  --accent-bright:   var(--ds-blue-500);
  --accent-soft:     var(--ds-blue-50);
  --accent-warm:     #d97757;

  --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --page-margin: clamp(20px, 5vw, 80px);
  --ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
  --radius-md: 10px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
body {
  font-family: var(--font-sans);
  color: var(--text-primary);
  background: var(--bg-page);
  line-height: 1.6;
  overflow-x: hidden;
}

/* ===== Header ===== */
.site-header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  padding: 14px var(--page-margin);
  background: rgba(255,255,255,0.72);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s ease, background 0.3s ease;
}
.site-header.scrolled { border-bottom-color: var(--border-subtle); background: rgba(255,255,255,0.88); }
.header-inner { max-width: 1400px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; }
.logo { display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--text-primary); }
.logo-icon { width: 28px; height: 21px; flex-shrink: 0; color: var(--accent); }
.logo-text { font-size: 18px; font-weight: 700; letter-spacing: -0.02em; }
.logo-text span { color: var(--accent); }
.header-nav { display: flex; align-items: center; gap: 28px; list-style: none; }
.header-nav a { text-decoration: none; color: var(--text-secondary); font-size: 14px; font-weight: 500; transition: color 0.2s ease; }
.header-nav a:hover { color: var(--text-primary); }

/* ===== Hero: Whale cellular assembly ===== */
.hero {
  position: relative; height: 100vh; min-height: 600px;
  overflow: hidden; background: var(--bg-page);
}
.hero-canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
.hero-overlay {
  position: absolute; inset: 0; z-index: 1; pointer-events: none;
  background: radial-gradient(ellipse at 70% 45%, transparent 25%, rgba(255,255,255,0.5) 72%);
}
.hero-content {
  position: absolute; inset: 0; z-index: 2;
  display: flex; flex-direction: column; justify-content: center;
  padding: 0 var(--page-margin); max-width: 580px;
}
.hero-eyebrow {
  display: inline-flex; align-items: center; gap: 10px;
  font-size: 13px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--accent); margin-bottom: 20px;
}
.hero-eyebrow .logo-icon { width: 22px; height: 17px; }
.hero-title {
  font-size: clamp(40px, 6.5vw, 76px); font-weight: 800; line-height: 1.06;
  letter-spacing: -0.03em; color: var(--text-primary); margin-bottom: 24px;
}
.hero-subtitle {
  font-size: clamp(16px, 2vw, 20px); font-weight: 400; line-height: 1.55;
  color: var(--text-secondary); max-width: 500px;
}

.scroll-indicator {
  position: absolute; bottom: 32px; left: 50%; transform: translateX(-50%); z-index: 2;
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  color: var(--text-tertiary); font-size: 11px; font-weight: 500;
  letter-spacing: 0.08em; text-transform: uppercase; pointer-events: none;
}
.scroll-line { width: 1px; height: 40px; background: var(--border-default); position: relative; overflow: hidden; }
.scroll-line::after {
  content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background: var(--accent); animation: scroll-progress 2.5s var(--ease-out-quart) infinite;
}
@keyframes scroll-progress { 0% { transform: translateY(-100%); } 50% { transform: translateY(0%); } 100% { transform: translateY(100%); } }

/* ===== Timeline Section ===== */
.timeline-scroll { position: relative; height: 600vh; }
.timeline-sticky {
  position: sticky; top: 0; height: 100vh;
  display: flex; align-items: center; overflow: hidden;
  background: var(--bg-page);
}
.timeline-inner {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: clamp(32px, 6vw, 80px); max-width: 1200px; margin: 0 auto;
  padding: 0 var(--page-margin); width: 100%; align-items: center;
}

/* Flow SVG — locked to a fixed frame; viewBox grows to shrink content (reference behavior) */
.flow-visual { display: flex; align-items: center; justify-content: center; height: 100%; overflow: hidden; }
.flow-svg { height: min(86vh, 640px); width: auto; max-width: 100%; }

/* Lanes */
.flow-lane-opacity { transition: opacity 0.5s ease; }
.flow-lane-opacity[class~="dimmed"] { opacity: 0.18; }

/* Flow lines: base line draws in; accent dashes flow along it */
.fl-pending { transition: stroke 0.5s ease, opacity 0.5s ease; opacity: 1; }
.flow-line-base { opacity: 0.6; }
.flow-line-accent { opacity: 0; }
.flow-lane-opacity[class~="active"] .flow-line-base {
  opacity: 1;
  animation: flow-draw var(--flow-duration, 1.6s) ease-out forwards;
}
.flow-lane-opacity[class~="active"] .flow-line-accent {
  opacity: 1;
  animation: flow-dash var(--flow-duration, 1.6s) linear infinite;
}
@keyframes flow-draw { to { stroke-dashoffset: 0; } }
@keyframes flow-dash { to { stroke-dashoffset: -14; } }

/* Start icons pop in */
.start-icon { transition: opacity 0.4s ease; }
.icon-pop {
  transform: scale(0);
  transition: transform 0.55s var(--ease-out-expo), opacity 0.4s ease;
  transform-origin: center;
}
.flow-lane-opacity[class~="active"] .icon-pop {
  transform: scale(1);
  opacity: 1;
}

/* End node whale assembles */
.node-end rect { transition: opacity 0.3s ease; }
.node-pop {
  transform: scale(0);
  transition: transform 0.55s var(--ease-out-expo), opacity 0.4s ease;
  transform-origin: center;
}
.flow-lane-opacity[class~="active"] .node-pop {
  transform: scale(1);
  opacity: 1;
}
.node-end:not(.inactive) rect { opacity: 1; }
.node-end.inactive rect { opacity: 0.12; }

.icon-label {
  font-family: var(--font-sans); font-size: 9px; font-weight: 500;
  fill: var(--text-tertiary); text-anchor: middle;
  transition: opacity 0.5s ease;
}
.flow-lane-opacity[class~="active"] .icon-label { opacity: 1; }
.flow-lane-opacity:not([class~="active"]) .icon-label { opacity: 0.4; }

/* Loopback */
.loop-shape { transition: opacity 0.6s ease; }
.loop-shape.revealed { opacity: 1; }
.loop-flow { transition: opacity 0.6s ease; }
.loop-flow.revealed { opacity: 1; }
.loop-flow .loop-arrow { animation: flow-dash 0.5s linear infinite; }

/* Step Cards */
.timeline-steps { display: flex; flex-direction: column; gap: 20px; }
.step {
  padding: 16px 22px;
  border-left: 2px solid var(--border-subtle);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  transition: opacity 0.4s ease, border-color 0.4s ease, background 0.4s ease;
}
.step.dimmed { opacity: 0.18; }
.step.active { border-left-color: var(--accent); background: var(--bg-surface); opacity: 1; }
.step-year { font-size: 11px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-tertiary); margin-bottom: 4px; }
.step.active .step-year { color: var(--accent); }
.step-title { font-size: 17px; font-weight: 700; letter-spacing: -0.01em; color: var(--text-primary); margin-bottom: 6px; }
.step-body { font-size: 13px; line-height: 1.55; color: var(--text-secondary); }

/* ===== Article ===== */
.article { padding: 72px 0 96px; }
.article-inner { max-width: 760px; margin: 0 auto; padding: 0 var(--page-margin); }
.article h2 { font-size: 24px; font-weight: 700; letter-spacing: -0.02em; margin: 56px 0 16px; }
.article h2:first-child { margin-top: 0; }
.article h3 { font-size: 19px; font-weight: 700; letter-spacing: -0.01em; margin: 36px 0 12px; }
.article p { font-size: 16px; line-height: 1.7; color: var(--text-secondary); margin-bottom: 16px; }
.article p strong { color: var(--text-primary); }
.article ul { margin: 0 0 16px 20px; }
.article li { font-size: 15px; line-height: 1.65; color: var(--text-secondary); margin-bottom: 8px; }
.article hr { border: none; border-top: 1px solid var(--border-subtle); margin: 48px 0; }

/* Footer */
.site-footer { border-top: 1px solid var(--border-subtle); padding: 48px var(--page-margin); background: var(--bg-surface); }
.footer-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 24px; }
.footer-brand { display: flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 600; color: var(--text-primary); }
.footer-brand .logo-icon { width: 22px; height: 17px; color: var(--accent); }
.footer-text { font-size: 13px; color: var(--text-tertiary); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
  .hero-canvas { display: none; }
}
@media (max-width: 768px) {
  .timeline-inner { grid-template-columns: 1fr; gap: 0; padding: 0 16px; }
  .flow-visual { display: block; height: 42vh; margin: 0 auto; }
  .flow-svg { height: 42vh; width: auto; max-width: 100%; }
  .timeline-steps { gap: 10px; margin-top: 4px; overflow-y: auto; }
  .step { padding: 10px 14px; }
  .step-title { font-size: 15px; }
  .step-body { font-size: 12px; }
  .hero-content { justify-content: flex-start; padding-top: 120px; max-width: 100%; }
  .hero-eyebrow { margin-bottom: 12px; }
  .hero-title { font-size: clamp(30px, 9vw, 46px); margin-bottom: 12px; }
  .hero-subtitle { font-size: 14px; max-width: 100%; }
  .hero-overlay {
    background: radial-gradient(ellipse at 50% 30%, transparent 20%, rgba(255,255,255,0.55) 75%);
  }
  .scroll-indicator { bottom: 16px; }
  .header-nav { gap: 14px; }
  .article-inner { padding: 0 20px; }
  .article h2 { font-size: 21px; margin-top: 40px; }
  .article p { font-size: 15px; }
}
</style>
</head>
<body>

<!-- Header -->
<header class="site-header" id="header">
  <div class="header-inner">
    <a href="#" class="logo" aria-label="DeepSeek Research">
      __LOGO__
      <span class="logo-text">DeepSeek <span>Research</span></span>
    </a>
    <nav><ul class="header-nav"><li><a href="#timeline">Research</a></li><li><a href="#about">About</a></li></ul></nav>
  </div>
</header>

<!-- Hero -->
<section class="hero" id="hero">
  <canvas class="hero-canvas" id="hero-canvas" aria-hidden="true"></canvas>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <p class="hero-eyebrow">__LOGO_SMALL__ DeepSeek Research Institute</p>
    <h1 class="hero-title">When AI builds itself</h1>
    <p class="hero-subtitle">Our progress toward recursive self-improvement — where AI systems learn to design, train, and refine the next generation of intelligence. Watch the DeepSeek whale assemble itself, cell by cell, the way the loop compounds.</p>
  </div>
  <div class="scroll-indicator" aria-hidden="true"><span>Scroll</span><div class="scroll-line"></div></div>
</section>

<!-- Timeline -->
<section class="timeline-scroll" id="timeline-scroll">
  <div class="timeline-sticky">
    <div class="timeline-inner">

      <div class="flow-visual">
        __TIMELINE_SVG__
      </div>

      <!-- Step Cards -->
      <div class="timeline-steps">
        <div class="step active" id="step-0">
          <p class="step-year">2021–2023</p>
          <h3 class="step-title">Building the first DeepSeek</h3>
          <p class="step-body">In the early days, work at DeepSeek looked like work at any other tech company: people writing code, designing architectures, and tuning hyperparameters by hand. Human researchers drove every decision.</p>
        </div>
        <div class="step dimmed" id="step-1">
          <p class="step-year">2023–2025</p>
          <h3 class="step-title">Chatbots</h3>
          <p class="step-body">People used early AI chatbots to help with parts of the process, like generating short code snippets and summarizing research papers. The models were assistants — useful but not autonomous.</p>
        </div>
        <div class="step dimmed" id="step-2">
          <p class="step-year">2025–2026</p>
          <h3 class="step-title">Coding agents</h3>
          <p class="step-body">As agents became more capable, they were able to write and edit code on their own. DeepSeek's R1 reasoning model could verify outputs, and coding agents began contributing to training infrastructure.</p>
        </div>
        <div class="step dimmed" id="step-3">
          <p class="step-year">Today</p>
          <h3 class="step-title">Autonomous agents</h3>
          <p class="step-body">Agents can now run code themselves and delegate hours of work to other agents. They assist in architecture search, data curation, and hyperparameter tuning — the research loop starts accelerating.</p>
        </div>
        <div class="step dimmed" id="step-4">
          <p class="step-year">20XX?</p>
          <h3 class="step-title">Closing the loop</h3>
          <p class="step-body">In the future, agents could become capable enough to build and train models themselves. If this happens, AI progress may start to accelerate exponentially — not through better hardware, but through <strong>AI designing the AIs that design the AIs</strong>.</p>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- Article -->
<article class="article" id="about">
  <div class="article-inner">

    <h2>Evidence from the outside world</h2>
    <p>The rate at which AI models improve is accelerating. The length of tasks that they can reliably complete on their own has been doubling roughly every four months, up from an earlier trend of doubling every seven months. In March 2024, DeepSeek's first reasoning models could complete software tasks that take humans about four minutes. A year later, R1 could manage tasks that took about an hour and a half. If this trend holds, tasks that take a skilled person days could come into range soon.</p>
    <p>The same pattern appears on coding and research benchmarks. <strong>SWE-bench</strong>, a standard test of real-world software engineering, hands a model an actual open-source codebase and a real bug report, and asks it to write a fix that passes the project's own tests. Models have gone from scoring in the low single digits to saturating the benchmark in two years. Benchmarks that test whether a model can reproduce existing research tell the same story: AI systems went from succeeding roughly 20% of the time in 2024 to saturating the benchmark fifteen months later.</p>

    <h2>Evidence from within DeepSeek</h2>
    <p>Building a frontier model takes two broad categories of work. There is <strong>engineering</strong>: writing the code, standing up the infrastructure, and overseeing model training. And there is <strong>research</strong>: deciding what experiments to run, interpreting what comes back, and figuring out which ideas to try next.</p>
    <p>Across both, the picture is consistent. In engineering, the model can be handed an underspecified problem and figure out how to solve it; humans supply the goal, but they no longer need to supply the method. In research, it can already match or outperform skilled humans at executing a well-specified experiment. However, large performance gaps persist when it comes to exercising judgement in choosing goals. That is the gap between AI today and a future system that could autonomously design its own successor.</p>
    <p>The model writes a significant proportion of DeepSeek's code. Before the introduction of agentic coding tools, this number was in the low single digits. That shift also shows up in output per engineer: lines of code merged per engineer per day stayed constant for years, then began to climb when the model began to run code rather than just suggesting it. The slope steepened again when models began to work autonomously over longer time horizons.</p>

    <hr>

    <h2>What might the future look like?</h2>
    <p>The evidence suggests that the human role is narrowing at each step in the AI development process. Once model- and human-authored code reach parity, humans will stop writing code entirely and shift to reviewing it. But if they can't review code as quickly as the model can generate it, human review becomes the bottleneck. Similarly, once the model can run experiments, the question shifts towards "which of these experiments is worth running?"</p>
    <p>An area of human comparative advantage, for now, is research taste and judgement — choosing which problems matter, which results to trust, and when an approach is a dead end. It is genuinely unclear whether today's training methods and architectures could unlock that capacity. But AI is rarely advanced by "eureka!" moments. There have been a few, like the Transformer architecture, but paradigm-shifting ideas arrive years apart. In between, most progress is incremental: we scale something up, see what breaks, fix it, and try again. That is exactly the kind of workflow the model now excels at.</p>

    <h2>What if we're wrong?</h2>
    <p>A natural objection is that the work that is still in human hands — choosing which problems to work on — is what matters most. Without that judgement, the model is a capable assistant, but not a system that could drive AI progress on its own.</p>
    <p>Even if the model never achieves good research taste, a conservative reading of the evidence still implies compounding acceleration. If humans spend most of their time on the single-digit fraction of work that is direction-setting, while the model handles the rest, that means each engineer is steering far more work than before. The less conservative reading is that the early evidence on improving research judgement — narrow as it is today — is an indicator that this capability is improving as well. "Research taste" might be just another capability that AI systems fail at for a time, then get good at.</p>

    <h2>Possible futures</h2>
    <p>What happens next depends on two things: whether the trend continues, and what we choose to do if it does. We can imagine at least three scenarios:</p>
    <ul>
      <li><strong>The trend stalls, but today's capabilities are widely diffused.</strong> Many of these trajectories may actually be S-curves. We may be approaching the bend, where returns to scale diminish and the line flattens.</li>
      <li><strong>AI labs continue to see compounding efficiency gains.</strong> AI development becomes substantially automated, but humans continue to set research directions and judge results. 100-person companies could do the work of 10,000-person organizations.</li>
      <li><strong>AI systems become capable of full recursive self-improvement.</strong> If technical trends continue and AI systems are able to develop the capabilities inherent to transformative human ingenuity, then they could design and refine themselves — closing the loop.</li>
    </ul>
    <p>In that last world, the pace of progress in AI development becomes determined entirely by the availability of compute. Humans play a substantially diminished role, likely moving most of our effort towards oversight, validation, and verification of an expanding "virtual lab" run by AI systems.</p>
    <p>We are not there yet, and recursive self-improvement is not inevitable. But it could come sooner than most institutions are prepared for.</p>

  </div>
</article>

<!-- Footer -->
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      __LOGO_FOOTER__
      DeepSeek Research
    </div>
    <p class="footer-text">Exploring the frontier of recursive self-improvement. © 2026 DeepSeek.</p>
  </div>
</footer>

<script>
// ===== Hero Canvas — Recursive cellular field that keeps assembling the whale =====
// Faithful to Anthropic's hero: a full-canvas grid of faint cells where a
// small population of live cells churns continuously. The whale mark acts as a
// probabilistic attractor — its silhouette keeps emerging from the evolving
// field and then dissipating, over and over, like recursive self-improvement.
(function() {
  const canvas = document.getElementById('hero-canvas');
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  const hero = document.getElementById('hero');

  // Official DeepSeek whale mask (60x45 grid) — the attractor shape
  const WC = __WHALE_CELLS__;
  const WX = __WHALE_W__, WY = __WHALE_H__;

  const CELL = 13;            // cell size (px)
  const GAP = 3;              // gap between cells
  const PITCH = CELL + GAP;   // grid pitch

  let w, h, cols, rows;
  let grid, next;             // 0=dead, 1..K=age
  let whaleSet = {};          // lookup "x,y" -> true
  let ox = 0, oy = 0;         // whale attractor origin (grid coords)
  let mx = -999, my = -999, tmx = -999, tmy = -999;
  let cycle = 0;              // cycle counter -> re-seed periodically
  const MAX_AGE = 5;

  // DeepSeek blue palette, darker toward the whale's core
  const COLORS = ['#9db5ff', '#5686fe', '#3964fe', '#4d6bfe', '#2f4c8f'];

  function resize() {
    const r = hero.getBoundingClientRect();
    w = r.width; h = r.height;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = w * dpr; canvas.height = h * dpr;
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cols = Math.floor(w / PITCH) + 2;
    rows = Math.floor(h / PITCH) + 2;
    // Scale whale to ~40% of viewport height so it reads as a logo, not a mural
    const targetH = Math.floor(h * 0.4 / PITCH);
    const scale = Math.max(10, Math.min(WY, targetH)) / WY;
    const wW = Math.round(WX * scale), wH = Math.round(WY * scale);
    let oxp, oyp;
    if (w < 768) {
      oxp = Math.floor((w - wW * PITCH) / 2 / PITCH);
      oyp = Math.floor(h * 0.55 / PITCH);
    } else {
      oxp = Math.floor((w - wW * PITCH - Math.max(60, w * 0.05)) / PITCH);
      oyp = Math.floor((h - wH * PITCH) / 2 / PITCH);
    }
    // Downsample whale mask to wW x wH grid
    // WC is [[x,y],...]; convert to a 2D lookup
    const wmask = {};
    WC.forEach(function(c) { wmask[c[1] * WX + c[0]] = true; });
    whaleSet = {};
    for (let gy = 0; gy < wH; gy++)
      for (let gx = 0; gx < wW; gx++) {
        const sx = Math.floor(gx * WX / wW), sy = Math.floor(gy * WY / wH);
        if (wmask[sy * WX + sx]) {
          whaleSet[(gx + oxp) + ',' + (gy + oyp)] = true;
        }
      }
    ox = oxp; oy = oyp;
    initGrid();
  }

  function initGrid() {
    grid = Array.from({length: rows}, function() { return new Array(cols).fill(0); });
    next = Array.from({length: rows}, function() { return new Array(cols).fill(0); });
    seedWhale();
  }

  // Initialize: fill the whale silhouette with cells; the automaton then keeps
  // it alive and churning, with fresh cells feeding in from the edges.
  function seedWhale() {
    clearGrid(grid);
    // lit ~85% of whale cells so the logo reads instantly on load
    const keys = Object.keys(whaleSet);
    for (let i = 0; i < keys.length; i++) {
      if (Math.random() < 0.85) {
        const xy = keys[i].split(',');
        const gx = +xy[0], gy = +xy[1];
        if (gx >= 0 && gx < cols && gy >= 0 && gy < rows) grid[gy][gx] = 1 + Math.floor(Math.random() * 3);
      }
    }
    // a few stray cells just outside to seed the outer churn
    const sH = Math.round(WY * Math.min(1, (h * 0.4 / PITCH) / WY));
    const sW = Math.round(WX * Math.min(1, (h * 0.4 / PITCH) / WY));
    for (let i = 0; i < 8; i++) {
      const gx = ox + Math.floor(Math.random() * sW);
      const gy = oy + Math.floor(Math.random() * sH) + sH;   // below the whale
      if (gx >= 0 && gx < cols && gy >= 0 && gy < rows && !whaleSet[gx + ',' + gy]) grid[gy][gx] = 1;
    }
  }

  function clearGrid(g) {
    for (let y = 0; y < rows; y++)
      for (let x = 0; x < cols; x++) g[y][x] = 0;
  }

  function countNeighbors(g, x, y) {
    let n = 0;
    for (let dy = -1; dy <= 1; dy++)
      for (let dx = -1; dx <= 1; dx++) {
        if (!dx && !dy) continue;
        const nx = x + dx, ny = y + dy;
        if (nx >= 0 && nx < cols && ny >= 0 && ny < rows && g[ny][nx] > 0) n++;
      }
    return n;
  }

  // Distance attractor strength (0..1) for a cell: 1 on whale, fading away
  let attractCache = {};
  function attractAt(x, y) {
    const key = x + ',' + y;
    if (attractCache[key] !== undefined) return attractCache[key];
    let a = 0;
    for (let dy = -3; dy <= 3 && a < 1; dy++)
      for (let dx = -3; dx <= 3 && a < 1; dx++) {
        if (whaleSet[(x + dx) + ',' + (y + dy)]) a = Math.max(a, 1 - (Math.abs(dx) + Math.abs(dy)) / 7);
      }
    attractCache[key] = a;
    return a;
  }

  function rebuildAttractCache() {
    attractCache = {};
  }

  // One automaton tick: cells churn under Conway-like rules; the whale field
  // biases births/survival so the silhouette repeatedly condenses out of the
  // noise. Max age caps every cell, so nothing freezes — it keeps growing.
  function step() {
    for (let y = 0; y < rows; y++)
      for (let x = 0; x < cols; x++) {
        const n = countNeighbors(grid, x, y);
        const a = attractAt(x, y);
        let v = 0;
        if (grid[y][x] > 0) {
          if (a >= 0.99) {
            // inside the whale silhouette: near-immortal, just cycles shade
            v = grid[y][x] + 1 > MAX_AGE ? 1 : grid[y][x] + 1;
          } else if (a >= 0.5) {
            // whale fringe: strong persistence, occasional churn
            if (n === 2 || n === 3 || Math.random() < 0.85) v = Math.min(MAX_AGE, grid[y][x] + 1);
            else v = 0;
          } else if (n === 2 || n === 3) {
            v = Math.min(MAX_AGE, grid[y][x] + 1);
          } else if (n === 1 && Math.random() < 0.3 * a) {
            v = grid[y][x];
          } else {
            v = 0;
          }
        } else {
          // empty: births concentrated on the whale fringe (growth boundary)
          if (n === 3) {
            v = Math.random() < 0.15 + 0.7 * Math.min(1, a * 2) ? 1 : 0;
          } else if (n === 2) {
            v = Math.random() < 0.08 * a ? 1 : 0;
          }
        }
        next[y][x] = v;
      }

    // Slow feeding rain keeps new cells arriving near the whale -> growth
    if (Math.random() < 0.02) {
      const cx = ox + 8, cy = oy + 8;
      const ang = Math.random() * Math.PI * 2;
      const dist = 3 + Math.random() * 12;
      const gx = Math.round(cx + Math.cos(ang) * dist);
      const gy = Math.round(cy + Math.sin(ang) * dist * 0.85);
      if (gx >= 0 && gx < cols && gy >= 0 && gy < rows) next[gy][gx] = 1;
    }

    const tmp = grid; grid = next; next = tmp;
    cycle++;
    // Every ~20s re-seed to restart the grow-out (the loop repeats)
    if (cycle > 200) { cycle = 0; seedWhale(); }
  }

  function drawCell(gx, gy, age, t) {
    const px = gx * PITCH, py = gy * PITCH;
    const pulse = 0.93 + 0.07 * Math.sin(t * 2 + (gx + gy) * 0.4);
    const s = CELL * pulse;
    ctx.fillStyle = COLORS[Math.min(age, MAX_AGE) - 1];
    roundRect(px + (CELL - s) / 2 + 0.5, py + (CELL - s) / 2 + 0.5, s - 1, s - 1, s * 0.3);
  }

  function roundRect(x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
    ctx.fill();
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    const t = performance.now() / 1000;
    mx += (tmx - mx) * 0.06; my += (tmy - my) * 0.06;

    // ---- Resting grid: faint rounded cells across the whole canvas ----
    ctx.fillStyle = 'rgba(237,243,254,0.6)';
    for (let gy = 0; gy < rows; gy++)
      for (let gx = 0; gx < cols; gx++) {
        if (grid[gy][gx] > 0) continue;
        roundRect(gx * PITCH + 1, gy * PITCH + 1, CELL - 1, CELL - 1, CELL * 0.3);
      }

    // ---- Live cells ----
    for (let gy = 0; gy < rows; gy++)
      for (let gx = 0; gx < cols; gx++) {
        const v = grid[gy][gx];
        if (v <= 0) continue;
        const px = gx * PITCH + CELL / 2, py = gy * PITCH + CELL / 2;
        const dist = Math.sqrt((px - mx) * (px - mx) + (py - my) * (py - my));
        if (dist < 140) {
          ctx.globalAlpha = 0.5 + (140 - dist) / 140 * 0.5;
          drawCell(gx, gy, v, t);
          ctx.globalAlpha = 1;
        } else {
          drawCell(gx, gy, v, t);
        }
      }
  }

  function loop() {
    draw();
    // automaton ticks ~10x/sec, drawing at full framerate (like the reference)
    if (Math.floor(performance.now() / 100) !== Math.floor((performance.now() - 100) / 100)) {
      step();
    }
    requestAnimationFrame(loop);
  }

  hero.addEventListener('mousemove', function(e) {
    const r = hero.getBoundingClientRect();
    tmx = e.clientX - r.left; tmy = e.clientY - r.top;
  });
  hero.addEventListener('mouseleave', function() { tmx = -999; tmy = -999; });
  hero.addEventListener('touchmove', function(e) {
    const r = hero.getBoundingClientRect();
    tmx = e.touches[0].clientX - r.left; tmy = e.touches[0].clientY - r.top;
  }, {passive: true});
  hero.addEventListener('touchend', function() { tmx = -999; tmy = -999; });

  window.addEventListener('resize', function() { resize(); rebuildAttractCache(); });
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { resize(); draw(); return; }
  resize();
  rebuildAttractCache();
  requestAnimationFrame(loop);
})();

// ===== Timeline Scroll Controller =====
(function() {
  const section = document.getElementById('timeline-scroll');
  const steps = document.querySelectorAll('.step');
  const lanes = document.querySelectorAll('.flow-lane-opacity');
  const loopShape = document.querySelector('.loop-shape');
  const loopFlow = document.querySelector('.loop-flow');
  const flowSvg = document.querySelector('.flow-svg');
  let current = -1, ticking = false;
  const T = 5;
  // Growing viewBox height anchors (matches reference reveal cadence)
  const VB = [182, 348, 514, 680, 930, 930];

  function easeOutCubic(x) { return 1 - Math.pow(1 - x, 3); }

  function setViewH(progress) {
    if (!flowSvg) return;
    const step = Math.min(T - 1, Math.floor(progress * T));
    const sub = Math.min(1, progress * T - step);
    const h = VB[step] + (VB[step + 1] - VB[step]) * easeOutCubic(sub);
    const cur = flowSvg.getAttribute('viewBox');
    flowSvg.setAttribute('viewBox', '20 0 557 ' + h.toFixed(2));
  }

  function setStep(idx) {
    if (idx === current) return;
    current = idx;

    steps.forEach(function(s, i) {
      s.classList.remove('active', 'dimmed');
      if (i === idx) s.classList.add('active');
      else s.classList.add('dimmed');
    });

    lanes.forEach(function(l, j) {
      var cls = l.getAttribute('class') || '';
      cls = cls.replace(/dimmed/g, '').replace(/active/g, '').replace(/\s+/g, ' ');
      if (j <= idx) cls += ' active';
      else cls += ' dimmed';
      l.setAttribute('class', cls.trim());
    });

    // Node whale pixel visibility: reveal the current node fully
    document.querySelectorAll('.node-end').forEach(function(n) {
      n.classList.remove('inactive');
    });

    const atEnd = idx >= 4;
    if (loopShape) { atEnd ? loopShape.classList.add('revealed') : loopShape.classList.remove('revealed'); }
    if (loopFlow) { atEnd ? loopFlow.classList.add('revealed') : loopFlow.classList.remove('revealed'); }
  }

  function update() {
    const r = section.getBoundingClientRect();
    const scrollable = r.height - window.innerHeight;
    if (scrollable <= 0) { ticking = false; return; }
    const progress = Math.max(0, Math.min(1, -r.top / scrollable));
    setViewH(progress);
    var newStep = Math.min(T - 1, Math.max(0, Math.floor(progress * T)));
    setStep(newStep);
    ticking = false;
  }

  window.addEventListener('scroll', function() {
    if (!ticking) { requestAnimationFrame(update); ticking = true; }
  }, {passive: true});
  update();
})();

// ===== Header =====
(function() {
  const hdr = document.getElementById('header');
  let t = false;
  window.addEventListener('scroll', function() {
    if (!t) {
      requestAnimationFrame(function() { hdr.classList.toggle('scrolled', window.scrollY > 20); t = false; });
      t = true;
    }
  }, {passive: true});
})();

// ===== Service Worker (offline / PWA) =====
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('sw.js').catch(function(e) {
      // registration may fail on file:// or offline dev; ignore silently
    });
  });
}
</script>

</body>
</html>
"""

# Substitute data
PAGE = PAGE.replace('__LOGO__', whale_logo('logo-icon'))
PAGE = PAGE.replace('__LOGO_SMALL__', whale_logo('logo-icon'))
PAGE = PAGE.replace('__LOGO_FOOTER__', whale_logo('logo-icon'))
PAGE = PAGE.replace('__TIMELINE_SVG__', TIMELINE_SVG)
PAGE = PAGE.replace('__WHALE_CELLS__', whale_cells_js)
PAGE = PAGE.replace('__WHALE_W__', str(whale_w))
PAGE = PAGE.replace('__WHALE_H__', str(whale_h))

open(BASE + 'index.html', 'w', encoding='utf-8').write(PAGE)
print('index.html written:', len(PAGE), 'chars')

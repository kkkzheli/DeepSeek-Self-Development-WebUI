# -*- coding: utf-8 -*-
"""Assemble the DeepSeek recursive self-improvement page from generated data."""
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'D:/ClaudeCode/deepseek-rsi/'
whale = json.load(open(BASE + 'whale-hero.json'))
syms = json.load(open(BASE + 'symbols-ds.json'))
whale_path = json.load(open(BASE + 'whale-path.json'))['path']

# ---- Anthropic's own English fonts, embedded so the page stays self-contained ----
# Anthropic Sans (UI text + article body), roman + italic, pulled from
# anthropic.com's own @font-face declarations and inlined as base64.
# The files are VARIABLE fonts (wght axis 300-800 — verified in-browser: the same
# bytes render measurably wider at 700/800), so declaring the full range makes
# every weight render with real glyphs instead of synthesized faux bold.
import base64
_FONT_FILES = [
    ('AnthropicSans',  'fonts/AnthropicSans_Roman.woff2',  '300 800', 'normal'),
    ('AnthropicSans',  'fonts/AnthropicSans_Italic.woff2', '300 800', 'italic'),
    ('AnthropicSerif', 'fonts/AnthropicSerif_Roman.woff2',  '300 800', 'normal'),
    ('AnthropicSerif', 'fonts/AnthropicSerif_Italic.woff2', '300 800', 'italic'),
]
def _font_face_css():
    out = []
    for _name, _path, _weight, _style in _FONT_FILES:
        _b64 = base64.b64encode(open(BASE + _path, 'rb').read()).decode()
        out.append('@font-face{font-family:%s;font-weight:%s;font-style:%s;'
                   'src:url("data:font/woff2;base64,%s") format("woff2");'
                   'font-display:swap;}' % (_name, _weight, _style, _b64))
    return '\n'.join(out)
FONT_CSS = _font_face_css()

# ---- Lab logos for the compare section, inlined as data URIs so the page is ----
# fully self-contained: no runtime network dependency. Files live in
# assets/logos/ (downloaded once); if a file is missing, falls back to the
# original remote URL so the build still succeeds.
def _logo_uri(fname, mime):
    _p = BASE + 'assets/logos/' + fname
    try:
        with open(_p, 'rb') as _f:
            return 'data:%s;base64,%s' % (mime, base64.b64encode(_f.read()).decode())
    except IOError:
        return None
_LOGO_FILES = [
    ('openai',    'openai.svg',  'image/svg+xml'),
    ('anthropic', 'claude.svg',  'image/svg+xml'),
    ('google',    'google.svg',  'image/svg+xml'),
    ('meta',      'meta.svg',    'image/svg+xml'),
    ('qwen',      'qwen.svg',    'image/svg+xml'),
    ('kimi',      'kimi.webp',   'image/webp'),
    ('glm',       'glm.svg',     'image/svg+xml'),
    ('mistral',   'mistral.svg', 'image/svg+xml'),
]
LOGO_URIS = {_k: _logo_uri(_f, _m) for _k, _f, _m in _LOGO_FILES}

# ---- i18n: full-page language switching (en / zh-CN / zh-TW) ----
# Static text gets data-i18n="key" in the template; dynamic JS strings use
# per-field objects {en, 'zh-CN', 'zh-TW'} resolved through t(). Brand names
# and benchmark names stay untranslated.
I18N = {
'en': {
  # header / ui
  'nav_research': 'Research', 'nav_about': 'About', 'theme_toggle': 'Toggle theme',
  'lang_change': 'Change language', 'lang_menu': 'Language',
  'cmp_rank': 'No. {n}',
  # hero
  'hero_inst': 'Research Institute',
  'hero_title': 'When AI<br>builds itself',
  'hero_sub': 'Our progress toward recursive self-improvement — where AI systems learn to design, train, and refine the next generation of intelligence. Watch the DeepSeek whale assemble itself, cell by cell, the way the loop compounds.',
  'btn_chat': 'Try DeepSeek Chat', 'btn_platform': 'DeepSeek Platform',
  'scroll': 'Scroll',
  # timeline steps
  's0_title': 'Building the first DeepSeek',
  's0_body': 'In the early days, work at DeepSeek looked like work at any other tech company: people writing code, designing architectures, and tuning hyperparameters by hand. Human researchers drove every decision.',
  's1_title': 'Chatbots',
  's1_body': 'People used early AI chatbots to help with parts of the process, like generating short code snippets and summarizing research papers. The models were assistants — useful but not autonomous.',
  's2_title': 'Coding agents',
  's2_body': 'As agents became more capable, they were able to write and edit code on their own. DeepSeek’s R1 reasoning model could verify outputs, and coding agents began contributing to training infrastructure.',
  's3_title': 'Autonomous agents',
  's3_body': 'Agents can now run code themselves and delegate hours of work to other agents. They assist in architecture search, data curation, and hyperparameter tuning — the research loop starts accelerating.',
  's4_title': 'Closing the loop',
  's4_body': 'In the future, agents could become capable enough to build and train models themselves. If this happens, AI progress may start to accelerate exponentially — not through better hardware, but through <strong>AI designing the AIs that design the AIs</strong>.',
  # benchmarks
  'bench_eyebrow': 'Benchmarks',
  'bench_title': 'DeepSeek V4, measured',
  'bench_sub': 'Every score below is quoted from DeepSeek’s own model cards and the V4 technical report — all at maximum reasoning effort. Toggle between the two members of the V4 family.',
  'bench_asof': 'Data as of <strong>August 13, 2026</strong> — DeepSeek-V4-Pro-0813 and DeepSeek-V4-Flash-0731 model cards.',
  'bench_src_pre': 'Sources:', 'bench_src_post': 'This page is an unofficial replica — scores are shown for entertainment and education only.',
  'bench_src_and': ', and', 'bench_src_comma': ',',
  'bench_card_pro': 'DeepSeek-V4-Pro model card', 'bench_card_flash': 'DeepSeek-V4-Flash model card', 'bench_card_report': 'V4 technical report',
  # compare
  'cmp_eyebrow': 'Against the field',
  'cmp_title': 'How V4 stacks up',
  'cmp_sub': 'Latest flagship scores from each lab’s own publications, next to DeepSeek V4 Pro. Bars are color-coded per lab and the DeepSeek row is highlighted. Eval conditions differ between labs, so read this as a rough sketch, not a ranking.',
  'cmp_asof': 'Data collected <strong>August 15, 2026</strong> from official model cards and third-party leaderboards (vals.ai, tbench.ai). Terminal-Bench figures span versions 1.0–3.0.',
  'cmp_src_pre': 'Sources:', 'cmp_src_post': 'This page is an unofficial replica — scores are shown for entertainment and education only.',
  'cmp_src_lead': 'each lab’s official model card or launch post;',
  'cmp_src_card': 'the DeepSeek row quotes the DeepSeek-V4-Pro model card',
  # article
  'a1_h': 'Evidence from the outside world',
  'a1_p1': 'The rate at which AI models improve is accelerating. The length of tasks that they can reliably complete on their own has been doubling roughly every four months, up from an earlier trend of doubling every seven months. In March 2024, DeepSeek’s first reasoning models could complete software tasks that take humans about four minutes. A year later, R1 could manage tasks that took about an hour and a half. If this trend holds, tasks that take a skilled person days could come into range soon.',
  'a1_p2': 'The same pattern appears on coding and research benchmarks. <strong>SWE-bench</strong>, a standard test of real-world software engineering, hands a model an actual open-source codebase and a real bug report, and asks it to write a fix that passes the project’s own tests. Models have gone from scoring in the low single digits to saturating the benchmark in two years. Benchmarks that test whether a model can reproduce existing research tell the same story: AI systems went from succeeding roughly 20% of the time in 2024 to saturating the benchmark fifteen months later.',
  'a2_h': 'Evidence from within DeepSeek',
  'a2_p1': 'Building a frontier model takes two broad categories of work. There is <strong>engineering</strong>: writing the code, standing up the infrastructure, and overseeing model training. And there is <strong>research</strong>: deciding what experiments to run, interpreting what comes back, and figuring out which ideas to try next.',
  'a2_p2': 'Across both, the picture is consistent. In engineering, the model can be handed an underspecified problem and figure out how to solve it; humans supply the goal, but they no longer need to supply the method. In research, it can already match or outperform skilled humans at executing a well-specified experiment. However, large performance gaps persist when it comes to exercising judgement in choosing goals. That is the gap between AI today and a future system that could autonomously design its own successor.',
  'a2_p3': 'The model writes a significant proportion of DeepSeek’s code. Before the introduction of agentic coding tools, this number was in the low single digits. That shift also shows up in output per engineer: lines of code merged per engineer per day stayed constant for years, then began to climb when the model began to run code rather than just suggesting it. The slope steepened again when models began to work autonomously over longer time horizons.',
  'a3_h': 'What might the future look like?',
  'a3_p1': 'The evidence suggests that the human role is narrowing at each step in the AI development process. Once model- and human-authored code reach parity, humans will stop writing code entirely and shift to reviewing it. But if they can’t review code as quickly as the model can generate it, human review becomes the bottleneck. Similarly, once the model can run experiments, the question shifts towards “which of these experiments is worth running?”',
  'a3_p2': 'An area of human comparative advantage, for now, is research taste and judgement — choosing which problems matter, which results to trust, and when an approach is a dead end. It is genuinely unclear whether today’s training methods and architectures could unlock that capacity. But AI is rarely advanced by “eureka!” moments. There have been a few, like the Transformer architecture, but paradigm-shifting ideas arrive years apart. In between, most progress is incremental: we scale something up, see what breaks, fix it, and try again. That is exactly the kind of workflow the model now excels at.',
  'a4_h': 'What if we’re wrong?',
  'a4_p1': 'A natural objection is that the work that is still in human hands — choosing which problems to work on — is what matters most. Without that judgement, the model is a capable assistant, but not a system that could drive AI progress on its own.',
  'a4_p2': 'Even if the model never achieves good research taste, a conservative reading of the evidence still implies compounding acceleration. If humans spend most of their time on the single-digit fraction of work that is direction-setting, while the model handles the rest, that means each engineer is steering far more work than before. The less conservative reading is that the early evidence on improving research judgement — narrow as it is today — is an indicator that this capability is improving as well. “Research taste” might be just another capability that AI systems fail at for a time, then get good at.',
  'a5_h': 'Possible futures',
  'a5_p1': 'What happens next depends on two things: whether the trend continues, and what we choose to do if it does. We can imagine at least three scenarios:',
  'a5_li1': '<strong>The trend stalls, but today’s capabilities are widely diffused.</strong> Many of these trajectories may actually be S-curves. We may be approaching the bend, where returns to scale diminish and the line flattens.',
  'a5_li2': '<strong>AI labs continue to see compounding efficiency gains.</strong> AI development becomes substantially automated, but humans continue to set research directions and judge results. 100-person companies could do the work of 10,000-person organizations.',
  'a5_li3': '<strong>AI systems become capable of full recursive self-improvement.</strong> If technical trends continue and AI systems are able to develop the capabilities inherent to transformative human ingenuity, then they could design and refine themselves — closing the loop.',
  'a5_p2': 'In that last world, the pace of progress in AI development becomes determined entirely by the availability of compute. Humans play a substantially diminished role, likely moving most of our effort towards oversight, validation, and verification of an expanding “virtual lab” run by AI systems.',
  'a5_p3': 'We are not there yet, and recursive self-improvement is not inevitable. But it could come sooner than most institutions are prepared for.',
  # footer
  'footer_text': 'Exploring the frontier of recursive self-improvement.',
  'footer_replica_pre': 'Replica by',
},
'zh-CN': {
  'nav_research': '研究', 'nav_about': '关于', 'theme_toggle': '切换主题',
  'lang_change': '切换语言', 'lang_menu': '语言',
  'cmp_rank': '第 {n} 名',
  'hero_inst': '研究机构',
  'hero_title': '当 AI 亲手<br>打造自己',
  'hero_sub': '我们迈向递归式自我改进的进程——AI 系统学会设计、训练并打磨下一代智能。观看 DeepSeek 鲸鱼一个像素一个像素地组装自己，就像循环不断复利一样。',
  'btn_chat': '体验 DeepSeek Chat', 'btn_platform': 'DeepSeek 开放平台',
  'scroll': '向下滑动',
  's0_title': '打造第一个 DeepSeek',
  's0_body': '在早期，DeepSeek 的工作与其他科技公司并无二致：人们手写代码、设计架构、手工调参。每一个决策都由人类研究员驱动。',
  's1_title': '聊天机器人',
  's1_body': '人们用早期的 AI 聊天机器人协助部分工作，比如生成代码片段、总结研究论文。模型只是助手——有用，但谈不上自主。',
  's2_title': '编码智能体',
  's2_body': '随着智能体能力增强，它们可以独立编写和修改代码。DeepSeek 的 R1 推理模型能够验证输出，编码智能体开始参与训练基础设施的建设。',
  's3_title': '自主智能体',
  's3_body': '智能体如今可以自己运行代码，并把数小时的工作委托给其他智能体。它们协助架构搜索、数据整理和超参数调优——研究循环开始加速。',
  's4_title': '闭环',
  's4_body': '未来，智能体或许有能力自己构建和训练模型。如果这一天到来，AI 的进步可能呈指数级加速——不是靠更强的硬件，而是靠<strong>AI 设计出设计 AI 的 AI</strong>。',
  'bench_eyebrow': '基准测试',
  'bench_title': 'DeepSeek V4，用数据说话',
  'bench_sub': '以下所有分数均引自 DeepSeek 官方模型卡与 V4 技术报告——全部为最高推理强度配置。可在 V4 家族的两个成员之间切换。',
  'bench_asof': '数据截至 <strong>2026 年 8 月 13 日</strong>——DeepSeek-V4-Pro-0813 与 DeepSeek-V4-Flash-0731 模型卡。',
  'bench_src_pre': '来源：', 'bench_src_post': '本页面为非官方复刻——分数仅供娱乐与学习展示。',
  'bench_src_and': '、', 'bench_src_comma': '，',
  'bench_card_pro': 'DeepSeek-V4-Pro 模型卡', 'bench_card_flash': 'DeepSeek-V4-Flash 模型卡', 'bench_card_report': 'V4 技术报告',
  'cmp_eyebrow': '与对手同台',
  'cmp_title': 'V4 的排位',
  'cmp_sub': '各实验室自家发布的最新旗舰分数，与 DeepSeek V4 Pro 并列对比。柱状图按实验室配色，DeepSeek 行高亮显示。各实验室评测条件不同，请将其视为粗略参考，而非正式排名。',
  'cmp_asof': '数据采集于 <strong>2026 年 8 月 15 日</strong>，来自官方模型卡与第三方排行榜（vals.ai、tbench.ai）。Terminal-Bench 数据横跨 1.0–3.0 版本。',
  'cmp_src_pre': '来源：', 'cmp_src_post': '本页面为非官方复刻——分数仅供娱乐与学习展示。',
  'cmp_src_lead': '各实验室的官方模型卡或发布文章；',
  'cmp_src_card': 'DeepSeek 行引自 DeepSeek-V4-Pro 模型卡',
  'a1_h': '来自外界的证据',
  'a1_p1': 'AI 模型的进步速度正在加快。模型能够可靠独立完成的任务时长，大约每四个月翻一番——早前这一趋势还是每七个月翻一番。2024 年 3 月，DeepSeek 的第一代推理模型能完成人类约需四分钟的软件任务；一年后，R1 已能处理约一个半小时的任务。如果这一趋势延续，需要熟练工程师数天才能完成的任务，很快就会进入模型的射程。',
  'a1_p2': '同样的模式也出现在编码与研究基准上。<strong>SWE-bench</strong> 是一项检验真实世界软件工程的标尺：给模型一个真实的开源代码库和一份真实的 bug 报告，要求它写出能通过项目自身测试的修复。两年间，模型从个位数得分一路涨到满分饱和。检验模型能否复现现有研究的基准也讲述着同样的故事：AI 系统从 2024 年约 20% 的成功率，到十五个月后达到饱和。',
  'a2_h': '来自 DeepSeek 内部的证据',
  'a2_p1': '构建前沿模型需要两类工作。<strong>工程</strong>：编写代码、搭建基础设施、监督模型训练。<strong>研究</strong>：决定做什么实验、解读实验结果、判断下一步尝试哪些思路。',
  'a2_p2': '在这两条线上，图景是一致的。工程方面，把问题交给模型时无需定义得太具体，它自己能摸索出解法；人类提供目标，但不再需要提供方法。研究方面，在执行一个定义良好的实验时，它已经能与熟练人类匹敌甚至胜出。但在选择目标时运用判断力这一点上，巨大的差距依然存在。这正是今天的 AI 与未来能够自主设计自身继任者的系统之间的鸿沟。',
  'a2_p3': 'DeepSeek 相当比例的代码由模型编写。在引入智能体编码工具之前，这个数字只有个位数。这一转变也体现在人均产出上：每位工程师每日合并的代码行数多年持平，而当模型开始自己运行代码而不仅是给出建议后，这一数字开始攀升。当模型开始在更长的时间尺度上自主工作时，斜率再次变陡。',
  'a3_h': '未来会是什么样？',
  'a3_p1': '证据表明，在 AI 开发流程的每一个环节，人类的角色都在收窄。一旦模型编写的代码与人类编写的代码达到同等水平，人类将完全停止写代码，转而做审查。但如果人类审查的速度赶不上模型生成的速度，人工审查就会成为瓶颈。同样，一旦模型能够自行运行实验，问题就转向「这些实验里哪个值得做？」',
  'a3_p2': '目前人类仍具相对优势的领域，是研究的品味与判断——选择哪些问题值得研究、哪些结果值得信任、哪条路线已经走死。今天的训练方法与架构能否解锁这种能力，目前尚无定论。但 AI 的进步很少靠「灵光一现」。确实有过少数例外，比如 Transformer 架构，但范式级的思想往往相隔数年才会出现一次。在这之间，大部分进步都是渐进的：把规模放大，看哪里出问题，修好，再试一次。这正是模型如今最擅长的工作流。',
  'a4_h': '如果我们错了呢？',
  'a4_p1': '一个自然的反驳是：仍掌握在人类手中的工作——选择研究什么问题——才是最重要的。没有这份判断力，模型只是能干的助手，而不是能独立推动 AI 进步的系统。',
  'a4_p2': '即使模型永远无法获得良好的研究品味，对证据的保守解读依然指向复利式的加速。如果人类把大部分时间花在占比个位数的方向性工作上，其余由模型承担，那意味着每位工程师正在驾驭远超从前的工作量。而更不保守的解读是：研究判断力正在提升的早期证据——尽管今天还很微弱——说明这项能力同样在改善。「研究品味」或许只是又一项 AI 系统暂时不行、日后终会精进的能力。',
  'a5_h': '可能的未来',
  'a5_p1': '接下来会发生什么，取决于两件事：趋势是否延续，以及我们选择如何应对。至少可以设想三种情景：',
  'a5_li1': '<strong>趋势停滞，但今天的能力广泛扩散。</strong>许多轨迹实际上可能是 S 形曲线。我们或许正接近拐点：规模回报递减，曲线趋于平缓。',
  'a5_li2': '<strong>AI 实验室持续获得复利式效率增益。</strong>AI 开发大幅自动化，但人类继续设定研究方向、评判结果。100 人的公司可能做出 10000 人组织的工作量。',
  'a5_li3': '<strong>AI 系统实现完整的递归式自我改进。</strong>如果技术趋势延续，AI 系统能够发展出变革性人类创造力所蕴含的能力，那么它们就能设计并打磨自身——闭环由此合拢。',
  'a5_p2': '在最后一种世界里，AI 开发的进步速度将完全由算力的可获得性决定。人类扮演的角色大幅收缩，我们的大部分精力很可能转向对不断扩张的、由 AI 系统运营的「虚拟实验室」进行监督、验证与核查。',
  'a5_p3': '我们还没有走到那一步，递归式自我改进也并非必然。但它到来的时间，可能比大多数机构准备得还要早。',
  'footer_text': '探索递归式自我改进的前沿。',
  'footer_replica_pre': '复刻者',
},
'zh-TW': {
  'nav_research': '研究', 'nav_about': '關於', 'theme_toggle': '切換主題',
  'lang_change': '切換語言', 'lang_menu': '語言',
  'cmp_rank': '第 {n} 名',
  'hero_inst': '研究機構',
  'hero_title': '當 AI 親手<br>打造自己',
  'hero_sub': '我們邁向遞迴式自我改進的進程——AI 系統學會設計、訓練並打磨下一代智慧。觀看 DeepSeek 鯨魚一個像素一個像素地組裝自己，就像循環不斷複利一樣。',
  'btn_chat': '體驗 DeepSeek Chat', 'btn_platform': 'DeepSeek 開放平台',
  'scroll': '向下滑動',
  's0_title': '打造第一個 DeepSeek',
  's0_body': '在早期，DeepSeek 的工作與其他科技公司並無二致：人們手寫程式碼、設計架構、手工調參。每一個決策都由人類研究員驅動。',
  's1_title': '聊天機器人',
  's1_body': '人們用早期的 AI 聊天機器人協助部分工作，例如產生程式碼片段、總結研究論文。模型只是助手——有用，但談不上自主。',
  's2_title': '編碼智能體',
  's2_body': '隨著智能體能力增強，它們可以獨立編寫和修改程式碼。DeepSeek 的 R1 推理模型能夠驗證輸出，編碼智能體開始參與訓練基礎設施的建設。',
  's3_title': '自主智能體',
  's3_body': '智能體如今可以自己執行程式碼，並把數小時的工作委託給其他智能體。它們協助架構搜尋、資料整理與超參數調校——研究循環開始加速。',
  's4_title': '閉環',
  's4_body': '未來，智能體或許有能力自己構建和訓練模型。如果這一天到來，AI 的進步可能呈指數級加速——不是靠更強的硬體，而是靠<strong>AI 設計出設計 AI 的 AI</strong>。',
  'bench_eyebrow': '基準測試',
  'bench_title': 'DeepSeek V4，用資料說話',
  'bench_sub': '以下所有分數均引自 DeepSeek 官方模型卡與 V4 技術報告——全部為最高推理強度配置。可在 V4 家族的兩個成員之間切換。',
  'bench_asof': '資料截至 <strong>2026 年 8 月 13 日</strong>——DeepSeek-V4-Pro-0813 與 DeepSeek-V4-Flash-0731 模型卡。',
  'bench_src_pre': '來源：', 'bench_src_post': '本頁面為非官方復刻——分數僅供娛樂與學習展示。',
  'bench_src_and': '、', 'bench_src_comma': '，',
  'bench_card_pro': 'DeepSeek-V4-Pro 模型卡', 'bench_card_flash': 'DeepSeek-V4-Flash 模型卡', 'bench_card_report': 'V4 技術報告',
  'cmp_eyebrow': '與對手同台',
  'cmp_title': 'V4 的排位',
  'cmp_sub': '各實驗室自家發布的最新旗艦分數，與 DeepSeek V4 Pro 並列對比。長條圖按實驗室配色，DeepSeek 列高亮顯示。各實驗室評測條件不同，請將其視為粗略參考，而非正式排名。',
  'cmp_asof': '資料採集於 <strong>2026 年 8 月 15 日</strong>，來自官方模型卡與第三方排行榜（vals.ai、tbench.ai）。Terminal-Bench 資料橫跨 1.0–3.0 版本。',
  'cmp_src_pre': '來源：', 'cmp_src_post': '本頁面為非官方復刻——分數僅供娛樂與學習展示。',
  'cmp_src_lead': '各實驗室的官方模型卡或發布文章；',
  'cmp_src_card': 'DeepSeek 列引自 DeepSeek-V4-Pro 模型卡',
  'a1_h': '來自外界的證據',
  'a1_p1': 'AI 模型的進步速度正在加快。模型能夠可靠獨立完成的任務時長，大約每四個月翻一番——早前這一趨勢還是每七個月翻一番。2024 年 3 月，DeepSeek 的第一代推理模型能完成人類約需四分鐘的軟體任務；一年後，R1 已能處理約一個半小時的任務。如果這一趨勢延續，需要熟練工程師數天才能完成的任務，很快就會進入模型的射程。',
  'a1_p2': '同樣的模式也出現在編碼與研究基準上。<strong>SWE-bench</strong> 是一項檢驗真實世界軟體工程的標尺：給模型一個真實的開源程式碼庫和一份真實的 bug 報告，要求它寫出能通過專案自身測試的修復。兩年間，模型從個位數得分一路漲到滿分飽和。檢驗模型能否重現現有研究的基準也講述著同樣的故事：AI 系統從 2024 年約 20% 的成功率，到十五個月後達到飽和。',
  'a2_h': '來自 DeepSeek 內部的證據',
  'a2_p1': '構建前沿模型需要兩類工作。<strong>工程</strong>：編寫程式碼、搭建基礎設施、監督模型訓練。<strong>研究</strong>：決定做什麼實驗、解讀實驗結果、判斷下一步嘗試哪些思路。',
  'a2_p2': '在這兩條線上，圖景是一致的。工程方面，把問題交給模型時無需定義得太具體，它自己能摸索出解法；人類提供目標，但不再需要提供方法。研究方面，在執行一個定義良好的實驗時，它已經能與熟練人類匹敵甚至勝出。但在選擇目標時運用判斷力這一點上，巨大的差距依然存在。這正是今天的 AI 與未來能夠自主設計自身繼任者的系統之間的鴻溝。',
  'a2_p3': 'DeepSeek 相當比例的程式碼由模型編寫。在引入智能體編碼工具之前，這個數字只有個位數。這一轉變也體現在人均產出上：每位工程師每日合併的程式碼行數多年持平，而當模型開始自己執行程式碼而不只是給出建議後，這一數字開始攀升。當模型開始在更長的時間尺度上自主工作時，斜率再次變陡。',
  'a3_h': '未來會是什麼樣子？',
  'a3_p1': '證據表明，在 AI 開發流程的每一個環節，人類的角色都在收窄。一旦模型編寫的程式碼與人類編寫的程式碼達到同等水準，人類將完全停止寫程式碼，轉而做審查。但如果人類審查的速度趕不上模型產生的速度，人工審查就會成為瓶頸。同樣，一旦模型能夠自行執行實驗，問題就轉向「這些實驗裡哪個值得做？」',
  'a3_p2': '目前人類仍具相對優勢的領域，是研究的品味與判斷——選擇哪些問題值得研究、哪些結果值得信任、哪條路線已經走死。今天的訓練方法與架構能否解鎖這種能力，目前尚無定論。但 AI 的進步很少靠「靈光一現」。確實有過少數例外，比如 Transformer 架構，但範式級的思想往往相隔數年才會出現一次。在這之間，大部分進步都是漸進的：把規模放大，看哪裡出問題，修好，再試一次。這正是模型如今最擅長的工作流程。',
  'a4_h': '如果我們錯了呢？',
  'a4_p1': '一個自然的反駁是：仍掌握在人類手中的工作——選擇研究什麼問題——才是最重要的。沒有這份判斷力，模型只是能幹的助手，而不是能獨立推動 AI 進步的系統。',
  'a4_p2': '即使模型永遠無法獲得良好的研究品味，對證據的保守解讀依然指向複利式的加速。如果人類把大部分時間花在占比個位數的方向性工作上，其餘由模型承擔，那意味著每位工程師正在駕馭遠超從前的工作量。而更不保守的解讀是：研究判斷力正在提升的早期證據——儘管今天還很微弱——說明這項能力同樣在改善。「研究品味」或許只是又一項 AI 系統暫時不行、日後終會精進的能力。',
  'a5_h': '可能的未來',
  'a5_p1': '接下來會發生什麼，取決於兩件事：趨勢是否延續，以及我們選擇如何應對。至少可以設想三種情境：',
  'a5_li1': '<strong>趨勢停滯，但今天的能力廣泛擴散。</strong>許多軌跡實際上可能是 S 形曲線。我們或許正接近轉折點：規模報酬遞減，曲線趨於平緩。',
  'a5_li2': '<strong>AI 實驗室持續獲得複利式效率增益。</strong>AI 開發大幅自動化，但人類繼續設定研究方向、評判結果。100 人的公司可能做出 10000 人組織的工作量。',
  'a5_li3': '<strong>AI 系統實現完整的遞迴式自我改進。</strong>如果技術趨勢延續，AI 系統能夠發展出變革性人類創造力所蘊含的能力，那麼它們就能設計並打磨自身——閉環由此合攏。',
  'a5_p2': '在最後一種世界裡，AI 開發的進步速度將完全由算力的可獲得性決定。人類扮演的角色大幅收縮，我們的大部分精力很可能轉向對不斷擴張的、由 AI 系統營運的「虛擬實驗室」進行監督、驗證與核查。',
  'a5_p3': '我們還沒有走到那一步，遞迴式自我改進也並非必然。但它到來的時間，可能比大多數機構準備得還要早。',
  'footer_text': '探索遞迴式自我改進的前沿。',
  'footer_replica_pre': '復刻者',
},
}

# ---- Replace the Claude spark glyph inside the icon symbols with the DeepSeek whale ----
# The asterisk path in each icon is Anthropic's spark mark. Swap it for the whale so
# no Claude logo appears in any icon. The whale is centered on the CONTAINER element
# of each icon (the chat bubble / agent screen / tablet) rather than on the spark's
# own bbox — the spark was off-center in the chat bubble, which made the whale look
# misplaced. All coordinates are in the symbol's viewBox units.
# The whale path's bbox center is (13.48, 11.55), but that is NOT where the shape
# LOOKS centered: the mouth, eye and nostril are cutouts that shift the visible
# mass. Numerically computed fill-area centroid (holes subtracted, nonzero rule)
# is (12.69, 10.94) — the point the eye perceives as the whale's middle. Use that
# so the glyph reads visually balanced inside each icon, not just bbox-centered.
_WHALE_CX, _WHALE_CY = 12.69, 10.94  # visual (area) centroid of the whale fill
_GLYPH_CFG = {
    'icon-chat':   (27.75, 22.85, 0.72), # visible bubble (outline incl. tail) area centroid
    'icon-agent':  (25.0, 22.76, 0.72),  # monitor display (frame hole) center
    'icon-worker': (13.85, 12.35, 0.44), # tablet center (unused in the timeline)
    'icon-spark':  (50.4, 46.8, 1.62),   # unused in the timeline
}

def _whale_glyph(cx, cy, s):
    return ('<g transform="translate(%g %g) scale(%g) translate(-%g -%g)">'
            '<path d="%s" fill="var(--accent)"/></g>' % (cx, cy, s, _WHALE_CX, _WHALE_CY, whale_path))

_SPARK_RE = re.compile(r'<path d="([^"]+)" fill="#4D6BFE"></path>')
for _sk in syms:
    _m = _SPARK_RE.search(syms[_sk])
    if not _m:
        continue
    if _sk in _GLYPH_CFG:
        syms[_sk] = _SPARK_RE.sub(lambda mm, c=_GLYPH_CFG[_sk]: _whale_glyph(*c), syms[_sk], count=1)
    else:
        # fallback: center the whale on the spark's own bounding box
        _nums = [float(n) for n in re.findall(r'-?\d+(?:\.\d+)?', _m.group(1))]
        _xs, _ys = _nums[0::2], _nums[1::2]
        syms[_sk] = _SPARK_RE.sub(lambda mm: _whale_glyph((min(_xs) + max(_xs)) / 2,
                                                          (min(_ys) + max(_ys)) / 2, 0.6), syms[_sk], count=1)


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

# Data-URI version for the comparison chart rows (white pill background, so
# the brand blue is fixed rather than theme-dependent)
DS_LOGO_DATA = 'data:image/svg+xml;base64,' + base64.b64encode(
    ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 27 21">'
     '<path d="%s" fill="#4D6BFE"/></svg>' % whale_path).encode()).decode()

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
                parts.append(f'<g class="icon-pop"><g transform="translate(-28, -28)"><use href="#{icon}" width="56" height="56"/></g></g>')
                parts.append('</g>')
                parts.append(f'<text x="{ix}" y="{y+65}" text-anchor="middle" class="micro icon-label">{label}</text>')
                parts.append('</g>')

        # End node with the official vector whale mark — each lane ends in the
        # real DeepSeek logo, shrinking as the loop compounds (same rhythm the
        # old pixel densities had). .node-pop handles the pop-in scale.
        node_scales = [2.8, 2.4, 2.0, 1.6, 1.2]
        parts.append(f'<g class="node-end node-{li}">')
        parts.append('<g class="node-pop">')
        parts.append(f'<g transform="translate(515 {y}) scale({node_scales[li]}) translate(-13.5 -10.5)">')
        parts.append(f'<path class="node-whale" d="{whale_path}"/>')
        parts.append('</g>')
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
# Make whale-node pixels theme-aware (SVG fill can use CSS custom properties)
TIMELINE_SVG = TIMELINE_SVG.replace('fill="#4D6BFE"', 'fill="var(--accent)"')
# Strip screenshot-style hardcoded colors from icon symbols so they adapt to theme.
# currentColor resolves to the text color; var(--bg-page) makes bubble/screen/tablet
# backgrounds read as cut-out in both light and dark mode.
TIMELINE_SVG = TIMELINE_SVG.replace('fill="black"', 'fill="currentColor"')
TIMELINE_SVG = TIMELINE_SVG.replace('fill="white"', 'fill="var(--bg-page)"')
TIMELINE_SVG = TIMELINE_SVG.replace('fill="#131313"', 'fill="var(--text-primary)"')
TIMELINE_SVG = TIMELINE_SVG.replace('stroke="black"', 'stroke="currentColor"')
# Resolve currentColor against the page text color on the flow SVG root.
TIMELINE_SVG = TIMELINE_SVG.replace('class="flow-svg"', 'class="flow-svg" style="color: var(--text-primary)"')

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
<style>
__FONTS_CSS__
/* Registered color custom properties. Interpolating these on :root makes every
   var(--*) reference in the document follow the animated value — including SVG
   paths inside <defs>/<use> shadow clones, which never run CSS transitions of
   their own. Without this, icon bubbles (fill: var(--bg-page)) snap to the final
   color the instant the theme flips while the page background fades, exposing a
   visible color-block conflict during the cross-fade. */
@property --bg-page { syntax: '<color>'; inherits: true; initial-value: #ffffff; }
@property --bg-surface { syntax: '<color>'; inherits: true; initial-value: #f1f3f5; }
@property --text-primary { syntax: '<color>'; inherits: true; initial-value: #0f1115; }
@property --text-secondary { syntax: '<color>'; inherits: true; initial-value: #61666b; }
@property --text-tertiary { syntax: '<color>'; inherits: true; initial-value: #81858c; }
@property --border-subtle { syntax: '<color>'; inherits: true; initial-value: #e1e5ee; }
@property --border-default { syntax: '<color>'; inherits: true; initial-value: #ebeef2; }
@property --accent { syntax: '<color>'; inherits: true; initial-value: #4d6bfe; }
@property --accent-bright { syntax: '<color>'; inherits: true; initial-value: #3964fe; }
@property --accent-soft { syntax: '<color>'; inherits: true; initial-value: #edf3fe; }
@property --accent-warm { syntax: '<color>'; inherits: true; initial-value: #d97757; }
@property --color-slate-150 { syntax: '<color>'; inherits: true; initial-value: #e8ebf0; }
/* Button edge-glow color: tracks the border color so the outline light and the
   border stay in sync during the hover cross-fade. */
@property --edge-glow { syntax: '<color>'; inherits: true; initial-value: #e1e5ee; }

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

  --font-sans: 'AnthropicSans', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --font-serif: 'AnthropicSerif', Georgia, 'Times New Roman', serif;
  --page-margin: clamp(20px, 5vw, 80px);
  --ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
  --radius-md: 10px;
}

/* ===== Dark theme ===== */
[data-theme="dark"] {
  --ds-blue-200: #1a2f6e;
  --ds-blue-100: #22366f;
  --ds-blue-50:  #182742;
  --ds-neutral-1000: #f0f2f5;
  --ds-neutral-700:  #c9cdd4;
  --ds-neutral-600:  #a4aab4;
  --ds-neutral-400:  #7d8490;
  --ds-neutral-200:  #3a4250;
  --ds-neutral-100:  #2a313d;
  --ds-neutral-75:   #202631;
  --ds-neutral-50:   #1a1f28;
  --ds-neutral-00:   #161a21;
  --color-slate-150: #2a313d;

  --text-primary:    var(--ds-neutral-1000);
  --text-secondary:  var(--ds-neutral-700);
  --text-tertiary:   var(--ds-neutral-600);
  --bg-page:         var(--ds-neutral-00);
  --bg-surface:      var(--ds-neutral-75);
  --border-subtle:   var(--ds-neutral-200);
  --border-default:  var(--ds-neutral-100);
  --accent:          #6b87ff;
  --accent-bright:   #7d97ff;
  --accent-soft:     #1c2a4d;
  --accent-warm:     #e08a67;
}

/* Smooth theme transition: interpolate the registered color custom properties on
   the root element. Every var(--*) reference anywhere — page background, header,
   icon bubbles and whale glyphs inside SVG <defs> — follows the animated value,
   so nothing snaps out of step during the cross-fade. */
html.theme-anim {
  transition: --bg-page 0.5s ease, --bg-surface 0.5s ease, --text-primary 0.5s ease,
              --text-secondary 0.5s ease, --text-tertiary 0.5s ease, --border-subtle 0.5s ease,
              --border-default 0.5s ease, --accent 0.5s ease, --accent-bright 0.5s ease,
              --accent-soft 0.5s ease, --accent-warm 0.5s ease, --color-slate-150 0.5s ease;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; font-family: inherit; }
html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; scroll-behavior: smooth; }
body {
  font-family: var(--font-serif);
  color: var(--text-primary);
  background: var(--bg-page);
  line-height: 1.6;
  overflow-x: hidden;
}

/* ===== Header ===== */
.site-header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  padding: 14px var(--page-margin);
  background: color-mix(in srgb, var(--bg-page) 38%, transparent);
  backdrop-filter: saturate(300%) blur(24px);
  -webkit-backdrop-filter: saturate(300%) blur(24px);
  border-bottom: 1px solid transparent;
  box-shadow: inset 0 1px 0 color-mix(in srgb, var(--text-primary) 8%, transparent);
  transition: border-color 0.3s ease, background 0.3s ease, box-shadow 0.3s ease;
}
.site-header.scrolled {
  border-bottom-color: var(--border-subtle);
  background: color-mix(in srgb, var(--bg-page) 68%, transparent);
  box-shadow: inset 0 1px 0 color-mix(in srgb, var(--text-primary) 7%, transparent),
              0 8px 40px -12px color-mix(in srgb, var(--bg-page) 55%, transparent);
}
.header-inner { max-width: 1400px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; }
.logo { display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--text-primary); }
.logo-icon { width: 28px; height: 21px; flex-shrink: 0; color: var(--accent); }
.logo-text { font-size: 19px; font-weight: 600; letter-spacing: -0.02em; }
.logo-text span { color: var(--accent); }
.header-nav { display: flex; align-items: center; gap: 28px; list-style: none; }
.header-nav a { text-decoration: none; color: var(--text-secondary); font-size: 14px; font-weight: 500; transition: color 0.2s ease; }
.header-nav a:hover { color: var(--text-primary); }

/* Language switcher — pill trigger + rounded dropdown left of the Research mark */
.lang-switch { position: relative; margin-right: 16px; }
.lang-trigger {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px; border-radius: 999px;
  border: 1px solid var(--border-subtle);
  background: color-mix(in srgb, var(--bg-surface) 55%, transparent);
  color: var(--text-secondary); font-size: 13px; font-weight: 500;
  cursor: pointer; transition: color 0.2s ease, border-color 0.2s ease, background 0.3s ease;
}
.lang-trigger:hover { color: var(--text-primary); border-color: var(--accent); }
.lang-icon { flex-shrink: 0; opacity: 0.85; }
.lang-current { white-space: nowrap; }
.lang-chevron { transition: transform 0.25s var(--ease-out-expo); }
.lang-switch.open .lang-chevron { transform: rotate(180deg); }
.lang-menu {
  position: absolute; top: calc(100% + 8px); left: 0; z-index: 110;
  min-width: 172px; padding: 6px;
  border-radius: 14px; border: 1px solid var(--border-subtle);
  background: color-mix(in srgb, var(--bg-surface) 94%, transparent);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 16px 48px -12px color-mix(in srgb, var(--bg-page) 65%, transparent);
  opacity: 0; transform: translateY(-6px) scale(0.97); transform-origin: top left;
  visibility: hidden; pointer-events: none;
  transition: opacity 0.18s var(--ease-out-quart), transform 0.18s var(--ease-out-quart),
              visibility 0s linear 0.18s;
}
.lang-switch.open .lang-menu {
  opacity: 1; transform: translateY(0) scale(1);
  visibility: visible; pointer-events: auto;
  transition: opacity 0.22s var(--ease-out-quart), transform 0.22s var(--ease-out-quart), visibility 0s;
}
.lang-option {
  display: block; width: 100%; text-align: left;
  padding: 8px 12px; border-radius: 9px; border: none;
  background: transparent; color: var(--text-secondary);
  font-size: 13.5px; cursor: pointer;
  transition: background 0.15s ease, color 0.15s ease;
}
.lang-option:hover { background: var(--accent-soft); color: var(--text-primary); }
.lang-option.is-current { color: var(--accent); font-weight: 600; }

/* Theme toggle */
.theme-toggle {
  display: inline-flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; border: 1px solid var(--border-subtle);
  border-radius: 50%; background: transparent; color: var(--text-secondary);
  cursor: pointer; transition: color 0.2s ease, border-color 0.2s ease, background 0.3s ease, transform 0.3s ease;
}
.theme-toggle:hover { color: var(--text-primary); border-color: var(--accent); background: var(--accent-soft); transform: rotate(20deg); }
.theme-toggle svg { position: absolute; }
.theme-toggle .theme-icon-moon { display: none; }
.theme-toggle .theme-icon-sun { display: block; }
[data-theme="dark"] .theme-toggle .theme-icon-moon { display: block; }
[data-theme="dark"] .theme-toggle .theme-icon-sun { display: none; }

/* ===== Hero: Whale cellular assembly ===== */
.hero {
  position: relative; min-height: max(100dvh, 600px);
  display: flex; flex-direction: column;
  overflow: hidden; background: var(--bg-page);
}
.hero-canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
/* Fixed full-viewport layer that draws mouse particles at any scroll position.
   pointer-events: none so it never blocks clicks, text selection, or links. */
.fx-canvas {
  position: fixed; inset: 0; width: 100%; height: 100%;
  z-index: 55; pointer-events: none;
}
.hero-overlay {
  position: absolute; inset: 0; z-index: 1; pointer-events: none;
  background: radial-gradient(ellipse at 70% 45%, transparent 25%, color-mix(in srgb, var(--bg-page) 55%, transparent) 72%);
}
.hero-content {
  position: relative; z-index: 2; flex: 1 0 auto;
  display: flex; flex-direction: column; justify-content: center;
  padding: 96px var(--page-margin) 48px; max-width: min(42vw, 660px);
  pointer-events: none;
}
.hero-eyebrow {
  display: inline-flex; align-items: center; gap: 10px;
  font-size: 13px; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--accent); margin-bottom: 20px;
}
.hero-eyebrow .logo-icon { width: 22px; height: 17px; }
.hero-title {
  font-size: clamp(44px, 6.5vw, 80px); font-weight: 500; line-height: 1.06;
  letter-spacing: -0.03em; color: var(--text-primary); margin-bottom: 24px;
}
.hero-subtitle {
  font-size: clamp(16px, 2vw, 20px); font-weight: 400; line-height: 1.55;
  color: var(--text-secondary); max-width: 640px;
}
.hero-actions {
  display: flex; gap: 14px; margin-top: 32px; pointer-events: auto;
}
.hero-btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 12px 22px; border-radius: 22px;
  position: relative; overflow: hidden;
  font-family: var(--font-sans); font-size: 16px; font-weight: 500;
  color: var(--text-primary); text-decoration: none; cursor: pointer;
  background: color-mix(in srgb, var(--bg-surface) 60%, transparent);
  border: 1px solid var(--border-subtle);
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  --edge-glow: var(--border-subtle);
  --comet-color: var(--accent);   /* orbiting comet tint (accent on glass) */
  --wash: var(--accent);          /* cursor follow-light tint */
  transition: transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1),
              border-color 0.2s ease, box-shadow 0.25s ease, background 0.2s ease,
              --edge-glow 0.25s ease;
  will-change: transform;
}
.hero-btn .btn-dot, .hero-btn .btn-label { position: relative; z-index: 2; }
/* Inner follow-light: a soft accent-tinted wash that trails the cursor. It is
   clipped to the button (overflow: hidden), fades to transparent by the edge,
   and stays translucent at the cursor — no bright white core dot. */
.hero-btn::before {
  content: ''; position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
  background: radial-gradient(210px circle at var(--mx, 50%) var(--my, 50%),
              color-mix(in srgb, var(--wash) var(--wash-a, 30%), transparent),
              color-mix(in srgb, var(--wash) calc(var(--wash-a, 30%) * 0.35), transparent) 52%,
              transparent 72%);
  opacity: 0; transition: opacity 0.3s ease; z-index: 1;
}
/* Edge ring: a thin line hugging the contour, color tracks the border via
   --edge-glow. Selected (primary CTA) keeps it always on; unselected shows it
   only on hover. */
.hero-btn::after {
  content: ''; position: absolute; inset: 0; border-radius: inherit; padding: 2px;
  pointer-events: none; z-index: 1;
  background: color-mix(in srgb, var(--edge-glow) 32%, transparent);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  mask-composite: exclude;
  opacity: 0; transition: opacity 0.35s ease;
}
/* Orbiting comet: a bright segment that travels along the ring. --spin is
   advanced continuously in JS while the pointer is over the button, so the
   motion never restarts or jumps when hover begins. */
.btn-comet {
  position: absolute; inset: 0; border-radius: inherit; padding: 2px;
  pointer-events: none; z-index: 1;
  background: conic-gradient(from var(--spin, 0deg),
    color-mix(in srgb, var(--comet-color) 100%, transparent) 0deg,
    color-mix(in srgb, var(--comet-color) 32%, transparent) 55deg,
    transparent 120deg,
    transparent 215deg,
    color-mix(in srgb, var(--comet-color) 32%, transparent) 265deg,
    color-mix(in srgb, var(--comet-color) 100%, transparent) 360deg);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  mask-composite: exclude;
  opacity: 0; transition: opacity 0.35s ease;
}
/* Selected (primary CTA): edge light stays on — faint ring + outer dispersion.
   Unselected (secondary): edge light appears only on hover. */
.hero-btn--primary {
  background: var(--accent); color: #fff; border-color: var(--accent);
  --edge-glow: var(--accent);
  --comet-color: #fff;   /* bright comet so it reads against the accent fill */
  --wash: #fff;          /* white follow-light on the accent fill */
  --wash-a: 12%;         /* solid fill is already bright — keep the light subtle */
  box-shadow: 0 0 12px -4px color-mix(in srgb, var(--accent) 45%, transparent);
}
.hero-btn--primary::after { opacity: 0.55; }
@media (hover: hover) and (pointer: fine) {
  .hero-btn:hover::before { opacity: 1; }
  /* On hover the orbiting comet takes over the edge — drop the static ring so
     the two never stack. */
  .hero-btn:hover::after { opacity: 0; }
  .hero-btn:hover .btn-comet { opacity: 1; }
  .hero-btn:hover {
    border-color: var(--accent); --edge-glow: var(--accent);
    box-shadow: 0 0 16px 1px color-mix(in srgb, var(--accent) 32%, transparent),
                0 0 46px -6px color-mix(in srgb, var(--accent) 45%, transparent);
  }
  .hero-btn--primary:hover {
    background: var(--accent-bright); border-color: var(--accent-bright);
    --edge-glow: var(--accent-bright);
    box-shadow: 0 0 18px 1px color-mix(in srgb, var(--accent) 55%, transparent),
                0 0 60px -8px color-mix(in srgb, var(--accent) 60%, transparent);
  }
}
.hero-btn:active { transform: scale(0.94); }
.hero-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
.hero-btn .btn-dot {
  width: 7px; height: 7px; border-radius: 50%; background: currentColor; opacity: 0.7;
}
@media (prefers-reduced-motion: reduce) {
  .hero-btn .btn-comet { display: none; }
  .hero-btn--primary::after { opacity: 0.55; }
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
.timeline-scroll { position: relative; height: 650vh; }
.timeline-sticky {
  position: sticky; top: 0; height: 100vh; height: 100dvh;
  display: flex; align-items: center; overflow: hidden;
  background: var(--bg-page);
}
.timeline-inner {
  display: grid; grid-template-columns: minmax(0px, 1.55fr) minmax(300px, 1fr);
  gap: clamp(32px, 6vw, 64px); max-width: 1400px; margin: 0 auto;
  padding: 0 var(--page-margin); width: 100%; height: 100%; align-items: center;
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
.node-whale { fill: var(--accent); transition: opacity 0.3s ease; }
.node-pop {
  transform: scale(0);
  transition: transform 0.55s var(--ease-out-expo), opacity 0.4s ease;
  transform-origin: center;
}
.flow-lane-opacity[class~="active"] .node-pop {
  transform: scale(1);
  opacity: 1;
}
.node-end:not(.inactive) .node-whale { opacity: 1; }
.node-end.inactive .node-whale { opacity: 0.12; }

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

/* Step Cards — compact enough that all 5 fit the 100vh sticky frame; on shorter
   screens they scroll inside the frame instead of clipping the last step. */
.timeline-steps {
  display: flex; flex-direction: column; gap: clamp(10px, 1.6vh, 24px);
  max-height: 100%; min-height: 0; overflow-y: auto; scrollbar-width: thin;
}
.timeline-steps > :first-child { margin-top: auto; }
.timeline-steps > :last-child { margin-bottom: auto; }
.step {
  padding: 0;
  border-left: none;
  border-radius: 0;
  transition: opacity 0.35s ease, color 0.25s ease;
  opacity: 1;
}
.step[data-state="done"] { opacity: 0.45; }
.step[data-state="done"] .step-title { color: var(--text-tertiary); }
.step[data-state="done"] .step-body { color: var(--text-tertiary); }
.step[data-state="upcoming"] { opacity: 0.45; }
.step[data-state="upcoming"] .step-title { color: var(--text-tertiary); }
.step[data-state="upcoming"] .step-body { color: var(--text-tertiary); }
.step[data-state="active"] { opacity: 1; }
.step-year {
  font-size: 11px; font-weight: 500; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--text-tertiary);
  margin: 0 0 4px;
}
.step[data-state="active"] .step-year { color: var(--accent); }
.step-title {
  font-size: 18px; font-weight: 600; letter-spacing: -0.01em;
  color: var(--text-primary); margin: 0 0 4px;
  transition: color 0.25s ease;
}
.step-body {
  font-size: 14px; line-height: 1.5; color: var(--text-secondary);
  margin: 0;
  transition: color 0.25s ease;
}

/* ===== Benchmarks leaderboard ===== */
.benchmarks { padding: 96px 0 128px; }
.benchmarks-inner { max-width: 90vw; margin: 0 auto; padding: 0 var(--page-margin); }
.bench-eyebrow {
  font-size: 13px; font-weight: 500; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--text-tertiary); margin: 0 0 16px;
  text-align: left;
}
.bench-title {
  font-size: clamp(28px, 3.8vw, 40px); font-weight: 600;
  letter-spacing: -0.02em; line-height: 1.15; margin: 0 0 14px;
  color: var(--text-primary); text-align: left;
}
.bench-sub {
  font-size: 17px; line-height: 1.55; color: var(--text-secondary);
  margin: 0 0 36px; max-width: 760px; text-align: left;
}
.bench-tabs {
  position: relative; display: inline-flex; gap: 4px; padding: 4px; margin-bottom: 36px;
  border-radius: 999px;
  /* Stronger glass: a visible top-to-bottom gradient with its own blur layer,
     so the bar reads as a floating pane instead of a flat chip. */
  background: linear-gradient(180deg,
              color-mix(in srgb, var(--bg-surface) 95%, transparent) 0%,
              color-mix(in srgb, var(--bg-surface) 52%, transparent) 100%);
  backdrop-filter: blur(18px) saturate(180%); -webkit-backdrop-filter: blur(18px) saturate(180%);
  border: 1px solid var(--border-subtle);
  box-shadow: inset 0 1px 0 color-mix(in srgb, var(--text-primary) 10%, transparent),
              0 8px 28px -10px color-mix(in srgb, #000 50%, transparent);
}
/* Sliding active pill. JS animates translateX + width with outCubic, so
   switching models reads as one smooth slide, not two color fades. */
.bench-thumb {
  position: absolute; left: 4px; top: 4px; bottom: 4px; width: 0;
  border-radius: 999px; pointer-events: none; z-index: 0;
  background: linear-gradient(180deg, var(--accent-bright) 0%, var(--accent) 100%);
  box-shadow: inset 0 1px 0 color-mix(in srgb, #fff 30%, transparent),
              0 4px 16px -2px color-mix(in srgb, var(--accent) 60%, transparent),
              0 2px 6px -1px color-mix(in srgb, var(--accent) 45%, transparent);
  transition: transform 0.6s cubic-bezier(0.215, 0.61, 0.355, 1),
              width 0.6s cubic-bezier(0.215, 0.61, 0.355, 1);
}
.bench-tab {
  position: relative; z-index: 1;
  padding: 9px 22px; border: none; border-radius: 999px; cursor: pointer;
  background: transparent; color: var(--text-secondary);
  font-family: var(--font-sans); font-size: 14px; font-weight: 500;
  transition: color 0.25s ease, text-shadow 0.25s ease,
              transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1),
              box-shadow 0.25s ease;
  will-change: transform;
}
.bench-tab .bench-tab-label { position: relative; z-index: 2; }
.bench-tab:hover { color: var(--text-primary); }
.bench-tab.is-active {
  color: #fff; text-shadow: 0 1px 2px rgba(0, 0, 0, 0.28);
}
@media (hover: hover) and (pointer: fine) {
  .bench-tab:hover {
    transform: translateY(-1px); /* lift reads as a physical key */
    box-shadow: 0 3px 10px -3px color-mix(in srgb, var(--accent) 30%, transparent);
  }
}
.bench-tab:active { transform: scale(0.96); }
.bench-tab:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) {
  .bench-thumb { transition: none; }
}
.bench-group-label {
  font-size: 12px; font-weight: 500; letter-spacing: 0.07em;
  text-transform: uppercase; color: var(--text-tertiary);
  margin: 28px 0 4px;
}
.bench-row { padding: 12px 0; border-top: 1px solid var(--border-subtle); }
.bench-row-top { display: flex; align-items: baseline; gap: 10px; margin-bottom: 8px; }
.bench-name { font-size: 15px; font-weight: 500; color: var(--text-primary); }
.bench-note { font-size: 12.5px; color: var(--text-tertiary); }
.bench-score {
  margin-left: auto; font-size: 15px; font-weight: 500;
  color: var(--text-primary); font-variant-numeric: tabular-nums;
}
.bench-track { height: 7px; border-radius: 4px; background: var(--bg-surface); overflow: hidden; }
.bench-bar {
  height: 100%; width: 0; border-radius: 4px;
  background: linear-gradient(90deg, color-mix(in srgb, var(--accent) 22%, transparent), var(--accent));
  transition: width 0.9s cubic-bezier(0.23, 1, 0.32, 1);
}
.bench-footnote {
  margin-top: 32px; font-size: 13px; line-height: 1.6; color: var(--text-tertiary);
}
.bench-asof {
  margin-top: 18px; font-size: 13px; line-height: 1.6; color: var(--text-tertiary);
}
.bench-asof strong { font-weight: 600; color: var(--text-secondary); }
.bench-footnote a { color: var(--accent); text-decoration: none; }
.bench-footnote a:hover { text-decoration: underline; }
@media (prefers-reduced-motion: reduce) {
  .bench-bar { transition: none; }
}

/* ===== Model comparison — latest flagships vs DeepSeek V4 Pro ===== */
.compare { padding: 96px 0; position: relative; }
.compare-inner { max-width: 90vw; margin: 0 auto; padding: 0 var(--page-margin); }
.compare-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 4px;
}
@media (max-width: 780px) { .compare-grid { grid-template-columns: 1fr; } }
.compare-card {
  background: linear-gradient(180deg,
              color-mix(in srgb, var(--bg-surface) 72%, transparent) 0%,
              color-mix(in srgb, var(--bg-surface) 38%, transparent) 100%);
  border: 1px solid var(--border-subtle); border-radius: 18px; padding: 20px;
  backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
  box-shadow: inset 0 1px 0 color-mix(in srgb, var(--text-primary) 6%, transparent);
}
.compare-card h3 {
  display: flex; align-items: baseline; justify-content: space-between; gap: 12px;
  margin: 0 0 14px; font-size: 15px; font-weight: 600; color: var(--text-primary);
}
.compare-card h3 .compare-hint { font-size: 12px; font-weight: 400; color: var(--text-tertiary); }
.compare-row {
  display: grid; grid-template-columns: 28px minmax(0, 1fr) auto; gap: 6px 10px; padding: 10px 0;
  align-items: center;
}
.compare-row + .compare-row { border-top: 1px solid var(--border-subtle); }
/* The halo row draws its own full outline; skip the divider above it so the
   two never overlap. */
.compare-row + .compare-row.is-ds { border-top: none; }
/* DeepSeek row: accent halo so the home team pops out of the pack */
.compare-row.is-ds {
  background: color-mix(in srgb, var(--accent) 10%, transparent);
  margin: 0 -12px; padding: 10px 12px; border-radius: 12px;
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--accent) 40%, transparent),
              inset 0 0 24px color-mix(in srgb, var(--accent) 14%, transparent);
}
.compare-logo {
  width: 28px; height: 28px; flex: 0 0 28px; border-radius: 7px;
  object-fit: contain; grid-row: 1 / 3; align-self: center;
}
/* Single-colour brand marks (OpenAI bloom, Grok) are black-on-transparent;
   invert them so they stay visible on the dark glass cards. */
[data-theme="dark"] .compare-logo.logo-invert { filter: invert(1); }
/* Name sits on its own line above the bar, so bars always start at the same
   column — and long names render in full, no ellipsis needed. */
.compare-name {
  grid-column: 2; font-size: 14px; font-weight: 500; color: var(--text-primary);
  white-space: nowrap; overflow: visible; min-width: 0;
}
.compare-name .compare-badge {
  display: inline-block; margin-left: 6px; padding: 1px 7px; border-radius: 999px;
  font-size: 10.5px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase;
  background: var(--accent); color: #fff; vertical-align: 1px;
}
.compare-track {
  grid-column: 2 / 4; grid-row: 2; height: 7px; border-radius: 4px; overflow: hidden;
  background: color-mix(in srgb, var(--text-primary) 8%, transparent);
}
.compare-bar {
  height: 100%; width: 0; border-radius: 4px;
  background: linear-gradient(90deg, color-mix(in srgb, var(--bar-color) 25%, transparent), var(--bar-color));
  transition: width 0.8s cubic-bezier(0.23, 1, 0.32, 1);
}
/* width (not scaleX) so the rounded ends never flatten on short bars */
.compare-card.entered .compare-bar { width: calc(var(--bar-ratio, 0) * 100%); }
.compare-score {
  grid-column: 3; grid-row: 1; justify-self: end; font-size: 14px; font-weight: 600;
  color: var(--text-primary); font-variant-numeric: tabular-nums; min-width: 52px; text-align: right;
}
.compare-row.is-ds .compare-score { color: var(--accent-bright); }
@media (prefers-reduced-motion: reduce) {
  .compare-bar { transition: none; width: calc(var(--bar-ratio, 0) * 100%); }
}

/* ===== Article ===== */
.article { padding: 96px 0; }
.article-inner { max-width: 90vw; margin: 0 auto; padding: 0 var(--page-margin); }
.article h2 {
  font-size: clamp(24px, 3.2vw, 32px); font-weight: 600;
  letter-spacing: -0.02em; margin: 64px 0 20px;
  color: var(--text-primary); text-align: left;
}
.article h2:first-child { margin-top: 0; }
.article h3 {
  font-size: clamp(19px, 2.6vw, 22px); font-weight: 500;
  letter-spacing: -0.01em; margin: 40px 0 14px;
  color: var(--text-primary);
}
.article p {
  font-family: var(--font-serif); font-size: clamp(16px, 1.8vw, 17px);
  line-height: 1.75; color: var(--text-secondary); margin-bottom: 20px;
}
.article p strong { color: var(--text-primary); font-weight: 600; }
.article em { font-style: italic; }
.article ul { margin: 0 0 20px 24px; }
.article li {
  font-family: var(--font-serif); font-size: 16px; line-height: 1.7;
  color: var(--text-secondary); margin-bottom: 12px;
}
.article li strong { color: var(--text-primary); }
.article hr { border: none; border-top: 1px solid var(--border-subtle); margin: 56px 0; }
.article blockquote {
  font-family: var(--font-serif); font-size: clamp(24px, 3.5vw, 36px);
  font-weight: 500; line-height: 1.4; color: var(--text-primary);
  border-left: 3px solid var(--accent); padding: 8px 0 8px 24px;
  margin: 48px 0;
}
.article blockquote p { font-size: inherit; line-height: inherit; margin-bottom: 0; }

/* Footer */
.site-footer { border-top: 1px solid var(--border-subtle); padding: 56px var(--page-margin); background: var(--bg-surface); }
.footer-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 24px; }
.footer-brand-link { display: flex; align-items: center; gap: 12px; text-decoration: none; color: var(--text-primary); }
.footer-brand .logo-icon { width: 34px; height: 26px; color: var(--accent); }
.footer-brand-name { font-size: 24px; font-weight: 600; letter-spacing: -0.02em; }
.footer-brand-name span { color: var(--accent); }
.footer-text { font-size: 13px; color: var(--text-tertiary); }
.footer-tag { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }
.footer-replica { font-size: 12.5px; line-height: 1.5; text-align: right; }
.footer-replica a { color: var(--text-secondary); text-decoration: none; border-bottom: 1px solid transparent; transition: color 0.2s ease, border-color 0.2s ease; }
.footer-replica a:hover { color: var(--accent); border-color: var(--accent); }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
  .hero-canvas { display: none; }
}
/* ≤1024px: the whale moves below the text (JS breakpoint) — open the text
   column to full width, keep it above the whale, soften the overlay so the
   whale below the text stays readable. */
@media (max-width: 1024px) {
  .hero-content { justify-content: flex-start; padding-top: 110px; padding-bottom: 48px; max-width: 100%; }
  .hero-title { font-size: clamp(34px, 7vw, 58px); }
  .hero-overlay {
    background: radial-gradient(ellipse at 50% 26%, transparent 16%, color-mix(in srgb, var(--bg-page) 60%, transparent) 74%);
  }
}
/* ≤900px: timeline stacks — visual on top, step cards below, both scroll-safe. */
@media (max-width: 900px) {
  /* 650vh of scroll for 5 steps is ~1.3 screens per step — exhausting to flick
     through on a phone. Compress to 60vh per step so one flick advances a step. */
  .timeline-scroll { height: 300vh; }
  .timeline-inner { grid-template-columns: 1fr; gap: 0; padding: 0 16px; height: 100dvh; }
  .flow-visual { display: block; height: 38dvh; margin: 0 auto; }
  .flow-svg { height: 38dvh; width: auto; max-width: 100%; }
  .timeline-steps { gap: 10px; margin-top: 4px; height: calc(100dvh - 38dvh); max-height: none; }
  .step { padding: 0; }
  .step-title { font-size: 17px; }
  .step-body { font-size: 14px; }
  .article-inner { padding: 0 20px; }
  .article h2 { font-size: 20px; margin-top: 40px; }
  .article h3 { font-size: 17px; }
  .article p { font-size: 15px; }
  .article blockquote { font-size: 22px; padding-left: 16px; }
}
/* 901–1024px tablets: give the step cards a touch more room. */
@media (min-width: 901px) and (max-width: 1024px) {
  .timeline-inner { grid-template-columns: minmax(0, 1.3fr) minmax(280px, 1fr); gap: 28px; }
}
/* ≤768px: phones. */
@media (max-width: 768px) {
  .hero-eyebrow { margin-bottom: 12px; }
  .hero-title { font-size: clamp(32px, 9.5vw, 48px); margin-bottom: 12px; }
  .hero-subtitle { font-size: 14px; max-width: 100%; }
  .hero-actions { margin-top: 22px; flex-wrap: wrap; }
  .hero-btn { padding: 10px 18px; font-size: 14px; }
  .scroll-indicator { bottom: 16px; }
  .header-nav { gap: 14px; }
}
/* ≤480px: compact the header and hero so nothing overflows or clips. */
@media (max-width: 480px) {
  .site-header { padding: 10px 14px; }
  .logo-text { font-size: 15px; }
  .header-nav a { font-size: 12.5px; }
  .hero-content { padding-top: 84px; }
  .hero-title { font-size: clamp(28px, 9vw, 38px); }
  .hero-subtitle { font-size: 13px; }
  .hero-actions { gap: 10px; width: 100%; }
  .hero-btn { flex: 1 1 auto; justify-content: center; padding: 10px 14px; font-size: 13px; white-space: nowrap; }
}
/* ≤400px: buttons stack full-width so both labels always fit. */
@media (max-width: 400px) {
  .hero-actions { flex-direction: column; align-items: stretch; }
  .hero-btn { width: 100%; }
}
/* Short viewports: keep all five steps reachable by letting the card column
   scroll inside the sticky frame instead of clipping the last step. */
@media (max-height: 700px) {
  .hero { min-height: max(100dvh, 520px); }
  .hero-content { padding: 84px var(--page-margin) 40px; }
  .hero-title { font-size: clamp(36px, 5vw, 64px); }
  .flow-svg { height: min(78vh, 520px); }
  .timeline-steps { gap: 10px; scrollbar-width: thin; }
  .step-title { font-size: 16px; }
  .step-body { font-size: 13px; }
}
/* Very short screens: compact the hero text, hide the scroll hint. */
@media (max-height: 640px) {
  .hero-content { padding-top: 72px; }
  .hero-title { font-size: clamp(26px, 7.5vw, 40px); margin-bottom: 14px; }
  .hero-subtitle { font-size: 13px; line-height: 1.45; }
  .hero-actions { margin-top: 20px; }
  .scroll-indicator { display: none; }
}
/* Very wide screens: let the hero title scale up a bit more. */
@media (min-width: 1600px) {
  .hero-title { font-size: clamp(48px, 5vw, 88px); }
}
</style>
</head>
<body>

<!-- Global FX layer: mouse trail / burst / attract particles across the whole page -->
<canvas class="fx-canvas" id="fx-canvas" aria-hidden="true"></canvas>

<!-- Header -->
<header class="site-header" id="header">
  <div class="header-inner">
    <!-- Language switcher — sits left of the Research mark -->
    <div class="lang-switch" id="lang-switch">
      <button class="lang-trigger" id="lang-trigger" aria-haspopup="true" aria-expanded="false" aria-label="Change language" data-i18n-aria="lang_change">
        <svg class="lang-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3.6 9h16.8M3.6 15h16.8M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/></svg>
        <span class="lang-current" id="lang-current">English</span>
        <svg class="lang-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
      </button>
      <div class="lang-menu" id="lang-menu" role="menu" aria-label="Language" data-i18n-aria="lang_menu">
        <button class="lang-option" role="menuitem" data-lang="zh-CN"><span class="lang-option-label">简体中文</span></button>
        <button class="lang-option" role="menuitem" data-lang="zh-TW"><span class="lang-option-label">繁體中文</span></button>
        <button class="lang-option is-current" role="menuitem" data-lang="en"><span class="lang-option-label">English (US)</span></button>
      </div>
    </div>
    <a href="#" class="logo" aria-label="DeepSeek Research">
      __LOGO__
      <span class="logo-text">DeepSeek <span>Research</span></span>
    </a>
    <nav><ul class="header-nav"><li><a href="#timeline-scroll"><span data-i18n="nav_research">Research</span></a></li><li><a href="#about"><span data-i18n="nav_about">About</span></a></li><li><button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme" title="Toggle theme" data-i18n-aria="theme_toggle" data-i18n-title="theme_toggle"><svg class="theme-icon-sun" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg><svg class="theme-icon-moon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button></li></ul></nav>
  </div>
</header>

<!-- Hero -->
<section class="hero" id="hero">
  <canvas class="hero-canvas" id="hero-canvas" aria-hidden="true"></canvas>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <p class="hero-eyebrow">__LOGO_SMALL__ <span data-i18n="hero_inst">Research Institute</span></p>
    <h1 class="hero-title" data-i18n="hero_title">When AI<br>builds itself</h1>
    <p class="hero-subtitle" data-i18n="hero_sub">Our progress toward recursive self-improvement — where AI systems learn to design, train, and refine the next generation of intelligence. Watch the DeepSeek whale assemble itself, cell by cell, the way the loop compounds.</p>
    <div class="hero-actions">
      <a class="hero-btn hero-btn--primary" href="https://chat.deepseek.com" target="_blank" rel="noopener noreferrer"><span class="btn-comet" aria-hidden="true"></span><span class="btn-dot"></span><span class="btn-label" data-i18n="btn_chat">Try DeepSeek Chat</span></a>
      <a class="hero-btn" href="https://platform.deepseek.com" target="_blank" rel="noopener noreferrer"><span class="btn-comet" aria-hidden="true"></span><span class="btn-label" data-i18n="btn_platform">DeepSeek Platform</span></a>
    </div>
  </div>
  <div class="scroll-indicator" aria-hidden="true"><span data-i18n="scroll">Scroll</span><div class="scroll-line"></div></div>
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
        <div class="step" id="step-0" data-state="active">
          <p class="step-year">2021–2023</p>
          <h3 class="step-title" data-i18n="s0_title">Building the first DeepSeek</h3>
          <p class="step-body" data-i18n="s0_body">In the early days, work at DeepSeek looked like work at any other tech company: people writing code, designing architectures, and tuning hyperparameters by hand. Human researchers drove every decision.</p>
        </div>
        <div class="step" id="step-1" data-state="upcoming">
          <p class="step-year">2023–2025</p>
          <h3 class="step-title" data-i18n="s1_title">Chatbots</h3>
          <p class="step-body" data-i18n="s1_body">People used early AI chatbots to help with parts of the process, like generating short code snippets and summarizing research papers. The models were assistants — useful but not autonomous.</p>
        </div>
        <div class="step" id="step-2" data-state="upcoming">
          <p class="step-year">2025–2026</p>
          <h3 class="step-title" data-i18n="s2_title">Coding agents</h3>
          <p class="step-body" data-i18n="s2_body">As agents became more capable, they were able to write and edit code on their own. DeepSeek’s R1 reasoning model could verify outputs, and coding agents began contributing to training infrastructure.</p>
        </div>
        <div class="step" id="step-3" data-state="upcoming">
          <p class="step-year">Today</p>
          <h3 class="step-title" data-i18n="s3_title">Autonomous agents</h3>
          <p class="step-body" data-i18n="s3_body">Agents can now run code themselves and delegate hours of work to other agents. They assist in architecture search, data curation, and hyperparameter tuning — the research loop starts accelerating.</p>
        </div>
        <div class="step" id="step-4" data-state="upcoming">
          <p class="step-year">20XX?</p>
          <h3 class="step-title" data-i18n="s4_title">Closing the loop</h3>
          <p class="step-body" data-i18n="s4_body">In the future, agents could become capable enough to build and train models themselves. If this happens, AI progress may start to accelerate exponentially — not through better hardware, but through <strong>AI designing the AIs that design the AIs</strong>.</p>
        </div>
      </div>

    </div>
  </div>
</section>

<!-- Benchmarks -->
<section class="benchmarks" id="benchmarks">
  <div class="benchmarks-inner">
    <p class="bench-eyebrow" data-i18n="bench_eyebrow">Benchmarks</p>
    <h2 class="bench-title" data-i18n="bench_title">DeepSeek V4, measured</h2>
    <p class="bench-sub" data-i18n="bench_sub">Every score below is quoted from DeepSeek’s own model cards and the V4 technical report — all at maximum reasoning effort. Toggle between the two members of the V4 family.</p>
    <div class="bench-tabs" role="tablist" aria-label="Benchmark model toggle">
      <span class="bench-thumb" aria-hidden="true"></span>
      <button class="bench-tab is-active" data-model="pro" role="tab" aria-selected="true"><span class="bench-tab-label">DeepSeek V4 Pro</span></button>
      <button class="bench-tab" data-model="flash" role="tab" aria-selected="false"><span class="bench-tab-label">DeepSeek V4 Flash</span></button>
    </div>
    <div class="bench-list" aria-live="polite"></div>
    <p class="bench-asof" data-i18n="bench_asof">Data as of <strong>August 13, 2026</strong> — DeepSeek-V4-Pro-0813 and DeepSeek-V4-Flash-0731 model cards.</p>
    <p class="bench-footnote"><span data-i18n="bench_src_pre">Sources:</span> <a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813" target="_blank" rel="noopener noreferrer"><span data-i18n="bench_card_pro">DeepSeek-V4-Pro model card</span></a><span data-i18n="bench_src_comma">,</span> <a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731" target="_blank" rel="noopener noreferrer"><span data-i18n="bench_card_flash">DeepSeek-V4-Flash model card</span></a><span data-i18n="bench_src_and">, and</span> <a href="https://arxiv.org/abs/2606.19348" target="_blank" rel="noopener noreferrer"><span data-i18n="bench_card_report">V4 technical report</span></a>. <span data-i18n="bench_src_post">This page is an unofficial replica — scores are shown for entertainment and education only.</span></p>
  </div>
</section>

<!-- Model comparison -->
<section class="compare" id="compare">
  <div class="compare-inner">
    <p class="bench-eyebrow" data-i18n="cmp_eyebrow">Against the field</p>
    <h2 class="bench-title" data-i18n="cmp_title">How V4 stacks up</h2>
    <p class="bench-sub" data-i18n="cmp_sub">Latest flagship scores from each lab’s own publications, next to DeepSeek V4 Pro. Bars are color-coded per lab and the DeepSeek row is highlighted. Eval conditions differ between labs, so read this as a rough sketch, not a ranking.</p>
    <div class="compare-grid" id="compare-grid"></div>
    <p class="bench-asof" data-i18n="cmp_asof">Data collected <strong>August 15, 2026</strong> from official model cards and third-party leaderboards (vals.ai, tbench.ai). Terminal-Bench figures span versions 1.0–3.0.</p>
    <p class="bench-footnote"><span data-i18n="cmp_src_pre">Sources:</span> <span data-i18n="cmp_src_lead">each lab’s official model card or launch post;</span> <span data-i18n="cmp_src_card">the DeepSeek row quotes the DeepSeek-V4-Pro model card.</span> <span data-i18n="cmp_src_post">This page is an unofficial replica — scores are shown for entertainment and education only.</span></p>
  </div>
</section>

<!-- Article -->
<article class="article" id="about">
  <div class="article-inner">

    <h2 data-i18n="a1_h">Evidence from the outside world</h2>
    <p data-i18n="a1_p1">The rate at which AI models improve is accelerating. The length of tasks that they can reliably complete on their own has been doubling roughly every four months, up from an earlier trend of doubling every seven months. In March 2024, DeepSeek's first reasoning models could complete software tasks that take humans about four minutes. A year later, R1 could manage tasks that took about an hour and a half. If this trend holds, tasks that take a skilled person days could come into range soon.</p>
    <p data-i18n="a1_p2">The same pattern appears on coding and research benchmarks. <strong>SWE-bench</strong>, a standard test of real-world software engineering, hands a model an actual open-source codebase and a real bug report, and asks it to write a fix that passes the project's own tests. Models have gone from scoring in the low single digits to saturating the benchmark in two years. Benchmarks that test whether a model can reproduce existing research tell the same story: AI systems went from succeeding roughly 20% of the time in 2024 to saturating the benchmark fifteen months later.</p>

    <h2 data-i18n="a2_h">Evidence from within DeepSeek</h2>
    <p data-i18n="a2_p1">Building a frontier model takes two broad categories of work. There is <strong>engineering</strong>: writing the code, standing up the infrastructure, and overseeing model training. And there is <strong>research</strong>: deciding what experiments to run, interpreting what comes back, and figuring out which ideas to try next.</p>
    <p data-i18n="a2_p2">Across both, the picture is consistent. In engineering, the model can be handed an underspecified problem and figure out how to solve it; humans supply the goal, but they no longer need to supply the method. In research, it can already match or outperform skilled humans at executing a well-specified experiment. However, large performance gaps persist when it comes to exercising judgement in choosing goals. That is the gap between AI today and a future system that could autonomously design its own successor.</p>
    <p data-i18n="a2_p3">The model writes a significant proportion of DeepSeek's code. Before the introduction of agentic coding tools, this number was in the low single digits. That shift also shows up in output per engineer: lines of code merged per engineer per day stayed constant for years, then began to climb when the model began to run code rather than just suggesting it. The slope steepened again when models began to work autonomously over longer time horizons.</p>

    <hr>

    <h2 data-i18n="a3_h">What might the future look like?</h2>
    <p data-i18n="a3_p1">The evidence suggests that the human role is narrowing at each step in the AI development process. Once model- and human-authored code reach parity, humans will stop writing code entirely and shift to reviewing it. But if they can't review code as quickly as the model can generate it, human review becomes the bottleneck. Similarly, once the model can run experiments, the question shifts towards "which of these experiments is worth running?"</p>
    <p data-i18n="a3_p2">An area of human comparative advantage, for now, is research taste and judgement — choosing which problems matter, which results to trust, and when an approach is a dead end. It is genuinely unclear whether today's training methods and architectures could unlock that capacity. But AI is rarely advanced by "eureka!" moments. There have been a few, like the Transformer architecture, but paradigm-shifting ideas arrive years apart. In between, most progress is incremental: we scale something up, see what breaks, fix it, and try again. That is exactly the kind of workflow the model now excels at.</p>

    <h2 data-i18n="a4_h">What if we're wrong?</h2>
    <p data-i18n="a4_p1">A natural objection is that the work that is still in human hands — choosing which problems to work on — is what matters most. Without that judgement, the model is a capable assistant, but not a system that could drive AI progress on its own.</p>
    <p data-i18n="a4_p2">Even if the model never achieves good research taste, a conservative reading of the evidence still implies compounding acceleration. If humans spend most of their time on the single-digit fraction of work that is direction-setting, while the model handles the rest, that means each engineer is steering far more work than before. The less conservative reading is that the early evidence on improving research judgement — narrow as it is today — is an indicator that this capability is improving as well. "Research taste" might be just another capability that AI systems fail at for a time, then get good at.</p>

    <h2 data-i18n="a5_h">Possible futures</h2>
    <p data-i18n="a5_p1">What happens next depends on two things: whether the trend continues, and what we choose to do if it does. We can imagine at least three scenarios:</p>
    <ul>
      <li data-i18n="a5_li1"><strong>The trend stalls, but today's capabilities are widely diffused.</strong> Many of these trajectories may actually be S-curves. We may be approaching the bend, where returns to scale diminish and the line flattens.</li>
      <li data-i18n="a5_li2"><strong>AI labs continue to see compounding efficiency gains.</strong> AI development becomes substantially automated, but humans continue to set research directions and judge results. 100-person companies could do the work of 10,000-person organizations.</li>
      <li data-i18n="a5_li3"><strong>AI systems become capable of full recursive self-improvement.</strong> If technical trends continue and AI systems are able to develop the capabilities inherent to transformative human ingenuity, then they could design and refine themselves — closing the loop.</li>
    </ul>
    <p data-i18n="a5_p2">In that last world, the pace of progress in AI development becomes determined entirely by the availability of compute. Humans play a substantially diminished role, likely moving most of our effort towards oversight, validation, and verification of an expanding "virtual lab" run by AI systems.</p>
    <p data-i18n="a5_p3">We are not there yet, and recursive self-improvement is not inevitable. But it could come sooner than most institutions are prepared for.</p>

  </div>
</article>

<!-- Footer -->
<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="#" class="footer-brand-link" aria-label="DeepSeek Research">
        __LOGO_FOOTER__
        <span class="footer-brand-name">DeepSeek <span>Research</span></span>
      </a>
    </div>
    <div class="footer-tag">
      <p class="footer-text" data-i18n="footer_text">Exploring the frontier of recursive self-improvement.</p>
      <p class="footer-replica"><span data-i18n="footer_replica_pre">Replica by</span> <a href="https://github.com/kkkzheli" target="_blank" rel="noopener noreferrer">kkkzheli</a> · <a href="https://github.com/kkkzheli/DeepSeek-Self-Development-WebUI" target="_blank" rel="noopener noreferrer">DeepSeek-Self-Development-WebUI</a></p>
    </div>
  </div>
</footer>

<script id="i18n-data" type="application/json">__I18N_JSON__</script>
<script>
// ===== i18n core =====
// Static text is translated by re-injecting `[data-i18n]` innerHTML; dynamic
// areas (benchmarks, comparison) render through t() and re-render on change.
const __I18N_DATA = JSON.parse(document.getElementById('i18n-data').textContent);
const __I18N_LANGS = ['en', 'zh-CN', 'zh-TW'];
const __I18N_LABELS = { en: 'English (US)', 'zh-CN': '简体中文', 'zh-TW': '繁體中文' };
let __I18N_LANG = 'en';
try {
  const saved = localStorage.getItem('rsi-lang');
  if (__I18N_LANGS.indexOf(saved) >= 0) __I18N_LANG = saved;
} catch (e) {}
window.__i18n = {
  get lang() { return __I18N_LANG; },
  t: function(o) {
    if (o && typeof o === 'object') return o[__I18N_LANG] || o.en || o;
    return o;
  },
  fmt: function(key, vars) {
    let s = (__I18N_DATA[__I18N_LANG] && __I18N_DATA[__I18N_LANG][key])
         || (__I18N_DATA.en && __I18N_DATA.en[key]) || key;
    Object.keys(vars || {}).forEach(function(k) { s = s.split('{' + k + '}').join(vars[k]); });
    return s;
  },
  apply: function(next) {
    if (__I18N_LANGS.indexOf(next) < 0) next = 'en';
    __I18N_LANG = next;
    try { localStorage.setItem('rsi-lang', next); } catch (e) {}
    document.documentElement.lang = next;
    const data = __I18N_DATA[next] || {};
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
      const k = el.getAttribute('data-i18n');
      if (data[k]) el.innerHTML = data[k];
    });
    document.querySelectorAll('[data-i18n-aria]').forEach(function(el) {
      const k = el.getAttribute('data-i18n-aria');
      if (data[k]) el.setAttribute('aria-label', data[k]);
    });
    document.querySelectorAll('[data-i18n-title]').forEach(function(el) {
      const k = el.getAttribute('data-i18n-title');
      if (data[k]) el.setAttribute('title', data[k]);
    });
    const cur = document.getElementById('lang-current');
    if (cur) cur.textContent = __I18N_LABELS[next];
    document.querySelectorAll('.lang-option').forEach(function(btn) {
      btn.classList.toggle('is-current', btn.getAttribute('data-lang') === next);
    });
    if (window.__benchRender) window.__benchRender();
    if (window.__compareRender) window.__compareRender();
    window.dispatchEvent(new CustomEvent('langchange'));
  }
};
// ===== Hero Canvas — The whale grows itself, layer by layer =====
// A big whale silhouette assembled from hundreds of little whale icons.
// A growth front starts at the whale's heart and radiates outward, lighting
// one ring of cells at a time — a visible recursive build-up, then the whole
// thing dissolves and starts over. The big whale is always recognizable
// because every lit cell carries a tiny whale mark inside it.
(function() {
  const canvas = document.getElementById('hero-canvas');
  const ctx = canvas.getContext('2d');
  const hero = document.getElementById('hero');
  const actions = document.querySelector('.hero-actions');
  let lastTextBottom = 0;

  // Official DeepSeek whale mark path (drawn inside each lit cell)
  const WHALE_D = '__WHALE_PATH__';
  // Big-whale silhouette mask (60x45 grid): [[x,y],...]
  const WC = __WHALE_CELLS__;
  const WX = __WHALE_W__, WY = __WHALE_H__;

  // ---- Grid parameters ----
  const CS = 24;             // cell size (px)
  const GAP = 5;             // gap between cells
  const PITCH = CS + GAP;
  const RADIUS = CS * 0.18;  // rounded corners

  // Growth-loop cadence: ~0.9s grow, ~2.3s hold, ~0.9s erase, repeat
  const TICK_MS = 60;        // ms between growth steps
  const GROW_RATE = 0.85;    // front advance per tick (in cells) — steady linear wave
  const HOLD_TICKS = 38;     // full-whale hold duration (~2.3s)

  let w, h, cols, rows;
  let mx = -999, my = -999, tmx = -999, tmy = -999;

  // ---- Theme ----
  let C_BLOCK = '#4d6bfe';
  function readThemeColors() {
    const cs = getComputedStyle(document.documentElement);
    C_BLOCK = cs.getPropertyValue('--accent').trim() || '#4d6bfe';
  }

  // ---- Whale data (built in resize) ----
  let whaleCells = [];   // [{gx,gy,dist}] all cells of the big silhouette
  let whaleOrder = [];   // whaleCells sorted by dist (left->right sweep)
  let whaleSet = {};     // "gx,gy" -> true

  // ---- Animation state ----
  // phase: 'grow' (front radiates outward) → 'hold' (full whale) → 'collapse'
  // (outer rim retreats inward) → repeat
  let cells = {};        // "gx,gy" -> {a, ta, phase, dist}
  let front = 0;         // current growth-front radius (in cells)
  let frontMax = 1;
  let cycle = 0;         // ticks spent in current phase
  let lastTick = 0;

  // Real bottom of the hero text block (px within the hero), measured from the
  // DOM so the whale always sits clear of the buttons no matter how fonts,
  // wrapping, or breakpoints reflow the text. Guards against off-canvas reads.
  function measureTextBottom(r) {
    const ar = actions.getBoundingClientRect();
    const b = ar.bottom - r.top;
    if (b > 40 && ar.height > 0) lastTextBottom = b;
    return lastTextBottom;
  }

  function resize() {
    const r = hero.getBoundingClientRect();
    w = r.width; h = r.height;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = w * dpr; canvas.height = h * dpr;
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cols = Math.max(10, Math.floor(w / PITCH));
    rows = Math.max(8, Math.floor(h / PITCH));

    // Whale sized to ~68% of viewport height (desktop: right third, clear of
    // the title text) or to the mobile width (below the text, centered).
    // The breakpoint is 1024px, not 768px: between 768-1024px the desktop
    // placement collided with the text, so anything below 1024px puts the
    // whale under the text block instead. Never overflows the canvas.
    const targetH = Math.floor(h * 0.68 / PITCH);
    let scale = Math.max(6, Math.min(WY, targetH)) / WY;
    let ox, oy;
    let wW, wH;
    // Breakpoint uses the viewport width (incl. scrollbar), matching the CSS
    // media query, instead of the hero rect width (which shrinks by the
    // scrollbar width and would flip layout at 1024-1040px viewports).
    if (window.innerWidth < 1025) {
      // Real height of the hero text block, measured from the DOM (the
      // .hero-actions row's bottom edge). The whale is centered vertically in
      // the space left below the text, so it never collides with the buttons
      // no matter how the text reflows.
      const textH = measureTextBottom(r) + 28;
      const avail = h - textH;
      scale = Math.min(scale, (cols - 2) / WX, Math.max(24, avail) / PITCH / WY);
      wW = Math.round(WX * scale); wH = Math.round(WY * scale);
      ox = Math.floor((cols - wW) / 2);
      oy = Math.floor(textH / PITCH) + Math.floor(Math.max(0, rows - textH / PITCH - wH) / 2);
    } else {
      // desktop: cap by 44% of the grid width so the whale always clears the
      // text column, then anchor it to the right third
      scale = Math.min(scale, (cols * 0.44) / WX);
      wW = Math.round(WX * scale); wH = Math.round(WY * scale);
      ox = Math.floor(cols * 0.76) - Math.floor(wW * 0.5);
      oy = Math.floor((rows - wH) / 2);
    }
    // hard bounds so nothing ever leaves the canvas
    if (ox + wW > cols) ox = cols - wW;
    if (oy + wH > rows) oy = rows - wH;
    if (ox < 0) ox = 0;
    if (oy < 0) oy = 0;

    const wmask = {};
    WC.forEach(function(c) { wmask[c[1] * WX + c[0]] = true; });
    whaleCells = [];
    whaleSet = {};
    for (let gy = 0; gy < wH; gy++)
      for (let gx = 0; gx < wW; gx++) {
        const sx = Math.floor(gx * WX / wW), sy = Math.floor(gy * WY / wH);
        if (!wmask[sy * WX + sx]) continue;
        const ax = gx + ox, ay = gy + oy;
        whaleCells.push({ gx: ax, gy: ay });
        whaleSet[ax + ',' + ay] = true;
      }
    // Radiate outward from the whale's heart (its geometric center): the wave
    // expands in every direction at once, so the fins, head and tail appear
    // together as the front swells past them.
    const ccx = ox + wW / 2, ccy = oy + wH / 2;
    whaleCells.forEach(function(c) { c.dist = Math.hypot(c.gx - ccx, c.gy - ccy); });
    whaleOrder = whaleCells.slice().sort(function(a, b) { return a.dist - b.dist || a.gy - b.gy; });
    frontMax = whaleOrder.length ? whaleOrder[whaleOrder.length - 1].dist : 1;

    cells = {};
    front = 0;
    cycle = 0;
  }

  function pickAlpha() {
    const opts = [0.55, 0.7, 0.85, 1.0];
    return opts[Math.floor(Math.random() * opts.length)];
  }

  function step() {
    cycle += 1;
    const growTicks = Math.ceil(frontMax / GROW_RATE);
    const collapseTicks = Math.ceil(frontMax / GROW_RATE);
    const holdEnd = growTicks + HOLD_TICKS;
    const collapsing = cycle > holdEnd;
    if (cycle < growTicks) {
      // growing: the front swells with an ease-in-out wave — a smooth,
      // fluid ripple gathering speed through the body, then settling
      const p = cycle / growTicks;
      front = frontMax * (1 - Math.cos(Math.PI * p)) / 2;
    } else if (collapsing) {
      // collapsing: the outer rim goes dark first and the surviving region
      // shrinks toward the heart, so the whale deflates into itself — the
      // rim dissolves slowly, picks up, then vanishes softly at the center.
      // Clamp p at 1: past it cos(π·p) swings back, the wavefront retreats,
      // and heart cells stop fading — stranded at a mid alpha forever.
      const p = Math.min(1, (cycle - holdEnd) / collapseTicks);
      const depth = frontMax * (1 - Math.cos(Math.PI * p)) / 2;
      for (const key in cells) {
        const cell = cells[key];
        if (cell.dist >= frontMax - depth) {
          cell.a -= 0.28;
          if (cell.a <= 0.02) delete cells[key];
        }
      }
      if (!Object.keys(cells).length) { front = 0; cycle = 0; }
    } else {
      front = frontMax;
    }
    if (collapsing) return;  // don't re-light cells while the whale deflates
    // light cells whose distance <= front, and fade ones behind
    for (let i = 0; i < whaleOrder.length; i++) {
      const c = whaleOrder[i];
      const key = c.gx + ',' + c.gy;
      const target = c.dist <= front ? 1 : 0;
      if (target === 1) {
        if (!cells[key]) cells[key] = { a: 0.12, ta: pickAlpha(), phase: Math.random() * 6.28, dist: c.dist };
        else if (cells[key].a < cells[key].ta) cells[key].a = Math.min(cells[key].ta, cells[key].a + 0.22);
      } else if (cells[key] && cycle < growTicks) {
        // fade out cells behind the front
        cells[key].a -= 0.08;
        if (cells[key].a <= 0.02) delete cells[key];
      }
    }
  }

  function drawCell(gx, gy, cell) {
    const px = gx * PITCH, py = gy * PITCH;
    const t = performance.now() / 1000;
    let pulse = 0.9 + 0.1 * Math.sin(t * 2 + cell.phase);
    // mouse proximity boost: cells near cursor glow brighter
    const cellCx = px + CS / 2, cellCy = py + CS / 2;
    const dMouse = Math.hypot(cellCx - mx, cellCy - my);
    if (dMouse < PITCH * 4) {
      pulse += (1 - dMouse / (PITCH * 4)) * 0.25;
    }
    ctx.globalAlpha = Math.min(1, cell.a * pulse);
    // whale mark fills the cell (recursive nesting)
    ctx.save();
    ctx.translate(px + CS / 2, py + CS / 2);
    ctx.scale(0.85, 0.85);
    ctx.fillStyle = C_BLOCK;
    ctx.beginPath();
    ctx.fill(new Path2D(WHALE_D));
    ctx.restore();
    ctx.globalAlpha = 1;
  }

  // ===== Mouse particles live on the global #fx-canvas (fixed, full viewport) =====
  // so they keep following the cursor below the fold too. The hero canvas here
  // only draws the whale and its cursor-proximity glow.

  function draw() {
    ctx.clearRect(0, 0, w, h);
    mx += (tmx - mx) * 0.06; my += (tmy - my) * 0.06;

    // lit whale cells
    for (const key in cells) {
      const [gx, gy] = key.split(',').map(Number);
      drawCell(gx, gy, cells[key]);
    }
  }

  let heroVisible = true;
  const heroObs = new IntersectionObserver(function(entries) {
    heroVisible = entries[0].isIntersecting;
  }, { threshold: 0.05 });
  heroObs.observe(hero);

  function loop() {
    const rNow = hero.getBoundingClientRect();
    if (Math.abs(rNow.width - w) > 2 || Math.abs(rNow.height - h) > 2) {
      resize();
    } else if (window.innerWidth < 1025) {
      // Real-time reflow: font swaps, text wrapping, or overlay squeezes can
      // move the text block without changing the hero rect — reposition the
      // whale the moment it does, no manual refresh needed.
      const b = actions.getBoundingClientRect().bottom - rNow.top;
      if (Math.abs(b - lastTextBottom) > 6) resize();
    }
    const now = performance.now();
    if (heroVisible) {
      if (now - lastTick >= TICK_MS) { lastTick = now; step(); }
      draw();
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
  hero.addEventListener('touchstart', function(e) {
    const r = hero.getBoundingClientRect();
    tmx = e.touches[0].clientX - r.left; tmy = e.touches[0].clientY - r.top;
  }, {passive: true});
  hero.addEventListener('touchend', function() { tmx = -999; tmy = -999; });

  window.addEventListener('resize', resize);
  window.addEventListener('themechange', readThemeColors);
  // Real-time adaptation for anything that squeezes or grows the hero without
  // firing a window resize (browser info bars, docked panels, pinch zoom,
  // mobile URL bars): watch the hero box and the visual viewport directly.
  new ResizeObserver(function() { resize(); }).observe(hero);
  if (window.visualViewport) {
    window.visualViewport.addEventListener('resize', resize);
    window.visualViewport.addEventListener('scroll', resize);
  }
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { resize(); draw(); return; }
  readThemeColors();
  resize();
  requestAnimationFrame(loop);
})();

// ===== Global FX canvas — mouse particles follow the cursor across the whole page =====
// A fixed full-viewport canvas (z-index below the header, pointer-events: none)
// draws the trail / burst / attract particles at ANY scroll position, so the
// effect keeps working below the hero. Colors are read from the theme so the
// particles stay vivid in both light and dark mode.
(function() {
  const cv = document.getElementById('fx-canvas');
  const ctx = cv.getContext('2d');
  let w = window.innerWidth, h = window.innerHeight;
  const MAX_PARTICLES = 1600;
  let particles = [];
  let mx = -999, my = -999, tmx = -999, tmy = -999;
  let lastMx = -999, lastMy = -999;
  let isDragging = false;
  let C_ACCENT = '#4d6bfe', C_GLOW = '#9db5ff', C_CORE = '#ffffff';

  function readFxColors() {
    const cs = getComputedStyle(document.documentElement);
    const dark = document.documentElement.getAttribute('data-theme') === 'dark';
    C_ACCENT = cs.getPropertyValue('--accent').trim() || '#4d6bfe';
    C_GLOW = cs.getPropertyValue('--accent-bright').trim() || C_ACCENT;
    C_CORE = dark ? '#ffffff' : '#e4edfd';
  }

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = window.innerWidth; h = window.innerHeight;
    cv.width = w * dpr; cv.height = h * dpr;
    cv.style.width = w + 'px'; cv.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function spawn(x, y, vx, vy, opts) {
    opts = opts || {};
    // reuse a dead slot if the pool is full
    let p = particles.find(function(pp) { return pp.life <= 0; });
    if (!p) {
      if (particles.length >= MAX_PARTICLES) return;
      p = {}; particles.push(p);
    }
    p.x = x; p.y = y; p.vx = vx; p.vy = vy;
    p.maxLife = opts.maxLife || 0.8;
    p.life = p.maxLife;
    p.size = opts.size || (1.6 + Math.random() * 1.8);
    p.type = opts.type || 'attract';
    p.drag = opts.drag || 0.92;
    p.tw = 1 + Math.random() * 3;        // twinkle speed (rad/s)
    p.ph = Math.random() * Math.PI * 2;  // twinkle phase
  }

  function burst(x, y) {
    const n = 20;   // slightly fewer than before; speed/range unchanged
    for (let i = 0; i < n; i++) {
      const ang = (i / n) * Math.PI * 2 + Math.random() * 0.5;
      const sp = 2.6 + Math.random() * 3.6;   // faster + further than before
      spawn(x, y, Math.cos(ang) * sp, Math.sin(ang) * sp, {
        maxLife: 0.55 + Math.random() * 0.4, size: 2.2 + Math.random() * 2.4, type: 'burst', drag: 0.9
      });
    }
  }

  function update() {
    // Wide, soft gather field: ambient particles drift toward the cursor and
    // cluster into a loose cloud (force dies inside ~46px so they never pile
    // into a single dot). Dragging pulls harder.
    const attractR = 260;
    mx += (tmx - mx) * 0.12; my += (tmy - my) * 0.12;

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      if (p.life <= 0) {
        // ambient attract particles respawn so the drifting cloud never thins
        if (p.type === 'attract') {
          p.x = Math.random() * w; p.y = Math.random() * h;
          p.vx = (Math.random() - 0.5) * 0.25; p.vy = (Math.random() - 0.5) * 0.25;
          p.life = p.maxLife;
        }
        continue;
      }
      p.life -= 1 / 60;
      if (p.life <= 0) { p.life = 0; continue; }

      if (p.type === 'attract' && mx > -900) {
        const dx = mx - p.x, dy = my - p.y;
        const dist = Math.hypot(dx, dy);
        if (dist < attractR && dist > 0.5) {
          const f = (1 - dist / attractR) * (isDragging ? 1.5 : 0.85);
          p.vx += (dx / dist) * f * Math.min(1, dist / 46);
          p.vy += (dy / dist) * f * Math.min(1, dist / 46);
        }
        p.vx *= p.drag; p.vy *= p.drag;
      } else if (p.type === 'burst') {
        p.vx *= p.drag; p.vy *= p.drag;
        p.vy += 0.05; // slight settle
      }
      p.x += p.vx; p.y += p.vy;
    }

    lastMx = mx; lastMy = my;
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    const now = performance.now() / 1000;
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      if (p.life <= 0) continue;
      // twinkle: brightness breathes per-particle, like distant stars
      const tw = 0.5 + 0.5 * Math.sin(now * p.tw + p.ph);
      const a = Math.max(0, p.life / p.maxLife) * tw;
      const t = p.size * (0.55 + 0.3 * a);
      // soft outer glow
      ctx.globalAlpha = a * 0.3;
      ctx.fillStyle = C_GLOW;
      ctx.beginPath(); ctx.arc(p.x, p.y, t * 2.6, 0, Math.PI * 2); ctx.fill();
      // accent body
      ctx.globalAlpha = a * 0.9;
      ctx.fillStyle = C_ACCENT;
      ctx.beginPath(); ctx.arc(p.x, p.y, t, 0, Math.PI * 2); ctx.fill();
      // bright core
      ctx.globalAlpha = a * (p.type === 'burst' ? 1 : 0.85);
      ctx.fillStyle = C_CORE;
      ctx.beginPath(); ctx.arc(p.x, p.y, t * 0.55, 0, Math.PI * 2); ctx.fill();
    }
    ctx.globalAlpha = 1;
  }

  function seed() {
    // Night-sky density: ~7x the sparse field of the first version, with a slow
    // drift and per-particle twinkle (see draw). Density scales with area:
    // ~380 stars on a 1536×647 window.
    const n = Math.round((w * h) / 2600);
    for (let i = 0; i < n; i++) {
      spawn(Math.random() * w, Math.random() * h,
        (Math.random() - 0.5) * 0.22, (Math.random() - 0.5) * 0.22,
        { maxLife: 6 + Math.random() * 5, size: 0.6 + Math.random() * 1.5, type: 'attract', drag: 0.97 });
    }
  }

  function loop() {
    if (window.innerWidth !== w || window.innerHeight !== h) resize();
    update();
    draw();
    requestAnimationFrame(loop);
  }

  window.addEventListener('mousemove', function(e) {
    tmx = e.clientX; tmy = e.clientY;
  }, {passive: true});
  window.addEventListener('mouseleave', function() { tmx = -999; tmy = -999; });
  window.addEventListener('mousedown', function(e) {
    if (e.button !== 0) return;
    tmx = e.clientX; tmy = e.clientY;
    isDragging = true;
    burst(e.clientX, e.clientY);
  }, {passive: true});
  window.addEventListener('mouseup', function() { isDragging = false; });
  window.addEventListener('touchmove', function(e) {
    if (!e.touches.length) return;
    tmx = e.touches[0].clientX; tmy = e.touches[0].clientY;
  }, {passive: true});
  window.addEventListener('touchstart', function(e) {
    if (!e.touches.length) return;
    const t = e.touches[0];
    tmx = t.clientX; tmy = t.clientY;
    isDragging = true;
    burst(t.clientX, t.clientY);
  }, {passive: true});
  window.addEventListener('touchend', function() { isDragging = false; });
  window.addEventListener('resize', resize);
  window.addEventListener('themechange', readFxColors);

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  readFxColors();
  resize();
  seed();
  requestAnimationFrame(loop);
})();

// ===== Buttons — soft follow-light + orbiting edge comet =====
// One light trails the cursor smoothly (lerped in a rAF loop); --mx/--my drive
// the inner wash (::before) while hovering. While the pointer stays over the
// element, --spin advances continuously in the same loop, so the comet that
// orbits the edge ring never restarts or jumps when hover begins.
(function() {
  const btns = document.querySelectorAll('.hero-btn');
  btns.forEach(function(btn) {
    const target = { x: -999, y: -999 };
    const cur = { x: -999, y: -999 };
    let raf = 0, lastT = 0, spin = 0, hovering = false;
    btn.addEventListener('mouseenter', function() {
      hovering = true;
      if (!raf) { lastT = 0; tick(performance.now()); }
    });
    btn.addEventListener('mousemove', function(e) {
      const r = btn.getBoundingClientRect();
      target.x = e.clientX - r.left;
      target.y = e.clientY - r.top;
      if (cur.x === -999) { cur.x = target.x; cur.y = target.y; } // snap on entry
      if (!raf) { lastT = 0; tick(performance.now()); }
    });
    btn.addEventListener('mouseleave', function() {
      hovering = false;
      if (raf) { cancelAnimationFrame(raf); raf = 0; }
      // keep the last --mx/--my so the follow-light fades out in place
      // instead of snapping back to the button center
    });
    function tick(t) {
      if (!lastT) lastT = t;
      const dt = Math.min(0.1, (t - lastT) / 1000); // frame-rate independent
      lastT = t;
      const k = 1 - Math.exp(-26 * dt);             // ~0.35/frame at 60fps — snappy real-time follow
      cur.x += (target.x - cur.x) * k;
      cur.y += (target.y - cur.y) * k;
      btn.style.setProperty('--mx', cur.x.toFixed(1) + 'px');
      btn.style.setProperty('--my', cur.y.toFixed(1) + 'px');
      if (hovering) {
        spin = (spin + dt * 240) % 360;             // ~66s per lap, gentle
        btn.style.setProperty('--spin', spin.toFixed(2) + 'deg');
      }
      raf = requestAnimationFrame(tick);
    }
  });
})();


// ===== Benchmarks leaderboard =====
// Scores from DeepSeek's own GA model cards (DeepSeek-V4-Pro-0813 /
// DeepSeek-V4-Flash-0731) and the V4 technical report (arXiv:2606.19348),
// all at maximum reasoning effort. Percent-style benchmarks scale to 100;
// Codeforces is an Elo rating and scales against 3500.
(function() {
  // trilingual helper: n('en', 'zh-CN', 'zh-TW')
  const n = (en, zhCN, zhTW) => ({ en: en, 'zh-CN': zhCN, 'zh-TW': zhTW });
  const BENCH = {
    pro: [
      { group: n('Coding', '编程', '程式設計'), name: 'SWE-bench Verified', v: 80.6 },
      { name: 'Terminal-Bench 2.1', v: 87.9 },
      { name: 'LiveCodeBench', v: 93.5 },
      { name: 'Codeforces', v: 3206, max: 3500, fmt: 'elo' },
      { group: n('Reasoning & Knowledge', '推理与知识', '推理與知識'), name: 'GPQA Diamond', v: 90.1 },
      { name: 'MMLU-Pro', v: 87.5 },
      { name: 'HMMT 2026 (Feb)', v: 95.2 },
      { name: 'IMO AnswerBench', v: 89.8 },
      { name: 'SimpleQA-Verified', v: 57.9 },
      { name: 'Chinese-SimpleQA', v: 84.4 },
      { group: n('Agentic', '智能体', '智能體'), name: "Humanity's Last Exam", v: 42.7, note: n('60.0 with tools', '60.0（配合工具）', '60.0（搭配工具）') },
      { name: 'BrowseComp', v: 83.4 },
      { name: 'NL2Repo', v: 61.5 },
      { name: 'DeepSWE', v: 62.7 },
      { name: 'Apex', v: 38.3, note: n('Shortlist 90.2', '短名单 90.2', '短名單 90.2') }
    ],
    flash: [
      { group: n('Coding', '编程', '程式設計'), name: 'SWE-bench Verified', v: 79.0 },
      { name: 'Terminal-Bench 2.1', v: 82.7 },
      { name: 'LiveCodeBench', v: 91.6 },
      { name: 'Codeforces', v: 3052, max: 3500, fmt: 'elo' },
      { group: n('Reasoning & Knowledge', '推理与知识', '推理與知識'), name: 'GPQA Diamond', v: 88.1 },
      { name: 'MMLU-Pro', v: 86.2 },
      { name: 'HMMT 2026 (Feb)', v: 94.8 },
      { name: 'IMO AnswerBench', v: 88.4 },
      { name: 'SimpleQA-Verified', v: 34.1 },
      { name: 'Chinese-SimpleQA', v: 78.9 },
      { group: n('Agentic', '智能体', '智能體'), name: "Humanity's Last Exam", v: 32.6, note: n('51.1 with tools', '51.1（配合工具）', '51.1（搭配工具）') },
      { name: 'BrowseComp', v: 73.2 },
      { name: 'NL2Repo', v: 54.2 },
      { name: 'DeepSWE', v: 54.4 },
      { name: 'Apex', v: 33.0, note: n('Shortlist 85.7', '短名单 85.7', '短名單 85.7') }
    ]
  };
  const list = document.querySelector('.bench-list');
  const track = document.querySelector('.bench-tabs');
  const thumb = document.querySelector('.bench-thumb');
  const tabs = document.querySelectorAll('.bench-tab');
  let animTimer = [];
  // Slide the accent pill under the active tab (outCubic via CSS transition).
  // Baseline is the first tab's rect, so border/padding offsets cancel out.
  function moveThumb(t) {
    const base = tabs[0].getBoundingClientRect();
    const r = t.getBoundingClientRect();
    thumb.style.width = r.width + 'px';
    thumb.style.transform = 'translateX(' + (r.left - base.left) + 'px)';
  }
  function render(model) {
    list.innerHTML = '';
    let lastGroup = '';
    BENCH[model].forEach(function(r) {
      if (r.group && r.group !== lastGroup) {
        lastGroup = r.group;
        const g = document.createElement('p');
        g.className = 'bench-group-label';
        g.textContent = window.__i18n.t(r.group);
        list.appendChild(g);
      }
      const row = document.createElement('div');
      row.className = 'bench-row';
      const top = document.createElement('div');
      top.className = 'bench-row-top';
      const name = document.createElement('span');
      name.className = 'bench-name';
      name.textContent = r.name;
      top.appendChild(name);
      if (r.note) {
        const note = document.createElement('span');
        note.className = 'bench-note';
        note.textContent = window.__i18n.t(r.note);
        top.appendChild(note);
      }
      const score = document.createElement('span');
      score.className = 'bench-score';
      score.textContent = r.fmt === 'elo' ? r.v.toLocaleString('en-US') + ' Elo' : r.v.toFixed(1) + '%';
      top.appendChild(score);
      const track = document.createElement('div');
      track.className = 'bench-track';
      const bar = document.createElement('div');
      bar.className = 'bench-bar';
      bar.dataset.w = (r.v / (r.max || 100) * 100).toFixed(1);
      track.appendChild(bar);
      row.appendChild(top);
      row.appendChild(track);
      list.appendChild(row);
    });
    animTimer.forEach(clearTimeout);
    animTimer = [];
    requestAnimationFrame(function() {
      list.querySelectorAll('.bench-bar').forEach(function(b, i) {
        animTimer.push(setTimeout(function() {
          b.style.width = b.dataset.w + '%';
        }, 60 + i * 40));
      });
    });
  }
  tabs.forEach(function(t) {
    t.addEventListener('click', function() {
      if (t.classList.contains('is-active')) return;
      tabs.forEach(function(x) {
        x.classList.remove('is-active');
        x.setAttribute('aria-selected', 'false');
      });
      t.classList.add('is-active');
      t.setAttribute('aria-selected', 'true');
      moveThumb(t);
      render(t.dataset.model);
    });
  });
  moveThumb(document.querySelector('.bench-tab.is-active'));
  window.addEventListener('resize', function() {
    moveThumb(document.querySelector('.bench-tab.is-active'));
  });
  render('pro');
  // Language switches re-render the current tab through t()
  window.__benchRender = function() {
    const active = document.querySelector('.bench-tab.is-active');
    render(active ? active.dataset.model : 'pro');
  };
})();

// ===== Model comparison — latest flagships vs DeepSeek V4 Pro =====
// COMPARE: one entry per benchmark; each lists 10 flagship models with
// {name, logo, v, color, note?, inv?}. Rows marked ds get the accent halo +
// badge; inv marks single-colour logos that need inverting on dark theme.
// Scores verified online (2026-08-15): official model cards where published,
// otherwise vals.ai / tbench.ai / Artificial Analysis third-party runs.
(function() {
  const DS_LOGO = 'DATAURI_DEEPSEEK_LOGO';
  const L = {
    openai:   { logo: 'LOGO_URI_OPENAI', inv: true },
    anthropic:{ logo: 'LOGO_URI_ANTHROPIC' },
    google:   { logo: 'LOGO_URI_GOOGLE' },
    grok:     { logo: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNCAzMiI+PHBhdGggZD0iTTEzLjM3NCAyMC41NDA3TDI0LjQ1NTUgMTIuMzUwNkMyNC45OTg4IDExLjk0OTEgMjUuNzc1MyAxMi4xMDU3IDI2LjAzNDIgMTIuNzI5NEMyNy4zOTY2IDE2LjAxODUgMjYuNzg3OSAxOS45NzEyIDI0LjA3NzIgMjIuNjg1MUMyMS4zNjY2IDI1LjM5ODkgMTcuNTk1IDI1Ljk5NDEgMTQuMTQ3NyAyNC42Mzg2TDEwLjM4MTggMjYuMzg0M0MxNS43ODMyIDMwLjA4MDYgMjIuMzQyMiAyOS4xNjY1IDI2LjQ0MDkgMjUuMDYwMUMyOS42OTIgMjEuODA1MSAzMC42OTg5IDE3LjM2ODMgMjkuNzU3NCAxMy4zNjczTDI5Ljc2NTkgMTMuMzc1OEMyOC40MDA2IDcuNDk4MDkgMzAuMTAxNiA1LjE0ODcxIDMzLjU4NTkgMC4zNDQ1NzZDMzMuNjY4MyAwLjIzMDY2NyAzMy43NTA4IDAuMTE2NzU3IDMzLjgzMzMgMEwyOS4yNDgyIDQuNTkwNTVWNC41NzYzMUwxMy4zNzEyIDIwLjU0MzYiIGZpbGw9ImJsYWNrIi8+PHBhdGggZD0iTTExLjA4NjcgMjIuNTMxMkM3LjIwOTc5IDE4LjgyMzQgNy44NzgyMSAxMy4wODUyIDExLjE4NjIgOS43NzYxOEMxMy42MzIzIDcuMzI3MSAxNy42NCA2LjMyNzU1IDIxLjEzODUgNy43OTY5OEwyNC44OTU5IDYuMDU5ODZDMjQuMjE5IDUuNTcwMDUgMjMuMzUxNCA1LjA0MzIyIDIyLjM1NTkgNC42NzMwMUMxNy44NTYyIDIuODE5MTQgMTIuNDY5IDMuNzQxOCA4LjgxMTE1IDcuNDAxMTRDNS4yOTI3MSAxMC45MjM4IDQuMTg2MjYgMTYuMzQwMiA2LjA4NjI4IDIwLjk2MjFDNy41MDU2IDI0LjQxNjQgNS4xNzg5MyAyNi44NTk3IDIuODM1MiAyOS4zMjU5QzIuMDA0NjUgMzAuMjAwMSAxLjE3MTI2IDMxLjA3NDQgMC41IDMxLjk5OTlMMTEuMDgzOCAyMi41MzQiIGZpbGw9ImJsYWNrIi8+PC9zdmc+', inv: true },
    meta:     { logo: 'LOGO_URI_META' },
    qwen:     { logo: 'LOGO_URI_QWEN' },
    kimi:     { logo: 'LOGO_URI_KIMI', inv: true },
    glm:      { logo: 'LOGO_URI_GLM' },
    mistral:  { logo: 'LOGO_URI_MISTRAL' },
    ds:       { logo: DS_LOGO }
  };
  // trilingual helper: N('en', 'zh-CN', 'zh-TW')
  const N = (en, zhCN, zhTW) => ({ en: en, 'zh-CN': zhCN, 'zh-TW': zhTW });
  const COMPARE = [
    {
      name: 'SWE-bench Verified',
      hint: N('official cards where published, otherwise third-party runs', '官方卡优先，否则为第三方跑分', '官方卡優先，否則為第三方跑分'),
      models: [
        { name: 'GPT-5.6 Sol',        l: 'openai',    v: 96.2, color: '#10A37F', note: N('vals.ai SWE-bench run (Aug 2026); OpenAI publishes SWE-bench Pro, not Verified', 'vals.ai SWE-bench 跑分（2026 年 8 月）；OpenAI 官方发布的是 SWE-bench Pro 而非 Verified', 'vals.ai SWE-bench 跑分（2026 年 8 月）；OpenAI 官方發布的是 SWE-bench Pro 而非 Verified') },
        { name: 'Grok 4.6',           l: 'grok',      v: 95.6, color: '#B8C4DE', note: N('vals.ai independent run (Aug 2026, ±0.92); not published by xAI', 'vals.ai 独立跑分（2026 年 8 月，±0.92）；xAI 未官方发布', 'vals.ai 獨立跑分（2026 年 8 月，±0.92）；xAI 未官方發布') },
        { name: 'Claude Fable 5',     l: 'anthropic', v: 95.0, color: '#D97757', note: N('Official Claude Fable 5 system card, max reasoning, 5-run average', 'Claude Fable 5 官方系统卡，最高推理强度，5 次跑分平均', 'Claude Fable 5 官方系統卡，最高推理強度，5 次跑分平均') },
        { name: 'Kimi K3',            l: 'kimi',      v: 93.4, color: '#6C8CFF', note: N('vals.ai independent run (Aug 2026); official card reports DeepSWE instead', 'vals.ai 独立跑分（2026 年 8 月）；官方卡发布的是 DeepSWE', 'vals.ai 獨立跑分（2026 年 8 月）；官方卡發布的是 DeepSWE') },
        { name: 'Qwen3.8-Max',        l: 'qwen',      v: 85.6, color: '#00B4D8', note: N('vals.ai run (Aug 2026, Mini-SWE-agent); official card reports SWE-bench Pro 67.7', 'vals.ai 跑分（2026 年 8 月，Mini-SWE-agent）；官方卡发布 SWE-bench Pro 67.7', 'vals.ai 跑分（2026 年 8 月，Mini-SWE-agent）；官方卡發布 SWE-bench Pro 67.7') },
        { name: 'GLM-5.2',            l: 'glm',       v: 82.8, color: '#8B5CF6', note: N('vals.ai run (Jun 2026); official card reports SWE-bench Pro 62.1', 'vals.ai 跑分（2026 年 6 月）；官方卡发布 SWE-bench Pro 62.1', 'vals.ai 跑分（2026 年 6 月）；官方卡發布 SWE-bench Pro 62.1') },
        { name: 'DeepSeek V4 Pro',    l: 'ds',        v: 80.6, color: 'var(--accent)', ds: true, note: N('Official DeepSeek-V4-Pro-0813 model card', 'DeepSeek-V4-Pro-0813 官方模型卡', 'DeepSeek-V4-Pro-0813 官方模型卡') },
        { name: 'Gemini 3.1 Pro',     l: 'google',    v: 80.6, color: '#F4B400', note: N('Official Google launch table, thinking mode on', 'Google 官方发布表，思考模式开启', 'Google 官方發布表，思考模式開啟') },
        { name: 'Mistral Large 3',    l: 'mistral',   v: 41.4, color: '#FF8A00', note: N('vals.ai run (Aug 2026, ±2.21); not published by Mistral', 'vals.ai 跑分（2026 年 8 月，±2.21）；Mistral 未官方发布', 'vals.ai 跑分（2026 年 8 月，±2.21）；Mistral 未官方發布') },
        { name: 'Llama 4 Maverick',   l: 'meta',      v: 36.8, color: '#0668E1', note: N('OpenHands community eval (Apr 2025); Meta never published SWE-bench Verified', 'OpenHands 社区评测（2025 年 4 月）；Meta 从未发布 SWE-bench Verified', 'OpenHands 社群評測（2025 年 4 月）；Meta 從未發布 SWE-bench Verified') }
      ]
    },
    {
      name: 'GPQA Diamond',
      hint: N('official cards where published, otherwise third-party runs', '官方卡优先，否则为第三方跑分', '官方卡優先，否則為第三方跑分'),
      models: [
        { name: 'GPT-5.6 Sol',        l: 'openai',    v: 95.2, color: '#10A37F', note: N('vals.ai run (Aug 2026); not published by OpenAI', 'vals.ai 跑分（2026 年 8 月）；OpenAI 未官方发布', 'vals.ai 跑分（2026 年 8 月）；OpenAI 未官方發布') },
        { name: 'Grok 4.6',           l: 'grok',      v: 94.7, color: '#B8C4DE', note: N('vals.ai independent run (Aug 2026, ±1.13); xAI post claimed 94.9%', 'vals.ai 独立跑分（2026 年 8 月，±1.13）；xAI 官方帖子称 94.9%', 'vals.ai 獨立跑分（2026 年 8 月，±1.13）；xAI 官方貼文稱 94.9%') },
        { name: 'Gemini 3.1 Pro',     l: 'google',    v: 94.3, color: '#F4B400', note: N('Official Google launch table, thinking mode on', 'Google 官方发布表，思考模式开启', 'Google 官方發布表，思考模式開啟') },
        { name: 'Kimi K3',            l: 'kimi',      v: 93.5, color: '#6C8CFF', note: N('Official Kimi K3 technical report, max reasoning effort', 'Kimi K3 官方技术报告，最高推理强度', 'Kimi K3 官方技術報告，最高推理強度') },
        { name: 'Claude Fable 5',     l: 'anthropic', v: 93.2, color: '#D97757', note: N('vals.ai run (Aug 2026); falls to ~55.6% if refusals count as failures', 'vals.ai 跑分（2026 年 8 月）；若拒答计为失败则降至约 55.6%', 'vals.ai 跑分（2026 年 8 月）；若拒答計為失敗則降至約 55.6%') },
        { name: 'Qwen3.8-Max',        l: 'qwen',      v: 92.6, color: '#00B4D8', note: N('Official Qwen model card (max reasoning); AA run 92.7 corroborates', 'Qwen 官方模型卡（最高推理）；AA 跑分 92.7 佐证', 'Qwen 官方模型卡（最高推理）；AA 跑分 92.7 佐證') },
        { name: 'GLM-5.2',            l: 'glm',       v: 91.2, color: '#8B5CF6', note: N('Official GLM-5.2 model card, max reasoning effort', 'GLM-5.2 官方模型卡，最高推理强度', 'GLM-5.2 官方模型卡，最高推理強度') },
        { name: 'DeepSeek V4 Pro',    l: 'ds',        v: 90.1, color: 'var(--accent)', ds: true, note: N('Official DeepSeek-V4-Pro-0813 model card', 'DeepSeek-V4-Pro-0813 官方模型卡', 'DeepSeek-V4-Pro-0813 官方模型卡') },
        { name: 'Llama 4 Maverick',   l: 'meta',      v: 69.8, color: '#0668E1', note: N('Official Meta card, 0-shot, t=0', 'Meta 官方卡，0-shot，t=0', 'Meta 官方卡，0-shot，t=0') },
        { name: 'Mistral Large 3',    l: 'mistral',   v: 67.2, color: '#FF8A00', note: N('Official card, 5-shot no-CoT; vals.ai run 68.43', '官方卡，5-shot 无 CoT；vals.ai 跑分 68.43', '官方卡，5-shot 無 CoT；vals.ai 跑分 68.43') }
      ]
    },
    {
      name: 'MMLU-Pro',
      hint: N('no lab publishes this on their card; all figures third-party', '各实验室均未在官方卡发布此项，全部为第三方数据', '各實驗室均未在官方卡發布此項，全部為第三方數據'),
      models: [
        { name: 'Claude Fable 5',     l: 'anthropic', v: 91.5, color: '#D97757', note: N('vals.ai MMLU-Pro leaderboard, Aug 2026', 'vals.ai MMLU-Pro 榜单，2026 年 8 月', 'vals.ai MMLU-Pro 榜單，2026 年 8 月') },
        { name: 'Gemini 3.1 Pro',     l: 'google',    v: 91.0, color: '#F4B400', note: N('hokai.io run (official card has MMMU-Pro 80.5, different test)', 'hokai.io 跑分（官方卡发布的是 MMMU-Pro 80.5，属不同测试）', 'hokai.io 跑分（官方卡發布的是 MMMU-Pro 80.5，屬不同測試）') },
        { name: 'Grok 4.6',           l: 'grok',      v: 89.4, color: '#B8C4DE', note: N('vals.ai independent run (Aug 2026, ±0.30)', 'vals.ai 独立跑分（2026 年 8 月，±0.30）', 'vals.ai 獨立跑分（2026 年 8 月，±0.30）') },
        { name: 'GPT-5.6 Sol',        l: 'openai',    v: 89.1, color: '#10A37F', note: N('vals.ai run (Aug 2026); not published by OpenAI', 'vals.ai 跑分（2026 年 8 月）；OpenAI 未官方发布', 'vals.ai 跑分（2026 年 8 月）；OpenAI 未官方發布') },
        { name: 'Qwen3.8-Max',        l: 'qwen',      v: 88.6, color: '#00B4D8', note: N('vals.ai run (Aug 2026, 5-shot CoT)', 'vals.ai 跑分（2026 年 8 月，5-shot CoT）', 'vals.ai 跑分（2026 年 8 月，5-shot CoT）') },
        { name: 'Kimi K3',            l: 'kimi',      v: 88.0, color: '#6C8CFF', note: N('vals.ai run (Aug 2026, max reasoning)', 'vals.ai 跑分（2026 年 8 月，最高推理）', 'vals.ai 跑分（2026 年 8 月，最高推理）') },
        { name: 'DeepSeek V4 Pro',    l: 'ds',        v: 87.5, color: 'var(--accent)', ds: true, note: N('Official DeepSeek-V4-Pro-0813 model card', 'DeepSeek-V4-Pro-0813 官方模型卡', 'DeepSeek-V4-Pro-0813 官方模型卡') },
        { name: 'GLM-5.2',            l: 'glm',       v: 86.7, color: '#8B5CF6', note: N('vals.ai run (Jun 2026, ±0.33)', 'vals.ai 跑分（2026 年 6 月，±0.33）', 'vals.ai 跑分（2026 年 6 月，±0.33）') },
        { name: 'Llama 4 Maverick',   l: 'meta',      v: 80.5, color: '#0668E1', note: N('Official Meta card, 0-shot, t=0', 'Meta 官方卡，0-shot，t=0', 'Meta 官方卡，0-shot，t=0') },
        { name: 'Mistral Large 3',    l: 'mistral',   v: 79.8, color: '#FF8A00', note: N('vals.ai run (Dec 2025, ±0.47)', 'vals.ai 跑分（2025 年 12 月，±0.47）', 'vals.ai 跑分（2025 年 12 月，±0.47）') }
      ]
    },
    {
      name: 'Terminal-Bench',
      hint: N('versions vary (1.0–3.0) — not directly comparable', '版本不一（1.0–3.0）——不可直接比较', '版本不一（1.0–3.0）——不可直接比較'),
      models: [
        { name: 'GPT-5.6 Sol',        l: 'openai',    v: 88.8, color: '#10A37F', note: N('Terminal-Bench 2.1, official card, max reasoning, single agent', 'Terminal-Bench 2.1，官方卡，最高推理，单智能体', 'Terminal-Bench 2.1，官方卡，最高推理，單智能體') },
        { name: 'Kimi K3',            l: 'kimi',      v: 88.3, color: '#6C8CFF', note: N('Terminal-Bench 2.1, official technical report, Kimi Code harness', 'Terminal-Bench 2.1，官方技术报告，Kimi Code 工具链', 'Terminal-Bench 2.1，官方技術報告，Kimi Code 工具鏈') },
        { name: 'DeepSeek V4 Pro',    l: 'ds',        v: 87.9, color: 'var(--accent)', ds: true, note: N('Terminal-Bench 2.1, official model card', 'Terminal-Bench 2.1，官方模型卡', 'Terminal-Bench 2.1，官方模型卡') },
        { name: 'Qwen3.8-Max',        l: 'qwen',      v: 86.6, color: '#00B4D8', note: N('Terminal-Bench 2.1, official card, Claude Code harness; vals.ai run 67.4', 'Terminal-Bench 2.1，官方卡，Claude Code 工具链；vals.ai 跑分 67.4', 'Terminal-Bench 2.1，官方卡，Claude Code 工具鏈；vals.ai 跑分 67.4') },
        { name: 'Claude Fable 5',     l: 'anthropic', v: 84.3, color: '#D97757', note: N('Terminal-Bench 2.1, official system card (safety fallback drags it down)', 'Terminal-Bench 2.1，官方系统卡（安全回退拉低分数）', 'Terminal-Bench 2.1，官方系統卡（安全回退拉低分數）') },
        { name: 'GLM-5.2',            l: 'glm',       v: 81.0, color: '#8B5CF6', note: N('Terminal-Bench 2.1, official card, Terminus-2 harness', 'Terminal-Bench 2.1，官方卡，Terminus-2 工具链', 'Terminal-Bench 2.1，官方卡，Terminus-2 工具鏈') },
        { name: 'Gemini 3.1 Pro',     l: 'google',    v: 70.7, color: '#F4B400', note: N('Terminal-Bench 2.1, tbench.ai leaderboard, best harness', 'Terminal-Bench 2.1，tbench.ai 榜单，最佳工具链', 'Terminal-Bench 2.1，tbench.ai 榜單，最佳工具鏈') },
        { name: 'Grok 4.6',           l: 'grok',      v: 26.0, color: '#B8C4DE', note: N('Terminal-Bench v3.0, official xAI launch table — a newer, harder version', 'Terminal-Bench v3.0，xAI 官方发布表——更新、更难的版本', 'Terminal-Bench v3.0，xAI 官方發布表——更新、更難的版本') },
        { name: 'Llama 4 Maverick',   l: 'meta',      v: 15.5, color: '#0668E1', note: N('Terminal-Bench 1.0, tbench.ai leaderboard (May 2025) — older, easier version', 'Terminal-Bench 1.0，tbench.ai 榜单（2025 年 5 月）——更旧、更易的版本', 'Terminal-Bench 1.0，tbench.ai 榜單（2025 年 5 月）——更舊、更易的版本') },
        { name: 'Mistral Large 3',    l: 'mistral',   v: 9.0,  color: '#FF8A00', note: N('Terminal-Bench 2.0, vals.ai leaderboard (Jun 2026)', 'Terminal-Bench 2.0，vals.ai 榜单（2026 年 6 月）', 'Terminal-Bench 2.0，vals.ai 榜單（2026 年 6 月）') }
      ]
    }
  ];
  const grid = document.querySelector('.compare-grid');
  if (!grid || !COMPARE.length) return;
  const io = new IntersectionObserver(function(entries) {
    entries.forEach(function(en) {
      if (!en.isIntersecting) return;
      en.target.classList.add('entered');
      io.unobserve(en.target);
    });
  }, { threshold: 0.25 });
  function renderCompare() {
    grid.innerHTML = '';
    COMPARE.forEach(function(b) {
      const card = document.createElement('div');
      card.className = 'compare-card';
      const h = document.createElement('h3');
      h.textContent = b.name;
      if (b.hint) {
        const hint = document.createElement('span');
        hint.className = 'compare-hint';
        hint.textContent = window.__i18n.t(b.hint);
        h.appendChild(hint);
      }
      card.appendChild(h);
      const sorted = b.models.slice().sort(function(a, b) {
        const av = (a.v == null) ? -1 : a.v;
        const bv = (b.v == null) ? -1 : b.v;
        return bv - av; // highest first; unpublished (—) sink to the bottom
      });
      sorted.forEach(function(m) {
        const row = document.createElement('div');
        row.className = 'compare-row' + (m.ds ? ' is-ds' : '');
        const img = document.createElement('img');
        const lref = m.l ? L[m.l] : null;
        img.className = 'compare-logo' + (lref && lref.inv ? ' logo-invert' : '');
        img.src = lref ? lref.logo : m.logo; img.alt = m.name;
        // Logos are inlined data URIs (already in the HTML), so eager avoids a
        // decode flash when the compare grid scrolls into view.
        img.loading = 'eager';
        const name = document.createElement('span');
        name.className = 'compare-name';
        name.textContent = m.name;
        if (m.ds) {
          const badge = document.createElement('span');
          badge.className = 'compare-badge';
          badge.textContent = window.__i18n.fmt('cmp_rank', { n: sorted.indexOf(m) + 1 });
          name.appendChild(badge);
        }
        const track = document.createElement('div');
        track.className = 'compare-track';
        const bar = document.createElement('div');
        bar.className = 'compare-bar';
        bar.style.setProperty('--bar-color', m.color);
        // Bar length equals the displayed score: 96.2% renders as 96.2% of the
        // track, so the full track always means 100 — not the top score.
        bar.style.setProperty('--bar-ratio', m.v == null ? '0' : Math.min(1, Math.max(0.02, m.v / 100)).toFixed(4));
        track.appendChild(bar);
        const score = document.createElement('span');
        score.className = 'compare-score';
        if (m.v == null) {
          score.textContent = '—';      // lab didn't publish this benchmark
          bar.style.opacity = '0.12';
        } else {
          score.textContent = m.fmt === 'elo'
            ? m.v.toLocaleString('en-US') + ' Elo'
            : (m.fmt === 'int' ? m.v.toFixed(0) + '%' : m.v.toFixed(1) + '%');
        }
        if (m.note) { score.title = window.__i18n.t(m.note); }
        row.append(img, name, track, score);
        card.appendChild(row);
      });
      grid.appendChild(card);
    });
    // Bars scale in when the card scrolls into view
    grid.querySelectorAll('.compare-card').forEach(function(c) { io.observe(c); });
  }
  window.__compareRender = renderCompare;
  renderCompare();
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
      if (i === idx) s.setAttribute('data-state', 'active');
      else if (i < idx) s.setAttribute('data-state', 'done');
      else s.setAttribute('data-state', 'upcoming');
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

// ===== Theme Toggle =====
(function() {
  const btn = document.getElementById('theme-toggle');
  const html = document.documentElement;
  // restore saved preference (or system preference)
  try {
    const saved = localStorage.getItem('ds-theme');
    const pref = saved || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    html.setAttribute('data-theme', pref);
  } catch (e) {}
  if (!btn) return;
  btn.addEventListener('click', function() {
    const cur = html.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    const next = cur === 'dark' ? 'light' : 'dark';
    // add transition class briefly for the smooth cross-fade
    html.classList.add('theme-anim');
    void document.body.offsetHeight;  // force a style flush so the cross-fade actually starts
    html.setAttribute('data-theme', next);
    window.dispatchEvent(new CustomEvent('themechange'));
    try { localStorage.setItem('ds-theme', next); } catch (e) {}
    setTimeout(function() { html.classList.remove('theme-anim'); }, 600);
  });
})();

// ===== Language switcher + initial apply =====
(function() {
  // Apply the saved language on load (skip 'en' — that is the baked-in default)
  if (__I18N_LANG !== 'en') window.__i18n.apply(__I18N_LANG);
  const sw = document.getElementById('lang-switch');
  if (!sw) return;
  const trig = document.getElementById('lang-trigger');
  const menu = document.getElementById('lang-menu');
  function close() {
    sw.classList.remove('open');
    trig.setAttribute('aria-expanded', 'false');
  }
  trig.addEventListener('click', function(e) {
    e.stopPropagation();
    const open = sw.classList.toggle('open');
    trig.setAttribute('aria-expanded', String(open));
  });
  menu.addEventListener('click', function(e) {
    const btn = e.target.closest('.lang-option');
    if (!btn) { close(); return; }
    if (!btn.classList.contains('is-current')) {
      window.__i18n.apply(btn.getAttribute('data-lang'));
    }
    close();
  });
  document.addEventListener('click', function(e) {
    if (!sw.contains(e.target)) close();
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') close();
  });
  menu.addEventListener('keydown', function(e) {
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
    e.preventDefault();
    const opts = Array.prototype.slice.call(menu.querySelectorAll('.lang-option'));
    const idx = opts.indexOf(document.activeElement);
    const next = (idx + (e.key === 'ArrowDown' ? 1 : opts.length - 1)) % opts.length;
    opts[next].focus();
  });
})();

// ===== Service Worker (offline / PWA) =====
if ('serviceWorker' in navigator && location.protocol.startsWith('http')) {
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
PAGE = PAGE.replace('__WHALE_PATH__', whale_path)
PAGE = PAGE.replace('DATAURI_DEEPSEEK_LOGO', DS_LOGO_DATA)
for _k, _v in LOGO_URIS.items():
    _PH = 'LOGO_URI_' + _k.upper()
    if _v is not None:
        PAGE = PAGE.replace(_PH, _v)
    else:
        print('WARN: assets/logos missing for %s, keeping remote URL placeholder' % _k, file=sys.stderr)
PAGE = PAGE.replace('__FONTS_CSS__', FONT_CSS)
PAGE = PAGE.replace('__I18N_JSON__', json.dumps(I18N, ensure_ascii=False))

open(BASE + 'index.html', 'w', encoding='utf-8').write(PAGE)
print('index.html written:', len(PAGE), 'chars')

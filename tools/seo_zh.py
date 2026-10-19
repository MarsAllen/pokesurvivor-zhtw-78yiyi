# 繁中說明頁（zh/）：本 fork 新增（P4-01），由 tools/make_seo_pages.py 最後呼叫 run()。
#   node tools/export_data.js && python tools/make_seo_pages.py
# 說明文字直接用中文寫在這裡；遊戲資料（寶可夢、招式、道具、屬性、成就…）用遊戲本身的繁中字典
# （export_data.js 匯出的 zh，來源是 lang-zh-names.js、lang-zh.js、lang-fork.js）翻譯。
# FAQ 與最新消息以上游的西文標題對應：上游新增或改了標題，執行時會列在「缺少繁中」裡。
import re

M = None          # make_seo_pages 模組（run() 設定）
missing = []
PATS = []

def zh(s):
    Z = M.D['zh']
    if not re.search(r'[^\W\d_]', s): return s      # 數字、符號：原樣（和遊戲的 i18n 一樣）
    if s in Z: return Z[s]
    for rx, v in PATS:
        m = rx.match(s)
        if m:
            g = iter(m.groups())
            return re.sub(r'\{x\}', lambda _: zh(next(g)), v)
    if s not in missing: missing.append(s)
    return M.en(s)

def esc(s): return M.esc(s)
def name(d): return zh(M.BY[d]['name'])
def tname(t): return zh(M.TN.get(t, t))
def tbadge(t): return f'<i class="ty" style="background:{M.TC.get(t, "#888")}">{esc(tname(t))}</i>'
def sprite(d, shiny=False, up='../'):
    return M.sprite(d, shiny, up=up).replace(f'alt="{esc(M.BY[d]["name"])}', f'alt="{esc(name(d))}')
def lk(pid, to): return M.rel(M.PATH['zh'][pid], M.PATH['zh'][to])
def cta(pid, text): return M.cta(pid, 'zh', text)
def write(pid, title, desc, body, ld=None): M.write(pid, 'zh', page(pid, title, desc, body, ld))
def crumbs(pid, h1): return {'@context': 'https://schema.org', '@graph': [M.crumbs(pid, 'zh', h1)]}

NAV = [('guide', '指南'), ('pokedex', '圖鑑'), ('legends', '傳說'), ('moves', '招式'), ('types', '屬性')]
FOOT = [('guide', '遊戲指南'), ('pokedex', '寶可夢圖鑑'), ('legends', '傳說寶可夢與競技場'), ('shinies', '異色寶可夢'), ('types', '屬性相剋表'),
        ('moves', '招式'), ('items', '攜帶道具'), ('achievements', '成就'), ('news', '最新消息'), ('support', '支持原作者')]

def page(pid, title, desc, body, ld=None):
    SITE, PATH = M.SITE, M.PATH
    me = PATH['zh'][pid]
    up = '../' * me.count('/')
    nav = ''.join(f'<a href="{lk(pid, p)}">{esc(t)}</a>' for p, t in NAV)
    foot = ' · '.join(f'<a href="{lk(pid, p)}">{esc(t)}</a>' for p, t in FOOT)
    other = M.rel(me, PATH['en'][pid])
    legal = ('PokéSurvivor 是<b>免費、非營利</b>的同人遊戲，沒有廣告也沒有內購。與任天堂、Creatures、GAME FREAK 及 The Pokémon Company 無關；'
             '寶可夢及其角色的權利屬於各自的權利人。角色圖：PMD SpriteCollab（CC BY-NC 4.0）· 資料：PokéAPI · 音樂與音效為原作原創。'
             '遊戲沒有任何官方加密貨幣或代幣，使用遊戲名稱的代幣都與本遊戲無關。'
             '原作程式碼採用 PolyForm Noncommercial 1.0.0 授權（Copyright 2026 JPTER78）。'
             '這個繁體中文版由 78yiyi 製作，<b>不收取任何費用</b>；官方網站只有 pokesurvivor.com。')
    fork = ('這是 78yiyi 製作的 PokéSurvivor <b>繁體中文非官方版</b>，與原作者無關。官方網站：'
            '<a href="https://pokesurvivor.com/">pokesurvivor.com</a>。')
    code = (f'<a href="https://github.com/JPTER78/pokesurvivor">原作程式碼（JPTER78）</a> · '
            f'<a href="{M.FORK_REPO}">本版本（78yiyi）</a> · <a href="{M.FORK_REPO}/issues">回報問題</a>')
    ldj = ('<script type="application/ld+json">\n' + M.json.dumps(ld, ensure_ascii=False) + '\n</script>') if ld else ''
    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{SITE}{me}">
<meta name="theme-color" content="#0a1430">
<meta property="og:type" content="website">
<meta property="og:site_name" content="PokéSurvivor 繁中非官方版">
<meta property="og:locale" content="zh_TW">
<meta property="og:url" content="{SITE}{me}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{up}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="48x48" href="{up}assets/icons/icon-48.png">
<link rel="icon" type="image/png" sizes="96x96" href="{up}assets/icons/icon-96.png">
<link rel="icon" type="image/png" sizes="144x144" href="{up}assets/icons/icon-144.png">
<link rel="apple-touch-icon" href="{up}assets/icons/icon-180.png">
<link rel="stylesheet" href="{up}css/pages.css">
{ldj}
</head>
<body>
<header class="top">
  <a class="brand" href="{lk(pid, 'home')}">PokéSurvivor</a>
  <nav>{nav}<a class="lang" hreflang="en" href="{other}">English</a><a class="play" href="{lk(pid, 'home')}">免費開玩</a></nav>
</header>
<main>
<p class="lead" style="max-width:820px;margin:0 auto 14px;font-size:15px;text-align:center">{fork}</p>
{body}
</main>
<footer>
  <p>{foot}</p>
  <p>{legal}</p>
  <p>{code}</p>
</footer>
</body>
</html>
'''

# ================= 指南 =================
def faq():
    N = M.N
    A = {
     '¿PokéSurvivor es gratis?': ('PokéSurvivor 要錢嗎？', '完全免費。這是非營利的同人遊戲，沒有廣告也沒有內購。原作者接受自願贊助（只用在伺服器上，不會帶來任何遊戲優勢）；這個繁中非官方版不收取任何款項。'),
     '¿Hay que descargar algo?': ('需要下載嗎？', '不用。直接在電腦、平板或手機的瀏覽器裡玩。也可以用「加到主畫面」安裝成 App。'),
     '¿Se puede jugar en el móvil?': ('可以用手機玩嗎？', '可以，請橫向持握。手指放在螢幕任何地方拖曳就能移動（搖桿會出現在你按下的位置），點招式可以切換，右上角的按鈕可以暫停。'),
     '¿Está en inglés?': ('有中文嗎？', '有。這個版本是繁體中文非官方版，遊戲會依瀏覽器語言顯示繁體中文、英文或西班牙文，也可以在「設定」裡切換。'),
     '¿Puedo jugar con mis amigos?': ('可以和朋友一起玩嗎？', '可以，線上組隊最多 4 人。用暱稱加好友，邀請他們進你的房間就能開始。經驗值大家共用，隊友倒下時站在他旁邊就能把他救起來。'),
     '¿Cuántos Pokémon hay?': ('有幾隻寶可夢？', f'9 個地區（從{zh("Kanto")}到{zh("Paldea")}）共 {N} 隻寶可夢，全部都能當夥伴；有異色的，也能用異色版遊玩。'),
     '¿Cómo consigo más Pokémon?': ('怎麼取得更多寶可夢？', '用扭蛋。扭蛋要用遊玩時賺到的獎券來抽：一般寶可夢偶爾會掉落獎券，首領和裂縫中的傳說寶可夢有時會給 ×10 獎券。獎券不能用真錢購買。'),
     '¿Qué son las grietas?': ('裂縫是什麼？', '偶爾才會出現的神祕傳送門。走進去就會在該屬性的競技場（共 18 種）和一隻傳說寶可夢對戰。贏了有獎勵；倒下就回到原本的地圖。'),
     '¿Se guarda mi progreso?': ('進度會保存嗎？', '用帳號（名稱＋密碼，或 Google）登入，進度會存在雲端，在任何裝置都能繼續。訪客可以馬上開始玩，但進度不會保存。'),
     '¿Es un juego oficial de Pokémon?': ('這是寶可夢官方遊戲嗎？', '不是。這是免費、非營利的同人專案，與任天堂、GAME FREAK 和 The Pokémon Company 無關。這個繁體中文版也不是原作者製作的，而是 78yiyi 製作的非官方版本。'),
    }
    out = []
    for q, _ in M.FAQ['es']:
        if q in A: out.append(A[q])
        elif 'FAQ: ' + q not in missing: missing.append('FAQ: ' + q)
    return out

def guide():
    pid, N = 'guide', M.N
    na = len(M.D['achievements'])
    qa = faq()
    body = f'''<article class="doc">
<h1>PokéSurvivor 遊戲指南</h1>
<p class="lead">PokéSurvivor 是一款<b>寶可夢生存遊戲</b>，玩法類似《Survivor.io》和《吸血鬼倖存者》（Vampire Survivors），在瀏覽器裡就能免費玩：
選一隻夥伴，在無限延伸的地圖上移動，招式會自動施放，同時要躲開一波波包圍你的野生寶可夢。你能撐多久？</p>
{cta(pid, '立即免費開玩')}
<h2>怎麼玩</h2>
<ul>
<li><b>電腦：</b>用 <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> 或方向鍵移動。用 <kbd>1</kbd>–<kbd>4</kbd>、<kbd>Q</kbd>/<kbd>E</kbd> 或點圖示切換招式。按 <kbd>Esc</kbd> 暫停。</li>
<li><b>手機或平板（橫向）：</b>在螢幕任何地方拖曳手指就能移動，點招式切換，右上角的按鈕暫停。</li>
<li>你的寶可夢會用目前的招式<b>自動攻擊</b>，你只要負責閃避和走位。</li>
<li>收集經驗值就能<b>升級</b>，從三張卡片中選一張：學新的<a href="{lk(pid, 'moves')}">招式</a>、強化已有的招式，或強化你的寶可夢。</li>
</ul>
<h2>遊戲特色</h2>
<ul class="feat">
<li><b>9 個地區共 {N} 隻寶可夢</b>（<a href="{lk(pid, 'pokedex')}">看圖鑑</a>），每隻都有自己的招式和永久強化。</li>
<li><b>招式會進化</b>：升到最高等級並拿到對應的強化卡，{zh('Ascuas')}會變成{zh('Llamarada')}、{zh('Burbuja')}會變成{zh('Surf')}…</li>
<li><b>有個性的敵人</b>：有的會治療、替同伴張開護盾、呼叫支援、自爆，或在地上預警後發射光束。</li>
<li><b>首領</b>和<a href="{lk(pid, 'legends')}"><b>裂縫</b>：18 個傳說競技場</a>，每種屬性一個。</li>
<li><a href="{lk(pid, 'types')}"><b>天氣與屬性相剋</b></a>：下雨時水屬性變強、火屬性變弱；還有大晴天、沙暴、下雪和起霧。</li>
<li>野生的<a href="{lk(pid, 'shinies')}"><b>異色寶可夢</b></a>（4096 分之 1），扭蛋也抽得到。</li>
<li>每個地區都有<b>拉霸機造型的扭蛋</b>，用遊玩時賺到的獎券來抽。</li>
<li><a href="{lk(pid, 'items')}"><b>攜帶道具</b></a>，例如{zh('Restos')}、{zh('Cinta Elección')}、{zh('Vidasfera')}。</li>
<li>和好友<b>最多 4 人線上組隊</b>。</li>
<li>每日與每週<b>任務</b>、<a href="{lk(pid, 'achievements')}"><b>{na} 個成就</b></a>（獎牌與稱號）、公開個人檔案和排行榜。</li>
<li>支援<b>繁體中文、英文、西班牙文</b>，電腦和手機都能玩，也能<b>安裝成 App</b>。</li>
</ul>
<h2>撐得更久的訣竅</h2>
<ol>
<li>不要站著不動：繞大圈移動，讓怪物群排成一列跟在你後面。</li>
<li>善用屬性相剋：切換成對眼前敵人效果絕佳的招式。</li>
<li>地上的預警（逐漸填滿的圓圈和線條）代表攻擊快要落下：趕快離開。</li>
<li>優先打倒會治療或張護盾的寶可夢。</li>
<li>把金幣花在你最喜歡的夥伴的強化上。</li>
</ol>
<h2>常見問題</h2>
{''.join(f'<h3>{esc(q)}</h3><p>{esc(a)}</p>' for q, a in qa)}
{cta(pid, '開始玩 PokéSurvivor')}
</article>'''
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'FAQPage', 'inLanguage': 'zh-Hant', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in qa]},
        M.crumbs(pid, 'zh', '指南')]}
    write(pid, 'PokéSurvivor 遊戲指南：玩法、訣竅與常見問題（繁中非官方版）',
          f'PokéSurvivor 在電腦和手機上怎麼玩、遊戲特色（{N} 隻寶可夢、線上組隊、傳說裂縫、扭蛋）、撐得更久的訣竅與常見問題。', body, ld)

# ================= 圖鑑 =================
def dexcard(e, up):
    d = e['dex']
    tag = '<b class="leg">傳說</b>' if d in M.LEG else ('<b class="st">初始</b>' if e.get('starter') else '')
    return (f'<li id="p{d}">{sprite(d, up=up)}<span class="n">#{d:03d}</span><span class="nm">{esc(name(d))}</span>'
            f'<span class="tys">{"".join(tbadge(t) for t in e.get("types", []))}</span>{tag}</li>')

def pokedex():
    pid, N = 'pokedex', M.N
    up = M.upof(pid, 'zh')
    secs = []
    for g in range(1, 10):
        mons = [e for e in M.DEX if e.get('gen') == g]
        gid = M.gen_name(g, 'en').lower()
        secs.append(f'<section id="{gid}"><h2>{zh(M.gen_name(g, "es"))} <small>（第 {g} 世代 · {len(mons)} 隻）</small></h2>'
                    f'<ul class="dexgrid">{"".join(dexcard(e, up) for e in mons)}</ul></section>')
    gens = ''.join(f'<a href="#{M.gen_name(g, "en").lower()}">{zh(M.gen_name(g, "es"))}</a>' for g in range(1, 10))
    h1 = f'PokéSurvivor 寶可夢圖鑑：{N} 隻可以玩的寶可夢'
    lead = (f'這些寶可夢都能在 PokéSurvivor 裡當你的夥伴。這是一款能在瀏覽器和手機上免費玩的寶可夢生存遊戲，收錄 9 個地區共 {N} 隻；'
            f'可以選作初始夥伴，或用扭蛋（遊玩時賺到的獎券）取得，牠們也會以野生敵人、首領和裂縫中的傳說寶可夢登場。')
    body = f'<article class="doc wide"><h1>{esc(h1)}</h1><p class="lead">{esc(lead)}</p><nav class="gens">{gens}</nav>{"".join(secs)}{cta(pid, "選擇你的夥伴，免費開玩")}</article>'
    ld = {'@context': 'https://schema.org', '@graph': [{'@type': 'CollectionPage', 'name': h1, 'url': M.SITE + M.PATH['zh'][pid], 'inLanguage': 'zh-Hant'},
                                                        M.crumbs(pid, 'zh', '寶可夢圖鑑')]}
    write(pid, f'PokéSurvivor 寶可夢圖鑑：{N} 隻可玩寶可夢（9 個地區）',
          f'PokéSurvivor 可以使用的 {N} 隻寶可夢完整列表，從{zh("Kanto")}到{zh("Paldea")}，附屬性。免費的瀏覽器寶可夢遊戲。', body, ld)

# ================= 傳說寶可夢與競技場 =================
def legends():
    pid = 'legends'
    up = M.upof(pid, 'zh')
    nl = len(M.LEG)
    cards = ''.join(dexcard(M.BY[d], up) for d in sorted(M.LEG))
    ar = ''.join(f'<li>{tbadge(t)} <b>{esc(zh(M.D["arenas"][t]))}</b></li>' for t in M.TYPES if t in M.D['arenas'])
    h1 = '傳說寶可夢與裂縫：PokéSurvivor 的 18 個競技場'
    body = (f'<article class="doc wide"><h1>{esc(h1)}</h1>'
            '<p class="lead">地圖上偶爾會打開一道<b>神祕的裂縫</b>。走進去就會在該屬性的競技場裡對上一隻<b>傳說寶可夢</b>，每個競技場都有自己的地形和天氣。'
            '贏了有機會拿到扭蛋用的 <b>×10 獎券</b>；倒下就沒有獎勵，回到原本的地圖。組隊時大家會一起進去。</p>'
            f'<h2>18 個競技場，每種屬性一個</h2><ul class="arenas">{ar}</ul>'
            '<p>有兩種屬性的傳說寶可夢，會隨機用其中一種屬性的競技場。地形也有影響：岩漿會灼傷、冰面會打滑、水會讓你變慢…</p>'
            f'<h2>{nl} 隻傳說寶可夢</h2><ul class="dexgrid">{cards}</ul>{cta(pid, "去找裂縫：免費開玩")}</article>')
    write(pid, 'PokéSurvivor 傳說寶可夢與裂縫：18 個屬性競技場',
          f'PokéSurvivor 的裂縫怎麼運作、18 個傳說競技場（每種屬性一個），以及能挑戰的 {nl} 隻傳說寶可夢。', body, crumbs(pid, h1))

# ================= 異色寶可夢 =================
def shinies():
    pid, N = 'shinies', M.N
    up = M.upof(pid, 'zh')
    pairs = ''.join(f'<li><span class="pair">{sprite(d, up=up)}{sprite(d, True, up=up)}</span><span class="nm">{esc(name(d))}</span></li>'
                    for d in M.SHOW if M.META.get(d, {}).get('sh'))
    h1 = 'PokéSurvivor 的異色寶可夢：怎麼取得'
    body = f'''<article class="doc wide"><h1>{h1}</h1>
<p class="lead"><b>異色</b>寶可夢是顏色不同的稀有版本。PokéSurvivor 裡幾乎所有 {N} 隻寶可夢都有異色版，而且是真正的異色角色圖。</p>
<h2>怎麼取得</h2>
<ul><li><b>野生：</b>每隻出現的寶可夢都有 <b>4096 分之 1</b> 的機率是異色（和經典作品一樣）。你會看到牠閃閃發光並跳出提示：打倒牠就是你的了。</li>
<li><b>扭蛋：</b>每一抽都有 <b>100 分之 1</b> 的機率是異色。</li>
<li>抽到重複的異色寶可夢，會得到三倍的寶可金幣。</li>
<li>擁有夥伴的異色版之後，就能用異色版遊玩（在收藏裡選擇）。</li></ul>
<h2>一般與異色</h2><ul class="dexgrid pairs">{pairs}</ul>{cta(pid, '出發尋找異色寶可夢')}</article>'''
    write(pid, 'PokéSurvivor 異色寶可夢：機率與取得方式',
          '在 PokéSurvivor 取得異色寶可夢的方法：野生 4096 分之 1、扭蛋 100 分之 1。一般與異色外觀對照。', body, crumbs(pid, h1))

# ================= 屬性相剋表 =================
def types_page():
    pid = 'types'
    TYPES, TC, X = M.TYPES, M.TC, M.D['matrix']
    def cell(v):
        cls = 'x16' if v > 1.05 else ('x03' if v < 0.35 else ('x06' if v < 0.95 else ''))
        return f'<td class="{cls}">{"×" + f"{v:g}" if cls else ""}</td>'
    head = ''.join(f'<th class="vt" title="{esc(tname(t))}"><span style="background:{TC[t]}">{esc(tname(t))}</span></th>' for t in TYPES)
    rows = ''.join(f'<tr><th>{tbadge(a)}</th>{"".join(cell(X[a][d]) for d in TYPES)}</tr>' for a in TYPES)
    table = f'<div class="tablewrap"><table class="chart" id="chart"><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
    script = '''<script>
document.querySelectorAll('#chart td').forEach(td => {
  td.onmouseenter = () => { const r = td.parentElement, i = [...r.children].indexOf(td);
    document.querySelectorAll('#chart tr').forEach(tr => tr.children[i] && tr.children[i].classList.add('hl')); r.classList.add('hl'); };
  td.onmouseleave = () => document.querySelectorAll('#chart .hl').forEach(e => e.classList.remove('hl'));
});
</script>'''
    T = lambda *ts: '、'.join(tname(t) for t in ts)
    h1 = 'PokéSurvivor 屬性相剋表'
    intro = ('<p class="lead">和本傳遊戲相同的屬性相剋，但為了生存遊戲<b>調整得比較溫和</b>（你一次只用一個招式，也不能換寶可夢）：'
             '效果絕佳是 <b>×1.6</b>，效果不好是 <b>×0.6</b>，沒有效果則變成 <b>×0.3</b>。雙屬性會相乘（上限 ×2.4）。'
             '雙向都適用：你攻擊敵人和敵人攻擊你都一樣。</p><p>橫列：攻擊招式的屬性 · 直行：被攻擊的寶可夢的屬性。</p>')
    wx = (f'<h2>天氣也有影響</h2><ul><li><b>下雨：</b>{T("water")}屬性增強，{T("fire")}屬性減弱。</li><li><b>大晴天：</b>{T("fire")}屬性增強，{T("water")}屬性減弱。</li>'
          f'<li><b>沙暴：</b>{T("rock", "ground", "steel")}屬性增強，其他屬性會受到傷害。</li><li><b>下雪：</b>{T("ice")}屬性增強，其他屬性會受到傷害並變慢。</li>'
          f'<li><b>起霧：</b>{T("ghost", "fairy", "psychic")}屬性增強。</li></ul>')
    body = f'<article class="doc wide"><h1>{h1}</h1>{intro}{table}{wx}{cta(pid, "實際試試看：免費開玩")}</article>{script}'
    write(pid, 'PokéSurvivor 屬性相剋表（互動式）與天氣效果',
          'PokéSurvivor 互動式屬性相剋表：18 種屬性的 ×1.6／×0.6／×0.3 倍率，以及下雨、大晴天、沙暴、下雪、起霧對戰鬥的影響。', body, crumbs(pid, h1))

# ================= 招式 =================
KIND = {'projectile': '投射', 'melee': '近戰', 'beam': '光束', 'orbit': '環繞', 'nova': '爆發', 'aura': '光環', 'buff': '增益',
        'boomerang': '迴旋', 'chain': '連鎖', 'mine': '地雷', 'meteor': '流星', 'turret': '砲台', 'dash': '衝刺', 'trail': '軌跡', 'cone': '扇形'}

def moves_page():
    pid = 'moves'
    rows = []
    for t in M.TYPES:
        for m in [x for x in M.D['moves'] if x['type'] == t]:
            evo = m['evo']
            evo_txt = f'<b>{esc(zh(evo["name"]))}</b><small>需要 {esc(zh(evo["needs"]))} · {esc(zh(evo["text"]))}</small>' if evo else '—'
            rows.append(f'<tr><td><b>{esc(zh(m["name"]))}</b></td><td>{tbadge(t)}</td><td>{KIND.get(m["kind"], m["kind"])}</td>'
                        f'<td>{esc(zh(m["desc"]))}</td><td class="evo">{evo_txt}</td></tr>')
    nm, nevo = len(M.D['moves']), sum(1 for m in M.D['moves'] if m['evo'])
    h1 = 'PokéSurvivor 的招式與進化'
    intro = (f'<p class="lead">共有 <b>{nm} 個招式</b>，涵蓋 18 種屬性。你的寶可夢會用目前的招式自動攻擊，升級時可以選卡片學新招式，或把招式強化到 5 級。'
             f'<b>其中 {nevo} 個可以進化</b>：升到最高等級、拿到它要求的強化卡（{zh("Potencia")}、{zh("Vigor")}、{zh("Reflejos")}…），就會出現金色的進化卡。</p>')
    th = '<th>招式</th><th>屬性</th><th>類型</th><th>效果</th><th>進化成</th>'
    body = f'<article class="doc wide"><h1>{h1}</h1>{intro}<div class="tablewrap"><table class="list"><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>{cta(pid, "免費開玩試試看")}</article>'
    write(pid, f'PokéSurvivor 招式列表：{nm} 個招式與進化',
          f'PokéSurvivor 全部 {nm} 個招式（依屬性分類）、各自的效果和進化（{zh("Ascuas")} → {zh("Llamarada")}、{zh("Burbuja")} → {zh("Surf")}…）。', body, crumbs(pid, h1))

# ================= 攜帶道具 =================
def items_page():
    pid = 'items'
    rows = ''.join(f'<li><b>{esc(zh(i["name"]))}</b><span>{esc(zh(i["desc"]))}</span></li>' for i in M.D['items'])
    ni = len(M.D['items'])
    h1 = 'PokéSurvivor 的攜帶道具'
    intro = ('<p class="lead">在一局遊戲中，可以從寶箱和打倒首領時取得<b>攜帶道具</b>。一次只能帶<b>一個</b>：找到新的道具時，可以選擇要留下哪一個。效果持續整局。</p>')
    body = f'<article class="doc"><h1>{h1}</h1>{intro}<ul class="items">{rows}</ul>{cta(pid, "去找道具：免費開玩")}</article>'
    ex = '、'.join(zh(x) for x in ('Restos', 'Cinta Elección', 'Banda Focus', 'Vidasfera'))
    write(pid, f'PokéSurvivor 攜帶道具：全部 {ni} 種', f'PokéSurvivor 的 {ni} 種攜帶道具（{ex}…）與各自的效果。', body, crumbs(pid, h1))

# ================= 成就 =================
def ach_page():
    pid = 'achievements'
    secs = []
    for cid, cname in M.D['achCats'] or []:
        items = [a for a in M.D['achievements'] if a['cat'] == cid]
        if not items: continue
        li = ''.join('<li><b>' + esc(zh(a['name'])) + '</b><span>' + esc(zh(a['desc'])) + '</span>'
                     + ('<em>' + esc(zh(a['title'])) + '</em>' if a['title'] else '') + '</li>' for a in items)
        secs.append(f'<h2>{esc(zh(cname))} <small>（{len(items)}）</small></h2><ul class="items ach">{li}</ul>')
    na = len(M.D['achievements'])
    h1 = f'PokéSurvivor 的 {na} 個成就'
    intro = ('<p class="lead">每個成就都會給你一枚<b>獎牌</b>、一份<b>獎勵</b>（獎券和金幣），最難的還會給你一個顯示在公開個人檔案上的<b>稱號</b>。'
             '每隻傳說寶可夢、收集寶可夢、撐過時間、打倒首領、讓招式進化…都有對應的成就。</p><p>斜體字是可以解鎖的稱號。</p>')
    body = f'<article class="doc wide"><h1>{h1}</h1>{intro}{"".join(secs)}{cta(pid, "開始解鎖成就")}</article>'
    write(pid, f'PokéSurvivor 成就列表：{na} 個成就、獎牌與稱號',
          f'PokéSurvivor 全部 {na} 個成就與獎牌、稱號：收藏、生存、戰鬥、裂縫與傳說寶可夢。', body, crumbs(pid, h1))

# ================= 最新消息 =================
NEWS = {
 'Coloca los botones a tu gusto en el móvil': ('手機按鍵位置自由調整',
  '在「設定 > 操作 > 調整按鍵位置」可以把招式、暫停鍵和搖桿拖到任何位置，也能選擇固定式搖桿。'),
 'La única web oficial es pokesurvivor.com': ('唯一的官方網站是 pokesurvivor.com',
  'PokéSurvivor 現在免費，以後也會免費。如果有其他網站要你為獎券、金幣或任何東西付錢，那不是原作者，而是複製品。從這天起，遊戲程式碼改用非商業授權（PolyForm Noncommercial 1.0.0）。'),
 'Recupera tu cuenta con Gmail': ('用 Gmail 找回帳號',
  '用名稱和密碼遊玩的玩家，現在可以綁定 Gmail：忘記密碼時用 Google 登入，就是同一個帳號。'),
 'La Sentencia de Arceus': ('阿爾宙斯的審判',
  '撐到第 30 分鐘時，阿爾宙斯會從天而降，把你帶到審判遺跡：牠無法被打倒，追你的速度越來越快，而且每 5 秒就會有一隻傳說寶可夢加入，血量和傷害都是前一隻的兩倍。新增三個成就和新音樂，歷來排行榜也重新開始。'),
 'Partidas sin límite, grietas con menos azar y novedades en el juego': ('不限時長的對局、更穩定的裂縫，以及遊戲內的最新消息',
  '修正超過 84 分鐘後畫面變黑或無限升級的錯誤；萬一出問題，遊戲會自動存檔。裂縫至少每 2.5 分鐘出現一次，還沒收集到的傳說寶可夢出現機率更高。治療型敵人的治療量依你的傷害計算，並設有上限。組隊時，房主切換分頁會讓所有人一起暫停。另外修正 iPhone 的問題、在選單加入異色切換、加強近戰招式，並在遊戲內加入「最新消息」按鈕。'),
 'Vínculos: fusiona movimientos al vencer legendarios': ('羈絆：打倒傳說寶可夢就能融合招式',
  '在裂縫中每打倒一隻傳說寶可夢，就會得到一個羈絆：把兩個招式連在一起同時施放、只占一個欄位；之後每打倒一隻傳說寶可夢就再多一個，最多同時 4 個，這樣就有空間學更多招式。另外，裂縫出現得更頻繁了。'),
 'Jefes con varios ataques, 8 tipos de movimiento nuevos y más reto': ('首領有多種攻擊、8 種新招式類型，難度提高',
  '首領和傳說寶可夢有 4 種會先預警的攻擊，會逼近或從遠處攻擊，血量剩一半時會暴怒。新增 12 個招式和 8 種攻擊方式：迴旋、連鎖、地雷、流星、砲台、衝刺、軌跡和扇形。敵人變少但變強，對局中途會有事件（單一屬性的怪物群、黃金時間、迷路的寶可夢），還有帶著滿滿金幣逃跑的喵喵；水屬性寶可夢游泳不會減速，排行榜也加入了防作弊。'),
 'Móvil, inglés y ajustes': ('手機版、英文版與設定',
  '現在可以在手機和平板上用觸控搖桿遊玩，支援西班牙文和英文，也能安裝成 App。新增設定畫面，可以自動調整畫質；畫面上的敵人變少但變強。'),
 'Misiones, logros y enemigos con personalidad': ('任務、成就與有個性的敵人',
  '每日與每週任務、127 個有獎牌和稱號的成就、公開個人檔案、攜帶道具、招式進化，以及會治療、保護、召喚或自爆的敵人。'),
 'Grietas legendarias y clima': ('傳說裂縫與天氣',
  '裂縫會通往 18 個傳說競技場，每種屬性一個；天氣會改變戰局；新增屬性相剋表和用獎券抽的拉霸機扭蛋。'),
 'Cooperativo y ranking': ('組隊與排行榜',
  '和好友名單裡的朋友最多 4 人線上組隊，還有每日、每週、每月、每年和歷來排行榜。'),
}

def news():
    pid = 'news'
    items = []
    for d, t, _ in M.NEWS:
        if t[0] in NEWS:
            h, x = NEWS[t[0]]
            items.append(f'<article class="news"><time datetime="{d}">{d}</time><h2>{esc(h)}</h2><p>{esc(x)}</p></article>')
        elif 'NEWS: ' + t[0] not in missing:
            missing.append('NEWS: ' + t[0])
    h1 = 'PokéSurvivor 最新消息'
    body = f'<div class="doc"><h1>{h1}</h1><p class="lead">原作 PokéSurvivor 的更新紀錄（繁中翻譯）。</p>{"".join(items)}{cta(pid, "免費開玩")}</div>'
    write(pid, h1 + ' · 遊戲更新紀錄', 'PokéSurvivor 最近的更新：新功能、改進與修正（繁中翻譯）。', body, crumbs(pid, h1))

# ================= 支持原作者 =================
def support():
    pid = 'support'
    F = M.D['funding']
    val = lambda v: f'每月 €{v}' if isinstance(v, (int, float)) else esc(zh(v))
    rows = ''.join(f'<tr><td>{esc(zh(c))}</td><td class="num">{val(v)}</td></tr>' for c, v in F['costs'])
    btns = ''.join(x for x in [f'<a class="btn" href="https://ko-fi.com/{F["kofi"]}" rel="noopener">到 Ko-fi 贊助</a>' if F['kofi'] else '',
                               f'<a class="btn ghost" href="https://github.com/sponsors/{F["sponsors"]}" rel="noopener">GitHub Sponsors</a>' if F['sponsors'] else ''])
    h1 = '支持 PokéSurvivor 原作者'
    body = f'''<article class="doc"><h1>{h1}</h1>
<p class="lead">PokéSurvivor 現在免費，以後也會免費：沒有廣告、沒有內購，也沒有付費優勢。如果你喜歡這款遊戲、想幫它繼續營運下去，
可以<b>自願贊助原作者 JPTER78</b>。原作者表示，所有款項都用在伺服器和網域上。</p>
<p><b>這個繁體中文非官方版（78yiyi）不收取任何款項</b>，下面的連結都是原作者的贊助管道。</p>
<p>贊助不會帶來任何遊戲內的優勢：所有玩家都在同樣的條件下遊玩。</p>
<h2>原作的營運成本</h2>
<table class="list"><tbody>{rows}</tbody></table>
<p>這是原作網站 pokesurvivor.com 的成本：伺服器負責保存進度和帳號、排行榜與組隊，玩的人越多，成本越高。</p>
<h2>怎麼支持</h2>
<p>{btns or '原作者的贊助管道還沒開放。'}</p>
<p>免費但很有幫助的方式：把遊戲分享給朋友、推薦給別人，以及回報錯誤（繁中版的問題請到 <a href="{M.FORK_REPO}/issues">GitHub Issues</a>）。</p>
{cta(pid, '回到遊戲')}</article>'''
    write(pid, '支持 PokéSurvivor：贊助原作者',
          'PokéSurvivor 免費、無廣告。自願贊助會給原作者 JPTER78，用在伺服器和網域上；這個繁中非官方版不收取任何款項。', body, crumbs(pid, h1))

def run(module):
    global M, PATS
    M = module
    PATS = []
    for k, v in M.D['zh'].items():
        if '{x}' in k:
            parts = [re.escape(p) for p in k.split('{x}')]
            PATS.append((re.compile('^' + '(.+?)'.join(parts) + '$'), v))
    guide(); pokedex(); legends(); shinies(); types_page(); moves_page(); items_page(); ach_page(); news(); support()
    if missing:
        print(f'缺少繁中（{len(missing)}，暫時用英文或略過）：')
        for s in missing: print('  ', s)
    return len(M.PAGES) - 1

/* 產生 docs/handoff/BALANCE.md：遊戲數值總表（從 js/ 的資料與系統模組直接讀出）。
 *   node tools/make_balance_doc.js
 * 改了數值之後重新執行，文件就會和遊戲一致。名稱同時列出西文原名與繁中譯名。
 */
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.join(__dirname, '..');
const noop = () => {};
const fakeCtx = new Proxy({}, { get: () => noop });
const G = {};
const sandbox = {
  G, console, Math, JSON, Date, Map, Set, Object, Array, Number, String, RegExp, Promise, Symbol, Infinity, NaN, isFinite, parseInt, parseFloat,
  location: { pathname: '/', protocol: 'file:' }, navigator: { language: 'es', languages: ['es'] }, localStorage: { getItem: () => 'es', setItem: noop },
  document: { documentElement: {}, createElement: () => ({ getContext: () => fakeCtx, width: 0, height: 0 }), addEventListener: noop, querySelector: () => null, body: {} },
  addEventListener: noop, matchMedia: () => ({ matches: false }), CanvasRenderingContext2D: function () {}, Image: function () {}, performance: { now: () => 0 },
  setTimeout: noop, setInterval: noop, requestAnimationFrame: noop
};
sandbox.window = sandbox;
vm.createContext(sandbox);
const read = f => fs.readFileSync(path.join(ROOT, f), 'utf8');
const load = f => vm.runInContext(read(f), sandbox, { filename: f });

load('js/core/util.js');
load('js/core/i18n.js');
const ZH = {};
G.I18n.add = (d, to = 'en') => { if (to === 'zh') Object.assign(ZH, d); };
for (const f of ['js/data/lang-zh-names.js', 'js/data/lang-zh.js', 'js/data/pokedex.js', 'js/data/sprites-meta.js', 'js/data/moves.js',
                 'js/data/types.js', 'js/data/enemies.js', 'js/data/upgrades.js', 'js/data/items.js', 'js/systems/levelup.js',
                 'js/systems/gacha.js', 'js/systems/spawner.js', 'js/entities/player.js']) {
  try { load(f); } catch (e) { console.warn('aviso', f, e.message); }
}

const zh = es => (ZH[es] && ZH[es] !== es ? `${es}（${ZH[es]}）` : es);
const num = v => (typeof v === 'number' ? +v.toFixed(3) : v ?? '');
const table = (head, rows) => [`| ${head.join(' | ')} |`, `|${head.map(() => '---').join('|')}|`, ...rows.map(r => `| ${r.map(c => String(num(c)).replace(/\|/g, '\\|')).join(' | ')} |`)].join('\n');
// 從原始碼抓常數那一行（未匯出的閉包常數），並附上出處。
const srcLine = (file, re) => {
  const lines = read(file).split(/\r?\n/);
  const i = lines.findIndex(l => re.test(l));
  return i < 0 ? `（找不到：${file}）` : `\`${lines[i].trim()}\`（${file}:${i + 1}）`;
};

const out = [];
const h = s => out.push('', s, '');
out.push('# 數值總表（BALANCE）', '',
  '> 由 `node tools/make_balance_doc.js` 從遊戲原始碼產生，**不要手改**；改了數值就重新產生。',
  '> 名稱格式：西文原名（繁中）。時間單位為秒，除非另外註明。');

// ---------------- 玩家 ----------------
h('## 1. 玩家成長');
out.push('升級所需經驗：`Player.xpFor(level) = floor((8 + 6·level + 1.6·level^1.75) × 4)`（js/entities/player.js）', '');
const xpRows = [];
let total = 0;
for (let lv = 1; lv <= 40; lv++) { const need = G.Player.xpFor(lv); total += need; if (lv <= 10 || lv % 5 === 0) xpRows.push([lv, need, total]); }
out.push(table(['等級', '升到下一級需要', '累計'], xpRows));
h('### 升級卡片（局內強化，js/systems/levelup.js）');
out.push('權重：新招式 10、招式強化 8、進化 40（有就必出）、能力卡 4（招式欄未滿）／7（已滿）／14（可解鎖進化）。三張卡依權重抽、不重複。', '');
out.push(table(['id', '名稱', '效果', '本局上限'], G.LevelUp.STATS.map(s => [s.id, zh(s.title), ZH[s.desc] || s.desc, s.max || '無'])));

// ---------------- 永久強化 ----------------
h('## 2. 永久強化（每隻寶可夢各自購買，js/data/upgrades.js）');
out.push('價格：`round(base × grow^目前等級 / 10) × 10` 寶可金幣。', '');
out.push(table(['id', '名稱', '每級效果', '上限', '第 1 級', '最後一級', '全部買完'], G.Upgrades.LIST.map(u => {
  let sum = 0; for (let l = 0; l < u.max; l++) sum += G.Upgrades.cost(u.id, l);
  return [u.id, zh(u.name), ZH[u.unit] || u.unit, u.max, G.Upgrades.cost(u.id, 0), G.Upgrades.cost(u.id, u.max - 1), sum];
})));

// ---------------- 屬性 ----------------
h('## 3. 屬性相剋（js/data/types.js）');
out.push('原作把正作的倍率柔化：×2 → ×1.6、×0.5 → ×0.6、×0（無效）→ ×0.3；雙屬性相乘，夾在 [×0.3, ×2.4]。雙向適用（你打敵人、敵人打你）。',
  '', '傷害公式：`招式 dmg × 玩家 atk（種族攻擊 × 強化 × 增益）× 屬性倍率 × 天氣倍率 × 會心 1.5`（js/systems/combat.js `hit()`）。', '');
const types = Object.keys(G.U.TYPE_NAME);
const short = t => (ZH[G.U.TYPE_NAME[t]] || t);
out.push(table(['攻\\守', ...types.map(short)], types.map(a => [short(a), ...types.map(d => { const m = G.Types.mult(a, [d]); return m === 1 ? '·' : m; })])));

// ---------------- 招式 ----------------
h(`## 4. 招式（${G.Moves.ALL.length} 個，js/data/moves.js）`);
out.push('同一隻寶可夢能學的招式＝自己的屬性＋一般屬性。只有「啟用中」的招式會發動（1–4 / Q / E 切換）。', '');
out.push(table(['id', '名稱', '屬性', 'kind', 'cd', 'dmg', 'count', 'pierce', 'radius', '進化（條件）'], G.Moves.ALL.map(m => {
  const ev = G.Moves.evoInfo(Object.assign(G.Moves.instance(m.id, m.maxLvl)), {});
  return [m.id, zh(m.name), short(m.type), m.kind, m.cd, m.dmg, m.count ?? '', m.pierce ?? '', m.radius ?? '', ev ? `${zh(ev.name)}（${zh(ev.needName)}）` : '—'];
})));
h('### 每種 kind 的升級階梯（Lv1 → Lv5）');
const kinds = [...new Set(G.Moves.ALL.map(m => m.kind))];
for (const k of kinds) {
  const m = G.Moves.ALL.find(x => x.kind === k);
  out.push(`- **${k}**：` + m.ups.map((u, i) => `Lv${i + 2} ${ZH[u.t] || u.t}`).join('；'));
}

// ---------------- 敵人 ----------------
h('## 5. 敵人與生怪（js/data/enemies.js、js/systems/spawner.js）');
out.push('每局開始時，每個階層從 BST 範圍內隨機選 7 隻當「本局陣容」（至少 1 隻支援型；第 2 階層起至少 1 隻預警攻擊型；最快的一隻變成 runner）。', '');
out.push(table(['階層', '開始時間', 'BST 範圍', 'hp', 'spd', 'dmg', 'xp'], G.Enemies.TIERS.map((t, i) => [i + 1, t.from, t.bst.join('–'), t.hp, t.spd, t.dmg, t.xp])));
out.push('', '首領（非傳說，依 BST 抽選；實際數值為 hp × 1.35、dmg × 1.2）：', '');
out.push(table(['出現時間', 'hp', 'dmg', 'xp', 'BST 範圍'], G.Enemies.BOSS_SLOTS.map(b => [b.at, b.hp, b.dmg, b.xp, b.bst.join('–')])));
out.push('', '生怪常數：',
  `- 同時在場上限：${srcLine('js/systems/spawner.js', /const CAP = /)}（達 85% 後新出的敵人是菁英：hp ×1.6、dmg ×1.25、xp ×1.6）`,
  `- 密度與倍率：${srcLine('js/systems/spawner.js', /const DENSITY = /)}`,
  `- 額外血量：${srcLine('js/systems/spawner.js', /const hpK = /)}`,
  `- 異色率：${srcLine('js/systems/spawner.js', /const SHINY_RATE = /)}`,
  `- 隨時間成長：${srcLine('js/data/enemies.js', /return \{ hp: 1 \+ t \/ 95/)}`,
  '- 怪物潮：每 38–56 秒一次（首領戰期間暫停），數量 `(14 + floor(t/22)) × 0.4`。', '');
out.push(table(['分鐘', '每秒生成數 rate(t)', 'hp 倍率（scale×hpK）', 'dmg 倍率（scale×2.4）'], [0, 1, 2, 3, 5, 7, 10, 15, 20, 25, 30].map(min => {
  const t = min * 60, sc = G.Enemies.scale(t), hpK = 3.3 + Math.min(1.7, t / 210);
  return [min, G.Spawner.rate(t), sc.hp * hpK, sc.dmg * 2.4];
})));

// ---------------- 扭蛋 ----------------
h('## 6. 扭蛋（js/systems/gacha.js）');
out.push('- 機率：1★ 45% · 2★ 30% · 3★ 17% · 4★ 6.5% · 5★ 1.5%',
  `- 保底：${srcLine('js/systems/gacha.js', /const PITY_5 = /)}（每個卡池各自計算）；×10 連抽保證至少一隻 4★`,
  `- 異色：${srcLine('js/systems/gacha.js', /const SHINY_RATE = /)}`,
  `- 重複退款：${srcLine('js/systems/gacha.js', /const REFUND = /)}（異色重複 ×3）`,
  '- 費用：×1 用 1 張獎券；×10 用 10 張獎券或 1 張 ×10 獎券。');

// ---------------- 道具 ----------------
h('## 7. 攜帶道具（每局一個，js/data/items.js）');
out.push(table(['id', '名稱', '效果'], (G.Items.LIST || []).map(i => [i.id, zh(i.name), ZH[i.desc] || i.desc])));

// ---------------- 節奏 ----------------
h('## 8. 一局的節奏');
out.push(
  `- 生態區每 240 秒切換：${srcLine('js/game.js', /Math\.floor\(time \/ 240\)/)}`,
  `- 裂縫：${srcLine('js/systems/rift.js', /const CHECK = /)}；${srcLine('js/systems/rift.js', /const ARENA_R = /)}`,
  `- 局中事件（怪物潮屬性、黃金時刻、迷路寶可夢）：${srcLine('js/systems/events.js', /const EVERY = /)}`,
  `- 寶藏精靈：${srcLine('js/systems/events.js', /const THIEF_FIRST = /)}`,
  `- 天氣：${srcLine('js/systems/weather.js', /const FROM = /)}`,
  `- 阿爾宙斯的審判：${srcLine('js/systems/judgment.js', /const AT = /)}；${srcLine('js/systems/judgment.js', /const BOSS_EVERY = /)}`,
  `- 主迴圈：可變時間步長，每格上限 1/30 秒（${srcLine('js/game.js', /const dt = Math\.min\(1 \/ 30/)}）`
);

fs.writeFileSync(path.join(ROOT, 'docs', 'handoff', 'BALANCE.md'), out.join('\n') + '\n');
console.log('ok: docs/handoff/BALANCE.md');

/* 產生 js/data/lang-zh-names.js：寶可夢、招式、道具、屬性、地區的官方繁中名稱。
 *   node tools/make_lang_zh_names.js
 *
 * - 寶可夢：pokedex.js 的英文名 -> PokeAPI pokemon_species_names（依圖鑑編號）。
 * - 招式／道具／屬性／地區：lang-en.js 的英文官方名 -> PokeAPI 同一筆資料的繁中名，
 *   key 仍是遊戲原本的西班牙文（i18n 以西班牙文原句為 key）。
 * - PokeAPI 的 CSV 只下載一次，快取在 tools/cache/pokeapi/（不進 repo）。
 * - 對不到的英文名稱會列出來，交給 lang-zh.js 手動翻譯。
 * 另外輸出 tools/cache/zh-todo.tsv：lang-en.js 中還沒有繁中名稱的條目（序號、西文、英文），供手動翻譯。
 */
const fs = require('fs'), path = require('path'), vm = require('vm'), https = require('https');
const ROOT = path.join(__dirname, '..');
const CACHE = path.join(ROOT, 'tools', 'cache', 'pokeapi');
const CSV_BASE = 'https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/';
const FILES = ['pokemon_species_names', 'move_names', 'item_names', 'type_names', 'region_names'];
const LANG_EN = 9, LANG_ZH_HANT = 4;

function download(url, dest) {
  return new Promise((resolve, reject) => {
    https.get(url, res => {
      if (res.statusCode !== 200) { res.resume(); reject(new Error(`${res.statusCode} ${url}`)); return; }
      const out = fs.createWriteStream(dest);
      res.pipe(out);
      out.on('finish', () => out.close(resolve));
    }).on('error', reject);
  });
}

function parseCsv(text) {
  const rows = [];
  for (const line of text.split(/\r?\n/)) {
    if (!line) continue;
    const cells = [];
    let cur = '', quoted = false;
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (quoted) {
        if (c === '"' && line[i + 1] === '"') { cur += '"'; i++; }
        else if (c === '"') quoted = false;
        else cur += c;
      } else if (c === '"') quoted = true;
      else if (c === ',') { cells.push(cur); cur = ''; }
      else cur += c;
    }
    cells.push(cur);
    rows.push(cells);
  }
  return rows.slice(1);
}

const norm = s => s.toLowerCase().normalize('NFKD').replace(/[^a-z0-9]/g, '');

function loadGame() {
  const noop = () => {};
  const G = {};
  const sandbox = {
    G, console, Math, JSON, Map, Set, Object, Array, RegExp,
    location: { pathname: '/', protocol: 'file:' }, navigator: { language: 'es', languages: ['es'] },
    localStorage: { getItem: () => 'es', setItem: noop }, document: { documentElement: {} },
    CanvasRenderingContext2D: function () {}
  };
  sandbox.window = sandbox;
  vm.createContext(sandbox);
  const load = f => vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), sandbox, { filename: f });
  load('js/core/util.js');
  load('js/core/i18n.js');
  const en = {};
  G.I18n.add = d => Object.assign(en, d);
  load('js/data/lang-en.js');
  load('js/data/pokedex.js');
  return { en, dex: G.DEX };
}

async function main() {
  fs.mkdirSync(CACHE, { recursive: true });
  const tables = {};
  for (const f of FILES) {
    const p = path.join(CACHE, f + '.csv');
    if (!fs.existsSync(p)) { console.log('下載', f); await download(CSV_BASE + f + '.csv', p); }
    const byId = new Map();
    for (const [id, lang, name] of parseCsv(fs.readFileSync(p, 'utf8'))) {
      if (+lang !== LANG_EN && +lang !== LANG_ZH_HANT) continue;
      const e = byId.get(id) || {};
      if (+lang === LANG_EN) e.en = name; else e.zh = name;
      byId.set(id, e);
    }
    tables[f] = byId;
  }

  const { en, dex } = loadGame();
  const out = {};
  const missing = [];

  for (const p of dex) {
    const e = tables.pokemon_species_names.get(String(p.dex));
    if (e && e.zh) out[p.name] = e.zh; else missing.push(`寶可夢 #${p.dex} ${p.name}`);
  }

  // 地區名在西文與英文多半相同（Kanto、Johto…），直接以英文名為 key。
  for (const e of tables.region_names.values()) if (e.en && e.zh && out[e.en] === undefined) out[e.en] = e.zh;

  // 順序決定同名時誰優先：Psychic 在遊戲裡是屬性（超能力），不是招式（精神強念）。
  const enToZh = new Map();
  for (const f of ['type_names', 'region_names', 'item_names', 'move_names']) {
    for (const e of tables[f].values()) if (e.en && e.zh && !enToZh.has(norm(e.en))) enToZh.set(norm(e.en), e.zh);
  }
  // 剛好和道具／招式同名的一般 UI 用語（Mejora = 強化，不是道具「升級資料」）。
  const NOT_NAMES = new Set(['Mejora', 'Fuerza', '¡Banda Focus!']);
  for (const [es, enName] of Object.entries(en)) {
    if (out[es] !== undefined || es.includes('{x}') || NOT_NAMES.has(es)) continue;
    const zh = enToZh.get(norm(enName));
    if (zh) out[es] = zh;
  }

  const body = Object.entries(out).map(([k, v]) => `  ${JSON.stringify(k)}: ${JSON.stringify(v)},`).join('\n');
  const header = `/* ============ lang-zh-names.js — GENERADO, no editar a mano ============
 * 由 tools/make_lang_zh_names.js 產生：寶可夢、招式、道具、屬性、地區的官方繁中名稱
 * （資料來源 PokeAPI，CSV 快取在 tools/cache/pokeapi/）。手動翻譯放在 lang-zh.js。
 */
G.I18n.add({
${body}
}, 'zh');
`;
  fs.writeFileSync(path.join(ROOT, 'js', 'data', 'lang-zh-names.js'), header);

  const todo = Object.entries(en).filter(([es]) => out[es] === undefined);
  fs.writeFileSync(path.join(ROOT, 'tools', 'cache', 'zh-todo.tsv'),
    todo.map(([es, e], i) => `${i + 1}\t${es.replace(/\t|\n/g, ' ')}\t${e.replace(/\t|\n/g, ' ')}`).join('\n') + '\n');

  console.log(`ok: ${Object.keys(out).length} 個名稱（寶可夢 ${dex.length - missing.filter(m => m.startsWith('寶可夢')).length}），`
    + `待手動翻譯 ${todo.length} 條 -> tools/cache/zh-todo.tsv`);
  if (missing.length) console.log('缺少繁中名稱：\n  ' + missing.join('\n  '));
}

main().catch(e => { console.error(e); process.exit(1); });

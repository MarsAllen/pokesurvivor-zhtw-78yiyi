/* 檢查繁中翻譯的覆蓋率：英文字典（lang-en.js、lang-fork.js）有、但繁中字典都沒有的 key。
 *   node tools/check_lang_zh.js
 * 也會檢查 {x} 空格數量是否與西文原句一致。有缺漏或錯誤時以 exit code 1 結束。
 * 與上游同步後執行，把列出的 key 補進 js/data/lang-zh.js。
 */
const fs = require('fs'), path = require('path'), vm = require('vm');
const ROOT = path.join(__dirname, '..');

const dicts = { en: {}, zh: {} };
const sandbox = { G: { I18n: { add: (d, to = 'en') => Object.assign(dicts[to], d) } } };
vm.createContext(sandbox);
for (const f of ['js/data/lang-en.js', 'js/data/lang-fork.js', 'js/data/lang-zh-names.js', 'js/data/lang-zh.js']) {
  vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), sandbox, { filename: f });
}

const count = s => (s.match(/\{x\}/g) || []).length;
const missing = Object.keys(dicts.en).filter(k => dicts.zh[k] === undefined);
const badSlots = Object.entries(dicts.zh).filter(([es, zh]) => count(es) !== count(zh));

const total = Object.keys(dicts.en).length;
console.log(`繁中覆蓋率：${total - missing.length} / ${total}`);
if (missing.length) console.log('缺少：\n' + missing.map(k => `  ${JSON.stringify(k)}: ${JSON.stringify(dicts.en[k])}`).join('\n'));
if (badSlots.length) console.log('{x} 數量不符：\n' + badSlots.map(([es, zh]) => `  ${es} -> ${zh}`).join('\n'));
process.exit(missing.length || badSlots.length ? 1 : 0);

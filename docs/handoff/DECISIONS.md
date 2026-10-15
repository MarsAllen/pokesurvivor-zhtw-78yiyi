# 決策紀錄（DECISIONS）

格式：`D-編號｜日期｜決策`，接著寫理由與影響。新的加在最下面；推翻舊決策時新增一筆，並在舊的那筆標 `（已被 D-xx 取代）`。

---

**D-01｜2026-10-15｜以上游最新版（`c31715d`）為基礎，而不是最後的 MIT 版 `b297089`**
目的是非商業，PolyForm Noncommercial 允許研究、修改、分享；最新版包含近期的合作模式修正與手機按鍵配置。
影響：本 fork 永遠不能商業化。如果將來要商業化，只能從 `b297089` 之前的 MIT 程式碼重新出發，而且素材與 IP 仍然要全部換掉。

**D-02｜2026-10-15｜使用公開 GitHub fork（不是私有匯入）**
可以一鍵 Sync 上游，fork 關係本身就是署名。公開 repo 的 fork 不能設成私有。

**D-03｜2026-10-15｜`firebase-config.js` 設為 `null`，`.firebaserc` 改成佔位值，刪除 `CNAME`**
避免本機或部署後連到上游作者付費的 Firebase 專案，也避免 GitHub Pages 搶用 `pokesurvivor.com` 網域。
注意：repo 裡的 `index.html` / `app.min.js` 仍是上游產物，要等 P1-01 重新 build 才會生效。

**D-04｜2026-10-15｜AGENTS.md 是唯一的規範來源，CLAUDE.md 只指向它；上游原本的 CLAUDE.md 移到 `docs/handoff/UPSTREAM_CLAUDE.md`**
Claude Code 和 Codex 輪流接手時讀同一份規範。上游的 CLAUDE.md 有「commit 不加 AI 署名」等只屬於原作者的規範，不適用本 fork。

**D-05｜2026-10-15｜保留原作者的贊助連結，並加註本 fork 不收款**
`.github/FUNDING.yml`（GitHub Sponsor 按鈕）、`js/data/funding.js`、`support-ui.js`、`apoyar/` 都指向原作者的 Ko-fi 和 GitHub Sponsors，全部保留。
理由：原作者免費開放原始碼，替他導流是回饋，也符合「非官方 fork、尊重原作」的立場。
附加要求（P1-02 執行）：支持頁加註「此為原作者 JPTER78 的贊助管道，本繁中 fork 不收取任何款項」。
本 fork 不得加入任何屬於自己的收款管道（PolyForm NC 與 CC BY-NC 都禁止）。

**D-06｜2026-10-15｜線上版＝repo 原始碼，不需要再做逆向工程**
驗證方式：
1. 線上 `https://pokesurvivor.com/version.json` 的 `v` 為 `bc2124ff1d`，與 repo 相同；線上 `js/app.min.js` 的 SHA-1 為 `bc2124ff1d30566b8b283f46bf0b8ffc41c98591`，與 repo commit 的檔案逐位元組相同。
2. 在暫存資料夾用上游 `c31715d` 的 `dev.html`、`js/`、`tools/` 執行 `node tools/build.js`（Node 24、npx terser@5、javascript-obfuscator@4.1.1），產出的 SHA-1 同樣是 `bc2124ff1d…`，代表 build 可重現。
結論：線上遊戲完全由 repo 原始碼產生，沒有未公開的程式碼。之後研究原作直接讀原始碼即可；REA 只在上游未來出現「線上有、repo 沒有」的差異時才需要。
附帶好處：`build.js` 的產出可重現，之後可以用「重新 build 後比對雜湊」來驗證 refactor 沒有改到產物（只限沒有改動原始碼的情況）。

**D-07｜2026-10-15｜繁中化沿用原作的「翻譯層」，名稱也走字典，不改資料檔**
- `i18n.js` 新增 `zh`：`add(dict, 'zh')`；繁中模式先載入英文字典當備援，再由繁中覆蓋（樣板也能覆蓋）。`zh-*` 瀏覽器語系自動選繁中。新增 `G.I18n.locale`（日期與貨幣格式用）。
- 名稱不在 `pokedex.js` 加 `zh` 欄位（原 PLAN 的寫法），而是由 `tools/make_lang_zh_names.js` 產生 `lang-zh-names.js` 字典：寶可夢以英文名為 key（西文與英文相同），招式、道具、屬性以遊戲的西文名為 key，透過 lang-en.js 的英文官方名對照 PokeAPI 的 zh-Hant 名稱。
  理由：不用改任何顯示名稱的程式碼，與上游同步時衝突最少；原作的英文版本來就是這樣運作的。
- 同名衝突以「屬性 > 地區 > 道具 > 招式」的優先順序處理（Psychic 是「超能力」不是「精神強念」）；剛好與道具同名的 UI 用語（Mejora、Fuerza）排除，改為手動翻譯。
- 只有西文與英文內容的地方（更新日誌、說明頁連結），繁中模式顯示英文版。排行榜的組句另外寫了繁中分支（`ranking-ui.js`）。
- 已知限制：片段比對只處理 4 個字元以上的 key，所以短字串（例如 `Nv.`）要另外寫成樣板。

**D-08｜2026-10-15｜非官方標示與聯絡方式**
- 標題、登入畫面、頁尾、法律聲明（新增「非官方版本」段落）、「設定 › 關於」都標明「繁體中文非官方版（78yiyi）」，並保留「官方網站是 pokesurvivor.com」的說明。
- 法律聲明的「聯絡與內容移除」改指向本 fork 的 GitHub Issues，**不公開 Allen 的信箱**；原始碼連結改為本 fork，並另列原作 repo。
- 支持頁與結算後的贊助提示改寫為「款項給原作者 JPTER78，本版本不收款」（延續 D-05）。
- 本 fork 新增或改寫的西文字串，英文與繁中翻譯都放在 `js/data/lang-fork.js`，不改上游的 `lang-en.js`，減少同步衝突。

**D-09｜2026-10-15｜繁中像素字型：俐方體11號子集，改名 YiyiPixel TC**
- 來源 Cubic 11（OFL 1.1，固定 commit `4c566f7`）。只保留翻譯實際用到的字（約 1600 字，66 KB woff2）。
- 子集屬於 OFL 的「修改版本」，不能使用保留名稱「Cubic／俐方體」，所以改名；原版權聲明（nameID 0）保留；授權全文 `assets/fonts/OFL-Cubic11.txt`；出處寫在 `CREDITS.md`、法律聲明與「關於」。
- 以 `unicode-range` 併入 `Pixelify` family，不改任何繪圖程式碼。粗細範圍必須和 Pixelify 的兩組一致，瀏覽器才會當成同一組複合字型。
- `sw.js` 對字型是 cache-first，所以 CSS 的字型網址帶 `?v=內容雜湊`；`make_font_zh.py` 產出可重現（不更新時間戳記）。
- 已知缺字：「戽」（字型本身沒有），會用系統字型顯示。

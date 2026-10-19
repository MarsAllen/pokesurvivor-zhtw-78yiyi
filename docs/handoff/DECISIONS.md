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

**D-10｜2026-10-16｜本 fork 的 Firebase 專案與雲端設定**
- 專案 `pokesurvivor-zhtw-78yiyi`（擁有者 marsallen03@gmail.com），**Spark 免費方案**，未啟用 Google Analytics、Gemini in Firebase、Identity Platform。超出免費額度時 Firebase 會直接拒絕請求，不會收費，所以不設預算警示。
- 登入：電子郵件/密碼（遊戲用「名稱＋密碼」，內部信箱網域 `jugadores.pokesurvivor-zhtw-78yiyi.firebaseapp.com`，從不寄信）＋ Google（公開名稱「PokéSurvivor 繁中非官方版」）。授權網域：localhost、marsallen.github.io。
- Firestore：Standard 版、`(default)`、**asia-east1（台灣）**。RTDB：**asia-southeast1（新加坡，沒有台灣節點）**。
- 雲端只在 `db.js` 的 `HOSTS`（marsallen.github.io、localhost、127.0.0.1）連線。
- 不部署 `functions/`（原作已停用，且需要 Blaze 方案）；`signups.js` 維持 `OFF = true`（不限新帳號數，也不呼叫原作的 Worker）。（2026-10-17：兩者已隨上游刪除，見 D-12）
- `net.js` 的 `TURN_URL` 留空：Phase 3 之前組隊只用 STUN 直連，嚴格 NAT 的玩家可能連不上（`ALLOW_RELAY = false`，與原作相同）。（2026-10-17：上游已刪掉整段 TURN 程式，見 D-12）
- 管理員 UID：Allen（Google 登入，名稱 78yiyi）`FMiUvL3vPaRWnGUY5sMXO9VMgb23`，寫在 `firestore.rules` 的 `admin()` 與 `js/net/ranking.js` 的 `ADMINS`，兩處要一致，改了要重新部署規則。
- 部署：`firebase.cmd deploy --only firestore,database --project pokesurvivor-zhtw-78yiyi`。要在 Allen 的終端機（已 `firebase login`）執行；PowerShell 的執行原則會擋 `.ps1`，所以用 `firebase.cmd`／`npm.cmd`。
- 存檔上傳節奏沿用原作的省額度設計：一般修改 2 小時才上傳、重要事件 15 秒、關閉或切走頁面時立即上傳；所以平常看到 `pending` 是正常的。
- 官方工具：Firebase CLI（npm 全域）與官方 Claude 外掛 `firebase@firebase`（marketplace `firebase/agent-skills`，含 agent skills 與 Firebase MCP server）。不安裝非官方的 Firebase 工具。
- 安全規則已偏離上游（2026-10-16 稽核，D-11）：排行榜名稱綁定身分、摘要列欄位驗證、pres 只給好友讀。同步上游時保留這三處。
- API 金鑰（Browser key）限制：只接受 `https://marsallen.github.io/*`、`http://localhost:8080/*`、`https://pokesurvivor-zhtw-78yiyi.firebaseapp.com/*` 的請求（API 範圍維持 Firebase 自動設定的 25 個）。Google Cloud 不接受 `localhost:*` 萬用埠號，所以**本機測試必須用 8080 埠**（`.claude/launch.json` 就是 8080）；換網域或埠號時要到 Google Cloud 主控台 › API 和服務 › 憑證 新增。

**D-11｜2026-10-16｜安全規則強化（稽核第 2–4 項），第 1 項暫緩**
- 依官方 skill 稽核（`docs/handoff/SECURITY-AUDIT.md`），Allen 決定先修第 2、3、4 項：
  排行榜名稱必須是 ≤16 字元字串、單人紀錄名稱必須等於自己的 `profiles` 暱稱；排行榜摘要列只允許固定欄位且全部要等於已驗證的紀錄；`pres` 只有本人與已確認的好友能讀。
- 第 1 項（被封鎖者刪檔重建即可解除封鎖）同日稍後修正：沒有採用「被封鎖者不能刪存檔」的簡單修法（會讓被封鎖者的「刪除帳號」只做一半，也違反法律聲明的「可以隨時刪除帳號」），改成封鎖另存在只有管理員能寫的 `bans/{uid}`，排行榜寫入檢查它；`ranking.js` 的 `setMarked`／`markedAccounts` 改用 `bans`，`saves.ban` 照舊更新以保持相容。
- 第 2–4 項只改 `firestore.rules`；第 1 項另外改了 `js/net/ranking.js`。修改處都有 `fork（安全稽核 2026-10-16）` 註解，這兩個檔案偏離上游，同步時要手動合併。
- 驗證：部署前後各跑一次攻擊／正常測試（測試表 `s_zz_audit`，已清除），結果見 SECURITY-AUDIT.md。

**D-12｜2026-10-17｜第一次同步上游：跟著拿掉 TURN、新帳號上限**
- 上游 `bd7f3dd`（2026-10-15）因費用刪掉 Cloudflare TURN Worker（`cloudflare/`）、`functions/`（新帳號上限的「門房」函式）、`js/net/signups.js` 與登入畫面的名額提示；組隊只靠 Google 免費 STUN 直連。本 fork 原本就把 `TURN_URL` 留空、`signups.js` 關閉，所以直接採用上游的刪除，`net.js` 用上游版本。
- 同一批更新的「金幣／獎券帳本」（`save.led`）會寫進雲端存檔；`firestore.rules` 的 `saneSave` 只檢查 `coins`、`tickets`，不限制其他欄位，所以不用改規則（實測上傳成功）。
- 上游 `5bbc3b2` 的「必要更新」（`build.js --forzar`）本 fork 先不用；一般發布照舊不加這個參數。
- `CLAUDE.md` 衝突時保留 fork 版，上游內容複製到 `docs/handoff/UPSTREAM_CLAUDE.md`。

**D-13｜2026-10-19｜說明頁改用本 fork 網址，西文／英文頁不讓搜尋引擎收錄**
- `make_seo_pages.py` 的 `SITE` 改成 `https://marsallen.github.io/pokesurvivor-zhtw-78yiyi/`：canonical、hreflang、og、結構化資料、`robots.txt`、`sitemap.xml` 都指向本 fork。`404.html` 改用子路徑開頭的絕對連結（原本的 `/` 開頭會連到 `marsallen.github.io` 根目錄）。
- 西文／英文說明頁、英文版遊戲 `en/`、`contacto/` 加 `noindex`，`sitemap.xml` 只列遊戲首頁。理由：這些頁面是原作網站的複本，改成自己的 canonical 後會和 pokesurvivor.com 搶搜尋結果；原作者特別提醒過「其他網站是複本」，不和原作競爭也符合 D-05「替原作導流」的立場。本 fork 要被搜尋到的是繁中內容（P4-01 的 `zh/` 頁面再開放收錄）。想改回來：拿掉 `NOINDEX` 那幾處、恢復 sitemap 的迴圈。
- 每頁上方加非官方說明（西／英＋繁中一句），連到官方網站；頁尾改成「原作 GitHub · 本 fork GitHub」；支持頁註明連結是原作者的、本 fork 不收款（補上 D-05 原本只做在遊戲內的部分）。
- `contacto/` 是上游手寫的頁面，上面是原作者的信箱：加一段說明「這是原作者的聯絡方式，繁中版的問題請到本 fork 的 GitHub Issues」。

**D-14｜2026-10-19｜繁中說明頁 zh/ 與繁中首頁，開放搜尋引擎收錄**
- 繁中頁放 `zh/`，網址名稱沿用英文版（`zh/guide/`、`zh/pokedex/`、`zh/legendaries/`…）；繁中的「首頁」就是遊戲本身（`index.html`），所以沒有 `zh/index.html`。
- 文案寫在 fork 自己的 `tools/seo_zh.py`，不在上游的 `make_seo_pages.py` 裡加 `elif lang == 'zh'`：上游幾乎每天改那個檔（主要是最新消息），內嵌繁中會一直衝突。上游檔只加了幾個 hook（`PATH['zh']`、sitemap、結尾的 `seo_zh.run()`）。代價是上游改版型時繁中頁不會自動跟上。
- 遊戲資料（寶可夢、招式、道具、屬性、成就、競技場、地區）用遊戲本身的繁中字典翻譯，用語和遊戲一致（裂縫、獎券、首領、羈絆、攜帶道具…）。FAQ 與最新消息以上游的西文標題對應，上游新增的會列為「缺少繁中」。
- 繁中內容依本 fork 實情改寫：支援三種語言、繁中版不收款（贊助給原作者）、「這是官方遊戲嗎」補上非官方版說明、支持頁註明成本表是原作網站的。
- 首頁：`<html lang="zh-Hant">`、繁中 title／description；SEO 標記放在 `dev.html` 的 `fork-seo` 區塊（canonical 指向本 fork、`robots` index、繁中 og、結構化資料 `isBasedOn` 原作）。仍用 `build.js --sin-seo`，上游指向 pokesurvivor.com 的 `seo:` 區塊不進 `index.html`。
- 西班牙文玩家的分頁標題也會是繁中（i18n 在西文模式不翻譯）；英文模式由 `lang-fork.js` 翻成英文。可接受：本 fork 以繁中為主。

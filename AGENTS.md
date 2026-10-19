# AGENTS.md — PokéSurvivor 繁中 fork（pokesurvivor-zhtw-78yiyi）

本檔是 **Claude Code 與 Codex 共用** 的唯一規範來源（`CLAUDE.md` 只是指向這裡）。
任何 AI 代理接手時，**先讀完本檔，再讀 `docs/handoff/PROGRESS.md` 最後一筆**，然後才動手。

---

## 1. 專案是什麼

- 上游：<https://github.com/JPTER78/pokesurvivor>（官方站 pokesurvivor.com，西班牙文為主＋英文）。
- 本 repo：上游的 **公開 GitHub fork**，維護者 Allen（創作代號 78yiyi）。
- 目的（兩者並行）：
  - **A｜非商業繁中同人版**：繁中化、自架、加入自己的改動。
  - **B｜學習**：逐模組讀懂原作系統，必要時重寫，但手感與數值要與原作一致。
- 作法：**直接 fork 修改**（不是從零重寫），沿用 PMD sprites。

## 2. 硬性限制（違反任何一條都不可合併）

1. **非商業**：程式碼為 PolyForm Noncommercial 1.0.0（`b297089` 之後），sprites 為 CC BY-NC 4.0，
   Pokémon 為 Nintendo / Creatures / GAME FREAK / TPC 的 IP。**不得販售、收費、內購、放廣告、加入付費抽獎。**
2. **保留授權與署名**：不可刪改 `LICENSE`、`LICENSE-NONCOMMERCIAL.md`、`CREDITS.md`；
   PolyForm Required Notice：`Copyright 2026 JPTER78 (https://github.com/JPTER78/pokesurvivor)` 必須保留。
3. **標明非官方**：對外顯示的名稱、頁面須能看出是「非官方繁中 fork」，不可冒充 pokesurvivor.com。
4. **不可連到上游的雲端資源**：上游 Firebase 專案 `pokesurvivor-free`、Cloudflare Worker
   `turn.pokesurvivor.com`、上游 Cloudflare ACCOUNT_ID 都屬於原作者，fork 不可使用。
   本 fork 用自己的 Firebase 專案 `pokesurvivor-zhtw-78yiyi`（Spark 免費方案，詳見 DECISIONS D-10）；**不要升級 Blaze、不要啟用 Identity Platform、不要加回 Cloud Functions 或其他付費服務**（上游 2026-10-15 已刪掉 `functions/` 與 `cloudflare/`）。
5. **不要把機密放進 repo**（Firebase Web config 不是機密；service account、TURN secret、token 才是）。
6. **不要對上游發 PR**，除非 Allen 明確要求。建立 PR 時 base repo 一定是 `MarsAllen/...`。

## 3. 技術概覽（詳見 `docs/handoff/ARCHITECTURE.md`）

- Vanilla JS + Canvas 2D（1280×720），無框架、執行時無依賴。全域命名空間 `G`，每個檔案是 `G.X = (() => {...})()` 模組。
- `dev.html` = **原始頁面**（逐檔載入 ~70 個 script）；`index.html` 與 `js/app.min.js` 由 `tools/build.js` **產生，禁止手改**。
- 資料表在 `js/data/`；`pokedex.js`、`sprites-meta.js` 是 `tools/` 腳本產生的，不要手改。
- i18n：遊戲內文字以**西班牙文原句為 key**，`js/data/lang-en.js` 為英文對照；繁中將以 `lang-zh.js` 同樣方式加入（Phase 1）。
- 存檔：localStorage（本機）／Firestore（雲端，已啟用）。多人：WebRTC + RTDB signaling（已啟用），只用 Google 免費 STUN 直連（上游 2026-10-15 拿掉了 TURN）。
- 改了 `firestore.rules`／`database.rules.json`／`firestore.indexes.json` 要重新部署：在 Allen 的終端機執行 `firebase.cmd deploy --only firestore,database --project pokesurvivor-zhtw-78yiyi`（先加 `--dry-run` 驗證）。官方 Firebase 外掛（skills＋MCP）已安裝，可在新 session 使用。
- 注意：Claude Code 的 Bash／PowerShell 工具可能在沙盒中執行，`npm -g` 等寫到使用者目錄的安裝不一定會落到真實系統；要在真實系統執行或需要使用者憑證的指令（例如 firebase），用終端機分頁。

## 4. 如何執行

```bash
# 本機開發（用 dev.html；Service Worker 與部分功能需要 http）
python -m http.server 8080
# 瀏覽 http://localhost:8080/dev.html
```

```bash
# 產生發布版（會改 index.html / js/app.min.js / version.json）
node tools/build.js --sin-seo
```

- Node 24、Python 3.12 已在 Allen 的機器上驗證可用。build 會透過 `npx` 下載 terser 與 javascript-obfuscator。
- 改了 `js/`、`dev.html` 之後，**合併前要重新 build**（`node tools/build.js --sin-seo`，再執行 `PYTHONIOENCODING=utf-8 python tools/make_seo_pages.py` 更新 `en/index.html`），並把 `index.html`、`en/index.html`、`js/app.min.js`、`version.json` 一起 commit。`sitemap.xml` 如果只有日期變動就還原。
- 說明頁（`guia/`、`pokedex/`、`en/*`、`zh/*`、`404.html`、`robots.txt`、`sitemap.xml`）全由 `tools/make_seo_pages.py` 產生，不要手改；網址用檔頭的 `SITE`（本 fork 的 GitHub Pages 子路徑），西文／英文頁一律 `noindex`（D-13），繁中頁 `zh/` 與首頁開放收錄（D-14）。唯一手寫的是 `contacto/index.html`。
- 繁中說明頁的文案在 `tools/seo_zh.py`（遊戲資料用遊戲的繁中字典翻譯，所以先執行 `node tools/export_data.js`）。`make_seo_pages.py` 印出「缺少繁中」時要補齊再合併（上游改了 FAQ 問題或新增最新消息，就補進 `seo_zh.py` 的 `faq()`／`NEWS`）。
- 首頁的繁中 SEO（canonical、og、結構化資料、`robots` index、`PS_PAGES`）在 `dev.html` 的 `<!-- fork-seo:begin -->` 區塊：`build.js --sin-seo` 只拿掉上游的 `seo:` 區塊，所以 `index.html` 會保留它；`en/index.html` 由 `make_seo_pages.py` 拿掉。
- 開發時用 `dev.html`（逐檔載入，console 可以存取 `G`）；`index.html` 是混淆過的發布版，`G` 不會出現在 console。
- 本 fork 新增或改寫的西文字串：英文與繁中翻譯放進 `js/data/lang-fork.js`（不要改上游的 `lang-en.js`）；其他繁中翻譯放在 `js/data/lang-zh.js`。合併前執行 `node tools/check_lang_zh.js`，必須 100%。
- 改了繁中翻譯（`lang-zh*.js`、`lang-fork.js`）後要執行 `PYTHONIOENCODING=utf-8 python tools/make_font_zh.py` 重新產生字型子集（會自動更新 `css/style.css` 裡的 `?v=` 雜湊），否則新出現的字會用系統字型顯示。
- 用腳本改上游的檔案時要保留原本的換行字元（上游多為 CRLF；Python 用 `newline=''` 讀寫）。
- `python -m http.server` 不會送 no-cache 標頭，瀏覽器可能沿用舊的 js：改了檔案卻看不到效果時，先清除 Service Worker 與快取再重新載入（做法見 PROGRESS 2026-10-15（三））。
- 預覽工具在伺服器就緒前就會開 `/`，Service Worker 可能回傳快取的舊頁面；看到舊版本時重新導向一次即可。
- 在 Claude 桌面版的內建瀏覽器裡，預覽面板隱藏時 rAF 不會觸發，解法見 PROGRESS 2026-10-15（二）。
- 內建瀏覽器也會直接擋掉 `confirm()`／`alert()`（`confirm` 立刻回傳 false）。遊戲裡需要確認的動作（檢舉、封鎖、刪除好友、訪客登出等）在面板裡會像「沒反應」；要測這些請用一般瀏覽器，或在 console 暫時覆寫 `window.confirm = () => true`（只限測試分頁）。
- 排行榜讀過的資料會在瀏覽器快取 30 分鐘（原作的省額度設計），所以剛上傳的紀錄不一定馬上看得到；要確認資料請直接查 Firestore 的 `lbs/{表名}`。

## 5. 工作流程（交接協定）

1. 開工：讀本檔 → `docs/handoff/PROGRESS.md` 最新一筆 → `docs/handoff/PLAN.md` 找下一個 `TODO` 任務。
2. 一次只做一個任務 ID（例如 `P1-03`）；開分支 `feat/P1-03-short-name`（或 `fix/…`、`docs/…`）。**不要直接 commit 到 `main`。**
3. 完成條件寫在 PLAN 的每個任務裡；達成後把狀態改成 `DONE`，並附上 commit／PR。
4. **收工前（包含 token 快用完時）必定**：
   - 在 `PROGRESS.md` 最上方新增一筆（日期、代理名稱、做了什麼、卡在哪、下一步、未驗證的部分）。
   - commit 並 push 目前分支，即使工作只做了一半（commit 訊息標 `WIP`）。
5. 做出重要取捨時，記到 `docs/handoff/DECISIONS.md`。
6. 推送到遠端、合併 main、對外發布之前，先向 Allen 確認。**GitHub Pages 從 `main` 根目錄自動部署（https://marsallen.github.io/pokesurvivor-zhtw-78yiyi/），合併進 main 就等於對外發布**，所以合併前一定要先重新 build 並實測。

### Commit 格式

```
<type>(<task-id>): <簡短說明>

<為什麼這樣改；必要時列出驗證方式>
```

type：`feat` / `fix` / `i18n` / `docs` / `chore` / `refactor`。

## 6. 程式慣例

- 沿用原作風格：`G` 命名空間、IIFE 模組、2 空白縮排、單引號、沒有 build-time 型別。
- 原作的西班牙文註解保留；新增的註解用**繁體中文**，只寫「為什麼」。
- 新增 script 檔要加進 `dev.html` 的 `<!-- scripts:begin -->` 區塊，並視需要加進 `js/main.js` 的 `NEED` 清單。
- 改到遊戲數值或手感時，在 PR 說明「原值 → 新值」與理由；B 目的的重寫**預設不改數值**。
- 不加多餘抽象層、不預留擴充點、不加不必要的錯誤處理。

## 7. 與上游同步

```bash
git fetch upstream
git merge upstream/main   # 在獨立分支上做，例如 chore/sync-upstream-YYYYMMDD
```

衝突高風險檔：`js/core/firebase-config.js`、`js/core/db.js`（HOSTS 白名單、NAME_DOMAIN）、
`js/data/lang-en.js`、`dev.html`、產生的 `index.html` / `app.min.js`（衝突時直接重新 build）、
`firestore.rules`（保留 `fork（安全稽核 2026-10-16）` 那三處，見 `docs/handoff/SECURITY-AUDIT.md`，合併後要重新部署）、
`js/net/ranking.js`（管理員 UID）、`tools/make_seo_pages.py`（標了 `fork：` 的地方：`SITE`、noindex、非官方標示、支持頁說明、404、sitemap）、
`contacto/index.html`（非官方說明＋noindex）、`dev.html` 開頭（`<html lang="zh-Hant">`、繁中 title／description、`fork-seo` 區塊；`make_seo_pages.py` 的 `game_en()` 用這兩個字串當比對鍵，改了要一起改）、
`tools/export_data.js`（匯出繁中字典）、`js/ui/settings-ui.js` 與 `support-ui.js`（繁中模式連到 `zh/` 頁）。
上游新增的西班牙文字串要同步補進 `lang-zh.js`（`node tools/check_lang_zh.js` 會列出缺少的）。
上游的 `CLAUDE.md` 要整份複製到 `docs/handoff/UPSTREAM_CLAUDE.md`（本 repo 的 `CLAUDE.md` 保留 fork 版）。
合併後照「改了 js 之後」的流程重新 build；說明頁、`404.html`、`robots.txt`、`sitemap.xml` 有衝突時先取任一邊，再執行 `node tools/export_data.js` 和 `make_seo_pages.py` 重新產生。第一次同步的紀錄見 PROGRESS 2026-10-17。

## 8. 參考文件

- `docs/handoff/PLAN.md` — 分階段計劃與任務清單
- `docs/handoff/PROGRESS.md` — 進度日誌
- `docs/handoff/ARCHITECTURE.md` — 系統地圖
- `docs/handoff/DECISIONS.md` — 決策紀錄
- `docs/handoff/UPSTREAM_CLAUDE.md` — 上游作者原本的工作規範（西班牙文，發布流程與自動更新機制的出處）
- `GDD.md`、`docs/FIREBASE.md`、`docs/PUBLICAR.md` — 上游設計與部署文件

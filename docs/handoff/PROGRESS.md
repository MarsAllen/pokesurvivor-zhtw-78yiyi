# 進度日誌（PROGRESS）

**最新的放在最上面。** 每次收工（包含 token 快用完時）都要新增一筆，格式：

```
## YYYY-MM-DD｜代理（Claude / Codex）｜分支
- 完成：
- 進行中／卡住：
- 下一步：
- 未驗證：
```

---

## 2026-10-19｜Claude｜fix/P4-00-seo-pages

- 完成：P4-00 說明頁壞連結與原作網域。
  - 查到的狀況：說明頁之間本來就用相對路徑，真正壞掉的是 `404.html`（`/` 開頭的絕對路徑，在 GitHub Pages 子路徑下 9 個連結全壞）；canonical、hreflang、og、結構化資料、`robots.txt`、`sitemap.xml`、`en/index.html` 都指向 pokesurvivor.com。
  - 修改 `tools/make_seo_pages.py`：`SITE` 改成本 fork、404 用 `BASE` 子路徑、西文／英文頁 `noindex`、sitemap 只列首頁、每頁加非官方說明、頁尾加本 fork GitHub、支持頁註明款項給原作者（D-13）。`contacto/index.html` 手動加非官方說明＋noindex。重新執行 `export_data.js`、`make_seo_pages.py`。
  - 驗證：寫了離線連結檢查（依 GitHub Pages 子路徑解析每個 href/src，404 模擬從深層網址顯示）：修改前 9 個壞連結，修改後 2757 個內部連結 0 個壞掉；頁面中剩下的 pokesurvivor.com 只有「官方網站在 pokesurvivor.com」的說明連結。本機瀏覽器看過支持頁、聯絡頁（無橫向捲動、無錯誤請求）。
- 下一步：P4-01 繁中說明頁（`zh/`）；首頁 `index.html` 的 `<html lang>`、title、description 還是西文，也可以一起改成繁中。
- 未驗證：搜尋引擎實際收錄情況（GitHub Pages 專案網站的 robots.txt 不會被讀，要用 Search Console）。

---

## 2026-10-17｜Claude｜chore/sync-upstream-20261016

- 完成：P4-02 第一次同步上游（合併到上游 `5bbc3b2`，共 2 個 commit）。
  - 上游內容：拿掉 TURN／Cloudflare Worker、`functions/`、`signups.js`（新帳號上限）；金幣與獎券改用每台裝置的帳本 `save.led`，兩台裝置同時玩不會互相蓋掉，離開 30 分鐘後回來會從雲端拉一次；「必要更新」（`build.js --forzar`）；更新日誌兩筆。
  - 衝突：`CLAUDE.md` 保留 fork 版（上游版複製到 `UPSTREAM_CLAUDE.md`）；`net.js` 用上游版（fork 原本只把 `TURN_URL` 留空，上游已整段刪除）；`signups.js` 刪除；產生的檔案重新 build（版本 `bb74894349`）。`db.js` 自動合併，`HOSTS`／`NAME_DOMAIN` 保留。`firestore.rules`、`ranking.js` 上游沒改，沒有衝突。
  - 繁中：新字串 1 條（必要更新的倒數提示），覆蓋率 1167/1167；字型不用重做（字都已經有）。
  - 本機實測（dev.html＋index.html，78yiyi）：載入沒有錯誤請求；帳本建立（`led.base` = 金幣 625、獎券 2），帶帳本的存檔上傳雲端成功（規則沒擋）；登入畫面的名額提示元素已移除；必要更新提示的繁中翻譯正確。
- 文件：AGENTS §7（同步流程補上 UPSTREAM_CLAUDE、sitemap、check_lang_zh）、ARCHITECTURE（帳本、updater、拿掉 TURN）、DECISIONS D-12、PLAN（P4-02 DONE、P3-01/02 DROPPED）。
- 下一步：P4-00 說明頁壞連結。
- 未驗證：組隊（`net.js`／`coop.js` 有改，需要兩台裝置）；兩台裝置同時玩的金幣合併（上游邏輯，等 Allen 實際用手機＋電腦玩時觀察）。

---

## 2026-10-16（三）｜Claude｜fix/rules-hardening

- 完成：用官方 skill `firebase-security-rules-auditor` 稽核安全規則，修正前 2 分（詳見 `docs/handoff/SECURITY-AUDIT.md`）。依 Allen 指示修正第 2、3、4 項（排行榜名稱綁定身分、摘要列欄位驗證、pres 只給好友讀），已部署；部署前後實測攻擊被擋、正常功能不受影響，測試資料已清除。
- 補充：Allen 回報「每週排行榜還是沒紀錄」，是上一輪封鎖測試把 test78 的紀錄從所有表刪掉了（伺服器上四張單人表都是空的）；test78 要再玩一局超過 2:13 才會重新上榜（手機記著他的最佳 133 秒）。
- 後續（同日）：稽核第 1 項也修了：封鎖改記在只有管理員能寫的 `bans/{uid}`（`firestore.rules` ＋ `ranking.js`），已部署並以 78yiyi 實測「封鎖 → 刪檔重建 → 仍無法上榜 → 解除封鎖 → 可上榜」，存檔已還原（金幣 625）。
- 下一步：P4-02 第一次同步上游；P4-00 說明頁壞連結。
- 未驗證：沒有用模擬器跑自動測試（沒裝 Java）；組隊排行榜（`g_*`）的寫入規則沒有額外改動，但也還沒實際寫入過。

---

## 2026-10-16（二）｜Claude｜fix/mod-ui-zh

- Allen 用手機（名稱＋密碼帳號 test78）＋電腦（78yiyi）實測的結果：
  - 註冊、手機操作、好友：正常。
  - 組隊：行動數據下正常（同一個 Wi-Fi 的情境沒有測，等之後有問題再處理）。
  - 排行榜：電腦看「每週」沒有 test78，其他分頁有。**原因是原作的 30 分鐘讀取快取**：電腦在 test78 上傳紀錄之前（15:23）看過每週表，快取了空表；其他分頁是之後（15:33）才看的。Firestore 上每週表 `s_w2026-42j` 的資料是正確的。不是錯誤，不修改。
  - 檢舉沒反應：**Claude 的內建瀏覽器面板會直接擋掉 `confirm()`**（2 毫秒回傳 false、不顯示對話框），遊戲以為按了取消。一般瀏覽器與手機正常。在本機暫時覆寫 `window.confirm` 後實測：檢舉寫入、管理畫面列出、封鎖、解除封鎖都正常（P2-05 完成）。
- 修正：管理畫面（`mod-ui.js`）的西班牙文補上繁中（原作英文版也沒翻）。封鎖帳號列表的小字被原作標成 `translate="no"`，維持原樣。
- 組隊排行榜沒有資料：Allen 確認那局未滿 2 分鐘（`MIN_T = 120`，不會上傳），屬於正常。待 Allen 再玩一局超過 2 分鐘的組隊後確認 `g_*` 表有寫入。
- 未驗證：同一個 Wi-Fi 下組隊、iOS Safari。

---

## 2026-10-16｜Claude｜feat/P2-02-firebase

- 完成：
  - 在 Allen 登入的瀏覽器裡建立 Firebase 專案 `pokesurvivor-zhtw-78yiyi`（Spark），啟用電子郵件/密碼與 Google 登入、加入授權網域 marsallen.github.io，建立 Firestore（台灣）與 RTDB（新加坡），註冊網頁應用程式（D-10）。
  - 安裝官方 Firebase CLI（Allen 的終端機，`npm.cmd -g`）與官方 Claude 外掛 `firebase@firebase`（skills＋MCP）；Allen 完成 `firebase login`。
  - 程式碼：填入 config、HOSTS／NAME_DOMAIN 改成本 fork、TURN 留空、管理員 UID 設為 Allen；部署 Firestore 規則與索引、RTDB 規則。
  - 本機驗證：雲端模式、Allen 用 Google 註冊（78yiyi）、`flush()` 後 Firestore `saves/{uid}` 寫入金幣 600、夥伴 #4、性格 travieso；重新載入後從雲端讀回、`isAdmin()` 為 true。
- 發現：
  - Claude 的 Bash／PowerShell 工具在沙盒裡，`npm -g` 沒有落到真實系統；Allen 的 PowerShell 會擋 `.ps1`，要用 `firebase.cmd`／`npm.cmd`。
  - 終端機分頁 c2 的輸入列曾經顯示錯亂，但指令其實有執行（第二次部署顯示 already up to date）。
  - 存檔 `pending` 是原作的省額度設計（2 小時才上傳；關閉頁面時會立即上傳）。
- 後續（同日）：已合併發布；Allen 在線上版用 Google 登入，存檔正確讀回（金幣 600、小火龍、收藏 1/966）。P2-07 完成：API 金鑰限制在 marsallen.github.io、localhost:8080、firebaseapp.com（其他網域 403），線上版登入仍正常。
- 下一步：用第二個帳號＋手機測好友、排行榜、組隊與封鎖（決定是否需要 Phase 3 TURN）；P2-03 用 emulator 跑規則測試。
- 未驗證：名稱＋密碼註冊、好友、排行榜、組隊（需要第二個帳號）、手機。

---

## 2026-10-15（五）｜Claude｜fix/zh-online-qa

- 完成：
  - P1-10：Allen 開啟 GitHub Pages（main、根目錄），線上版 https://marsallen.github.io/pokesurvivor-zhtw-78yiyi/ 上線。
  - 線上驗證（桌機 Chrome，內建瀏覽器）：載入最新 build、繁中像素字型、Service Worker 接管、console 無錯誤、所有請求都在自己的網域（沒有 Firebase 或原作伺服器）；瀏覽器語系為中文時自動顯示繁中；訪客模式走完測驗 → 開局 → 戰鬥 → 升級選卡 → 暫停 → 放棄這局 → 結算。
  - 修正線上 QA 發現的翻譯問題：暫停提示的 `moverse ·` 誤翻成「招式」（改為「移動」）；結算金幣明細的 `recogidas` 漏翻（補上「撿到」）。
- 已知小問題：升級標題顯示「等級 2!」（驚嘆號是獨立的標點節點，翻譯層不處理），不影響遊玩；原作說明頁的絕對連結在子路徑下會壞（P4-00）。
- 下一步：Allen 用手機實測（P1-09）；之後 Phase 2 雲端（需要 Allen 建 Firebase 專案）。

---

## 2026-10-15（四）｜Claude｜feat/P1-04-zh-font、docs/P1-07-08-architecture（都已合併進 main）

- 完成：
  - P1-04：繁中像素字型 YiyiPixel TC（俐方體11號子集，66 KB）以 `unicode-range` 併入 `Pixelify`，DOM 與 canvas 都已確認使用（D-09）。
  - P1-07：ARCHITECTURE 補完主迴圈與更新順序、一局的時間軸、傷害與成長公式、存檔結構與合併規則。
  - P1-08：`tools/make_balance_doc.js` 產生 `docs/handoff/BALANCE.md`（經驗曲線、升級卡、永久強化價格、屬性表、64 個招式與進化、敵人階層與首領、生怪速率、扭蛋、道具、節奏常數）。
- 更正 Codex 先前分析中的數字（以原始碼為準）：同時在場敵人上限是 **64**（不是 280，舊版是 420）；組隊同步約 **15 次／秒、relay 5 次／秒**（不是 15／7／3 Hz）；主迴圈是可變步長。
- 下一步：Phase 1 剩下需要 Allen 的 **P1-09（手機實機 QA）** 和 **P1-10（部署 GitHub Pages、決定網域）**；之後是 Phase 2 雲端（需要 Allen 建 Firebase 專案）。
- 未驗證：手機觸控、iOS Safari、長時間遊玩（30 分鐘審判）的繁中顯示。

---

## 2026-10-15（三）｜Claude｜feat/P1-01-rebuild、feat/P1-03-zh-i18n、feat/P1-02-unofficial（都已合併進 main）

- 完成：
  - P1-01：以 fork 設定重新 build，發布版不再內含上游 Firebase 設定；修正 `build.js` 在路徑含空白時於 Windows 失敗的問題。
  - P1-03／05／06：繁體中文上線。`i18n.js` 支援 `zh`（缺字退回英文）、設定頁可選「繁體中文」、`zh-*` 語系自動選繁中；`lang-zh-names.js`（PokeAPI 官方名稱，966 隻寶可夢＋招式、道具、屬性、地區）、`lang-zh.js`（手動翻譯 996 條＋原作英文版也缺的字串）；`tools/check_lang_zh.js` 覆蓋率 100%。
  - P1-02：標題、登入、頁尾、法律聲明、關於、支持頁都標明非官方版；聯絡改用 GitHub Issues（D-08）。
  - 實測：繁中模式走完登入 → 測驗 → 主選單各畫面 → 一局 → 結算，用 DOM 掃描與攔截 canvas `fillText` 確認沒有殘留的西文或英文；英文與西文模式回歸測試正常；發布版 `index.html` 繁中正常。
- 發現（給後續接手者）：
  - 清除瀏覽器快取的做法（在 console 執行）：
    `for (const r of await navigator.serviceWorker.getRegistrations()) await r.unregister(); for (const k of await caches.keys()) await caches.delete(k); await Promise.all([...document.scripts].filter(s => s.src).map(s => fetch(s.src, {cache: 'reload'}))); location.reload();`
  - 找殘留未翻譯字串的方法：DOM 用 TreeWalker 掃描含拉丁字母的文字節點；canvas 則包裝 `CanvasRenderingContext2D.prototype.fillText`，記錄 `G.I18n.t(s)` 之後仍含拉丁字母的字串。
  - 遊戲裡「繁中退回英文」的地方：更新日誌（只有西文與英文）、說明頁連結（`en/guide/`、`en/pokedex/`）。
- 下一步：P1-04（繁中像素字型；目前繁中字是瀏覽器的系統字型）。
- 未驗證：手機實機、組隊與雲端相關畫面的繁中（需要 Phase 2/3 的雲端）。

---

## 2026-10-15（二）｜Claude｜chore/P0-05-06-verify

- 完成：
  - P0-06：線上 `app.min.js` 與 repo 逐位元組相同，而且用上游原始碼重新 build 可以重現同一個雜湊。線上版沒有隱藏程式碼（DECISIONS D-06）。
  - P0-05：在 `http://localhost:8080/dev.html` 以訪客模式走完 登入 → 8 題人格測驗 → 主選單 → 開局 → 自動攻擊與戰鬥 → 升級三選一（玩到 0:41、Lv3），沒有 JS 錯誤或 unhandled rejection。DB 狀態為 `mode: local`、`localReason: config`，確認沒有連到雲端。
  - 新增 `.claude/launch.json`（`python -m http.server 8080`）。
- 發現（給後續接手者）：
  - **Claude 桌面版內建瀏覽器的預覽面板隱藏時，`requestAnimationFrame` 完全不會觸發**，遊戲會停在 0:00。測試時可以在 console 執行
    `window.requestAnimationFrame = cb => setTimeout(() => cb(performance.now()), 16); G.Game.init();`
    重新啟動迴圈（只影響該分頁，不要寫進程式碼）。
  - **預覽工具預設開啟 `/`，也就是 `index.html`（上游 build，內含上游 Firebase 設定）**。本次曾短暫載入過一次（localhost 在上游 HOSTS 白名單內，所以會初始化上游的 Firestore SDK；沒有登入，也沒有寫入）。在 P1-01 完成前，一定要直接開 `/dev.html`。
  - REA `capture_browser_scenario`（無頭 Chromium）裡，登入面板 `#btn-guest` 30 秒內一直不可見，原因未查（可能和 headless 或 reduced-motion 有關）。之後要做自動化測試時再研究。
  - 原作的英文翻譯有缺漏：人格測驗結果的性格名稱（例如 `Impulsivo`）在英文模式下沒有翻譯。
  - 瀏覽器語系不是西班牙文時，預設會顯示英文（`i18n.js`）。P1-03 要讓 `zh-*` 對應到繁中。
- 下一步：P1-01（用 fork 的設定重新 build `index.html`／`app.min.js`）。
- 未驗證：完整的 10 分鐘局、首領、裂縫、死亡結算、手機觸控。

---

## 2026-10-15｜Claude｜setup/handoff-docs

- 完成：
  - 在 GitHub fork 上游（`JPTER78/pokesurvivor` @ `c31715d`）到 `MarsAllen/pokesurvivor`，clone 到本機，並設定 `upstream` remote。
  - P0-03：刪除 `CNAME`；`.firebaserc` 改成佔位值；`js/core/firebase-config.js` 設為 `null`（純本機模式）。
  - P0-04：新增 `AGENTS.md`、`CLAUDE.md`（指向 AGENTS.md），以及 `docs/handoff/`（PLAN、PROGRESS、ARCHITECTURE、DECISIONS）；上游 CLAUDE.md 移到 `docs/handoff/UPSTREAM_CLAUDE.md`；README 開頭加上非官方 fork 聲明。
  - P0-02：Allen 已把 repo 改名為 `pokesurvivor-zhtw-78yiyi`，本機 `origin` 也已更新。
  - D-05：決定保留原作者的贊助連結，並在支持頁加註本 fork 不收款（由 P1-02 執行）。
- 進行中／卡住：無。
- 下一步：P0-05（本機跑 `dev.html` 玩一局）→ P0-06（用 REA 比對線上版）→ P1-01（重新 build）。
- 未驗證：
  - 還沒有在本機實際啟動過遊戲。
  - `index.html` / `app.min.js` 仍是上游 build（內含上游 Firebase 設定），在完成 P1-01 前只用 `dev.html` 測試。
- 發現（給後續接手者）：
  - Codex 先前分析中「程式碼 MIT」已經過時：2026-10-14 起改為 PolyForm NC（`b297089` 之前是 MIT）。
  - 畫布不是固定 1280×720，而是依視窗大小、DPR 上限 1.5。
  - Pixelify Sans 沒有 CJK 字形，繁中化一定要另外處理字型（P1-04）。
  - `pokedex.js` 只有英文名稱，繁中名稱要從 PokeAPI 的 `zh-hant` 取得（P1-06）。

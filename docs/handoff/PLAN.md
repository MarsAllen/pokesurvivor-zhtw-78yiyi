# 分階段計劃（PLAN）

狀態：`TODO` / `DOING` / `DONE` / `BLOCKED`。每次只做一個任務；完成時填上 commit 或 PR。
需要 Allen 決定或操作的項目標 **[Allen]**。

---

## Phase 0｜建立基礎

| ID | 狀態 | 任務 | 完成條件 |
|---|---|---|---|
| P0-01 | DONE | 在 GitHub fork 上游到 `MarsAllen` | fork 存在 |
| P0-02 | DONE | 把 repo 改名為 `pokesurvivor-zhtw-78yiyi`，並更新本機 `origin` | <https://github.com/MarsAllen/pokesurvivor-zhtw-78yiyi> |
| P0-03 | DONE | 拿掉與上游衝突的設定：刪除 `CNAME`、`.firebaserc` 改成佔位值、`firebase-config.js` 設為 `null` | 見 `setup/handoff-docs` 分支 |
| P0-04 | DONE | 撰寫 AGENTS.md 與 `docs/handoff/` 交接文件 | 同上 |
| P0-05 | DONE | 本機跑起 `dev.html`，以訪客模式玩一局，記錄 console 錯誤 | 冒煙測試通過、沒有錯誤（見 PROGRESS 2026-10-15 第二筆） |
| P0-06 | DONE | 比對線上 pokesurvivor.com 的 `app.min.js` 與 repo HEAD | 可重現 build，雜湊完全一致，見 DECISIONS D-06 |

## Phase 1｜讀懂＋繁中化＋單人版（只用本機存檔）

| ID | 狀態 | 任務 | 完成條件 |
|---|---|---|---|
| P1-01 | DONE | 用 fork 的設定重新 build（`node tools/build.js --sin-seo`），讓 `index.html` 和 `app.min.js` 不再內含上游的 Firebase 設定；並修正 `build.js` 在路徑含空白時的 Windows 錯誤 | `app.min.js` 已搜尋不到 `pokesurvivor-free`；`index.html` 顯示本機模式、沒有載入 Firebase SDK |
| P1-02 | DONE | 標明非官方：標題、登入畫面、README 開頭；`login.js` 的 `host` 提示改成本 fork 的說明；支持頁保留原作者贊助連結並加註本 fork 不收款（DECISIONS D-05） | 任何玩家畫面都能看出這是「非官方繁中 fork」，並附上原作連結；支持頁有不收款聲明 |
| P1-03 | DONE | i18n 加入 `zh`：`i18n.js` 支援 `zh`（`zh-TW`、`zh-Hant`、`zh-HK` 的瀏覽器語系自動選中，`ps.lang` 可存 `zh`），設定畫面加入語言選項 | 切換到繁中後重新整理，語言設定仍保留 |
| P1-04 | DONE | 繁中字型：選一套 OFL 授權的繁中像素字型（候選：俐方體 11 號 Cubic 11、Fusion Pixel），用 `pyftsubset` 依 `lang-zh.js` 與寶可夢名稱實際用到的字做子集，作為 Pixelify 的 fallback；授權檔放進 `assets/fonts/` | 子集字型小於 500 KB；選單、HUD、canvas 文字都沒有豆腐字；`CREDITS.md` 有加註 |
| P1-05 | DONE | 建立 `js/data/lang-zh.js`：以 `lang-en.js` 的 key 為基準翻譯全部字串，再補上原作英文版也沒翻的字串（性格名稱、忘記密碼說明、管理畫面、時間格式等） | `node tools/check_lang_zh.js` 覆蓋率 1153/1153；走完登入、測驗、主選單各畫面、一局到結算，DOM 與 canvas 掃描都沒有殘留 |
| P1-06 | DONE | 寶可夢、招式、道具、屬性、地區的官方繁中名稱：`tools/make_lang_zh_names.js` 從 PokeAPI CSV 產生 `js/data/lang-zh-names.js`（作法改變，見 DECISIONS D-07） | 966 隻都有繁中名稱；HUD、結算、收藏都正確顯示 |
| P1-07 | DONE | 逐模組研讀（目的 B），依序：`game.js` → `player.js` → `combat.js` → `enemy.js` → `spawner.js` → `world.js` → `levelup.js` → `progress.js` → `db.js`；每讀完一個就補 ARCHITECTURE 對應段落（資料結構、主要函式、數值來源） | ARCHITECTURE 不再有「待深入」（已補主迴圈順序、時間軸、傷害公式、存檔結構；之後重寫某模組時，再補該模組函式層級的筆記） |
| P1-08 | DONE | 把數值表整理成可讀的 `docs/handoff/BALANCE.md`（敵人、招式、升級曲線、生怪節奏、gacha 機率），由 `tools/make_balance_doc.js` 從 `js/` 產生 | 文件可重複產生；數字和遊戲內一致 |
| P1-09 | DOING **[Allen]** | 手機與桌機 QA（桌機 Chrome 線上版已驗證；手機實機待 Allen）：Chrome 桌機、Android Chrome、iOS Safari 各完整玩一局 10 分鐘以上 | PROGRESS 中有 QA 紀錄 |
| P1-10 | DONE | 部署到 GitHub Pages（純本機存檔模式，從 `main` 的根目錄部署） | https://marsallen.github.io/pokesurvivor-zhtw-78yiyi/ 可以遊玩（2026-10-15 驗證） |

> 目的 B 的重寫：在 P1-07 讀懂某個模組後，如果要改寫，另開 `refactor/P1-07-<module>` 任務，**預設不改任何數值**，
> 並用相同種子（seed）或錄影並排比對手感。

## Phase 2｜雲端（帳號、存檔、排行榜）

| ID | 狀態 | 任務 | 完成條件 |
|---|---|---|---|
| P2-01 | DONE | 建立自己的 Firebase 專案 `pokesurvivor-zhtw-78yiyi`（Spark、未啟用 Identity Platform）、Web App；登入方式、授權網域、Firestore（asia-east1）、RTDB（asia-southeast1）見 DECISIONS D-10 | 已取得 config |
| P2-02 | DONE | 填入 `firebase-config.js`、更新 `.firebaserc`；`db.js` 的 `HOSTS`、`NAME_DOMAIN` 改成本 fork；停用原作 TURN Worker | 本機可以 Google 登入並寫入雲端存檔（2026-10-16 驗證）；線上版待合併後驗證 |
| P2-03 | DOING | 部署規則與索引（已部署）；安全稽核完成並修正第 1–4 項（見 `SECURITY-AUDIT.md`）；用 emulator 跑自動規則測試（未做，需要 Java 21） | 其他使用者無法讀寫自己的存檔；稽核的攻擊測試被拒絕 |
| P2-04 | DONE | `functions/`（新帳號上限）不部署、`signups.js` 維持 `OFF = true`（與原作相同，見 D-10） | 決策已記錄 |
| P2-05 | DONE | 管理員 UID 設為 Allen（`firestore.rules` admin()、`ranking.js` ADMINS，已部署）；管理畫面補上繁中 | 2026-10-16 實測：檢舉 → 管理畫面列出 → 封鎖（四張排行榜的紀錄被移除、出現在「已封鎖」）→ 解除封鎖，全部正常 |
| P2-06 | DONE | 費用：Spark 方案不會產生費用（超量時 Firebase 直接拒絕請求），不需要預算警示；若升級 Blaze 再設定 | 決策已記錄 |
| P2-07 | DONE | Browser API key 的網站限制：`https://marsallen.github.io/*`、`http://localhost:8080/*`、`https://pokesurvivor-zhtw-78yiyi.firebaseapp.com/*`（Google 登入彈窗需要） | 其他網域回應 403，三個允許的網址回應 200；線上版登入正常（2026-10-16 驗證） |

## Phase 3｜四人合作

| ID | 狀態 | 任務 | 完成條件 |
|---|---|---|---|
| P3-01 | DROPPED | ~~自架 Cloudflare TURN Worker~~：上游 2026-10-15 因費用把 TURN 整個拿掉，`cloudflare/` 已刪（D-12）。真的有人連不上時再另外評估 | — |
| P3-02 | DROPPED | ~~`net.js` 的 `TURN_URL`、`signups.js` 的 `URL` 改成自己的 Worker~~：兩者都已隨上游刪除 | — |
| P3-03 | TODO | 多裝置測試：同一 Wi-Fi、行動網路、跨 NAT；四人房、斷線重連、倒地救援、同步選牌 | QA 紀錄 |

## Phase 4｜內容頁與長期維護

| ID | 狀態 | 任務 | 完成條件 |
|---|---|---|---|
| P4-00 | DONE | SEO 頁面（`guia/`、`pokedex/`、`en/*`、`404.html`、`sitemap.xml`、`robots.txt`、`en/index.html` 的 canonical／og 標記）仍是原作內容並指向 pokesurvivor.com；而且用「/」開頭的絕對連結，在 GitHub Pages 子路徑下會壞。要改成本 fork 的路徑或停用 | 產生的頁面中不再出現上游網域（「官方網站」說明除外）。2026-10-19 完成：改 `make_seo_pages.py`（`SITE`、404 用子路徑、noindex、非官方標示），離線檢查 2757 個內部連結 0 個壞掉 |
| P4-01 | DONE | `make_seo_pages.py` 加入 `zh/` 輸出（圖鑑、招式、屬性、傳說、異色、道具、成就、指南、更新日誌）；首頁改繁中並開放收錄 | `zh/` 頁面已產生並可瀏覽（2026-10-19：10 頁，`tools/seo_zh.py`，D-14） |
| P4-02 | DONE | 建立與上游同步的固定流程（AGENTS.md §7；每次同步用 `check_lang_zh.js` 補 `lang-zh.js` 缺少的 key） | 第一次同步完成（2026-10-17，上游 `5bbc3b2`） |
| P4-03 | TODO | 本 fork 的原創改動（Allen 決定內容） | — |

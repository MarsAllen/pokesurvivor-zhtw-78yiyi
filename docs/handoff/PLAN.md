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
| P1-02 | TODO | 標明非官方：標題、登入畫面、README 開頭；`login.js` 的 `host` 提示改成本 fork 的說明；支持頁保留原作者贊助連結並加註本 fork 不收款（DECISIONS D-05） | 任何玩家畫面都能看出這是「非官方繁中 fork」，並附上原作連結；支持頁有不收款聲明 |
| P1-03 | DONE | i18n 加入 `zh`：`i18n.js` 支援 `zh`（`zh-TW`、`zh-Hant`、`zh-HK` 的瀏覽器語系自動選中，`ps.lang` 可存 `zh`），設定畫面加入語言選項 | 切換到繁中後重新整理，語言設定仍保留 |
| P1-04 | TODO | 繁中字型：選一套 OFL 授權的繁中像素字型（候選：俐方體 11 號 Cubic 11、Fusion Pixel），用 `pyftsubset` 依 `lang-zh.js` 與寶可夢名稱實際用到的字做子集，作為 Pixelify 的 fallback；授權檔放進 `assets/fonts/` | 子集字型小於 500 KB；選單、HUD、canvas 文字都沒有豆腐字；`CREDITS.md` 有加註 |
| P1-05 | DONE | 建立 `js/data/lang-zh.js`：以 `lang-en.js` 的 key 為基準翻譯全部字串，再補上原作英文版也沒翻的字串（性格名稱、忘記密碼說明、管理畫面、時間格式等） | `node tools/check_lang_zh.js` 覆蓋率 1153/1153；走完登入、測驗、主選單各畫面、一局到結算，DOM 與 canvas 掃描都沒有殘留 |
| P1-06 | DONE | 寶可夢、招式、道具、屬性、地區的官方繁中名稱：`tools/make_lang_zh_names.js` 從 PokeAPI CSV 產生 `js/data/lang-zh-names.js`（作法改變，見 DECISIONS D-07） | 966 隻都有繁中名稱；HUD、結算、收藏都正確顯示 |
| P1-07 | TODO | 逐模組研讀（目的 B），依序：`game.js` → `player.js` → `combat.js` → `enemy.js` → `spawner.js` → `world.js` → `levelup.js` → `progress.js` → `db.js`；每讀完一個就補 ARCHITECTURE 對應段落（資料結構、主要函式、數值來源） | ARCHITECTURE 不再有「待深入」 |
| P1-08 | TODO | 把數值表整理成可讀的 `docs/handoff/BALANCE.md`（敵人、招式、升級曲線、生怪節奏、gacha 機率），由腳本從 `js/data/` 產生 | 文件可重複產生；數字和遊戲內一致 |
| P1-09 | TODO | 手機與桌機 QA：Chrome 桌機、Android Chrome、iOS Safari 各完整玩一局 10 分鐘以上 | PROGRESS 中有 QA 紀錄 |
| P1-10 | TODO **[Allen]** | 部署到 GitHub Pages（純本機存檔模式）；決定網域（`*.github.io` 或自有網域） | 公開網址可以遊玩 |

> 目的 B 的重寫：在 P1-07 讀懂某個模組後，如果要改寫，另開 `refactor/P1-07-<module>` 任務，**預設不改任何數值**，
> 並用相同種子（seed）或錄影並排比對手感。

## Phase 2｜雲端（帳號、存檔、排行榜）

| ID | 狀態 | 任務 | 完成條件 |
|---|---|---|---|
| P2-01 | TODO **[Allen]** | 建立自己的 Firebase 專案（**不要啟用 Identity Platform**）、Web App，並設定 API key 的網域限制 | 拿到 config |
| P2-02 | TODO | 填入 `firebase-config.js`、更新 `.firebaserc`；`db.js` 的 `HOSTS` 改成本 fork 的網域、`NAME_DOMAIN` 改成自有字串 | 在部署網域上可以註冊、登入、雲端存檔 |
| P2-03 | TODO | 審查並部署 `firestore.rules`、`database.rules.json`、`firestore.indexes.json`；用 emulator 跑規則測試 | 其他使用者無法讀寫自己的存檔 |
| P2-04 | TODO | 評估 `functions/`（新帳號限制）與 `signups.js`（MAU 上限）是否需要；需要就部署，不需要就停用並記到 DECISIONS | 決策已記錄 |
| P2-05 | TODO | 排行榜、好友、管理後台（`mod-ui.js`）的管理員帳號設定 | 管理員可以封鎖測試帳號 |
| P2-06 | TODO | 費用監控：Firebase 預算警示 | 預算警示已設定 |

## Phase 3｜四人合作

| ID | 狀態 | 任務 | 完成條件 |
|---|---|---|---|
| P3-01 | TODO **[Allen]** | 開 Cloudflare 帳號、設定 Realtime TURN；`wrangler.toml` 換成自己的 `ACCOUNT_ID`、route，secret 用 `wrangler secret put` | Worker 已上線 |
| P3-02 | TODO | `net.js` 的 `TURN_URL`、`signups.js` 的 `URL` 改成自己的 Worker | 合作模式拿得到 TURN 憑證 |
| P3-03 | TODO | 多裝置測試：同一 Wi-Fi、行動網路、跨 NAT；四人房、斷線重連、倒地救援、同步選牌 | QA 紀錄 |

## Phase 4｜內容頁與長期維護

| ID | 狀態 | 任務 | 完成條件 |
|---|---|---|---|
| P4-01 | TODO | `make_seo_pages.py` 加入 `zh/` 輸出（圖鑑、招式、屬性、傳說、異色、道具、成就、指南、更新日誌） | `zh/` 頁面已產生並可瀏覽 |
| P4-02 | TODO | 建立與上游同步的固定流程（每次同步補 `lang-zh.js` 缺少的 key，由 P1-05 的比對腳本找出） | 第一次同步完成 |
| P4-03 | TODO | 本 fork 的原創改動（Allen 決定內容） | — |

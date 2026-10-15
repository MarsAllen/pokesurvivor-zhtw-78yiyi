# 系統地圖（ARCHITECTURE）

> 狀態：**初版骨架**（2026-10-15，Claude）。依檔頭註解、載入順序與少量原始碼整理而成。
> 標 `待深入` 的段落由 P1-05 逐模組研讀時補完；補完後把該段的「待深入」拿掉。

## 1. 總覽

- 約 70 個 JS 檔、約 2 萬行（不含產生的 `app.min.js`）。全部掛在全域 `G` 上，`js/core/util.js` 建立 `window.G`。
- 每個模組都是 `G.Name = (() => { ...; return { 公開 API }; })();`，**沒有 import/export**，依賴關係完全靠 `dev.html` 的載入順序。
- 正式版由 `tools/build.js` 依 `dev.html` 的 `<!-- scripts:begin -->…<!-- scripts:end -->` 串接 → terser → javascript-obfuscator，
  並包在 IIFE 內讓 `G` 不出現在 console（防作弊）。`--expose` 可產生不包裝、不混淆的版本給自動測試。
- 畫布：`#game` 依視窗大小調整，內部解析度 = CSS 尺寸 × `min(1.5, devicePixelRatio)`（**不是固定 1280×720**）。

## 2. 遊戲流程（`js/game.js`）

```
login ─> 人格測驗（只有第一次）─> 主選單 ─> run ─> 結算 ─> 主選單
                                   ├─ 寶可夢（收藏）
                                   ├─ 強化
                                   └─ Gacha
```

- `G.Game` 迴圈狀態：`ui`（選單，背景照常繪製世界）／`playing`／`levelup`／`paused`／`over`。
- `G.Flow` 負責畫面切換；`js/main.js` 檢查 `NEED` 清單中的模組是否都已載入，再呼叫 `G.Flow.boot()`。
- 主迴圈使用 `requestAnimationFrame`；時間步進方式（固定或可變 dt）`待深入`。

## 3. 模組地圖（依 `dev.html` 載入順序）

| 層 | 檔案 | 職責 |
|---|---|---|
| core | `util.js` | 共用 helper，建立 `G` |
| core | `i18n.js` | 翻譯層（es→en／zh）：DOM（MutationObserver）、canvas（包裝 fillText/strokeText）、alert/confirm；精確句、`{x}` 樣板、片段（≥4 字元）三層比對。`G.I18n.lang`（es/en/zh）、`G.I18n.locale` |
| data | `lang-en.js` | 英文字典（key＝西班牙文原句）；繁中模式也會先載入當備援 |
| data | `lang-zh-names.js`* | 寶可夢、招式、道具、屬性、地區的官方繁中名稱（`tools/make_lang_zh_names.js` 產生） |
| data | `lang-zh.js` | 繁中手動翻譯（本 fork 新增）；`tools/check_lang_zh.js` 檢查覆蓋率 |
| core | `settings.js` | 本裝置設定 |
| data | `music.js` | 樂譜（自訂文字格式），由 `audio.js` 合成 |
| data | `pokedex.js`* | 966 隻的 dex、名稱（英文）、屬性、hp/spd/atk（由種族值換算）、rarity、gen、starter、leg |
| data | `sprites-meta.js`* | PMD sprite 每個動作的影格尺寸與錨點 |
| core | `firebase-config.js` | Firebase Web config（fork 目前為 `null`） |
| core | `db.js` | 存檔：`cloud`（Firebase）或 `local`（localStorage）；含帳號、合併策略、HOSTS 白名單 |
| core | `audio.js` | Web Audio 合成器＋排程器＋卷積殘響；音效限制同時發聲數 |
| core | `input.js` / `touch.js` | 鍵鼠／觸控（浮動或固定搖桿） |
| core | `sprites.js` | PMD 動畫器，依需求載入、LRU（`MAX_SHEETS = 200`） |
| core | `camera.js` | 世界↔螢幕座標 |
| data | `moves.js` | 招式目錄（melee/beam/orbit/nova/aura/buff…） |
| data | `types.js` | 18 屬性相剋表 |
| data | `starters.js` | 初始夥伴與人格測驗題目 |
| data | `enemies.js` | 野生敵人定義（各世代） |
| data | `upgrades.js` / `items.js` | 永久強化／單局裝備道具 |
| data | `missions.js` / `achievements.js` | 每日、每週任務模板／成就、獎牌、稱號 |
| data | `funding.js` / `changelog.js` | 贊助資訊／更新日誌（西＋英） |
| world | `tiles.js` | 程式繪製的像素地形 |
| world | `world.js` | 無限開放場地：16×16 tile 的 chunk，資料永遠生成、圖像只烘焙可見範圍（`MAX_IMAGES = 48`） |
| entities | `vfx.js` / `fx.js` | 招式像素特效／粒子、傷害數字（依畫質有上限） |
| entities | `projectile.js` | 投射物與光球 |
| entities | `enemy.js` | 野生寶可夢與其管理器（個性：治療、護盾、召喚…）、空間網格 |
| entities | `pickup.js` | 經驗球與道具 |
| entities | `player.js` | 玩家操控的寶可夢 |
| systems | `combat.js` | 招式執行與碰撞 |
| systems | `spawner.js` | 波次、首領、異色（每波 `CAP = 64`，菁英從 0.85 開始）`待深入` |
| systems | `levelup.js` | 升級三選一 |
| systems | `gacha.js` | 每個世代一個卡池 |
| systems | `interact.js` | 祭壇、泉水、上鎖寶箱、陷阱 |
| systems | `rift.js` | 裂縫與傳說寶可夢競技場 |
| systems | `judgment.js` | 第 30 分鐘的「阿爾宙斯審判」 |
| systems | `events.js` | 局中事件、寶藏精靈 |
| systems | `weather.js` | 天氣（晴、雨、沙、雪、霧） |
| systems | `pathing.js` | 敵人繞過岩石與湖 |
| systems | `progress.js` | 任務、成就與帳號統計 |
| systems | `hazards.js` | 敵人的地面預警攻擊 |
| net | `social.js` | 暱稱、好友、上線狀態、邀請、房間（`MAX_PLAYERS = 4`） |
| net | `signups.js` | 每月新帳號上限（呼叫上游 `turn.pokesurvivor.com/mau`） |
| net | `net.js` | WebRTC 連線＋relay（`TURN_URL = https://turn.pokesurvivor.com/`） |
| net | `coop.js` | 合作模式：房主權威，處理敵人、掉落、經驗 |
| net | `ranking.js` | 存活時間排行榜（日、週、月、歷史、好友、各寶可夢） |
| ui | `icons.js` | 字元圖轉 canvas 的像素圖示 |
| ui | 其餘 `*-ui.js`、`hud.js`、`login.js`、`test.js`、`menu.js`、`slots.js` | 各畫面；`mod-ui.js` 是隱藏的排行榜管理畫面 |
| core | `updater.js` | 每 5 分鐘檢查 `version.json`，有新版就自動重新載入（選單中直接、局中等結束） |
| — | `game.js` / `main.js` | 主迴圈與流程／開機 |

`*` = 由 `tools/` 腳本產生，不要手改。

## 4. 資料與存檔

- localStorage key 前綴 `ps.`（例：`ps.lang`、`ps.nick.<uid>`、`ps.rk.c.<key>`、`ps.ask`）。存檔主結構 `待深入`（`db.js`）。
- 雲端合併規則（上游 README）：收藏取聯集、強化與統計取最大值、金幣與夥伴取最新版本。
- 訪客模式只存在記憶體中。

## 5. 雲端與多人（Phase 2/3 才會啟用）

| 功能 | 技術 | 上游設定位置 |
|---|---|---|
| 帳號、雲端存檔、好友、排行榜 | Firebase Auth + Firestore | `firestore.rules`、`firestore.indexes.json` |
| 房間、signaling、relay | Firebase Realtime Database | `database.rules.json` |
| 新帳號限制等 | Cloud Functions | `functions/index.js` |
| TURN 憑證、上線人數、MAU | Cloudflare Worker + Durable Objects | `cloudflare/turn-worker.js`、`wrangler.toml` |
| 多人連線 | WebRTC DataChannel，星狀、房主權威 | `js/net/net.js`、`coop.js` |

需要從上游網域改掉的寫死位址：`db.js`（`HOSTS`、`NAME_DOMAIN`）、`net.js`（`TURN_URL`）、`signups.js`（`URL`）、
`funding.js`、`login.js` 的非官方站提示、`wrangler.toml`（`routes`、`ACCOUNT_ID`）、SEO 頁面與 `index.html` 的 canonical。

## 6. 靜態內容頁（SEO）

`pokedex/`、`movimientos/`、`tipos/`、`legendarios/`、`shinies/`、`objetos/`、`logros/`、`guia/`、`novedades/`、
`apoyar/`、`contacto/`，以及 `en/` 下對應的英文版，由 `tools/export_data.js` + `tools/make_seo_pages.py` 產生。繁中版本放在 Phase 4。

## 7. 素材

- `assets/pokemon/{dex}/`：PMD 動畫表（Idle、Walk、Attack、Shoot、Charge、Hurt、Faint），8 方向；`s/` 為異色版。
  依 `-Shadow.png` 推出的地面錨點對齊。
- 實體座標 `(x, y)` 代表**腳底**；碰撞在地面平面計算，投射物繪製時抬高並畫出影子。
- 字型：Pixelify Sans（OFL）＋自製數字版本（`tools/make_font.py`）。**沒有 CJK 字形**，繁中需要另外的字型方案（見 PLAN P1-04）。

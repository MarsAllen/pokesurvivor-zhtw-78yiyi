# 系統地圖（ARCHITECTURE）

> 狀態：2026-10-15（Claude）依原始碼整理。數值細節在 `BALANCE.md`（由 `tools/make_balance_doc.js` 產生）。
> 讀程式時的建議順序：`game.js` → `player.js` → `combat.js` → `enemy.js` → `spawner.js` → `world.js` → `levelup.js` → `progress.js` → `db.js`。

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
- 主迴圈 `loop()` 先排下一格 rAF 再執行 `frame()`：一格出錯不會讓遊戲凍住；連續 180 格出錯就結束這局並存檔。
- **可變時間步長**：`dt = min(1/30, 實際經過秒數) × speedK`（不是固定步長；卡頓時遊戲會變慢而不是跳格）。
- `update(dt)` 的順序（只在 `playing`）：審判動畫 → 死亡動畫 → `time += dt`、每 240 秒換生態區 →
  `Player.update` → （合作）隊友傀儡 → `Camera.follow` → `World.update` → `Path.update`＋`Spawner.update`（房主）→
  `EnemyMgr.update` → `rebuildGrid`（空間網格每格重建）→ `Combat.tick` → `Projectiles.update` → `Combat.resolve` →
  `Combat.updateFields` → `Pickups.update` → `Hazards` → `Interact` → `Rift` → `Judgment` → `Events` → `Weather` → `FX` →
  音樂 → `maybeLevelUp()`（房主）→ 羈絆 → 全滅檢查。
- 繪製：地面 → 液體 → 預警 → 地面特效 → 掉落物 → 依 Y 排序的物件／敵人／玩家／裂縫／阿爾宙斯 → 投射物 → 空中特效 → 天氣 → 暈影 → HUD → 觸控。

### 一局的時間軸（數值見 BALANCE.md §5、§8）

| 時間 | 事件 |
|---|---|
| 0 | 第 1 階層敵人；每局隨機抽「本局陣容」（`Enemies.rollRun`） |
| 70／160／260／380／500 秒 | 第 2–6 階層加入，舊階層權重降低 |
| 每 38–56 秒 | 怪物潮（首領戰時暫停） |
| 75 秒起每 30 秒 20% | 裂縫（存在 45 秒，競技場戰 120 秒，打倒傳說得獎券＋羈絆） |
| 120 秒起每 60 秒 18% | 天氣（約 1 分鐘） |
| 2–4 分鐘起 | 寶藏精靈（15 秒內抓住） |
| 每 240 秒 | 換生態區 |
| 每 240–300 秒 | 局中事件：屬性怪物潮／黃金時刻／迷路寶可夢（各 30 秒） |
| 3／6／9／12／15 分鐘 | 首領（非傳說） |
| 28 分鐘 | 不再開裂縫 |
| 30 分鐘 | 阿爾宙斯的審判：無敵的阿爾宙斯＋每 5 秒一隻強度倍增的傳說，撐到倒下為止 |

### 傷害與成長

- 玩家打敵人：`招式 dmg × 玩家 atk × 屬性倍率（柔化，0.3–2.4）× 天氣倍率 ×（會心 1.5）`（`combat.js hit()`）。
- 玩家 `atk` = 種族攻擊（`pokedex.js` 由種族值換算）× 永久強化 × 局內「威力」卡 × 增益招式層數。
- 敵人數值 = 階層模板 × 個體修正（種族 HP／速度）× 隨時間成長 `scale(t)` × 額外血量 `hpK(t)`；傷害再 ×2.4、經驗 ×5.6；場上達 85% 上限後新生成的是菁英。
- 招式 Lv1→5 依 `kind` 套用共用的升級階梯；滿級且本局拿過指定的能力卡，就會出現金色「進化」卡（必出）。

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
| systems | `spawner.js` | 生怪：在視野外的圓環生成；速率 `rate(t)`、場上上限 64（**不是 280**）、85% 後生成菁英；首領依時間表；怪物潮；異色 1/4096 |
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
| net | `net.js` | WebRTC 連線（只用 STUN）＋relay（`ALLOW_RELAY = false`） |
| net | `coop.js` | 合作模式：房主權威，處理敵人、掉落、經驗 |
| net | `ranking.js` | 存活時間排行榜（日、週、月、歷史、好友、各寶可夢） |
| ui | `icons.js` | 字元圖轉 canvas 的像素圖示 |
| ui | 其餘 `*-ui.js`、`hud.js`、`login.js`、`test.js`、`menu.js`、`slots.js` | 各畫面；`mod-ui.js` 是隱藏的排行榜管理畫面 |
| core | `updater.js` | 每 5 分鐘檢查 `version.json`，有新版就自動重新載入（選單中直接、局中等結束）；`version.json` 有 `force: true`（`build.js --forzar`）時，局中 10 秒後結束該局（照放棄處理，會存檔）再重新載入 |
| — | `game.js` / `main.js` | 主迴圈與流程／開機 |

`*` = 由 `tools/` 腳本產生，不要手改。

## 4. 資料與存檔

- localStorage key 前綴 `ps.`：`ps.accounts`（本機帳號）、`ps.session`、`ps.save.<帳號>`（存檔）、`ps.cloud.*`、`ps.lang`、`ps.nick.<uid>`、`ps.rk.c.<key>`（排行榜快取）、`ps.ask`。
- 存檔結構（`db.js newSave()`，`v: 3`）：`coins`（起始 500）、`owned`／`shiny`（dex → { at, from }）、`partner`／`partnerShiny`、`starter`、`personality`、
  `pupg`（dex → 各寶可夢的永久強化等級）、`tickets { t1, t10 }`、`pity`（世代 → 未出 5★ 的抽數）、`legends`、`arenas`、`itemsFound`、`evoMoves`、`ach`、
  `missions`、`profile { favs, title }`、`stats { runs, bestTime, bestLevel, totalKills, pulls, … }`。舊版存檔由 `migrate()` 補欄位。
- 雲端合併規則（`db.js merge()`，可重複套用）：收藏、傳說、競技場、道具、進化、成就取聯集；強化與統計取最大值；同一天的任務取較大進度；夥伴、pity 用較新的版本。
- 金幣與獎券用「帳本」`save.led`（上游 2026-10-15）：每台裝置（`localStorage` 的 `ps.dev`）各記 `[累計得到, 累計花掉]`，合併時每筆取較大值，餘額＝全部加總，所以兩台裝置同時玩不會互相蓋掉。`led.base` 是導入帳本前的餘額，`led.old` 是舊版遊戲分頁的變動。離開超過 30 分鐘再回來時會從雲端拉一次合併（`pullSoon`）。
- 訪客模式只存在記憶體中。

## 5. 雲端與多人（Firebase 已啟用；只用 STUN 直連）

| 功能 | 技術 | 設定位置 | 本 fork 狀態 |
|---|---|---|---|
| 帳號、雲端存檔、好友、排行榜 | Firebase Auth + Firestore | `firestore.rules`、`firestore.indexes.json` | 已啟用（`pokesurvivor-zhtw-78yiyi`，D-10） |
| 房間、signaling、relay | Firebase Realtime Database | `database.rules.json` | 已啟用（relay 關閉，`ALLOW_RELAY = false`） |
| 多人連線 | WebRTC DataChannel，星狀、房主權威；約 15 次／秒，走 RTDB relay 時 5 次／秒 | `js/net/net.js`、`coop.js` | 只用 STUN 直連 |

已改成本 fork 的位址：`db.js`（`HOSTS`、`NAME_DOMAIN`）、`ranking.js` 與 `firestore.rules` 的管理員 UID。
仍是上游的：`funding.js`（原作者的贊助，D-05）、SEO 頁面（P4-00）。
上游 2026-10-15 刪掉了 TURN（Cloudflare Worker）、`functions/`（新帳號上限）與 `signups.js`，本 fork 跟著刪（D-12）。

## 6. 靜態內容頁（SEO）

`pokedex/`、`movimientos/`、`tipos/`、`legendarios/`、`shinies/`、`objetos/`、`logros/`、`guia/`、`novedades/`、
`apoyar/`、`contacto/`，以及 `en/` 下對應的英文版，由 `tools/export_data.js` + `tools/make_seo_pages.py` 產生。繁中版本放在 Phase 4。

## 7. 素材

- `assets/pokemon/{dex}/`：PMD 動畫表（Idle、Walk、Attack、Shoot、Charge、Hurt、Faint），8 方向；`s/` 為異色版。
  依 `-Shadow.png` 推出的地面錨點對齊。
- 實體座標 `(x, y)` 代表**腳底**；碰撞在地面平面計算，投射物繪製時抬高並畫出影子。
- 字型：Pixelify Sans（OFL）＋自製數字版本（`tools/make_font.py`）。繁中用 `YiyiPixelTC.woff2`（俐方體11號的子集，`tools/make_font_zh.py` 產生），在 `css/style.css` 以同一個 family `Pixelify` 加上 `unicode-range` 組成複合字型，DOM 與 canvas 都會自動使用。

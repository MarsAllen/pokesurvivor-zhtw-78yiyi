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

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

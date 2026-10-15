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

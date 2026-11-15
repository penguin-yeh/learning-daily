# learning-daily
**產生信件前請先讀 [STYLE.md](STYLE.md)（「技術手札」風格、Gmail 行內 CSS）並照做。**

## 發佈方式

每天的學習內容不再寄 email，改成直接發佈在 GitHub Pages：<https://penguin-yeh.github.io/learning-daily/>

1. 當天內容整理成 `data/YYYY-MM-DD.json`（欄位見 `scripts/render_email.py` 檔頭）。
2. `python3 scripts/render_email.py data/YYYY-MM-DD.json > YYYY-MM-DD.html`，再複製成 `index.html`（永遠是最新一天）。
3. 更新 `learning-log.md`，commit 並 push 到 `main`。

`sample-2026-11-13.html` 與 `data/sample-2026-11-13.json` 是新風格的節錄範例（內容節錄自 11/13 當天內容）。需要 GitHub Pages 設成從 `main` 根目錄發佈。

## 日期切換

每個日期頁面與 `index.html` 最上方都有「前一天／日期選單／後一天」導覽列，由 `scripts/add_nav.py` 產生（冪等、行內 CSS）。產生新頁面後請執行 `python3 scripts/add_nav.py`；`pages.yml` 也會在每次發佈前自動補跑，所以漏跑也會補上。

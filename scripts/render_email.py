#!/usr/bin/env python3
"""
render_email.py — 產生「每日學習筆記」的固定風格 HTML（風格規範見 STYLE.md「技術手札」）。

用途：
每天的 Routine 只需要把當天的教學內容整理成一份 JSON（結構見下方 SAMPLE），
餵給這支 script，就能得到一份排版、配色都固定一致的 HTML email 內容，
存成 YYYY-MM-DD.html 與 index.html 後 commit 並 push 到 main，由 GitHub Pages 發佈（不再寄 email）。

用法：
    python3 scripts/render_email.py input.json > output.html
    # 或
    cat input.json | python3 scripts/render_email.py > output.html

JSON 格式（欄位說明）：
{
  "date": "2026-08-19",
  "is_review": false,              // true 則內文會標注「複習」
  "theme": "（選填）三個領域今天若剛好有自然關聯，一句話帶過；沒有就省略，不要硬拗。",
  "algo": [
    {
      "topic": "Graph Traversal：BFS／DFS 與拓樸排序",
      "explanation_html": "<p>...核心概念說明（可含 <b>、<code>、<ul>、<pre> 等基本標籤）...</p>",
      "derivation_html": "<p>（選填）時間/空間複雜度或某個數字上限是怎麼推導出來的...</p>",
      "source_label": "（選填）真實原始碼的來源標示，例如 \"leetcode.com 官方題解 / C++\" 或某個真實 repo 的檔案路徑",
      "source_url": "（選填）對應的真實連結，讓讀者可以自己點進去核對",
      "source_code": "（選填）真實、逐字抄錄自來源的程式碼純文字（不要加 HTML tag，腳本會自動 escape 並排版成等寬字體區塊）",
      "problems": [
        {"id": "200", "title": "Number of Islands",
         "url": "https://leetcode.com/problems/number-of-islands/",
         "note": "經典 grid BFS/DFS 連通分量題，時間 O(rows*cols) 空間 O(rows*cols)"}
      ],
      "tip_html": ""
    }
  ],
  "csapp": [
    {
      "chapter": "Ch.9",
      "section": "9.10 Garbage Collection",
      "explanation_html": "<p>...章節科普...</p>",
      "derivation_html": "<p>（選填）例如某個公式/常數/門檻值是怎麼推導出來的...</p>",
      "source_label": "（選填）例如 \"gcc -S 對應輸出\" 或某個真實檔案路徑＋行號",
      "source_url": "（選填）",
      "source_code": "（選填）真實的組語/程式碼/指令輸出純文字",
      "tip_html": "<p>（選填）額外補充，例如常考陷阱、與其他章節的關聯...</p>"
    }
  ],
  "linux": [
    {
      "topic": "Memory Barriers（記憶體屏障）",
      "explanation_html": "<p>...Linux Kernel 主題科普，強調是 CS:APP 概念的具體實作...</p>",
      "derivation_html": "<p>（選填）...</p>",
      "source_label": "（選填，Linux Kernel 領域強烈建議每天都要有）例如 \"kernel.org cgit · include/linux/list.h#L54-L61\"",
      "source_url": "（選填）對應的真實 cgit / GitHub 連結，含行號錨點",
      "source_code": "（選填）逐字抄錄自真實核心原始碼的純文字片段",
      "tip_html": "<p>（選填）額外補充...</p>"
    }
  ],
  "sources": [
    {"label": "LeetCode 題目彙整", "url": "https://github.com/wisdompeak/LeetCode"},
    {"label": "CS:APP 筆記", "url": "https://hackmd.io/@sysprog/CSAPP"}
  ]
}

`algo`/`csapp`/`linux` 現在都是**長度為 1 的陣列**（每個領域當天只講一個主題，但講得更深、
更完整）。腳本本身不限制陣列長度，若未來需求改變也能容納多個子主題，但目前的 Routine 規則是
每天每個領域固定只放 1 個項目。`theme` 欄位（選填）用一句話點出貫穿當天三個領域的關聯，
會顯示在信件最上方；沒有自然關聯就整個省略這個 key，不要硬湊。

每個項目的 `tip_html`、`derivation_html`、`source_label`／`source_url`／`source_code` 都是
選填欄位（沒有內容就給空字串或不放這個 key，不會渲染對應框）。

`derivation_html`（🔢 數學推導區塊）：只要內容涉及公式、複雜度、常數、門檻值、位元寬度等
「數字」，且有「為什麼是這樣」值得講的地方，就填入這個欄位，會渲染成一個用固定紫色
（跨三個領域都一樣，不隨 accent 變色，方便一眼認出這是「數學推導」區塊）標示的獨立框，
和 `tip_html` 的補充框並列但視覺上可區分。若該主題今天沒有明顯的數字/公式成分，就不要
硬湊，留空或不放這個 key 即可。

`source_code`（📄 原始碼區塊）：放**真實存在、逐字抄錄**的原始碼／組語／指令輸出，會渲染成
深色等寬字體的程式碼框，跟用白話描述的 `explanation_html` 視覺上明顯區隔開來，讓讀者一眼
就知道「這段是真的抄自原始出處，不是我用文字重述的」。`source_label` 是這段程式碼的出處
標示（檔案路徑＋行號、或指令名稱），會顯示在程式碼框上方；`source_url` 是可點擊核對的真實
連結。三個欄位要嘛一起出現、要嘛都不放——**絕對不要編造看起來像真的、但其實是憑空想像的
路徑／行號／程式碼**，找不到可信原始碼來源時就整個省略這一組欄位，寧可沒有也不要造假。

行內 `<code>`／`<pre>` 的樣式**固定由這支腳本統一決定，內容 JSON 完全不需要、也不應該自己
加 style**：`explanation_html`／`tip_html`／`derivation_html` 裡只要寫最單純的
`<code>0x1234</code>` 或 `<pre>...</pre>`，腳本會自動幫它們套上跟 `source_code` 大區塊
同一套深色底樣式（見 `autostyle_code()`），確保每天輸出的視覺風格完全一致，不會因為當天
內容有沒有手動加樣式而有落差。如果 HTML 裡的 `<code>`／`<pre>` 已經自帶 `style=`，腳本不會
覆蓋它——但正常情況下不需要自己加。

進階名詞小框框：三個領域每個子項目的 `explanation_html` 內文裡，若提到需要額外解釋的
進階概念，直接在該處內文插入以下固定樣式的行內框（依所在領域套對應強調色，不要用其他顏色），
不要全部塞進 tip_html —— tip_html 只留給該子項目結尾的單一整體補充：

    <div style="margin:10px 0;padding:10px 14px;border:1px dashed #e2ddd0;border-radius:4px;font-size:13px;line-height:1.6;color:#7a766b;">
      <b style="color:{ACCENT};">名詞</b>　解釋文字...
    </div>

其中 {ACCENT} 依領域代入：algo → #2f5f9e，csapp → #b0561a，linux → #2c7357。

輸出：完整 <html>...</html> 字串（inline CSS，Gmail 相容），並在 stderr 印出建議的頁面標題。

設計方向：「技術手札」—— 見 STYLE.md。全部行內 CSS、寬 600px、table 版面；
三個領域（演算法／CS:APP／Linux Kernel）各自分色（藍／銅橘／森綠），領域標籤為實心 tab，
報頭下方有「今日目錄」。所有顏色與字型集中在下方 COLORS／字型常數。
"""

import json
import re
import sys

# ---- 固定視覺風格（所有顏色/字體都集中在這裡，確保每天輸出風格一致）----
COLORS = {
    "outer": "#f4f1ea",      # 外層底色
    "paper": "#fffefb",      # 信紙／頁面色
    "ink": "#22252b",
    "muted": "#7a766b",
    "rule": "#e2ddd0",
    "algo": "#2f5f9e",       # 藍墨水：演算法
    "csapp": "#b0561a",      # 銅橘：CS:APP
    "linux": "#2c7357",      # 森綠：Linux Kernel
    "review": "#a8751f",     # 複習標記專用
    "derivation": "#6b4a9a", # 紫：數學推導專用，跨領域固定同一色
    "derivation_bg": "#f6f2fb",
    "code_bg": "#22252b",    # 深色：真實原始碼區塊背景
    "code_text": "#ece8dd",
    "code_muted": "#a39d90",
}

MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"
SERIF = "Georgia,'Noto Serif TC',serif"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang TC','Microsoft JhengHei',sans-serif"
CODE_FONT = MONO

WEEKDAYS = "一二三四五六日"

LEGACY_COLORS = {"#e7e4dd": COLORS["rule"], "#918e85": COLORS["muted"], "#7089a0": COLORS["algo"],
                 "#c98a4b": COLORS["csapp"], "#5f8575": COLORS["linux"]}


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def weekday_label(date: str) -> str:
    from datetime import datetime
    try:
        d = datetime.strptime(date, "%Y-%m-%d")
        return f"{date}（週{WEEKDAYS[d.weekday()]}）"
    except ValueError:
        return date


# 內文裡隨手寫的 <code>...</code>／<pre>...</pre>，固定套上深色底，
# 樣式由這支腳本統一決定。已經自帶 style 屬性的標籤不會被覆蓋。
# 用 background-color（而非 background 簡寫）：Gmail 對簡寫支援不穩定。
def _code_css() -> str:
    return (
        f"background-color:{COLORS['code_bg']};color:{COLORS['code_text']};"
        f"padding:1px 6px;border-radius:4px;font-family:{CODE_FONT};font-size:0.92em;"
    )


def _pre_css() -> str:
    return (
        f"display:block;margin:10px 0;background-color:{COLORS['code_bg']};color:{COLORS['code_text']};"
        f"padding:12px 14px;border-radius:4px;font-family:{CODE_FONT};font-size:12.5px;"
        f"line-height:1.6;white-space:pre-wrap;word-break:break-word;overflow-x:auto;"
    )


def autostyle_code(html: str) -> str:
    """幫內文裡沒有自帶 style 的 <code>/<pre> 標籤補上固定的深色底樣式。"""
    if not html:
        return html
    # 舊版配色（北歐極簡）自動換成新色票，讓舊格式的內文也一致
    for old_c, new_c in LEGACY_COLORS.items():
        html = html.replace(old_c, new_c)
    html = re.sub(r"<code(?![^>]*\bstyle=)>", f'<code style="{_code_css()}">', html)
    html = re.sub(r"<pre(?![^>]*\bstyle=)>", f'<pre style="{_pre_css()}">', html)
    return html


def label_css(color: str) -> str:
    return f"font-family:{MONO};font-size:11px;letter-spacing:1.5px;color:{color};text-transform:uppercase;"


def render_problem(p: dict, accent: str) -> str:
    pid = esc(str(p.get("id", "")))
    title = esc(p.get("title", ""))
    url = p.get("url", "#")
    note = esc(p.get("note", ""))
    note_html = (
        f'<div style="margin-top:2px;color:{COLORS["muted"]};font-size:13px;line-height:1.6;padding-left:2px;">{note}</div>'
        if note else ""
    )
    return f"""
    <div style="margin-top:10px;">
      <span style="display:inline-block;min-width:44px;text-align:center;border:1px solid {accent};border-radius:3px;padding:0 6px;font-family:{MONO};font-size:12px;color:{accent};">{pid}</span>
      <a href="{url}" style="margin-left:8px;color:{COLORS['ink']};font-size:15px;text-decoration:underline;">{title}</a>
      {note_html}
    </div>"""


def render_tip(accent: str, tip_html: str) -> str:
    if not tip_html:
        return ""
    return f"""
    <div style="margin-top:14px;border:1px dashed {COLORS['rule']};border-radius:4px;padding:12px 16px;">
      <div style="{label_css(accent)}">NOTE · 補充</div>
      <div style="margin-top:6px;font-size:13.5px;line-height:1.75;color:{COLORS['muted']};">
        {autostyle_code(tip_html)}
      </div>
    </div>"""


def render_derivation(derivation_html: str) -> str:
    if not derivation_html:
        return ""
    accent = COLORS["derivation"]
    return f"""
    <div style="margin-top:14px;border:1px solid {accent};background-color:{COLORS['derivation_bg']};border-radius:4px;padding:12px 16px;">
      <div style="{label_css(accent)}">🔢 數學推導</div>
      <div style="margin-top:6px;font-size:13.5px;line-height:1.75;color:{COLORS['ink']};">
        {autostyle_code(derivation_html)}
      </div>
    </div>"""


def render_source(label: str, url: str, code: str) -> str:
    if not code:
        return ""
    label_html = ""
    if label or url:
        label_text = esc(label)
        label_inner = (
            f'<a href="{url}" style="color:{COLORS["code_muted"]};text-decoration:underline;">{label_text}</a>'
            if url else label_text
        )
        label_html = f'<div style="margin-top:8px;font-size:12px;color:{COLORS["code_muted"]};">{label_inner}</div>'
    return f"""
    <div style="margin-top:14px;border-radius:4px;padding:14px 16px;background-color:{COLORS['code_bg']};">
      <div style="{label_css(COLORS['code_muted'])}">📄 原始碼</div>
      {label_html}<pre style="margin:8px 0 0;font-family:{CODE_FONT};font-size:12.5px;line-height:1.6;color:{COLORS['code_text']};white-space:pre-wrap;word-break:break-word;">{esc(code)}</pre>
    </div>"""


def render_item(accent: str, index: int, heading: str, body_html: str, tip_html: str = "", extra_html: str = "", derivation_html: str = "", source_label: str = "", source_url: str = "", source_code: str = "") -> str:
    top_margin = "20px" if index == 0 else "30px"
    return f"""
    <div style="margin-top:{top_margin};">
      <div style="font-family:{MONO};font-size:11px;color:{accent};letter-spacing:1px;">§{index + 1:02d}</div>
      <div style="margin-top:4px;font-family:{SERIF};font-size:20px;font-weight:700;line-height:1.4;color:{accent};">{esc(heading)}</div>
      <div style="margin-top:12px;border-left:3px solid {accent};padding-left:14px;font-size:14.5px;line-height:1.85;color:{COLORS['ink']};">
        {autostyle_code(body_html)}
      </div>
      {extra_html}
      {render_derivation(derivation_html)}
      {render_source(source_label, source_url, source_code)}
      {render_tip(accent, tip_html)}
    </div>"""


def render_domain(accent: str, tab: str, items: list, item_heading_fn, extra_fn=None, first: bool = False) -> str:
    body = "".join(
        render_item(
            accent, i,
            item_heading_fn(item),
            item.get("explanation_html", ""),
            item.get("tip_html", ""),
            extra_fn(item, accent) if extra_fn else "",
            item.get("derivation_html", ""),
            item.get("source_label", ""),
            item.get("source_url", ""),
            item.get("source_code", ""),
        )
        for i, item in enumerate(items)
    )
    sep = "" if first else f'<div style="margin-top:34px;border-top:1px solid {COLORS["rule"]};"></div>'
    return f"""
    {sep}
    <div style="margin-top:28px;border-bottom:2px solid {accent};">
      <span style="display:inline-block;background-color:{accent};color:#ffffff;padding:4px 12px;font-family:{MONO};font-size:11px;letter-spacing:1.5px;text-transform:uppercase;">{esc(tab)}</span>
    </div>
    {body}"""


def render_toc(rows: list) -> str:
    """今日目錄：rows = [(領域簡稱, 色, 子主題)]，內容直接取自各領域標題。"""
    trs = "".join(
        f"""
      <tr>
        <td width="14" style="padding:5px 0;"><div style="width:9px;height:9px;background-color:{color};"></div></td>
        <td width="96" style="padding:5px 0;font-family:{MONO};font-size:11.5px;color:{COLORS['muted']};">{esc(name)}</td>
        <td style="padding:5px 0;font-size:14px;color:{COLORS['ink']};">{esc(title)}</td>
      </tr>"""
        for name, color, title in rows
    )
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px;">{trs}</table>'


def render(data: dict) -> str:
    date = data.get("date", "")
    is_review = bool(data.get("is_review"))
    theme = data.get("theme", "")
    algo = data.get("algo", []) or []
    csapp = data.get("csapp", []) or []
    linux = data.get("linux", []) or []
    sources = data.get("sources", []) or []

    review_tag = (
        f'<span style="margin-left:8px;padding:1px 8px;border:1px solid {COLORS["review"]};border-radius:3px;color:{COLORS["review"]};">複習</span>'
        if is_review else ""
    )

    theme_html = (
        f'<div style="margin-top:14px;border-left:2px solid {COLORS["ink"]};padding-left:12px;font-family:{SERIF};font-size:14.5px;line-height:1.8;color:{COLORS["ink"]};font-style:italic;">{esc(theme)}</div>'
        if theme else ""
    )

    algo_head = lambda item: item.get("topic", "")
    csapp_head = lambda item: f'{item.get("chapter", "")}　{item.get("section", "")}'.strip("　 ")
    linux_head = lambda item: item.get("topic", "")

    toc_rows = (
        [("演算法", COLORS["algo"], algo_head(i)) for i in algo]
        + [("CS:APP", COLORS["csapp"], csapp_head(i)) for i in csapp]
        + [("Linux Kernel", COLORS["linux"], linux_head(i)) for i in linux]
    )

    algo_section = render_domain(
        COLORS["algo"], "A · 演算法 · LeetCode", algo, algo_head,
        lambda item, accent: "".join(render_problem(p, accent) for p in item.get("problems", [])),
        first=True,
    )
    csapp_section = render_domain(COLORS["csapp"], "B · CS:APP", csapp, csapp_head)
    linux_section = render_domain(COLORS["linux"], "C · Linux Kernel", linux, linux_head)

    sources_links = "　·　".join(
        f'<a href="{s.get("url", "#")}" style="color:{COLORS["muted"]};text-decoration:underline;">{esc(s.get("label", ""))}</a>'
        for s in sources
    )
    sources_html = (
        f'<div style="margin-top:34px;padding-top:14px;border-top:1px solid {COLORS["rule"]};font-family:{MONO};font-size:11.5px;line-height:2;color:{COLORS["muted"]};">{sources_links}</div>'
        if sources_links else ""
    )

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>每日東東 · {esc(date)}</title></head>
<body style="margin:0;padding:0;background-color:{COLORS['outer']};font-family:{FONT};">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:{COLORS['outer']};padding:28px 12px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background-color:{COLORS['paper']};border:1px solid {COLORS['rule']};">
          <tr>
            <td style="padding:32px 24px 36px 24px;">
              <div style="{label_css(COLORS['muted'])}">DAILY LEARNING NOTE</div>
              <div style="margin-top:8px;font-family:{SERIF};font-size:28px;font-weight:700;color:{COLORS['ink']};line-height:1.25;">每日東東</div>
              <div style="margin-top:10px;font-family:{MONO};font-size:12px;color:{COLORS['muted']};">{esc(weekday_label(date))}{review_tag}</div>
              {theme_html}
              <div style="margin-top:22px;border-bottom:3px double {COLORS['ink']};"></div>
              {render_toc(toc_rows)}
              {algo_section}
              {csapp_section}
              {linux_section}
              {sources_html}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def main():
    raw = sys.stdin.read() if len(sys.argv) < 2 else open(sys.argv[1], encoding="utf-8").read()
    data = json.loads(raw)

    print(render(data))

    date = data.get("date", "")
    algo_topics = "、".join(i.get("topic", "") for i in data.get("algo", []))
    review_tag = "（複習）" if data.get("is_review") else ""
    print(f"TITLE: [{date}] 每日東東：{algo_topics}{review_tag}", file=sys.stderr)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
render_email.py — 產生「每日學習信」的固定風格 HTML 內容。

用途：
每天的 Routine 只需要把當天的教學內容整理成一份 JSON（結構見下方 SAMPLE），
餵給這支 script，就能得到一份排版、配色都固定一致的 HTML email 內容，
直接丟給 Gmail 的 send_message(htmlBody=...) 使用。

用法：
    python3 scripts/render_email.py input.json > output.html
    # 或
    cat input.json | python3 scripts/render_email.py > output.html

JSON 格式（欄位說明）：
{
  "date": "2026-08-18",
  "is_review": false,              // true 則內文會標注「複習」
  "algo": {
    "topic": "Sliding Window",
    "explanation_html": "<p>...核心概念說明（可含 <b>、<code>、<ul> 等基本標籤）...</p>",
    "problems": [
      {"id": "3", "title": "Longest Substring Without Repeating Characters",
       "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
       "note": "經典模板題，練習雙指針 + hashset"}
    ]
  },
  "csapp": {
    "chapter": "Ch.6",
    "section": "6.3 快取記憶體的組織方式",
    "explanation_html": "<p>...章節科普...</p>",
    "tip_html": "<p>（選填）額外補充，例如常考陷阱、與其他章節的關聯...</p>"
  },
  "linux": {
    "topic": "Process Scheduling（CFS）",
    "explanation_html": "<p>...Linux Kernel 主題科普，強調是 CS:APP 概念的具體實作...</p>",
    "tip_html": "<p>（選填）額外補充...</p>"
  },
  "sources": [
    {"label": "LeetCode 題目彙整", "url": "https://github.com/wisdompeak/LeetCode"},
    {"label": "CS:APP 筆記", "url": "https://hackmd.io/@sysprog/CSAPP"}
  ]
}

`algo`/`linux` 的 `tip_html` 用法與 `csapp.tip_html` 相同（選填欄位，沒有就不放這個 key，不會渲染補充框）。

進階名詞小框框：三個區塊的 `explanation_html` 內文裡，若提到需要額外解釋的進階概念，
直接在該處內文插入以下固定樣式的行內框（依所在區塊套對應強調色，不要用其他顔色），
不要全部塞進 tip_html —— tip_html 只留給段落結尾的單一整體補充：

    <div style="margin:10px 0;padding:10px 14px;border:1px dashed #e7e4dd;border-radius:6px;font-size:13px;line-height:1.6;color:#918e85;">
      <b style="color:{ACCENT};">名詞</b>　解釋文字...
    </div>

其中 {ACCENT} 依區塊代入：algo → #7089a0，csapp → #c98a4b，linux → #5f8575。

輸出：完整 <html>...</html> 字串（inline CSS，Gmail 相容），並在 stderr 印出建議的 email 主旨。

設計方向：北歐極簡風 —— 單一無襯線字體、大量留白、克制但不失溫度的用色。
不設大標題，日期後直接接內容；小標題與段落左側重點線用同一個強調色標記，
段落之間靠留白與極細分隔線區隔；有補充內容時，用一個虛線圍住的區域呈現。
三個領域（演算法／CS:APP／Linux Kernel）各自狜立分色，依序排列。
"""

import json
import sys

# ---- 固定視覺風格（所有顏色/字體都集中在這裡，確保每天輸出風格一致）----
COLORS = {
    "paper": "#faf9f7",
    "ink": "#2a2a27",
    "muted": "#918e85",
    "rule": "#e7e4dd",
    "accent": "#7089a0",    # 灰藍：連結、頁首等全篇通用元素
    "algo": "#7089a0",      # 灰藍：演算法區塊小標題／重點線
    "csapp": "#c98a4b",     # 淺橘：CS:APP 區塊小標題／重點線
    "linux": "#5f8575",     # 灰綠：Linux Kernel 區塊小標題／重點線
    "review": "#a8875b",    # 複習標記專用，極少量使用
}

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang TC','Microsoft JhengHei',sans-serif"


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_problem(p: dict) -> str:
    pid = esc(str(p.get("id", "")))
    title = esc(p.get("title", ""))
    url = p.get("url", "#")
    note = esc(p.get("note", ""))
    note_html = (
        f'<div style="margin-top:2px;color:{COLORS["muted"]};font-size:13px;line-height:1.6;">{note}</div>'
        if note else ""
    )
    return f"""
    <div style="margin-top:12px;">
      <span style="color:{COLORS['algo']};font-size:13px;">{pid}　</span>
      <a href="{url}" style="color:{COLORS['ink']};font-size:15px;text-decoration:none;border-bottom:1px solid {COLORS['rule']};">{title}</a>
      {note_html}
    </div>"""


def render_tip(accent: str, tip_html: str) -> str:
    if not tip_html:
        return ""
    return f"""
    <div style="margin-top:14px;border:1px dashed {COLORS['rule']};border-radius:6px;padding:12px 16px;">
      <div style="font-size:11px;letter-spacing:.08em;color:{accent};text-transform:uppercase;">補充</div>
      <div style="margin-top:6px;font-size:13.5px;line-height:1.7;color:{COLORS['muted']};">
        {tip_html}
      </div>
    </div>"""


def render_section(accent: str, eyebrow: str, heading: str, body_html: str, tip_html: str = "", extra_html: str = "") -> str:
    return f"""
    <tr><td style="padding-top:36px;">
      <div style="font-size:12px;letter-spacing:.08em;color:{accent};text-transform:uppercase;">
        {esc(eyebrow)}
      </div>
      <div style="margin-top:8px;font-size:19px;font-weight:600;color:{accent};">
        {esc(heading)}
      </div>
      <div style="margin-top:12px;border-left:3px solid {accent};padding-left:14px;font-size:14.5px;line-height:1.8;color:{COLORS['ink']};">
        {body_html}
      </div>
      {render_tip(accent, tip_html)}
      {extra_html}
    </td></tr>"""


def render(data: dict) -> str:
    date = data.get("date", "")
    is_review = bool(data.get("is_review"))
    algo = data.get("algo", {}) or {}
    csapp = data.get("csapp", {}) or {}
    linux = data.get("linux", {}) or {}
    sources = data.get("sources", []) or []

    review_tag = (
        f'<span style="color:{COLORS["review"]};margin-left:8px;">複習</span>' if is_review else ""
    )

    problems_html = "".join(render_problem(p) for p in algo.get("problems", []))

    algo_section = render_section(
        COLORS["algo"], "演算法 · LeetCode",
        algo.get("topic", ""),
        algo.get("explanation_html", ""),
        algo.get("tip_html", ""),
        problems_html,
    )

    csapp_chapter = f'{csapp.get("chapter", "")}　{csapp.get("section", "")}'.strip("　 ")
    csapp_section = render_section(
        COLORS["csapp"], "CS:APP",
        csapp_chapter,
        csapp.get("explanation_html", ""),
        csapp.get("tip_html", ""),
    )

    linux_section = render_section(
        COLORS["linux"], "Linux Kernel",
        linux.get("topic", ""),
        linux.get("explanation_html", ""),
        linux.get("tip_html", ""),
    ) if linux else ""

    sources_links = "　　".join(
        f'<a href="{s.get("url", "#")}" style="color:{COLORS["accent"]};text-decoration:none;">{esc(s.get("label", ""))}</a>'
        for s in sources
    )
    sources_html = (
        f'<div style="margin-top:24px;font-size:12px;color:{COLORS["muted"]};">{sources_links}</div>'
        if sources_links else ""
    )

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:{COLORS['paper']};font-family:{FONT};">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{COLORS['paper']};padding:40px 0;">
    <tr>
      <td align="center">
        <table role="presentation" width="560" cellpadding="0" cellspacing="0" style="width:560px;max-width:90vw;">
          <tr>
            <td>
              <div style="font-size:12px;color:{COLORS['muted']};">
                {esc(date)}　每日東東{review_tag}
              </div>
              <div style="margin-top:16px;border-bottom:1px solid {COLORS['rule']};"></div>
            </td>
          </tr>
          {algo_section}
          <tr><td style="padding-top:32px;border-bottom:1px solid {COLORS['rule']};"></td></tr>
          {csapp_section}
          <tr><td style="padding-top:32px;border-bottom:1px solid {COLORS['rule']};"></td></tr>
          {linux_section}
          <tr><td>{sources_html}</td></tr>
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
    topic = data.get("algo", {}).get("topic", "")
    chapter = data.get("csapp", {}).get("chapter", "")
    review_tag = "（複習）" if data.get("is_review") else ""
    print(f"SUBJECT: 今日學習：{topic} + CS:APP {chapter}{review_tag}", file=sys.stderr)


if __name__ == "__main__":
    main()

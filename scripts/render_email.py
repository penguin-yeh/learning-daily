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
  "is_review": false,                 // true 則主旨/內文會標注「複習」
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
    "explanation_html": "<p>...章節科普...</p>"
  },
  "sources": [
    {"label": "LeetCode 題目彙整", "url": "https://github.com/wisdompeak/LeetCode"},
    {"label": "CS:APP 筆記", "url": "https://hackmd.io/@sysprog/CSAPP"}
  ]
}

輸出：完整 <html>...</html> 字串（inline CSS，Gmail 相容），並在 stderr 印出建議的 email 主旨。
"""

import json
import sys


# ---- 固定視覺風格（所有顏色/字體都集中在這裡，確保每天輸出風格一致）----
COLORS = {
    "bg": "#f4f5f7",
    "card_bg": "#ffffff",
    "text": "#1f2430",
    "muted": "#6b7280",
    "algo_accent": "#2563eb",   # 藍：演算法區塊
    "algo_accent_bg": "#eff6ff",
    "csapp_accent": "#059669",  # 綠：CS:APP 區塊
    "csapp_accent_bg": "#ecfdf5",
    "badge_review_bg": "#fef3c7",
    "badge_review_text": "#92400e",
    "border": "#e5e7eb",
    "link": "#2563eb",
}

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang TC','Microsoft JhengHei',sans-serif"


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_problem(p: dict) -> str:
    pid = esc(str(p.get("id", "")))
    title = esc(p.get("title", ""))
    url = p.get("url", "#")
    note = esc(p.get("note", ""))
    return f"""
    <tr>
      <td style="padding:10px 14px;border:1px solid {COLORS['border']};border-radius:8px;display:block;margin-bottom:8px;">
        <div style="font-size:14px;color:{COLORS['muted']};">#{pid}</div>
        <a href="{url}" style="font-size:16px;font-weight:600;color:{COLORS['link']};text-decoration:none;">{title}</a>
        <div style="font-size:13px;color:{COLORS['muted']};margin-top:4px;">{note}</div>
      </td>
    </tr>
    """


def render(data: dict) -> str:
    date = esc(data.get("date", ""))
    is_review = bool(data.get("is_review", False))
    algo = data.get("algo", {})
    csapp = data.get("csapp", {})
    sources = data.get("sources", [])

    review_badge = ""
    if is_review:
        review_badge = f"""<span style="display:inline-block;background:{COLORS['badge_review_bg']};color:{COLORS['badge_review_text']};font-size:12px;font-weight:600;padding:3px 10px;border-radius:999px;margin-left:8px;">複習</span>"""

    problems_html = "\n".join(render_problem(p) for p in algo.get("problems", []))

    sources_html = ""
    if sources:
        items = "".join(
            f'<li style="margin-bottom:4px;"><a href="{s.get("url","#")}" style="color:{COLORS["link"]};text-decoration:none;">{esc(s.get("label",""))}</a></li>'
            for s in sources
        )
        sources_html = f"""
        <div style="margin-top:24px;padding-top:16px;border-top:1px solid {COLORS['border']};">
          <div style="font-size:12px;color:{COLORS['muted']};margin-bottom:6px;">參考來源</div>
          <ul style="margin:0;padding-left:18px;font-size:13px;color:{COLORS['muted']};">{items}</ul>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:{COLORS['bg']};font-family:{FONT};">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{COLORS['bg']};padding:24px 0;">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background:{COLORS['card_bg']};border-radius:12px;overflow:hidden;max-width:600px;width:100%;">

          <!-- Header -->
          <tr>
            <td style="padding:24px 28px 16px 28px;border-bottom:1px solid {COLORS['border']};">
              <div style="font-size:13px;color:{COLORS['muted']};">{date} ・ 每日學習信</div>
              <div style="font-size:20px;font-weight:700;color:{COLORS['text']};margin-top:4px;">
                {esc(algo.get('topic',''))} + CS:APP {esc(csapp.get('chapter',''))}{review_badge}
              </div>
            </td>
          </tr>

          <!-- Algo Section -->
          <tr>
            <td style="padding:24px 28px;">
              <div style="display:inline-block;background:{COLORS['algo_accent_bg']};color:{COLORS['algo_accent']};font-size:12px;font-weight:700;padding:4px 10px;border-radius:6px;letter-spacing:0.5px;">
                演算法主題
              </div>
              <div style="font-size:18px;font-weight:700;color:{COLORS['text']};margin-top:10px;">
                {esc(algo.get('topic',''))}
              </div>
              <div style="font-size:14px;line-height:1.7;color:{COLORS['text']};margin-top:8px;">
                {algo.get('explanation_html','')}
              </div>

              <div style="font-size:13px;font-weight:700;color:{COLORS['muted']};margin-top:18px;margin-bottom:8px;">
                對應 LeetCode 題目
              </div>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                {problems_html}
              </table>
            </td>
          </tr>

          <!-- CSAPP Section -->
          <tr>
            <td style="padding:0 28px 24px 28px;">
              <div style="display:inline-block;background:{COLORS['csapp_accent_bg']};color:{COLORS['csapp_accent']};font-size:12px;font-weight:700;padding:4px 10px;border-radius:6px;letter-spacing:0.5px;">
                CS:APP {esc(csapp.get('chapter',''))}
              </div>
              <div style="font-size:18px;font-weight:700;color:{COLORS['text']};margin-top:10px;">
                {esc(csapp.get('section',''))}
              </div>
              <div style="font-size:14px;line-height:1.7;color:{COLORS['text']};margin-top:8px;">
                {csapp.get('explanation_html','')}
              </div>
              {sources_html}
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:16px 28px;background:{COLORS['bg']};text-align:center;">
              <div style="font-size:12px;color:{COLORS['muted']};">持續累積，面試等級的理解就是這樣一天一天堆出來的 💪</div>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
    return html


def suggested_subject(data: dict) -> str:
    algo_topic = data.get("algo", {}).get("topic", "")
    chapter = data.get("csapp", {}).get("chapter", "")
    subject = f"今日學習：{algo_topic} + CS:APP {chapter}"
    if data.get("is_review"):
        subject += "（複習）"
    return subject


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    print(render(data))
    print(f"SUBJECT: {suggested_subject(data)}", file=sys.stderr)


if __name__ == "__main__":
    main()

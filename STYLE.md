# 每日東東（學習信）風格規範：「技術手札」

> 給負責產生本 repo 信件的 bot（Grok bot）：**產生任何一封信之前，先完整讀完這份文件並嚴格遵守。** 這是 Gmail HTML 信，不是網頁。
>
> **注意：** `scripts/render_email.py` 目前輸出的還是舊的「北歐極簡」配色與版面。本文件是新的目標樣式，兩者不一致時**以本文件為準**；若你有權修改腳本，請先把 `COLORS`、`FONT` 與各 `render_*` 函式改成符合本文件再產生信件，並一起 commit。內容欄位（JSON 結構）不變，不要新增欄位。

## 0. 硬性規則

1. **全部使用行內 CSS**，不准有 `<style>` 區塊、不准外部資源。Gmail 會拿掉 `<style>`、`background` 簡寫、`position`、`display:grid`，所以：
   - 底色一律寫 `background-color`，不要寫 `background`。
   - 版面用 `<table role="presentation">`，不要用 grid／flex。
2. 信件寬度上限 **600px**（外層 `width="100%"` 搭配 `max-width:600px`；不要寫 `width="600"`，手機會橫向捲動），手機不可橫向捲動。
3. 不准：漸層、陰影、emoji 裝飾（除了下面指定的 📄 與 🔢）、圖片。
4. 繁體中文。程式碼、組語、路徑與行號必須**逐字抄錄真實來源**，找不到就整組省略，不准編造。
5. 深度優先：每個領域只講一個具體的窄子主題（見 `ROUTINE_PROMPT.md`），版面不要為了好看而加內容。

## 1. 設計 token

| 用途 | 值 |
|---|---|
| 外層底色 | `#f4f1ea` |
| 信紙色 | `#fffefb` |
| 邊框／分隔線 | `#e2ddd0` |
| 主文字 | `#22252b` |
| 次要文字 | `#7a766b` |
| 演算法色 | `#2f5f9e`（藍墨水） |
| CS:APP 色 | `#b0561a`（銅橘） |
| Linux Kernel 色 | `#2c7357`（森綠） |
| 數學推導 | 字 `#6b4a9a`、底 `#f6f2fb`（三個領域共用） |
| 原始碼區 | 底 `#22252b`、字 `#ece8dd`、次要字 `#a39d90` |
| 複習標記 | `#a8751f` |

字型：

- 內文：`-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang TC','Microsoft JhengHei',sans-serif`
- 標題、主題引言：`Georgia,'Noto Serif TC',serif`
- 標籤、編號、日期：`ui-monospace,'SF Mono',Menlo,Consolas,monospace`

領域色只用在三處：領域標籤（tab）、小標題、內文左側線。其餘一律用墨色與灰。

## 2. 版面順序

1. 外層與信紙（3.1）
2. 報頭：眉標、標題、日期、複習標記、主題引言（3.2）
3. **今日目錄**：三個領域各一行，點出今天的子主題（3.3，內容直接取自各領域 `topic`／`section`，不新增欄位）
4. 演算法 → CS:APP → Linux Kernel 三個領域區塊，順序固定，中間以細線分隔（3.4–3.9）
5. 參考來源連結列（3.10）

## 3. 區塊寫法

### 3.1 外層

```html
<body style="margin:0;padding:0;background-color:#f4f1ea">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f1ea;padding:28px 12px">
<tr><td align="center">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background-color:#fffefb;border:1px solid #e2ddd0">
<tr><td style="padding:32px 24px 36px 24px">
  …所有區塊（每個區塊用 <div> 或獨立 <table>）…
</td></tr></table>
</td></tr></table></body>
```

### 3.2 報頭

```html
<div style="font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:11px;letter-spacing:2px;color:#7a766b;text-transform:uppercase">DAILY LEARNING NOTE</div>
<div style="font-family:Georgia,'Noto Serif TC',serif;font-size:28px;font-weight:700;color:#22252b;line-height:1.25;margin-top:8px">每日東東</div>
<div style="font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:12px;color:#7a766b;margin-top:10px">YYYY-MM-DD（週X）
  <!-- 複習日才放 --><span style="margin-left:8px;padding:1px 8px;border:1px solid #a8751f;border-radius:3px;color:#a8751f">複習</span>
</div>
<!-- theme 有才放，沒有整塊省略 -->
<div style="margin-top:14px;border-left:2px solid #22252b;padding-left:12px;font-family:Georgia,'Noto Serif TC',serif;font-size:14.5px;line-height:1.8;color:#22252b;font-style:italic">一句話主題引言</div>
<div style="margin-top:22px;border-bottom:3px double #22252b"></div>
```

### 3.3 今日目錄

三行，每行：領域色小方塊、領域簡稱、今天的子主題。

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px">
  <tr>
    <td width="14" style="padding:5px 0"><div style="width:9px;height:9px;background-color:#2f5f9e"></div></td>
    <td width="96" style="padding:5px 0;font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:11.5px;color:#7a766b">演算法</td>
    <td style="padding:5px 0;font-size:14px;color:#22252b">子主題名稱</td>
  </tr>
  <!-- CS:APP 方塊 #b0561a、Linux 方塊 #2c7357，同結構 -->
</table>
```

### 3.4 領域標籤（tab）與領域區塊

領域之間用 `<div style="margin-top:34px;border-top:1px solid #e2ddd0"></div>` 分隔。領域標籤是一塊實心小標籤，底下一條同色 2px 線：

```html
<div style="margin-top:28px;border-bottom:2px solid #2f5f9e">
  <span style="display:inline-block;background-color:#2f5f9e;color:#ffffff;padding:4px 12px;font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:11px;letter-spacing:1.5px;text-transform:uppercase">A · 演算法 · LeetCode</span>
</div>
```

標籤文字：`A · 演算法 · LeetCode`、`B · CS:APP`、`C · Linux Kernel`（色依序為藍、銅橘、森綠）。

### 3.5 子項目（每個領域目前固定一項）

```html
<div style="margin-top:20px">
  <div style="font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:11px;color:#2f5f9e;letter-spacing:1px">§01</div>
  <div style="margin-top:4px;font-family:Georgia,'Noto Serif TC',serif;font-size:20px;font-weight:700;line-height:1.4;color:#2f5f9e">子主題標題</div>
  <div style="margin-top:12px;border-left:3px solid #2f5f9e;padding-left:14px;font-size:14.5px;line-height:1.85;color:#22252b">…explanation_html…</div>
  <!-- 依序：problems（演算法）、derivation、source_code、tip -->
</div>
```

CS:APP 標題格式：`Ch.X　X.Y 小節名`（章節編號在前）。

### 3.6 行內程式碼與進階名詞小框

- `<code>`：`background-color:#22252b;color:#ece8dd;padding:1px 6px;border-radius:4px;font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:0.92em`
- `<pre>`：`display:block;margin:10px 0;background-color:#22252b;color:#ece8dd;padding:12px 14px;border-radius:4px;font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:12.5px;line-height:1.6;white-space:pre-wrap;word-break:break-word`
- 進階名詞小框（放在內文裡，用該領域色當名詞色）：

```html
<div style="margin:10px 0;padding:10px 14px;border:1px dashed #e2ddd0;border-radius:4px;font-size:13px;line-height:1.6;color:#7a766b"><b style="color:{領域色};">名詞</b>　解釋文字…</div>
```

### 3.7 LeetCode 題目列（只有演算法有）

```html
<div style="margin-top:10px">
  <span style="display:inline-block;min-width:44px;text-align:center;border:1px solid #2f5f9e;border-radius:3px;padding:0 6px;font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:12px;color:#2f5f9e">200</span>
  <a href="題目網址" style="margin-left:8px;color:#22252b;font-size:15px;text-decoration:underline">題目名稱</a>
  <div style="margin-top:2px;color:#7a766b;font-size:13px;line-height:1.6;padding-left:2px">一句話說明與複雜度</div>
</div>
```

### 3.8 數學推導（有數字、公式、門檻值才放）

```html
<div style="margin-top:14px;border:1px solid #6b4a9a;background-color:#f6f2fb;border-radius:4px;padding:12px 16px">
  <div style="font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:11px;letter-spacing:1.5px;color:#6b4a9a;text-transform:uppercase">🔢 數學推導</div>
  <div style="margin-top:6px;font-size:13.5px;line-height:1.75;color:#22252b">…derivation_html…</div>
</div>
```

### 3.9 原始碼與補充

原始碼區（`source_label`／`source_url`／`source_code` 三者齊全才放）：

```html
<div style="margin-top:14px;border-radius:4px;padding:14px 16px;background-color:#22252b">
  <div style="font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:11px;letter-spacing:1.5px;color:#a39d90;text-transform:uppercase">📄 原始碼</div>
  <div style="margin-top:8px;font-size:12px;color:#a39d90"><a href="來源網址" style="color:#a39d90;text-decoration:underline">來源標示（檔案路徑＋行號）</a></div>
  <pre style="margin:8px 0 0;font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:12.5px;line-height:1.6;color:#ece8dd;white-space:pre-wrap;word-break:break-word">逐字原始碼</pre>
</div>
```

補充框（`tip_html` 有才放，虛線框，標籤用領域色）：

```html
<div style="margin-top:14px;border:1px dashed #e2ddd0;border-radius:4px;padding:12px 16px">
  <div style="font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:11px;letter-spacing:1.5px;color:#2f5f9e;text-transform:uppercase">NOTE · 補充</div>
  <div style="margin-top:6px;font-size:13.5px;line-height:1.75;color:#7a766b">…tip_html…</div>
</div>
```

### 3.10 參考來源

```html
<div style="margin-top:34px;padding-top:14px;border-top:1px solid #e2ddd0;font-family:ui-monospace,'SF Mono',Menlo,Consolas,monospace;font-size:11.5px;line-height:2;color:#7a766b">
  <a href="網址" style="color:#7a766b;text-decoration:underline">來源標籤</a>　·　<a href="網址" style="color:#7a766b;text-decoration:underline">來源標籤</a>
</div>
```

## 4. 檢查清單

- [ ] 沒有 `<style>`、`class=`、`background:`（只用 `background-color`）。
- [ ] 顏色全部來自第 1 節；領域色只出現在 tab、小標題、左側線、題號框、名詞小框標籤。
- [ ] 今日目錄三行，文字與下面三個領域的標題一致。
- [ ] 原始碼是逐字真實抄錄，且 label、url、code 三者齊全或整組省略。
- [ ] 信件 HTML 沒有被 escape 過（寄出後用 `get_message` 讀回 snippet 確認不是 `&lt;`）。
- [ ] 手機寬度不橫向捲動。
- [ ] 主旨格式維持 `ROUTINE_PROMPT.md` 的規定。

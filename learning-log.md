# 學習紀錄（Daily Learning Log）

> 由「每日學習信」Routine 自動維護。每次寄出當天的學習信後，會在下方 append 一行紀錄，
> 格式：`YYYY-MM-DD | 演算法: [主題] | 題目: [題號]`（若當天也涵蓋 CS:APP／Linux 進度，會另外加上對應欄位）
> Routine 會依照最近 14 天的紀錄，挑選尚未教過的主題；若都教過則允許複習並在信件標題加註「（複習）」。
> 註：CS:APP／Linux／演算法（LeetCode）三個領域的教學進度已於 2026-08-24 全部重置，歷史紀錄已清空。下次執行視為從頭開始：CS:APP 從 Ch.1 開始、Linux 從成大課程進度表第一週開始、演算法不再受近 14 天避重複限制。
> 註（2026-09-02 補記）：2026-08-27～2026-09-01 這六天的執行 session 各自被指派到獨立、彼此不相通的 git 分支，寄出的信件內容各不相同，但每個 session 更新的 learning-log.md 都沒有被 merge 回 main，導致 main 上的進度紀錄從 8/26 之後就沒再更新——這也是為什麼 CS:APP 連續好幾天都顯示同一個章節（§2.1.4）：每天的新 session 都是根據這份沒更新的 log 獨立算出「下一節」，才會一直算出同一個答案。以下六行是事後從各自的孤兒分支中找回、依實際寄信日期補登的紀錄，內容經比對 Gmail 寄件備份確認無誤。**由於 CS:APP §2.1.4、Linux EWMA／定點數這兩個主題實際上已經被連續教了很多天，下一次執行請直接跳到 CS:APP §2.1.5、Linux Kernel 週次表的下一個新主題，不要再重複。**

<!-- LOG START -->
主線: 鏈結串列的環狀結構 | 2026-08-25 | 演算法: 快慢指標與 Floyd 判圈演算法（141/142/876/202/287）| CS:APP: Ch.1 1.1–1.9 電腦系統導覽 | Linux: Linux 核心 Linked List 實作（container_of 與 intrusive linked list）
2026-08-26 | 演算法: 位元反轉的分治技巧 Reverse Bits／平行位元計數（190/191/338）| CS:APP: Ch.2 §2.1.3 Addressing and Byte Ordering（定址與位元組順序）| Linux: 第1週 ERR_PTR／PTR_ERR／IS_ERR 錯誤碼編碼進指標
2026-08-27 | 演算法: 單調堆疊 Monotonic Stack（739/503/84/42）| CS:APP: Ch.2 §2.1.4 Representing Strings（字串的表示法）| Linux: 第2週 整數表示法與 Bitwise 操作在核心中的應用（overflow.h／二補數／位元旗標）
2026-08-28 | 演算法: Union-Find（互斥集合／並查集）路徑壓縮與按秩合併（684/990/547/399/305）| CS:APP: Ch.2 §2.1.4 Representing Strings（字串表示法）| Linux: 第1週 解讀計算機編碼：二補數（Two's Complement）的數學設計與資安意涵
主線: 字串的位元組表示 | 2026-08-29 | 演算法: Sliding Window 滑動視窗，可變窗口與定長窗口兩種變形（3/76/239/567）| CS:APP: Ch.2 §2.1.4 表示字串（Representing Strings，null-terminated 與資安關聯）| Linux: 第1週 核心定點數機制與 EWMA（Load Average 固定點運算實作，kernel/sched/loadavg.c）
2026-08-30 | 演算法: Backtracking 排列組合與剪枝框架（46/78/39/51）| CS:APP: Ch.2 §2.1.4 Representing Strings | Linux: 第1週 排序演算法（lib/list_sort.c 的 Bottom-up Merge Sort）
2026-08-31 | 演算法: 單調堆疊 Monotonic Stack（739/503/84/42/239）| CS:APP: Ch.2 2.1.4 Representing Strings | Linux: Load Average 的定點數（Fixed-Point）實作與核心避免浮點數的原因
2026-09-01 | 演算法: 併查集 Union-Find / Disjoint Set Union（684/990/1319/947）| CS:APP: Ch.2 2.1.4 Representing Strings | Linux: 核心定點數機制與 EWMA（DECLARE_EWMA 巨集）
2026-09-02 | 演算法: 單調堆疊 Monotonic Stack（739/84/42/496）| CS:APP: Ch.2 §2.1.4 Representing Strings（字串的表示法）| Linux: 第1週 核心定點數機制與 EWMA（DECLARE_EWMA，include/linux/average.h）
主線: 機器碼與 FPU/SIMD 暫存器本質上都只是一串位元組，語意來自解讀規則 | 2026-09-03 | 演算法: 二分搜尋於答案空間 Binary Search on Answer Space（875/1011/410/1482）| CS:APP: Ch.2 §2.1.5 Representing Code（程式碼的位元組表示，機器碼不具可攜性）| Linux: 第1週 核心浮點數限制的另一面：kernel_fpu_begin()/kernel_fpu_end() 臨界區間（AES-NI／RAID6 SIMD 例外使用）
<!-- LOG END -->

# HackMD 文件與獨立 Disqus 留言

## 目前決定（2026-09-15）

- 五個線上頁面繼續使用正式站既有的 HackMD 文件來源，保留原內容、排版、圖片與噗浪小工具。不維護本地 Markdown / HTML 副本。
- 積木頁在 HackMD iframe 外獨立載入 Disqus；不以 HackMD 的登入或留言功能作為本站留言入口。
- 正式入口統一為 https://papple23g-ahkcompiler.herokuapp.com 。先發布移除搬遷公告的版本，再撤掉新網址的 DNS 與 Heroku 綁定，不更動其他網域、App 或方案。
- 此決定取代原先的本地文件遷移與 giscus 評估；遷移程式、產物與自動匯入 CI 已撤回，可從 Git 歷史找回。

## 留言識別與行為

| 項目 | 值 |
| --- | --- |
| Forum shortname | `ahkcompiler` |
| Thread ID | `8080995238`（查證用，不當作 page.identifier） |
| page.identifier | `r1RuM08tB` |
| page.url | `https://hackmd.io/%40papple23g/r1RuM08tB` |
| 原討論串 | https://disqus.com/home/discussion/ahkcompiler/ahk_hackmd_66/ |

以上識別值不隨本機或正式站 host 改變；不匯入、搬移或刪除歷史留言。

留言在主頁 load 完成後的下一個事件循環自動請求，讓 Brython 先開始初始化。實際開始請求後 20 秒仍未完成會顯示重試與原串入口；以 Disqus onReady 判定完成。其他頁面不載入 Disqus；離線積木頁只提供正式站留言連結。

只有積木頁使用 `Cross-Origin-Opener-Policy: same-origin-allow-popups`，保留 Google / Disqus 登入彈出視窗與原頁面的通知關係；其他頁面維持 Django 預設。參考 [Google 文件](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid?hl=en)及 [Disqus 固定識別文件](https://help.disqus.com/en/articles/1717137-use-configuration-variables-to-avoid-split-threads-and-missing-comments)。

## 驗證與限制

- 自動驗證：5 項 Django 測試覆蓋五頁原文件來源、本機與正式 host 回應一致、移除搬遷公告、留言載入範圍及 COOP；5 項離線匯出測試；6 項 Node 留言載入／重試測試。
- 2026-09-15 撤回遷移後，本機五頁的 HackMD iframe 均回應 200；關於頁恢復噗浪小工具及 mailto 連結。積木轉換實際產生 AHK 語法，填表頁切換 Alt 後語法同步更新，獨立 Disqus 顯示 210 則。HackMD 的 paragraphBookmark 403 與 PostHog 訊息在既有正式站也出現，不列為本站修復完成或零 console 錯誤。
- 先前本機 Chrome 驗證：210 則公開留言與巢狀回覆可見，Google 登入視窗關閉後身份自動更新。未送出測試留言，不宣稱已通過發表測試。這是先前紀錄，不取代本次正式站驗收。
- HackMD、Disqus、噗浪與外部圖片仍受第三方可用性及瀏覽器內容封鎖影響。Disqus 可能含廣告；不保證所有瀏覽器或隱私設定都能使用。
- RSS 只有最近 25 則，並非完整備份；先前與 embed 的 5 則共同樣本相差 5 小時，原因未確認，本次不改寫歷史時間。

```powershell
& 'C:\Users\pappl\venvs\ahkcompiler_venv\Scripts\python.exe' manage.py check
& 'C:\Users\pappl\venvs\ahkcompiler_venv\Scripts\python.exe' manage.py test --verbosity=2
& 'C:\Users\pappl\venvs\ahkcompiler_venv\Scripts\python.exe' -m unittest discover -s tests -v
node --test tests/comments.test.cjs
git diff --check
```

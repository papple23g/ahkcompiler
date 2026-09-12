# 網頁留言系統與歷史留言恢復

## 2026-09-12 決定：沿用既有 Disqus

已查證舊留言仍保存在 Disqus。本次在 `/ahkblockly` 的文件 iframe 外提供「載入留言」按鈕；Markdown 繼續由 repository 維護。本節取代下方原先尚未查明舊留言時的 giscus 建議。

| 項目 | 已確認值 |
| --- | --- |
| Forum shortname | `ahkcompiler` |
| Thread ID | `8080995238`（查證用途，不當作 page.identifier） |
| page.identifier | `r1RuM08tB` |
| page.url | `https://hackmd.io/%40papple23g/r1RuM08tB` |
| 原討論串 | [AHK 積木使用說明](https://disqus.com/home/discussion/ahkcompiler/ahk_hackmd_66/) |
| 查證時公開留言數 | 210 |
| 查證時狀態 | `isClosed=false`、`isDeleted=false` |

資料來自 Disqus 公開 embed 回應的 `disqus-threadData`，並已在 Chrome 本機網站留言框確認 210 則及原回覆。Forum 另有 12 則語法產生器留言，本次不混入。

### 整合與限制

- `static/comments.js` 僅在積木頁載入；按下按鈕後才請求 Disqus。20 秒未完成則顯示重試與原串入口；以 `onReady` 判定完成，不以腳本下載成功冒充留言已顯示。
- 新舊網域沿用相同原 URL / identifier，不使用目前瀏覽器網址識別留言。未修改 Disqus 後台、原串 URL 或匯入任何留言。
- 歷史 HackMD URL 僅作為 Disqus 識別資料，不是文件來源。文件檢查只豁免 `static/comments.js` 中該精確設定行，其餘筆記引用仍禁止。
- 留言區以局部樣式消除通用 iframe 浮動並限制寬度；文件 CSP 不放寬。
- 既有及未來離線積木頁只保留正式網站入口。匯出器透過 `scripts/offline_comments.py` 整段替換標記區塊，包含 Disqus 載入腳本。
- Disqus 可能提供廣告，目前不允許匿名發言。未代使用者登入或發布測試留言，實際送出未測試。
- [公開 RSS](https://ahkcompiler.disqus.com/latest.rss) 回傳最近 25 則，不能當成完整備份。完整備份需管理員另行[匯出](https://help.disqus.com/en/articles/1717164-comments-export)，不要將含私人資料的匯出檔提交至公開 repository。

### 驗證

```powershell
& C:\Users\pappl\venvs\ahkcompiler_venv\Scripts\python.exe -m unittest discover -s tests -v
& C:\Users\pappl\venvs\ahkcompiler_venv\Scripts\python.exe scripts/docs.py --check
node --test tests/comments.test.cjs
git diff --check
```

PR 底版使用 Django 1.11 的 `django.conf.urls.url`，本機環境為 Django 5.2.17。下列 alias 僅存在於驗證程序，不改 production 原始碼或 dependencies：

```powershell
& C:\Users\pappl\venvs\ahkcompiler_venv\Scripts\python.exe -c "import django.conf.urls; from django.urls import re_path; django.conf.urls.url = re_path; from django.core.management import execute_from_command_line; import os; os.environ['DJANGO_SETTINGS_MODULE']='ahkcompiler.settings'; execute_from_command_line(['manage.py','test','myapp','--verbosity=2'])"
```

本機 browser smoke 使用相同 alias 啟動 `runserver 127.0.0.1:8765 --noreload`；這不代表已驗證原 Django 1.11 production 環境。

驗收結果：8 項文件／離線測試、4 項 Node 載入流程測試、2 項 Django 頁面測試及文件生成檢查通過。Chrome 網站內可見 210 則、輸入框、登入入口與巢狀回覆，並可切換最新排序及載入更多留言。核對 RSS 中少偉Wiki 的函式提問及王竣平的回覆（`6151066857`、`6158571627`），另可讀到 2020 年留言。手機尺寸檢查中 iframe 內容寬度與 scrollWidth 同為 384px，未水平溢出；Blockly 預設範例仍能產生 AHK 語法。

Codex 內建瀏覽器此次 iframe 曾停留空白並觸發逾時，重試提示確實顯示；Chrome 同一頁及相同設定成功。內建瀏覽器相容性問題未標記為已修復。正式網域部署後仍須重驗嵌入與登入；本 PR 不部署。

整合依據：[官方 Embed Code](https://help.disqus.com/en/articles/1717112-universal-embed-code)、[避免分裂討論串](https://help.disqus.com/en/articles/1717137-use-configuration-variables-to-avoid-split-threads-and-missing-comments)。

## 初期評估（歷史紀錄；目前決定以上節為準）

HackMD 近期改版後，既有 iframe 內的留言體驗不再適合作為本站的留言入口。本次先將文件內容移回 repository；留言系統建議獨立於 Markdown 內容，避免再次把文件綁死在單一筆記平台。

## 建議：giscus

首選 **giscus**。本站 repository 已啟用 GitHub Discussions，而 giscus 將每個頁面的留言儲存在 GitHub Discussions：不需要另外維護資料庫、可直接在 GitHub 管理與封鎖留言、支援回覆與 reactions，也能以 pathname/title 等方式把頁面映射到固定討論串。

代價是留言者需要 GitHub 帳號並授權 giscus；對 AHK / 程式開發者社群通常可接受，但若目標是讓完全沒有 GitHub 帳號的一般使用者留言，這會增加門檻。

實作時建議：

1. 安裝 giscus GitHub App 到 `papple23g/ahkcompiler`，並建立專用 Discussion category（例如 `網站留言`）。
2. 以固定 key（例如文件 slug）映射 discussion，不依賴目前 Heroku URL，避免未來換網域後留言串失聯。
3. 在文件 iframe **外層的本站頁面**載入 giscus，而不是塞進產生的 Markdown HTML；如此離線版仍可完全離線，線上留言則只存在主站。
4. 加上 `giscus.json` 限制允許載入留言元件的 origin；正式網域確定後再設定。
5. 不把 giscus 的 `repo-id` / `category-id` 猜寫進程式碼；由 giscus 設定頁取得正確值後再做第二個小 PR。

## 其他方案

### utterances

也是無自建後端方案，但留言存在 GitHub Issues。優點是簡單、免費、無廣告；缺點是把網站留言混進 issue tracker，而且功能與討論結構比 Discussions 弱。既然此 repository 已開啟 Discussions，沒有明顯理由優先於 giscus。

### Waline

若「訪客不應被要求擁有 GitHub 帳號」是硬需求，Waline 比較適合。它有自己的 server、帳號/社群登入與多種資料庫支援，可部署到 Vercel / Docker / 自架環境。代價是多一套服務、資料庫、備份、反垃圾與維運工作。

### Disqus

整合成本低，也能用固定 identifier 維持頁面討論串。但它是第三方託管服務，資料與產品政策受外部平台控制；這次搬離 HackMD 的目的之一就是降低這種耦合，因此不建議作為新預設。若舊 HackMD 文件的 `disqus: ahkcompiler` 曾產生值得保留的歷史留言，可先調查能否以既有 Disqus shortname / identifier 找回，再決定是否做一次性遷移或保留唯讀入口。

## 結論

目前建議採 **「repository 內 Markdown + 線上頁面 giscus + 離線版不載入留言」**。這與現有 GitHub 開源專案的維護方式最一致，也把文件內容與留言服務拆開；未來即使再更換 Markdown renderer，Discussion 資料仍留在 repository 的 GitHub 社群空間。

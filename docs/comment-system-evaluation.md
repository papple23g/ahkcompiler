# 網頁留言系統評估

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

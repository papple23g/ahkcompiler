# 開發與維護

使用者操作與離線版下載見 [README](../README.md)。本專案使用 Django、Brython 與 Blockly；產生的腳本採用 AutoHotkey v1.1 語法。

## 本機環境（Windows / Python 3.12）

目前使用 Python 3.12、Django 5.2.17、Brython 3.11.3，AHK 輸出相容 AutoHotkey v1.1。Python 套件版本以 [`requirements.txt`](../requirements.txt) 為準。

在 repository 根目錄執行；使用專案外部的虛擬環境，已有環境可跳過建立及安裝步驟：

```powershell
uv venv "$env:USERPROFILE\venvs\ahkcompiler_venv" --python 3.12
& "$env:USERPROFILE\venvs\ahkcompiler_venv\Scripts\Activate.ps1"
uv pip install -r requirements.txt
python manage.py check
python manage.py test
python manage.py runserver 8000
```

開啟 [本機積木頁](http://127.0.0.1:8000/ahkblockly)。VS Code 選擇同一個外部環境即可啟動 Django 偵錯，不需暫時 alias。

`Failed to hardlink files; falling back to full copy` 表示 uv 改用複製安裝，不是啟動失敗原因；需要消除提示時可加 `--link-mode=copy`。

## 測試

```powershell
python manage.py check
python manage.py test
python -m unittest discover -s tests -v
node --test tests/ads.test.cjs tests/comments.test.cjs
git diff --check
```

Django 測試預設只探索 `myapp`，避免匯入供瀏覽器使用的 Brython 子模組。`unittest` 指令執行離線匯出及瀏覽器程式的 Python 測試；Node 指令驗證廣告與留言載入行為，需要已安裝 Node.js。

單獨執行 AHK 編譯測試：

```powershell
python -m unittest discover -s tests -p test_ahk_compile.py -v
python manage.py test myapp.test_compile
```

前端測試直接讀取並執行既有來源函數，驗證 XML → AHK 的熱鍵、算式、中文、註解、迴圈及共用前置碼；不另寫一套產生器。測試用 XML 元素介面只支援這些函數使用的選擇器，不能取代瀏覽器驗收。

目前 EXE 按鈕使用外部 `/compile` 服務；測試模擬成功、伺服器錯誤及連線例外，檢查傳送內容、二進位下載與按鈕復原。另測試 Django 保留的 `/cp`、`/dl`、`/rm` 路徑，包括 UTF-8 BOM 編碼設定、UUID、64-bit 參數與檔案操作。網路、編譯器、刪檔與等待均隔離，不會送出程式碼、執行 Ahk2Exe 或啟動產生的 EXE；通過單元測試不代表真實 EXE 編譯成功。

舊版 `/cp` 尚未檢查編譯退出碼或確認 EXE 產生；`/dl`、`/rm` 的缺少參數及 `/dl` 缺少檔案情況也未處理。這些既有缺失未在新增測試時修改，也未將錯誤行為固定為正確契約。

版面或操作功能變更仍應在瀏覽器確認：積木拖拉、語法產生、複製、AHK／XML 下載、說明捲動與留言。廣告版面涵蓋桌面、911 px 分界及手機，並確認說明框實際寬度 300／299 px 時的顯示切換。

## 說明與留言

各頁沿用既有 HackMD 文件與排版，不在 repository 維護副本。積木頁在文件外載入原 Disqus 留言串；留言與 Google 登入不依賴 HackMD。正式入口為 `papple23g-ahkcompiler.herokuapp.com`。

來源識別、登入行為及既有驗證紀錄見[留言系統文件](comment-system-evaluation.md)。

## 離線匯出

[`onlineToOffline.py`](../onlineToOffline.py) 從正式網站取得填表與積木頁的 HTML，處理後寫入 `protable`。廣告移除由 [`scripts/offline_ads.py`](../scripts/offline_ads.py) 處理；有未移除或標記不完整的廣告程式時會拒絕匯出，避免將線上廣告帶進離線版本。留言轉為線上討論串入口。

既有離線發行版本與下載步驟見 [README 的離線版](../README.md#離線版)。

## 單一廣告版位

`/ahkblockly` 使用說明上方的固定 300 × 250 版位。本機僅顯示示意素材，不請求 Google 廣告；正式程式限定於正式網站的 HTTPS `/ahkblockly`。其他子頁面及離線版本不帶廣告。

- 桌面版位留在工具右側；視窗寬度 911 px 以下，廣告與說明一起移到工具下方，手機亦保留。
- 說明框實際寬度不足 300 px 時暫時收起，不留空白；初始空間不足會等放寬後才載入。
- 已載入的版位縮窄後可恢復同一版位，不需重新載入頁面；一次頁面載入最多建立一個 loader、初始化一次。拖拉、縮放與下載不刷新廣告。
- 載入錯誤、無填充、初始化失敗或 20 秒逾時會收起，放寬也不重試。逾時從首次載入 loader 起算，不因縮放重新計時。

正式廣告預設停用。網站核准、根目錄 `ads.txt` 核對與適用的隱私權／同意設定完成後，將環境變數 `AHK_ADSENSE_SLOT` 設為有效的手動廣告單元 ID；空值停用新頁面載入的廣告。自動廣告保持停用，關閉會改動版位的自動最佳化。

收益觀察從首次正常放送後的下一個完整台北日期開始，記錄 30 天的單元曝光、涵蓋率、預估收益與 RPM，搭配 GA4 的流量及裝置類別。收益大於零只代表收入流程已驗證；曝光不足標記為資料不足。若妨礙操作或收到政策警告，清空 slot 停用。

## 貢獻

問題回報可附上重現步驟、瀏覽器與畫面；程式變更可透過 Pull Request 提交，說明變更目的與驗證結果。開發與測試指令見上方章節，授權見 [LICENSE](../LICENSE)。

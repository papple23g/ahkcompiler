# AHK 語法產生器

透過填表或拖曳積木，產生 Windows 自動化腳本：熱鍵、鍵盤與滑鼠操作、文字處理、條件判斷及迴圈。

輸出採用 **AutoHotkey v1.1 語法**，請使用 AHK v1 執行；不能直接以 AHK v2 執行。

| 工具 | 適合用途 |
| --- | --- |
| [積木語法產生器](https://papple23g-ahkcompiler.herokuapp.com/ahkblockly) | 組合多個動作與流程，匯入／匯出 XML 積木檔 |
| [填表語法產生器](https://papple23g-ahkcompiler.herokuapp.com/ahktool) | 設定熱鍵與常用動作，快速產生語法 |

## 積木語法產生器

1. 開啟[積木頁面](https://papple23g-ahkcompiler.herokuapp.com/ahkblockly)，從左側分類拖出積木並接合。
2. 設定積木中的文字、按鍵或選項，按「▼轉換為AHK語法」。
3. 按「複製語法」或「下載.ahk檔案」，將產生的腳本交給 AutoHotkey v1 執行。

「💾另存積木檔」可保存 XML；之後用「📥匯入積木檔」繼續編輯。

「下載.exe檔(64-bit)」是實驗功能，會將程式碼傳送至外部編譯服務，可能因服務狀態而失敗。

![積木編輯與語法輸出範例](https://i.imgur.com/XDxVKCd.png)

## 填表語法產生器

1. 開啟[填表頁面](https://papple23g-ahkcompiler.herokuapp.com/ahktool)，選擇熱鍵與要執行的功能。
2. 填入需要的參數，確認產生的語法後按「複製語法」。
3. 將語法存成 `.ahk` 檔，以 AutoHotkey v1 執行。

![填表設定與語法輸出範例](https://i.imgur.com/bCXaDEs.png)

## 離線版

1. 下載既有的 [AHK Blockly 1.12.0 ZIP](https://github.com/papple23g/ahkcompiler/releases/download/1.12.0/AHK.Blockly.1.12.0.zip) 並解壓縮。
2. 用瀏覽器開啟其中的 `ahkblockly.html`（積木）或 `ahktool.html`（填表）。

此發行版本為 1.12.0，功能可能與線上版不同。

## 開發、貢獻與授權

本機開發與測試見[開發文件](docs/development.md)；問題回報及程式貢獻見[貢獻說明](docs/development.md#貢獻)。

本專案採用 [MIT 授權](LICENSE)。

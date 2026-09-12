---
tags: Autohotkey
---

### Q: AHK 積木支持 2.0 語法器嗎?
AHK 官方在去年底發布新版 [Autohotkey v2](https://wyagd001.github.io/v2/docs/v2-changes.htm) 語法，比舊版 1.1 的語法更加合理且靈活
可惜 AHK 積木與這個新版語法並不相容
因此作者正在開發 AHK 積木 2.0，並且將追加更多功能，請拭目以待

### Q: 有離線版的AHK語法產生器嗎?
有的，可至[此處](https://github.com/papple23g/ahkcompiler/releases)下載最新的 `AHK.Blockly.xxx.zip` 壓縮檔，其中`AHK_Blockly.html`為離線版AHK積木，而`AHK_Tool.html`為離線版AHK表單語法產生器，均應使用瀏覽器開啟
目前AHK積木不支援 2.0 版，僅支援 1.1 版 ( AHK1.1 免安裝載點: [AutoHotkey_1.1.36.02.zip](https://github.com/papple23g/ahkcompiler/releases/download/1.12.0/AutoHotkeyPortable_1.1.36.02.zip))

### Q: 在遊戲裡面用AHK操作鍵盤滑鼠好像會失效?
有些遊戲會擋自動控制，可以用系統管理員啟動腳本，或者把 Send 指令改成 SendPlay 再試試看。如果是在 Bluestacks 模擬器上使用，則要改用 ControlClick 這個語法(可以參考這個[影片](https://youtu.be/ravOMFD-Zmw?t=663)在時間軸 11:00 左右的示範)

### Q: 如何提高搜尋圖片的成功機率? 圖片有色差怎麼辦?
AHK 可以搜尋有些微色差的截圖，根據官網對圖片搜尋語法 [ImageSearch](https://wyagd001.github.io/zh-cn/docs/commands/ImageSearch.htm) 的說明，可在指令中的「檔名參數」的前面加上「*N」，N是一個數字，越大代表偵測的色差範圍越廣，不過也會花費較久的時間，例如可將
`ImageSearch, X, Y, 0, 0, W, H,%__ImageFilePath%`
改寫為
`ImageSearch, X, Y, 0, 0, W, H,*10 %__ImageFilePath%`

### Q: AHK 積木執行出現錯誤訊息「ERROR:This line does not contain a recognized action. the program will exit.」
這是因為您使用了網頁的自動翻譯功能，部分程式碼的被翻譯成中文導致程式編譯失敗，建議先關閉自動翻譯的功能後再使用

### Q: 如何使用AHK獲取網頁中的文字?
在 [【AHK】#08 使用AHK操作網頁元素](https://www.youtube.com/watch?v=MLkDhCXAv6w) 介紹影片中，有提到複製 <span style="color:blue">JS Path</span> 元素的方法，如果點擊是加上`.click()`語法的話，獲取文字就是加上`.innerText`，例如在本網站的網址列上打 <code>alert(<span style="color:blue">document.querySelector(`"`#div_header > h1 > b`"`)</span>.innerText)</code>，前面再加上`Javascript:`後按Enter，就會跳出標題文字訊息「AHK 語法產生器」

### Q: 如何從 Javascript 傳遞文字給 AHK?
根據[這篇](https://stackoverflow.com/questions/33855641/copy-output-of-a-javascript-variable-to-the-clipboard)提供的語法，在本網站執行以下 Javascript 指令可以將標題文字訊息「AHK 語法產生器」複製到剪貼簿中 :
<code>function copyToClipboard(text) { var dummy = document.createElement(`"`textarea`"`); document.body.appendChild(dummy); dummy.value = text; dummy.select(); document.execCommand(`"`copy`"`); document.body.removeChild(dummy); }; copyToClipboard(<span style="color:blue">document.querySelector(`"`#div_header > h1 > b`"`)</span>.innerText);
</code>

隨後，AHK 便可用內置變量 [Clipboard](https://wyagd001.github.io/zh-cn/docs/misc/Clipboard.htm) 去存取剪貼簿的內容


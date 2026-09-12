作者 : [逆道者](https://papple23g-ahkcompiler.herokuapp.com/about)
網站 : [AutoHotKey 積木語法產生器](https://papple23g-ahkcompiler.herokuapp.com/ahkblockly)


[Toc]

## 為何防毒軟體會出現警告
Autohotkey雖然是方便的腳本工具，但是被編譯成exe檔案後就會看不到腳本內容，而這隱藏的風險成為有心人的操作工具，因此防毒軟體會對AHK編譯的exe檔特別敏感。
如果您相信本站編譯好的腳本沒有任何危害的話，請參考下一個章節。若不放心的話，也可以改成下載.ahk檔(存文字檔)，然後使用Autohotkey執行即可。
本網站的完整程式碼公布於 [Github - ahkcompiler](https://github.com/papple23g/ahkcompiler/blob/master/myapp/views.py)。
## 如何跳過防毒/攔截訊息

- Windows Defender 防毒軟體
![](https://i.imgur.com/gbY6PWU.png)


- Avast 防毒軟體
![](https://i.imgur.com/6Bz9g88.png)





## 按下 [下載.exe] 按鈕後, 發生了什麼事
首先網頁前端會將AHK程式碼傳送至一台Window伺服器中進行exe編譯
接著再將exe檔案傳送回網頁前端
伺服器中的.ahk和.exe檔會在下載完後被自動刪除
```sequence
網頁前端 -> 伺服器: 傳送AHK程式碼
note right of 伺服器: 產生.ahk檔案
note right of 伺服器: 轉譯為.exe檔案
伺服器 -> 網頁前端 : 傳送.exe檔案
note left of 網頁前端: 下載檔案
網頁前端 -> 伺服器: 刪除檔案請求
note right of 伺服器: 刪除.ahk及.exe檔案

```

由於筆者找不到適合的Window線上部署空間
因此出動了家裡沒有在用的舊電腦

<p style="text-align:center">
<img src="https://i.imgur.com/qjX3Ftl.png">
<br>
<span>(圖)純粹用於編譯AHK的舊主機，請大家為它加油!</span>
</p>

## 我載好了exe檔，為何腳本沒有執行成功/沒有反應?
請對下載的exe檔案按右鍵>使用管理者身分執行
之後等待約10秒後，螢幕右下角出現綠色圖示 ![](https://i.imgur.com/fKNzAz4.png =15x15) 代表腳本已成功運行中







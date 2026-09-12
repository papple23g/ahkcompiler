# AHK 語法產生器

[![](https://img.shields.io/static/v1?label=Python&message=v3.12&color=blue)](https://www.python.org/)
[![](https://img.shields.io/static/v1?label=Brython&message=v3.7.5&color=purple)](https://github.com/brython-dev/brython)
[![](https://img.shields.io/static/v1?label=Django&message=v5.2.17&color=green)](https://www.djangoproject.com/)
[![](https://img.shields.io/static/v1?label=Autohotkey&message=v1.1.30.03&color=#3F627F)](https://www.autohotkey.com/)


本網站使用 Django 架設 [Autohotkey](https://www.autohotkey.com/) 語法產生器

使用者可根據自己的需求產生自動化腳本與程式

本站提供 [填表](#填表產生語法) 與 [積木](#積木拼圖產生語法) 兩種方式產生腳本


## 本機開發（Windows / Python 3.12）

使用專案外部的虛擬環境；已有環境可跳過建立步驟：

```powershell
uv venv "$env:USERPROFILE\venvs\ahkcompiler_venv" --python 3.12
& "$env:USERPROFILE\venvs\ahkcompiler_venv\Scripts\Activate.ps1"
uv pip install -r requirements.txt -r requirements-docs.txt
python manage.py check
python manage.py test
python manage.py runserver 8000
```

開啟 `http://127.0.0.1:8000/ahkblockly`。VS Code 選擇同一個外部環境後可直接啟動 Django 偵錯，不需要暫時 alias。Django 測試預設只探索 `myapp`，避免匯入供瀏覽器使用的 Brython 子模組；文件測試另執行 `python -m unittest discover -s tests -v`。

`Failed to hardlink files; falling back to full copy` 表示 uv 改用複製安裝，不是啟動失敗原因；需要消除提示時可加 `--link-mode=copy`。

## 填表產生語法

使用使用填寫表單的方式快速產生AHK語法

網頁 : https://papple23g-ahkcompiler.herokuapp.com/ahktool

### 瀏覽圖

![AHK首頁- 網頁瀏覽圖](https://i.imgur.com/bCXaDEs.png)


## <span style="background-color:#f1c40fbb">積木拼圖產生語法</span>

使用 [Google Blockly](https://developers.google.com/blockly) 的拼圖引擎撰寫製作AHK腳本

網頁 : https://papple23g-ahkcompiler.herokuapp.com/ahkblockly

### 瀏覽圖
![AHK積木拼圖產生語法 - 網頁瀏覽圖](https://i.imgur.com/XDxVKCd.png)

### 離線版
執行方法:
1. 請至 [點擊此連結](https://github.com/papple23g/ahkcompiler/releases/download/1.12.0/AHK.Blockly.1.12.0.zip) 下載 `.zip` 檔後解壓縮
2. 執行裡面的 `ahktool.html` 與 `ahkblockly.html` 網頁檔案即可

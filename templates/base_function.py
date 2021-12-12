"""
負責基本函式或共同的函式
"""

from browser import document as doc
from browser.html import *
from browser import bind, window, alert
from browser.local_storage import storage

# 過渡JS物件和函式
log = window.console.log
FormatHTML = window.FormatHTML
DownloadTextFile = window.DownloadTextFile


# Blockly=window.Blockly
# workspace=window.workspace
# #將介面改為桌機瀏覽模式 (因此手機上可以編輯文字拼圖)
# Blockly.utils.userAgent.MOBILE=False
# Blockly.utils.userAgent.ANDROID=False
# Blockly.utils.userAgent.IPAD=False


# 定義函式:JS特殊符號解碼器
def JavascriptSymbolDecoder(encodedStr):
    parser = window.DOMParser.new()
    dom = parser.parseFromString(
        '<!doctype html><body>' + encodedStr, 'text/html')
    decodedString = dom.body.textContent
    return decodedString

# 定義動作:複製文字 #不需要建立外部額外元素


def CopyTextToClipborad(string):
    # 將文字先禁行解碼
    string = JavascriptSymbolDecoder(string)
    # 製作暫時元素複製文字
    textarea_elt_forCopyText = TEXTAREA()
    textarea_elt_forCopyText.text = string
    doc <= textarea_elt_forCopyText
    textarea_elt_forCopyText.select()
    doc.execCommand("copy")
    textarea_elt_forCopyText.remove()

# 定義功能函數:增加CSS樣式字串


def AddStyle(style_str):
    style_elt = doc.select_one('head').select_one('style')
    style_elt.text += style_str


AddStyle("""
    .hidden{
        display:none;
    }

""")
# 定義功能函數:找到對應tagName的父元素


def ParentElt(elt, parent_tagName):
    while (elt.tagName != parent_tagName):
        elt = elt.parent
    return elt


# 定義DIV網頁header區塊
def DIV_header():
    div_elt = DIV(id="div_header", Class="w3-row-padding w3-indigo")
    # 設置網頁標頭H1元素
    H1_title_elt = H1(
        B(
            f"AHK 語法產生器", style={
                "font-family": "微軟正黑體"
            }
        ),
        style={"float": "left"},
    )

    # 排版
    div_elt <= H1_title_elt
    return div_elt


AddStyle('''
    #here{
        height: 100px;
    }
    #div_header{
        height: 100px;
        position: relative;
        z-index: 10;
    }
''')

# 定義DIV導覽列區塊


def DIV_bars(nbo_subpage_int):
    # 定義A導覽列按鈕元素
    def DIV_ButtonBar(button_name, id=None, link=None):
        unactive_className = "w3-bar-item w3-button w3-large w3-hover-blue"
        div_elt = DIV(button_name, Class=unactive_className)
        if id:
            div_elt.id = id
        return A(div_elt, href=link)
    # 設置DIV導覽列區塊
    div_elt = DIV(Class="w3-bar w3-black bars")

    # 設置DIV導覽列中的按鈕
    div_btnBar_elt_list = [
        DIV_ButtonBar("首頁", id="首頁", link='/ahktool'),
        DIV_ButtonBar("AHK積木", id="AHK積木", link='/ahkblockly'),
        DIV_ButtonBar("更新日誌", id="更新日誌", link='/updateDiary'),
        DIV_ButtonBar("關於作者", id="關於作者", link='/about'),
        DIV_ButtonBar("常見Q&A", id="常見Q&A", link='/faq'),
    ]

    # 將當前子頁面的按鈕亮起
    div_btnBar_elt_list[nbo_subpage_int].classList.add('AButton_bar_actived')

    # 排版
    for div_btnBar_elt in div_btnBar_elt_list:
        div_elt <= div_btnBar_elt

    # 設定bar被按下時的樣式
    AddStyle("""
        #button_bar_add_emoji{
            color: yellow;
        }
        .AButton_bar_actived{
            background-color:gray;
        }
        .bars{
            margin: 0px 0px 1em;
            font-family: 微軟正黑體;
            position: relative;
            z-index: 10;
        }
    """)

    return div_elt


# 子頁面之前的元素空出間隔
AddStyle('''
#div_subMainPage>*{
        padding:20px;
    }
'''
         )

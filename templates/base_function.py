"""
負責基本函式或共同的函式
"""

from browser import document as doc
from browser.html import *
from browser import bind,window,alert,ajax
#過渡JS物件和函式
log=window.console.log
FormatHTML=window.FormatHTML
DownloadTextFile=window.DownloadTextFile
Blockly=window.Blockly
workspace=window.workspace

# #將介面改為桌機瀏覽模式 (因此手機上可以編輯文字拼圖)
Blockly.utils.userAgent.MOBILE=False
Blockly.utils.userAgent.ANDROID=False
Blockly.utils.userAgent.IPAD=False


#定義動作:複製文字 #不需要建立外部額外元素
def CopyTextToClipborad(string):
    textarea_elt_forCopyText=TEXTAREA()
    textarea_elt_forCopyText.text=string
    doc<=textarea_elt_forCopyText
    textarea_elt_forCopyText.select()
    doc.execCommand("copy")
    textarea_elt_forCopyText.remove()

#定義功能函數:增加CSS樣式字串
def AddStyle(style_str):
    style_elt=doc.select_one('head').select_one('style')
    style_elt.text+=style_str

AddStyle("""
    .hidden{
        display:none;
    }

""")
#定義功能函數:找到對應tagName的父元素
def ParentElt(elt,parent_tagName):
    while (elt.tagName!=parent_tagName):
        elt=elt.parent
    return elt

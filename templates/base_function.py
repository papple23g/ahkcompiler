"""
負責基本函式或共同的函式
"""

from browser import window,doc#,ajax,alert,bind,timer,confirm
from browser.html import *

#引渡Javascript印出資料log語法
log=window.console.log



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

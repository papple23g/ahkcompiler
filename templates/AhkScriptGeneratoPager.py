"""
#啟動測試指令
cd "C:\Users\Peter Wang\Google Drive\mysite2"
python2 manage.py runserver 0.0.0.0:8001

cd "C:\Users\pappl\Google Drive\mysite2"
python manage.py runserver 0.0.0.0:8000

#更新上傳指令
cd "C:\Users\Peter Wang\Google Drive\mysite2"
cd "C:\Users\pappl\Google Drive\mysite2"
git add .
git commit -m "

git push heroku master
git push -u origin master
1
#可選指令
heroku run python manage.py makemigrations  (可選，如果本地有新增app應用)
heroku run  python manage.py migrate (可選，如果本地有新增app應用)
heroku run python manage.py createsuperuser (可選，如果本地有新增超級管理員)
heroku run python manage.py collectstatic(可選，如果有新增static的檔案)

#刪除Emoji範例
heroku run python manage.py shell -a papple23g-mysite2
from myapp.models import Emoji
Emoji.objects.filter(id="13600").delete()

"""



#移除載入頁面訊息
#doc['loading_webpage_msg'].remove()

#定義DIV網頁header區塊
def DIV_header():
    div_elt=DIV(id="div_header",Class="w3-row-padding w3-green")
    #設置網頁標頭H1元素
    H1_title_elt=H1(
        B(
            f"AHK 語法產生器"
            ,style={
                "font-family":"微軟正黑體"
            }
        ),
        style={"float":"left"},
    )
    
    #排版
    div_elt<=H1_title_elt
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

#定義DIV導覽列區塊
def DIV_bars():
    #定義A導覽列按鈕元素
    def DIV_ButtonBar(button_name,id=None):
        unactive_className="w3-bar-item w3-button w3-large w3-hover-blue"
        div_elt=DIV(button_name,Class=unactive_className)
        if id:            
            div_elt.id=id
        return div_elt
    #設置DIV導覽列區塊
    div_elt=DIV(Class="w3-bar w3-black bars")

    #排版:設置導覽列bars的順序
    '第一個bar:初始設定已經被按下'
    AButton_bar_frist=DIV_ButtonBar("搜尋表符",id="button_bar_search_emoji")
    AButton_bar_frist.classList.add("AButton_bar_actived")

    '其他bars'
    div_elt<=DIV_ButtonBar("積木",id="button_bar_blockly")
    div_elt<=DIV_ButtonBar("更新日誌",id="button_bar_update_diary")
    #div_elt<=DIV_ButtonBar("其他推廣",id="button_bar_other_production")
    #div_elt<=DIV_ButtonBar("關於作者",id="button_bar_about_author")

    #設定bar被按下時的樣式
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


#排版:置入DIV網頁header區塊
doc.body.insertBefore(DIV_header(),doc['blocklyDiv'])
doc.body.insertBefore(DIV_bars(),doc['blocklyDiv'])
doc['blocklyDiv'].style.visibility="visible"
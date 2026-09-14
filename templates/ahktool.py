from browser import alert, bind, doc, window
from browser.html import *

VERSION = "2.6"

# region 設置全域變數:AHK自定義函數字典
FUNCTION_DICT = {
    "AutoInput":
    """
;使用剪貼簿插入文字
AutoInput(InputStr){
    clipboard_save = %ClipboardAll%
    clipboard:=
    clipboard = %InputStr%
    ClipWait
    Send ^v
    clipboard = %clipboard_save%
}
""",
    "WebSite_Clipboard":
    """
;將關鍵字帶入網址查詢(version:190624)
WebSite_Clipboard(UrlA,UrlB,website_name:="",ShowInputBox:="True"){
    ;備份並清空剪貼簿
    clipboard_save = %ClipboardAll%
    Clipboard :=""
    ;獲取選取的關鍵字
    Send ^{c}
    Sleep 200
    keyWord = %Clipboard%
    ;恢復先前的剪貼簿
    Clipboard = %clipboard_save%
    ;若沒有選取文字被選取，則跳出輸入文字框讓使用者輸入關鍵字，複製到剪貼簿
    if (keyWord="" and ShowInputBox="True"){
        ;若未設定網站名稱，則用
        if (website_name=""){
            website_name=%UrlA%
        }
        InputBox, keyWord,搜尋關鍵字,%website_name%,,,150
    }
    ;將關鍵字做解碼處理，並嵌入搜尋網址中
    if (ErrorLevel=0 and keyWord!=""){
        Copy= % UriEncode(keyWord)
        Run %UrlA%%Copy%%UrlB%
    }
    return
}


""",
    "UriEncode":
    """
;讓關鍵字轉化為網址解碼形式，得以讓關鍵字正確被搜尋
;參考自https://rosettacode.org/wiki/URL_encoding#AutoHotkey
UriEncode(Uri){
    VarSetCapacity(Var, StrPut(Uri, "UTF-8"), 0)
    StrPut(Uri, &Var, "UTF-8")
    f := A_FormatInteger
    SetFormat, IntegerFast, H
    While Code := NumGet(Var, A_Index - 1, "UChar")
        If (Code >= 0x30 && Code <= 0x39 ; 0-9
            || Code >= 0x41 && Code <= 0x5A ; A-Z
            || Code >= 0x61 && Code <= 0x7A) ; a-z
            Res .= Chr(Code)
        Else
            Res .= "%" . SubStr(Code + 0x100, -1)
    SetFormat, IntegerFast, %f%
    Return, Res
}
""",
    "GoToClipboardWebSite":
    """
;前往滑鼠選取的網址
GoToClipboardWebSite(){
    clipboard_save=%ClipboardAll%
    clipboard:=
    Send ^{c}
    ClipWait
    Run %Clipboard%
    clipboard = %clipboard_save%
    return
}
""",
    "ClickPosition":
    """
;模擬滑鼠點擊
ClickPosition(posX,posY,ClickCount:=1,Speed:=0,CoordMode:="Screen",Return:=true){
    ;若使用相對模式
    if (CoordMode="Relative"){
        CoordMode,Mouse,Screen
        MouseGetPos, posX_i, posY_i ;儲存原來的滑鼠位置
        ;根據點擊次數是否為零來使用MouseClick或MouseMove
        if %ClickCount%{
            MouseClick,,%posX%,%posY%,%ClickCount%,%Speed%,,R ;點擊相對位置
        }else{
            MouseMove, %posX%, %posY%,%Speed%
        }
    ;若使用其他模式
    }else{
        CoordMode,Mouse,%CoordMode%
        MouseGetPos, posX_i, posY_i ;儲存原來的滑鼠位置
        ;根據點擊次數是否為零來使用MouseClick或MouseMove
        if %ClickCount%{
            MouseClick,,%posX%,%posY%,%ClickCount%,%Speed%
        }else{
            MouseMove, %posX%, %posY%,%Speed%
        }
    }
    ;是否點擊後返回
    if %Return%{
        MouseMove, %posX_i%, %posY_i%,%Speed%
    }
    return
}
""",
    "StringInActiveTitle":
    """
;偵測目前視窗標題是否含有某一段文字
StringInActiveTitle(String){
    WinGetActiveTitle,WinTitle
    IfInString, WinTitle, %String%
    {
        return True
    }
    else
    {
        return False
    }
}
""",
    "ClickPicture":
    """
;模擬滑鼠點擊圖片
ClickPicture(ImageFilePath,ClickCount:=1,Speed:=0,Return:=true,ShowError:=true){
    pos:=GetPicturePosition(ImageFilePath)
    if %pos%{
        posX:=pos[1]
        posY:=pos[2]
        ClickPosition(posX,posY,ClickCount,Speed,,Return)
        return [posX,posY]
    }else{
        if %ShowError% {
            MSGBOX 畫面中找不到圖片`n %ImageFilePath%
        }
        return false
    }
    
}
""",
    "GetPicturePosition":
    """
;獲取圖片的位置
GetPicturePosition(ImageFilePath){
    gui,add,picture,hwndmypic,%ImageFilePath%
    controlgetpos,,,width,height,,ahk_id %mypic%
    CoordMode Pixel
    ImageSearch, FoundX, FoundY, 0, 0, A_ScreenWidth, A_ScreenHeight,%ImageFilePath%
    CoordMode Mouse
    if %FoundX%{
        return [FoundX+width/2,FoundY+height/2]
    } else {
        return FoundX
    }
}
""",
    "ExecuteJavascriptOnUrlBar":
    """
;在瀏覽器上執行Javascript, v1.0
ExecuteJavascriptOnUrlBar(str,delay:=300){
    Sleep %delay%
    ;聚焦在網址列
    Send ^l
    Sleep %delay%
    ;輸入Javascript語法
    AutoInput("_Javascript:" . str . ";void(0);")
    ;刪除前綴底線符號，並執行Javascript語法
    Sleep %delay%
    Send {Home}{Delete}{Enter}
    Return
}
""",
    "WebElementAction":
    """
;控制網頁物件(預設為點擊)
WebElementAction(selector,action:="Click",value:=0,delay:=300){
    ;設置獲取網頁物件語法
    element_str=document.querySelector("%selector%")
    ;設置動作語法
    if (action="Click"){
	action_str:=".click()"
    }else if (action="Focus"){
	action_str:=".focus();" . element_str . ".select()"
    }else if (action="Input"){
	action_str=.value="%value%"
    }else if (action="Select"){
	action_str=.selectedIndex="%value%"
    }
    ;生成Javascript語法並在瀏覽器上執行
    javascript_str:=element_str . action_str
    ExecuteJavascriptOnUrlBar(javascript_str,delay)
    Return
}
""",
}
# endregion 設置全域變數:AHK自定義函數字典

# **定義定期刷新顯示AHK語法動作**


def render_ahk_script():
    if doc['div_hotkey_setting'].innerHTML != "":  # 若設定組合鍵勾選區塊已經被BRYTHON生成，才執行以下動作
        # 獲取組合鍵設定模式
        hotkey_setting_mode = doc['div_hotkey_setting'].select(
            "input[type=radio]:checked")[0].value
        # 若組合鍵設定模式不為自訂，則輸出一般的組合鍵符號
        if hotkey_setting_mode != "custom":
            # 獲取所有勾選的inputCheckbox組合鍵元素列表
            inputCheckbox_func_key_elt_list = doc.select(
                "#div_hotkey_setting input.function_key[type='checkbox']")
            # 獲取所有勾選的inputCheckbox前綴功能元素列表
            inputCheckbox_prefix_function_elt_list = doc.select(
                "#div_hotkey_setting input.prefix_function[type='checkbox']")

            # 獲取已勾選前綴符號
            prefix_symbol = "".join(
                checkbox.symbol if checkbox.checked else "" for checkbox in inputCheckbox_prefix_function_elt_list)
            # 獲取已勾選組合鍵符號
            function_key_symbol = "".join(
                checkbox.symbol if checkbox.checked else "" for checkbox in inputCheckbox_func_key_elt_list)
            # 獲取一般鍵盤符號
            normal_key_symbol = doc['div_hotkey_setting_area'].select("select.normal_key")[
                0].value

            # 產生執行熱鍵符號，含冒號
            ahk_key_script = prefix_symbol+function_key_symbol+normal_key_symbol+":: "

        # 若組合鍵設定模式為自訂，則輸出匹配型按鍵符號

        else:
            select_elt_normal_key_list = doc['div_hotkey_setting_area'].select(
                "select.normal_key")
            # 若組自訂合鍵設定模式區塊加載完成
            if len(select_elt_normal_key_list) == 2:
                # 獲取所有勾選的inputCheckbox前綴功能元素列表
                inputCheckbox_prefix_function_elt_list = doc.select(
                    "#div_hotkey_setting input.prefix_function[type='checkbox']")
                # 設置前綴符號
                prefix_symbol = "".join(
                    checkbox.symbol if checkbox.checked else "" for checkbox in inputCheckbox_prefix_function_elt_list)
                # 獲取自訂雙按鍵符號
                key_A, key_B = [select_elt.value for select_elt in doc['div_hotkey_setting_area'].select(
                    "select.normal_key")]
                ahk_key_script = f"{prefix_symbol}{key_A} & {key_B}::"
                if doc['div_hotkey_setting_area'].select("input[type='checkbox']")[0].checked:
                    ahk_key_script += "\n" + \
                        f"{prefix_symbol}{key_B} & {key_A}::"+"\n"
            # 若組自訂合鍵設定模式區塊未加載完成
            else:
                ahk_key_script = ""

        # 定義跳出訊息視窗的AHK語法字串
        def ShowMsgByMsgbox_ahkCommand(msg_str, msg_type):
            # 替換訊息文字特殊符號
            msg_str = msg_str.replace("%", "`%").replace(",", "`,")
            com_str = ""
            if msg_type == "目前滑鼠位置":
                com_str += "\nCoordMode, Mouse, Screen\n"
                com_str += "MouseGetPos, posX, posY\n"
                com_str += "Msgbox,(%posX%`,%posY%)"
            elif msg_type == "目前視窗名稱":
                com_str += "\nWinGetActiveTitle,WinTitle\n"
                com_str += "Msgbox,%WinTitle%"
            elif msg_type == "今天日期":
                com_str += "Msgbox,%A_YYYY%/%A_MM%/%A_DD%"
            else:
                com_str += f"Msgbox,{msg_str}"
            return com_str

        # 定義跳出訊息視窗的AHK語法字串
        def ShowMsgByTooltip_ahkCommand(msg_str, msg_type):
            # 顯示提示持續時間(毫秒)
            lifetime = 1500
            # 替換訊息文字特殊符號
            msg_str = msg_str.replace("%", "`%").replace(",", "`,")
            com_str = "\nCoordMode, Mouse, Screen\n"
            com_str += "\nCoordMode, ToolTip, Screen\n"
            com_str += "MouseGetPos, posX, posY\n"
            if msg_type == "目前滑鼠位置":
                com_str += "ToolTip,(%posX%`,%posY%),posX,posY\n"
            elif msg_type == "目前視窗名稱":
                com_str += "WinGetActiveTitle,WinTitle\n"
                com_str += "ToolTip,%WinTitle%,posX,posY\n"
            elif msg_type == "今天日期":
                com_str += "ToolTip,%A_YYYY%/%A_MM%/%A_DD%,posX,posY\n"
            else:
                com_str += f"ToolTip,{msg_str},posX,posY\n"
            com_str += f"Sleep {lifetime}\n"
            com_str += "ToolTip,"
            return com_str

        "加入執行語法(未定義)"
        ahk_exec_script = None

        # 獲取DIV組合鍵功能區塊
        div_function_elt = doc.select('#DIV_function')[0]
        if div_function_elt:  # 等待加載完畢
           # 獲取SELECT組合鍵功能元素
            select_elt = div_function_elt.select("select")[0]
            # 獲取DIV組合鍵子功能設定區塊
            div_func_conent_elt = div_function_elt.select("#DIV_func_conent")[
                0]

            # 3#根據選的組合鍵功能設置AHK語法(輸出:ahk_exec_script)
            if select_elt.value in ["開啟資料夾", "開啟網頁", "執行程式"]:
                input_elt = div_func_conent_elt.select("input")[0]
                input_text = input_elt.value if input_elt.value else input_elt.placeholder
                ahk_exec_script = f'Run "{input_text}"'
                # 更正百分比符號錯誤
                if select_elt.value == "開啟網頁":
                    ahk_exec_script = ahk_exec_script.replace(
                        "%", "`%").replace(",", "`,")
            elif select_elt.value == "開啟檔案":
                filePath = div_func_conent_elt.select(
                    "input[type='text']")[0].value
                programPath = div_func_conent_elt.select(
                    "input[type='text']")[1].value
                checkbox_elt = div_func_conent_elt.select(
                    'input[type="checkbox"]')[0]
                ahk_exec_script = 'Run' + \
                    (f' "{programPath}"' if checkbox_elt.checked else "") + \
                    f' "{filePath}"'
            elif select_elt.value == "搜尋滑鼠選取的關鍵字":
                A_url = doc['input_A_url'].value
                B_url = doc['input_B_url'].value
                do_show_inputbox = "True" if doc['inputCheck_showInputBox'].checked else "False"
                if "hidden" in doc['website_name'].className:
                    website_name = doc['select_searchWebSite'].value
                else:
                    website_name = doc['input_website_name'].value
                ahk_exec_script = f'WebSite_Clipboard("{A_url}","{B_url}","{website_name}","{do_show_inputbox}")'
            elif select_elt.value == "終止程序":
                input_text = div_func_conent_elt.select("input")[0].value
                ahk_exec_script = f'Process, Close, "{input_text}"'
            elif select_elt.value == "清空資源回收桶":
                ahk_exec_script = "FileRecycleEmpty"
            elif select_elt.value == "熱字串(自動展開縮寫)":
                abbreviation_input_elt = div_func_conent_elt.select("input[type='text']")[
                    0]
                abbreviation_text = abbreviation_input_elt.value if abbreviation_input_elt.value else abbreviation_input_elt.placeholder
                # 抓取勾選元素
                inputCheckbox_elt_list = doc["DIV_func_conent"].select(
                    "input[type=checkbox]")
                # 覆蓋ahk語法按鍵字串(如*oc等等符號)
                ahk_key_script = ":"
                ahk_key_script += "".join([(inputCheckbox_elt.symbol if inputCheckbox_elt.checked else inputCheckbox_elt.nosymbol)
                                          for inputCheckbox_elt in inputCheckbox_elt_list[:-1]])
                ahk_key_script += f":{abbreviation_text}::"
                extendedString_input_text_elt = div_func_conent_elt.select("input[type='text']")[
                    1]
                ahk_exec_script = extendedString_input_text_elt.value if extendedString_input_text_elt.value else extendedString_input_text_elt.placeholder
                # 若勾選使用剪貼布展開文字，則使用AutoInput
                if inputCheckbox_elt_list[-1].checked:
                    ahk_exec_script = "\n"+f"AutoInput(\"{ahk_exec_script}\")"
            elif select_elt.value == "插入文字":
                insert_method = doc["DIV_func_conent"].select(
                    "input[type='radio']:checked")[0].value
                input_text = (
                    doc['input_inserted_text'].value if doc['input_inserted_text'].value else doc['input_inserted_text'].placeholder)
                # 若選擇使用剪貼簿
                if insert_method == "AutoInput":
                    ahk_exec_script = 'AutoInput("{}")'.format(input_text)
                else:
                    ahk_exec_script = insert_method+" {TEXT}"+input_text
            elif select_elt.value == "音量調節":
                input_radio_checked_elt = div_func_conent_elt.select(
                    "input[type='radio']:checked")[0]
                volumn_action = input_radio_checked_elt.value
                if volumn_action == "up":
                    input_number_elt = input_radio_checked_elt.parent.nextSibling
                    ahk_exec_script = f"SoundSet +{input_number_elt.value}"
                elif volumn_action == "down":
                    input_number_elt = input_radio_checked_elt.parent.nextSibling
                    ahk_exec_script = f"SoundSet -{input_number_elt.value}"
                elif volumn_action == "mute":
                    ahk_exec_script = "SoundSet, +1, , mute"
                elif volumn_action == "set":
                    input_number_elt = input_radio_checked_elt.parent.nextSibling
                    ahk_exec_script = f"SoundSet {input_number_elt.value}"
                else:
                    ahk_exec_script = "錯誤"
            elif select_elt.value == "執行cmd命令":
                ahk_exec_script = "Run %comspec%"
                input_text_elt = div_func_conent_elt.select(
                    "input[type=text]")[0]
                input_checkbox_elt = div_func_conent_elt.select(
                    "input[type=checkbox]")[0]
                ahk_exec_script += " /c " if input_checkbox_elt.checked else " /k "
                ahk_exec_script += input_text_elt.value
            elif select_elt.value == "鎖定/登出/休眠/關機":
                system_action = doc["DIV_func_conent"].select(
                    "input[type='radio']:checked")[0].value
                system_action_force = doc["DIV_func_conent"].select(
                    "input[type='checkbox']")[0].checked
                if system_action == "lock":
                    DisableInputElt(doc["DIV_func_conent"].select(
                        "input[type='checkbox']")[0])
                    ahk_exec_script = "Run rundll32.exe user32.dll`,LockWorkStation"
                elif system_action == "logout":
                    UndisableInputElt(doc["DIV_func_conent"].select(
                        "input[type='checkbox']")[0])
                    ahk_exec_script = "Shutdown, {}".format(
                        0+4*system_action_force)
                elif system_action == "sleep":
                    DisableInputElt(doc["DIV_func_conent"].select(
                        "input[type='checkbox']")[0])
                    ahk_exec_script = 'DllCall("PowrProf\SetSuspendState", "int", 0, "int", 0, "int", 0)'
                elif system_action == "hibernate":
                    DisableInputElt(doc["DIV_func_conent"].select(
                        "input[type='checkbox']")[0])
                    ahk_exec_script = 'DllCall("PowrProf\SetSuspendState", "int", 1, "int", 0, "int", 0)'
                elif system_action == "shutdown":
                    UndisableInputElt(doc["DIV_func_conent"].select(
                        "input[type='checkbox']")[0])
                    ahk_exec_script = "Shutdown, {}".format(
                        1+4*system_action_force)
                elif system_action == "reboot":
                    UndisableInputElt(doc["DIV_func_conent"].select(
                        "input[type='checkbox']")[0])
                    ahk_exec_script = "Shutdown, {}".format(
                        2+4*system_action_force)
                else:
                    ahk_exec_script = ""
            elif select_elt.value == "禁用該組合鍵":
                ahk_exec_script = "return"
            elif select_elt.value == "進入滑鼠選取的網址":
                ahk_exec_script = "GoToClipboardWebSite()"
            elif select_elt.value == "點擊指定座標位置":
                x_pos, y_pos, ClickCount, Speed = [
                    inputNumberElt.value for inputNumberElt in doc["DIV_func_conent"].select("input[type='number']")]
                coord_mode = doc["DIV_func_conent"].select(
                    "input[type='radio']:checked")[0].value
                coord_mode = coord_mode[0].upper()+coord_mode[1:]
                Return = ("true" if doc["DIV_func_conent"].select(
                    "input[type='checkbox']")[0].checked else "false")
                ahk_exec_script = f"ClickPosition({x_pos}, {y_pos}, {ClickCount}, {Speed}, \"{coord_mode}\", {Return})"

            elif select_elt.value == "點擊畫面中的圖片":
                ImageFilePath = doc["DIV_func_conent"].select(
                    "input[type='text']")[0].value
                ClickCount, Speed = [inputNumberElt.value for inputNumberElt in doc["DIV_func_conent"].select(
                    "input[type='number']")]
                Return = ("true" if doc["DIV_func_conent"].select(
                    "input[type='checkbox']")[0].checked else "false")
                ShowError = ("true" if doc["DIV_func_conent"].select(
                    "input[type='checkbox']")[1].checked else "false")
                ahk_exec_script = f"ClickPicture(\"{ImageFilePath}\", {ClickCount}, {Speed},{Return},{ShowError})"

            elif select_elt.value == "AHK測試工具":
                ahk_test_tool_action = doc["DIV_func_conent"].select(
                    "input[type='radio']:checked")[0].value
                selected_show_msg = doc["DIV_func_conent"].select("select")[
                    0].value
                input_elt = doc["DIV_func_conent"].select(
                    "input[type='text']")[0]
                input_elt_value = (
                    input_elt.value if input_elt.value else input_elt.placeholder)
                if ahk_test_tool_action == "msgbox":
                    ahk_exec_script = ShowMsgByMsgbox_ahkCommand(
                        input_elt_value, selected_show_msg)
                elif ahk_test_tool_action == "tooltip":
                    ahk_exec_script = ShowMsgByTooltip_ahkCommand(
                        input_elt_value, selected_show_msg)

            elif select_elt.value == "AHK腳本操作":
                select_elt = doc["DIV_func_conent"].select("select")[0]
                if select_elt.value == "編輯目前腳本":
                    ahk_exec_script = "Run Notepad.exe %A_ScriptFullPath%"
                elif select_elt.value == "更新目前腳本(Reload)":
                    ahk_exec_script = "Run %A_AhkPath% /r %A_ScriptFullPath%"

            ##
            elif select_elt.value == "模擬點擊/輸入等":
                select_elt = doc["DIV_func_conent"].select("select")[0]
                input_cssSelector_elt = doc["DIV_func_conent"].select("input.css_selector")[
                    0]
                if doc["DIV_func_conent"].select("input.input_text"):
                    input_value = doc["DIV_func_conent"].select(
                        "input.input_text")[0].value
                elif doc["DIV_func_conent"].select("input.selected_index"):
                    input_value = doc["DIV_func_conent"].select(
                        "input.selected_index")[0].value
                else:
                    input_value = 0
                input_delayTime = doc["DIV_func_conent"].select("input.delay_time")[
                    0].value

                if select_elt.value == "點擊":
                    web_action = "Click"
                elif select_elt.value == "輸入":
                    web_action = "Input"
                elif select_elt.value == "選擇":
                    web_action = "Select"
                elif select_elt.value == "聚焦":
                    web_action = "Focus"

                selector_str = input_cssSelector_elt.value.replace("\"", "\'")

                ahk_exec_script = f"WebElementAction(\"{selector_str}\",\"{web_action}\",\"{input_value}\",{input_delayTime})"

            else:
                ahk_exec_script = "(錯誤)"

        # ahk_exec_script若為多行指令，則補上"return"
        if "\n" in (ahk_key_script+ahk_exec_script) and (ahk_exec_script[-6:] != "return"):
            ahk_exec_script += "\nreturn"

        # 合成AHK語法:合併組合鍵符號和執行語法
        ahk_script = ahk_key_script+ahk_exec_script

        # 消除空白行的程式碼
        ahk_script = ahk_script.replace("\n\n", "\n")

        # 若勾選僅在標題含有該文字的視窗下執行，就補充#if StringInActiveTitle函數
        if doc['ifWinTitle_CheckboxElt'].checked:
            string_in_active_title = doc['ifWinTitle_InputElt'].value
            ahk_script = f"#if StringInActiveTitle(\"{string_in_active_title}\")" + \
                "\n"+ahk_script+"\n"+"#if"

    # 更新DIV顯示對應AHK語法區塊文字
    div_ahk_srcipt_output = doc.select("#ahk_srcipt_output")
    # 若該區塊已經被BRYTHON生成，才執行更新動作
    if div_ahk_srcipt_output:
        # 顯示AHK語法
        div_ahk_srcipt_output[0].text = ahk_script

    # 定義動作:根據string內容列出包含的函數名稱列表
    def RelateFunctionList(string):
        return [function_name for function_name in FUNCTION_DICT.keys() if (function_name+"(" in string)]

    # 抓出組合鍵AHK語法包含的函數名稱列表
    ahk_related_function_list = RelateFunctionList(ahk_script)

    # 根據包含的函數名稱列表產生所有函式內容字串
    ahk_function_srcipt_output_text = "".join(
        [FUNCTION_DICT[function_name] for function_name in ahk_related_function_list])

    # 若組合鍵AHK語法不包含任何函式，則會在顯示函式頁籤內顯示"(無)"
    if ahk_function_srcipt_output_text == "":
        ahk_function_srcipt_output_text = "(無)"
        # 停用函式頁籤
        doc["function_div_page_tag"].classList.add("div_page_tag_none")
        # 強制切換至[AHK語法]標籤
        doc["ahk_script_div_page_tag"].click()

    # 若組合鍵AHK語法包含函式，就不斷追加函式內容語法中包含的函式內容
    else:
        # 不斷執行
        while True:
            # 獲取目前functino script字串包含的函式
            ahkFuntionOnly_related_function_list = RelateFunctionList(
                ahk_function_srcipt_output_text)
            # 若全部函式都已經包含在組合鍵AHK語法包含的函式內，就中止迴圈
            if set(ahkFuntionOnly_related_function_list) <= set(ahk_related_function_list):
                break
            # 若還有
            else:
                new_function_list = list(
                    set(ahkFuntionOnly_related_function_list)-set(ahk_related_function_list))
                ahk_related_function_list.extend(new_function_list)
                ahk_function_srcipt_output_text += "".join(
                    [FUNCTION_DICT[function_name] for function_name in new_function_list])
        # 開啟函式頁籤
        doc["function_div_page_tag"].classList.remove("div_page_tag_none")

    # 顯示關聯函式內容
    doc["ahk_function_srcipt_output"].text = ahk_function_srcipt_output_text

# 定義觸發事件:改變INPUT時變動AHK語法


def RenderAhkIfInputChange(ev):
    render_ahk_script()


# 設置樣式全域變數
ACTIVE_SCRIPT_TAG_COLOR = "#ddd"
UNACTIVE_SCRIPT_TAG_COLOR = "#bbb"

# 設定全域樣式
AddStyle("""
    .page_border span,.page_border select,.page_border option,.pointerCursor_onhover span{
        font-size:15px;
        font-family:微軟正黑體;
        font-weight:bold;
    }
    /* 禁用文字選取功能 */
    .user_select_none{
        -moz-user-select: none;
        -webkit-user-select: none;
        -ms-user-select: none;
        user-select: none;
        -o-user-select: none;
    }
""")

# 定義含文字勾選元素A_INPUTCheckbox，點擊文字也可進行勾選
# attr_dict可設定設置inputCheckbox勾選元素的附帶變數


def A_INPUTCheckbox(item_name, checked=False, attr_dict={"symbol": ""}, Class=None, id=None):
    # 定義SPAN文字被勾選時動作:勾選前方的checkbox
    def do_ckecking(ev):
        if ev.target.tagName != "INPUT":
            input_ckeckbox_elt = ev.currentTarget.select("input")[0]
            input_ckeckbox_elt.click()
    # 設置inputCheckbox勾選元素，並選擇性加上Class

    inputCheckbox_elt = INPUT(type="checkbox", checked=checked)
    if Class:
        inputCheckbox_elt.className = Class
    if id:
        inputCheckbox_elt.id = id
    if attr_dict:
        for k, v in attr_dict.items():
            setattr(inputCheckbox_elt, k, v)
    return SPAN(inputCheckbox_elt+SPAN(item_name), Class="pointerCursor_onhover").bind('click', do_ckecking)


# 設定DIV設定組合鍵功能區塊樣式
AddStyle("""
    .pointerCursor_onhover:hover *{
        cursor:pointer;
    }""")

# 定義含文字勾選元素A_INPUTCheckbox，點擊文字也可進行勾選


def A_INPUTRadio(item_name, checked=False, name="", value=""):
    # 定義SPAN文字被勾選時動作:選擇前方的Radio
    def do_ckecking(ev):
        if ev.target.tagName != "INPUT":
            input_ckeckbox_elt = ev.currentTarget.select("input")[0]
            input_ckeckbox_elt.click()
    inputRadio_elt = INPUT(type="radio", checked=checked,
                           name=name, value=value)
    return SPAN(inputRadio_elt+SPAN(item_name), Class="pointerCursor_onhover").bind('click', do_ckecking)


# 定義動作:關閉INPUT元素的互動，並使文字便灰
def DisableInputElt(input_elt):
    disable_text_color = "#bbb"
    input_elt.disabled = True
    input_elt.nextSibling.style.color = disable_text_color
# 定義動作:恢復INPUT元素的互動以及文字樣式


def UndisableInputElt(input_elt):
    undisable_text_color = "#000"
    input_elt.disabled = False
    input_elt.nextSibling.style.color = undisable_text_color

# 定義DIV設定組合鍵區塊元素【設定組合鍵】


def Div_hotkey_setting():

    # 定義SELECT選擇熱鍵元素
    def SELECT_hotkey():
        select_hotkey = SELECT(Class="normal_key")
        # 輸出A到Z選項
        for i in range(ord("A"), ord("Z")+1):
            select_hotkey <= OPTION(chr(i), value=chr(i))
        # 輸出常用按鍵選項
        for key in ["Enter", "Space", "Tab", "CapsLock", "Esc", "Backspace", "Delete", "Home", "End", "PgUp", "PgDn", "Insert", "PrintScreen", "AppsKey", "ScrollLock", "Pause"]:
            select_hotkey <= OPTION(key, value=key)
        # 輸出滑鼠按鍵選項
        select_hotkey <= OPTION("滑鼠左鍵", value="LButton")
        select_hotkey <= OPTION("滑鼠右鍵", value="RButton")
        select_hotkey <= OPTION("滑鼠中鍵", value="MButton")
        select_hotkey <= OPTION("滑鼠上滾", value="WheelUp")
        select_hotkey <= OPTION("滑鼠下滾", value="WheelDown")
        # 輸出方向鍵選項
        select_hotkey <= OPTION("↑", value="Up")
        select_hotkey <= OPTION("↓", value="Down")
        select_hotkey <= OPTION("←", value="Left")
        select_hotkey <= OPTION("→", value="Right")
        # 輸出數字鍵(上排和右側)按鍵選項
        select_hotkey <= OPTION("`", value="`")
        for key in [str(i) for i in range(10)]+["Numpad"+str(i) for i in range(10)]:
            select_hotkey <= OPTION(key, value=key)
        select_hotkey <= OPTION("Numpad.", value="NumpadDot")
        select_hotkey <= OPTION("Numpad/", value="NumpadDiv")
        select_hotkey <= OPTION("Numpad*", value="NumpadMult")
        select_hotkey <= OPTION("Numpad-", value="NumpadSub")
        select_hotkey <= OPTION("Numpad+", value="NumpadAdd")
        select_hotkey <= OPTION("NumpadEnter", value="NumpadEnter")
        select_hotkey <= OPTION("NumLock", value="NumLock")
        # 輸出F1至F24按鍵選項
        for key in ["F"+str(i) for i in range(1, 25)]:
            select_hotkey <= OPTION(key, value=key)
        # 預設組合鍵設定為^+C
        select_hotkey.selectedIndex = "2"
        return select_hotkey

    #定義組合鍵前綴DIV元素 - 收合型態
    def DIV_elt_Collapsed_prefixSymbol_setting():

        # 定義動作:展開前綴DIV元素
        def OpenPrefixSettingArea(ev):
            ev.currentTarget.style.display = "none"
            doc['div_elt_prefixSymbol_setting'].style.display = "block"

        div_elt = DIV(id="collapsed_prefixSymbol_setting")
        div_elt <= SPAN("︾", Class="expand_or_collapse_span_text")
        div_elt.bind("click", OpenPrefixSettingArea)
        return div_elt

    #定義組合鍵前綴DIV元素 - 展開型態
    def DIV_elt_Expanded_prefixSymbol_setting():

        # 定義勾取"使用程式開啟"時的動作:開放文字欄輸入
        def checkbox_onClick(ev):
            inputCheckbox_elt = ev.currentTarget
            input_elt = inputCheckbox_elt.parent.parent.select('input[type="text"]')[
                0]
            input_elt.disabled = (not inputCheckbox_elt.checked)

        # 定義動作:收起前綴DIV元素
        def CollapsePrefixSettingArea(ev):
            doc['div_elt_prefixSymbol_setting'].style.display = "none"
            doc['collapsed_prefixSymbol_setting'].style.display = "block"

        div_elt = DIV(id="div_elt_prefixSymbol_setting")

        # 設置收合區塊
        div_elt_do_collapse = DIV(id="div_elt_do_collapse")
        div_elt_do_collapse <= SPAN("︽", Class="expand_or_collapse_span_text")
        div_elt_do_collapse.bind("click", CollapsePrefixSettingArea)

        # 設置組合鍵前綴展開DIV子區塊
        div_elt_prefixSymbol_setting_area = DIV(
            id="div_elt_prefixSymbol_setting_area")
        div_elt_prefixSymbol_setting_area <= A_INPUTCheckbox(
            "保留預設按鍵功能", attr_dict={"symbol": "~"}, Class="prefix_function")+SPAN("　")
        div_elt_prefixSymbol_setting_area <= A_INPUTCheckbox(
            "避免自我觸發", attr_dict={"symbol": "$"}, Class="prefix_function")+SPAN("　")
        div_elt_prefixSymbol_setting_area <= A_INPUTCheckbox(
            "可在其他組合鍵觸發", attr_dict={"symbol": "*"}, Class="prefix_function")+BR()
        a_inputCheckbox_elt = A_INPUTCheckbox(
            "僅在標題含有該文字的視窗下執行: ", id="ifWinTitle_CheckboxElt")
        a_inputCheckbox_elt.select("input")[0].bind("click", checkbox_onClick)
        div_elt_prefixSymbol_setting_area <= a_inputCheckbox_elt
        div_elt_prefixSymbol_setting_area <= INPUT(
            type="text", id="ifWinTitle_InputElt", size="30", disabled=True)

        # 排版
        div_elt <= div_elt_do_collapse
        div_elt <= div_elt_prefixSymbol_setting_area
        return div_elt

    # 定義組合鍵前綴設定區塊(包含收合和展開)
    def DIV_elt_prefixSymbol_setting():
        div_elt = DIV()
        div_elt <= DIV_elt_Collapsed_prefixSymbol_setting()
        div_elt <= DIV_elt_Expanded_prefixSymbol_setting()
        return div_elt

    # 定義簡易組合鍵設定DIV區塊(分頁一)
    def DIV_elt_simple_setting():
        div_elt = DIV(id="div_elt_simple_setting")
        # 輸出勾選功能鍵
        div_elt <= A_INPUTCheckbox(
            "Ctrl", attr_dict={"symbol": "^"}, Class="function_key")+SPAN(" ")
        div_elt <= A_INPUTCheckbox(
            "Shift", attr_dict={"symbol": "+"}, Class="function_key")+SPAN(" ")
        div_elt <= A_INPUTCheckbox(
            "Alt", attr_dict={"symbol": "!"}, Class="function_key")+SPAN(" ")
        div_elt <= A_INPUTCheckbox(
            "Win", attr_dict={"symbol": "#"}, Class="function_key")+SPAN(" ")
        # 加上「+」符號
        div_elt <= SPAN("+ ")
        # 匹配一般按鍵
        div_elt <= SELECT_hotkey()
        # 預設:勾選Ctrl和Shift
        for input_checkbox_elt in div_elt.select("input[type='checkbox']")[:2]:
            input_checkbox_elt.click()

        return div_elt

    # 定義進階組合鍵設定DIV區塊(分頁二)
    def DIV_elt_advanced_setting():
        div_elt = DIV(id="div_elt_advanced_setting")
        table = TABLE()

        # 輸出勾選左側功能鍵
        tr_left_function_key = TR()
        tr_left_function_key <= TD(A_INPUTCheckbox(
            "LCtrl", attr_dict={"symbol": "<^"}, Class="function_key"))
        tr_left_function_key <= TD(A_INPUTCheckbox(
            "LShift", attr_dict={"symbol": "<+"}, Class="function_key"))
        tr_left_function_key <= TD(A_INPUTCheckbox(
            "LAlt", attr_dict={"symbol": "<!"}, Class="function_key"))
        tr_left_function_key <= TD(A_INPUTCheckbox(
            "LWin", attr_dict={"symbol": "<#"}, Class="function_key"))

        # 匹配一般按鍵
        tr_left_function_key <= TD(SPAN("+ ")+SELECT_hotkey(), rowspan="2")

        # 輸出勾選右側功能鍵
        tr_right_function_key = TR()
        tr_right_function_key <= TD(A_INPUTCheckbox(
            "RCtrl", attr_dict={"symbol": ">^"}, Class="function_key"))
        tr_right_function_key <= TD(A_INPUTCheckbox(
            "RShift", attr_dict={"symbol": ">+"}, Class="function_key"))
        tr_right_function_key <= TD(A_INPUTCheckbox(
            "RAlt", attr_dict={"symbol": ">!"}, Class="function_key"))
        tr_right_function_key <= TD(A_INPUTCheckbox(
            "RWin", attr_dict={"symbol": ">#"}, Class="function_key"))

        # 用表格排版
        table <= tr_left_function_key
        table <= tr_right_function_key
        div_elt <= table

        # 預設:勾選Ctrl和Shift
        for input_checkbox_elt in div_elt.select("input[type='checkbox']")[:2]:
            input_checkbox_elt.click()

        return div_elt

    # 定義自訂組合鍵設定DIV區塊(分頁三)
    def DIV_elt_custom_setting():
        div_elt = DIV(id="div_custom_setting")
        select_elt_hotkey_A = SELECT_hotkey()
        select_elt_hotkey_B = SELECT_hotkey()
        # 設定預設為Z+X
        select_elt_hotkey_A.value = "Z"
        select_elt_hotkey_B.value = "X"

        # 設置勾選元素:"不考慮按下先後順序"
        checkbox_elt = A_INPUTCheckbox("不考慮按下先後順序")
        checkbox_elt.select('input')[0].style = {'margin-top': '12px'}

        # 排版
        div_elt <= select_elt_hotkey_A + \
            SPAN(" + ")+select_elt_hotkey_B+SPAN("　")
        div_elt <= checkbox_elt

        return div_elt

    # 定義動作:更改組合鍵設定模式

    def ChangeHotkeySettingModel(ev):
        hotkey_setting_mode = ev.currentTarget.select("input")[0].value
        div_hotkey_setting_area = doc['div_hotkey_setting_area']
        div_hotkey_setting_area.clear()
        # 獲取"保留預設按鍵功能"INPUTCheckbox元素
        remain_keyFuntion_inputCheckbox_elt = doc['div_elt_prefixSymbol_setting_area'].select(
            'input[type="checkbox"]')[0]
        # 若為簡易模式
        if hotkey_setting_mode == "simple":
            div_hotkey_setting_area <= DIV_elt_simple_setting()
            # 推薦不使用"保留預設按鍵功能"
            if remain_keyFuntion_inputCheckbox_elt.checked:
                remain_keyFuntion_inputCheckbox_elt.click()
        # 若為進階模式
        elif hotkey_setting_mode == "advanced":
            div_hotkey_setting_area <= DIV_elt_advanced_setting()
            # 推薦不使用"保留預設按鍵功能"
            if remain_keyFuntion_inputCheckbox_elt.checked:
                remain_keyFuntion_inputCheckbox_elt.click()
        # 若為自訂模式
        elif hotkey_setting_mode == "custom":
            div_hotkey_setting_area <= DIV_elt_custom_setting()
            # 推薦使用"保留預設按鍵功能"
            if not remain_keyFuntion_inputCheckbox_elt.checked:
                remain_keyFuntion_inputCheckbox_elt.click()

        # 綁定新生成的功能子選項元素:改變inupt元素時更新AHK語法
        for input_elt in div_hotkey_setting_area.select("input"):
            input_elt.bind("input", RenderAhkIfInputChange)
        # 綁定新生成的功能子選項元素:改變select元素時更新AHK語法
        for select_elt in div_hotkey_setting_area.select("select"):
            select_elt.bind("change", RenderAhkIfInputChange)

        # 刷新語法
        render_ahk_script()

    # 排版
    div_hotkey_setting = DIV(id="div_hotkey_setting", Class="user_select_none")

    div_hotkey_setting <= A_INPUTRadio("簡易", checked=True, name="hotkey_setting_mode", value="simple").bind(
        "input", ChangeHotkeySettingModel)+SPAN(" ")
    div_hotkey_setting <= A_INPUTRadio("進階", checked=False, name="hotkey_setting_mode", value="advanced").bind(
        "input", ChangeHotkeySettingModel)+SPAN(" ")
    div_hotkey_setting <= A_INPUTRadio("自訂", checked=False, name="hotkey_setting_mode", value="custom").bind(
        "input", ChangeHotkeySettingModel)

    # 主設定區塊DIV

    div_hotkey_setting_area = DIV(id="div_hotkey_setting_area")
    div_hotkey_setting_area <= DIV_elt_simple_setting()
    div_hotkey_setting <= div_hotkey_setting_area

    div_hotkey_setting <= DIV_elt_prefixSymbol_setting()

    # 綁定新生成的功能子選項元素:改變inupt元素時更新AHK語法
    for input_elt in div_hotkey_setting.select("input"):
        input_elt.bind("input", RenderAhkIfInputChange)
    # 綁定新生成的功能子選項元素:改變select元素時更新AHK語法
    for select_elt in div_hotkey_setting.select("select"):
        select_elt.bind("change", RenderAhkIfInputChange)

    return div_hotkey_setting


AddStyle("""
    .expand_or_collapse_span_text{
        font-size: 20px;
        font-weight: normal;
    }
    #div_hotkey_setting_area{
        margin-top: 7px;
    }

    #div_elt_prefixSymbol_setting, #div_elt_prefixSymbol_setting_area, #collapsed_prefixSymbol_setting{
        background-color: #d6fff9;
    }

    #div_elt_prefixSymbol_setting, #collapsed_prefixSymbol_setting{
        margin-top: 12px;
    }
    #collapsed_prefixSymbol_setting{
        text-align: center;
        height: 15px;
        border-radius: 20px;
        cursor: pointer;
    }
    #div_elt_prefixSymbol_setting{
        border-radius: 10px;
    }

    #div_elt_do_collapse{
        text-align: center;
        cursor: pointer;
    }
    #div_elt_prefixSymbol_setting_area{
        height: 100px;
        border-radius: 10px;
        padding-left: 15px;
        padding-bottom: 20px;
        padding-top: 10px;
    }
    #ifWinTitle_InputElt{
        margin-top: 10px;
    }""")


# 定義DIV設定執行功能區塊【設定功能】
def DIV_function():
    # 設置準輸出DIV元素
    div_elt = DIV(id="DIV_function", Class="user_select_none")

    # 2#定義DIV功能子選項(路徑、方式、對象等)區塊
    def DIV_func_conent(func_name):
        div_elt = DIV(id="DIV_func_conent")
        if func_name == "開啟檔案":
            div_elt <= SPAN("檔案路徑: ")
            div_elt <= INPUT(type="text", size="30")+BR()
            # 定義勾取"使用程式開啟"時的動作:開放文字欄輸入

            def checkbox_onClick(ev):
                inputCheckbox_elt = ev.currentTarget
                input_elt = inputCheckbox_elt.parent.parent.select('input[type="text"]')[
                    1]
                input_elt.disabled = (not inputCheckbox_elt.checked)
            a_inputCheckbox_elt = A_INPUTCheckbox("使用程式開啟(路徑):")
            a_inputCheckbox_elt.select("input")[0].bind(
                "click", checkbox_onClick)
            div_elt <= a_inputCheckbox_elt
            div_elt <= INPUT(type="text", size="30", disabled=True)
        elif func_name == "開啟資料夾":
            div_elt <= SPAN("資料夾路徑: ")+INPUT(type="text",
                                             size="30", placeholder="C:\\")
        elif func_name == "開啟網頁":
            div_elt <= SPAN("網址: ")
            div_elt <= INPUT(type="text", size="30",
                             placeholder="www.google.com")
        elif func_name == "進入滑鼠選取的網址":
            pass
        elif func_name == "搜尋滑鼠選取的關鍵字":  # 待追加
            select_elt = SELECT(
                style={"margin-top": "10px"}, id="select_searchWebSite")
            select_elt <= OPTION("Google搜尋")
            select_elt <= OPTION("Youtube搜尋")
            select_elt <= OPTION("自訂...")
            select_elt <= OPTION("WIKI維基百科")
            select_elt <= OPTION("Google地圖搜尋")
            select_elt <= OPTION("Google搜尋趨勢")
            select_elt <= OPTION("Google翻譯")
            select_elt <= OPTION("Evernote搜尋")
            select_elt <= OPTION("Facebook搜尋")
            select_elt <= OPTION("cdict(英翻中/中翻英)")
            select_elt <= OPTION("噗浪搜尋")
            select_elt <= OPTION("推特搜尋")
            select_elt <= OPTION("萌典(中文字典)")

            span_websiteName_elt = SPAN(id="website_name", Class="hidden")
            span_websiteName_elt <= SPAN(
                " 網站名稱(可選):")+INPUT(type="text", id="input_website_name")

            div_elt <= SPAN("進行 ")+select_elt
            div_elt <= span_websiteName_elt
            div_elt <= BR()+BR()
            div_elt <= A_INPUTCheckbox(
                "若無選取文字，則跳出搜尋框", checked=True, id="inputCheck_showInputBox")
            div_elt <= HR()
            div_elt <= SPAN("關鍵字之前的網址: ")
            input_elt_A = INPUT(value="https://www.google.com.tw/search?q=",
                                type="text", size="40", disabled=True, id="input_A_url")
            div_elt <= input_elt_A+BR()
            div_elt <= SPAN("關鍵字之後的網址: ")
            input_elt_B = INPUT(value="", type="text",
                                size="40", disabled=True, id="input_B_url")
            div_elt <= input_elt_B

            # 定義動作:更換INPUT關鍵字前後網址

            def change_input(ev):
                select_elt = ev.currentTarget
                input_elt_A.disabled = True
                input_elt_B.disabled = True
                if select_elt.value == "Google搜尋":
                    input_elt_A.value = "https://www.google.com.tw/search?q="
                    input_elt_B.value = ""
                elif select_elt.value == "Youtube搜尋":
                    input_elt_A.value = "https://www.youtube.com/results?search_query="
                    input_elt_B.value = ""
                elif select_elt.value == "WIKI維基百科":
                    input_elt_A.value = "http://zh.wikipedia.org/w/index.php?title=Special:Search&search="
                    input_elt_B.value = ""
                elif select_elt.value == "Google地圖搜尋":
                    input_elt_A.value = "https://www.google.com.tw/maps/search/"
                    input_elt_B.value = ""
                elif select_elt.value == "Google搜尋趨勢":
                    input_elt_A.value = "https://www.google.com/trends/explore?q="
                    input_elt_B.value = ""
                elif select_elt.value == "Google翻譯":
                    input_elt_A.value = "https://translate.google.com.tw/?tab=wT#view=home&op=translate&sl=auto&tl=zh-TW&text="
                    input_elt_B.value = ""
                elif select_elt.value == "Facebook搜尋":
                    input_elt_A.value = "https://www.facebook.com/search/top/?q="
                    input_elt_B.value = ""
                elif select_elt.value == "Evernote搜尋":
                    input_elt_A.value = "https://www.evernote.com/client/web#?query="
                    input_elt_B.value = ""
                elif select_elt.value == "噗浪搜尋":
                    input_elt_A.value = "https://www.plurk.com/w/#"
                    input_elt_B.value = "?time=365"
                elif select_elt.value == "推特搜尋":
                    input_elt_A.value = "https://twitter.com/search?q="
                    input_elt_B.value = ""
                elif select_elt.value == "cdict(英翻中/中翻英)":
                    input_elt_A.value = "https://cdict.net/?q="
                    input_elt_B.value = ""
                elif select_elt.value == "萌典(中文字典)":
                    input_elt_A.value = "https://www.moedict.tw/"
                    input_elt_B.value = ""
                else:
                    input_elt_A.value = ""
                    input_elt_A.disabled = False
                    input_elt_B.value = ""
                    input_elt_B.disabled = False

                if select_elt.value == "自訂...":
                    doc['website_name'].classList.remove("hidden")
                else:
                    doc['website_name'].classList.add("hidden")

            select_elt.bind("change", change_input)

        elif func_name == "點擊指定座標位置":
            def inputTextChangeRange(ev):
                ev.currentTarget.nextSibling.value = ev.currentTarget.value

            def inputRangeChangeText(ev):
                ev.currentTarget.previousSibling.value = ev.currentTarget.value

            def inputTextOrRangeChangeSpan(ev):
                value = int(ev.currentTarget.value)
                if value == 0:
                    span_text = "立即"
                elif 1 <= value <= 3:
                    span_text = "快速"
                elif 4 <= value <= 6:
                    span_text = "適中"
                elif 7 <= value <= 9:
                    span_text = "緩慢"
                else:
                    span_text = "極慢"
                if ev.currentTarget.type == "range":
                    ev.currentTarget.nextSibling.text = span_text
                elif ev.currentTarget.type == "number":
                    ev.currentTarget.nextSibling.nextSibling.text = span_text
            div_elt <= SPAN("座標　X:")+INPUT(type="number", value="100", min="0", style={"width": "60px"})+SPAN(
                " Y: ")+INPUT(type="number", value=200, step=1, style={"width": "60px"})+BR()
            div_elt <= TABLE(
                TR(
                    TD(SPAN("以", style={"margin-left": "-3px"}), rowspan="3")
                    + TD(A_INPUTRadio("屏幕", checked=True,
                         name="coordinate_item", value="screen"))
                    + TD(SPAN("的左上角作為座標原點"), rowspan="3")
                )
                + TR(TD(A_INPUTRadio("當前視窗", checked=False,
                     name="coordinate_item", value="window")))
                + TR(TD(A_INPUTRadio("滑鼠目前位置", checked=False, name="coordinate_item", value="relative"))), style={"margin-top": "10px"}
            )
            div_elt <= SPAN("點擊")+INPUT(type="number", value=1,
                                        min=0, step=1, style={"width": "30px"})+SPAN("次　")
            div_elt <= SPAN("移動延遲")+INPUT(type="number", value=0, min=0, max=10, step=1, style={"width": "30px"}).bind("input", inputTextChangeRange).bind("input", inputTextOrRangeChangeSpan)+INPUT(
                type="range", value=0, max=10, min=0, style={"width": "80px", "position": "relative", "top": "6px"}).bind("input", inputRangeChangeText).bind("input", inputTextOrRangeChangeSpan)+SPAN("立即")+BR()

            a_INPUTCheckbox = A_INPUTCheckbox("點擊後返回原位置", checked=True)
            a_INPUTCheckbox.select('input[type="checkbox"]')[
                0].style = {'margin-top': '12px'}
            div_elt <= a_INPUTCheckbox

        elif func_name == "點擊畫面中的圖片":
            div_elt <= SPAN("圖片檔案路徑: ")
            div_elt <= INPUT(type="text", size="30")+BR()

            def inputTextChangeRange(ev):
                ev.currentTarget.nextSibling.value = ev.currentTarget.value

            def inputRangeChangeText(ev):
                ev.currentTarget.previousSibling.value = ev.currentTarget.value

            def inputTextOrRangeChangeSpan(ev):
                value = int(ev.currentTarget.value)
                if value == 0:
                    span_text = "立即"
                elif 1 <= value <= 3:
                    span_text = "快速"
                elif 4 <= value <= 6:
                    span_text = "適中"
                elif 7 <= value <= 9:
                    span_text = "緩慢"
                else:
                    span_text = "極慢"
                if ev.currentTarget.type == "range":
                    ev.currentTarget.nextSibling.text = span_text
                elif ev.currentTarget.type == "number":
                    ev.currentTarget.nextSibling.nextSibling.text = span_text

            div_elt <= SPAN("點擊")+INPUT(type="number", value=1,
                                        min=0, step=1, style={"width": "30px"})+SPAN("次　")
            div_elt <= SPAN("移動延遲")+INPUT(type="number", value=0, min=0, max=10, step=1, style={"width": "30px"}).bind("input", inputTextChangeRange).bind("input", inputTextOrRangeChangeSpan)+INPUT(
                type="range", value=0, max=10, min=0, style={"width": "80px", "position": "relative", "top": "6px"}).bind("input", inputRangeChangeText).bind("input", inputTextOrRangeChangeSpan)+SPAN("立即")+BR()

            a_INPUTCheckbox = A_INPUTCheckbox("點擊後返回原位置", checked=True)
            a_INPUTCheckbox.select('input[type="checkbox"]')[
                0].style = {'margin-top': '12px'}
            div_elt <= a_INPUTCheckbox+BR()

            a_INPUTCheckbox = A_INPUTCheckbox("若圖片不在畫面上就跳出警示", checked=False)
            a_INPUTCheckbox.select('input[type="checkbox"]')[
                0].style = {'margin-top': '12px'}
            div_elt <= a_INPUTCheckbox

        elif func_name == "執行程式":
            select_elt = SELECT()
            select_elt <= OPTION("程式路徑 ")
            select_elt <= OPTION("記事本")
            select_elt <= OPTION("小算盤")
            select_elt <= OPTION("小畫家")
            select_elt <= OPTION("剪取工具")
            select_elt <= OPTION("命令提示字元")
            # 定義動作:更換INPUT程式路徑

            def change_input(ev):
                select_elt = ev.currentTarget
                input_elt = select_elt.nextSibling
                input_elt.remove()
                div_elt = select_elt.parent
                if select_elt.value == "程式路徑":
                    input_elt = INPUT(type="text", size="30")
                elif select_elt.value == "記事本":
                    input_elt = INPUT(value="Notepad.exe",
                                      disabled=True, type="text", size="30")
                elif select_elt.value == "小算盤":
                    input_elt = INPUT(
                        value="%A_WinDir%\system32\calc.exe", disabled=True, type="text", size="30")
                elif select_elt.value == "小畫家":
                    input_elt = INPUT(
                        value="%A_WinDir%\system32\mspaint.exe", disabled=True, type="text", size="30")
                elif select_elt.value == "自黏便箋":
                    input_elt = INPUT(value="StikyNot.exe",
                                      disabled=True, type="text", size="30")
                elif select_elt.value == "剪取工具":
                    input_elt = INPUT(
                        value="%A_WinDir%\system32\SnippingTool.exe", disabled=True, type="text", size="30")
                elif select_elt.value == "命令提示字元":
                    input_elt = INPUT(
                        value="%A_WinDir%\system32\cmd.exe", disabled=True, type="text", size="30")
                div_elt <= input_elt
            div_elt <= select_elt.bind("change", change_input)
            div_elt <= INPUT(type="text", size="30")
        elif func_name == "終止程序":
            div_elt <= SPAN("程序名稱: ")+INPUT(type="text", size="30")
        elif func_name == "清空資源回收桶":
            pass
        elif func_name == "插入文字":
            div_elt <= SPAN("文字: ")+INPUT(type="text", size="30",
                                          placeholder="123", id="input_inserted_text")+BR()
            form_elt = FORM()
            form_elt <= A_INPUTRadio(
                "使用剪貼簿　", checked=True, name="insert_string_method", value="AutoInput")
            form_elt <= A_INPUTRadio(
                "使用SendInput　", name="insert_string_method", value="SendInput")
            form_elt <= A_INPUTRadio(
                "使用SendRaw　", name="insert_string_method", value="SendRaw")
            form_elt <= A_INPUTRadio(
                "使用Send", name="insert_string_method", value="Send")
            div_elt <= form_elt
        elif func_name == "熱字串(自動展開縮寫)":
            # 定義動作:滑鼠點擊文字框後將所有預設文字(placeholder)消除
            def ClearPlaceholder(ev):
                for input_elt in ev.currentTarget.parent.select("input[type='text']"):
                    input_elt.placeholder = ""
            div_elt <= SPAN("輸入縮寫: ")+INPUT(type="text", size="10",
                                            placeholder="btw").bind("focusin", ClearPlaceholder)+SPAN("時 ,")+BR()
            div_elt <= SPAN("展開文字: ")+INPUT(type="text", size="30",
                                            placeholder="By the way").bind("focusin", ClearPlaceholder)+BR()
            # 設置勾選元素並設定attr_dict:打勾選項會在ahk熱字串設定符號加入symbol，否則加入nosymbol
            div_elt <= A_INPUTCheckbox("按下終止鍵後展開(如空格、Enter、Tab...)", checked=True, attr_dict={
                                       "symbol": "", "nosymbol": "*"})+BR()
            div_elt <= A_INPUTCheckbox("展開後不觸發終止鍵　", checked=True, attr_dict={
                                       "symbol": "o", "nosymbol": ""})
            div_elt <= A_INPUTCheckbox("縮寫區分大小寫　", checked=True, attr_dict={
                                       "symbol": "c", "nosymbol": ""})
            div_elt <= A_INPUTCheckbox("可在字詞間展開　", checked=True, attr_dict={
                                       "symbol": "?", "nosymbol": ""})+BR()
            div_elt <= A_INPUTCheckbox("使用剪貼簿展開(解決中英切換問題)　", checked=False)
        elif func_name == "音量調節":
            def ClickPreviousSelectEltWhenInputChange(ev):
                ev.currentTarget.previousSibling.click()

            def ChangeVolumeValue(ev):
                ev.currentTarget.nextSibling.text = ev.currentTarget.value

            form_elt = FORM()
            input_number_style_dict = {"width": "50px", "text-align": "right"}
            form_elt <= A_INPUTRadio("提高 ", checked=True, name="volumn", value="up")+INPUT(value="2", type="number",
                                                                                           style=input_number_style_dict).bind("focus", ClickPreviousSelectEltWhenInputChange)+SPAN(" %")+BR()
            form_elt <= A_INPUTRadio("降低 ", name="volumn", value="down")+INPUT(value="2", type="number", max="50", min="0",
                                                                               style=input_number_style_dict).bind("focus", ClickPreviousSelectEltWhenInputChange)+SPAN(" %")+BR()
            form_elt <= A_INPUTRadio(
                "靜音/取消靜音", name="volumn", value="mute")+BR()
            form_elt <= A_INPUTRadio("變更為 ", name="volumn", value="set")+INPUT(value="50", step="1", type="range", max="100", min="0").bind(
                "input", ChangeVolumeValue).bind("focus", ClickPreviousSelectEltWhenInputChange)+SPAN("50")+SPAN(" %")+BR()
            div_elt <= form_elt
        elif func_name == "執行cmd命令":
            div_elt <= SPAN("指令碼: ")
            div_elt <= INPUT(type="text", size="30")+BR()
            div_elt <= A_INPUTCheckbox("執行完後關閉視窗")
        elif func_name == "鎖定/登出/休眠/關機":
            form_elt = FORM(style={"margin-top": "8px"})
            form_elt <= A_INPUTRadio(
                "鎖定　", checked=True, name="system_action", value="lock")
            form_elt <= A_INPUTRadio(
                "登出　", name="system_action", value="logout")
            form_elt <= A_INPUTRadio(
                "睡眠　", name="system_action", value="sleep")
            form_elt <= A_INPUTRadio(
                "休眠　", name="system_action", value="hibernate")
            form_elt <= A_INPUTRadio(
                "關機　", name="system_action", value="shutdown")
            form_elt <= A_INPUTRadio(
                "重新啟動　", name="system_action", value="reboot")
            div_elt <= form_elt+BR()
            div_elt <= A_INPUTCheckbox("強制執行")
        elif func_name == "禁用該組合鍵":
            pass
        elif func_name == "AHK腳本操作":
            select_elt = SELECT()
            select_elt <= OPTION("編輯目前腳本")
            select_elt <= OPTION("更新目前腳本(Reload)")
            div_elt <= select_elt
        elif func_name == "AHK測試工具":
            div_elt <= A_INPUTRadio(
                "跳出視窗　", name="ahkTestTool_action", value="msgbox", checked=True)
            div_elt <= A_INPUTRadio(
                "跳出提示", name="ahkTestTool_action", value="tooltip")+BR()

            # 定義綁定事件:選擇顯示變量改變input的value
            def ChangeInputShowingTestElt(ev):
                select_elt = ev.currentTarget
                input_elt = select_elt.nextSibling
                if select_elt.value == "訊息文字":
                    input_elt.value = ""
                    input_elt.disabled = False
                elif select_elt.value == "今天日期":
                    input_elt.value = "%A_YYYY%/%A_MM%/%A_DD%"
                    input_elt.disabled = True
                elif select_elt.value == "目前滑鼠位置":
                    input_elt.value = "(%posX%,%posY%)"
                    input_elt.disabled = True
                elif select_elt.value == "目前視窗名稱":
                    input_elt.value = ""
                    input_elt.placeholder = ""
                    input_elt.disabled = True
                else:
                    input_elt.value = "(錯誤)"
                    input_elt.disabled = True

            # 定義顯示文本/變量內容DIV區塊
            def MsgContent():
                default_msg_str = "Hello"

                # 定義綁定清空預設內容
                def ClearPlaceholder(ev):
                    ev.currentTarget.placeholder = ""

                # 定義綁定恢復預設內容
                def RecoverPlaceholder(ev):
                    ev.currentTarget.placeholder = default_msg_str

                div_elt = DIV(style={"margin-left": "5px"})

                select_elt = SELECT()
                select_elt <= OPTION("訊息文字")
                select_elt <= OPTION("今天日期")
                select_elt <= OPTION("目前滑鼠位置")
                select_elt <= OPTION("目前視窗名稱")

                select_elt.bind("change", ChangeInputShowingTestElt)

                div_elt <= select_elt+INPUT(type="text", size="20", placeholder=default_msg_str).bind(
                    "focus", ClearPlaceholder).bind("focusout", RecoverPlaceholder)
                return div_elt

            div_elt <= MsgContent()

        elif func_name == "模擬點擊/輸入等":

            # 設置設定CSS語法區塊
            def DIV_SAPN_INPUT_targetWebEltCSS():
                div_elt = DIV(style={"margin-top": "7px"})
                div_elt <= SPAN("目標網頁物件: ")+INPUT(
                    style={"width": "300px"},
                    placeholder=" 輸入該物件的CSS選擇器",
                    Class="css_selector",
                ).bind("input", RenderAhkIfInputChange)
                return div_elt

            # 設置延遲設定區塊
            def DIV_settingDelay():
                div_elt = DIV(style={"margin-top": "7px"})
                div_elt <= SPAN("執行延遲 ")+INPUT(
                    value="100",
                    type="number",
                    min="1",
                    Class="delay_time",
                    style={
                        "width": "60px",
                        "margin-top": "10px",
                    }).bind("input", RenderAhkIfInputChange)+SPAN(" 毫秒 (設置太短可能執行失敗)")
                return div_elt

            # 設置點擊網頁物件設定DIV元素
            def DIV_ClickWebEltAction():
                div_elt = DIV()
                div_elt <= DIV_SAPN_INPUT_targetWebEltCSS()
                div_elt <= DIV_settingDelay()
                return div_elt

            # 設置聚焦網頁物件設定DIV元素
            def DIV_FocusWebEltAction():
                div_elt = DIV()
                div_elt <= DIV_SAPN_INPUT_targetWebEltCSS()
                div_elt <= DIV_settingDelay()
                return div_elt

            # 設置輸入網頁物件設定DIV元素
            def DIV_InputWebEltAction():
                div_elt = DIV()
                div_elt <= DIV_SAPN_INPUT_targetWebEltCSS()
                div_elt <= SPAN("輸入文字 ")+INPUT(style={"margin-top": "10px"},
                                               Class="input_text").bind("input", RenderAhkIfInputChange)
                div_elt <= DIV_settingDelay()
                return div_elt

            # 設置選擇網頁物件設定DIV元素
            def DIV_SelectWebEltAction():
                div_elt = DIV()
                div_elt <= DIV_SAPN_INPUT_targetWebEltCSS()
                div_elt <= SPAN(" 選擇第 ")+INPUT(
                    type="number",
                    min="1",
                    Class="selected_index",
                    style={
                        "width": "35px",
                        "margin-top": "10px",
                    }).bind("input", RenderAhkIfInputChange)+SPAN(" 個項目")
                div_elt <= DIV_settingDelay()
                return div_elt

            # 定義綁定事件:選擇網頁物件方法，改變輸入內容
            def ChangeWebAction(ev):

                # 清空設置區塊
                div_elt = doc['div_webAction_setting']
                div_elt.clear()

                if ev.currentTarget.value == "點擊":
                    div_elt <= DIV_ClickWebEltAction()
                elif ev.currentTarget.value == "聚焦":
                    div_elt <= DIV_FocusWebEltAction()
                elif ev.currentTarget.value == "輸入":
                    div_elt <= DIV_InputWebEltAction()
                elif ev.currentTarget.value == "選擇":
                    div_elt <= DIV_SelectWebEltAction()

            select_elt = SELECT()
            select_elt.bind("change", ChangeWebAction)
            select_elt <= OPTION("點擊")
            select_elt <= OPTION("輸入")
            select_elt <= OPTION("選擇")
            select_elt <= OPTION("聚焦")
            div_elt <= select_elt

            div_webAction_setting_elt = DIV(id="div_webAction_setting")
            div_webAction_setting_elt <= DIV_ClickWebEltAction()

            div_elt <= div_webAction_setting_elt

        # 特別處理:如果功能是熱字串，則關閉設定組合建功能，文字變灰
        div_hotkey_setting = doc["div_hotkey_setting"]
        inputAndSelect_elt_in_input_key_area_list = div_hotkey_setting.select(
            "input")+div_hotkey_setting.select("select")
        span_elt_in_input_key_area_list = div_hotkey_setting.select("span")
        if func_name == "熱字串(自動展開縮寫)":
            for elt in inputAndSelect_elt_in_input_key_area_list:
                elt.disabled = True
            for elt in span_elt_in_input_key_area_list:
                elt.style.color = "#bbb"
        else:
            for elt in inputAndSelect_elt_in_input_key_area_list:
                elt.disabled = False
            for elt in span_elt_in_input_key_area_list:
                elt.style.color = ""

        return div_elt

    # 定義動作:選擇功能選項時改變功能子選項(檔案路徑等)區塊
    def change_div_func_conent(ev):
        div_func_conent = ev.currentTarget.nextSibling
        div_func = ev.currentTarget.parent
        div_func_conent.remove()
        div_func <= DIV_func_conent(ev.currentTarget.value)
        # 綁定新生成的功能子選項元素:改變inupt元素時更新AHK語法
        for input_elt in div_func.select("input"):
            input_elt.bind("input", RenderAhkIfInputChange)
        # 綁定新生成的功能子選項元素:改變select元素時更新AHK語法
        for select_elt in div_func.select("select"):
            select_elt.bind("change", RenderAhkIfInputChange)

    # 1#設置功能選單
    select_function = SELECT(id="SELECT_function").bind(
        'change', change_div_func_conent)

    optgroup_elt = OPTGROUP(label="啟動指令")
    optgroup_elt <= OPTION("開啟檔案")
    optgroup_elt <= OPTION("開啟資料夾")
    optgroup_elt <= OPTION("開啟網頁")
    optgroup_elt <= OPTION("執行程式")
    optgroup_elt <= OPTION("終止程序")
    select_function <= optgroup_elt

    optgroup_elt = OPTGROUP(label="文字相關")
    optgroup_elt <= OPTION("插入文字")
    optgroup_elt <= OPTION("熱字串(自動展開縮寫)")
    select_function <= optgroup_elt

    optgroup_elt = OPTGROUP(label="選取文字後的動作")
    optgroup_elt <= OPTION("搜尋滑鼠選取的關鍵字")
    optgroup_elt <= OPTION("進入滑鼠選取的網址")
    select_function <= optgroup_elt

    optgroup_elt = OPTGROUP(label="模擬滑鼠")
    optgroup_elt <= OPTION("點擊指定座標位置")
    optgroup_elt <= OPTION("點擊畫面中的圖片", Class="updated")
    select_function <= optgroup_elt

    optgroup_elt = OPTGROUP(label="模擬網頁物件操作")
    optgroup_elt <= OPTION("模擬點擊/輸入等", Class="updated")
    select_function <= optgroup_elt

    optgroup_elt = OPTGROUP(label="系統動作")
    optgroup_elt <= OPTION("清空資源回收桶")
    optgroup_elt <= OPTION("執行cmd命令")
    optgroup_elt <= OPTION("鎖定/登出/休眠/關機")
    select_function <= optgroup_elt

    optgroup_elt = OPTGROUP(label="系統設定")
    optgroup_elt <= OPTION("音量調節")
    optgroup_elt <= OPTION("禁用該組合鍵")
    select_function <= optgroup_elt

    optgroup_elt = OPTGROUP(label="AHK相關")
    optgroup_elt <= OPTION("AHK腳本操作")
    optgroup_elt <= OPTION("AHK測試工具", Class="updated")
    select_function <= optgroup_elt

    # 綁定新生成的設定功能選項元素:改變select元素時更新AHK語法
    select_function.bind("change", RenderAhkIfInputChange)
    # 預設設定功能為開啟資料夾
    select_function.selectedIndex = "1"
    # 排版
    div_elt <= select_function
    div_func_conent = DIV_func_conent("開啟資料夾")  # 預設設定功能為開啟資料夾
    div_elt <= div_func_conent
    # 綁定新生成的功能子選項元素:改變inupt元素時更新AHK語法
    for input_elt in div_func_conent.select("input"):
        input_elt.bind("input", RenderAhkIfInputChange)
    # 綁定新生成的功能子選項元素:改變select元素時更新AHK語法
    for select_elt in div_func_conent.select("select"):
        select_elt.bind("change", RenderAhkIfInputChange)
    return div_elt


# 設定DIV設定組合鍵功能區塊樣式
AddStyle("""
    input[type="text"]{
        margin:10px 3px 3px 3px;
    }
    #DIV_func_conent{
        margin-top: 10px;
        margin-left: 30px;
    }
""")

AddStyle("""
    .div_page_tag_none{
        color: #666;
        text-shadow: #eee 1px 2px;
        cursor:default !important;
        pointer-events:none !important;
    }
""")

# 定義DIV顯示對應AHK語法區塊


def DIV_ahkScriptBlock():
    div_elt = DIV(Class="div_ahk_srcipt")
    div_container = DIV(Class="ahk_block_container")
    div_elt <= div_container
    div_container <= PRE("請勾選組合鍵設定", id="ahk_srcipt_output")
    div_container <= PRE("(無)", id="ahk_function_srcipt_output", style={
                         "display": "none"})
    div_container <= DIV(
        BUTTON("複製所有函式", id="copy_all_function_button").bind(
            "click", doCopyAllFunction)
        + PRE(
            "".join(FUNCTION_DICT.values()),
        ),
        id="all_function_srcipt_output",
        style={"display": "none"},

    )

    return div_elt


# 設定DIV顯示對應AHK語法區塊樣式
AddStyle("""
    #copy_all_function_button{
        float:right;
    }
    .ahk_block_container{
        padding:10px;
        overflow-x:scroll;
    }
    #ahk_srcipt_output,#ahk_function_srcipt_output{
        width:100%;
        background-color:"""+ACTIVE_SCRIPT_TAG_COLOR+""";
    }
    #ahk_srcipt_output{
        font-size: 18px;
        font-family: 新明細體;
        margin:0;
    }
    #ahk_function_srcipt_output{
        border:0;
    }
""")


# 定義DIV語法顯示區域切換標籤區塊
def DIV_SciptTabs():

    # 定義切換頁籤動作
    def SwitchScriptPage(ev):
        # 獲取跳轉物件
        div_sciptTabs = ev.currentTarget.parent
        div_tag_current = div_sciptTabs.select("div.tag_active")[0]
        div_tag_jumpTo = ev.currentTarget
        # 若符合跳轉條件
        if div_tag_current != div_tag_jumpTo:
            # 切換AHK標籤的樣式:透過增減ClassName

            # 跳離目前tab和AHK語法區塊
            div_tag_current.classList.remove("tag_active")
            div_tag_current.classList.add("tag_unactive")
            doc[div_tag_current.correspond_div_page_id].style.display = "none"

            # 跳至點遠tab和AHK語法區塊
            div_tag_jumpTo.classList.remove("tag_unactive")
            div_tag_jumpTo.classList.add("tag_active")
            doc[div_tag_jumpTo.correspond_div_page_id].style.display = "block"

    div_elt = DIV()

    # 定義DIV標籤，預設為非激活狀態
    def DIV_Tab(string, Class="tag_unactive", correspond_div_page_id="", id=None):
        style = {"width": "auto", "float": "left", "padding": "8px",
                 "cursor": "pointer", "border-raius": ""}
        if id:
            div_elt = DIV(string, Class=Class, style=style, id=id)
        else:
            div_elt = DIV(string, Class=Class, style=style)
        div_elt.bind("click", SwitchScriptPage)
        div_elt.classList.add("ahk_script_tag")
        div_elt.correspond_div_page_id = correspond_div_page_id
        return div_elt

    # 語法頁籤排版
    div_elt <= DIV_Tab("AHK語法", id="ahk_script_div_page_tag",
                       Class="tag_active", correspond_div_page_id="ahk_srcipt_output")
    div_elt <= DIV_Tab("關聯函式", id="function_div_page_tag",
                       correspond_div_page_id="ahk_function_srcipt_output")
    div_elt <= DIV_Tab("所有函式", id="all_function_div_page_tag",
                       correspond_div_page_id="all_function_srcipt_output")
    return div_elt


# 設定啟用和非啟用標籤顏色
AddStyle("""
    div#all_function_div_page_tag{
        float: right !important;
    }
    div.div_ahk_srcipt{
        background-color:"""+ACTIVE_SCRIPT_TAG_COLOR+""";
        width:100%;
    }
    div.ahk_script_tag{
        padding:10px 5px;
        white-space:nowrap;
        background-color:"""+ACTIVE_SCRIPT_TAG_COLOR+""";
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        font-family: 微軟正黑體;
        font-weight: bold;
        text-shadow: #fff 1px 1px 1px;
    }
    div.tag_active{
        background-color:"""+ACTIVE_SCRIPT_TAG_COLOR+""";
    }
    div.tag_unactive{
        background-color:"""+UNACTIVE_SCRIPT_TAG_COLOR+""";
    }
""")


# 進行排版
div_main = DIV(Class="main")
doc['div_subMainPage'] <= div_main

# 主區塊樣式
AddStyle("""
    div.main{
        width:100%;
        max-width:600px;
    }
""")


div_setting_hotkey = DIV(Class="page_border")
div_setting_hotkey <= Div_hotkey_setting()
div_main <= div_setting_hotkey

div_setting_function = DIV(Class="page_border")
div_setting_function <= DIV_function()+BR()
div_main <= div_setting_function

# 深藍區塊樣式
AddStyle("""
    div.block_header{
        background-color: #344ece;
        color:#fff;
        border-radius:10px 10px 0 0;
        padding: 8px;
        font-family: 微軟正黑體;
        font-weight: bold;
    }
""")

# 淺藍區塊樣式
AddStyle("""
    div.page_border{
        background-color: #9cedf1;
    	padding: 20px 20px 20px 20px;
        margin: 0 0 10px 0px;
        border-radius: 0 0 10px 10px;
    }
""")

# 定義複製AHK語法動作


def doCopy(ev):
    string = doc["ahk_srcipt_output"].text
    ahk_function_srcipt_output_text = doc["ahk_function_srcipt_output"].text
    if (ahk_function_srcipt_output_text != "(無)") and (doc['dont_copy_function'].checked):
        string += "\n\n"
        string += doc["ahk_function_srcipt_output"].text
    CopyTextToClipborad(string)
    alert("複製語法成功")

# 定義複製所有函式動作


def doCopyAllFunction(ev):
    CopyTextToClipborad(
        doc['all_function_srcipt_output'].select('pre')[0].text)


# 設置子頁面標頭DIV元素
div_title_elt = DIV()
# 設置版本標題
h1_title_elt = H1(f"AutoHotKey 自動化工具語法產生器 v{VERSION}", style={
                  "color": "#3939dc", "font-size": "18px", "font-weight": "600", 'float': 'left'})
# 設置FB DIV元素
div_fb_elt = DIV(id='div_fb', style={'float': 'right'})
div_fb_elt.innerHTML = r'<div id="fb-root" style="float:right"></div><div class="fb-like" data-href"https://papple23g-ahkcompiler.herokuapp.com/ahktool" data-layout="button_count" data-action="like" data-size="small" data-show-faces="false" data-share="true"></div>'  # style="float:right"
#
div_title_elt <= h1_title_elt
div_title_elt <= div_fb_elt+DIV(style={'clear': 'both'})


# 排版
div_main <= div_title_elt
# 置入設定組合鍵區塊
div_main <= DIV("設定組合鍵", Class="block_header")
div_main <= div_setting_hotkey
# 隱藏前綴設定DIV區塊
doc['div_elt_prefixSymbol_setting'].style.display = "none"
# 置入設定功能區塊
div_main <= DIV("設定功能", Class="block_header")
div_main <= div_setting_function
# 置入AHK程式碼區塊
div_main <= DIV_SciptTabs()
div_main <= DIV(style={"clear": "both"})
div_main <= DIV(DIV_ahkScriptBlock())
div_main <= DIV(
    BUTTON("複製語法", id="copy_button").bind("click", doCopy)
    + A_INPUTCheckbox("同時複製關聯函式", checked=True, id="dont_copy_function"),
    style={"float": "left"},
)
AddStyle("""
    #dont_copy_function{
        margin-left:10px;
    }
    #copy_button{
        height: 30px;
        border-radius: 6px;
        text-align: center;
        font-family: 微軟正黑體;
        font-size: 15px;
        font-weight: bold;
        margin-top: 10px;
        text-shadow: #fff 1px 1px 1px;
        outline: none;
    }
    .updated{
        color:blue;
    }
    .hidden{
        display:none;
    }
""")

# 設置使用說明iframe
iframe_elt = IFRAME(src="https://hackmd.io/@papple12g/rJvq8d2uh")
div_iframe_elt = DIV(iframe_elt)
doc['div_subMainPage'] <= div_iframe_elt
AddStyle('''
    div.main {
        width: 69% !important;
        float: left;
        margin-right: 150px;
        margin-bottom: 150px;
    }

    iframe{
        float: left;
        border: none;
        width: 460px;
        height: 1000px;
    }

    @media only screen and (max-width: 911px) {
        div.main {
            width: 90% !important;
        }
        iframe{
            width: 90%;
        }
    }
''')

# 遮蔽文字輸入欄:僅在標題含有該文字的視窗下執行
doc['ifWinTitle_InputElt'].disabled = True

# 刷新語法
render_ahk_script()  # 載入時刷新語法

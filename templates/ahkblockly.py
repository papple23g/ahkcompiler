#{% verbatim %}


#全域變數
Blockly=window.Blockly
workspace=window.workspace

#縮排
TAB_SPACE="    "


#定義函式:將xml格式化
def FormatXML(xml_str):
    xml_str=FormatHTML(xml_str)
    xml_str_line_list=xml_str.split('\n')
    xml_str_line_list=[xml_str_line for xml_str_line in xml_str_line_list if xml_str_line.strip()!=""]
    return "\n".join(xml_str_line_list)

#定義動作:尋找該層下的選擇器
def FindCurrent(elt,css_selector,get_one=True):
    com_elt_list=[elt_child for elt_child in elt.select(css_selector) if elt_child.parent==elt]
    if get_one:
        if com_elt_list:
            return com_elt_list[0]
        else:
            return None
    else:
        return com_elt_list

#設置解析xml用的隱藏div容器
div_xml_elt=DIV(id="div_xml",style={'display':'none'})
doc<=div_xml_elt

#定義動作:轉換xml為block
def XmlToBlockly(ev):
    #若xml的更改事件不是起源於blockly，就繼續執行
    if not hasattr(ev,"changeStartFromBlockly"):
        #print('xml>block')
        #獲取textarea_xml元素中的xml_str
        textarea_elt=doc['textarea_xml']
        xml_str=textarea_elt.value
        #製作臨時div容器以生成xml元素
        div_xml_elt=doc["div_xml"]
        div_xml_elt.innerHTML=xml_str
        xml_elt=div_xml_elt.select_one('xml')
        #若xml元素產生成功，就將xml元素嵌入至blockly區塊顯示
        if xml_elt:
            Blockly.Xml.clearWorkspaceAndLoadFromXml(xml_elt,workspace)
        #輸出格式化xml到
        xml_format_str=FormatXML(textarea_elt.value)
        textarea_elt.value=xml_format_str
        
#定義動作:顯示blocks的xml (必須等待Block載入完成)
def BlocklyToXml(ev):
    #啟用複製和下載AHK檔案按鈕
    for btn_elt in doc['div_copy_ahkfile_btns_area'].select('button'):
        btn_elt.disabled=False
    #print('block>xml')
    #自blockly獲取xml_str
    xml_blockly_elt=Blockly.Xml.workspaceToDom(workspace)
    doc['textarea_xml'].value=FormatXML(xml_blockly_elt.outerHTML)
    #製作input事件，觸發XmlToAHK，並附加起源資訊到事件元素中
    input_ev = window.Event.new("input")
    input_ev.changeStartFromBlockly=True
    doc['textarea_xml'].dispatchEvent(input_ev)

#定義動作:轉譯xml為AHK語法
def XmlToAHK(ev):
    ##註冊物件型Block元素列表 (不能被獨立轉譯)
    OBJ_BLOCK_LIST=[
        'function_key',
        'special_key',
        'normal_key',
        'filepath',
        'text',
        'webpage',
        'built_in_program',
        'built_in_dirpath',
        'built_in_webpage',
        'path_combined',
        'built_in_time',
        'math_arithmetic',
        'math_number',
        'variables_get',
        'logic_boolean',
        'logic_compare',
        'logic_operation',
        'logic_null',
        'logic_negate',
        'in_str',
        'right_click_menu', #不讓右鍵清單獨立執行，否則會無限循環跳出清單
    ]

    if ev.type in ["input","click"]:
        #print('xml>ahk')
        # print('XmlToAHK',"ev.type:",ev.type)
        #至textarea_xml元素獲取xml
        textarea_xml_elt=ev.currentTarget
        xml_str=textarea_xml_elt.value
        #獲取要輸出到指定的textarea元素
        textarea_ahk_elt=doc['textarea_ahk']

        #生成AHK程式碼
        ahk_code=""
        #建立暫時的div容器用來解析xml
        div_parseXml_elt=DIV()
        div_parseXml_elt.innerHTML=xml_str
        block_elt_list=div_parseXml_elt.select('xml>block')
        for block_elt in block_elt_list:
            #不要轉譯落單的field block
            if block_elt.attrs['type'] not in OBJ_BLOCK_LIST:
                ahk_code+=AHK_block(block_elt)+'\n'

        textarea_ahk_elt.innerHTML=ahk_code

        #移除暫時的div容器
        del div_parseXml_elt


#定義函式:抽出元素的註解
def Comment(elt,get_all_comment=False):
    com_str=""
    commit_elt_list=[]
    #判斷輸入的元素是否存在
    if elt:
        if get_all_comment:
            commit_elt_list=elt.select('comment')
        else:
            #搜尋該層下的comment
            commit_elt=FindCurrent(elt,'comment')
            #判斷該元素是否有comment
            if commit_elt:
                commit_elt_list.append(commit_elt)
        for commit_elt in commit_elt_list:
            commit_str=commit_elt.text
            #處理多行註解
            commit_str=commit_str.replace('\n','\n;')
            com_str+=f";{commit_str}\n"
            commit_elt.remove()
    
    return com_str

#定義函式:解析value元素為AHK語法
def AHK_value(value_elt,get_all_comment=False):
    if value_elt:
        block_underValue_elt=value_elt.select_one('block')
        return AHK_block(block_underValue_elt,get_all_comment=get_all_comment,separate_comment=True)
    else:
        return ("","")

#定義函式:解析statement元素為AHK語法
def AHK_statement(statement_elt,for_hotkey=False,Indentation=True):
    com_str=""
    if statement_elt:
        block_underStatement_elt=FindCurrent(statement_elt,'block')
        if block_underStatement_elt:
            statement_str=AHK_block(block_underStatement_elt)
            if for_hotkey:
                if statement_str.count('\n')>1 :
                    com_str+=f'\n{statement_str}Return\n'
                else:
                    com_str+=f"{statement_str}"
            else:
                #處理執行式縮排
                statement_str=TAB_SPACE*Indentation+statement_str.replace("\n","\n"+TAB_SPACE*Indentation)
                #去除執行式中空白的文字行
                statement_str='\n'.join([statement_str for statement_str in statement_str.split('\n') if statement_str.replace(';','').strip()!=""])+'\n'
                com_str+=statement_str
    return com_str


#定義函式:解析block元素為AHK語法
def AHK_block(block_elt,get_all_comment=False,separate_comment=False):
    com_str=""
    comment_str=""

    #判斷是否要轉譯該Block
    block_is_disabled_bool=True
    if block_elt:
        if block_elt.attrs.get("disabled",None):
            if block_elt.attrs["disabled"]=="true":
                block_is_disabled_bool=True
            else:
                block_is_disabled_bool=False        
        else:
            block_is_disabled_bool=False

    #若需要轉譯
    if not block_is_disabled_bool:
        comment_str+=Comment(block_elt,get_all_comment=get_all_comment)

        #region 按鍵Blockly

        if block_elt.attrs['type']=="hotkey_execute":
            hotkey_str=""
            statement_str=""

            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            if value_elt:
                #獲取功能鍵
                block_functionKey_elt_list=value_elt.select('block[type="function_key"]')
                for block_functionKey_elt in block_functionKey_elt_list:
                    functionKey_str,functionKey_comment=AHK_block(block_functionKey_elt,separate_comment=True)
                    hotkey_str+=functionKey_str
                    com_str+=functionKey_comment
                #獲取一般鍵
                block_normalKey_elt_list=value_elt.select('block[type="normal_key"]')
                block_normalKey_elt_list.extend(value_elt.select('block[type="special_key"]'))
                for block_normalKey_elt in block_normalKey_elt_list:
                    normalKey_str,normalKey_comment=AHK_block(block_normalKey_elt,separate_comment=True)
                    hotkey_str+=normalKey_str
                    com_str+=normalKey_comment
                #獲取執行元素
                statement_elt=FindCurrent(block_elt,'statement[name="DO"]')
                if statement_elt:
                    statement_str=AHK_statement(statement_elt,for_hotkey=True)
                    
            com_str+=hotkey_str+f"::{statement_str}\n"
                
        elif block_elt.attrs['type']=="function_key":
            field_elt=FindCurrent(block_elt,'field')
            function_key_name=field_elt.text
            function_key_dict={
                'Ctrl':'^',
                'Shift':'+',
                'Alt':'!',
                'Win':'#',
                'R':'>',
                'L':'<',
            }
            for k,v in function_key_dict.items():
                function_key_name=function_key_name.replace(k,v)
            com_str+=function_key_name

        elif block_elt.attrs['type'] in ["normal_key","special_key"]:
            field_elt=FindCurrent(block_elt,'field')
            function_key_name=field_elt.text
            com_str+=function_key_name

        elif block_elt.attrs['type']=="return":
            com_str+='Return'
        
        #endregion 按鍵Blockly

        #region 熱字串Blockly
        elif block_elt.attrs['type'] in ["hotstring","hotstring_advanced"]:
            #獲取縮寫元素
            value_abb_elt=FindCurrent(block_elt,'value[name="ABB"]')
            value_abb_str,value_abb_comment=AHK_value(value_abb_elt)
            value_abb_str=value_abb_str[1:-1] #去除冒號
            com_str+=value_abb_comment
            #獲取展開文字元素
            value_text_elt=FindCurrent(block_elt,'value[name="TEXT"]')
            value_text_str,value_text_comment=AHK_value(value_text_elt)
            #去除冒號(只針對文字進行去除，不針對變量或函式)
            if value_text_str[0]==value_text_str[-1]=='"':
                value_text_str=value_text_str[1:-1] 
            com_str+=value_text_comment
            #獲取熱字串設定元素
            hotstring_setting_str=""
            expand_raw_text_bool=False
            statement_setting_elt=FindCurrent(block_elt,'statement[name="SETTING"]')
            if statement_setting_elt:
                hotstringSetting_dict={
                    "hotstringSetting_autoExpaned":"*",
                    "hotstringSetting_dontFireEndKey":"o",
                    "hotstringSetting_caseSensitive":"c",
                    "hotstringSetting_expanedInWrods":"?",
                }
                block_hotstringSetting_elt_list=statement_setting_elt.select('block')
                for block_hotstringSetting_elt in block_hotstringSetting_elt_list:
                    if block_hotstringSetting_elt.attrs['type']!="hotstringSetting_rawText":
                        hotstring_setting_symbol=hotstringSetting_dict[block_hotstringSetting_elt.attrs['type']]
                        hotstring_setting_str+=hotstring_setting_symbol
                    else:
                        expand_raw_text_bool=True
            #若要展開的文字元素不是文字(例如變數或函式返回值)，則換至下一行使用SendInput TEXT
            if value_text_elt and FindCurrent(value_text_elt,'block') and FindCurrent(value_text_elt,'block').attrs['type']!="text":
                com_str+=f':{hotstring_setting_str}:{value_abb_str}::\nSendInput % "{{TEXT}}" . {value_text_str}\nReturn\n'
            else:
                com_str+=f':{hotstring_setting_str}:{value_abb_str}::{f"{{TEXT}}"*expand_raw_text_bool}{value_text_str}\n'
        
        elif block_elt.attrs['type']=="hotstring_do":
            #獲取縮寫元素
            value_abb_elt=FindCurrent(block_elt,'value[name="ABB"]')
            value_abb_str,value_abb_comment=AHK_value(value_abb_elt)
            value_abb_str=value_abb_str[1:-1] #去除冒號
            com_str+=value_abb_comment
            #獲取執行內容元素
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt,for_hotkey=True)
            #獲取熱字串設定元素
            hotstring_setting_str=""
            statement_setting_elt=FindCurrent(block_elt,'statement[name="SETTING"]')
            if statement_setting_elt:
                #獲取熱字串設定元素中的註解
                comment_setting_elt_list=statement_setting_elt.select('comment')
                for comment_setting_elt in comment_setting_elt_list:
                    com_str+=Comment(comment_setting_elt.parent)
                hotstringSetting_dict={
                    "hotstringSetting_autoExpaned":"*",
                    "hotstringSetting_dontFireEndKey":"o",
                    "hotstringSetting_caseSensitive":"c",
                    "hotstringSetting_expanedInWrods":"?",
                }
                block_hotstringSetting_elt_list=statement_setting_elt.select('block')
                for block_hotstringSetting_elt in block_hotstringSetting_elt_list:
                    if block_hotstringSetting_elt.attrs['type']!="hotstringSetting_rawText":
                        hotstring_setting_symbol=hotstringSetting_dict[block_hotstringSetting_elt.attrs['type']]
                        hotstring_setting_str+=hotstring_setting_symbol

            com_str+=f':{hotstring_setting_str}:{value_abb_str}::{statement_do_str}\n'

        #endregion 熱字串Blockly
        
        #region 動作Blockly
        
        elif block_elt.attrs['type']=="open":
            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)

            com_str+=value_comment
            com_str+=f'Run % {value_str}\n'

        elif block_elt.attrs['type']=="file_recycle_empty":
            com_str+='FileRecycleEmpty\n'

        elif block_elt.attrs['type']=="msgbox":
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)

            com_str+=value_comment

            com_str+=f"Msgbox % {value_str}\n"

        elif block_elt.attrs['type']=="send_text":
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)

            com_str+=value_comment
            com_str+=f'SendInput % "{{TEXT}}" . {value_str}\n'

        elif block_elt.attrs['type']=="set_clipboard":
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)

            com_str+=value_comment
            com_str+=f'Clipboard := {value_str}\n'

        elif block_elt.attrs['type']=="close_process":
            field_elt=FindCurrent(block_elt,'field')
            com_str+=f'Process, Close, {field_elt.text}\n'

        elif block_elt.attrs['type']=="sleep":
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            com_str+=value_comment
            com_str+=f'Sleep % {value_str}\n'


        elif block_elt.attrs['type']=="shutdown":
            #獲取動作
            field_action_elt=FindCurrent(block_elt,'field[name="action"]')
            field_action_str=field_action_elt.text
            #獲取是否強制執行
            field_force_elt=FindCurrent(block_elt,'field[name="force"]')
            field_force_str=field_force_elt.text            
            #若為Shutdown語法 (登出/關機/重新啟動)
            if field_action_str in ["logout","shutdown","restart"]:
                action_int=0 if field_action_str=="logout" else 1 if field_action_str=="shutdown" else 2
                force_int=4 if field_force_str=="TRUE" else 0
                com_str+=f"Shutdown, {action_int+force_int}\n"
            #若為DllCall語法 (睡眠/休眠)
            elif field_action_str in ["sleep","deepsleep"]:
                var_int=0 if field_action_str=="sleep" else 1
                com_str+=f'DllCall("PowerProf\\SetSuspendState", "int", {var_int}, "int", 0, "int", 0,)\n'
            else:
                com_str+='Run rundll32.exe user32.dll`,LockWorkStation\n'




        #endregion 動作Blockly

        #region 物件Blockly

        #剪貼簿內容
        elif block_elt.attrs['type']=="clipboard":
            com_str+='Clipboard'

        #目錄、檔案、網頁
        elif block_elt.attrs['type'] in ["filepath","dirpath","webpage"]:
            filed_elt=FindCurrent(block_elt,'field[name="NAME"]')
            filed_str=filed_elt.text
            #若為網頁，則需要替換特殊字元
            if block_elt.attrs['type']=="webpage":
                filed_str=filed_str.replace("%","`%").replace(",","`,")
            com_str+=f'"{filed_str}"'
        
        #文字
        elif block_elt.attrs['type']=="text":
            field_elt=FindCurrent(block_elt,'field')
            field_elt_str=field_elt.text.replace('`','``')
            if field_elt:
                com_str+=f'"{field_elt_str}"'

        #合併文字
        elif block_elt.attrs['type']=="text_join":
            mutation_elt=FindCurrent(block_elt,"mutation")
            mutation_items_int=int(mutation_elt.attrs['items'])
            value_str_list=[]
            for i_item in range(mutation_items_int):
                value_elt=FindCurrent(block_elt,f'value[name="ADD{i_item}"]')
                value_str,value_comment=AHK_value(value_elt)
                value_str_list.append(value_str)
            
            value_str_list_str=" . ".join(value_str_list)
            com_str+=value_str_list_str


        #內建程式變量
        elif block_elt.attrs['type']=="built_in_program":
            field_elt=FindCurrent(block_elt,'field')
            if field_elt:
                built_in_program_dict={
                    "notepad":'"Notepad.exe"',
                    "mspaint":' windir . "\system32\mspaint.exe"',
                    "calc":' windir . "\system32\calc.exe"',
                    "SnippingTool":' windir . "\system32\SnippingTool.exe"',
                    "cmd":' windir . "\system32\cmd.exe"',
                    "ahkfile":'A_ScriptFullPath',
                    "ahkexe":'A_AhkPath',
                }
                field_str=built_in_program_dict[field_elt.text]
                com_str+=f'{field_str}'

        #內建路徑變量
        elif block_elt.attrs['type']=="built_in_dirpath":
            field_elt=FindCurrent(block_elt,'field')
            if field_elt:
                built_in_program_dict={
                    "desktop":'A_Desktop',
                    "mydocuments":'A_MyDocuments',
                    "startup":'A_Startup',
                    "temp":'A_Temp',
                    "windows":'A_WinDir',
                    "ahkfilepath":'A_ScriptDir',
                }
                field_str=built_in_program_dict[field_elt.text]
                com_str+=f'{field_str}'

        elif block_elt.attrs['type']=="built_in_webpage":
            field_elt=FindCurrent(block_elt,'field')
            if field_elt:
                built_in_webpage_dict={
                    "google":'https://www.google.com',
                    "youtube":'https://www.youtube.com',
                    "facebook":'https://www.facebook.com',
                    "wikipedia":'https://zh.wikipedia.org',
                    "pchome":"https://www.pchome.com.tw",
                    "yahoo":"https://yahoo.com",
                    "googlemap":"https://www.google.com.tw/maps",
                    "ahk":"https://www.autohotkey.com",
                    "ahkblockly":"https://sites.google.com/view/ahktool/ahkblockly",
                }
                field_str=built_in_webpage_dict[field_elt.text]
                com_str+=f'"{field_str}"'

        #路徑合併
        elif block_elt.attrs['type']=="path_combined":
            value_mainPath_elt=FindCurrent(block_elt,'value[name="main_path"]')
            value_mainPath_str,value_mainPath_comment=AHK_value(value_mainPath_elt)
            com_str+=value_mainPath_comment

            value_subPath_elt=FindCurrent(block_elt,'value[name="sub_path"]')
            value_subPath_str,value_subPath_comment=AHK_value(value_subPath_elt)
            com_str+=value_subPath_comment
            
            com_str+=f'{value_mainPath_str} . "\\" . {value_subPath_str}'

        #數字
        elif block_elt.attrs['type']=="math_number":
            field_elt=FindCurrent(block_elt,'field[name="NUM"]')
            com_str+=field_elt.text.strip()

        #數學算式
        elif block_elt.attrs['type']=="math_arithmetic":
            field_op_elt=FindCurrent(block_elt,'field[name="OP"]')
            field_op_str_dict={
                'ADD':'+',
                'MINUS':'-',
                'MULTIPLY':'*',
                'DIVIDE':'/',
                'POWER':'**',
            }
            field_op_str=field_op_str_dict[field_op_elt.text]

            value_a_elt=FindCurrent(block_elt,'value[name="A"]')
            value_a_str,_=AHK_value(value_a_elt)
            
            value_b_elt=FindCurrent(block_elt,'value[name="B"]')
            value_b_str,_=AHK_value(value_b_elt)

            com_str+=f'({value_a_str}{field_op_str}{value_b_str})'



        #日期時間
        elif block_elt.attrs['type']=="built_in_time":
            field_elt=FindCurrent(block_elt,'field[name="NAME"]')
            built_in_time_dict={
                "year":"A_YYYY",
                "month":"A_MM",
                "day":"A_DD",
                "wday":"(A_WDay=1 ? 7 : A_WDay-1)",
                "hour":"A_Hour",
                "min":"A_Min",
                "sec":"A_Sec",
            }
            com_str+=built_in_time_dict[field_elt.text]

        elif block_elt.attrs['type']=="built_in_wday_zh":
            com_str+='Array("日","一","二","三","四","五","六")[A_WDay]'


        #endregion 物件Blockly
        
        #region 模擬鍵盤Blockly
        elif block_elt.attrs['type']=="send_key":
            hotkey_str=""

            #移除next元素(使用虛擬DIV容器)
            block_sendKey_elt=DIV()
            block_sendKey_elt.innerHTML=block_elt.innerHTML
            next_sendKey_elt=block_sendKey_elt.select_one('next')
            if next_sendKey_elt:
                next_sendKey_elt.remove()
            #獲取功能鍵
            block_functionKey_elt_list=block_sendKey_elt.select('block[type="function_key"]')
            for block_functionKey_elt in block_functionKey_elt_list:
                functionKey_str,functionKey_comment=AHK_block(block_functionKey_elt,separate_comment=True)
                hotkey_str+=functionKey_str
                com_str+=functionKey_comment
            #獲取一般鍵(將英文字母按鍵名稱降為小寫)
            block_normalKey_elt_list=block_sendKey_elt.select('block[type="normal_key"]')
            block_normalKey_elt_list.extend(block_sendKey_elt.select('block[type="special_key"]'))
            for block_normalKey_elt in block_normalKey_elt_list:
                normalKey_str,normalKey_comment=AHK_block(block_normalKey_elt,separate_comment=True)
                hotkey_str+=(normalKey_str.lower() if block_normalKey_elt.attrs['type']=="normal_key" else f"{{{normalKey_str}}}")
                com_str+=normalKey_comment
            
            com_str+=f'Send, {hotkey_str}\n'

        elif block_elt.attrs['type']=="send_keys":
            hotkey_str=""

            #移除next元素(使用虛擬DIV容器)
            block_sendKey_elt=DIV()
            block_sendKey_elt.innerHTML=block_elt.innerHTML
            next_sendKey_elt=block_sendKey_elt.select_one('next')
            if next_sendKey_elt:
                next_sendKey_elt.remove()
            #獲取一般連續鍵
            filed_elt=FindCurrent(block_elt,'field')
            
            com_str+=f'Send, {filed_elt.text}\n'

        elif block_elt.attrs['type']=="send_key_times":
            #移除next元素(使用虛擬DIV容器)
            block_sendKey_elt=DIV()
            block_sendKey_elt.innerHTML=block_elt.innerHTML
            next_sendKey_elt=block_sendKey_elt.select_one('next')
            if next_sendKey_elt:
                next_sendKey_elt.remove()
            #獲取功能鍵
            functionKey_all_str=""
            block_functionKey_elt_list=block_sendKey_elt.select('block[type="function_key"]')
            for block_functionKey_elt in block_functionKey_elt_list:
                functionKey_str,functionKey_comment=AHK_block(block_functionKey_elt,separate_comment=True)
                functionKey_all_str+=functionKey_str
                com_str+=functionKey_comment
            #獲取一般鍵(將英文字母按鍵名稱降為小寫)，此處應只有獲取一個元素
            block_normalKey_elt_list=block_sendKey_elt.select('block[type="normal_key"]')
            block_normalKey_elt_list.extend(block_sendKey_elt.select('block[type="special_key"]'))
            for block_normalKey_elt in block_normalKey_elt_list:
                normalKey_str,normalKey_comment=AHK_block(block_normalKey_elt,separate_comment=True)
                if block_normalKey_elt.attrs['type']=="normal_key":
                    normalKey_str=normalKey_str.lower()
                com_str+=normalKey_comment

            #獲取次數元素
            value_times_elt=FindCurrent(block_elt,'value[name="TIMES"]')
            value_times_str,value_times_comment=AHK_value(value_times_elt)
            com_str+=value_times_comment
            
            com_str+=f'Send, {functionKey_all_str}{{{normalKey_str} {value_times_str}}}\n'

        #等待功能鍵釋放
        elif block_elt.attrs['type']=="key_wait":
            #獲取功能鍵
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt)
            com_str+=value_comment
            #對於等待Win按鍵釋放，需要兩行程式碼寫完
            if value_str=="Win":
                com_str+=f'KeyWait, LWin\nKeyWait, RWin\n'
            else:
                com_str+=f'KeyWait, {value_str}\n'

        #按著功能鍵
        elif block_elt.attrs['type']=="key_pressing":
            #獲取功能鍵
            value_elt=FindCurrent(block_elt,'value')
            value_str,value_comment=AHK_value(value_elt)
            com_str+=value_comment
            #獲取執行元素
            statement_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_str=AHK_statement(statement_elt,Indentation=False) #不要將執行式縮排
            #輸出程式碼
            com_str=f'Send {{{value_str} Down}}\n{statement_str}Send {{{value_str} Up}}\n'




        #endregion 模擬鍵盤Blockly

        #region 模擬滑鼠Blockly

        #coord_mode
        elif block_elt.attrs['type']=="coord_mode":
            field_name_elt=FindCurrent(block_elt,'field[name="NAME"]')
            coord_mode_str=field_name_elt.text
            coord_mode_str=coord_mode_str[0].upper()+coord_mode_str[1:]
            com_str+=f'CoordMode, Mouse , {coord_mode_str}\n'

        #點擊(x,y)
        elif block_elt.attrs['type']=="click_x_y":
            value_x_elt=FindCurrent(block_elt,f'value[name="X"]')
            value_x_str,value_x_comment=AHK_value(value_x_elt)
            com_str+=value_x_comment
            x_is_var_bool=True if (value_x_elt and FindCurrent(value_x_elt,'block').attrs['type']=="variables_get") else False

            value_y_elt=FindCurrent(block_elt,f'value[name="Y"]')
            value_y_str,value_y_comment=AHK_value(value_y_elt)
            com_str+=value_y_comment
            y_is_var_bool=True if (value_y_elt and FindCurrent(value_y_elt,'block').attrs['type']=="variables_get") else False

            value_times_elt=FindCurrent(block_elt,f'value[name="TIMES"]')
            value_times_str,value_times_comment=AHK_value(value_times_elt)
            com_str+=value_times_comment
            times_is_var_bool=True if (value_times_elt and FindCurrent(value_times_elt,'block').attrs['type']=="variables_get") else False
           
            com_str+=f"Click {'%'*x_is_var_bool}{value_x_str}{'%'*x_is_var_bool}, {'%'*y_is_var_bool}{value_y_str}{'%'*y_is_var_bool}, {'%'*times_is_var_bool}{value_times_str}{'%'*times_is_var_bool}\n"
        
        elif block_elt.attrs['type']=="mouse_get_pos":
            value_posX_elt=FindCurrent(block_elt,f'value[name="posX"]')
            value_posX_str,value_posX_comment=AHK_value(value_posX_elt)
            com_str+=value_posX_comment

            value_posY_elt=FindCurrent(block_elt,f'value[name="posY"]')
            value_posY_str,value_posY_comment=AHK_value(value_posY_elt)
            com_str+=value_posY_comment

            com_str+=f'MouseGetPos, {value_posX_str}, {value_posY_str}\n'
        
        
        #endregion 模擬滑鼠Blockly

        #region 函式Blockly

        elif block_elt.attrs['type']=="procedures_defnoreturn":
            #獲取函式名稱
            field_name_elt=FindCurrent(block_elt,'field[name="NAME"]')
            function_name_str=field_name_elt.text
            #獲取變數列表
            arg_str_list=[]
            mutation_elt=FindCurrent(block_elt,'mutation')
            if mutation_elt:
                for arg_elt in mutation_elt.select('arg'):
                    arg_str_list.append(arg_elt.attrs['name'])
            arg_str=", ".join(arg_str_list)
            #獲取執行內容
            statement_elt=FindCurrent(block_elt,'statement[name="STACK"]')
            statement_str=AHK_statement(statement_elt)
            #輸出程式碼
            com_str+=f'{function_name_str}({arg_str}){{\n{statement_str}}}\n'

        elif block_elt.attrs['type']=="procedures_defreturn":
            #獲取函式名稱
            field_name_elt=FindCurrent(block_elt,'field[name="NAME"]')
            function_name_str=field_name_elt.text
            #獲取變數列表
            arg_str_list=[]
            mutation_elt=FindCurrent(block_elt,'mutation')
            if mutation_elt:
                for arg_elt in mutation_elt.select('arg'):
                    arg_str_list.append(arg_elt.attrs['name'])
            arg_str=", ".join(arg_str_list)
            #獲取執行內容
            statement_elt=FindCurrent(block_elt,'statement[name="STACK"]')
            statement_str=AHK_statement(statement_elt)
            #獲取返回內容
            value_return_elt=FindCurrent(block_elt,'value[name="RETURN"]')
            value_return_str,value_return_comment=AHK_value(value_return_elt)
            value_return_str=TAB_SPACE + f'Return {value_return_str}\n'
            com_str+=value_return_comment
            #輸出程式碼
            com_str+=f'{function_name_str}({arg_str}){{\n{statement_str}{value_return_str}}}\n'
        

        elif block_elt.attrs['type']=="procedures_callnoreturn":
            #獲取函式名稱
            mutation_elt=block_elt.select_one('mutation')
            function_name_str=mutation_elt.attrs['name']
            #獲取變數列表
            arg_elt_list=mutation_elt.select('arg')
            arg_str_list=[]
            for i_arg in range(len(arg_elt_list)):
                #獲取參數數值
                value_arg_elt=FindCurrent(block_elt,f'value[name="ARG{i_arg}"]')
                value_arg_str,_=AHK_value(value_arg_elt)
                value_arg_str=value_arg_str if value_arg_str else ""
                #獲取參數名稱
                arg_elt=arg_elt_list[i_arg]
                arg_name_str=arg_elt.attrs['name']
                #生成「參數:=數值」表達式
                arg_str=f'{arg_name_str}:={value_arg_str}'
                arg_str_list.append(arg_str)
            arg_str_list_str=", ".join(arg_str_list)
            com_str+=f'{function_name_str}({arg_str_list_str})\n' #沒有return是執行式，所以要換行

        elif block_elt.attrs['type']=="procedures_callreturn":
            #獲取函式名稱
            mutation_elt=block_elt.select_one('mutation')
            function_name_str=mutation_elt.attrs['name']
            #獲取變數列表
            arg_elt_list=mutation_elt.select('arg')
            arg_str_list=[]
            for i_arg in range(len(arg_elt_list)):
                #獲取參數數值
                value_arg_elt=FindCurrent(block_elt,f'value[name="ARG{i_arg}"]')
                value_arg_str,_=AHK_value(value_arg_elt)
                value_arg_str=value_arg_str if value_arg_str else ""
                #獲取參數名稱
                arg_elt=arg_elt_list[i_arg]
                arg_name_str=arg_elt.attrs['name']
                #生成「參數:=數值」表達式
                arg_str=f'{arg_name_str}:={value_arg_str}'
                arg_str_list.append(arg_str)
            arg_str_list_str=", ".join(arg_str_list)
            
            com_str+=f'{function_name_str}({arg_str_list_str})' #有return東西會向左賦值，所以不用換行


        #endregion 函式Blockly

        #region 變數Blockly
        elif block_elt.attrs['type']=="variables_get":
            #獲取變數名稱(取代空白為底線)
            var_name=block_elt.select_one('field').text
            var_name=var_name.replace(" ","_").replace("　","_")
            com_str+=var_name

        elif block_elt.attrs['type']=="variables_set":
            #獲取變數名稱(取代空白為底線)
            field_elt=FindCurrent(block_elt,'field[name="VAR"]')
            var_name=field_elt.text.replace(" ","_").replace("　","_")
            #獲取賦值內容
            value_elt=FindCurrent(block_elt,'value[name="VALUE"]')
            value_str,value_comment=AHK_value(value_elt)
            com_str+=value_comment
            #輸出程式
            com_str+=f'{var_name} := {value_str}\n'

        elif block_elt.attrs['type']=="math_change":
            field_elt=FindCurrent(block_elt,'field[name="VAR"]')
            var_name=field_elt.text.replace(" ","_").replace("　","_")
            value_str="0"
            #獲取賦值內容
            value_delta_elt=FindCurrent(block_elt,'value[name="DELTA"]')
            #若有放置數字blockly
            if FindCurrent(value_delta_elt,'block'):
                value_str,value_comment=AHK_value(value_delta_elt)
                com_str+=value_comment
            #若為預設影子blockly
            else:
                shadow_elt=FindCurrent(value_delta_elt,'shadow')
                value_str=FindCurrent(shadow_elt,'field').text
            
            #輸出程式
            com_str+=f'{var_name} += {value_str}\n'


        #endregion 變數Blockly

        #region 邏輯Blockly
        
        elif block_elt.attrs['type']=="controls_if":
            #獲取判斷布林值
            value_if0_elt=FindCurrent(block_elt,'value[name="IF0"]')
            value_if0_str,value_if0_comment=AHK_value(value_if0_elt,get_all_comment=True)
            com_str+=value_if0_comment
            #獲取執行式
            statement_do0_elt=FindCurrent(block_elt,'statement[name="DO0"]')
            statement_do0_str=AHK_statement(statement_do0_elt)
            com_str+=f"if {value_if0_str} {{\n{statement_do0_str}}}"

            mutation_elt=FindCurrent(block_elt,'mutation')
            #若是多層if層次block
            if mutation_elt:
                if mutation_elt.attrs.get('elseif'):
                    nb_elseif_int=int(mutation_elt.attrs.get('elseif'))
                    for i in range(1,nb_elseif_int+1):
                        #獲取判斷布林值
                        value_ifn_elt=FindCurrent(block_elt,f'value[name="IF{i}"]')
                        value_ifn_str,value_ifn_comment=AHK_value(value_ifn_elt,get_all_comment=True)
                        #取消註解的斷行，讓其出現在 }else if () { 同一行的後段
                        value_ifn_comment=value_ifn_comment.replace('\n','')
                        #獲取執行式
                        statement_don_elt=FindCurrent(block_elt,f'statement[name="DO{i}"]')
                        statement_don_str=AHK_statement(statement_don_elt)
                        
                        com_str+=f"else if {value_ifn_str} {{ {value_ifn_comment}\n{statement_don_str}}}"
                if mutation_elt.attrs.get('else'):
                    #獲取執行式
                    statement_doElse_elt=FindCurrent(block_elt,'statement[name="ELSE"]')
                    statement_doElse_str=AHK_statement(statement_doElse_elt)
                    com_str+=f"else {{\n{statement_doElse_str}}}"
            com_str+='\n'           

        #邏輯not
        elif block_elt.attrs['type']=="logic_negate":
            value_elt=FindCurrent(block_elt,'value[name="BOOL"]')
            value_str,value_comment=AHK_value(value_elt)
            com_str+=value_comment
            com_str+=f'not {value_str}'

        #邏輯null
        elif block_elt.attrs['type']=="logic_null":
            com_str+='""'    

        #邏輯真假
        elif block_elt.attrs['type']=="logic_boolean":
            field_op_elt=FindCurrent(block_elt,'field[name="BOOL"]')
            com_str+=field_op_elt.text

        #邏輯比較
        elif block_elt.attrs['type']=="logic_compare":
            #獲取操作類型
            field_op_elt=FindCurrent(block_elt,'field[name="OP"]')
            op_str_dict={
                'EQ':'=',
                'NEQ':'!=',
                'LT':'<',
                'LTE':'<=',
                'GT':'>',
                'GTE':'>=',
            }
            field_op_str=op_str_dict[field_op_elt.text]
            #獲取比較值A
            value_a_elt=FindCurrent(block_elt,'value[name="A"]')
            value_a_str,value_a_comment=AHK_value(value_a_elt)
            com_str+=value_a_comment
            #獲取比較值B
            value_b_elt=FindCurrent(block_elt,'value[name="B"]')
            value_b_str,value_b_comment=AHK_value(value_b_elt)
            com_str+=value_b_comment
            #輸出程式
            com_str+=f'({value_a_str} {field_op_str} {value_b_str})'

        #邏輯操作(AND OR)
        elif block_elt.attrs['type']=="logic_operation":
            #獲取操作類型
            field_op_elt=FindCurrent(block_elt,'field[name="OP"]')
            field_op_str=field_op_elt.text
            #獲取比較值A
            value_a_elt=FindCurrent(block_elt,'value[name="A"]')
            value_a_str,value_a_comment=AHK_value(value_a_elt)
            com_str+=value_a_comment
            #獲取比較值B
            value_b_elt=FindCurrent(block_elt,'value[name="B"]')
            value_b_str,value_b_comment=AHK_value(value_b_elt)
            com_str+=value_b_comment
            #輸出程式
            com_str+=f'({value_a_str} {field_op_str} {value_b_str})'

        #包含文字
        elif block_elt.attrs['type']=="in_str":
            #獲取主要文字
            value_text_elt=FindCurrent(block_elt,'value[name="text"]')
            value_text_str,value_text_comment=AHK_value(value_text_elt)
            com_str+=value_text_comment
            #獲取次要對比文字
            value_subtext_elt=FindCurrent(block_elt,'value[name="sub_text"]')
            value_subtext_str,value_subtext_comment=AHK_value(value_subtext_elt)
            com_str+=value_subtext_comment
            #獲取要使用的函式名稱
            field_elt=FindCurrent(block_elt,'field[name="NAME"]')
            func_str="not "*(field_elt.text=="not_contain")+"InStr"
            #輸出程式
            com_str+=f'{func_str}({value_text_str},{value_subtext_str})'

            




        #endregion 邏輯Blockly

        #region 右鍵清單

        elif block_elt.attrs['type']=="right_click_menu":
            menu_myMenu_add_str=""
            label_str=""
            #遍歷所有項目
            statement_elt=FindCurrent(block_elt,'statement')
            #設置項目計數器(防止重複Lable名稱)
            i_item=1
            block_item_elt_list=[]
            block_item_elt=FindCurrent(statement_elt,'block')
            if block_item_elt:
                block_item_elt_list.append(block_item_elt)
                while FindCurrent(block_item_elt,'next'):
                    next_elt=FindCurrent(block_item_elt,'next')
                    block_item_elt=FindCurrent(next_elt,'block')
                    block_item_elt_list.append(block_item_elt)
            
            for block_item_elt in block_item_elt_list:

                if block_item_elt.attrs['type']=="right_click_menu_item":
                    #獲取項目名稱
                    field_itemName_elt=FindCurrent(block_item_elt,'field[name="item_name"]')
                    item_name_raw_str=field_itemName_elt.text
                    item_name_str=item_name_raw_str.replace(" ","_").replace("　","_")
                    menu_myMenu_add_str+=f"Menu,MyMenu,Add,{item_name_raw_str},{item_name_str}_{i_item}\n"
                    #獲取執行式
                    statement_do_elt=FindCurrent(block_item_elt,'statement[name="DO"]')
                    statement_do_str=AHK_statement(statement_do_elt)
                    label_str+=f"{item_name_str}_{i_item}:\n{statement_do_str}return\n"
                    #增加項目計數
                    i_item+=1
                elif block_item_elt.attrs['type']=="right_click_menu_item_hr":
                    menu_myMenu_add_str+=f"Menu,MyMenu,Add,\n"



            #輸出程式碼
            com_str+='''Loop,1{
CoordMode, Menu, Screen
CoordMode, Mouse, Screen

'''+ menu_myMenu_add_str +'''
MouseGetPos,MX,MY
Menu,MyMenu,Show,% MX,% MY
Reload
WinKill,menu launcher -quits right after .ahk,WinText,ET
return

'''+ label_str +'''}\n'''



        #endregion 右鍵清單

        #region 音量控制

        elif block_elt.attrs['type']=="volume_adjust":
            #獲取同整動作
            field_action_elt=FindCurrent(block_elt,'field[name="action"]')
            field_action_str=field_action_elt.text
            add_or_sub_symbol_str='+' if field_action_str=="add" else '-' if field_action_str=="sub" else ""
            #獲取調整數值
            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            value_str=value_str if value_str else 0
            com_str+=value_comment
            #輸出程式碼
            com_str+=f"SoundSet {add_or_sub_symbol_str}{value_str}\n"

        elif block_elt.attrs['type']=="volume_mute":
            #輸出程式碼
            com_str+="SoundSet,+1, , mute\n"

            

        


        #endregion 音量控制

        #region 系統資訊Blockly
        elif block_elt.attrs['type']=="computer_name":
            com_str+="A_ComputerName"

        elif block_elt.attrs['type']=="user_name":
            com_str+="A_UserName"

        elif block_elt.attrs['type']=="win_get_active_title":
            #獲取變數名稱
            value_elt=FindCurrent(block_elt,'value[name="NAME"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            com_str+=value_comment

            com_str+=f'WinGetActiveTitle, {value_str}\n'

        #endregion 系統資訊Blockly

        #region 循環Blockly

        #Loop循環
        elif block_elt.attrs['type']=="controls_repeat_ext":
            #獲取重複次數
            value_elt=FindCurrent(block_elt,'value[name="TIMES"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            com_str+=value_comment
            #獲取執行式
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt)
            com_str+=f"Loop {value_str} {{\n{statement_do_str}}}"

        #while循環
        elif block_elt.attrs['type']=="controls_whileUntil":
            #獲取布林值
            value_elt=FindCurrent(block_elt,'value[name="BOOL"]')
            value_str,value_comment=AHK_value(value_elt,get_all_comment=True)
            value_str=value_str if value_str else "False"
            com_str+=value_comment
            #獲取迴圈方式
            field_elt=FindCurrent(block_elt,'field[name="MODE"]')
            while_str="while"+" not"*(field_elt.text!="WHILE")
            #獲取執行式
            statement_do_elt=FindCurrent(block_elt,'statement[name="DO"]')
            statement_do_str=AHK_statement(statement_do_elt)
            com_str+=f"{while_str} {value_str} {{\n{statement_do_str}}}"

        #break或continue
        elif block_elt.attrs['type']=="controls_flow_statements":
            field_elt=FindCurrent(block_elt,'field')
            com_str+=field_elt.text.lower()+'\n'

        #endregion 循環Blockly

        #region 自訂程式碼Blockly

        elif block_elt.attrs['type']=="ahk_code":
            field_elt=FindCurrent(block_elt,'field')
            com_str+=field_elt.text+'\n'

        elif block_elt.attrs['type']=="cmd":
            #獲取CMD程式碼
            field_code_elt=FindCurrent(block_elt,'field[name="code"]')
            cmd_code_str=field_code_elt.text
            #獲取使否執行後關閉
            field_doClose_elt=FindCurrent(block_elt,'field[name="do_close"]')
            arg_str='/c' if field_doClose_elt.text=="TRUE" else '/k'

            com_str+=f'Run %comspec% {arg_str} {cmd_code_str}\n'

        #endregion 自訂程式碼Blockly

        #處理下一個block
        next_elt=FindCurrent(block_elt,'next',get_one=True)
        if next_elt:
            block_next_elt=FindCurrent(next_elt,'block')
            com_str+=AHK_block(block_next_elt)

    if separate_comment:
        return  com_str,comment_str   
    else:
        return comment_str+com_str



#綁定事件:workspace更換時就轉譯blocks為xml
def ClearAhkCodeArea(ev):
    #清空AHK code
    doc['textarea_ahk'].innerHTML=""
    #禁用複製和下載AHK檔案按鈕
    for btn_elt in doc['div_copy_ahkfile_btns_area'].select('button'):
        btn_elt.disabled=True


workspace.addChangeListener(ClearAhkCodeArea)

#綁定事件:停用落單的blockly
#workspace.addChangeListener(Blockly.Events.disableOrphans);

#region 插入範例1
xml_ex_1='''<xml>
  <block type="procedures_defreturn" id="qlK:U]~IEWC+1@gAN:lK" x="24" y="23">
    <mutation statements="false"></mutation>
    <field name="NAME">現在時間</field>
    <comment pinned="false" h="44" w="325">請按右鍵＞創造函式積木，來使用此函式積木</comment>
    <value name="RETURN">
      <block type="text_join" id="8X0.OxgdRV2Q2QE8mMFT">
        <mutation items="11"></mutation>
        <value name="ADD0">
          <block type="built_in_time" id="3*b_Ao:WS1JMA~pdCo@1">
            <field name="NAME">year</field>
          </block>
        </value>
        <value name="ADD1">
          <block type="text" id="s)pS:L;BF`;kflQBLVNR">
            <field name="TEXT">/</field>
          </block>
        </value>
        <value name="ADD2">
          <block type="built_in_time" id="N)U2e8AB{xaJHW!c;h#/">
            <field name="NAME">month</field>
          </block>
        </value>
        <value name="ADD3">
          <block type="text" id="Hin^|y$w@)Bz-3fxYJo_">
            <field name="TEXT">/</field>
          </block>
        </value>
        <value name="ADD4">
          <block type="built_in_time" id="Tfi4BII%@Ap31W]Fg9%l">
            <field name="NAME">day</field>
          </block>
        </value>
        <value name="ADD5">
          <block type="text" id="r_0%Xpw_71L_L[Ao-8oo">
            <field name="TEXT">-</field>
          </block>
        </value>
        <value name="ADD6">
          <block type="built_in_time" id="G|$^aoRw?.-nvdlw)h!-">
            <field name="NAME">hour</field>
          </block>
        </value>
        <value name="ADD7">
          <block type="text" id="Z!nnU}TwQHz|QeNz_J=|">
            <field name="TEXT">:</field>
          </block>
        </value>
        <value name="ADD8">
          <block type="built_in_time" id="14gg/Elks,(H;_T}(=lO">
            <field name="NAME">min</field>
          </block>
        </value>
        <value name="ADD9">
          <block type="text" id="]h^=X9AaM^g5^w/CakfK">
            <field name="TEXT">:</field>
          </block>
        </value>
        <value name="ADD10">
          <block type="built_in_time" id="mpTd{yebnp:R/%H30rj3">
            <field name="NAME">sec</field>
          </block>
        </value>
      </block>
    </value>
  </block>
  <block type="procedures_defreturn" id="[ZFzaKc.WVOfgb*~E4X4" x="418" y="59">
    <mutation statements="false"></mutation>
    <field name="NAME">現在日期</field>
    <comment pinned="false" h="44" w="325">請按右鍵＞創造函式積木，來使用此函式積木</comment>
    <value name="RETURN">
      <block type="text_join" id=".wPxQ{%A/.TkGGUS:/l@">
        <mutation items="9"></mutation>
        <value name="ADD0">
          <block type="text" id="8edf;tX{wP:I5]xI5#J6">
            <field name="TEXT">中華民國</field>
          </block>
        </value>
        <value name="ADD1">
          <block type="math_arithmetic" id="krA].qgE(Jj?l-e5{xf=">
            <field name="OP">MINUS</field>
            <comment pinned="false" h="36" w="151">將西元年換算成民國年</comment>
            <value name="A">
              <block type="built_in_time" id="/S==O~?Y~e7=jb2C51fZ">
                <field name="NAME">year</field>
              </block>
            </value>
            <value name="B">
              <block type="math_number" id="7=F;I#5W!4l[Eb5E0+(k">
                <field name="NUM">1911</field>
              </block>
            </value>
          </block>
        </value>
        <value name="ADD2">
          <block type="text" id="`v|z$:CWB/sQ+^pdH{5%">
            <field name="TEXT">年</field>
          </block>
        </value>
        <value name="ADD3">
          <block type="math_arithmetic" id="nz0W2[Z?Tc-^uebU5ErH">
            <field name="OP">MULTIPLY</field>
            <comment pinned="false" h="37" w="155">將「09月」改為「9月」</comment>
            <value name="A">
              <block type="built_in_time" id=":a4vRzNmHkUGvM~GOiI/">
                <field name="NAME">month</field>
              </block>
            </value>
            <value name="B">
              <block type="math_number" id="M=k.jK]pT9IYzBLlYKPe">
                <field name="NUM">1</field>
              </block>
            </value>
          </block>
        </value>
        <value name="ADD4">
          <block type="text" id="3WT_$zY8oDl!1WHN37}~">
            <field name="TEXT">月</field>
          </block>
        </value>
        <value name="ADD5">
          <block type="built_in_time" id="Ba=0#KTsgH`Ijdly#0+q">
            <field name="NAME">day</field>
          </block>
        </value>
        <value name="ADD6">
          <block type="text" id="Z,A}^E`o/6Cyo)m}AqT%">
            <field name="TEXT">日</field>
          </block>
        </value>
        <value name="ADD7">
          <block type="text" id="H78r)U*L}t~7e.@L5dM2">
            <field name="TEXT">  星期</field>
          </block>
        </value>
        <value name="ADD8">
          <block type="built_in_wday_zh" id="EkC@I@+HGH5^cu~3G=S="></block>
        </value>
      </block>
    </value>
  </block>
  <block type="hotstring" id="TNWAh{Y3xozLNH.7tGxR" x="26" y="369">
    <value name="ABB">
      <block type="text" id="8:Q2t+aU.@:TJJ:CLY^b">
        <field name="TEXT">\\now</field>
      </block>
    </value>
    <value name="TEXT">
      <block type="procedures_callreturn" id="F[M88Yax:0WU4!*Qdg+1">
        <mutation name="現在時間"></mutation>
      </block>
    </value>
  </block>
  <block type="hotstring" id="Lx0J5yJv8G#uLgpx7bO(" x="440" y="370">
    <value name="ABB">
      <block type="text" id="R8UjYUXVQlt@`+d/F=pE">
        <field name="TEXT">\date</field>
      </block>
    </value>
    <value name="TEXT">
      <block type="procedures_callreturn" id="aq{LXI=8j-YmPl}vs0wX">
        <mutation name="現在日期"></mutation>
      </block>
    </value>
  </block>
</xml>'''

#endregion 插入範例1


#插入範本
def ViewEx(ev):
    doc['textarea_xml'].value=xml_ex_1
    XmlToBlockly(window.Event.new("input"))
    #doc['btn_blockToAhk'].click()

#設置AHK語法轉換結果畫面元素
div_showAhkArea_elt=DIV(id="div_show_ahk_area")

#設置橫幅DIV元素，並填充文字和複製、下載按鈕
div_showAhkAreaHeader_elt=DIV(id="div_show_ahk_btns")
div_showAhkAreaHeader_elt<=BUTTON("▼轉換為AHK語法",id="btn_blockToAhk").bind("click",BlocklyToXml)
div_showAhkAreaHeader_elt<=BUTTON("載入範本1").bind("click",ViewEx)

#定義動作:複製AHK語法
def CopyAhkCode(ev):
    ahk_code=doc['textarea_ahk'].innerHTML
    CopyTextToClipborad(ahk_code)
    alert('複製成功!')

#定義動作:下載AHK檔案
def DownloadAhkCode(ev):
    ahk_code=doc['textarea_ahk'].innerHTML
    filename="myahk.ahk"
    DownloadTextFile(filename,ahk_code)

#設置複製和下載按鈕
div_showAhkAreaBtns_elt=DIV(id="div_copy_ahkfile_btns_area")
div_showAhkAreaBtns_elt<=BUTTON("複製語法").bind("click",CopyAhkCode)
div_showAhkAreaBtns_elt<=BUTTON("下載.ahk檔案").bind("click",DownloadAhkCode)

#排版
div_showAhkArea_elt<=div_showAhkAreaHeader_elt
div_showAhkArea_elt<=PRE(
    id="textarea_ahk",
)
div_showAhkArea_elt<=div_showAhkAreaBtns_elt


#設置XML轉換結果畫面元素
div_textareaXml_elt=DIV(id='input_xml_area')
#實際部屬時，要把XML區塊隱藏起來
if 'herokuapp' in window.location.hostname:
    div_textareaXml_elt.style.display="none"
div_textareaXml_elt
div_textareaXml_elt<=P("xml:")
textarea_showXml_elt=TEXTAREA(
    id="textarea_xml",
)
textarea_showXml_elt.bind('input',XmlToAHK)
textarea_showXml_elt.bind('input',XmlToBlockly)
div_textareaXml_elt<=textarea_showXml_elt


#設置使用說明iframe
iframe_elt=IFRAME(src="https://hackmd.io/@papple23g/r1RuM08tB")
div_iframe_elt=DIV(iframe_elt)

#設置子頁面標頭DIV元素
div_title_elt=DIV()
#設置標頭H1元素
VERSION="1.6" ##
h1_title_elt=H1(f"AutoHotKey 積木語法產生器 v{VERSION}",style={"color":"rgb(220, 107, 57)","font-size":"18px","font-weight":"600",'float':'left'})
#設置FB DIV元素
div_fb_elt=DIV(id='div_fb',style={'float':'right'})
div_fb_elt.innerHTML=r'<div id="fb-root" style="float:right"></div><div class="fb-like" data-href"https://papple23g-ahkcompiler.herokuapp.com/ahkblockly" data-layout="button_count" data-action="like" data-size="small" data-show-faces="false" data-share="true"></div>' # style="float:right"
#
div_title_elt<=h1_title_elt
div_title_elt<=div_fb_elt+DIV(style={'clear':'both'})

#排版

#設置版本標題
doc['div_ahkblockly_gui'].insertBefore(div_title_elt,doc['div_ahkblockly_gui'].select_one('div'))
#載入完Brython後才顯示workspace區塊 (才能一併顯示頁面)
doc['blocklyDiv'].style.visibility="visible"
#在ahkblockly_gui置入程式碼區塊
doc['div_ahkblockly_gui']<=div_showAhkArea_elt
doc['div_ahkblockly_gui']<=div_textareaXml_elt
#置入說明區塊
doc['div_subMainPage']<=div_iframe_elt
AddStyle('''

    #div_ahkblockly_gui {
        width: 69% !important;
        float: left;
        margin-bottom: 150px;

    }

    iframe{
        float: left;
        border: none;
        width: 30%;
        min-width: 200px;
        height: 1000px;
    }

    @media only screen and (max-width: 911px) {
        #div_ahkblockly_gui {
            width: 90% !important;
        }
        iframe{
            width: 90%;
        }
    }
''')
#調整workspace為符合當前頁面的尺寸
Blockly.svgResize(workspace)

#定義動作:儲存
def StoringXml(ev):
    #獲取workspace blockly的xml
    xml_str=Blockly.Xml.workspaceToDom(workspace).outerHTML
    #紀錄xml到暫存空間
    storage['xml']=xml_str
workspace.addChangeListener(StoringXml)


#首次載入網頁時，若暫存空間裡有xml的資料，就印出該資資料
if 'xml' in storage.keys():
    #獲取之前儲存的xml資料
    doc['textarea_xml'].value=storage['xml']
    #觸發xml轉Blockly
    doc['textarea_xml'].dispatchEvent(window.Event.new("input"))
#否則，解析workspace
else:
    BlocklyToXml(window.Event.new("change"))



#{% endverbatim %}
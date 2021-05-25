var hotstring_color = "#CD5C5C";
var hotstringSetting_color = "#D0873E";

Blockly.Blocks['list_str'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck("Array")
            .appendField("串列文字化");
        this.setOutput(true, null);
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['break_line_chr'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("↵ 換行");
        this.setOutput(true, "String");
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['screenshot'] = {
    init: function() {
        this.appendValueInput("path")
            .setCheck("dirpath")
            .appendField("擷取螢幕至路徑");
        this.appendValueInput("filename")
            .setCheck(["filepath", "dirpath", "String"])
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("圖片檔名為");
        this.appendDummyInput()
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField(new Blockly.FieldDropdown([
                [".png", ".png"],
                [".jpg", ".jpg"],
                ["無 (自訂於檔名)", ""]
            ]), "subfilename");
        this.setInputsInline(false);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};
Blockly.Blocks['set_brightness'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("螢幕亮度");
        this.appendValueInput("NAME")
            .setCheck("Number")
            .appendField(new Blockly.FieldDropdown([
                ["增加", "add"],
                ["減少", "sub"],
                ["設為", "set"]
            ]), "action");
        this.appendDummyInput()
            .appendField("%");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(90);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['close_monitor'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("關閉顯示器");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['msgbox_yesorno'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("跳出確認視窗");
        this.appendValueInput("title")
            .setCheck("String")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("標題");
        this.appendValueInput("text")
            .setCheck("String")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("內容");
        this.appendStatementInput("yes")
            .setCheck(null)
            .setAlign(Blockly.ALIGN_CENTRE)
            .appendField("若按了[是]");
        this.appendStatementInput("no")
            .setCheck(null)
            .appendField("若按了[否]");
        this.setPreviousStatement(true, null);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['inputbox'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("待使用者輸入值");
        this.appendDummyInput()
            .appendField("紀錄至變數")
            .appendField(new Blockly.FieldVariable("輸入值"), "NAME");
        this.appendValueInput("title")
            .setCheck("String")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("輸入框標題");
        this.appendValueInput("text")
            .setCheck("String")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("輸入框內容");
        this.appendDummyInput()
            .appendField("設定視窗寬度")
            .appendField(new Blockly.FieldNumber(0, 400, Infinity, 1), "w")
            .appendField("高度")
            .appendField(new Blockly.FieldNumber(0, 150, Infinity, 1), "h");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(330);
        this.setTooltip("");
        this.setHelpUrl("");
    }
}

Blockly.Blocks['math_random'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("設")
            .appendField(new Blockly.FieldVariable("X"), "NAME")
            .appendField("為一個從");
        this.appendValueInput("min")
            .setCheck("Number");
        this.appendValueInput("max")
            .setCheck("Number")
            .appendField("至");
        this.appendDummyInput()
            .appendField("的隨機")
            .appendField(new Blockly.FieldDropdown([
                ["整數", "int"],
                ["浮點數", "float"]
            ]), "type");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['math_round'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck("Number");
        this.appendValueInput("digit")
            .setCheck("Number")
            .appendField("四捨五入至小數點第");
        this.appendDummyInput()
            .appendField("位");
        this.setInputsInline(true);
        this.setOutput(true, "Number");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['math_mod'] = {
    init: function() {
        this.appendValueInput("a")
            .setCheck("Number");
        this.appendValueInput("b")
            .setCheck("Number")
            .appendField("除以");
        this.appendDummyInput()
            .appendField("的")
            .appendField(new Blockly.FieldDropdown([
                ["餘數", "餘數"],
                ["商數", "商數"]
            ]), "NAME");
        this.setInputsInline(true);
        this.setOutput(true, "Number");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['math_constant2'] = {
    init: function() {
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([
                ["π", "pi"],
                ["e", "e"],
                ["φ", "golden_ratio"]
            ]), "NAME");
        this.setOutput(true, "Number");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['math_function2'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck("Number");
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([
                ["的絕對值", "abs"],
                ["向上取整數", "ceil"],
                ["向下取整數", "floor"]
            ]), "NAME");
        this.setInputsInline(true);
        this.setOutput(true, "Number");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['math_function'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck("Number")
            .appendField(new Blockly.FieldDropdown([
                ["sin", "sin"],
                ["cos", "cos"],
                ["tan", "tan"],
                ["asin", "asin"],
                ["acos", "acos"],
                ["atan", "atan"],
                ["√", "sqrt"],
                ["log", "log"],
                ["ln", "ln"],
                ["e^", "exp"]
            ]), "NAME")
            .appendField("(");
        this.appendDummyInput()
            .appendField(")");
        this.setOutput(true, "Number");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['open_with_main_program'] = {
    init: function() {
        this.appendValueInput("main_program")
            .setCheck(["filepath", "String"])
            .appendField("用");
        this.appendValueInput("file")
            .setCheck(["dirpath", "filepath", "link", "String"])
            .appendField("程式來開啟");
        this.appendDummyInput()
            .appendField("檔案");
        this.setInputsInline(true);
        this.setOutput(true, "filepath");
        this.setColour(290);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['reload'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("刷新AHK腳本");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['hotkey_execute_setting_ifwinactive'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("只生效於當前視窗標題含文字 : ")
            .appendField(new Blockly.FieldTextInput(""), "text");
        this.setPreviousStatement(true, "hotkey_execute_setting");
        this.setNextStatement(true, "hotkey_execute_setting");
        this.setColour(195);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['hotkey_execute_setting_cantriggeronotherhotkey'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("可在其他組合鍵觸發");
        this.setPreviousStatement(true, "hotkey_execute_setting");
        this.setNextStatement(true, "hotkey_execute_setting");
        this.setColour(195);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['hotkey_execute_setting_donottriggeritself'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("避免自我觸發");
        this.setPreviousStatement(true, "hotkey_execute_setting");
        this.setNextStatement(true, "hotkey_execute_setting");
        this.setColour(195);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['hotkey_execute_setting_keepkeyfuncdefalut'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("保留預設按鍵功能");
        this.setPreviousStatement(true, "hotkey_execute_setting");
        this.setNextStatement(true, "hotkey_execute_setting");
        this.setColour(195);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['hotkey_execute_with_setting'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(["normal_key", "function_key", "special_key"])
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("當按下");
        this.appendStatementInput("DO")
            .setCheck("action")
            .appendField("執行");
        this.appendStatementInput("SETTING")
            .setCheck("hotkey_execute_setting")
            .appendField("設定");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['get_key_state'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(['normal_key', 'special_key'])
            .appendField("按鍵");
        this.appendDummyInput()
            .appendField("是被按著的");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour(210);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['web_element_alert'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(null)
            .appendField("跳出網頁訊息");
        this.setInputsInline(false);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#C79304");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['web_element_selectedindex'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck('web_element')
            .appendField("下拉選單");
        this.appendValueInput("to_value")
            .setCheck("Number")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("選擇第");
        this.appendDummyInput()
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("　　　　　　　項目");
        this.setInputsInline(false);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#C79304");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['web_element_setValue'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck('web_element')
            .appendField("文字框");
        this.appendValueInput("to_value")
            .setCheck(["Number", "String"])
            .appendField("設值為");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#C79304");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['web_element_focus'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck('web_element')
            .appendField("聚焦在");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#C79304");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['web_element_click'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck('web_element')
            .appendField("點擊");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#C79304");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['web_element'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("網頁元素")
            .appendField(new Blockly.FieldDropdown([
                ["JS path", "js_path"],
                ["CSS selector", "css"]
            ]), "elt_address")
            .appendField(":")
            .appendField(new Blockly.FieldTextInput("#button"), "NAME");
        this.setInputsInline(false);
        this.setOutput(true, 'web_element');
        this.setColour("#E3B776");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['str_replace'] = {
    init: function() {
        this.appendValueInput("text")
            .setCheck(["String", "link", "dirpath", "filepath"])
            .appendField("文字");
        this.appendValueInput("subs")
            .setCheck("String")
            .appendField("的");
        this.appendValueInput("to")
            .setCheck("String")
            .appendField("替換為");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['win_activate'] = {
    init: function() {
        this.appendValueInput("title")
            .setCheck("String")
            .appendField("置頂視窗, 標題含:");
        this.setInputsInline(false);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['run_or_active'] = {
    init: function() {
        this.appendValueInput("run")
            .setCheck(["dirpath", "filepath", "link", "String"])
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("開啟");
        this.appendValueInput("title")
            .setCheck("String")
            .appendField("或置頂視窗, 標題含:");
        this.setInputsInline(false);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['while_true'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("無限循環");
        this.appendStatementInput("DO")
            .setCheck("action");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(120);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['image_filepath'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(["filepath", "String"])
            .appendField("圖片來源");
        this.setInputsInline(false);
        this.setPreviousStatement(true, "get_picture_pos_setting");
        this.setNextStatement(true, "get_picture_pos_setting");
        this.setColour("#DB7093");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['image_search_area'] = {
    init: function() {
        this.appendValueInput("X")
            .setCheck("Number")
            .appendField("偵測範圍 X1:");
        this.appendValueInput("Y")
            .setCheck("Number")
            .appendField("Y1:");
        this.appendValueInput("W")
            .setCheck("Number")
            .appendField("X2:");
        this.appendValueInput("H")
            .setCheck("Number")
            .appendField("Y2:");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "get_picture_pos_setting");
        this.setNextStatement(true, "get_picture_pos_setting");
        this.setColour("#DB7093");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['pixel_search_area'] = {
    init: function() {
        this.appendValueInput("X")
            .setCheck("Number")
            .appendField("偵測範圍 X1:");
        this.appendValueInput("Y")
            .setCheck("Number")
            .appendField("Y1:");
        this.appendValueInput("W")
            .setCheck("Number")
            .appendField("X2:");
        this.appendValueInput("H")
            .setCheck("Number")
            .appendField("Y2:");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "get_pixel_pos_setting");
        this.setNextStatement(true, "get_pixel_pos_setting");
        this.setColour("#E8A0A0");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['pixel_color_id'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("色碼 #")
            .appendField(new Blockly.FieldTextInput("FFFFFF"), "ColorID");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "get_pixel_pos_setting");
        this.setNextStatement(true, "get_pixel_pos_setting");
        this.setColour("#E8A0A0");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['pixel_rgb_color'] = {
    init: function() {
        this.appendValueInput("R")
            .setCheck("Number")
            .appendField("R");
        this.appendValueInput("G")
            .setCheck("Number")
            .appendField("G");
        this.appendValueInput("B")
            .setCheck("Number")
            .appendField("B");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "get_pixel_pos_setting");
        this.setNextStatement(true, "get_pixel_pos_setting");
        this.setColour("#E8A0A0");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['get_pixel_pos'] = {
    init: function() {
        this.appendStatementInput("get_pixel_pos_setting")
            .setCheck("get_pixel_pos_setting")
            .appendField("偵測像素");
        this.appendDummyInput()
            .appendField("將獲得的座標紀錄至變數(")
            .appendField(new Blockly.FieldVariable("圖片像素X"), "pos_x")
            .appendField(",")
            .appendField(new Blockly.FieldVariable("圖片像素Y"), "pos_y")
            .appendField(")");
        this.appendStatementInput("DO")
            .setCheck("action")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("找到像素時");
        this.appendStatementInput("ELSE_DO")
            .setCheck("action")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("找不到時");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#E8A0A0");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['get_picture_pos_ver200419'] = {
    init: function() {
        this.appendStatementInput("get_picture_pos_setting")
            .setCheck("get_picture_pos_setting")
            .appendField("偵測圖片");
        this.appendDummyInput()
            .appendField("將獲得的座標紀錄至變數(")
            .appendField(new Blockly.FieldVariable("圖片座標X"), "pos_x")
            .appendField(",")
            .appendField(new Blockly.FieldVariable("圖片座標Y"), "pos_y")
            .appendField(")");
        this.appendStatementInput("DO")
            .setCheck("action")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("找到圖片時");
        this.appendStatementInput("ELSE_DO")
            .setCheck("action")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("找不到時");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#DB7093");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['get_picture_pos_ver200406'] = {
    init: function() {
        this.appendValueInput("image_filepath")
            .setCheck(["filepath", "String"])
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("在當前畫面搜尋圖片");
        this.appendDummyInput()
            .appendField("獲得座標(")
            .appendField(new Blockly.FieldVariable("圖片座標X"), "pos_x")
            .appendField(",")
            .appendField(new Blockly.FieldVariable("圖片座標Y"), "pos_y")
            .appendField(")");
        this.appendStatementInput("DO")
            .setCheck(null)
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("找到圖片後");
        this.appendStatementInput("ELSE_DO")
            .setCheck(null)
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("找不到時");
        this.setInputsInline(false);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#DB7093");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['get_picture_pos'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("在當前畫面搜尋圖片")
            .appendField(new Blockly.FieldTextInput("C:\\*.png"), "img_filepath");
        this.appendDummyInput()
            .appendField("並將位置座標紀錄至(")
            .appendField(new Blockly.FieldVariable("圖片座標X"), "pos_x")
            .appendField(",")
            .appendField(new Blockly.FieldVariable("圖片座標Y"), "pos_y")
            .appendField(")");
        this.appendStatementInput("DO")
            .setCheck(null)
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("找到圖片後");
        this.appendStatementInput("ELSE_DO")
            .setCheck(null)
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("找不到時");
        this.setInputsInline(false);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#DB7093");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['block_input'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("防止外部按鍵干擾的情況下，執行:");
        this.appendStatementInput("DO")
            .setCheck(null)
            .setAlign(Blockly.ALIGN_RIGHT);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#708090");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['search_selected_keyword_custom'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("將選取的關鍵字進行")
            .appendField(new Blockly.FieldTextInput("(自訂範例) Google學術網"), "website_name")
            .appendField("搜尋");
        this.appendDummyInput()
            .appendField("    關鍵字之前的網址:")
            .appendField(new Blockly.FieldTextInput("https://scholar.google.com.tw/scholar?hl=zh-TW&as_sdt=0%2C5&q="), "url_a");
        this.appendDummyInput()
            .appendField("    關鍵字之後的網址:")
            .appendField(new Blockly.FieldTextInput("&btnG="), "url_b");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['search_selected_keyword'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("將選取的關鍵字進行")
            .appendField(new Blockly.FieldDropdown([
                ["Google搜尋", "google"],
                ["Youtube搜尋", "youtube"],
                ["WIKI搜尋", "wiki"],
                ["百度搜尋", "baidu"],
                ["Google地圖搜尋", "google_map"],
                ["Google搜尋趨勢", "google_trend"],
                ["Gooogle翻譯", "google_translate"],
                ["Evernote搜尋", "evernote"],
                ["Facebook搜尋", "facebook"],
                ["cdict(英翻中/中翻英)", "cdict"],
                ["噗浪搜尋", "plurk"],
                ["推特搜尋", "twitter"],
                ["萌典(中文字典)", "moedict"]
            ]), "NAME");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['open_select_url'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("進入被選取的網址文字");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['paste_text'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(null)
            .appendField("貼上文字");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['key_pressing'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(["special_key", "normal_key"])
            .appendField("按著");
        this.appendDummyInput()
            .appendField("不放");
        this.appendStatementInput("DO")
            .setCheck(null)
            .appendField("執行");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['key_down'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(["special_key", "normal_key"])
            .appendField("按著");
        this.appendDummyInput()
            .appendField("不放");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['key_up'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(["special_key", "normal_key"])
            .appendField("釋放");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};



Blockly.Blocks['key_wait'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(["special_key", "normal_key"])
            .appendField("等待按鍵");
        this.appendDummyInput()
            .appendField("釋放");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#80ADC4");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['cmd'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("CMD碼")
            .appendField(new Blockly.FieldTextInput("Notepad.exe"), "code")
            .appendField("執行完後")
            .appendField(new Blockly.FieldDropdown([
                ["關閉視窗", "close"],
                ["不關閉視窗", "dont_close"]
            ]), "do_close");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#C4C4C4");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['volume_mute'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("靜音 / 取消靜音");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#C95E00");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['volume_adjust'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("音量")
            .appendField(new Blockly.FieldDropdown([
                ["增加", "add"],
                ["降低", "sub"],
                ["設為", "set"],
            ]), "action");
        this.appendValueInput("NAME")
            .setCheck("Number");
        this.appendDummyInput()
            .appendField("%");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#C95E00");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['shutdown'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("電腦")
            .appendField(new Blockly.FieldDropdown([
                ["關機", "shutdown"],
                ["登出", "logout"],
                ["睡眠", "sleep"],
                ["休眠", "deepsleep"],
                ["鎖定", "lock"],
                ["重新啟動", "restart"]
            ]), "action")
            .appendField("　")
            .appendField(new Blockly.FieldCheckbox("TRUE"), "force")
            .appendField("強制執行");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['right_click_menu_item_hr'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("──── 項目水平線 ────");
        this.setPreviousStatement(true, ["right_click_menu_item", "right_click_menu_item_hr"]);
        this.setNextStatement(true, ["right_click_menu_item", "right_click_menu_item_hr"]);
        this.setColour("#00CED1");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['right_click_menu_item'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("項目")
            .appendField(new Blockly.FieldTextInput("名稱"), "item_name");
        this.appendStatementInput("DO")
            .setCheck(null)
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("執行");
        this.setInputsInline(false);
        this.setPreviousStatement(true, ["right_click_menu_item", "right_click_menu_item_hr"]);
        this.setNextStatement(true, ["right_click_menu_item", "right_click_menu_item_hr"]);
        this.setColour("#00CED1");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};



Blockly.Blocks['right_click_menu'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("顯示右鍵清單");
        this.appendStatementInput("NAME")
            .setCheck("right_click_menu_item");
        this.setInputsInline(false);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#00CED1");
        this.setTooltip("");
        this.setHelpUrl("");
    }
}


Blockly.Blocks['in_str'] = {
    init: function() {
        this.appendValueInput("text")
            .setCheck("String");
        this.appendValueInput("sub_text")
            .setCheck("String")
            .appendField(new Blockly.FieldDropdown([
                ["包含", "contain"],
                ["不包含", "not_contain"]
            ]), "NAME")
            .appendField("文字");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour(210);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['win_get_active_title'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(null)
            .appendField("將目前視窗名稱紀錄至");
        this.appendDummyInput()
            .appendField("變數");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#956D49");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['mouse_get_pos'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("將目前滑鼠座標紀錄至(")
            .appendField(new Blockly.FieldVariable("滑鼠座標X"), "posX")
            .appendField(",")
            .appendField(new Blockly.FieldVariable("滑鼠座標Y"), "posY")
            .appendField(") 兩個變數");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(60);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['coord_mode'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("設定以")
            .appendField(new Blockly.FieldDropdown([
                ["螢幕左上角", "screen"],
                ["視窗左上角", "window "],
            ]), "NAME");
        this.appendDummyInput()
            .appendField("為座標原點");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(60);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['click_x_y'] = {
    init: function() {
        this.appendValueInput("X")
            .setCheck("Number")
            .appendField("滑鼠至 X:");
        this.appendValueInput("Y")
            .setCheck("Number")
            .appendField("Y:");
        this.appendValueInput("TIMES")
            .setCheck("Number")
            .appendField("點擊");
        this.appendDummyInput()
            .appendField("次");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(60);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['ahk_code'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("AHK碼")
            .appendField(new Blockly.FieldTextInput("Msgbox % \"Hellow World !\""), "NAME");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#818181");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['computer_name'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("本電腦名稱");
        this.setOutput(true, "String");
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['user_name'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("本用戶名稱");
        this.setOutput(true, "String");
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};



Blockly.Blocks['set_clipboard'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(null)
            .appendField("剪貼簿內容 設為");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['built_in_wday_zh'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("現星期(一 ~ 日)");
        this.setOutput(true, "String");
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['return'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("禁用該熱鍵");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#555555");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['clipboard'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("剪貼簿內容");
        this.setInputsInline(true);
        this.setOutput(true, null);
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['sleep'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck("Number")
            .appendField("等待");
        this.appendDummyInput()
            .appendField("毫秒");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour("#80ADC4");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['built_in_webpage'] = {
    init: function() {
        this.appendDummyInput()
            .setAlign(Blockly.ALIGN_CENTRE)
            .appendField(new Blockly.FieldDropdown([
                ["Google網頁", "google"],
                ["Youtube網頁", "youtube"],
                ["Facebook網頁", "facebook"],
                ["百度搜尋", "baidu"],
                ["Wikipedia網頁", "wikipedia"],
                ["PChome網頁", "pchome"],
                ["Yahoo網頁", "yahoo"],
                ["Google地圖", "googlemap"],
                ["AHK官網", "ahk"],
                ["AHK積木網頁", "ahkblockly"],
            ]), "NAME");
        this.setOutput(true, "link");
        this.setColour(290);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['built_in_time'] = {
    init: function() {
        this.appendDummyInput()
            .setAlign(Blockly.ALIGN_CENTRE)
            .appendField(new Blockly.FieldDropdown([
                ["現年(YYYY)", "year"],
                ["現月(01-12)", "month"],
                ["現日(01-31)", "day"],
                ["現星期(1-7)", "wday"],
                ["現時(00-23)", "hour"],
                ["現分(00-59)", "min"],
                ["現秒(00-59)", "sec"],
            ]), "NAME");
        this.setOutput(true, "Number");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['built_in_program'] = {
    init: function() {
        this.appendDummyInput()
            .setAlign(Blockly.ALIGN_CENTRE)
            .appendField(new Blockly.FieldDropdown([
                ["記事本", "notepad"],
                ["小畫家", "mspaint"],
                ["小算盤", "calc"],
                ["剪取工具", "SnippingTool"],
                ["命令提示字元", "cmd"],
                ["AHK腳本", "ahkfile"],
                ["AHK主程式", "ahkexe"],
            ]), "NAME");
        this.setOutput(true, "filepath");
        this.setColour(290);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['built_in_dirpath'] = {
    init: function() {
        this.appendDummyInput()
            .setAlign(Blockly.ALIGN_CENTRE)
            .appendField(new Blockly.FieldDropdown([
                ["桌面", "desktop"],
                ["我的文件", "mydocuments"],
                ["啟動資料夾", "startup"],
                ["臨時資料夾", "temp"],
                ["Windows資料夾", "windows"],
                ["AHK腳本目錄", "ahkfilepath"],
            ]), "NAME");
        this.setOutput(true, "dirpath");
        this.setColour(290);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['path_combined'] = {
    init: function() {
        this.appendValueInput("main_path")
            .setCheck("dirpath")
            .appendField("路徑");
        this.appendValueInput("sub_path")
            .setCheck(["dirpath", "filepath"])
            .appendField("底下的");
        this.setInputsInline(true);
        this.setOutput(true, "filepath");
        this.setColour(290);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['send_keys'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("送出連續按鍵")
            .appendField(new Blockly.FieldTextInput("abc"), "NAME");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['send_text'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(["String", "Number"])
            .appendField("輸入文字");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['hotstring_do'] = {
    init: function() {
        this.appendValueInput("ABB")
            .setCheck("String")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("當輸入");
        this.appendStatementInput("DO")
            .setCheck("action")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("執行");
        this.appendStatementInput("SETTING")
            .setCheck("hotstring_setting")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("設定");
        this.setColour(hotstring_color);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['hotstringSetting_autoExpaned'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("立即展開而不用按下終止鍵 (如空格、Enter、Tab...)");
        this.setPreviousStatement(true, "hotstring_setting");
        this.setNextStatement(true, "hotstring_setting");
        this.setColour(hotstringSetting_color);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};
Blockly.Blocks['hotstringSetting_dontFireEndKey'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("展開後不觸發終止鍵");
        this.setPreviousStatement(true, "hotstring_setting");
        this.setNextStatement(true, "hotstring_setting");
        this.setColour(hotstringSetting_color);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};
Blockly.Blocks['hotstringSetting_caseSensitive'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("縮寫區分大小寫");
        this.setPreviousStatement(true, "hotstring_setting");
        this.setNextStatement(true, "hotstring_setting");
        this.setColour(hotstringSetting_color);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};
Blockly.Blocks['hotstringSetting_expanedInWrods'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("可在字詞間觸發");
        this.setPreviousStatement(true, "hotstring_setting");
        this.setNextStatement(true, "hotstring_setting");
        this.setColour(hotstringSetting_color);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};
Blockly.Blocks['hotstringSetting_rawText'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("使用{TEXT}展開 (可展開中文)");
        this.setPreviousStatement(true, "hotstring_setting");
        this.setNextStatement(true, "hotstring_setting");
        this.setColour(hotstringSetting_color);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['hotstring_advanced'] = {
    init: function() {
        this.appendValueInput("ABB")
            .setCheck("String")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("輸入縮寫");
        this.appendValueInput("TEXT")
            .setCheck(["String", "Number"])
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("展開為");
        this.appendStatementInput("SETTING")
            .setCheck("hotstring_setting")
            .appendField("設定");
        this.setInputsInline(false);
        this.setColour(hotstring_color);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['hotstring'] = {
    init: function() {
        this.appendValueInput("ABB")
            .setCheck("String")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("輸入縮寫");
        this.appendValueInput("TEXT")
            .setCheck(["String", "Number"])
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("按下Enter展開為");
        this.setInputsInline(false);
        this.setColour(hotstring_color);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['send_key'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(["normal_key", "function_key", "special_key"])
            .appendField("送出按鍵");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['send_key_times'] = {
    init: function() {
        this.appendValueInput("KEY")
            .setCheck(["normal_key", "function_key", "special_key"])
            .appendField("送出按鍵");
        this.appendValueInput("TIMES")
            .setCheck("Number")
            .appendField("按");
        this.appendDummyInput()
            .appendField("次");
        this.setInputsInline(true);
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['close_process'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("終止程式")
            .appendField(new Blockly.FieldTextInput("*.exe"), "NAME");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['file_recycle_empty'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("清空資源回收桶");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};



Blockly.Blocks['filepath'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("檔案路徑")
            .appendField(new Blockly.FieldTextInput(""), "NAME");
        this.setOutput(true, "filepath");
        this.setColour(290);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['dirpath'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("目錄路徑")
            .appendField(new Blockly.FieldTextInput("C:\\"), "NAME");
        this.setOutput(true, "dirpath");
        this.setColour(290);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['webpage'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("網頁")
            .appendField(new Blockly.FieldTextInput("https://www.google.com"), "NAME");
        this.setOutput(true, "link");
        this.setColour(290);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};


Blockly.Blocks['open'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(["dirpath", "filepath", "link", "String"])
            .appendField("開啟");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['hotkey_execute'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(["normal_key", "function_key", "special_key"])
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("當按下");
        this.appendStatementInput("DO")
            .setCheck("action")
            .setAlign(Blockly.ALIGN_RIGHT)
            .appendField("執行");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['function_key'] = {
    init: function() {
        this.appendValueInput("function_key")
            .setCheck(["function_key", "normal_key", "special_key"])
            .appendField(new Blockly.FieldDropdown([
                ["Ctrl", "Ctrl"],
                ["Shift", "Shift"],
                ["Alt", "Alt"],
                ["Win", "Win"],
                ["LCtrl", "LCtrl"],
                ["LShift", "LShift"],
                ["LAlt", "LAlt"],
                ["LWin", "LWin"],
                ["RCtrl", "RCtrl"],
                ["RShift", "RShift"],
                ["RAlt", "RAlt"],
                ["RWin", "RWin"],
            ]), "function_key").appendField("+");
        this.setOutput(true, "function_key");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['normal_key'] = {
    init: function() {
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([
                ["A", "A"],
                ["B", "B"],
                ["C", "C"],
                ["D", "D"],
                ["E", "E"],
                ["F", "F"],
                ["G", "G"],
                ["H", "H"],
                ["I", "I"],
                ["J", "J"],
                ["K", "K"],
                ["L", "L"],
                ["M", "M"],
                ["N", "N"],
                ["O", "O"],
                ["P", "P"],
                ["Q", "Q"],
                ["R", "R"],
                ["S", "S"],
                ["T", "T"],
                ["U", "U"],
                ["V", "V"],
                ["W", "W"],
                ["X", "X"],
                ["Y", "Y"],
                ["Z", "Z"],
            ]), "normal_key");
        this.setOutput(true, "normal_key");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['special_key'] = {
    init: function() {
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown([
                ["Ctrl", "Ctrl"],
                ["Shift", "Shift"],
                ["Alt", "Alt"],
                ["Win", "Win"],
                ["LCtrl", "LCtrl"],
                ["LShift", "LShift"],
                ["LAlt", "LAlt"],
                ["LWin", "LWin"],
                ["RCtrl", "RCtrl"],
                ["RShift", "RShift"],
                ["RAlt", "RAlt"],
                ["RWin", "RWin"],
                ["Enter", "Enter"],
                ["Space", "Space"],
                ["Tab", "Tab"],
                ["CapsLock", "CapsLock"],
                ["Esc", "Esc"],
                ["Backspace", "Backspace"],
                ["Delete", "Delete"],
                ["Home", "Home"],
                ["End", "End"],
                ["PgUp", "PgUp"],
                ["PgDn", "PgDn"],
                ["Insert", "Insert"],
                ["PrintScreen", "PrintScreen"],
                ["AppsKey", "AppsKey"],
                ["ScrollLock", "ScrollLock"],
                ["Pause", "Pause"],
                ["滑鼠左鍵", "LButton"],
                ["滑鼠右鍵", "RButton"],
                ["滑鼠中鍵", "MButton"],
                ["滑鼠上滾", "WheelUp"],
                ["滑鼠下滾", "WheelDown"],
                ["↑", "Up"],
                ["↓", "Down"],
                ["←", "Left"],
                ["→", "Right"],
                ["Numpad0", "Numpad0"],
                ["Numpad1", "Numpad1"],
                ["Numpad2", "Numpad2"],
                ["Numpad3", "Numpad3"],
                ["Numpad4", "Numpad4"],
                ["Numpad5", "Numpad5"],
                ["Numpad6", "Numpad6"],
                ["Numpad7", "Numpad7"],
                ["Numpad8", "Numpad8"],
                ["Numpad9", "Numpad9"],
                ["Numpad.", "NumpadDot"],
                ["Numpad/", "NumpadDiv"],
                ["Numpad*", "NumpadMult"],
                ["Numpad-", "NumpadSub"],
                ["Numpad+", "NumpadAdd"],
                ["NumpadEnter", "NumpadEnter"],
                ["NumLock", "NumLock"],
                ["` (～)", "`"],
                ["0 (）)", "0"],
                ["1 (！)", "1"],
                ["2 (＠)", "2"],
                ["3 (＃)", "3"],
                ["4 (＄)", "4"],
                ["5 (％)", "5"],
                ["6 (︿)", "6"],
                ["7 (＆)", "7"],
                ["8 (＊)", "8"],
                ["9 (（)", "9"],
                ["－　(＿)", "-"],
                ["＝　(＋)", "="],
                ["［　(｛)", "["],
                ["］　(｝)", "]"],
                ["＼　(｜)", "\\"],
                ["；　(：)", "`;"],
                ["　’　(＂)", "'"],
                ["，　(＜)", "`,"],
                ["．　(＞)", "."],
                ["／　(？)", "/"],
                ["F1", "F1"],
                ["F2", "F2"],
                ["F3", "F3"],
                ["F4", "F4"],
                ["F5", "F5"],
                ["F6", "F6"],
                ["F7", "F7"],
                ["F8", "F8"],
                ["F9", "F9"],
                ["F10", "F10"],
                ["F11", "F11"],
                ["F12", "F12"],
            ]), "special_key");
        this.setOutput(true, "special_key");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['msgbox'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(null)
            .appendField("跳出訊息");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
}

Blockly.Blocks['traytip'] = {
    init: function() {
        this.appendValueInput("NAME")
            .setCheck(null)
            .appendField("桌面通知");
        this.setPreviousStatement(true, "action");
        this.setNextStatement(true, "action");
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
}

Blockly.Blocks['system_info_num'] = {
    init: function() {
        this.appendDummyInput()
            .setAlign(Blockly.ALIGN_CENTRE)
            .appendField(new Blockly.FieldDropdown([
                ["本螢幕寬度", "screen_width"],
                ["本螢幕高度", "screen_height"],
                ["本螢幕位置X", "screen_x"],
                ["本螢幕位置Y", "screen_y"],
            ]), "NAME");
        this.setOutput(true, "Number");
        this.setColour(230);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['system_info_str'] = {
    init: function() {
        this.appendDummyInput()
            .setAlign(Blockly.ALIGN_CENTRE)
            .appendField(new Blockly.FieldDropdown([
                ["本用戶名稱", "user_name"],
                ["本電腦名稱", "computer_name"],
            ]), "NAME");
        this.setOutput(true, "Number");
        this.setColour(160);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};
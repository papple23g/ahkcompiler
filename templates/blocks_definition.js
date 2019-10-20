var hotstring_color = "#CD5C5C";
var hotstringSetting_color = "#D0873E";

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
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
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
            .appendField("將目前視窗名稱輸出至");
        this.appendDummyInput()
            .appendField("變數");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour("#956D49");
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['mouse_get_pos'] = {
    init: function() {
        this.appendValueInput("posX")
            .setCheck(null)
            .appendField("將目前滑鼠座標輸出至(");
        this.appendValueInput("posY")
            .setCheck(null)
            .appendField(",");
        this.appendDummyInput()
            .appendField(") 兩個變數");
        this.setInputsInline(true);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
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
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
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
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
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
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour("#C4C4C4");
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
            .appendField("剪接簿內容 設為");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(260);
        this.setTooltip("");
        this.setHelpUrl("");
    }
};

Blockly.Blocks['built_in_wday_zh'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("現週(一 ~ 日)");
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
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
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
        this.setColour(290);
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
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
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
        this.setOutput(true, "dirpath");
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
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
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
            .setCheck(["dirpath", "filepath", "link"])
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
                ["Numpad.", "Numpad."],
                ["Numpad/", "Numpad/"],
                ["Numpad*", "Numpad*"],
                ["Numpad-", "Numpad-"],
                ["Numpad+", "Numpad+"],
                ["NumpadEnter", "NumpadEnter"],
                ["NumLock", "NumLock"],
                ["`", "`"],
                ["0", "0"],
                ["1", "1"],
                ["2", "2"],
                ["3", "3"],
                ["4", "4"],
                ["5", "5"],
                ["6", "6"],
                ["7", "7"],
                ["8", "8"],
                ["9", "9"],
                ["－", "-"],
                ["＝", "="],
                ["［", "["],
                ["］", "]"],
                ["＼", "\\"],
                ["；", "`;"],
                ["’", "'"],
                ["，", "`,"],
                ["．", "."],
                ["／", "/"],
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
};
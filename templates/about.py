
#設置更新日誌iframe
iframe_elt=IFRAME(id="iframe_ahktool_iframe",src="https://hackmd.io/@papple23g/SkRWltCVB")
div_iframe_elt=DIV(iframe_elt)

#排版
doc['div_subMainPage']<=div_iframe_elt
AddStyle('''
    iframe{
        border: none;
        width: 100%;
        height: 3000px;
    }
''')
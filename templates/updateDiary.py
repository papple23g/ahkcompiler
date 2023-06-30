
# 設置更新日誌iframe
ahktool_iframe_elt = IFRAME(
    id="iframe_ahktool_iframe", src="https://hackmd.io/@papple12g/rk3yqOnO2")
div_ahktoolIframe_elt = DIV(ahktool_iframe_elt)

ahkblockly_iframe_elt = IFRAME(
    id="iframe_ahkblockly_iframe", src="https://hackmd.io/@papple12g/SJ1fcu2On")
div_ahkblocklyIframe_elt = DIV(ahkblockly_iframe_elt)

# 排版
doc['div_subMainPage'] <= ahktool_iframe_elt
doc['div_subMainPage'] <= ahkblockly_iframe_elt
AddStyle('''
    iframe{
        float: left;
        border: none;
        width: 45%;
        height: 3000px;
    }

    @media only screen and (max-width: 911px) {
        iframe{
            width: 90%;
        }
    }
''')

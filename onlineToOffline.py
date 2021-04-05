import requests
import os


for app_web_name in [
        'ahktool',
        'ahkblockly',
    ]:

    url=f"https://papple23g-ahkcompiler.herokuapp.com/{app_web_name}"
    # url=u"http://127.0.0.1:8000/ahkblockly"
    res=requests.get(url)


    html=res.text


    need_comment_out_str_list=[
        "doc['div_headerAndBars']",
        'div_showAhkAreaBtns_elt<=BUTTON("下載.exe檔(64-bit)"',
        'div_showAhkAreaBtns_elt<=SPAN("←測試功能',
        "doc['div_subMainPage']<=div_iframe_elt"
    ]

    for need_comment_out_str in need_comment_out_str_list:
        html=html.replace(need_comment_out_str,'#'+need_comment_out_str)

    need_to_replace_str_pairList_list=[
        ['<script src="https://cdn.rawgit.com/brython-dev/brython/3.7.5/www/src/brython.js"></script>','<script src="lib\\brython_3.7.5.js"></script>\n<script src="lib\\brython_stdlib_3.7.5.js"></script>'],
        ["if 'herokuapp' in window.location.hostname:","if True:"],
        ['width: 69% !important;','width: 100% !important;'],
        ['/static/workspace.js','lib/workspace.js'],
        ['href="/static/favicon200218-2.ico"','href="lib/favicon200218-2.ico"'],
        # ['https://use.fontawesome.com/releases/v5.8.1/css/all.css','lib/all.css'],
        ['</script>\n</body>','''
doc['div_copy_ahkfile_btns_area']<=SPAN("Produced by ")
doc['div_copy_ahkfile_btns_area']<=A("papple23g",href="https://papple23g-ahkcompiler.herokuapp.com/about")
</script>\n</body>
''']
    ]

    for need_to_replace_str_pairList in need_to_replace_str_pairList_list:
        html=html.replace(need_to_replace_str_pairList[0],need_to_replace_str_pairList[1])


    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + f'\\protable\\{app_web_name}.html','w',encoding='utf-8') as f:
        f.write(html)

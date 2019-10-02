from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
import os
import uuid

def homepage(req):
    html='<p>123</p>'
    return HttpResponse(html)

def cp(req):
    req_body=req.body.decode()
    ahk_code=req_body
    linebreak_index=ahk_code.find('\n')
    os_type=ahk_code[:linebreak_index+1]
    ahk_code='#SingleInstance force\n'+ahk_code
    filename_key=uuid.uuid4()
    #撰寫ahk檔案
    with open(f"ahkfile1_30/{filename_key}.ahk",'w',encoding="utf-8-sig") as f:
        f.write(ahk_code)
    #執行編譯
    if '64-bit' in os_type:
        cmd_command=f"cd ahkfile1_30 & Ahk2Exe.exe /in {filename_key}.ahk /out {filename_key}.exe /bin \"Unicode 64-bit.bin\" /mpress 1"
    else:
        cmd_command=f"cd ahkfile1_30 & Ahk2Exe.exe /in {filename_key}.ahk /out {filename_key}.exe /bin \"Unicode 32-bit.bin\" /mpress 1"
    print('CMD',cmd_command)
    os.system(cmd_command)
    return HttpResponse(filename_key)

def dl(req):
    filename_key=req.GET.dict()['filename_key']
    filename_key=filename_key[:filename_key.find('?foo=')] if '?foo=' in filename_key else filename_key
    response = FileResponse(open(f'ahkfile1_30/{filename_key}.exe', 'rb'))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="myahk.exe"'
    return response
    
    #return HttpResponse('OKOK!'+filename_key)
from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse
import os
import uuid
import time

def homepage(req):
    return render(req,"AhkScriptGeneratoPager.html")

#定義API:執行AHK編譯為EXE檔
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

#定義API:下載.exe檔
def dl(req):
    filename_key=req.GET.dict()['filename_key']
    filename_key=filename_key[:filename_key.find('?foo=')] if '?foo=' in filename_key else filename_key
    #確認檔名key的uuid版本是否符合格式
    if version_uuid(filename_key)==4:
        response = FileResponse(open(f'ahkfile1_30/{filename_key}.exe', 'rb'))
        response['Content-Type']='application/octet-stream'
        response['Content-Disposition']='attachment;filename="myahk.exe"'
        return response
    else:
        return HttpResponse('unkown uuid vervion')
    
    #return HttpResponse('OKOK!'+filename_key)


#定義API:移除.ahk和.exe檔
def rm(req):
    filename_key=req.GET.dict()['filename_key']
    #確認檔名key的uuid版本是否符合格式
    if version_uuid(filename_key)==4:
        time.sleep(5)
        ahk_filepath=f'ahkfile1_30/{filename_key}.ahk'
        exe_filepath=f'ahkfile1_30/{filename_key}.exe'
        for filepath in [ahk_filepath,exe_filepath]:
            if os.path.isfile(filepath):
                os.remove(filepath)
                print('REMOVE',filepath,'success.')
        return HttpResponse('OKOK!'+filename_key)
    else:
        return HttpResponse('unkown uuid vervion')

#定義檢查函數:uuid版本是否符合格式
def version_uuid(uuid_str):
    try:
        return uuid.UUID(uuid_str).version
    except ValueError:
        return None
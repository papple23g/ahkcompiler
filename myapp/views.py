from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.http import FileResponse
import logging
import os
import subprocess
import uuid
import time
from pathlib import Path

logger=logging.getLogger(__name__)

#編譯器目錄(絕對路徑,避免 Windows 在 shell=False 時不依 cwd 尋找執行檔)
COMPILER_DIR=Path(__file__).resolve().parent.parent/"ahkfile1_30"
COMPILE_TIMEOUT_SECONDS=30

def homepage(req):
    return HttpResponse("home page.")

def ahk_webpage(req: HttpRequest, subpage: str) -> HttpResponse:
    response = render(req,"ahk_webpage.html",{'subpage':subpage})
    if subpage == 'ahkblockly':
        # Preserve the opener connection used by Disqus social-login popups.
        response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
    return response

#定義API:執行AHK編譯為EXE檔
def cp(req):
    req_body=req.body.decode()
    ahk_code=req_body
    linebreak_index=ahk_code.find('\n')
    os_type=ahk_code[:linebreak_index+1]
    ahk_code='#SingleInstance force\n'+ahk_code
    filename_key=uuid.uuid4()
    ahk_path=COMPILER_DIR/f"{filename_key}.ahk"
    exe_path=COMPILER_DIR/f"{filename_key}.exe"
    #撰寫ahk檔案
    with open(ahk_path,'w',encoding="utf-8-sig") as f:
        f.write(ahk_code)
    #執行編譯
    # if '64-bit' in os_type:
    cmd_args=[str(COMPILER_DIR/"Ahk2Exe.exe"),"/in",ahk_path.name,"/out",exe_path.name,"/bin","Unicode 64-bit.bin","/mpress","1"]
    # else:
    #     cmd_args=[str(COMPILER_DIR/"Ahk2Exe.exe"),"/in",ahk_path.name,"/out",exe_path.name,"/bin","Unicode 32-bit.bin","/mpress","1"]
    try:
        subprocess.run(cmd_args,cwd=COMPILER_DIR,shell=False,check=True,timeout=COMPILE_TIMEOUT_SECONDS,capture_output=True)
        if not exe_path.is_file() or exe_path.stat().st_size==0:
            raise RuntimeError("compiler produced no output file")
    except (subprocess.SubprocessError,OSError,RuntimeError):
        logger.exception("AHK compile failed for %s",filename_key)
        for filepath in (ahk_path,exe_path):
            filepath.unlink(missing_ok=True)
        return HttpResponse("compile failed",status=500)
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
        return HttpResponseRedirect("https://papple23g-ahkcompiler.herokuapp.com/ahkblockly")
    
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
        return HttpResponseRedirect("https://papple23g-ahkcompiler.herokuapp.com/ahkblockly")

#定義檢查函數:uuid版本是否符合格式
def version_uuid(uuid_str):
    try:
        return uuid.UUID(uuid_str).version
    except ValueError:
        return None

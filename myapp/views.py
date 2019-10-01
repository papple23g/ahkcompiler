from django.shortcuts import render
from django.http import HttpResponse
from django.http import FileResponse

def homepage(req):
    html='<p>123</p>'
    return HttpResponse(html)

def dl(req):
    response = FileResponse(open('01.png', 'rb'))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="01.png"'
    return response
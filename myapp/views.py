from django.shortcuts import render
from django.http import HttpResponse

def homepage(req):
    html='<p>123</p>'
    return HttpResponse(html)

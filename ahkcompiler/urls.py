from django.contrib import admin
from django.urls import re_path
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),

    re_path(r'^$', homepage),
    re_path(r'(?P<subpage>ahktool)', ahk_webpage),
    re_path(r'(?P<subpage>ahkblockly)', ahk_webpage),
    re_path(r'(?P<subpage>updateDiary)', ahk_webpage),
    re_path(r'(?P<subpage>about)', ahk_webpage),
    re_path(r'(?P<subpage>faq)', ahk_webpage),


    re_path(r'^dl$', dl),
    re_path(r'^cp$', cp),
    re_path(r'^rm$', rm),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

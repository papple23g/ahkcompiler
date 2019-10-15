from django.conf.urls import url
from django.contrib import admin
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', homepage),
    url(r'(?P<subpage>^ahk.+)',ahk_webpage),


    url(r'^dl$', dl),
    url(r'^cp$', cp),
    url(r'^rm$', rm),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

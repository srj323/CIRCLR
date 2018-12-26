from django.urls import path,re_path,include
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='fileindex'),
    re_path(r'^(?P<file_id>[^/]+)/$', views.filedisplay, name='filedisplay'),
]

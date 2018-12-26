# chat/urls.py
from django.urls import path,re_path,include

from . import views
app_name="chat"
urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    
]

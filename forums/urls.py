from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('', views.index, name='forum-home'),
	path('<slug>',views.forumpage,name='forumpage'),
	path('<forum>/<topic>',views.topicpage,name='topicpage'),
	path('new/', ForumCreateView.as_view(), name='forum-create'),
	path('(?P<slug>[-\w]+)/$/update', ForumUpdateView.as_view(), name='forum-update'),
	path('(?P<slug>[-\w]+)/$/delete', ForumDeleteView.as_view(), name='forum-delete'),
	path('<forum>/new/', TopicCreateView.as_view(), name='topic-create'),
	path('<forum>/(?P<slug>[\w-]+)/update', TopicUpdateView.as_view(), name='topic-update'),
	path('<forum>/(?P<slug>[\w-]+)/delete', TopicDeleteView.as_view(), name='topic-delete'),
	#path('<slug>/new/', views.topic_create_view, name='topic-create'),
	#path('<forum>/<slug>/delete', TopicDeleteView.as_view(), name='topic-delete'),
]
#(?P<slug>[-\w]+)/$
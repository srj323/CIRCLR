from django.urls import path,include,re_path
from api import views
from rest_framework.authtoken import views as authviews
urlpatterns = [
    path('userprofile',views.userprofile,name='userprofile'),
    path('testview',views.testview,name='testview'),
    path('interests',views.interests,name='interests'),
    path('friends',views.friends,name='friends'),
    path('friendrequest',views.friendrequest,name='friendrequest'),
    path('message',views.message,name='message'),
    path('forums',views.forums,name='forums'),
    path('topics',views.topics,name='topics'),
    path('posts',views.posts,name='posts'),
    path('polls',views.polls,name='polls'),
    path('vote',views.vote,name='vote'),
    re_path(r'^api-token-auth/', authviews.obtain_auth_token)
]

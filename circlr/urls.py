"""circlr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from accounts import views as accounts_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import PasswordResetCompleteView

urlpatterns = [
	path('reset/done/', PasswordResetCompleteView.as_view(template_name="accounts/reset_password_complete.html"), name="password_reset_complete"),
    path('admin/', admin.site.urls),
	path('api/',include('api.urls')),
    re_path(r'^accounts/', include('accounts.urls', namespace='accounts')),
    re_path(r'^$', accounts_views.home, name="home"),
    path('', include('django.contrib.auth.urls')),
    path('forums/', include('forums.urls')),
	path('friends/', include('friends.urls'), name="friends"),
    path('polls/', include('polls.urls')),
	re_path(r'^files/', include('files.urls')),
    re_path(r'^chat/', include('chat.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

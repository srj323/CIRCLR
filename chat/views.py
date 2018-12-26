# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import UserProfile
import json
from django.views.decorators.csrf import csrf_exempt
from .logger import *
from .validator import *

@login_required(login_url='/accounts/login/')
def index(request):
    recentlist = get_recents(request.user.username)
    return render(request, 'chat/index.html', {
        'userlist' : User.objects.all(),
        'recentlist':recentlist
    })

@login_required(login_url='/accounts/login/')
def room(request, room_name):
    if roomvalidate(request.user.username,room_name):
        recentlist = get_recents(request.user.username)
        return render(request, 'chat/chatroom.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'message_log':load_log(room_name),
            'userlist' : User.objects.all(),
            'recentlist':recentlist
            })
    else:
        return render(request,'chat/linkbroken.html',{})

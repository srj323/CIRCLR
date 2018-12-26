from django.contrib.auth.models import User
def roomvalidate(username,roomname):
    difference = roomname.replace(username,"",1)
    reconstructed = "".join(sorted([username,difference]))
    userlist =  User.objects.filter(username=difference )
    if roomname == reconstructed and len(userlist):
        return True
    else:
        return False
def receiver_gen(username,roomname):
    return User.objects.filter(username=roomname.replace(username,"",1))[0]

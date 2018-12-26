from django.shortcuts import render,redirect
from .forms import Forms_city,registration_form,Searchu,Searchi
from .models import Friends_Status
from accounts.models import Interest_Model, UserProfile
from django.contrib.auth.models import User
from collections import Counter
from django.http import HttpResponse
from django.db.models import Q
import json
from django.contrib.auth.decorators import login_required
from circlr import settings
from django.core.mail import send_mail
# Create your views here.


@login_required(login_url="/accounts/login")
def sendr(request):
    if request.method == 'POST':
        req=request.POST['req']
        receiver=User.objects.get(username=req)
        response_data={}
        if not Friends_Status.objects.filter(Q(sender=receiver,receiver=request.user,status=False) | Q(sender=request.user,receiver=receiver,status=False)):
            Friends_Status.objects.create(sender=request.user,receiver=receiver,status=False)
            response_data['success']='Friend Request Sent'
            send_mail(
                    'Friend Request',
                    'You have a friend request from '+ request.user.username,
                    settings.EMAIL_HOST_USER,
                    [receiver.email]
                    )
        else:
            response_data['success']='Error Sending Request try to reload the page'

    return HttpResponse(json.dumps(response_data), content_type="application/json")



@login_required(login_url="/accounts/login")
def acceptr(request):
    if request.method == 'POST':
        accept=request.POST['receiver']
        response_data={}
        sender=User.objects.get(username=accept)
        Friends_Status.objects.filter(sender=sender,receiver=request.user,status=False).update(status=True)
        response_data['success']='Friend Request Accepted'
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required(login_url="/accounts/login")
def decliner(request):
    if request.method == 'POST':
        decline=request.POST['receiver']
        option=request.POST['option']
        sender=User.objects.get(username=decline)
        Friends_Status.objects.filter(Q(sender=sender,receiver=request.user) | Q(sender=request.user,receiver=sender)).delete()

        response_data={}

        if option == '0':
            response_data['success']='Friend Request Declined'
        else :
            response_data['success']='UnFriended'
    return HttpResponse(json.dumps(response_data), content_type="application/json")






@login_required(login_url="/accounts/login")
def matching(request):
        form=Searchu(request.POST)
        form1=Searchi(request.POST)

        allusers=Interest_Model.objects.all()
        getfriends1=Friends_Status.objects.filter(sender=request.user, status=True)
        getfriends2=Friends_Status.objects.filter(receiver=request.user, status=True)
        pendingfriends=Friends_Status.objects.filter(receiver=request.user, status=False)
        pendingfriends1=Friends_Status.objects.filter(sender=request.user)
        pendingfriends2=Friends_Status.objects.filter(receiver=request.user)

        filteringbutton=[]
        pendingfrnd=[]
        friends=[]
        for frnd in getfriends1:
            friends.append(frnd.receiver.username)
        for frnd in getfriends2:
            friends.append(frnd.sender.username)
        for frnds in pendingfriends:
            pendingfrnd.append(frnds.sender.username)
        for frnds in pendingfriends2:
            filteringbutton.append(frnds.sender.username)
        for frnd in pendingfriends1:
            filteringbutton.append(frnd.receiver.username)
        suggestionlist=[]
        pendingfrnd=list(set(pendingfrnd))
        #for suggestion finding current user city and interests
        curruser = UserProfile.objects.get(user=request.user)
        if curruser.city!=None:
            suggcitylist = UserProfile.objects.filter(city=curruser.city)
            for userprof in suggcitylist:
                if userprof.user!=request.user:
                    suggestionlist.append(userprof.user)

        curruserinterest=[]
        curruser=User.objects.get(username=request.user.username)

        cr1_interest=Interest_Model.objects.filter(username=curruser)

        for i in cr1_interest:
                curruserinterest.append(i.interest);



        for intrst in curruserinterest:
            suggtemp = Interest_Model.objects.filter(interest=intrst)
            for i in suggtemp:
                if str(i.username) != request.user.username:
                    suggestionlist.append(i.username)


        suggestionlist.sort(key=Counter(suggestionlist).get, reverse=True)
        suggestionlist = [ e
                    for i, e in enumerate(suggestionlist)
                    if suggestionlist.index(e) == i
                ]

        suggestionlist= [x for x in suggestionlist if x.username not in friends]
        print("suggestionlist:->"+str(suggestionlist))


        if form.is_valid():
            text=form.cleaned_data['search_namebyuser']
            list2=[]
            if User.objects.filter(username__icontains=text).count()>0:
                srchuser=User.objects.filter(username__icontains=text)
                for i in srchuser:
                    list2.append(i.username)

            return render(request, 'friends/friendsugg.html', {'userlist':list2,'form':form,'form1':form1,'suggestionlist':suggestionlist, 'friends':friends,'pendingfrnds':pendingfrnd, 'filteringbutton':filteringbutton})

        elif form1.is_valid():
            text1=form1.cleaned_data['search_namebyinterest']
            text1 = text1.lower().replace(","," ").split(" ")
            text1 = list(filter(None, text1))
            list1=[]
            for intrst in text1:
                temp = Interest_Model.objects.filter(interest=intrst)
                for i in temp:
                    if str(i.username) != request.user.username:
                        list1.append(i.username)
            
            list1.sort(key=Counter(list1).get, reverse=True)
            list1 = [ e
                        for i, e in enumerate(list1)
                        if list1.index(e) == i
                    ]



            return render(request, 'friends/friendsugg.html', {'interestlist':list1,'form':form,'form1':form1,'curruserinterest':curruserinterest,'suggestionlist':suggestionlist,'friends':friends,'pendingfrnds':pendingfrnd, 'filteringbutton':filteringbutton})
        args = {'form':form,'form1':form1,'suggestionlist':suggestionlist,'friends':friends,'pendingfrnds':pendingfrnd,'filteringbutton':filteringbutton}
        return render(request, 'friends/friendsugg.html', args)

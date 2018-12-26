from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import *
from friends.models import *
from api.serializers import *
from django.db.models import Q
import json

# Create your views here.
@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def userprofile(request):
    if request.method=='GET':
        username = request.GET.get('username')

        try:
            user = User.objects.get(username=username)
            profile = UserProfile.objects.get(user=user)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        serializer= UserProfileSerializer(profile)
        return JsonResponse(serializer.data,status=200)
    if request.method=='POST':
        username = request.user.username
        if request.POST.get('username')== username:
            user = User.objects.get(username=username)
            profile=UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(profile,request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
        else:
            return HttpResponse(status=403)


def testview(request):
    return HttpResponse("Thhanks")

@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def interests(request):
    if request.method=='GET':
        username = request.GET.get('username')

        try:
            user = User.objects.get(username=username)
            interests = Interest_Model.objects.filter(username=user)
        except User.DoesNotExist:
            return HttpResponse(status=404)
        serializer = InterestSerializer(interests,many=True)
        return JsonResponse(serializer.data,safe=False)


    if request.method=="POST":
        username=request.user.username
        if username == request.POST.get("username"):
            if request.POST.get("mode")=="addinterest":
                serializer = InterestSerializer(data=request.data)
                if serializer.is_valid():
                    try:
                        serializer.save()
                    except Exception as e:
                        print(e)
                        return JsonResponse({"message":"Interest Already Exists"},status=400)
                    return JsonResponse(serializer.data,status=201)
                return JsonResponse(serializer.errors,status=400)

            if request.POST.get("mode")=="removeinterest":
                try:
                    user = User.objects.get(username=username)
                    Interest_Model.objects.filter(username=user,interest=request.POST.get("interest")).delete()
                    return JsonResponse({},status=200)
                except:
                    return JsonResponse({"message":"BAD REQUEST"},status=400)
            return JsonResponse({"message":"BAD MODE"},status=400)
        else:
            return JsonResponse({"message":"Forbidden"},status=403)


@api_view(['GET','POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def friends(request):
    if request.method=='GET':
        username = request.GET.get('username')
        mode = request.GET.get('mode')
        status = lambda mode: True if mode=="c" else False
        if username==request.user.username and (mode=='p' or mode=='c'):
            try:
                user = User.objects.get(username=username)
                friends = Friends_Status.objects.filter(Q(sender=user)|Q(receiver=user)).filter(status= status(mode))
            except User.DoesNotExist:
                return JsonResponse({"Message":"User not found"},status=404)

            serializer = FriendsSerializer(friends,many=True)
            return JsonResponse(serializer.data,safe=False)
        else:
            return JsonResponse({"message":"Forbidden"},status=403)

@api_view(['POST','DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def friendrequest(request):
    if request.method=="POST":
        if request.user.username == request.POST.get("sender"):
            serializer = FriendsSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    return JsonResponse(serializer.data,status=201)
                except Exception as e:
                    print(e)
                    return JsonResponse({"message":"request Already Exists"},status=400)
            return JsonResponse(serializer.errors,status=400)
        return JsonResponse({"message":"Forbidden"},status=403)
    if request.method=="DELETE":
        if request.user.username == request.POST.get("sender"):
            sender = request.POST.get("sender")
            receiver = request.POST.get("receiver")
            try:
                Friends_Status.objects.filter((Q(sender__username=sender)&Q(receiver__username=receiver))|(Q(sender__username=receiver)&Q(receiver__username=sender))).delete()
                return JsonResponse({},status=200)
            except Exception as e:
                print(e)
                return JsonResponse({"message":"BAD REQUEST"},status=400)
        return JsonResponse({"message":"Forbidden"},status=403)

@api_view(['POST','GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def message(request):
    if request.method=="GET":
        sender = request.user.username
        receiver = request.GET.get("uid")
        messages = Message.objects.filter((Q(sender__username=sender)&Q(receiver__username=receiver))|(Q(sender__username=receiver)&Q(receiver__username=sender)))
        serializer = MessageSerializer(messages,many=True)
        return JsonResponse(serializer.data,safe=False)
    if request.method=='POST':
        if request.user.username==request.POST.get("sender"):
            serializer=MessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=201)
            return JsonResponse(serializer.errors,status=400)
        else:
            return JsonResponse({"message":"Forbidden"},status=403)


@api_view(['POST','GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def forums(request):
    if request.method=="GET":
        creatorid=request.GET.get("creatorid")
        forumname = request.GET.get("forumname")
        try:
            forums = Forum.objects.filter((Q(creatorid__username=creatorid)|Q(forumname__contains=forumname)))
            forumlist = Forum.objects.filter(Q(creatorid__username=creatorid)|Q(forumname__contains=forumname))
        except:
            return JsonResponse([],status=200,safe=False)
        print(forumlist)
        for forum in forums:
            if (forum.viewprivacy==3 and request.user.username != forum.creatorid.username):
                forumlist = forumlist.exclude(forumid=forum.forumid)
        serializer = ForumSerializer(forumlist,many=True)
        return JsonResponse(serializer.data,safe=False)
    if request.method=="POST":
        creatorid = request.POST.get("creatorid")
        if creatorid==request.user.username:
            serializer=ForumSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=201)
            return JsonResponse(serializer.errors,status=400)
        return JsonResponse({"message":"Forbidden"},status=403)

@api_view(['POST','GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def topics(request):
    if request.method=="GET":
        forumid = request.GET.get("forumid")
        try:
            topics = Topic.objects.filter(forumid__forumid = forumid)
            topiclist = Topic.objects.filter(forumid__forumid = forumid)
        except:
            return JsonResponse([],status=200,safe=False)
        for topic in topics:
            if (topic.viewprivacy==3 and request.user.username != topic.creatorid.username):
                topiclist = topiclist.exclude(topicid=topic.topicid)
        serializer = TopicSerializer(topiclist,many=True)
        return JsonResponse(serializer.data,safe=False)
    if request.method=="POST":
        creatorid = request.POST.get("creatorid")
        forumid = request.POST.get("forumid")
        if creatorid==request.user.username:
            try:
                if (Forum.objects.get(forumid=forumid).writeprivacy==2 and creatorid != Forum.objects.get(forumid=forumid).creatorid.username):
                    return JsonResponse({"message":"Forbidden"},status=403)
            except:
                return JsonResponse({"message":"Forbidden"},status=403)
            serializer=TopicSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=201)
            return JsonResponse(serializer.errors,status=400)
        return JsonResponse({"message":"Forbidden"},status=403)

@api_view(['POST','GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def posts(request):
    if request.method=="GET":
        topicid = request.GET.get("topicid")
        try:
            posts = Post.objects.filter(topicid__topicid=topicid)
        except:
            return JsonResponse([],status=200,safe=False)
        serializer = PostSerializer(posts,many=True)
        return JsonResponse(serializer.data,safe=False)
    if request.method=="POST":
        creatorid = request.POST.get("creatorid")
        topicid = request.POST.get("topicid")
        if request.user.username == creatorid:
            try:
                if Topic.objects.get(topicid=topicid).writeprivacy==3 and creatorid != Topic.objects.get(topicid=topicid).creatorid.username:
                    return JsonResponse({"message":"Forbidden"},status=403)
            except:
                return JsonResponse({"message":"Forbidden"},status=403)
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=201)
            return JsonResponse(serializer.errors,status=400)
        return JsonResponse({"message":"Forbidden"},status=403)

@api_view(['POST','GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def polls(request):
    if request.method=="GET":
        mode = request.GET.get("query")
        print(mode)
        if mode=='q':
            questions=Question.objects.all()
            serializer = QuestionSerializer(questions,many=True)
            return JsonResponse(serializer.data,safe=False)
        elif mode=='c':
            questionpk = request.GET.get("question")
            if not questionpk:
                return JsonResponse({"message":"Missing question"})
            choices = Choice.objects.filter(question__pk = questionpk)
            serializer = ChoiceSerializer(choices,many=True)
            return JsonResponse(serializer.data,safe=False)
        else:
            return JsonResponse({"message":"bad mode"},status=400)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def vote(request):
    if request.method=="POST":
        questionpk=request.POST.get("question")
        choice = request.POST.get("choice")
        username = request.user.username
        if choice==None or questionpk==None:
            return JsonResponse({"message":"Bad REQUEST"},status=400)
        try:
            choice = Choice.objects.filter(question__pk=questionpk).get(pk=choice)
        except:
            return JsonResponse({"message":"poll/choice not found"},status=404)    
        if choice != None and Voter.objects.filter(user=username,question_id=questionpk).count()==0:
            choice.votes +=1
            choice.save()
            Voter.objects.create(user=username,question_id=str(questionpk))
            return JsonResponse({},status=200)
        return JsonResponse({"message":"Forbidden"},status=403)

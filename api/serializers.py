from rest_framework import serializers
from accounts.models import *
from friends.models import *
from chat.models import *
from forums.models import *
from polls.models import *
from chat.logger import roomname_gen
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import IntegrityError

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = UserProfile
        fields = ('username','bio','city')

    def update(self,instance,validated_data):
        instance.bio = validated_data.pop('bio')
        instance.city = validated_data.pop('city')
        instance.save()
        return instance


class InterestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='username.username')

    class Meta:
        model = Interest_Model
        fields=('username','interest')

    def create(self,validated_data):
        username = validated_data.pop('username').pop('username')
        interestdata = validated_data.pop('interest')
        user = User.objects.get(username=username)
        if Interest_Model.objects.filter(username=user,interest=interestdata).count()>0:
            raise IntegrityError
        interestobject = Interest_Model.objects.create(username=user,interest=interestdata)
        interestobject.save()

        return interestobject




class FriendsSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')
    receiver = serializers.CharField(source='receiver.username')
    friendstatus=serializers.BooleanField(source='status')
    class Meta:
        model = Friends_Status
        fields=('sender','receiver','friendstatus')

    def create(self,validated_data):
        sender=validated_data.pop("sender").pop("username")
        receiver=validated_data.pop("receiver").pop("username")
        status = validated_data.pop("status")
        if sender==receiver:
            raise IntegrityError
        if status==False:
            if Friends_Status.objects.filter((Q(sender__username=sender)&Q(receiver__username=receiver))|(Q(sender__username=receiver)&Q(receiver__username=sender))).count()==0:
                friendsobject = Friends_Status.objects.create(sender=User.objects.get(username=sender),receiver=User.objects.get(username=receiver),status=False)
                return friendsobject
            else:
                raise IntegrityError
        else:
            friendsobject = Friends_Status.objects.filter(sender__username=receiver,receiver__username=sender)
            friendsobject.update(status=True)

        return friendsobject[0]

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')
    receiver = serializers.CharField(source='receiver.username')
    class Meta:
        model = Message
        fields=('sender','receiver','message','timestamp')
        read_only_fields = ('timestamp',)

    def create(self,validated_data):
        sender = validated_data.pop("sender").pop("username")
        receiver = validated_data.pop("receiver").pop("username")
        message = validated_data.pop("message")
        messageobject = Message.objects.create(sender=User.objects.get(username=sender),receiver=User.objects.get(username=receiver),message=message,roomname=roomname_gen(sender,receiver))
        return messageobject


class ForumSerializer(serializers.ModelSerializer):
    creatorid = serializers.CharField(source="creatorid.username")
    class Meta:
        model=Forum
        fields = ('forumid','creatorid','forumname','description','viewprivacy','writeprivacy','createdate')
        read_only_fields=('createdate',)

    def create(self,validated_data):
        creatorid = validated_data.pop("creatorid").pop("username")
        forumname = validated_data.pop("forumname")
        description = validated_data.pop("description")
        viewprivacy = validated_data.pop("viewprivacy")
        writeprivacy = validated_data.pop("writeprivacy")
        forumobject = Forum.objects.create(creatorid = User.objects.get(username=creatorid),forumname=forumname,description=description,viewprivacy=viewprivacy,writeprivacy=writeprivacy)
        return forumobject

class TopicSerializer(serializers.ModelSerializer):
    creatorid = serializers.CharField(source="creatorid.username")
    forumid=serializers.CharField(source="forumid.forumid")
    class Meta:
        model = Topic
        fields = ('topicid','creatorid','forumid','topicname','description','viewprivacy','writeprivacy','createdate')
        read_only_fields=('createdate',)

    def create(self,validated_data):
        creatorid = validated_data.pop("creatorid").pop("username")
        forumid = validated_data.pop("forumid").pop("forumid")
        topicname = validated_data.pop("topicname")
        description = validated_data.pop("description")
        viewprivacy = validated_data.pop("viewprivacy")
        writeprivacy = validated_data.pop("writeprivacy")
        topicobject = Topic.objects.create(creatorid=User.objects.get(username=creatorid),forumid=Forum.objects.get(forumid=forumid),topicname=topicname,description=description,viewprivacy=viewprivacy,writeprivacy=writeprivacy)
        return topicobject

class PostSerializer(serializers.ModelSerializer):
    creatorid = serializers.CharField(source="creatorid.username")
    topicid = serializers.CharField(source="topicid.topicid")
    class Meta:
        model = Post
        fields = ('postid','creatorid','topicid','content','createdate')
        read_only_fields = ('createdate',)

    def create(self,validated_data):
        creatorid = validated_data.pop("creatorid").pop("username")
        topicid=validated_data.pop("topicid").pop("topicid")
        content = validated_data.pop('content')
        postobject = Post.objects.create(creatorid = User.objects.get(username=creatorid),topicid=Topic.objects.get(topicid=topicid),content=content)
        return postobject




class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('pk','question_text','pub_date')
        read_only_fields=('pk',)

class ChoiceSerializer(serializers.ModelSerializer):
    questionpk = serializers.IntegerField(source = 'question.pk')
    class Meta:
        model = Choice
        fields = ('pk','questionpk','choice_text','votes')
        read_only_fields = ('pk',)

from django.test import TestCase,Client
from django.contrib.auth.models import User
from friends.models import Friends_Status
# Views Testing
class TestSearching(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="testuser1", email="testuser1002@ts.com", password="Hello World")
        self.user2 = User.objects.create(username="testuser2", email="testuser2002@ts.com", password="Hello World")
        self.client=Client()

    def test_searchbyusername(self):
        self.client.force_login(self.user1)
        response = self.client.post('/friends/matching/',{"search_namebyuser":"muk"})
        self.assertEqual(response.status_code, 200)

    def test_searchbyinterest(self):
        self.client.force_login(self.user1)
        response = self.client.post('/friends/matching/',{"search_namebyinterest":"networking,singing"})
        self.assertEqual(response.status_code, 200)

    def test_if_user_not_logeed_in(self):
        response = self.client.get('/friends/matching/',{"search_namebyuser":"muk"})
        self.assertEqual(response.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user1)
        response = self.client.get('/friends/matching/')
        self.assertEqual(response.status_code, 200)

class Testfriendrequests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="testuser1", email="testuser1002@ts.com", password="Hello World")
        self.user2 = User.objects.create(username="testuser2", email="testuser2002@ts.com", password="Hello World")
        self.client=Client()

    def test_sendingrequest(self):
        self.client.force_login(self.user1)
        response = self.client.post('/friends/sendr/',{"req":"testuser2"})
        user2=User.objects.get(username="testuser2")
        self.assertEqual(Friends_Status.objects.filter(sender=self.user1,receiver=user2,status=False).count(),1)
        friend_object=Friends_Status.objects.filter(sender=self.user1,receiver=user2,status=False)[0]
        self.assertEqual(friend_object.sender,self.user1)
        self.assertEqual(response.status_code, 200)

    def test_acceptingingrequest(self):
        self.client.force_login(self.user1)
        sendresponse = self.client.post('/friends/sendr/',{"req":"testuser2"})
        friend_object=Friends_Status.objects.filter(sender=self.user1,receiver=self.user2)[0]
        friend1_status=(friend_object.sender,friend_object.receiver,friend_object.status)
        result1=(self.user1,self.user2,False)
        self.assertEqual(friend1_status,result1)
        self.assertEqual(sendresponse.status_code, 200)

        self.client.force_login(self.user2)
        response = self.client.post('/friends/acceptr/',{"receiver":"testuser1"})
        friend_object=Friends_Status.objects.filter(sender=self.user1,receiver=self.user2)[0]
        self.assertEqual(friend_object.status,True)
        self.assertEqual(response.status_code, 200)

    def test_declingrequest(self):
        self.client.force_login(self.user1)
        sendresponse = self.client.post('/friends/sendr/',{"req":"testuser2"})
        friend_object=Friends_Status.objects.filter(sender=self.user1,receiver=self.user2)[0]
        friend1_status=(friend_object.sender,friend_object.receiver,friend_object.status)
        result1=(self.user1,self.user2,False)
        self.assertEqual(friend1_status,result1)
        self.assertEqual(sendresponse.status_code, 200)

        self.client.force_login(self.user2)
        response = self.client.post('/friends/decliner/',{"receiver":"testuser1","option":'0'})
        friend_object=Friends_Status.objects.filter(sender=self.user1,receiver=self.user2).count()
        self.assertEqual(friend_object,0)
        self.assertEqual(response.status_code, 200)

    def test_Unfriending(self):
        self.client.force_login(self.user1)
        sendresponse = self.client.post('/friends/sendr/',{"req":"testuser2"})
        friend_object=Friends_Status.objects.filter(sender=self.user1,receiver=self.user2)[0]
        friend1_status=(friend_object.sender,friend_object.receiver,friend_object.status)
        result1=(self.user1,self.user2,False)
        self.assertEqual(friend1_status,result1)
        self.assertEqual(sendresponse.status_code, 200)

        self.client.force_login(self.user2)
        acceptresponse = self.client.post('/friends/acceptr/',{"receiver":"testuser1"})
        friend_object=Friends_Status.objects.filter(sender=self.user1,receiver=self.user2)[0]
        self.assertEqual(friend_object.status,True)
        self.assertEqual(acceptresponse.status_code, 200)

        response = self.client.post('/friends/decliner/',{"receiver":"testuser1","option":'1'})
        friend_object=Friends_Status.objects.filter(sender=self.user1,receiver=self.user2).count()
        self.assertEqual(friend_object,0)
        self.assertEqual(response.status_code, 200)

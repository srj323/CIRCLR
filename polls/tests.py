import datetime

from django.utils import timezone
from django.test import TestCase , Client
from django.urls import reverse
from django.test.utils import override_settings
from django.core import mail
from .models import *
class QuestionModelTest(TestCase):
    """
    def setUp(self):
        self.name = Question.objects.create(question_text="Which is Best",pub_date=datetime.datetime.now)
        """
    def Create_Model(self):
        #name = self.name
        return Question.objects.create(question_text="Which is Best",pub_date=datetime.datetime.now())
    def test_model_creation(self):
        x = self.Create_Model()
        self.assertTrue(isinstance(x,Question))
        self.assertEqual(x.__str__(),x.question_text)
class ChoiceModelTest(TestCase):
    """
    def setUp(self):
        self.name = Choice.objects.create(choice_text="Apple",votes=10)
        """
    def Create_Model(self):
        #name = self.name
        return Choice.objects.create(question_id=2,choice_text="Apple",votes=10)
    def test_model_creation(self):
        x = self.Create_Model()
        self.assertTrue(isinstance(x,Choice))
class VoterModelTest(TestCase):
    """
    def setUp(self):
        self.name = Voter.objects.create(user="testuser",question_id=1)
        """
    def Create_Model(self):
        #name = self.name
        return Voter.objects.create(user="testuser" , question_id=2)
    def test_model_creation(self):
        x = self.Create_Model()
        self.assertTrue(isinstance(x,Voter))

#----------------------------------------------------URLS TESTING-------------------------------------------------------

"""
class BlankUrlTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_anonymous_ping(self):
        response = self.client.get('')
        print(response)
        self.assertRedirects(response,expected_url='/')
class IndexTest(TestCase):
    def setUp(self):
        self.client = Client()
    def test_anonymous_ping(self):
        response = self.client.get('')
        self.assertRedirects(response,expected_url='/')
"""
def create_question(question_text,published):
    return Question.objects.create(question_text=question_text,pub_date=datetime.datetime.now())

class IndexView(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser1",email="testuser@mail.com",password="Hi Guys")

    def test_index_view_with_no_question(self):
        c = Client
        self.client.force_login(self.user)
        question_list = Question.objects.all()
        url = reverse('polls:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        #self.assertContains(response,"No Polls Available")

class DetailView(TestCase):
    def test_detail_with_question(self):
        question = create_question(question_text="Which is Best",published=datetime.datetime.now())
        url = reverse('polls:detail',args=(question.id,))
        response = self.client.get(url)
        print(response)
        self.assertContains(response,question.question_text)


class PollTest(TestCase):

    def test_voting(self):
        client = Client()
        Question.objects.create(question_text="Which is Best", pub_date=datetime.datetime.now())
        Choice.objects.create(question_id=1,choice_text="Choice1",votes=0)
        # Perform a vote on the poll by mocking a POST request.
        response = client.post('/polls/1/vote/', {'choice': '1',})
        # In the vote view we redirect the user, so check the
        # response status code is 302.
        self.assertEqual(response.status_code, 302)
        # Get the choice and check there is now one vote.
        choice = Choice.objects.get(pk=1)
        self.assertEqual(choice.votes, 1)

class QuestionTest(TestCase):
    client = Client()
    def test_questions_details_submitted(self):
        question_text = Question.objects.create(question_text="Which is Best")
        pub_date = Question.objects.create(pub_date=datetime.datetime.now())
        no_of_choices = 3
        response = self.client.post('/polls/questions/',{'question': question_text , 'dateandtime':datetime.datetime.date , 'number':no_of_choices})
        self.assertEqual(response.status_code,200)
    """
    def test_missing_question(self):
        question_text = Question.objects.create(question_text="Which is Best")
        pub_date = Question.objects.create(pub_date=datetime.datetime.now())
        no_of_choices = 3
        response = self.client.post('/polls/questions/',
                                    {'dateandtime': datetime.datetime.date,
                                     'number': no_of_choices})
        self.assertEqual(response.status_code,302)

class ChoiceUrlTest(TestCase):
    client = Client()
    def test_choice_url(self):
        question_text = Question.objects.create(question_text="Hello Django Star")
        no_of_choices = 3
        response = self.client.post('/polls/choices/',{'question': question_text , 'dateandtime':datetime.datetime.date, 'number':no_of_choices})
        self.assertEqual(response.status_code,200)
        
        """
@override_settings(EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' )
class EmailTest(TestCase):
    def test_send_email(self):
        mail_sent_success = mail.send_mail('Subject here',
                       'Here is the message.',
                       'puppalahrithik2000@gmail.com', ['hrithik.p17@iiits.in'],
                       fail_silently=False)
        self.assertEquals(mail_sent_success,1)


class VoterTest(TestCase):
    Voter.objects.create(user="testuser1", question_id=1)
    Voter.objects.create(user="testuser2", question_id=2)
    Voter.objects.create(user="testuser3", question_id=3)
    def test_search_voter(self):
        self.assertTrue(Voter.objects.filter(question_id=1,user="testuser1").exists)
"""
class TestUrls(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser1",email="testuser@mail.com",password="Hi Guys")

    def test_(self):
        c = Client
        self.client.force_login(self.user)
"""

class TestViews(TestCase):

    def test_results_view_with_a_question_with_choices(self):
        question_with_choices = Question.objects.create(question_text="Hey Django User!")
        response = self.client.get(reverse('polls:results',
                                           args=(question_with_choices.id,)))
        self.assertEqual(response.status_code, 200)


    def test_detail_view_with_a_question_with_choices(self):
        question_with_choices = Question.objects.create(question_text="hey user !!")

        response = self.client.get(reverse('polls:detail',
                                   args=(question_with_choices.id,)))
        self.assertContains(response, question_with_choices.question_text,
                            status_code=200)

class QuestionViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser1", email="testuser@mail.com", password="Hi Guys")

    def test_index_view_with_no_question(self):
        c = Client
        self.client.force_login(self.user)
        question_list = Question.objects.all()
        """
            If no questions exist, an appropriate message should be displayed.
            """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_return_message(self):
        c = Client
        self.client.force_login(self.user)
        question_list = Question.objects.all()
        """
            If no questions exist, an appropriate message should be displayed.
            """
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")


class QuestionVoteTests(TestCase):
    def test_vote_method_without_select_choice(self):
        question = Question.objects.create(question_text="A question.")
        response = self.client.get(reverse('polls:vote',
                                   args=(question.id,)))
        self.assertIsNotNone(response.context['error_message'])

    def test_vote_method(self):
        question = Question.objects.create(question_text="A question.")
        choice = Choice.objects.create(question_id=1,choice_text="Hello",votes=0)
        choice = question.choice_set.get(pk=1)
        response = self.client.post(reverse('polls:vote',
                                            args=(question.id,)),
                                    data={'choice': choice.id})
        self.assertGreater(question.choice_set.get(pk=1).votes, choice.votes)
        self.assertRedirects(response,
                             expected_url=reverse('polls:results',
                                                  args=(question.id,)))


    def test_index_view_with_two_questions(self):
        Question.objects.create(question_text="poll qsn 1.")
        Question.objects.create(question_text="Poll qsn 2.")
        response = self.client.get(reverse('polls:index'))
        p = len(Question.objects.all())
        self.assertEqual(p,2)

    def test_index_view_with_no_polls(self):
        response = self.client.get(reverse('polls:index'))
        p = len(Question.objects.all())
        self.assertEqual(p,0)
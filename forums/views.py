from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import CreateTopicForm, CreatePostForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User


def index(request):
	latest_forums = Forum.objects.order_by('-createdate')
	context = {'latest_forums':latest_forums}
	return render(request, 'forums/index.html', context)

def forumpage(request, slug):
	curr_forum = get_object_or_404(Forum, slug=slug)
	if curr_forum.viewprivacy == 1 or curr_forum.viewprivacy == 2 and request.user.is_authenticated or curr_forum.viewprivacy == 3 and request.user == curr_forum.creatorid:
		alltopics = curr_forum.topic_set.order_by('-createdate')
		context = {'topics':alltopics, 'forum':curr_forum}
		return render(request, 'forums/forum.html', context)
	else:
		return HttpResponse("<b>Nice try Loser!</b>")

def topicpage(request, forum, topic):
	curr_forum = get_object_or_404(Forum, slug=forum)
	curr_topic = get_object_or_404(Topic, slug=topic)
	if curr_forum.viewprivacy == 1 or curr_forum.viewprivacy == 2 and request.user.is_authenticated or curr_forum.viewprivacy == 3 and request.user == curr_forum.creatorid:
		if curr_topic.viewprivacy == 1 or curr_topic.viewprivacy == 2 and request.user.is_authenticated or curr_topic.viewprivacy == 3 and request.user == curr_topic.creatorid:
			allposts = curr_topic.post_set.all()
			postform = CreatePostForm()
			if request.method == 'POST':
				postform = CreatePostForm(request.POST)
				if postform.is_valid():
					finaldata = postform.cleaned_data
					if request.user.is_authenticated:
						finaldata['creatorid'] = request.user
					else:
						finaldata['creatorid'] = None
					finaldata['topicid'] = curr_topic
					Post.objects.create(**finaldata)
					return redirect('topicpage', forum, topic)
			context = {'posts':allposts, 'forum':curr_forum, 'topic':curr_topic, 'form':postform}
			return render(request, 'forums/topic.html', context)
		else:
			return HttpResponse("<b>Nice try Loser!</b>")
	else:
		return HttpResponse("<b>Nice try Loser!</b>")

class ForumCreateView(LoginRequiredMixin, CreateView):
	model = Forum
	fields = ['forumname', 'viewprivacy' , 'writeprivacy' , 'description']
	def form_valid(self, form):
		form.instance.creatorid = self.request.user
		return super().form_valid(form)

class ForumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Forum
	fields = ['forumname', 'viewprivacy' , 'writeprivacy' , 'description']
	def form_valid(self, form):
		form.instance.creatorid = self.request.user
		return super().form_valid(form)
	def test_func(self):
		forum = self.get_object()
		if self.request.user == forum.creatorid:
			return True
		return False

class ForumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Forum
	success_url = '/forums'
	def test_func(self):
		forum = self.get_object()
		if self.request.user == forum.creatorid:
			return True
		return False

class TopicCreateView(LoginRequiredMixin, CreateView):
	model = Topic
	fields = ['topicname', 'viewprivacy' , 'writeprivacy' , 'description']
	def dispatch(self, request, *args, **kwargs):
		if request.method.lower() in self.http_method_names:
				handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
		else:
				handler = self.http_method_not_allowed
		self.request = request
		self.args = args
		self.kwargs = kwargs
		return handler(request, *args, **kwargs)
	def form_valid(self, form):
		form.instance.creatorid = self.request.user
		form.instance.forumid = Forum.objects.get(slug=self.kwargs['forum'])
		return super().form_valid(form)

class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Topic
	fields = ['topicname', 'viewprivacy' , 'writeprivacy' , 'description']
	def dispatch(self, request, *args, **kwargs):
		if request.method.lower() in self.http_method_names:
				handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
		else:
				handler = self.http_method_not_allowed
		self.request = request
		self.args = args
		self.kwargs = kwargs
		return handler(request, *args, **kwargs)
	def form_valid(self, form):
		form.instance.creatorid = self.request.user
		form.instance.forumid = Forum.objects.get(slug=self.kwargs['forum'])
		return super().form_valid(form)
	def test_func(self):
		topic = self.get_object()
		if self.request.user == topic.creatorid:
			return True
		return False

class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Topic
	def get_success_url(self):
		topic = self.get_object()
		return reverse('forumpage', kwargs={'slug':topic.forumid.slug})
	def test_func(self):
		topic = self.get_object()
		if self.request.user == topic.creatorid:
			return True
		return False
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify

class Forum(models.Model):
	forumid = models.AutoField(primary_key=True, verbose_name='ID')
	forumname = models.CharField(max_length=30 , verbose_name= ('Name'))
	createdate = models.DateTimeField(default=timezone.now , verbose_name= ('Date Created'))
	creatorid = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name= ('Creator'))
	viewprivacy = models.IntegerField(choices =((1, "Everyone"),
												(2, "People who are logged in."),
												(3, "Only You")),default=1, verbose_name= ('Who can view this forum'))
	writeprivacy = models.IntegerField(choices =((1,"People who are logged in"),
												(2,"Only You")),default=1, verbose_name= ('Who can create topics in this forum'))
	description = models.TextField(blank=True, null=True , verbose_name= ('Description'))
	slug = models.SlugField(('slug'), max_length=60, blank=True, unique=True)
	def __str__(self):
		return self.forumname
	def get_absolute_url(self):
		return reverse('forumpage', kwargs={'slug':self.slug})
	def save(self, *args, **kwargs):
		if not self.forumid:
			self.slug = slugify(self.forumname)+'-by-'+slugify(self.creatorid.username)+'-at-'+slugify(str(self.createdate)[-21:-13])+'-on-'+slugify(str(self.createdate)[:-22])
		if self.viewprivacy>self.writeprivacy+1:
			self.writeprivacy = self.viewprivacy-1
		super(Forum, self).save(*args, **kwargs)
	#forumimage
	#topics
	#subscribers

class Topic(models.Model):
	topicid = models.AutoField(primary_key=True, verbose_name= ('ID'))
	topicname = models.CharField(max_length=50, verbose_name= ('Name'))
	createdate = models.DateTimeField(default=timezone.now , verbose_name= ('Date Created'))
	creatorid = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name= ('Creator'))
	viewprivacy = models.IntegerField(choices =((1, "Everyone"),
												(2, "People who are logged in."),
												(3, "Only You")),default=1, verbose_name= ('Who can view this topic'))
	writeprivacy = models.IntegerField(choices =((1,"Everyone"),
												(2, "People who are logged in."),
												(3,"Only You")),default=1, verbose_name= ('Who can post in this topic'))
	#viewcount = models.IntegerField(default=0)
	forumid = models.ForeignKey(Forum, on_delete=models.CASCADE)
	description = models.TextField(blank=True, null=True , verbose_name= ('Description'))
	slug = models.SlugField(('slug'), max_length=60, blank=True, unique=True)
	def __str__(self):
		return self.topicname
	def save(self, *args, **kwargs):
		if not self.topicid:
			self.slug = slugify(self.topicname)+'-by-'+slugify(self.creatorid.username)+'-at-'+slugify(str(self.createdate)[-21:-13])+'-on-'+slugify(str(self.createdate)[:-22])
		if int(self.forumid.viewprivacy) > int(self.viewprivacy):
			self.viewprivacy=str(self.forumid.viewprivacy)
		if int(self.viewprivacy) > int(self.writeprivacy):
			self.writeprivacy = self.viewprivacy
		super(Topic, self).save(*args, **kwargs)
	def get_absolute_url(self):
		return reverse('topicpage', kwargs={'forum':self.forumid.slug, 'topic':self.slug})

class Post(models.Model):
	postid = models.AutoField(primary_key=True, verbose_name= ('ID'))
	createdate = models.DateTimeField(default=timezone.now, verbose_name= ('Date Created'))
	creatorid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name= ('Creator'), null=True, blank=True)
	topicid = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name= ('Topic'))
	content = models.TextField(verbose_name= ('Content'))
	def __str__(self):
		return self.content
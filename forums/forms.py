from django import forms
from django.utils import timezone

class CreateTopicForm(forms.Form):
	topicname = forms.CharField(label = "Name",max_length = 50)
	viewprivacy = forms.ChoiceField(choices =((1, "Public"),
												(2, "Group"),
												(3, "Private")),initial=1,label = "View Privacy")
	writeprivacy = forms.ChoiceField(choices =((1, "Public"),
												(2, "Group"),
												(3, "Private")),initial=1,label = "Write/Edit Privacy")
	description = forms.CharField(widget = forms.Textarea, label = "Description", required= False)

class CreatePostForm(forms.Form):
	content = forms.CharField(widget = forms.Textarea(attrs={'class':'posttext','style':'width:90%','rows':3}), label = "")
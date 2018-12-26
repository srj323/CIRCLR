from django import forms
from friends.models import Friends_Status
from accounts.models import Interest_Model
from django.contrib.auth.models import User



class registration_form(forms.ModelForm):


    class Meta:
        model=User
        fields=['username','first_name','last_name','email',]


class Forms_city(forms.ModelForm):

    class Meta:
        model=Interest_Model
        exclude = ['username',]

class Searchu(forms.Form):
    search_namebyuser = forms.CharField(max_length=100, required=True)
class Searchi(forms.Form):
    search_namebyinterest = forms.CharField(max_length=100, required=True)

from project.SHIRPI.models import Comment
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.forms.widgets import HiddenInput, Textarea


class CommentForm(ModelForm):
	comment = forms.CharField(widget=Textarea())
	cleanliness = forms.IntegerField(widget=HiddenInput)
	food_quality = forms.IntegerField(widget=HiddenInput)
	atmosphere = forms.IntegerField(widget=HiddenInput)
	wait_time = forms.IntegerField(widget=HiddenInput)
	class Meta:
		model = Comment
		exclude = ('restaurant', 'author', 'id', 'combined', 'created', 'last_modified')

class ProfileForm(ModelForm):
	class Meta:
		model = User
		

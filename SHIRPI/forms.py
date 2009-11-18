from project.SHIRPI.models import Comment
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.forms.widgets import HiddenInput, Textarea


class CommentForm(ModelForm):
	comment = forms.CharField(widget=Textarea())
	cleanliness = forms.IntegerField(initial="0", widget=HiddenInput)
	food_quality = forms.IntegerField(initial="0", widget=HiddenInput)
	atmosphere = forms.IntegerField(initial="0", widget=HiddenInput)
	wait_time = forms.IntegerField(initial="0", widget=HiddenInput)
	class Meta:
		model = Comment
		exclude = ('restaurant', 'author', 'id', 'combined', 'created', 'last_modified')

class ProfileForm(forms.Form):
	old_password = forms.CharField(widget = forms.PasswordInput(render_value=False))
	new_password = forms.CharField(widget = forms.PasswordInput(render_value=False))
	password_again = forms.CharField(widget = forms.PasswordInput(render_value=False))
	email = forms.CharField()
#	address = forms.CharField()

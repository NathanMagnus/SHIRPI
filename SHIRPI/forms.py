from project.SHIRPI.models import Comment
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.forms.widgets import HiddenInput, Textarea

'''
Class		: CommentForm
Description	: the form for a comment, based upon the comment model
'''
class CommentForm(ModelForm):
	comment = forms.CharField(widget=Textarea(), required=False)
	cleanliness = forms.IntegerField(initial="0", widget=HiddenInput)
	food_quality = forms.IntegerField(initial="0", widget=HiddenInput)
	atmosphere = forms.IntegerField(initial="0", widget=HiddenInput)
	overall = forms.IntegerField(initial="0", widget=HiddenInput)
	class Meta:
		model = Comment
		exclude = ('restaurant', 'author', 'id', 'combined', 'created', 'last_modified', 'ip')

'''
Class		: ProfileForm
Description	: the form for editing a profile - based upon the UserProfile model
'''
class ProfileForm(forms.Form):
	old_password = forms.CharField(widget = forms.PasswordInput(render_value=False), required=True)
	new_password = forms.CharField(widget = forms.PasswordInput(render_value=False), required=False)
	password_again = forms.CharField(widget = forms.PasswordInput(render_value=False), required=False)
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)

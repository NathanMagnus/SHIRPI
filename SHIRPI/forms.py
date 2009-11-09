from project.SHIRPI.models import Comment
from django.contrib.auth.models import User
from django.forms import ModelForm

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('restaurant', 'author', 'id', 'combined', 'created', 'last_modified')

class ProfileForm(ModelForm):
	class Meta:
		model = User

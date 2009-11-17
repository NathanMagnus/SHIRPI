from project.SHIRPI.models import Comment
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.widgets import HiddenInput, Textarea


class CommentForm(ModelForm):
	comment = forms.CharField(widget=Textarea())
	cleanliness = PositiveSmallIntegerField()
	food_quality = PositiveSmallIntegerField()
	atmosphere = PositiveSmallIntegerField()
	wait_time = PositiveSmallIntegerField()
	class Meta:
		model = Comment
		exclude = ('restaurant', 'author', 'id', 'combined', 'created', 'last_modified')

class ProfileForm(ModelForm):
	class Meta:
		model = User
		

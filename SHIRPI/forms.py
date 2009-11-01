from project.SHIRPI.models import Comment
from django.forms import ModelForm

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		exclude = ('restaurant', 'author', 'id', 'combined')

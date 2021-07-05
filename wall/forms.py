from django.forms import ModelForm, Textarea
from .models import Post, Comment


class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['picture']
        labels = {
            "picture": ''
        }


class NewPostForm2(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {
            "content": ''
        }

class PostCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            "content": 'Leave your comment'
        }
        widgets = {
            'content': Textarea(attrs={'rows': 2}),
        }
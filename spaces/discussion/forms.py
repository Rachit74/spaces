from django import forms
from .models import Post, Comment

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'cols': 100, 'placeholder': 'Write a comment...'})
        }
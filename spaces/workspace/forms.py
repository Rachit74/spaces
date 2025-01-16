from django import forms
from .models import Workspace, Post, Comment
from django.contrib.auth.models import User


class WorkspaceCreationForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  # Default to an empty queryset
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Members"
    )

    class Meta:
        model = Workspace
        fields = ['name', 'description', 'members']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract the user from kwargs
        super().__init__(*args, **kwargs)  # Call the parent constructor

        if user:
            # Set the queryset to the users followed by the logged-in user
            # only the users whose profile is in current user follows
            self.fields['members'].queryset = User.objects.filter(profile__in=user.profile.follows.all())

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'cols': 100})
        }
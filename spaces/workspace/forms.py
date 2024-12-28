from django import forms
from .models import Workspace
from django.contrib.auth.models import User


class WorkspaceCreationForm(forms.ModelForm):
    # forms.ModelMultipleChoiceField for choosing multiple members at once, will be changed to show only users that current user follows.
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # Fetch all users
        widget=forms.CheckboxSelectMultiple,  # Allows multiple selections with checkboxes
        required=False,  # Optional field
        label="Members"
    )

    class Meta:
        model = Workspace
        fields = ['name', 'description', 'members']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),  # Adjust textarea size
        }

from django import forms
from .models import Todo

class TodoCreationForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['task', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows':3, 'cols': 50, 'placeholder': 'Max length 500'})
        }
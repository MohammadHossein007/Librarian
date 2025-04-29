from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'نظر خود را وارد کنید...'
            }),
        }

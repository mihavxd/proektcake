from django import forms
from .models import Comment


class ContactForm(forms.Form):
    subject = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'input-txt', 'placeholder': 'Тема'}))
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'class': 'input-txt', 'placeholder': 'Сообщение', "rows": 5}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

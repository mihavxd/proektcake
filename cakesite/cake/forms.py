from django import forms
from django.conf import settings
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from .models import Comment
from django_recaptcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    subject = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'input-txt', 'placeholder': 'Тема'}))
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'class': 'input-txt', 'placeholder': 'Сообщение', "rows": 5}))




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'rating', 'body')
        widgets = {
            'body' : forms.Textarea(attrs={"rows": 5,}),
        }


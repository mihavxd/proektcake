from django import forms
from django.forms import TextInput, DateInput, TimeInput

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'date',
                  'time', 'wish']
        widgets = {
            'phone': TextInput(attrs={'placeholder': '+7 (___) ___-__-__'}),
            'date': DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            'time': TimeInput(format="%mm%hh", attrs={"type": "time"}),
        }

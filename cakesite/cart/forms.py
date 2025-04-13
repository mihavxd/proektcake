from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(2, 8)]
DESERT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 2)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label="Вес")
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class CartAddDesertForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=DESERT_QUANTITY_CHOICES, coerce=int, label="Вес")
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
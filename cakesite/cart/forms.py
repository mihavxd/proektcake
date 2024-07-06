from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(2, 8)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label="Вес")
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

from django import forms


class Form_Order(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    city = forms.CharField(max_length=100)
 
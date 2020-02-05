from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100) 

class Form_Order(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    city = forms.CharField(max_length=100)
    

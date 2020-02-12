from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100) 

class Form_Order(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    city = forms.CharField(max_length=100)

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
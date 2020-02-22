from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMessage
from .generation import GenerationToken
from django.http import Http404


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100) 


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ResetForm(forms.Form):
    email = forms.EmailField()

    def send_email(self, request, recip): 
        sender = settings.EMAIL_HOST_USER  
        gen = GenerationToken()
        token = gen.make_token() 
        request.session[recip] = token
        try:
            user = User.objects.get(email=recip)
        except User.DoesNotExist:
            return False  
        context = {
            'user': user.username,
            'email': recip, 
            'protocol': settings.PROTOCOL, 
            'token': token
        }
        template = get_template('reset/password_reset_email.html')
        html = template.render(context) 
        subject = 'Reset password' 
        email = EmailMessage(subject, html, sender, [recip])  
        email.send()
        return True


class ResetPassword(forms.Form):
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput, 
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False, 
    )



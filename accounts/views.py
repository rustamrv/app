from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse
from .forms import SignUpForm, LoginForm, ResetForm, ResetPassword
from django.views import View


class PasswordReset(View):

    def get(self, request, *args, **kwargs):  
        email = kwargs['email']
        token = kwargs['token'] 
        my_t = request.session[email] 
        if token == my_t:
            del request.session[email]
            form = ResetPassword(request.GET)
            return render(request, 'reset/password_reset_confirm.html',  {'form': form})            

        return HttpResponse('Token error. Please repeat.')


class SignUp(View):

    def get(self, request, *args, **kwargs): 
        form = SignUpForm() 
        return render(request, 'registration/signup.html', {'form': form}) 

    def post(self, request, *args, **kwargs): 
        form = SignUpForm(request.POST)
        if form.is_valid(): 
            user = form.save()
            auth_login(request, user)
            return redirect('home') 
        else:
            return HttpResponse("Error " + form.errors)
     
class LoginIn(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request, *args, **kwargs): 
        form = LoginForm(request.POST)
        if form.is_valid(): 
            cd = form.cleaned_data
            user = authenticate(username=cd['login'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login') 
  

class ResetEmail(View):

    def get(self, request, *args, **kwargs):
       form = ResetForm()
       return render(request, 'reset/password_reset.html', {'form': form})

    def post(self, request, *args, **kwargs): 
        form = ResetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            recip = cd['email']
            result = form.send_email(request, recip)
            if result:
                return render(request, 'reset/password_reset_done.html')
            return HttpResponse('Error email. Not found user')
        else:
            return HttpResponse('Invalid email')   
         

"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('mysite.urls'), name='home'),
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', accounts_views.signup, name='login'),
    
    path('reset/', auth_views.PasswordResetView.as_view(
                template_name='reset/password_reset.html',
                email_template_name='reset/password_reset_email.html',
                subject_template_name='reset/password_reset_subject.txt'
            ),
            name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='reset/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<username>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='reset/password_reset_confirm.html'),
            name='password_reset_confirm'),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='reset/password_reset_complete.html'),
        name='password_reset_complete'),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

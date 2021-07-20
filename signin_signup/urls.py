from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
   
    # path('register', registrationForm, name='register'),
    # path('save/', registration_form_save),
    # path('login/', loginForm, name='login'),
    path('login/login/', Login_auth),
    path('logout/',logoutSession, name='logout'),
    # path('login/register/', registrationForm),
    path('register/', registrationPage, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="Login.html"), name = 'login'),
    
    
]
from django.shortcuts import render
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import redirect
from django.db import IntegrityError
from client.views import Channel
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm

# Create your views here.

def registrationForm(request):
    return render(request,'Register.html')
    

def Login_auth(request):
    if request.method == "GET":
        return render(request,'Login.html')
    else:
        auth_user = authenticate(username=request.POST['authusername'], password=request.POST['authpassword'])   
        if auth_user is not None:
            login(request, auth_user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
            
def logoutSession(request):
    logout(request)
    return redirect('/')
        

# This is first method
def registrationPage(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to login.')
            channel = Channel(name=username)
            channel.save()
            return redirect('login')
            
    else:   
        # form = UserCreationForm()
        form = UserRegistrationForm()
    return render(request, 'Register.html', {'form':form})




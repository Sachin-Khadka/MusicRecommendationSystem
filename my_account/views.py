from django.shortcuts import render
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.db import IntegrityError
from .forms import UserUpdateForm, ProfileUpdateForm
# Create your views here.

# @login_required
# def profile(request):
#     return render(request,'profile.html')


def update_profile(request):
    if request.method == "GET":
        return render(request,'profile.html')
    
    elif request.user.is_authenticated:
        users = request.user
        user = User.objects.get(pk=users.id)
        user.first_name = request.POST['f_name']
        user.last_name = request.POST['l_name']
        user.email = request.POST['c_email']
        user.username = request.POST['u_name']
        user.set_password(request.POST['c_pass']) 
        user.save()
        return redirect('/')



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid and p_form.is_valid():
            u_form.save()
            p_form.save()  
            messages.success(request, f'Your Account has been Updated!')
            return redirect('profile')                             
    else:
        UserForm = UserUpdateForm(instance=request.user)
        ProfileForm = ProfileUpdateForm(instance=request.user.profile) 
    context_of_forms = {
        'UserForm': UserForm, 
        'ProfileForm': ProfileForm
    }
    return render(request, 'profile.html', context_of_forms)



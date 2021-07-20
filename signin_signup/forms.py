# from django.forms import ModelForms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import forms
# from .models import Profile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']


# class UserUpdateForm(form.ModelForm):
#      class Meta:
#         model = User 
#         fields = ['first_name', 'last_name','username', 'email']


# class ProfileUpdateForm(form.ModelForm):
#      class Meta:
#         model = Profile
#         field = ['image']

        




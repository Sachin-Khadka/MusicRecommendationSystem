from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm 

class UploadForm(forms.ModelForm):
    class Meta:
        model= models.Music
        fields=['title', 'description', 'image', 'singer', 'band', 'category', 'language', 'status', 'year_of_production']


# class UploadForm(forms.ModelForm):
#     class Meta:
#         model = models.Music
#         fields = '__all__'
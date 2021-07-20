from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm 

class ClientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model=models.Client
        fields=['address','mobile','profile_pic']


class GuestUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class GuestForm(forms.ModelForm):
    class Meta:
        model=models.Guest
        fields=['address','mobile','profile_pic']



class AdminRequestForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of client model will be shown there in html
    client=forms.ModelChoiceField(queryset=models.Client.objects.all(),empty_label="Customer Name",to_field_name='id')
    guest=forms.ModelChoiceField(queryset=models.Guest.objects.all(),empty_label="Guest Name",to_field_name='id')


class AskDateForm(forms.Form):
    date=forms.DateField()


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


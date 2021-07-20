from django.shortcuts import render
from django.http import HttpRequest
from dashboard import views
from django.contrib.auth.models import Group
from .models import Contact

# Create your views here.
def home(request):
    return render(request, 'index.html')


def ContactView(request):
    if request.method == 'POST':
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact.name = name 
        contact.email = email
        contact.subject = subject
        contact.message = message
        contact.save()
        return render(request,'contactsuccess.html', {'sac': name})
    return render(request,'index.html')

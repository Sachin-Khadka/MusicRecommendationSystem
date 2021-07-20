from django.urls import path
#from . views import *
from . import views 

urlpatterns = [
    path('', views.home, name = "usermanagement-home"),
    path('contact/', views.ContactView, name='contact'),
]

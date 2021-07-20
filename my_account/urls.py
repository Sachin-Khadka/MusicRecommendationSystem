
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('profile/update/',update_profile)

]

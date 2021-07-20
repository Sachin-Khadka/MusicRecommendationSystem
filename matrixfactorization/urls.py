from django.urls import path
from .import views

urlpatterns = [
    path('hacker/',views.recommend1,name='recommend')
]
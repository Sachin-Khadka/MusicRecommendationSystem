"""
- Music Recommendation System
- User Management System [Admin, Client, and Guest]
- Dashboard Management System 
- Music Management Sytem 
- Review and Rating Management System

"""
from django.contrib import admin
from django.urls import path
from dashboard import views

from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home_view,name=''),

    # For after click
    path('adminclick', views.adminclick_view, name = 'adminclick'),
    path('clientclick', views.clientclick_view,name = 'clientclick' ),
    path('guestclick', views.guestsclick_view, name = 'guestclick'),


    # For Signup
    path('clientsignup', views.client_signup_view,name='clientsignup'),
    path('guestsignup', views.guest_signup_view,name='guestsignup'),

    # For Login
    path('clientlogin', LoginView.as_view(template_name='client/clientlogin.html'),name='clientlogin'),
    path('guestlogin', LoginView.as_view(template_name='guest/guestlogin.html'),name='guestlogin'),
    path('adminlogin', LoginView.as_view(template_name='admin/adminlogin.html'),name='adminlogin'),


    # Admin Power for Client and Guest 
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-client', views.admin_client_view,name='admin-client'),
    path('admin-view-client',views.admin_view_client_view,name='admin-view-client'),
    path('delete-client/<int:pk>', views.delete_client_view,name='delete-client'),
    path('update-client/<int:pk>', views.update_client_view,name='update-client'),
    path('admin-add-client', views.admin_add_client_view,name='admin-add-client'),
    path('client-request', views.client_request_view,name='client-request'),
    path('client-dashboard', views.client_dashboard_view,name='client-dashboard'),
    path('client-profile', views.client_profile_view,name='client-profile'),
    path('edit-client-profile', views.edit_client_profile_view,name='edit-client-profile'),

    # Admin Power for Guest
    path('admin-guest', views.admin_guest_view,name='admin-guest'),
    path('admin-view-guest',views.admin_view_guest_view,name='admin-view-guest'),
    path('delete-guest/<int:pk>', views.delete_guest_view,name='delete-guest'),
    path('update-guest/<int:pk>', views.update_guest_view,name='update-guest'),
    path('admin-add-guest',views.admin_add_guest_view,name='admin-add-guest'),
    path('admin-approve-guest',views.admin_approve_guest_view,name='admin-approve-guest'),
    path('approve-guest/<int:pk>', views.approve_guest_view,name='approve-guest'),
    path('delete-guest/<int:pk>', views.delete_guest_view,name='delete-guest'),
    path('guest-profile', views.guest_profile_view,name='guest-profile'),
    path('edit-guest-profile', views.edit_guest_profile_view,name='edit-guest-profile'),
    path('guest-dashboard', views.guest_dashboard_view,name='guest-dashboard'),



    # For After login and logout 
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='index.html'),name='logout'),

    # For Contact us and About us
    path('aboutus', views.aboutus_view, name='aboutus'),
    path('contactus', views.contactus_view, name='contactus'),
    


   # For Feedback  
   path('guest_feedback_message/', views.guest_feedback_message, name="guest_feedback_message"),
   path('guest_feedback_message_reply/', views.guest_feedback_message_reply, name="guest_feedback_message_reply"),
   path('client_feedback_message/', views.client_feedback_message, name="client_feedback_message"),
   path('client_feedback_message_reply/',views.client_feedback_message_reply, name="client_feedback_message_reply"),

   path('client_feedback/', views.client_feedback, name="client_feedback"),
   path('client_feedback_save/',views.client_feedback_save, name="client_feedback_save"),

   path('guest_feedback', views.guest_feedback, name="guest_feedback"),
   path('guest_feedback_save/',views.guest_feedback_save, name="guest_feedback_save"),

 


  

   
]

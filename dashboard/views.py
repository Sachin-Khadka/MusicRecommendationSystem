from django.shortcuts import render,redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from django.views.generic import ListView, DetailView 
from client.views import Channel


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'index.html')


#for showing signup/login button for Client
def clientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'client/clientclick.html')

#for showing signup/login button for Guests
def guestsclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'guest/guestsclick.html')


#for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


# for client signup 
def client_signup_view(request):
    userForm=forms.ClientUserForm()
    clientForm=forms.ClientForm()
    mydict={'userForm':userForm,'clientForm':clientForm}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST)
        clientForm=forms.ClientForm(request.POST,request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            client=clientForm.save(commit=False)
            client.user=user
            client.save()
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
            username = userForm.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to login.')
            channel = Channel(name=username)
            channel.save()
        return HttpResponseRedirect('clientlogin')
    return render(request,'client/clientsignup.html',context=mydict)


# for guest signup 
def guest_signup_view(request):
    userForm=forms.GuestUserForm()
    guestForm=forms.GuestForm()
    mydict={'userForm':userForm,'guestForm':guestForm}
    if request.method=='POST':
        userForm=forms.GuestUserForm(request.POST)
        guestForm=forms.GuestForm(request.POST,request.FILES)
        if userForm.is_valid() and guestForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            guest=guestForm.save(commit=False)
            guest.user=user
            guest.save()
            my_guest_group = Group.objects.get_or_create(name='GUEST')
            my_guest_group[0].user_set.add(user)
            username = userForm.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to login.')
            channel = Channel(name=username)
            channel.save()
        return HttpResponseRedirect('guestlogin')
    return render(request,'guest/guestsignup.html',context=mydict)


#for checking user client, Guest or admin(by sumit)
def is_client(user):
    return user.groups.filter(name='CLIENT').exists()
def is_guest(user):
    return user.groups.filter(name='GUEST').exists()
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


# render after login for client  and guest.
def afterlogin_view(request):
    if is_client(request.user):
        return redirect('client-dashboard')
    elif is_guest(request.user):
        accountapproval=models.Guest.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('guest-dashboard')
        else:
            return render(request,'guest/guest_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



#============================================================================================
# ADMIN RELATED views start
#============================================================================================

# for admin dashboard view 
@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
    'total_client':models.Client.objects.all().count(),
    'total_guest':models.Guest.objects.all().count(),
    'client_feedback': models.FeedBackClient.objects.all().count(),
    'guest_feedback': models.FeedBackGuest.objects.all().count(),
    'total_feedback':models.FeedBackClient.objects.all().count() + models.FeedBackGuest.objects.all().count(),
    }
    return render(request,'admin/admin_dashboard.html',context=dict)

        

# for admin view for client 
@login_required(login_url='adminlogin')
def admin_client_view(request):
    return render(request,'admin/admin_client.html')

@login_required(login_url='adminlogin')
def admin_view_client_view(request):
    clients= models.Client.objects.all()
    print("Profile Pic: ", clients) 
    # print("Profile Pic: ", clients.profile_pic)
    return render(request,'admin/admin_view_client.html',{'clients':clients})


# admin delete - client 
@login_required(login_url='adminlogin')
def delete_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)
    user.delete()
    client.delete()
    return redirect('admin-view-client')

# admin update - client 
@login_required(login_url='adminlogin')
def update_client_view(request,pk):
    client=models.Client.objects.get(id=pk)
    user=models.User.objects.get(id=client.user_id)
    userForm=forms.ClientUserForm(instance=user)
    clientForm=forms.ClientForm(request.FILES,instance=client)
    mydict={'userForm':userForm,'clientForm':clientForm}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST,instance=user)
        clientForm=forms.ClientForm(request.POST,request.FILES,instance=client)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            clientForm.save()
            messages.success(request, f'Account is Updated Successfully!')
            return redirect('admin-view-client')
    return render(request,'admin/update_client.html',context=mydict)


# admin add - client 
@login_required(login_url='adminlogin')
def admin_add_client_view(request):
    userForm=forms.ClientUserForm()
    clientForm=forms.ClientForm()
    mydict={'userForm':userForm,'clientForm':clientForm}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST)
        clientForm=forms.ClientForm(request.POST,request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            client=clientForm.save(commit=False)
            client.user=user
            client.save()
            my_client_group = Group.objects.get_or_create(name='CLIENT')
            my_client_group[0].user_set.add(user)
            messages.success(request, f'New Client is Added Successfully!')
        return HttpResponseRedirect('/admin-view-client')
    return render(request,'admin/admin_add_client.html',context=mydict)



# for admin view for client 
@login_required(login_url='adminlogin')
def admin_guest_view(request):
    return render(request,'admin/admin_guest.html')

@login_required(login_url='adminlogin')
def admin_approve_guest_view(request):
    guests=models.Guest.objects.all().filter(status=False)
    return render(request,'admin/admin_approve_guest.html',{'guests':guests})

@login_required(login_url='adminlogin')
def approve_guest_view(request,pk):
    guest=models.Guest.objects.get(id=pk)
    guest.status=True
    guest.save()
    messages.success(request, f'Guest is Approved Successfully!')
    return render(request,'admin/admin_approve_guest_details.html')

# admin delete - guest
@login_required(login_url='adminlogin')
def delete_guest_view(request,pk):
    guest=models.Guest.objects.get(id=pk)
    user=models.User.objects.get(id=guest.user_id)
    user.delete()
    guest.delete()
    return redirect('admin-approve-guest')

# admin add - guest
@login_required(login_url='adminlogin')
def admin_add_guest_view(request):
    userForm=forms.GuestUserForm()
    guestForm=forms.GuestForm()
    mydict={'userForm':userForm,'guestForm':guestForm}
    if request.method=='POST':
        userForm=forms.GuestUserForm(request.POST)
        guestForm=forms.GuestForm(request.POST,request.FILES)
        if userForm.is_valid() and guestForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            guest=guestForm.save(commit=False)
            guest.user=user
            guest.status=True
            guest.save()
            my_guest_group = Group.objects.get_or_create(name='GUEST')
            my_guest_group[0].user_set.add(user)
            messages.success(request, f'New Guest is Added Successfully!')
            return HttpResponseRedirect('admin-view-guest')
        else:
            print('problem in form')
    return render(request,'admin/admin_add_guest.html',context=mydict)



# for admin view for client 
@login_required(login_url='adminlogin')
def admin_view_guest_view(request):
    guests=models.Guest.objects.all()
    return render(request,'admin/admin_view_guest.html',{'guests':guests})


# admin update - guest
@login_required(login_url='adminlogin')
def update_guest_view(request,pk):
    guest=models.Guest.objects.get(id=pk)
    user=models.User.objects.get(id=guest.user_id)
    userForm=forms.GuestUserForm(instance=user)
    guestForm=forms.GuestForm(request.FILES,instance=guest)
    mydict={'userForm':userForm,'guestForm':guestForm}
    if request.method=='POST':
        userForm=forms.GuestUserForm(request.POST,instance=user)
        guestForm=forms.GuestForm(request.POST,request.FILES,instance=guest)
        if userForm.is_valid() and guestForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            guestForm.save()
            messages.success(request, f'Account is Updated Successfully!')
            return redirect('admin-view-guest')
    return render(request,'admin/update_guest.html',context=mydict)


#============================================================================================
# ADMIN RELATED views END
#============================================================================================


#============================================================================================
# Client RELATED views start
#============================================================================================
from django.db.models import Q

@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_dashboard_view(request):
    client_obj = models.Client.objects.get(user=request.user.id)
    feedback_data_count = models.FeedBackClient.objects.filter(client_id=client_obj).count()
    context = {
        "feedback_data_count":feedback_data_count ,
        "client_obj": client_obj
    }
    return render(request,'client/client_dashboard.html', context)

@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_request_view(request):
    client=models.Client.objects.get(user_id=request.user.id)
    return render(request,'client/client_request.html',{'client':client})


@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def client_profile_view(request):
    client=models.Client.objects.get(user_id=request.user.id)
    return render(request,'client/client_profile.html',{'client':client})


@login_required(login_url='clientlogin')
@user_passes_test(is_client)
def edit_client_profile_view(request):
    client=models.Client.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=client.user_id)
    userForm=forms.ClientUserForm(instance=user)
    clientForm=forms.ClientForm(request.FILES,instance=client)
    mydict={'userForm':userForm,'clientForm':clientForm,'client':client}
    if request.method=='POST':
        userForm=forms.ClientUserForm(request.POST,instance=user)
        clientForm=forms.ClientForm(request.POST,instance=client)
        if userForm.is_valid() and clientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            clientForm.save()
            return HttpResponseRedirect('client-profile')
    return render(request,'client/edit_client_profile.html',context=mydict)


#============================================================================================
# Client RELATED views END
#============================================================================================






#============================================================================================
# Guest RELATED views start
#============================================================================================

@login_required(login_url='guestlogin')
@user_passes_test(is_guest)
def guest_dashboard_view(request):
    guest_obj = models.Guest.objects.get(user=request.user.id)
    feedback_data_count = models.FeedBackGuest.objects.filter(guest_id=guest_obj).count()
    context = {
        "feedback_data_count":feedback_data_count, 
        "guest_obj": guest_obj
    }
    guest=models.Guest.objects.get(user_id=request.user.id)
    return render(request,'guest/guest_dashboard.html', context)


@login_required(login_url='guestlogin')
@user_passes_test(is_guest)
def guest_profile_view(request):
    guest=models.Guest.objects.get(user_id=request.user.id)
    return render(request,'guest/guest_profile.html',{'guest':guest})

@login_required(login_url='guestlogin')
@user_passes_test(is_guest)
def edit_guest_profile_view(request):
    guest=models.Guest.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=guest.user_id)
    userForm=forms.GuestUserForm(instance=user)
    guestForm=forms.GuestForm(request.FILES,instance=guest)
    mydict={'userForm':userForm,'guestForm':guestForm,'guest':guest}
    if request.method=='POST':
        userForm=forms.GuestUserForm(request.POST,instance=user)
        guestForm=forms.GuestForm(request.POST,request.FILES,instance=guest)
        if userForm.is_valid() and guestForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            guestForm.save()
            return redirect('guest-profile')
    return render(request,'guest/edit_guest_profile.html',context=mydict)


#============================================================================================
# Guest RELATED views end
#============================================================================================



# for aboutus and contact
def aboutus_view(request):
    return render(request,'aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'contactussuccess.html')
    return render(request, 'contactus.html', {'form':sub})





#============================================================================================
# With Respect to Admin
#============================================================================================
def guest_feedback_message(request):
    feedbacks = models.FeedBackGuest.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin/guest_feedback_template.html', context)


@csrf_exempt
def guest_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = models.FeedBackGuest.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def client_feedback_message(request):
    feedbacks = models.FeedBackClient.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'admin/client_feedback_template.html', context)


@csrf_exempt
def client_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')
    try:
        feedback = models.FeedBackClient.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")




#============================================================================================
# Admin, Client, GUEST RELATED views for Feedback  
#============================================================================================

# For Client 

def client_feedback(request):
    client_obj = models.Client.objects.get(user=request.user.id)
    feedback_data = models.FeedBackClient.objects.filter(client_id=client_obj)
    feedback_data_count = models.FeedBackClient.objects.filter(client_id=client_obj).count()
    print("The data is:", feedback_data_count) 
    context = {
        "feedback_data": feedback_data,
        "feedback_data_count": feedback_data_count,
        "client_obj": client_obj
    }
    return render(request, 'client/client_feedback.html', context)


def client_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('client_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        client_obj = models.Client.objects.get(user_id=request.user.id)

        try:
            add_feedback = models.FeedBackClient(client_id=client_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('client_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('client_feedback')



# For Guest

def guest_feedback(request):
    guest_obj = models.Guest.objects.get(user=request.user.id)
    feedback_data = models.FeedBackGuest.objects.filter(guest_id=guest_obj)
    print(feedback_data)
    context = {
        "feedback_data": feedback_data,
        "guest_obj": guest_obj
    }
    return render(request, 'guest/guest_feedback.html', context)


def guest_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('guest_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        guest_obj = models.Guest.objects.get(user_id=request.user.id)

        try:
            add_feedback = models.FeedBackGuest(guest_id=guest_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('guest_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('guest_feedback')



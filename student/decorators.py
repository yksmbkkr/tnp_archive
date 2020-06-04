from .models import *
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from management.models import *

def not_manager_required(f):
    def wrap(request, *args, **kwargs):
        try:
            managers.objects.get(user=request.user)
            return redirect('management:m_home')
        except managers.DoesNotExist:
            pass
        return f(request,*args,**kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap




def create_profile_dec(f):
    def wrap(request, *args, **kwargs):
        try:
            profile_object = profile_set.objects.get(user = request.user)
        except profile_set.DoesNotExist:
            return redirect('management:m_home')
        #email_confirmation_object = email_confirmation.objects.get(user = request.user)
#        if not email_confirmation_object.confirm:
#            return redirect('not_confirmed')
        if profile_object.check:
            messages.info(request,"Your profile is already created.")
            return redirect('student:s_profile')
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

#This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr

def is_profile_created(f):
    def wrap(request, *args, **kwargs):
        try:
            profile_object = profile_set.objects.get(user = request.user)
        except profile_set.DoesNotExist:
            return redirect('management:m_home')
#        email_confirmation_object = email_confirmation.objects.get(user = request.user)
#        if not email_confirmation_object.confirm:
#            return redirect('not_confirmed')
        if not profile_object.check:
            messages.warning(request, "Complete your profile first.")
            return redirect('student:s_create_profile')
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__=f.__name__
    return wrap

#def confirm_mail(f):
#    def wrap(request, *args, **kwargs):
#        email_confirmation_object = email_confirmation.objects.get(user = request.user)
#        if email_confirmation_object.confirm:
#            return redirect('profile')
#        return f(request, *args, **kwargs)

#    wrap.__doc__ = f.__doc__
#    wrap.__name__=f.__name__
#    return wrap



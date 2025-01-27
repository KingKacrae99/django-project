from django.http import HttpResponseForbidden
from django.shortcuts import  redirect
from .models import *

def unauthenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def allow_users(roles=[]):
    def permissions(view_func):
        def wrapper(request, *args, **kwargs):
            user =  request.user

            if user.is_authenticated and (user.is_admin or user.role in roles):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have access to this page")
        return wrapper
    return permissions

def only_admin(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Only Admin has authorized access to this page.")
    return wrapper
from django.shortcuts import redirect
from django.contrib import messages

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You are not authorized to access this page.")
                return redirect('/')
        else:
            return redirect('login')
    return wrapper_func


def user_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            messages.error(request, "Admins are not allowed here.")
            return redirect('/admin/dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


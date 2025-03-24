from django.shortcuts import redirect


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper_func

def user_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('/admin/dashboard/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

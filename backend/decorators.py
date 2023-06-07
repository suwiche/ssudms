from django.shortcuts import redirect
from django.contrib.auth.models import User


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                if group == "superadmin":
                    return redirect('backend-index-page')
                elif group == "admin":
                    return redirect('frontend-index-page')
                elif group == "staff":
                    return redirect('frontend-records')

                return redirect('landingpage-index-page')

        return wrapper_func

    return decorator


def staff_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == "superadmin":
            return redirect('backend-index-page')
        if group == "admin" or group == "staff":
            return redirect('frontend-index-page')

    return wrapper_function
from django.shortcuts import redirect

def role_required(role):
    """Decorator that restricts view access to a specific user_type or list of types.

    ``role`` may be a single string or an iterable of strings. If the current
    user's ``user_type`` is not in the allowed set, they are redirected to
    login (the same behaviour as before).
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            allowed = role
            if isinstance(role, (list, tuple, set)):
                allowed = role
            else:
                allowed = {role}

            if request.user.user_type not in allowed:
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
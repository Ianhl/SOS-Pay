from django.http import HttpResponseForbidden
from functools import wraps

def user_is_tuckshop_owner(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'tuckshop_owner'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have access to this page.")
    return _wrapped_view


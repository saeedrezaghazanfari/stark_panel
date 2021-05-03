from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test

# ########### Mixins ########### @

# update user permission
class UpdateUserPermission():
    def dispatch(self, request, *args, **kwargs):
        if not request.user.id == kwargs.get('userID') or not request.user.is_active:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

# isacountants permission mixin
class AcountantPermision():
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_acountants or not request.user.is_active:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


# ########### Decorators ########### #

# is_active permission decorator
def active_required_decorator(function=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# is_superuser permission decorator
def superuser_required_decorator(function=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# isacountants permission decorator
def acountants_required_decorator(function=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_acountants,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# issuppurt permission
def suppurt_required_decorator(function=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_suppurt,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
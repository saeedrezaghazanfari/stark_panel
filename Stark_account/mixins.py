from django.contrib.auth.decorators import login_required, user_passes_test

# Decorators

# is_authenticated permission decorator
def authenticated_required_decorator(function=None, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=login_url,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
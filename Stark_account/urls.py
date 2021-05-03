from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
	path('sign-in', views.signin_page, name="signin"),
	path('sign-up', views.signup_page, name="signup"),
	# path('account/activation/<uidb64>/<token>', views.activate, name='activate'),
	path('sign-out', views.sign_out, name="signout"),
]

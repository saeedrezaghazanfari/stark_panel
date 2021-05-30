from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
	path('sign-in', views.signin_page, name="signin"),
	path('sign-up', views.signup_page, name="signup"),
	path('sign/forget-password', views.forgetPassword_page, name='forgetPw'),
	path('sign-out', views.sign_out, name="signout"),

	path('sign/change-password/<uidb64>/<token>', views.account_change_pw, name='forget_pw_email'),
	path('account/activation/<uidb64>/<token>', views.account_activate, name='activate'),
]

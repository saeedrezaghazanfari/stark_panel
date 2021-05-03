from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from Extentions.utils import get_user_code
from .forms import SigninForm, SignUpForm
from .models import User
from .mixins import authenticated_required_decorator
from django.utils.translation import activate

# imports for signup and activation 
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
# from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.translation import gettext_lazy as _


@authenticated_required_decorator(login_url='/')
def signin_page(request):
	login_form = SigninForm(request.POST or None)
	context = {
		'login_form': login_form,
	}
	if login_form.is_valid():
		# get username-email or password
		email_or_username = login_form.cleaned_data.get('emailORusername')
		password = login_form.cleaned_data.get('password')
		
		myuser = User.objects.filter(email__iexact=email_or_username).first()
		# authenticate by username
		if myuser:
			user = authenticate(request, username=myuser.username, password=password)
			if user is None:
				login_form.add_error('password', _('رمز عبور اشتباه است.') )
		
		# authenticate by email
		elif User.objects.filter(username__iexact=email_or_username).first():
			user = authenticate(request, username=email_or_username, password=password)
			if user is None:
				login_form.add_error('password', _('رمز عبور اشتباه است.') )
		
		else:
			login_form.add_error('emailORusername', _('ایمیل / نام کاربری شما فاقد اعتبار است.') )
		
		# user login and end login mission
		if user:
			login(request, user)
			context['login_form'] = login_form
			messages.info(request, _('شما با موفقیت وارد شدید.') )
			messages.info(request, _('به پنل کاربری استارک خوش آمدید.') )
			return redirect('pannel:home')

	return render(request, 'signin.html', context)


@authenticated_required_decorator(login_url='/')
def signup_page(request):
	if request.method == 'POST':
		max_id = User.objects.values('id').order_by('-id').first()
		get_max_id = dict(max_id)['id']
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.user_code = get_user_code()
			user.is_active = True
			user.id = int(get_max_id) + 1
			user.save()

			# current_site = get_current_site(request)    # get domain site

			# # send mail
			# mail_subject = 'به پنل کاربری استارک خوش آمدید'
			# messagee = render_to_string('content_of_email.html', {
			# 	'user': user,
			# 	'domain': current_site.domain,
			# 	'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			# 	'token':account_activation_token.make_token(user),
			# })
			# to_email = form.cleaned_data.get('email')
			# msg_EMAIL = EmailMessage(
			# 	mail_subject, messagee, from_email=settings.EMAIL_HOST_USER, to=[to_email]
			# )
			# msg_EMAIL.content_subtype = "html"
			# msg_EMAIL.send()

			form = SignUpForm()
			messages.info(request, _('ساخت اکانت شما موفقیت آمیز بود') )
			messages.info(request, _('برای ورود اطلاعات خود را وارد کنید') )
			# messages.info(request, _('برای فعالسازی حساب به ایمیل خود مراجعه کنید.') )
			return redirect('account:signin')
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})

# this function for activation account
# def activate(request, uidb64, token):
# 	try:
# 		uid = force_text(urlsafe_base64_decode(uidb64))
# 		user = User.objects.get(pk=uid)
# 	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
# 		user = None
# 	if user is not None and account_activation_token.check_token(user, token):
# 		# actiavate account
# 		user.is_active = True
# 		user.save()
# 		messages.info(request, _('حساب کاربری شما فعال گردید.') )
# 		messages.info(request, _('برای ورود به حساب ، اطلاعات خود را وارد کنید.') )
# 		return redirect('account:signin')
# 	else:
# 		return HttpResponse('لینک فعالسازی شما نامعتبر است.')

def sign_out(request):
	logout(request)
	return redirect('account:signin')
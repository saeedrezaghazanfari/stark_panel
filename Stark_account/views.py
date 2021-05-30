from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from Extentions.utils import get_user_code
from .forms import SigninForm, SignUpForm, getEmailToForgetPwForm
from .models import User
from .mixins import authenticated_required_decorator
from .forms import PasswordChangeForm       # customize the PasswordChangeForm
from django.utils.translation import get_language

# imports for signup and activation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
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

			request.session['username'] = user.username
			request.session['password'] = user.password
			if not request.POST.get('save-me-cehckbox'):
				request.session.set_expiry(0)

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
def forgetPassword_page(request):
	emailform = getEmailToForgetPwForm(request.POST or None)
	context = { 'emailform': emailform }

	if emailform.is_valid():

		email_get = emailform.cleaned_data.get('email')
		user_get = User.objects.filter(email=email_get).first()

		current_site = get_current_site(request)

		# send Eamil
		mail_subject = _('استارک | فراموشی رمزعبور')
		if get_language() == 'fa':
			messagee = render_to_string('email_forget_pw/_email_forget_pw_fa.html', {
				'username': user_get,
				'domain': current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(user_get.pk)),
				'token':account_activation_token.make_token(user_get),
				'date': datetime.now(),
			})
		elif get_language() == 'en':
			messagee = render_to_string('email_forget_pw/_email_forget_pw_en.html', {
				'username': user_get,
				'domain': current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(user_get.pk)),
				'token':account_activation_token.make_token(user_get),
				'date': datetime.now(),
			})
		elif get_language() == 'ar':
			messagee = render_to_string('email_forget_pw/_email_forget_pw_ar.html', {
				'username': user_get,
				'domain': current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(user_get.pk)),
				'token':account_activation_token.make_token(user_get),
				'date': datetime.now(),
			})
		to_email = email_get
		msg_EMAIL = EmailMessage(
			mail_subject, messagee, from_email=settings.EMAIL_HOST_USER, to=[to_email]
		)
		msg_EMAIL.content_subtype = "html"
		msg_EMAIL.send()
		
		messages.info(request, _('ایمیل فراموشی رمزعبور برای شما ارسال شد.') )
		return redirect('account:signin')

	return render(request, 'forget_password_page.html', context)

@authenticated_required_decorator(login_url='/')
def signup_page(request):
	if request.method == 'POST':
		max_id = User.objects.values('id').order_by('-id').first()
		get_max_id = dict(max_id)['id']
		form = SignUpForm(request.POST)

		# check the sured form
		if request.POST.get('sure-from-stark'):
			
			if form.is_valid():
				user = form.save(commit=False)
				user.user_code = get_user_code()
				user.is_active = False
				user.id = int(get_max_id) + 1
				user.save()

				current_site = get_current_site(request)    # get domain site

				# send mail
				mail_subject = _('به پنل کاربری استارک خوش آمدید')
				if get_language() == 'fa':
					messagee = render_to_string('email_activate/_email_activate_fa.html', {
						'username': user,
						'domain': current_site.domain,
						'uid':urlsafe_base64_encode(force_bytes(user.pk)),
						'token':account_activation_token.make_token(user),
						'date': datetime.now(),
					})
				elif get_language() == 'en':
					messagee = render_to_string('email_activate/_email_activate_en.html', {
						'username': user,
						'domain': current_site.domain,
						'uid':urlsafe_base64_encode(force_bytes(user.pk)),
						'token':account_activation_token.make_token(user),
						'date': datetime.now(),
					})
				elif get_language() == 'ar':
					messagee = render_to_string('email_activate/_email_activate_ar.html', {
						'username': user,
						'domain': current_site.domain,
						'uid':urlsafe_base64_encode(force_bytes(user.pk)),
						'token':account_activation_token.make_token(user),
						'date': datetime.now(),
					})
				to_email = form.cleaned_data.get('email')
				msg_EMAIL = EmailMessage(
					mail_subject, messagee, from_email=settings.EMAIL_HOST_USER, to=[to_email]
				)
				msg_EMAIL.content_subtype = "html"
				msg_EMAIL.send()

				form = SignUpForm()
				messages.info(request, _('ساخت اکانت شما موفقیت آمیز بود') )
				messages.info(request, _('برای فعالسازی حساب به ایمیل خود مراجعه کنید.') )
				return redirect('account:signin')
		else:
			messages.info(request, _('برای ثبت نام باید با قوانین و مقررات موافق باشید.') )
			return redirect('account:signup')	

	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})

# this function for change password form
def account_change_pw(request, uidb64, token):
	
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		password_form = PasswordChangeForm(user=request.user, data=request.POST)
		context = {
			'password_form': password_form
		}

		if password_form.is_valid():
			password_get = password_form.cleaned_data.get('new_password2')

			for i in password_get:
				if ord(i) > 1000:
					messages.info(request, _('رمزعبور باید شامل حروف انگلیسی، اعداد و علامت‌ها باشد.') )
					return redirect('account:signin')

			user.set_password(password_get)
			user.save()
			messages.info(request, _('رمزعبور شما بروزرسانی شد.') )
			messages.info(request, _('برای ورود اطلاعات خود را وارد کنید.') )
			return redirect('account:signin')

		return render(request, 'change_pw_form.html', context)

	else:
		messages.info(request, _('لینکی که با آن وارد شده‌اید، نامعتبر است.') )
		return redirect('account:signin')

# this function for activation account
def account_activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		# actiavate account
		user.is_active = True
		user.save()
		messages.info(request, _('حساب کاربری شما فعال گردید.') )
		messages.info(request, _('برای ورود به حساب، اطلاعات خود را وارد کنید.') )
		return redirect('account:signin')
	else:
		messages.info(request, _('لینک فعالسازی شما نامعتبر است.') )
		return redirect('account:signin')

def sign_out(request):
	if request.session.has_key('username'):
		request.session.flush()
	logout(request)
	return redirect('account:signin')
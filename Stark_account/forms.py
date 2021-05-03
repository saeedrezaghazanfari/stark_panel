from django import forms
from captcha.fields import CaptchaField
from .models import User
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.contrib.auth.forms import UserCreationForm


# generate login form
class SigninForm(forms.Form):
	emailORusername = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('نام کاربری و یا ایمیل خود را وارد کنید:') }), label= _("نام کاربری / ایمیل:"), required=False)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': _('رمز عبور خود را وارد کنید:') }), label= _("رمز عبور:") , required=False)
	captcha = CaptchaField()
	
	def clean_captcha(self):
		captcha = self.cleaned_data.get('captcha')
		

	def clean_emailORusername(self):
		email_un = self.cleaned_data.get('emailORusername')
	
		if len(email_un) <= 1:
			raise forms.ValidationError( _('نام کاربری خود را وارد کنید.') )
		
		if not User.objects.filter(email__iexact=email_un).first():
			if not User.objects.filter(username__iexact=email_un).first():
				raise forms.ValidationError( _('نام کاربری / ایمیل وارد شده فاقد اعتبار است.') )
		
		if not User.objects.filter(username__iexact=email_un).first():
			if not User.objects.filter(email__iexact=email_un).first():
				raise forms.ValidationError( _('نام کاربری / ایمیل وارد شده فاقد اعتبار است.') )
		return email_un

	def clean_password(self):
		password = self.cleaned_data.get('password')
		if len(password) <= 1:
			return forms.ValidationError( _('لطفا رمز عبور خود را وارد کنید.') )
		return password


class SignUpForm(UserCreationForm):
	first_name = forms.CharField(
		widget=forms.TextInput(),
		validators=[
			validators.MaxLengthValidator(30, _('نام نباید بیشتر از 30 کاراکتر باشد.') ),
			validators.MinLengthValidator(2, _('نام نباید کمتر از 2 کاراکتر باشد') )
		],
		label= _("نام")
	)
	last_name = forms.CharField(
		widget=forms.TextInput(),
		validators=[
			validators.MaxLengthValidator(30, _('نام خانوادگی نباید بیشتر از 30 کاراکتر باشد') ),
			validators.MinLengthValidator(3, _('نام خانوادگی نباید کمتر از 3 کاراکتر باشد.') )
		],
		label= _("نام خانوادگی")
	)
	
	class Meta:
		model = User
		fields = ('username', 'email', 'phone', 'first_name', 'last_name', 'national_code', 'password1', 'password2')

	def clean_username(self):
		username = self.cleaned_data.get('username')
		
		# check username in DB
		if User.objects.filter(username__iexact=username).first():
			raise forms.ValidationError( _('نام کاربری دیگری انتخاب کنید.') )
		if '@' in username:
			raise forms.ValidationError( _('نام کاربری نمیتواند شامل @ باشد.') )
		for i in username:
			if ord(i) > 1000:
				raise forms.ValidationError( _('نام کاربری باید تنها شامل حروف انگلیسی باشد.') )
		return username
	
	# no empty email
	def clean_email(self):
		email = self.cleaned_data.get('email')
		
		# check email in DB
		if User.objects.filter(email__iexact=email).first():
			raise forms.ValidationError( _('ایمیل دیگری انتخاب کنید.') )
		return email

	def clean_phone(self):
		phone = self.cleaned_data.get('phone')
		# check phone in DB
		if User.objects.filter(phone__iexact=phone).first():
			raise forms.ValidationError( _('شماره همراه دیگری انتخاب کنید') )
		return phone

	def clean_national_code(self):
		national_code = self.cleaned_data.get('national_code')
		# check national_code in DB
		if User.objects.filter(national_code__iexact=national_code).first():
			raise forms.ValidationError( _('کد ملی دیگری انتخاب کنید.') )
		return national_code

	def clean_password2(self):
		password2 = self.cleaned_data.get('password2')
		for i in password2:
			if ord(i) > 1000:
				raise forms.ValidationError( _('رمزعبور باید شامل حروف انگلیسی، اعداد و علامت‌ها باشد.') )
		return password2
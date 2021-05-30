from datetime import datetime
from django.core.validators import RegexValidator
from django.core import validators
from django.db import models
from Stark_siteSetting.models import SettingCategory
from Extentions.utils import jalali_convertor_tokens, jalali_convertor, get_bot_code
from Stark_account.models import User
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class Token(models.Model):
	title = models.CharField( _('عنوان ارز'), max_length=30)
	price_doallr = models.FloatField( _('قیمت به دلار'))
	count = models.FloatField( _('تعداد'))

	class Meta:
		verbose_name = _('توکن')
		verbose_name_plural = _('توکن ها')
		ordering = ['id']

	def __str__(self):
		return self.title

class ChartTokenPrice(models.Model):
	token = models.ForeignKey( Token, on_delete=models.CASCADE, related_name='charts' ) 
	price_dollar = models.FloatField( _('قیمت به دلار') )
	date = models.DateField( _('تاریخ') )

	class Meta:
		verbose_name = _('قیمت دوره ای توکن')
		verbose_name_plural = _('قیمت های توکن')
		ordering = ['id']

	def j_date(self):
		return jalali_convertor_tokens(self.date)
	j_date.short_description = _('تاریخ')

	def __str__(self):
		return f'{self.j_date()}'

class BuyAndSell(models.Model):
	CHOISE_SELL_BUY = ( ('buy', _('خرید') ),('sell', _('فروش')) )
	user = models.ForeignKey( User, on_delete=models.CASCADE, related_name='buysells')
	token = models.ForeignKey( Token, on_delete=models.CASCADE, related_name='buysells' )
	count = models.FloatField( _('تعداد'))
	buy_sell = models.CharField( _('خرید یا فروش؟'), max_length=10, default='buy', choices=CHOISE_SELL_BUY)
	date = models.DateTimeField( _('تاریخ و زمان'), default=datetime.now() )
	is_paid = models.BooleanField( _('پرداخت شده'), default=False)

	class Meta:
		verbose_name = _('خرید و فروش')
		verbose_name_plural = _('خرید و فروش ها')
		ordering = ['id']

	def j_date(self):
		return jalali_convertor(self.date)
	j_date.short_description = _('تاریخ و زمان')

	def __str__(self):
		return f'{self.j_date()}'

class UserStoke(models.Model):
	user = models.ForeignKey( User, on_delete=models.CASCADE, related_name='userstokes')
	token = models.ForeignKey( Token, on_delete=models.CASCADE, related_name='userstokes')
	count = models.FloatField( _('تعداد دارایی'))
	date = models.DateTimeField( _('آخرین زمان ثبت دارایی'), default=datetime.now())

	class Meta:
		verbose_name = _('سهم کاربر')
		verbose_name_plural = _('سهام کاربر')
		ordering = ['id']

	def j_date(self):
		return jalali_convertor(self.date)
	j_date.short_description = _('آخرین زمان ثبت دارایی')

	def __str__(self):
		return f'{self.j_date()}'

class UserWallet(models.Model):
	user = models.ForeignKey( User, on_delete=models.CASCADE, related_name='wallets')
	address = models.CharField( _('آدرس کیف پول'), max_length=45, unique=True, validators=[
		RegexValidator(
			r'\d?\w{10,45}$',
			message=_('فرمت کیف پول را اصلاح کنید.')
		),
	])
	date = models.DateTimeField( _('تاریخ و زمان خرید'), default=datetime.now())
	class Meta:
		verbose_name = _('کیف پول')
		verbose_name_plural = _('کیف پول های کاربران')
		ordering = ['id']

	def j_date(self):
		return jalali_convertor_tokens(self.date)
	j_date.short_description = _('تاریخ و زمان')

	def __str__(self):
		return f'{self.user.username} - {self.user.user_code}'

class WalletOrder(models.Model):
	ORDER_KIND_CHOICE = (('inc', _('افزایش موجودی') ), ('dec', _('برداشت از موجودی') ))

	user = models.ForeignKey( User, on_delete=models.CASCADE )
	price = models.FloatField( _('مبلغ') )
	type_order = models.CharField( _('نوع درخواست'), max_length=5, choices=ORDER_KIND_CHOICE, default='inc' )
	wallet_address = models.CharField( _('آدرس کیف پول'), max_length=42 )
	date = models.DateTimeField( _('تاریخ و زمان'), default=datetime.now() )
	is_paid = models.BooleanField( _('پرداخت شده'), default=False )

	class Meta:
		verbose_name = _('عملیات کیف پول')
		verbose_name_plural = _('عملیات های کیف پول')
		ordering = ['id']

	def j_date(self):
		return jalali_convertor(self.date)
	j_date.short_description = _('تاریخ و زمان')

	def __str__(self):
		return f'{self.user.username} - {self.wallet_address}'

class RobotSubscription(models.Model):
	bot_code = models.CharField( _('کد ربات'), max_length=20, default=get_bot_code, unique=True)
	user = models.ForeignKey( User, on_delete=models.CASCADE, related_name='robots')
	time_subscription = models.CharField( _('مدت اشتراک'), max_length=50)
	date = models.DateTimeField( _('تاریخ و زمان خرید'), default=datetime.now())
	is_paid = models.BooleanField( _('پرداخت شده'), default=False)
	is_active = models.BooleanField( _('فعال / غیرفعال'), default=False)
	last_date = models.DateTimeField( _('تاریخ و زمان انقضا'), default=datetime.now())
	is_expired = models.BooleanField( _('منقضی شده؟'), default=False)

	class Meta:
		verbose_name = _('اشتراک ربات')
		verbose_name_plural = _('اشتراک ربات ها')
		ordering = ['id']

	def j_date(self):
		return jalali_convertor(self.date)
	j_date.short_description = _('تاریخ و زمان')

	def j_last_date(self):
		return jalali_convertor(self.last_date)
	j_last_date.short_description = _('تاریخ و زمان انقضا')

	def __str__(self):
		return f'{self.j_date()}'

# Ticket
class Ticket(models.Model):
	CHOICE_TITLE = (('crashPay', _('اشتراک ربات') ), ('InOut', _('پرداختی / برداشتی') ), ('buytoken', _('خرید ارز') ), ('selltoken', _('فروش ارز') ))

	is_suppurt = models.BooleanField( _('آیا این پیام از طرف پشتیبان ارسال شود؟'), default=False )
	user = models.ForeignKey( User, on_delete=models.CASCADE, related_name='tickets', blank=True, null=True)
	title = models.CharField( _('عنوان تیکت'), max_length=15, default='crashPay', choices=CHOICE_TITLE )
	subject = models.CharField( _('موضوع پیام'), max_length=150, validators=[ validators.MinLengthValidator(5, _('موضوع تیکت نباید کمتر از 5 کاراکتر باشد.')) ])
	message = models.TextField( _('متن پیام') )
	date = models.DateTimeField( _('تاریخ و زمان'), default=datetime.now() )
	is_seen = models.BooleanField( _('دیده شده توسط پشتیبان:'), default=False )
	is_seen_user = models.BooleanField( _('دیده شده توسط کاربر:'), default=False )

	class Meta:
		verbose_name = _('تیکت')
		verbose_name_plural = _('تیکت ها')
		ordering = ['id']

	def j_date(self):
		return jalali_convertor(self.date)
	j_date.short_description = _('تاریخ و زمان')

	def __str__(self):
		return f'{self.j_date()}'

# ///  SIGNALS

# update ST1 2 3 4 Token
@receiver(post_save, sender=ChartTokenPrice)
def save_profile(sender, instance, **kwargs):
	if instance.token.title == 'ST1':
		token = Token.objects.filter(title='ST1').first()
		token.price_doallr = instance.price_dollar
		token.save()

	elif instance.token.title == 'ST2':
		token = Token.objects.filter(title='ST2').first()
		token.price_doallr = instance.price_dollar
		token.save()
		
	elif instance.token.title == 'ST3':
		token = Token.objects.filter(title='ST3').first()
		token.price_doallr = instance.price_dollar
		token.save()

	elif instance.token.title == 'ST4':
		token = Token.objects.filter(title='ST4').first()
		token.price_doallr = instance.price_dollar
		token.save()

# update user tokens
@receiver(post_save, sender=BuyAndSell)
def save_userToken(sender, instance, **kwargs):
	if instance.is_paid:
		if instance.buy_sell == 'buy':
			user = User.objects.filter(id=instance.user.id).first()
			user_stoke = UserStoke.objects.filter(user=user, token=instance.token).first()
			if user_stoke:
				user_stoke.count += instance.count
				user_stoke.date = datetime.now()
				user_stoke.save()
			else:
				UserStoke.objects.create(
					user=user, 
					token=instance.token, 
					count=instance.count,
					date=datetime.now()
				)
		elif instance.buy_sell == 'sell':
			user = User.objects.filter(id=instance.user.id).first()
			user_stoke = UserStoke.objects.filter(user=user, token=instance.token).first()
			if user_stoke:
				user_stoke.count -= instance.count
				user_stoke.date = datetime.now()
				user_stoke.save()
			else:
				UserStoke.objects.create(
					user=user, 
					token=instance.token, 
					count=instance.count,
					date=datetime.now()
				)

# update user payment and user impre
@receiver(post_save, sender=WalletOrder)
def save_userStokes(sender, instance, **kwargs):
	if instance.is_paid:
		user = User.objects.filter(id=instance.user.id).first()
		if UserWallet.objects.filter(user=user, address=instance.wallet_address).first():
			if instance.type_order == 'inc':
				user.payment_total += instance.price
				user.save()

			elif instance.type_order == 'dec':
				user.impression_total += instance.price
				user.save()
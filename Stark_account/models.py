from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from Extentions.utils import get_filename_ext_rand
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


def upload_image_path_avatar(instance, filename):
	name, ext, rand = get_filename_ext_rand(filename)
	final_name = f"{rand}{ext}"
	return f"user_avatars/{final_name}"

def upload_image_path_national_code(instance, filename):
	name, ext, rand = get_filename_ext_rand(filename)
	final_name = f"{rand}{ext}"
	return f"user_national_code/{final_name}"

class User(AbstractUser):
	email = models.EmailField(_('ایمیل'))
	user_code = models.CharField( _('کدکاربری'), max_length=15, default=0, unique=True)
	stoke = models.FloatField( _('موجودی نقدی'), default=0)                   # دارایی نقد
	payment_total = models.FloatField( _('پرداختی کل کاربر'), default=0)      # پرداختی کل
	impression_total = models.FloatField( _('برداشتی کل کاربر'), default=0)   # دریافتی کل
	robot_sub_total = models.FloatField( _('اشتراک ربات'), default=0)          # اشتراک ربات
	avatar = models.ImageField( _('تصویر'), upload_to=upload_image_path_avatar, null=True, blank=True)
	backup_email = models.EmailField( _('ایمیل پشتیبان'), blank=True, null=True)
	phone = models.CharField( _('شماره همراه'), max_length=20, validators=[
		RegexValidator(
			regex=r'^\+?\d{7,19}$',
			message= _('فرمت شماره تلفن را اصلاح کنید.')
		),
	])
	is_acountants = models.BooleanField( _('وضعیت حسابداری'), default=False, help_text= _("نشان میدهد که آیا این کاربر میتواند عملیات مربوط به حسابداری را انجام دهد یا نه.") )
	is_suppurt = models.BooleanField( _('وضعیت پشتیبانی'), default=False, help_text= _("نشان میدهد که آیا این کاربر میتواند عملیات های پشتیبانی را انجام دهد یا خیر.") )

	class Meta:
		verbose_name = _("کاربر")
		verbose_name_plural = _('کاربران')
		ordering = ['id']

	def tag_avatar(self):
		if self.avatar:
			return format_html(f'<div style="background: url({self.avatar.url}) no-repeat center center / cover; height:80px !important; width:80px !important; border-radius: 7px;">')
		return '-'
	tag_avatar.short_description = _('تصویر کاربر ')

	def __str__(self):
		return self.user_code
	
	def profit_user(self):
		from Stark_panel.st_modules import get_final_total
		final_total = get_final_total(self)
		return float( format( ((final_total + self.impression_total + self.robot_sub_total) - self.payment_total), '.2f') )

	def profit_percent_user(self):
		from Stark_panel.st_modules import get_final_total
		final_total = get_final_total(self)
		if (self.payment_total - self.robot_sub_total) == 0:
			return float( format( (final_total + self.impression_total) * 100, '.2f') )
		return float( format( (((final_total + self.impression_total) / (self.payment_total - self.robot_sub_total)) - 1) * 100, '.2f') )

	def get_userStokes(self, tokenTitle):
		from Stark_panel.models import UserStoke, ChartTokenPrice
		user_stw_stoke = UserStoke.objects.filter(user=self, token__title__iexact=tokenTitle).first()
		if user_stw_stoke:
			user_stw_stoke = user_stw_stoke.count
		if user_stw_stoke is None:
			user_stw_stoke = 0
		
		pr_dollar_st = ChartTokenPrice.objects.filter(token__title=tokenTitle).last()
		if pr_dollar_st:
			pr_dollar_st = pr_dollar_st.price_dollar
		if pr_dollar_st is None:
			pr_dollar_st = 0
		return (user_stw_stoke * pr_dollar_st)

	def final_total(self):
		st1_out = self.get_userStokes(tokenTitle='ST1')
		st2_out = self.get_userStokes(tokenTitle='ST2')
		st3_out = self.get_userStokes(tokenTitle='ST3')
		st4_out = self.get_userStokes(tokenTitle='ST4')
		return (self.stoke + st1_out + st2_out + st3_out + st4_out)

	# used from under functions
	def get_just_count_Usertoken(self, token):
		from Stark_panel.models import UserStoke
		user_stw_stoke = UserStoke.objects.filter(user=self, token__title__iexact=token).first()
		if user_stw_stoke:
			user_stw_stoke = user_stw_stoke.count
		if user_stw_stoke is None:
			user_stw_stoke = 0
		return float(user_stw_stoke)
	def get_st1_userStoke(self):
		return self.get_just_count_Usertoken(token='ST1')
	def get_st2_userStoke(self):
		return self.get_just_count_Usertoken(token='ST2')
	def get_st3_userStoke(self):
		return self.get_just_count_Usertoken(token='ST3')
	def get_st4_userStoke(self):
		return self.get_just_count_Usertoken(token='ST4')



	# defined to use from HB_Pannel.views.UpdateUser Class
	def get_absolute_url(self):
		return '/'
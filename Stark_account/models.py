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
	user_code = models.CharField( _('کدکاربری'), max_length=15, default=0, unique=True)
	stoke = models.FloatField( _('موجودی نقدی'), default=0)                   # دارایی نقد
	payment_total = models.FloatField( _('پرداختی کل کاربر'), default=0)      # پرداختی کل
	impression_total = models.FloatField( _('برداشتی کل کاربر'), default=0)   # دریافتی کل
	robot_sub_total = models.FloatField( _('اشتراک ربات'), default=0)          # اشتراک ربات
	avatar = models.ImageField( _('تصویر'), upload_to=upload_image_path_avatar, null=True, blank=True)
	national_code_image = models.ImageField( _('تصویر کدملی'), upload_to=upload_image_path_national_code, null=True, blank=True)
	national_code = models.CharField( _('کدملی'), max_length=25, blank=True, null=True)
	phone = models.CharField( _('شماره همراه'), max_length=20, blank=True, null=True, validators=[
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
			return format_html(f'<img src="{self.avatar.url}" style="height:80px !important; width:80px !important; border-radius: 7px;">')
		return '-'
	tag_avatar.short_description = _('تصویر کاربر ')

	def __str__(self):
		return self.user_code

	# defined to use from HB_Pannel.views.UpdateUser Class
	def get_absolute_url(self):
		return '/'
from datetime import datetime
from django.db import models
from Extentions.utils import get_filename_ext_rand, jalali_convertor_tokens
from django.db.models.signals import post_save
from Stark_account.models import User
from django.dispatch import receiver
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def upload_video_path(instance, filename):
	name, ext, rand = get_filename_ext_rand(filename)
	final_name = f"{rand}{ext}"
	return f"video_site/{final_name}"

def upload_img_poster_path(instance, filename):
	name, ext, rand = get_filename_ext_rand(filename)
	final_name = f"{rand}{ext}"
	return f"poster_site/{final_name}"

def upload_qrcode_image_path(instance, filename):
	name, ext, rand = get_filename_ext_rand(filename)
	final_name = f"{rand}{ext}"
	return f"qr_image_stark/{final_name}"

class SettingVideo(models.Model):
    CHOISE_FORMAT = (('video/mp4', 'video/mp4'), ('video/webm', 'video/webm'))
    CHOISE_LANG = (('en', _('انگیلیسی') ), ('fa', _('فارسی') ), ('ar', _('عربی') ))
    video_lang = models.CharField( _('زبان ویدئو'), max_length=5, default='en', choices=CHOISE_LANG)
    video = models.FileField( _('ویدئوی راهنما'), upload_to=upload_video_path, null=True, blank=True)
    ext = models.CharField( _('فرمت ویدئو'), max_length=10, default='video/mp4', choices=CHOISE_FORMAT)
    poster = models.ImageField( _('پوستر ویدئوی راهنما'), upload_to=upload_img_poster_path, null=True, blank=True)

    class Meta:
        verbose_name = _('تنظیمات ویدئو')
        verbose_name_plural = _('تنظیمات ویدئوها')
        ordering = ['id']

    def __str__(self):
        return f'{self.ext}'

class SettingCategory(models.Model):
    days = models.IntegerField( _('تعداد روزها'))
    free_days = models.IntegerField( _('تعداد روزهای هدیه'), blank=True, null=True)
    price = models.FloatField( _('قیمت تعرفه بر حسب تتر'))

    class Meta:
        verbose_name = _('تنظیمات تعرفه')
        verbose_name_plural = _('تنظیمات تعرفه ها')
        ordering = ['id']

    def __str__(self):
        return f'{self.days}'

class Stark_Setting(models.Model):
    wallet_addr = models.CharField( _('آدرس کیف پول'), max_length=60, default='no data' )
    img_qrcode = models.ImageField( _('تصویر کد کیوآر'), upload_to=upload_qrcode_image_path, null=True, blank=True)
    is_active = models.BooleanField( _('آیا این تنظیمات در پنل نشان داده شود؟'), default=False)

    class Meta:
        verbose_name = _('تنظیمات استارک')
        verbose_name_plural = _('تنظیمات استارک')
        ordering = ['id']
    
    def __str__(self):
        return self.wallet_addr

class NotifyModel(models.Model):
    title_fa = models.CharField( _('عنوان اعلان به فارسی'), max_length=60, blank=True, null=True)
    title_en = models.CharField( _('عنوان اعلان به انگلیسی'), max_length=60, blank=True, null=True)
    title_ar = models.CharField( _('عنوان اعلان به عربی'), max_length=60, blank=True, null=True)
    message_fa = models.TextField( _('متن اعلان به فارسی'), blank=True, null=True)
    message_en = models.TextField( _('متن اعلان به انگلیسی'), blank=True, null=True)
    message_ar = models.TextField( _('متن اعلان به عربی'), blank=True, null=True)
    link = models.URLField( _('لینک پیوست'), blank=True, null=True)
    date = models.DateTimeField( _('تاریخ و زمان'), default=datetime.now())
    send_mail = models.BooleanField( _('آیا ایمیل ارسال شود؟'), default=False, help_text= _('توجه: درنظر داشته باشید که بعد از زدن دکمه‌ی ذخبره، ایمیل به تمامی کاربران ارسال میشود.') )
    is_active = models.BooleanField( _('فعال / غیرفعال'), default=False)
    class Meta:
        verbose_name = _('اعلان')
        verbose_name_plural = _('اعلانات')
        ordering = ['id']

    def j_date(self):
        return jalali_convertor_tokens(self.date)
    j_date.short_description = _('تاریخ و زمان')

    def __str__(self):
        return f'{self.date}'

# update ST1 2 3 4 Token
@receiver(post_save, sender=NotifyModel)
def send_mail_toall(sender, instance, **kwargs):
    if instance.send_mail == True:
        mail_subject = _('استارک | اطلاعیه')
        if get_language() == 'fa':
            thelink = instance.link
            if not thelink:
                thelink = ''
            messagee = render_to_string('email_pallete/email_notify_fa.html', {
                'message': instance.message_fa,
                'title': instance.title_fa,
                'date': instance.date,
                'link': thelink,
            })
        elif get_language() == 'en':
            thelink = instance.link
            if not thelink:
                thelink = ''
            messagee = render_to_string('email_pallete/email_notify_en.html', {
                'message': instance.message_en,
                'title': instance.title_en,
                'date': instance.date,
                'link': thelink,
            })
        elif get_language() == 'ar':
            thelink = instance.link
            if not thelink:
                thelink = ''
            messagee = render_to_string('email_pallete/email_notify_ar.html', {
                'message': instance.message_ar,
                'title': instance.title_ar,
                'date': instance.date,
                'link': thelink,
            })
        to_email = User.objects.values_list('email', flat=True)
        msg_EMAIL = EmailMessage(
            mail_subject, messagee, from_email=settings.EMAIL_HOST_USER, to=to_email
        )
        msg_EMAIL.content_subtype = "html"
        msg_EMAIL.send()

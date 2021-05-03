from datetime import datetime
from django.db import models
from Extentions.utils import get_filename_ext_rand, jalali_convertor_tokens
from django.utils.translation import gettext_lazy as _

def upload_video_path(instance, filename):
	name, ext, rand = get_filename_ext_rand(filename)
	final_name = f"{rand}{ext}"
	return f"video_site/{final_name}"

def upload_img_poster_path(instance, filename):
	name, ext, rand = get_filename_ext_rand(filename)
	final_name = f"{rand}{ext}"
	return f"poster_site/{final_name}"

class SettingVideo(models.Model):
    CHOISE_FORMAT = (('video/mp4', 'video/mp4'), ('video/webm', 'video/webm'))
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

class NotifyModel(models.Model):
    title_fa = models.CharField( _('عنوان اعلان به فارسی'), max_length=60, blank=True, null=True)
    title_en = models.CharField( _('عنوان اعلان به انگلیسی'), max_length=60, blank=True, null=True)
    title_ar = models.CharField( _('عنوان اعلان به عربی'), max_length=60, blank=True, null=True)
    message_fa = models.TextField( _('متن اعلان به فارسی'), blank=True, null=True)
    message_en = models.TextField( _('متن اعلان به انگلیسی'), blank=True, null=True)
    message_ar = models.TextField( _('متن اعلان به عربی'), blank=True, null=True)
    link = models.URLField( _('لینک پیوست'), blank=True, null=True)
    date = models.DateTimeField( _('تاریخ و زمان'), default=datetime.now())
    is_active = models.BooleanField( _('فعال / غیرفعال'), default=False, blank=True, null=True )
    class Meta:
        verbose_name = _('اعلان')
        verbose_name_plural = _('اعلانات')
        ordering = ['id']

    def j_date(self):
        return jalali_convertor_tokens(self.date)
    j_date.short_description = _('تاریخ و زمان')

    def __str__(self):
        return f'{self.date}'
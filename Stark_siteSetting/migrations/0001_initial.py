# Generated by Django 3.2 on 2021-05-03 17:56

import Stark_siteSetting.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotifyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_fa', models.CharField(blank=True, max_length=60, null=True, verbose_name='عنوان اعلان به فارسی')),
                ('title_en', models.CharField(blank=True, max_length=60, null=True, verbose_name='عنوان اعلان به انگلیسی')),
                ('title_ar', models.CharField(blank=True, max_length=60, null=True, verbose_name='عنوان اعلان به عربی')),
                ('message_fa', models.TextField(blank=True, null=True, verbose_name='متن اعلان به فارسی')),
                ('message_en', models.TextField(blank=True, null=True, verbose_name='متن اعلان به انگلیسی')),
                ('message_ar', models.TextField(blank=True, null=True, verbose_name='متن اعلان به عربی')),
                ('link', models.URLField(blank=True, null=True, verbose_name='لینک پیوست')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 5, 3, 22, 26, 35, 348703), verbose_name='تاریخ و زمان')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True, verbose_name='فعال / غیرفعال')),
            ],
            options={
                'verbose_name': 'اعلان',
                'verbose_name_plural': 'اعلانات',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SettingCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.IntegerField(verbose_name='تعداد روزها')),
                ('free_days', models.IntegerField(blank=True, null=True, verbose_name='تعداد روزهای هدیه')),
                ('price', models.FloatField(verbose_name='قیمت تعرفه بر حسب تتر')),
            ],
            options={
                'verbose_name': 'تنظیمات تعرفه',
                'verbose_name_plural': 'تنظیمات تعرفه ها',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SettingVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to=Stark_siteSetting.models.upload_video_path, verbose_name='ویدئوی راهنما')),
                ('ext', models.CharField(choices=[('video/mp4', 'video/mp4'), ('video/webm', 'video/webm')], default='video/mp4', max_length=10, verbose_name='فرمت ویدئو')),
                ('poster', models.ImageField(blank=True, null=True, upload_to=Stark_siteSetting.models.upload_img_poster_path, verbose_name='پوستر ویدئوی راهنما')),
            ],
            options={
                'verbose_name': 'تنظیمات ویدئو',
                'verbose_name_plural': 'تنظیمات ویدئوها',
                'ordering': ['id'],
            },
        ),
    ]
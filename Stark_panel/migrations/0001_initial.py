# Generated by Django 3.2 on 2021-05-30 05:23

import Extentions.utils
import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='عنوان ارز')),
                ('price_doallr', models.FloatField(verbose_name='قیمت به دلار')),
                ('count', models.FloatField(verbose_name='تعداد')),
            ],
            options={
                'verbose_name': 'توکن',
                'verbose_name_plural': 'توکن ها',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='WalletOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='مبلغ')),
                ('type_order', models.CharField(choices=[('inc', 'افزایش موجودی'), ('dec', 'برداشت از موجودی')], default='inc', max_length=5, verbose_name='نوع درخواست')),
                ('wallet_address', models.CharField(max_length=42, verbose_name='آدرس کیف پول')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 5, 30, 9, 53, 42, 141998), verbose_name='تاریخ و زمان')),
                ('is_paid', models.BooleanField(default=False, verbose_name='پرداخت شده')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'عملیات کیف پول',
                'verbose_name_plural': 'عملیات های کیف پول',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=45, unique=True, validators=[django.core.validators.RegexValidator('\\d?\\w{10,45}$', message='فرمت کیف پول را اصلاح کنید.')], verbose_name='آدرس کیف پول')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 5, 30, 9, 53, 42, 141998), verbose_name='تاریخ و زمان خرید')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'کیف پول',
                'verbose_name_plural': 'کیف پول های کاربران',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserStoke',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.FloatField(verbose_name='تعداد دارایی')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 5, 30, 9, 53, 42, 141998), verbose_name='آخرین زمان ثبت دارایی')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userstokes', to='Stark_panel.token')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userstokes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'سهم کاربر',
                'verbose_name_plural': 'سهام کاربر',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_suppurt', models.BooleanField(default=False, verbose_name='آیا این پیام از طرف پشتیبان ارسال شود؟')),
                ('title', models.CharField(choices=[('crashPay', 'اشتراک ربات'), ('InOut', 'پرداختی / برداشتی'), ('buytoken', 'خرید ارز'), ('selltoken', 'فروش ارز')], default='crashPay', max_length=15, verbose_name='عنوان تیکت')),
                ('subject', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(5, 'موضوع تیکت نباید کمتر از 5 کاراکتر باشد.')], verbose_name='موضوع پیام')),
                ('message', models.TextField(verbose_name='متن پیام')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 5, 30, 9, 53, 42, 141998), verbose_name='تاریخ و زمان')),
                ('is_seen', models.BooleanField(default=False, verbose_name='دیده شده توسط پشتیبان:')),
                ('is_seen_user', models.BooleanField(default=False, verbose_name='دیده شده توسط کاربر:')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'تیکت',
                'verbose_name_plural': 'تیکت ها',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RobotSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_code', models.CharField(default=Extentions.utils.get_bot_code, max_length=20, unique=True, verbose_name='کد ربات')),
                ('time_subscription', models.CharField(max_length=50, verbose_name='مدت اشتراک')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 5, 30, 9, 53, 42, 141998), verbose_name='تاریخ و زمان خرید')),
                ('is_paid', models.BooleanField(default=False, verbose_name='پرداخت شده')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال / غیرفعال')),
                ('last_date', models.DateTimeField(default=datetime.datetime(2021, 5, 30, 9, 53, 42, 141998), verbose_name='تاریخ و زمان انقضا')),
                ('is_expired', models.BooleanField(default=False, verbose_name='منقضی شده؟')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='robots', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'اشتراک ربات',
                'verbose_name_plural': 'اشتراک ربات ها',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ChartTokenPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_dollar', models.FloatField(verbose_name='قیمت به دلار')),
                ('date', models.DateField(verbose_name='تاریخ')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charts', to='Stark_panel.token')),
            ],
            options={
                'verbose_name': 'قیمت دوره ای توکن',
                'verbose_name_plural': 'قیمت های توکن',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='BuyAndSell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.FloatField(verbose_name='تعداد')),
                ('buy_sell', models.CharField(choices=[('buy', 'خرید'), ('sell', 'فروش')], default='buy', max_length=10, verbose_name='خرید یا فروش؟')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 5, 30, 9, 53, 42, 141998), verbose_name='تاریخ و زمان')),
                ('is_paid', models.BooleanField(default=False, verbose_name='پرداخت شده')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buysells', to='Stark_panel.token')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buysells', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'خرید و فروش',
                'verbose_name_plural': 'خرید و فروش ها',
                'ordering': ['id'],
            },
        ),
    ]

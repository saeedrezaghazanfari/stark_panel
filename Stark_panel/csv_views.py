import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from Stark_account.models import User
from Extentions.utils import jalali_convertor_tokens, jalali_convertor
from .st_modules import *
from .models import (
	ChartTokenPrice, RobotSubscription, BuyAndSell, Ticket, Token, UserStoke, UserWallet, WalletOrder
) 
from .mixins import (
	superuser_required_decorator, active_required_decorator
)
# ######### Download CSV File ######### #

# csvHome in django admin
@active_required_decorator(login_url='/sign-in')
@superuser_required_decorator(login_url='/')
def admin_page_download_page(request):
	return render(request, 'admin/database_export.html')

# user csv
@active_required_decorator(login_url='/sign-in')
@superuser_required_decorator(login_url='/')
def user_csv(request):
	response = HttpResponse(content_type='text/csv')
	response.write(u'\ufeff'.encode('utf8'))
	writer = csv.writer(response)

	writer.writerow([
		_('آیدی در دیتابیس'),
		_('کدکاربری'),
		_('نام کاربری'),
		_('ایمیل'),
		_('نام'),
		_('نام خانوادگی'),
		_('فعال/غیرفعال'),
		_('وضعیت حسابدار'),
		_('وضعیت پشتیبان'),
		_('وضعیت ادمین'),
		_('شماره همراه'),
		_('کدملی'),
		_('موجودی فعلی'),
		_('کل پرداختی'),
		_('کل برداشتی'),
		_('اشتراک ربات'),
		_('موجودی کل'),
		_('تاریخ پیوستن'),
		_('آخرین ورود'),
	])

	if get_language() == 'fa':
		for user in User.objects.all():
			writer.writerow([
				user.id, 
				user.user_code, 
				user.username, 
				user.email, 
				user.first_name, 
				user.last_name, 
				user.is_active, 
				user.is_acountants, 
				user.is_suppurt, 
				user.is_superuser, 
				user.phone, 
				user.national_code, 
				user.stoke, 
				user.payment_total ,
				user.impression_total ,
				user.robot_sub_total ,
				get_final_total(user), 
				jalali_convertor(user.date_joined), 
				jalali_convertor(user.last_login)
			])

		response['Content-Disposition'] = 'attachment; filename="user_table.csv"'
		return response
	else:
		for user in User.objects.all():
			writer.writerow([
				user.id, 
				user.user_code, 
				user.username, 
				user.email, 
				user.first_name, 
				user.last_name, 
				user.is_active, 
				user.is_acountants, 
				user.is_suppurt, 
				user.is_superuser, 
				user.phone, 
				user.national_code, 
				user.stoke, 
				user.payment_total ,
				user.impression_total ,
				user.robot_sub_total ,
				get_final_total(user), 
				user.date_joined,
				user.last_login
			])

		response['Content-Disposition'] = 'attachment; filename="user_table.csv"'
		return response

# bot csv
@active_required_decorator(login_url='/sign-in')
@superuser_required_decorator(login_url='/')
def bot_csv(request):
	response = HttpResponse(content_type='text/csv')
	response.write(u'\ufeff'.encode('utf8'))
	writer = csv.writer(response)

	writer.writerow([
		_('آیدی در دیتابیس'),
		_('کدربات'),
		_('نام کاربری کاربر'),
		_('مدت اشتراک'),
		_('تاریخ و زمان'),
		_('پرداخت شده'),
		_('تاریخ و زمان انقضا'),
		_('فعال/غیرفعال'),
		_('منقضی شده؟'),
	])
	if get_language() == 'fa':
		for bot in RobotSubscription.objects.all():
			writer.writerow([
				bot.id, 
				bot.bot_code, 
				bot.user.username, 
				bot.time_subscription, 
				jalali_convertor(bot.date), 
				bot.is_paid, 
				jalali_convertor(bot.last_date), 
				bot.is_active,
				bot.is_expired,
			])
		response['Content-Disposition'] = 'attachment; filename="robot_subscription_table.csv"'
		return response

	else:
		for bot in RobotSubscription.objects.all():
			writer.writerow([
				bot.id, 
				bot.bot_code, 
				bot.user.username, 
				bot.time_subscription, 
				bot.date,
				bot.is_paid, 
				bot.last_date,
				bot.is_active,
				bot.is_expired,
			])
		response['Content-Disposition'] = 'attachment; filename="robot_subscription_table.csv"'
		return response

# token csv
@active_required_decorator(login_url='/sign-in')
@superuser_required_decorator(login_url='/')
def token_csv(request):
	response = HttpResponse(content_type='text/csv')
	response.write(u'\ufeff'.encode('utf8'))
	writer = csv.writer(response)

	writer.writerow([
		_('عنوان ارز'),
		_('قیمت به دلار'),
		_('تعداد'),
	])

	for token in Token.objects.all():
		writer.writerow([token.title, token.price_doallr, token.count])

	response['Content-Disposition'] = 'attachment; filename="token_table.csv"'
	return response

# ticket csv
@active_required_decorator(login_url='/sign-in')
@superuser_required_decorator(login_url='/')
def ticket_csv(request):
	response = HttpResponse(content_type='text/csv')
	response.write(u'\ufeff'.encode('utf8'))
	writer = csv.writer(response)

	writer.writerow([
		_('ارسال توسط پشتیبان'),
		_('نام کاربری کاربر'),
		_('عنوان تیکت'),
		_('موضوع تیکت' ),
		_('متن تیکت'),
		_('ارسال از پشتیبان بوده؟'),
		_('تاریخ و زمان ارسال'),
		_('دیده شده توسط پشتیبان'),
		_('دیده شده توسط کاربر'),
	])
	if get_language() == 'fa':
		for ticket in Ticket.objects.all():
			writer.writerow([
				ticket.is_suppurt,
				ticket.user.username, 
				ticket.title, 
				ticket.subject, 
				ticket.message, 
				ticket.is_suppurt, 
				jalali_convertor(ticket.date), 
				ticket.is_seen,
				ticket.is_seen_user,
			])
		response['Content-Disposition'] = 'attachment; filename="ticket_table.csv"'
		return response
	else:
		for ticket in Ticket.objects.all():
			writer.writerow([
				ticket.is_suppurt,
				ticket.user.username, 
				ticket.title, 
				ticket.subject, 
				ticket.message, 
				ticket.is_suppurt, 
				ticket.date, 
				ticket.is_seen,
				ticket.is_seen_user,
			])

		response['Content-Disposition'] = 'attachment; filename="ticket_table.csv"'
		return response

# buy_sell csv
@active_required_decorator(login_url='/sign-in')
@superuser_required_decorator(login_url='/')
def buy_sell_csv(request):
	response = HttpResponse(content_type='text/csv')
	response.write(u'\ufeff'.encode('utf8'))
	writer = csv.writer(response)

	writer.writerow([
		_('نام کاربری کاربر'),
		_('نام ارز'),
		_('تعداد ارز'),
		_('خرید/فروش'),
		_('تاریخ و زمان'),
		_('پرداخت شده؟'),
	])
	if get_language() == 'fa':
		for buy_sell in BuyAndSell.objects.all():
			writer.writerow([
				buy_sell.user.username, 
				buy_sell.token, 
				buy_sell.count, 
				buy_sell.buy_sell, 
				jalali_convertor(buy_sell.date), 
				buy_sell.is_paid
			])
		response['Content-Disposition'] = 'attachment; filename="buy_sell_table.csv"'
		return response
	else:
		for buy_sell in BuyAndSell.objects.all():
			writer.writerow([
				buy_sell.user.username, 
				buy_sell.token, 
				buy_sell.count, 
				buy_sell.buy_sell, 
				buy_sell.date, 
				buy_sell.is_paid
			])
		response['Content-Disposition'] = 'attachment; filename="buy_sell_table.csv"'
		return response

# user_stokes csv
@active_required_decorator(login_url='/sign-in')
@superuser_required_decorator(login_url='/')
def user_stokes_csv(request):
	response = HttpResponse(content_type='text/csv')
	response.write(u'\ufeff'.encode('utf8'))
	writer = csv.writer(response)

	writer.writerow([
		_('نام کاربری کاربر'),
		_('نام ارز'),
		_('تعداد دارایی'),
		_('آخرین زمان ثبت دارایی'),
	])
	if get_language() == 'fa':
		for userstoke in UserStoke.objects.all():
			writer.writerow([
				userstoke.user.username, 
				userstoke.token, 
				userstoke.count, 
				jalali_convertor(userstoke.date)
			])

		response['Content-Disposition'] = 'attachment; filename="user_stokes_table.csv"'
		return response
	else:
		for userstoke in UserStoke.objects.all():
			writer.writerow([
				userstoke.user.username, 
				userstoke.token, 
				userstoke.count, 
				userstoke.date
			])

		response['Content-Disposition'] = 'attachment; filename="user_stokes_table.csv"'
		return response

# chart_token_price csv
@active_required_decorator(login_url='/sign-in')
@superuser_required_decorator(login_url='/')
def chart_token_price_csv(request):
	response = HttpResponse(content_type='text/csv')
	response.write(u'\ufeff'.encode('utf8'))
	writer = csv.writer(response)

	writer.writerow([
		_('نام ارز'),
		_('قیمت به دلار'),
		_('تاریخ')
	])
	if get_language() == 'fa':
		for tokenprice in ChartTokenPrice.objects.all():
			writer.writerow([
				tokenprice.token, 
				tokenprice.price_dollar, 
				jalali_convertor_tokens(tokenprice.date)
			])

		response['Content-Disposition'] = 'attachment; filename="chart_token_price_table.csv"'
		return response
	else:
		for tokenprice in ChartTokenPrice.objects.all():
			writer.writerow([
				tokenprice.token, 
				tokenprice.price_dollar, 
				tokenprice.date
			])

		response['Content-Disposition'] = 'attachment; filename="chart_token_price_table.csv"'
		return response

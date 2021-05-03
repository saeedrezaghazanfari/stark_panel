# imports
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate, get_language
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View, UpdateView
from django.db.models import Q
from Stark_account.models import User
from Stark_siteSetting.models import SettingVideo, SettingCategory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from Extentions.utils import jalali_convertor

from .st_modules import *
from .models import (
	ChartTokenPrice, RobotSubscription, BuyAndSell, Ticket, Token, UserStoke, UserWallet, WalletOrder
) 
from .forms import (
	TicketForm, AddWalletUser, OrderWalletUserForm
)
from .mixins import (
	UpdateUserPermission, active_required_decorator
)

# change-language website
def change_lang(request):
	activate(request.GET.get('lang'))
	return redirect(request.GET.get('next'))


# home / index / dashboard
@active_required_decorator(login_url='/sign-in')
@login_required(login_url='/sign-in')
def home_page_pannel(request):
	fa_langcode = '/fa/' in request.path
	return render(request, 'user_panel.html', {
		'buy_sells_LAs': BuyAndSell.objects.filter(user__id=request.user.id).order_by('-id')[:10],
		'wallet_LAs': WalletOrder.objects.filter(user__id=request.user.id).order_by('-id')[:10],
		'bot_LAs': RobotSubscription.objects.filter(user__id=request.user.id).order_by('-id')[:10],

		'user_stoke_st3': request.user.userstokes.filter(token__title='ST3').first(),
		'user_stoke_st4': request.user.userstokes.filter(token__title='ST4').first(),
		'user_final_total': get_final_total(request.user),
		'profit': get_profit(request.user, 'profit'),
		'profit_percent': get_profit(request.user, 'percent'),

		# chart st3
		'prices_dollar_st3': get_chart(tokenName='ST3', typeOut='price', fa_lang_code=fa_langcode),
		'dates_st3': get_chart(tokenName='ST3', typeOut='date', fa_lang_code=fa_langcode),
		# chart st4
		'prices_dollar_st4': get_chart(tokenName='ST4', typeOut='price', fa_lang_code=fa_langcode),
		'dates_st4': get_chart(tokenName='ST4', typeOut='date', fa_lang_code=fa_langcode),
	})

# show charts
@active_required_decorator(login_url='/sign-in')
@login_required(login_url='/sign-in')
def show_chart_page(request, tokenTitle):
	fa_langcode = '/fa/' in request.path

	if tokenTitle == 'st1':
		return render(request, 'view_charts.html', {
			# chart st1
			'prices_dollar': get_chart(tokenName='ST1', typeOut='price', fa_lang_code=fa_langcode, num_last=30),
			'dates': get_chart(tokenName='ST1', typeOut='date', fa_lang_code=fa_langcode, num_last=30),
			'tokenTitle': 'ST1',
			'user_token_stock': request.user.userstokes.filter(token__title='ST1').first(),
			'last_price_chart': get_last_price_token(tokenName='ST1'),
		})
	elif tokenTitle == 'st2':
		return render(request, 'view_charts.html', {
			# chart st2
			'prices_dollar': get_chart(tokenName='ST2', typeOut='price', fa_lang_code=fa_langcode, num_last=30),
			'dates': get_chart(tokenName='ST2', typeOut='date', fa_lang_code=fa_langcode, num_last=30),
			'tokenTitle': 'ST2',
			'user_token_stock': request.user.userstokes.filter(token__title='ST2').first(),
			'last_price_chart': get_last_price_token(tokenName='ST2'),
		})
	elif tokenTitle == 'st3':
		return render(request, 'view_charts.html', {
			# chart st3
			'prices_dollar': get_chart(tokenName='ST3', typeOut='price', fa_lang_code=fa_langcode, num_last=30),
			'dates': get_chart(tokenName='ST3', typeOut='date', fa_lang_code=fa_langcode, num_last=30),
			'tokenTitle': 'ST3',
			'user_token_stock': request.user.userstokes.filter(token__title='ST3').first(),
			'last_price_chart': get_last_price_token(tokenName='ST3'),
		})
	elif tokenTitle == 'st4':
		return render(request, 'view_charts.html', {
			# chart st4
			'prices_dollar': get_chart(tokenName='ST4', typeOut='price', fa_lang_code=fa_langcode, num_last=30),
			'dates': get_chart(tokenName='ST4', typeOut='date', fa_lang_code=fa_langcode, num_last=30),
			'tokenTitle': 'ST4',
			'user_token_stock': request.user.userstokes.filter(token__title='ST4').first(),
			'last_price_chart': get_last_price_token(tokenName='ST4'),
		})

# user wallet
@active_required_decorator(login_url='/sign-in')
@login_required(login_url='/sign-in')
def user_wallet(request):
	
	thisUser = request.user
	orderwallet_form = OrderWalletUserForm(request.POST or None)
	
	context = {
		'wallet_LAs': WalletOrder.objects.filter(user__id=request.user.id).order_by('-id')[:30],
		'wallets': UserWallet.objects.filter(user=thisUser).order_by('-id'),
		'orderwallet_form': orderwallet_form,
		'counter_wallets': UserWallet.objects.filter(user=thisUser).count(),
	}
	if orderwallet_form.is_valid():
		orderWallet = orderwallet_form.save(commit=False)
		if orderWallet.price == 0:
			messages.info(request, _('میزان درخواستی را کنترل کنید.') )
			return redirect('pannel:userWallet')
		orderWallet.wallet_address = request.POST.get('userwalletaddress')
		orderWallet.user = thisUser
		orderWallet.date = datetime.now()
		orderWallet.save()
		# send ticket
		if orderwallet_form.cleaned_data.get('type_order') == 'inc':
			if get_language() == 'en': 
				msg = f"My UserID {thisUser.user_code}; I have a Request to increase wallet balance with {request.POST.get('userwalletaddress')} for {orderwallet_form.cleaned_data.get('price')}USDT. Thanks"
				sub = 'Request to Increase Wallet Balance'
			elif  get_language() == 'fa':
				msg = f"اینجانب با کد کاربری {thisUser.user_code} درخواست افزایش موجودی کیف پول با آدرس {request.POST.get('userwalletaddress')} به مبلغ {orderwallet_form.cleaned_data.get('price')} تتر را دارم. باتشکر"
				sub = 'درخواست افزایش موجودی کیف پول'
			elif  get_language() == 'ar':
				msg = f"اسمی المستخدم {thisUser.user_code} طلب زيادة رصيد المحفظة مع طلب آدر.{request.POST.get('userwalletaddress')} لـ {orderwallet_form.cleaned_data.get('price')}USDT لدي. شكرا"
				sub = 'طلب زيادة رصيد المحفظة'

			Ticket.objects.create(
				user=thisUser, 
				subject=sub, 
				title='InOut', 
				message=msg,
				date=datetime.now()
			)
		elif orderwallet_form.cleaned_data.get('type_order') == 'dec':
			if  get_language() == 'en':
				msg = f"My UserName and UserID {thisUser.user_code}; I have a Request to Withdrawal wallet balance with {request.POST.get('userwalletaddress')} for {orderwallet_form.cleaned_data.get('price')}USDT. Thanks"
				sub = 'Request withdrawal from Wallet balance'
			elif  get_language() == 'fa':
				msg = f"اینجانب با نام و کد کاربری {thisUser.user_code} درخواست برداشت از کیف پول با آدرس {request.POST.get('userwalletaddress')} مبلغ {orderwallet_form.cleaned_data.get('price')}  تتر را دارم. باتشکر"
				sub = 'درخواست برداشت از موجودی کیف پول'
			elif  get_language() == 'ar':
				msg = f"اسمي المستخدم {thisUser.user_code} طلب سحب من رصيد المحفظة مع طلب آدر.{request.POST.get('userwalletaddress')} لـ {orderwallet_form.cleaned_data.get('price')}USDT لدي. شكرا"
				sub = 'طلب سحب من رصيد المحفظة'

			Ticket.objects.create(
				user=thisUser, 
				subject=sub, 
				title='InOut', 
				message=msg,
				date=datetime.now()
			)

		context['orderwallet_form'] = orderwallet_form
		messages.info(request, _('درخواست شما ارسال شد. نتیجه‌ی عملیات از طریق تیکت ارسال میشود.')) 

	return render(request, 'wallet.html', context)


# add wallet user
class UserWallet_GetCreate(LoginRequiredMixin, View):
	def post(self, request):
		# create wallet
		if not request.POST.get('walletid'):
			walletAddr = request.POST.get('address')
			checkForm = AddWalletUser(request.POST or None)

			if checkForm.is_valid():
				counter = UserWallet.objects.filter(user=request.user).count()
				if counter < 6:
					newWallet = UserWallet.objects.create(user=request.user, address=walletAddr, date=datetime.now())
					messages.info(request, _('آدرس کیف پول شما با موفقیت اضافه شد.'))
					return redirect('pannel:userWallet')
				else:
					messages.info(request, _('حداکثر تعداد کیف پول 6 عدد میباشد.') )
					return redirect('pannel:userWallet')

			else:
				messages.info(request, _('خطایی در ثبت کیف پول به وجود آمد.') )
				return redirect('pannel:userWallet')

		# delete wallet
		else:
			if request.POST.get('sure-del-wallet'):
				UserWallet.objects.get(id=request.POST.get('walletid')).delete()
				messages.info(request, _('کیف پول با موفقیت حذف شد.') )
				return redirect('pannel:userWallet')
			else:
				messages.info(request, _('از حذف کیف پول خود مطمئن شوید.') )
				return redirect('pannel:userWallet')	

# Robot subscription
@active_required_decorator(login_url='/sign-in')
@login_required(login_url='/sign-in')
def robot_subscription(request):
	thisUser = request.user
	
	context = {
		'bot_categories': SettingCategory.objects.order_by('id'),
		'videos': SettingVideo.objects.all(),
	}
	if request.POST:
		if request.POST.get('ensure-pay-bot'):
			if not request.POST.get('type-bot-sub') == 'none':
				if not RobotSubscription.objects.filter(user=thisUser, is_expired=False).first() or not RobotSubscription.objects.filter(user=thisUser).first():
					
					time_subscription = request.POST.get('type-bot-sub')
					priceCate = SettingCategory.objects.filter(days=int(time_subscription)).first().price

					if priceCate == 0 and RobotSubscription.objects.filter(user=thisUser, time_subscription=time_subscription).first():
						messages.info(request, _('شما یک بار از تعرفه‌ی رایگان ما استفاده کرده‌اید.') )
						return redirect('pannel:robot')
					
					bot_reserve = RobotSubscription.objects.create(user=thisUser, time_subscription=time_subscription, is_paid=True, date=datetime.now(), last_date=datetime.now() + timedelta(days=int(time_subscription)))
					thisUser.stoke -= priceCate
					thisUser.save()
					
					if '/en/' in request.path:
						msg = f'My UserID {thisUser.user_code}; I am requesting a robot subscription {time_subscription}. Thanks'
						Ticket.objects.create(user=thisUser, subject='Request a Robot Subscription', title='crashPay', message=msg, date=datetime.now())
					elif '/fa/' in request.path:
						msg = f'اینجانب با کد کاربری {thisUser.user_code} درخواست اشتراک ربات { time_subscription }روزه را دارم. باتشکر'
						Ticket.objects.create(user=thisUser, subject='درخواست اشتراک ربات', title='crashPay', message=msg, date=datetime.now())
					elif '/ar/' in request.path:
						msg = f'لدي اسم مستخدم {thisUser.user_code} أطلب اشتراكًا في الروبوت {time_subscription} سريعًا. شكرا'
						Ticket.objects.create(user=thisUser, subject='طلب اشتراك روبوت', title='crashPay', message=msg, date=datetime.now())
					
					messages.info(request, _('درخواست شما ارسال شد. نتیجه‌ی عملیات از طریق تیکت ارسال میشود.') )
					return redirect('pannel:robot')
				
				else:
					messages.info(request, _('شما درحال حاظر یک ربات فعال دارید.') )
					return redirect('pannel:robot')
			else:
				messages.info(request, _('باید یک تعرفه انتخاب کنید.') )
				return redirect('pannel:robot')
		else:
			messages.info(request, _('برای نهایی کردن خرید باید از خرید خود مطمئن باشید.') )
			return redirect('pannel:robot')

	return render(request, 'bot_subscription.html', context)


# all ticket
@active_required_decorator(login_url='/sign-in')
@login_required(login_url='/sign-in')
def all_tickets(request):
	return render(request, 'ticket_all.html', {
		'tickets': Ticket.objects.filter(user=request.user).order_by('-id')[:20],
		'unreaduser_tickets': Ticket.objects.filter(user=request.user, is_seen_user=False, is_suppurt=True).order_by('-id')
	})


# add ticket
@active_required_decorator(login_url='/sign-in')
@login_required(login_url='/sign-in')
def add_tickets(request):
	ticket_form = TicketForm(request.POST or None)
	context = {
		'ticket_form': ticket_form,
	}
	if request.POST:
		if ticket_form.is_valid():
			ticketForm = ticket_form.save(commit=False)
			ticketForm.user = request.user
			ticketForm.save()

			messages.info(request, _('تیکت شما با موفقیت ارسال شد.') )
			return redirect('pannel:allTicket')
	return render(request, 'ticket_add.html', context)


# detail ticket
@active_required_decorator(login_url='/sign-in')
@login_required(login_url='/sign-in')
def detail_tickets(request, filterticket):
	context = {'tickets': None}
	if filterticket == 'bot-sub':
		context['tickets'] = Ticket.objects.filter(user=request.user, title='crashPay').order_by('-id')
		for tick in Ticket.objects.filter(user=request.user, title='crashPay', is_seen_user=False).all():
			tick.is_seen_user = True
			tick.save()
		return render(request, 'ticket_detail.html', context)

	elif filterticket == 'in-out':
		context['tickets'] = Ticket.objects.filter(user=request.user, title='InOut').order_by('-id')
		for tick in Ticket.objects.filter(user=request.user, title='InOut', is_seen_user=False).all():
			tick.is_seen_user = True
			tick.save()
		return render(request, 'ticket_detail.html', context)

	elif filterticket == 'buy-sell':
		lookup = Q(title='buytoken') | Q(title='selltoken') 
		context['tickets'] = Ticket.objects.filter(lookup, user=request.user).order_by('-id')
		for tick in Ticket.objects.filter(lookup, user=request.user, is_seen_user=False).all():
			tick.is_seen_user = True
			tick.save()
		return render(request, 'ticket_detail.html', context)


# update user data
class UpdateUser(UpdateUserPermission, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
	model = User
	pk_url_kwarg = 'userID'
	success_message = _('اطلاعات شما با موفقیت ذخیره شد.')
	fields = ['first_name', 'last_name' ,'avatar', 'national_code', 'national_code_image', 'phone']
	template_name = 'update_user.html'

# change user password
@active_required_decorator(login_url='/sign-in')
@login_required(login_url='/sign-in')
def change_password(request):
	chpw_form = PasswordChangeForm(user=request.user, data=request.POST)
	context = {
		'chpw_form': chpw_form,
	}
	if chpw_form.is_valid():
		old_pass = chpw_form.cleaned_data.get('old_password')
		password = chpw_form.cleaned_data.get('new_password1')
		thisUser = User.objects.get(id=request.user.id)

		# check the chars persian
		for i in password:
			if ord(i) > 1000:
				messages.info(request, _('رمزعبور باید شامل حروف انگلیسی، اعداد و علامت‌ها باشد.') )
				return redirect('pannel:changePw')

		# check old password
		if thisUser.check_password(old_pass):
			thisUser.set_password(password)
			thisUser.save()
			
			messages.info(request, _('پسورد شما با موفقیت تغییر کرد.') )
			messages.info(request, _('برای ورود اطلاعات خود را وارد کنید.') )
			return redirect('account:signin')
		chpw_form.add_error('old_password', _('پسورد شما اشتباه می‌باشد.') )

	return render(request, 'change_password.html', context)

# send request buy sell token
class BuySellTokenClassView(LoginRequiredMixin, View):
	def get(self, request):
		orderOpacity = request.GET.get('op')
		typeToken = request.GET.get('tk')

		if orderOpacity == '':
			orderOpacity = 0

		if typeToken == 'st1':
			price = 0
			lasttoken = ChartTokenPrice.objects.filter(token__title='ST1').last()
			if lasttoken:
				price = lasttoken.price_dollar
			output = float(orderOpacity) / float(price)
			output_formated = format(output, '.2f')
			return JsonResponse({'total': f'{output_formated} : ST1', 'status': 200})

		if typeToken == 'st2':
			price = 0
			lasttoken = ChartTokenPrice.objects.filter(token__title='ST2').last()
			if lasttoken:
				price = lasttoken.price_dollar
			output = float(orderOpacity) / float(price)
			output_formated = format(output, '.2f')
			return JsonResponse({'total': f'{output_formated} : ST2', 'status': 200})

		if typeToken == 'st3':
			price = 0
			lasttoken = ChartTokenPrice.objects.filter(token__title='ST3').last()
			if lasttoken:
				price = lasttoken.price_dollar
			output = float(orderOpacity) / float(price)
			output_formated = format(output, '.2f')
			return JsonResponse({'total': f'{output_formated} : ST3', 'status': 200})

		elif typeToken == 'st4':
			price = 0
			lasttoken = ChartTokenPrice.objects.filter(token__title='ST4').last()
			if lasttoken:
				price = lasttoken.price_dollar
			output = float(orderOpacity) / float(price)
			output_formated = format(output, '.2f')
			return JsonResponse({'total': f'{output_formated} : ST4', 'status': 200})

# send ticket to buy_sell
@active_required_decorator(login_url='/sign-in')
@login_required(login_url='/sign-in')
def buy_sell_sendticket(request):
	if request.POST:
		thisUser = request.user
		typeToken = request.POST.get('type-token')
		typeOrder = request.POST.get('type-order')
		opacityOrder = request.POST.get('opacity-order')

		if not opacityOrder:
			opacityOrder = 0

		if typeToken == 'st1':
			price = 0
			lasttoken = ChartTokenPrice.objects.filter(token__title='ST1').last()
			if lasttoken:
				price = lasttoken.price_dollar

		if typeToken == 'st2':
			price = 0
			lasttoken = ChartTokenPrice.objects.filter(token__title='ST2').last()
			if lasttoken:
				price = lasttoken.price_dollar

		if typeToken == 'st3':
			price = 0
			lasttoken = ChartTokenPrice.objects.filter(token__title='ST3').last()
			if lasttoken:
				price = lasttoken.price_dollar
			
		elif typeToken == 'st4':
			price = 0
			lasttoken = ChartTokenPrice.objects.filter(token__title='ST4').last()
			if lasttoken:
				price = lasttoken.price_dollar

		if not int(opacityOrder) == 0:
			if typeOrder == 'buytoken':
				buysell_token_order = 'buy'
				if get_language() == 'en':
					sub = f'Request to Buy {typeToken} Token'
					msg =f'My UserID {thisUser.user_code}; I have a request to Buy {typeToken} tokens to {float(opacityOrder) / float (price)} for the calculated price {opacityOrder} USDT. Thanks'
				
				elif get_language() == 'fa':
					sub = f'درخواست خرید توکن {typeToken}'
					msg =f'اینجانب با کد کاربری {thisUser.user_code} درخواست خرید توکن {typeToken} را به تعداد {float(opacityOrder) / float (price)} را به قیمت محاسبه شده ی {opacityOrder} تتر دارم. باتشکر'
				
				elif get_language() == 'ar':
					sub = f'طلب شراء رمز مميز {typeToken}'
					msg =f'لدي اسم الرمز طلب {thisUser.user_code} لشراء {typeToken} کن تعداد {float(opacityOrder) / float (price)} به بالسعر المحسوب {opacityOrder} USDT. شكرا'

			elif typeOrder == 'selltoken':
				buysell_token_order = 'sell'
				if get_language() == 'en':
					sub = f'Request to Sell {typeToken} Token'
					msg =f'My UserID {thisUser.user_code}; I have a request to sell {typeToken} tokens to {float(opacityOrder) / float (price)} for the calculated price {opacityOrder} USDT. Thanks'
				elif get_language() == 'fa':
					sub = f'درخواست فروش توکن {typeToken}'
					msg =f'اینجانب با کد کاربری {thisUser.user_code} درخواست فروش توکن {typeToken} را به تعداد {float(opacityOrder) / float (price)} را به قیمت محاسبه شده ی {opacityOrder} تتر دارم. باتشکر'
				elif get_language() == 'ar':
					sub = f'طلب بیع رمز مميز {typeToken}'
					msg =f'لدي اسم الرمز طلب {thisUser.user_code} لبیع {typeToken} کن تعداد {float(opacityOrder) / float (price)} به بالسعر المحسوب {opacityOrder} USDT. شكرا'

			Ticket.objects.create(
				user=thisUser, 
				title=typeOrder, 
				subject= sub,
				message=msg,
				date=datetime.now()
			)

			messages.info(request, _('درخواست شما ارسال شد. نتیجه‌ی عملیات از طریق تیکت ارسال میشود.') )
			return redirect('pannel:buySellToken', typeToken)

		else:
			messages.info(request, _('میزان درخواستی را کنترل کنید.') )
			return redirect('pannel:buySellToken', typeToken)

# send_ticket buy sell
@active_required_decorator(login_url='/sign-in')
@login_required(login_url='/sign-in')
def buy_sell_tokens(request, tokenNamekw):
	
	counter_st1 = 0
	sercher_st1 = UserStoke.objects.filter(user=request.user, token__title='ST1').last()
	if sercher_st1:
		counter_st1 = sercher_st1.count

	counter_st2 = 0
	sercher_st2 = UserStoke.objects.filter(user=request.user, token__title='ST2').last()
	if sercher_st2:
		counter_st2 = sercher_st2.count

	counter_st3 = 0
	sercher_st3 = UserStoke.objects.filter(user=request.user, token__title='ST3').last()
	if sercher_st3:
		counter_st3 = sercher_st3.count

	counter_st4 = 0
	sercher_st4 = UserStoke.objects.filter(user=request.user, token__title='ST4').last()
	if sercher_st4:
		counter_st4 = sercher_st4.count

	if tokenNamekw == 'st1':
		fa_langcode = '/fa/' in request.path
		context = {
			'user_token_st1_count': counter_st1,
			'user_token_st2_count': counter_st2,
			'user_token_st3_count': counter_st3,
			'user_token_st4_count': counter_st4,
			# chart st1
			'name_chart': 'ST1',
			'prices_dollar_chart': get_chart(tokenName='ST1', typeOut='price', fa_lang_code=fa_langcode),
			'dates_chart': get_chart(tokenName='ST1', typeOut='date', fa_lang_code=fa_langcode),
			'last_price_chart': get_last_price_token(tokenName='ST1'),
		}

	elif tokenNamekw == 'st2':
		fa_langcode = '/fa/' in request.path
		context = {
			'user_token_st1_count': counter_st1,
			'user_token_st2_count': counter_st2,
			'user_token_st3_count': counter_st3,
			'user_token_st4_count': counter_st4,
			# chart st2
			'name_chart': 'ST2',
			'prices_dollar_chart': get_chart(tokenName='ST2', typeOut='price', fa_lang_code=fa_langcode),
			'dates_chart': get_chart(tokenName='ST2', typeOut='date', fa_lang_code=fa_langcode),
			'last_price_chart': get_last_price_token(tokenName='ST2'),
		}

	elif tokenNamekw == 'st3':
		fa_langcode = '/fa/' in request.path
		context = {
			'user_token_st1_count': counter_st1,
			'user_token_st2_count': counter_st2,
			'user_token_st3_count': counter_st3,
			'user_token_st4_count': counter_st4,
			# chart st3
			'name_chart': 'ST3',
			'prices_dollar_chart': get_chart(tokenName='ST3', typeOut='price', fa_lang_code=fa_langcode),
			'dates_chart': get_chart(tokenName='ST3', typeOut='date', fa_lang_code=fa_langcode),
			'last_price_chart': get_last_price_token(tokenName='ST3'),
		}

	elif tokenNamekw == 'st4':
		fa_langcode = '/fa/' in request.path
		context = {
			'user_token_st1_count': counter_st1,
			'user_token_st2_count': counter_st2,
			'user_token_st3_count': counter_st3,
			'user_token_st4_count': counter_st4,
			# chart st4
			'name_chart': 'ST4',
			'prices_dollar_chart': get_chart(tokenName='ST4', typeOut='price', fa_lang_code=fa_langcode),
			'dates_chart': get_chart(tokenName='ST4', typeOut='date', fa_lang_code=fa_langcode),
			'last_price_chart': get_last_price_token(tokenName='ST4'),
		}
	return render(request, 'buy_sell_tokens.html', context)


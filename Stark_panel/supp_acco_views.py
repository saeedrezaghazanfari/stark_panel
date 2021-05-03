
from django.contrib import messages
from datetime import datetime
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import View, ListView
from django.db.models import Q
from django.utils.translation import get_language
from Stark_account.models import User
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
	RobotSubscription, BuyAndSell, Ticket, UserStoke, WalletOrder, UserWallet, ChartTokenPrice
) 
from .forms import (
	RobotSubscriptionForm, TicketForm, TicketResponseForm, AddToChart, SendTicket_OneUser, UserStoke_Form, BuyAndSell_Form, AddBotSubForm, WalletOrderAddForm
)
from .mixins import (
	AcountantPermision, acountants_required_decorator, suppurt_required_decorator, active_required_decorator
)

# define get absoulute url handle
def get_url_absolute():
	lang = get_language()
	if lang == 'fa':
		return '/fa/acountants/'
	elif lang == 'en':
		return '/en/acountants/'
	elif lang == 'ar':
		return '/ar/acountants/'

# list of users
@active_required_decorator(login_url='/sign-in')
@suppurt_required_decorator(login_url='/')
def suppurt_home_page(request):
	return render(request, 'is_supporter/supporter_panel.html', {
		'unread_tickets': Ticket.objects.filter(is_suppurt=False, is_seen=False).order_by('-id'),
	})

@active_required_decorator(login_url='/sign-in')
@suppurt_required_decorator(login_url='/')
def suppurt_set_useraccount_page(request):
	if request.POST:
		payment_total = request.POST.get('payment-total')
		account_total = request.POST.get('account-total')
		user_codee = request.POST.get('user-code')
		impre_total = request.POST.get('impre-total')
		robot_sub_total = request.POST.get('robot-sub-total')

		if not account_total:
			account_total = 0
		if not payment_total:
			payment_total = 0
		if not impre_total:
			impre_total = 0
		if not robot_sub_total:
			robot_sub_total = 0
		if not user_codee:
			messages.info(request, _('مشکلی رخ داده است.') )
			return redirect('pannel:su_home')

		if account_total and payment_total and impre_total and user_codee:
			sel_user = User.objects.filter(user_code=user_codee).first()
			sel_user.stoke = account_total
			sel_user.payment_total = payment_total
			sel_user.impression_total = impre_total
			sel_user.robot_sub_total = robot_sub_total
			sel_user.save()
			messages.info(request, _('اطلاعات کاربر با موفقیت ذخیره شد.') )
			return redirect('pannel:su_useraccount')

	return render(request, 'is_supporter/support_set_user_acc.html', {
		'users': User.objects.filter(is_active=True).order_by('-id'),
	})

# send ticket to user
@active_required_decorator(login_url='/sign-in')
@suppurt_required_decorator(login_url='/')
def ticket_of_user_page(request, ticketID):

	thisTicket = Ticket.objects.get(id=ticketID)
	# seened
	if request.user.is_suppurt:
		thisTicket.is_seen = True
		thisTicket.save()

	ticket_form = TicketResponseForm(request.POST or None)
	# send ticket to user
	if ticket_form.is_valid():
		res = ticket_form.save(commit=False)
		res.user = thisTicket.user
		res.title = thisTicket.title
		res.is_suppurt = True
		res.is_seen = True
		res.date = datetime.now()
		res.save()
		messages.info(request, _('پیام شما با موفقیت ارسال شد.') )
		return redirect('pannel:su_home')

	return render(request, 'is_supporter/support_response.html', {
		'ticket_form': ticket_form,
		'ticket': thisTicket,
	})

# all of user tickets
@active_required_decorator(login_url='/sign-in')
@suppurt_required_decorator(login_url='/')
def tickets_all_user_page(request):
	return render(request, 'is_supporter/support_all_ticket.html', {
		'tickets': Ticket.objects.filter(is_suppurt=False).order_by('-id'),
	})

# send a ticket to one user
@active_required_decorator(login_url='/sign-in')
@suppurt_required_decorator(login_url='/')
def send_ticket_one_user_page(request):
	sendticket_form = SendTicket_OneUser(request.POST or None)
	context = {
		'sendticket_form': sendticket_form
	}
	if sendticket_form.is_valid():
		obj_ticket = sendticket_form.save(commit=False)
		obj_ticket.date = datetime.now()
		obj_ticket.is_suppurt = True
		obj_ticket.save()
		messages.info(request, _('پیام با موفقیت ارسال شد.') )
		return redirect('pannel:su_home')
	return render(request, 'is_supporter/support_sendticket_a_user.html', context)

# ############ end suppurt ############ #



# ################# is_acountants pages ################# # 

@active_required_decorator(login_url='/sign-in')
@acountants_required_decorator(login_url='/')
def acountants_home_page(request):
	addtocharrt_form = AddToChart(request.POST or None)
	context = {
		'addtocharrt_form': addtocharrt_form,
		# counters of tables
		'user_counter': User.objects.all().count(), 
		'walletaddr_counter': UserWallet.objects.all().count(), 
		'user_stoke_counter': UserStoke.objects.all().count(), 
		'bots_counter': RobotSubscription.objects.all().count(),
		'buysells_counter': BuyAndSell.objects.all().count(),
		'walletorder_counter': WalletOrder.objects.all().count(),
	}
	if addtocharrt_form.is_valid():
		newprice = addtocharrt_form.save(commit=False)
		newprice.date = datetime.now()
		newprice.save()
		messages.info(request, _('با موفقیت اضافه شد.') )
		return redirect('pannel:ac_home')
	return render(request, 'is_acountants/accountant_panel.html', context)

# user list
class AccountantUsers(AcountantPermision, LoginRequiredMixin, ListView):
	template_name='is_acountants/acountants_user.html'
	model = User
	queryset = User.objects.order_by('-id')	

# accountant token prices
class AccountantTokenPrice(AcountantPermision, LoginRequiredMixin, ListView):
	template_name='is_acountants/acountant_chart_token_price.html'
	model = ChartTokenPrice
	queryset = ChartTokenPrice.objects.order_by('-id')	

class AccountantUserWalletAddress(AcountantPermision, LoginRequiredMixin, ListView):
	template_name='is_acountants/accountant_wallet_addr.html'
	model = UserWallet
	queryset = UserWallet.objects.order_by('-id')	

# bot list
@active_required_decorator(login_url='/sign-in')
@acountants_required_decorator(login_url='/')
def accountant_bots_page(request):
	AddBotSubForm_form = AddBotSubForm(request.POST or None)
	context = {
		'add_form': AddBotSubForm_form,
		'object_list': RobotSubscription.objects.order_by('-id')
	}	
	if AddBotSubForm_form.is_valid():
		AddBotSubForm_form_obj = AddBotSubForm_form.save(commit=False)
		AddBotSubForm_form_obj.date = datetime.now()
		AddBotSubForm_form_obj.save()
		messages.info(request, _('اشتراک ربات کاربر ذخیره شد.') )
		return redirect('pannel:ac_bots')
	return render(request, 'is_acountants/accountant_bots.html', context)

# Wallet AddForm
@active_required_decorator(login_url='/sign-in')
@acountants_required_decorator(login_url='/')
def accountant_walletuser_page(request):
	WalletOrderAddForm_form = WalletOrderAddForm(request.POST or None)
	context = {
		'add_form': WalletOrderAddForm_form,
		'object_list': WalletOrder.objects.order_by('-id')
	}	
	if WalletOrderAddForm_form.is_valid():
		WalletOrderAddForm_obj = WalletOrderAddForm_form.save(commit=False)
		WalletOrderAddForm_obj.date = datetime.now()
		WalletOrderAddForm_obj.save()
		messages.info(request, _('عملیات کیف پول اضافه شد.') )
		return redirect('pannel:ac_walletorders')
	return render(request, 'is_acountants/accountant_walletusers.html', context)

# buy sell list
@active_required_decorator(login_url='/sign-in')
@acountants_required_decorator(login_url='/')
def accountant_buy_sells_page(request):
	buyandsell_form = BuyAndSell_Form(request.POST or None)
	context = {
		'add_form': buyandsell_form,
		'object_list': BuyAndSell.objects.order_by('-id'),
	}
	if buyandsell_form.is_valid():
		buyandsell_form_obj = buyandsell_form.save(commit=False)
		buyandsell_form_obj.date = datetime.now()
		buyandsell_form_obj.save()
		messages.info(request, _('خرید و فروش توکن کاربر ذخیره شد.') )
		return redirect('pannel:ac_buysells')
	return render(request, 'is_acountants/accountant_buy_sells.html', context)


# user stokes
@active_required_decorator(login_url='/sign-in')
@acountants_required_decorator(login_url='/')
def accountant_userStokes_page(request):
	userstoke_form = UserStoke_Form(request.POST or None)
	context = {
		'add_form': userstoke_form,
		'object_list': UserStoke.objects.order_by('-id'),
	}
	if userstoke_form.is_valid():
		user_get = userstoke_form.cleaned_data.get('user')
		token_get = userstoke_form.cleaned_data.get('token')
		count_get = userstoke_form.cleaned_data.get('count')

		user_ex = UserStoke.objects.filter(user=user_get, token=token_get).first()
		if user_ex:
			user_ex.count = count_get
			user_ex.date = datetime.now()
			user_ex.save()
			messages.info(request, _('توکن کاربر ذخیره شد.') )
			return redirect('pannel:ac_userStoke')
		else:
			userstoke_form_obj = userstoke_form.save(commit=False)
			userstoke_form_obj.date = datetime.now()
			userstoke_form_obj.save()
			messages.info(request, _('توکن کاربر ذخیره شد.') )
			return redirect('pannel:ac_userStoke')

	return render(request, 'is_acountants/accountant_user_stokes.html', context)



################### EDIT THE LISTS #####################


### edit userStoke
class AccountantUserStokes_Edit(LoginRequiredMixin, AcountantPermision, SuccessMessageMixin, UpdateView):
	template_name = 'is_acountants/list-editor/audit-user-stoke.html'
	model = UserStoke
	success_message = _('تغییرات اعمال شد.')
	def get_context_data(self, ** kwargs):
		context = super().get_context_data(** kwargs)
		context ['object'] = UserStoke.objects.get(id=self.kwargs['pk'])
		return context
	success_url = get_url_absolute()
	fields = ['user', 'token', 'count', 'date']

# edit token prices
class AccountantTokenPrice_Edit(LoginRequiredMixin, AcountantPermision, SuccessMessageMixin, UpdateView):
	template_name = 'is_acountants/list-editor/audit-token-price.html'
	model = ChartTokenPrice
	success_message = _('تغییرات اعمال شد.')
	def get_context_data(self, ** kwargs):
		context = super().get_context_data(** kwargs)
		context ['object'] = ChartTokenPrice.objects.get(id=self.kwargs['pk'])
		return context
	success_url = get_url_absolute()
	fields = ['token', 'price_dollar', 'date']

### edit user wallets
class AccountantWalletuser_Edit(LoginRequiredMixin, AcountantPermision, SuccessMessageMixin, UpdateView):
	template_name = 'is_acountants/list-editor/audit-user-wallets.html'
	model = WalletOrder
	success_message = _('تغییرات اعمال شد.')
	def get_context_data(self, ** kwargs):
		context = super().get_context_data(** kwargs)
		context ['object'] = WalletOrder.objects.get(id=self.kwargs['pk'])
		return context
	success_url = get_url_absolute()
	fields = ['user', 'price', 'type_order', 'wallet_address', 'date', 'is_paid']


### edit user wallets
class AccountantBots_Edit(LoginRequiredMixin, AcountantPermision, SuccessMessageMixin, UpdateView):
	template_name = 'is_acountants/list-editor/audit-bot-subs.html'
	model = RobotSubscription
	success_message = _('تغییرات اعمال شد.')
	def get_context_data(self, ** kwargs):
		context = super().get_context_data(** kwargs)
		context ['object'] = RobotSubscription.objects.get(id=self.kwargs['pk'])
		return context
	success_url = get_url_absolute()
	fields = ['bot_code', 'user', 'time_subscription', 'date', 'is_paid', 'is_active', 'last_date']

### edit user wallets
class AccountantBuySells_Edit(LoginRequiredMixin, AcountantPermision, SuccessMessageMixin, UpdateView):
	template_name = 'is_acountants/list-editor/audit-buy-sells.html'
	model = BuyAndSell
	success_message = _('تغییرات اعمال شد.')
	def get_context_data(self, ** kwargs):
		context = super().get_context_data(** kwargs)
		context ['object'] = BuyAndSell.objects.get(id=self.kwargs['pk'])
		return context
	success_url = get_url_absolute()
	fields = ['user', 'token', 'count', 'buy_sell', 'date', 'is_paid']
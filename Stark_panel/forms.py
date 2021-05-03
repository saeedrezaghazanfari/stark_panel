from django import forms
from .models import RobotSubscription, Ticket, ChartTokenPrice, BuyAndSell, UserWallet, WalletOrder, UserStoke
from Stark_account.models import User
from django.core import validators

class RobotSubscriptionForm(forms.ModelForm):
	class Meta:
		model = RobotSubscription
		fields = ['time_subscription']

class TicketForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ['title','subject','message']

class TicketResponseForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ['subject', 'message']

class AddToChart(forms.ModelForm):
	class Meta:
		model = ChartTokenPrice
		fields = ['token', 'price_dollar']

class AddWalletUser(forms.ModelForm):
	class Meta:
		model = UserWallet
		fields = ['address']

class OrderWalletUserForm(forms.ModelForm):
	class Meta:
		model = WalletOrder
		fields = ['price', 'type_order']

class SendTicket_OneUser(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ['user', 'title', 'subject', 'message']

class UserStoke_Form(forms.ModelForm):
	class Meta:
		model = UserStoke
		fields = ['user', 'token', 'count']

class BuyAndSell_Form(forms.ModelForm):
	class Meta:
		model = BuyAndSell
		fields = ['user', 'token', 'count', 'buy_sell', 'is_paid']

class AddBotSubForm(forms.ModelForm):
	class Meta:
		model = RobotSubscription
		fields = ['user', 'time_subscription', 'is_paid', 'is_active']

class WalletOrderAddForm(forms.ModelForm):
	class Meta:
		model = WalletOrder
		fields = ['user', 'price', 'type_order', 'wallet_address', 'is_paid']

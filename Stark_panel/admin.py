from django.contrib import admin
from .models import (
	ChartTokenPrice, Token, BuyAndSell, UserStoke, RobotSubscription, Ticket, UserWallet, WalletOrder
)

class ChartAdmin(admin.ModelAdmin):
	list_display = ['token', 'price_dollar', 'j_date']
	search_fields = ['token', 'price_dollar', 'j_date']
	ordering = ['-id']

class TokenAdmin(admin.ModelAdmin):
	list_display = ['title', 'price_doallr', 'count']
	search_fields = ['title', 'price_doallr']
	ordering = ['-id']

class BuyAndSellAdmin(admin.ModelAdmin):
	list_display = ['user', 'token', 'count', 'buy_sell', 'j_date', 'is_paid']
	search_fields = ['user', 'token', 'buy_sell', 'j_date', 'is_paid']
	ordering = ['-id']

class UserStokeAdmin(admin.ModelAdmin):
	list_display = ['user', 'token', 'count', 'j_date']
	search_fields = ['user', 'token', 'j_date']
	ordering = ['-id']

class UserWalletAdmin(admin.ModelAdmin):
	list_display = ['user', 'address', 'j_date']
	search_fields = ['user', 'address', 'j_date']
	ordering = ['-id']

class WalletOrderAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'price', 'type_order', 'wallet_address', 'j_date', 'is_paid']
	search_fields = ['__str__', 'price', 'type_order', 'wallet_address', 'j_date', 'is_paid']
	ordering = ['-id']

class RobotSubscriptionAdmin(admin.ModelAdmin):
	list_display = ['bot_code', 'user', 'time_subscription', 'j_date', 'is_paid', 'j_last_date', 'is_active', 'is_expired']
	search_fields = ['bot_code', 'user', 'time_subscription', 'j_date', 'is_paid', 'j_last_date', 'is_active', 'is_expired']
	ordering = ['-id']

class TicketAdmin(admin.ModelAdmin):
	list_display = ['user', 'title', 'subject', 'is_suppurt', 'j_date', 'is_seen']
	search_fields = ['user', 'title', 'subject', 'is_suppurt', 'j_date', 'is_seen']
	ordering = ['-id']

admin.site.register(ChartTokenPrice, ChartAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(BuyAndSell, BuyAndSellAdmin)
admin.site.register(UserStoke, UserStokeAdmin)
admin.site.register(UserWallet, UserWalletAdmin)
admin.site.register(WalletOrder, WalletOrderAdmin)
admin.site.register(RobotSubscription, RobotSubscriptionAdmin)
admin.site.register(Ticket, TicketAdmin)

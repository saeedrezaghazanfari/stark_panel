from django.urls import path
from . import views
from . import csv_views
from . import supp_acco_views

app_name="pannel"
urlpatterns = [

	# built-in
	path('', views.home_page_pannel, name="home"),
	path('change-lang/', views.change_lang, name="ch_lang"),
	path('robot-subscription/', views.robot_subscription, name="robot"),
	path('user/edit/<int:userID>', views.UpdateUser.as_view(), name='editUser'),
	path('user/change/password', views.change_password, name='changePw'),
	path('charts/show/<str:tokenTitle>', views.show_chart_page, name='show_charts'),

	# buy sell token
	path('buy-sells/<str:tokenNamekw>', views.buy_sell_tokens, name='buySellToken'),
	path('buy-sells/send-ticket/', views.buy_sell_sendticket, name='buySellTicketsend'),

	# user wallet
	path('user/wallet/', views.user_wallet, name='userWallet'),
	path('user/manage/wallet/', views.UserWallet_GetCreate.as_view(), name='manageUserWallet'),

	# tickets:
	path('ticket/all/', views.all_tickets, name="allTicket"),
	path('ticket/detail/<str:filterticket>', views.detail_tickets, name="detailTicket"),
	path('ticket/create/', views.add_tickets, name="addTicket"),

	# is_acountants pages
	path('acountants/', supp_acco_views.acountants_home_page, name="ac_home"),
	path('acountants/users', supp_acco_views.AccountantUsers.as_view(), name="ac_users"),
	path('acountants/users/wallet-addresses/', supp_acco_views.AccountantUserWalletAddress.as_view(), name="ac_walletaddress"),
	path('acountants/token/prices/', supp_acco_views.AccountantTokenPrice.as_view(), name="ac_token_chartprice"),
	path('acountants/token/prices/<int:pk>', supp_acco_views.AccountantTokenPrice_Edit.as_view(), name="ac_token_chartprice_Edit"),
	path('acountants/users/wallet-orders/', supp_acco_views.accountant_walletuser_page, name="ac_walletorders"),
	path('acountants/users/wallet-orders/<int:pk>', supp_acco_views.AccountantWalletuser_Edit.as_view(), name="ac_walletorders_edit"),
	path('acountants/bots', supp_acco_views.accountant_bots_page, name="ac_bots"),
	path('acountants/bots/<int:pk>', supp_acco_views.AccountantBots_Edit.as_view(), name="ac_bots_id"),
	path('acountants/buy-sells', supp_acco_views.accountant_buy_sells_page, name="ac_buysells"),
	path('acountants/buy-sells/<int:pk>', supp_acco_views.AccountantBuySells_Edit.as_view(), name="ac_buysells_id"),
	path('acountants/user-stokes', supp_acco_views.accountant_userStokes_page, name="ac_userStoke"),
	path('acountants/user-stokes/<int:pk>', supp_acco_views.AccountantUserStokes_Edit.as_view(), name="ac_userStoke_edit"),

	# is_supporter pages
	path('support/', supp_acco_views.suppurt_home_page, name="su_home"),
	path('support/user/all-tickets/', supp_acco_views.tickets_all_user_page, name="su_all_tickets"),
	path('support/user/response/user/', supp_acco_views.send_ticket_one_user_page, name="su_sendticket_auser"),
	path('support/user/accounts/', supp_acco_views.suppurt_set_useraccount_page, name="su_useraccount"),
	path('support/user/response/<int:ticketID>', supp_acco_views.ticket_of_user_page, name="su_sendticket"),

	# csv file Download
	path('admin/downloads/', csv_views.admin_page_download_page, name='homw_csv'),
	path('admin/downloads/csv/users', csv_views.user_csv, name='user_csv'),
	path('admin/downloads/csv/bots', csv_views.bot_csv, name='bot_csv'),
	path('admin/downloads/csv/tokens', csv_views.token_csv, name='token_csv'),
	path('admin/downloads/csv/tickets', csv_views.ticket_csv, name='ticket_csv'),
	path('admin/downloads/csv/buy-sells', csv_views.buy_sell_csv, name='buy_sell_csv'),
	path('admin/downloads/csv/user-stokes', csv_views.user_stokes_csv, name='user_stokes_csv'),
	path('admin/downloads/csv/chart-token-price', csv_views.chart_token_price_csv, name='chart_token_price_csv'),
]
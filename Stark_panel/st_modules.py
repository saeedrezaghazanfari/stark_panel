from Stark_account.models import User
from Extentions.utils import jalali_convertor_tokens, jalali_convertor
from .models import (
    ChartTokenPrice, Token, UserStoke, Ticket, UserWallet, RobotSubscription, WalletOrder, BuyAndSell
)

# get total
# this function used from account.models.py
def get_userStoke_func(thisUser, tokenTitle):
	user_stw_stoke = UserStoke.objects.filter(user=thisUser, token__title__iexact=tokenTitle).first()
	if user_stw_stoke:
		user_stw_stoke = user_stw_stoke.count
	if user_stw_stoke is None:
		user_stw_stoke = 0
	
	pr_dollar_st = ChartTokenPrice.objects.filter(token__title=tokenTitle).last()
	if pr_dollar_st:
		pr_dollar_st = pr_dollar_st.price_dollar
	if pr_dollar_st is None:
		pr_dollar_st = 0

	return (user_stw_stoke * pr_dollar_st)


# this func for get user final total
def get_final_total(thisUser):
	# DOC::: A = User count of Token * price of a Token (USDT) ===> final Total (USDT) = A + user Stoke (USDT)
	st1_out = get_userStoke_func(thisUser=thisUser, tokenTitle='ST1')
	st2_out = get_userStoke_func(thisUser=thisUser, tokenTitle='ST2')
	st3_out = get_userStoke_func(thisUser=thisUser, tokenTitle='ST3')
	st4_out = get_userStoke_func(thisUser=thisUser, tokenTitle='ST4')

	# return thisUser.stoke + ( user_st1w_stoke * pr_dollar )
	return (thisUser.stoke + st1_out + st2_out + st3_out + st4_out)


# todo: get sood
def get_profit(thisUser, typeOut):
	user = User.objects.get(username=thisUser.username)
	final_total = get_final_total(thisUser)
	
	if typeOut == 'profit':
		return format( ((final_total + user.impression_total + user.robot_sub_total) - user.payment_total), '.2f')

	elif typeOut == 'percent':
		if (user.payment_total - user.robot_sub_total) == 0:
			return format( (final_total + user.impression_total) * 100, '.2f')
			# format(, '.6f')
		return format( (((final_total + user.impression_total) / (user.payment_total - user.robot_sub_total)) - 1) * 100, '.2f')


# get chart: price-date
def get_chart(tokenName, typeOut, fa_lang_code, num_last=15):
	if typeOut == 'date':
		if fa_lang_code:
			dates_get = ChartTokenPrice.objects.filter(token__title=tokenName).values_list('date', flat=True).order_by('id')
			dates = list(dates_get)[-num_last:]
			j_dates = []
			for date in dates:
				j_dates.append(jalali_convertor_tokens(date))
			return j_dates

		else:
			dates_get = ChartTokenPrice.objects.filter(token__title=tokenName).values_list('date', flat=True).order_by('id')
			dates = list(dates_get)[-num_last:]
			n_j_dates = []
			for date in dates:
				n_j_dates.append(date)
			return n_j_dates

	elif typeOut == 'price':
		token = Token.objects.filter(title__icontains=tokenName).first()
		if token:
			prices_get = ChartTokenPrice.objects.filter(token__title=tokenName).values_list('price_dollar', flat=True).order_by('id')
			prices_dollar = list(prices_get)[-num_last:]
			if prices_dollar is None:
				prices_dollar = None
			
			else:
				prices_get = ChartTokenPrice.objects.filter(token__title=tokenName).values_list('price_dollar', flat=True).order_by('id')
				prices_dollar = list(prices_get)[-num_last:]
				return prices_dollar


# add a data with id + 1   """ i'm not like this way """
def get_new_data_id(modelname):
	if modelname == 'User':
		max_id = User.objects.values('id').order_by('-id').first()

	if modelname == 'UserStoke':
		max_id = UserStoke.objects.values('id').order_by('-id').first()

	if modelname == 'Ticket':
		max_id = Ticket.objects.values('id').order_by('-id').first()

	if modelname == 'UserWallet':
		max_id = UserWallet.objects.values('id').order_by('-id').first()

	if modelname == 'RobotSubscription':
		max_id = RobotSubscription.objects.values('id').order_by('-id').first()

	if modelname == 'WalletOrder':
		max_id = WalletOrder.objects.values('id').order_by('-id').first()

	if modelname == 'ChartTokenPrice':
		max_id = ChartTokenPrice.objects.values('id').order_by('-id').first()
		
	if modelname == 'BuyAndSell':
		max_id = BuyAndSell.objects.values('id').order_by('-id').first()

	if not max_id:
		max_id = {'id': 0}
	get_max_id = dict(max_id)['id']
	return int(get_max_id) + 1

# get last price token
def get_last_price_token(tokenName):
	if ChartTokenPrice.objects.filter(token__title=tokenName).last():
		return ChartTokenPrice.objects.filter(token__title=tokenName).last().price_dollar
	return 0


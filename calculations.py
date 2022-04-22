from database import db
import math

# getting price and volume data
time_series_data = db.select_to_df('''
select symbol, trade_date, open_price, high_price, low_price, close_price, volume
from public.all_stock_data where symbol = 'INTC' 
''')

# getting other data (ex. P/E Ratio, 52 Week High, etc.)
overview_data = db.select_to_df('''
select symbol, marketcapitalization, ebitda, peratio, pegratio, bookvalue, dividendpershare, dividendyield, eps, revenuepersharettm, profitmargin, operatingmarginttm, returnonassetsttm, returnonequityttm, revenuettm, grossprofitttm, dilutedepsttm, quarterlyearningsgrowthyoy, quarterlyrevenuegrowthyoy, analysttargetprice, trailingpe, forwardpe, pricetosalesratiottm, pricetobookratio, evtorevenue, evtoebitda, beta, 52weekhigh, 52weeklow, yearly_weekhigh, yearly_weeklow 
from public.overview_data where symbol = 'INTC'
''')

# Retrieving Beta from dataframe
beta = overview_data['beta'][0]

# Calculating if Beta suggests high, low, same volatility or no corrolation
def beta_Volatility(beta):
	if 0 <= beta < 1:
		return 'Low Volatility'
	elif beta > 1:
		return 'High Volatility'
	elif beta == 1:
		return 'Same Volatility'
	elif beta < 0:
		return 'No Correlation'

print(beta_Volatility(beta))
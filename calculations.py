from database import db
import math

# User inputs stock symbol
symbol = input(str('Enter Stock: ')).upper()

# getting price and volume data
time_series_data = db.select_to_df(f'''
select symbol, trade_date, open_price, high_price, low_price, close_price, volume
from public.all_stock_data where symbol = '{symbol}' 
''')

# getting other data (ex. P/E Ratio, 52 Week High, etc.)
overview_data = db.select_to_df(f'''
select symbol, marketcapitalization, ebitda, peratio, pegratio, bookvalue, dividendpershare, dividendyield, eps, revenuepersharettm, profitmargin, operatingmarginttm, returnonassetsttm, returnonequityttm, revenuettm, grossprofitttm, dilutedepsttm, quarterlyearningsgrowthyoy, quarterlyrevenuegrowthyoy, analysttargetprice, trailingpe, forwardpe, pricetosalesratiottm, pricetobookratio, evtorevenue, evtoebitda, beta, 52weekhigh, 52weeklow, yearly_weekhigh, yearly_weeklow 
from public.overview_data where symbol = '{symbol}'
''')

# Retrieving variables from dataframe
beta = overview_data['beta'][0]
yearly_weekhigh = overview_data['yearly_weekhigh'][0]
yearly_weeklow = overview_data['yearly_weeklow'][0]
current_price = time_series_data['close_price'][0]
peg_ratio = overview_data['pegratio'][0]
dividend_yield = overview_data['dividendyield'][0]

def beta_Volatility(beta):
	if 0 <= beta < 1:
		return 'Low Volatility'
	elif beta > 1:
		return 'High Volatility'
	elif beta == 1:
		return 'Same Volatility'
	elif beta < 0:
		return 'No Correlation'

def yearly_high_low_BullBear(high, low, current):
	current_to_high = (current / high)*100
	current_to_low = (current / low)*100
	if current_to_high >= 95:
		return 'Bearish'
	if current_to_low <= 1.05:
		return 'Bullish'
	else:
		return 'In between'

def peg_ratio_BullBear(ratio):
	if ratio <= 1:
		return 'Bullish/Undervalued'
	elif ratio > 1:
		return 'Bearish/Overvalued'

def dividend_yield_Volatility(dividend):
	if dividend == 0:
		return 'High Volatility'
	elif dividend > 0:
		return 'Low volatility'

print(beta_Volatility(beta))
print(yearly_high_low_BullBear(yearly_weekhigh, yearly_weeklow, current_price))
print(peg_ratio_BullBear(peg_ratio))
print(dividend_yield_Volatility(dividend_yield))

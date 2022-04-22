from database import db
import math

# db = database('ec2-23-20-224-166.compute-1.amazonaws.com', 'zsuqqgfjipwpwu', '98b25a8a11bf2eb034266f33871bcc966d3a4217d37ed4e3f542bdccf1717c79', 'db1apeq0n8lsoa', '5432')
time_series_data = db.select_to_df('''
select symbol, trade_date, open_price, high_price, low_price, close_price, volume
from public.all_stock_data where symbol = 'NVDA' 
''')

overview_data = db.select_to_df('''
select symbol, marketcapitalization, ebitda, peratio, pegratio, bookvalue, dividendpershare, dividendyield, eps, revenuepersharettm, profitmargin, operatingmarginttm, returnonassetsttm, returnonequityttm, revenuettm, grossprofitttm, dilutedepsttm, quarterlyearningsgrowthyoy, quarterlyrevenuegrowthyoy, analysttargetprice, trailingpe, forwardpe, pricetosalesratiottm, pricetobookratio, evtorevenue, evtoebitda, beta, 52weekhigh, 52weeklow, yearly_weekhigh, yearly_weeklow 
from public.overview_data where symbol = 'INTC'
''')

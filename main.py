import psycopg2 as ps
import requests
import json

symbol = input(str('Ticker: ')).upper()
data_open_high_low_close_volume = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey=YW9W7ZBX5RBNC6V7'
r = requests.get(data_open_high_low_close_volume)
data = r.json()

trade_dates = list(data['Time Series (Daily)'].keys())
trade_dates_30_days = []
i = 0
while i < 30:
    trade_dates_30_days.append(trade_dates[i])
    i += 1

connection = ps.connect(
    host='ec2-23-20-224-166.compute-1.amazonaws.com', 
    user='zsuqqgfjipwpwu', 
    password='98b25a8a11bf2eb034266f33871bcc966d3a4217d37ed4e3f542bdccf1717c79', 
    database='db1apeq0n8lsoa', 
    port='5432')

def execute(command):
    cursor = connection.cursor()
    try:
        cursor.execute(command)
        connection.commit()
        print('Executed Successfully')
    except Exception as error:
        print(error)
    finally:
        connection.close

for dates in trade_dates_30_days:
    open = data['Time Series (Daily)'][dates]['1. open']
    high = data['Time Series (Daily)'][dates]['2. high']
    low = data['Time Series (Daily)'][dates]['3. low']
    close = data['Time Series (Daily)'][dates]['4. close']
    volume = data['Time Series (Daily)'][dates]['5. volume']
    create_table = f'''
    create table public.{symbol}_stock_data (
        id serial,
        trade_date varchar,
        open_price float,
        high_price float,
        low_price float,
        close_price float,
        volume float
    );
    '''
    # print(execute(create_table))
    insert_into = f"""
    insert into public.{symbol}_stock_data (
        trade_date,
        open_price,
        high_price,
        low_price,
        close_price,
        volume
    )
    values (
        '{dates}',
        {open},
        {high},
        {low},
        {close},
        {volume}
    )
    """
    # create table first, comment out, then insert data
    print(execute(insert_into))
# print(execute(create_table))


import psycopg2 as ps
import pandas as pd
import requests

class database:
  # When calling the class, the variables in the __init__ function are also inputted by the user
  def __init__(self, host, user, password, database, port):
    self.host = host
    self.user = user
    self.password = password
    self.database = database
    self.port = port
  
  def connect(self):
    connection = ps.connect(host=self.host,user=self.user,password=self.password,database=self.database,port=self.port)
    return connection

  def stock_data(self, symbol):
    # retriving json file with price and volume data
    time_series_daily = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey=YW9W7ZBX5RBNC6V7'
    overview = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey=YW9W7ZBX5RBNC6V7'
    r_tsd = requests.get(time_series_daily)
    r_o = requests.get(overview)
    time_series_data = r_tsd.json()
    overview_data = r_o.json()

    keys = list(overview_data.keys())
    del keys[1:13]
    del keys[27:-1]
    del keys[-1]
    new_keys = []

    for key in keys:
        new_keys.append(key.lower())

    new_keys.append('yearly_weekhigh')
    new_keys.append('yearly_weeklow')

    sql_columns = ','.join(new_keys)
    for key in keys:
        command = f'''
        insert into public.overview_data (
            {sql_columns}
        )  
        values (
            {overview_data{key}}
        );    
        '''
        self.insert(command)

    # returns last 30 trading days
    trade_dates = list(time_series_data['Time Series (Daily)'].keys())[0:30]
    
    # iterating through the last 30 trading dates to put price and volume data into database
    for dates in trade_dates:
        open = time_series_data['Time Series (Daily)'][dates]['1. open']
        high = time_series_data['Time Series (Daily)'][dates]['2. high']
        low = time_series_data['Time Series (Daily)'][dates]['3. low']
        close = time_series_data['Time Series (Daily)'][dates]['4. close']
        volume = time_series_data['Time Series (Daily)'][dates]['5. volume']
        
        command = f'''
            insert into public.all_stock_data (
            symbol,    
            trade_date,
            open_price,
            high_price,
            low_price,
            close_price,
            volume
            )
            values (
            '{symbol}',
            '{dates}',
            {open},
            {high},
            {low},
            {close},
            {volume}
            );
        '''
        self.insert(command)
    
  def select_to_df(self, command):
    connection = self.connect()
    try:
        cursor = connection.cursor()
        cursor.execute(command)
        print('Executed Successfully')
        # creating columns and rows for pandas dataframe
        all_data = []
        columns = []
        for column in cursor.description:
          columns.append(column[0])
        for rows in cursor.fetchall():
          all_data.append(dict(zip(columns, rows)))
        
        # creating pandas dataframe
        connection.commit()
        return pd.DataFrame(all_data)
        
    except Exception as error:
      print('Execution Failed: ', error)
    finally:
      connection.close()

  def insert(self, command):
    connection = self.connect()
    try:
        cursor = connection.cursor()
        cursor.execute(command)
        print('Inserted Successfully')
        connection.commit()
    except Exception as error:
        print('Insert Failed: ', error)
    finally:
        connection.close()

# Variables are empty so other people cannot see private database information
db = database('', '', '', '', '')
print(db.select_to_df('''
select symbol, trade_date, open_price, high_price, low_price, close_price, volume
from public.all_stock_data
'''))
print(db.stock_data('AAPL'))


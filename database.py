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
    r = requests.get(time_series_daily)
    data = r.json()
    
    # returns last 30 trading days
    trade_dates = list(data['Time Series (Daily)'].keys())[0:30]
    
    # iterating through the last 30 trading dates to put price and volume data into database
    for dates in trade_dates:
        open = data['Time Series (Daily)'][dates]['1. open']
        high = data['Time Series (Daily)'][dates]['2. high']
        low = data['Time Series (Daily)'][dates]['3. low']
        close = data['Time Series (Daily)'][dates]['4. close']
        volume = data['Time Series (Daily)'][dates]['5. volume']
        
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
    
  def execute(self, command):
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
        pd.DataFrame(all_data)
        
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
# print(db.connect())
print(db.stock_data('f'))


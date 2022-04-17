import psycopg2 as ps
import requests

time_series_daily = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&outputsize=compact&apikey=YW9W7ZBX5RBNC6V7'
r = requests.get(time_series_daily)
print(r)

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

  def execute(self, command):
    cursor = self.connect().cursor()
  try:
    cursor.execute(command)
    print('Executed Successfully')
    self.connect().commit()
  except Exception as error:
    print('Execution Failed: ', error)

    
command = '''
create table public.all_stock_data (
    id serial, 
    symbol varchar,
    trade_date varchar,
    open_price float,
    high_price float,
    low_price float,
    close_price float,
    volume float
);
'''

# Variables are empty so other people cannot see private database information
db = database('', '', '', '', '')
print(db.connect())

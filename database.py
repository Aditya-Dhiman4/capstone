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
    return connection
  
db = database('ec2-23-20-224-166.compute-1.amazonaws.com', 'zsuqqgfjipwpwu', '98b25a8a11bf2eb034266f33871bcc966d3a4217d37ed4e3f542bdccf1717c79', 'db1apeq0n8lsoa', '5432')
print(db.connect())

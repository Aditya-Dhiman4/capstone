import psycopg as ps
import requests

class database:
  # When calling the class, the variables in the __init__ function are also inputted by the user
  def __init__(self, host, user, password, database, port):
    self.host = host
    self.user = user
    self.password = password
    self.database = database
    self.port = port

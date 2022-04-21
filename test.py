import requests

overview = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=YW9W7ZBX5RBNC6V7'
r2 = requests.get(overview)
overview_data = r2.json()

keys = list(overview_data.keys())
print(keys)

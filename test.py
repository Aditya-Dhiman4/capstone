import requests

overview = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=YW9W7ZBX5RBNC6V7'
r2 = requests.get(overview)
overview_data = r2.json()

keys = list(overview_data.keys())
del keys[1:13]
del keys[27:-1]
del keys[-1]
new_keys = []

for key in keys:
    new_keys.append(key.lower())

new_keys.append('yearly_weekhigh')
new_keys.append('yearly_weeklow')

print(new_keys)

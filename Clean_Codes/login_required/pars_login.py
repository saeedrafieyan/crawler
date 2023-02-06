import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import time
import os


URL = 'https://onebill.parsonline.com/'
LOGIN_ROUTE = 'login/'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 'origin': URL, 'referer': URL + LOGIN_ROUTE}

s = requests.session()
login_payload = {
    'Username': 2256947,
    'Password': 759506,
    'Captcha': 0000
}

login_req = s.post(URL + LOGIN_ROUTE, headers=HEADERS, data=login_payload)
print(login_req.status_code)

cookies = login_req.cookies
soup = BeautifulSoup(s.get(URL + 'order?csid=fc8d44f8-ac95-4b0a-9354-bc6f4ee95ef2').text, 'html.parser')
services = soup.find('div', id='page-content-area')

headers = ['service name', 'traffic', 'price']
service_name, traffic, price = [], [], []

pars_services = pd.DataFrame(columns=headers)

for item in services.find_all('div','package type2'):
    title = (item.find_all('div', 'package-title'))
    traffic_temp = (item.find_all('div', 'package-body-title'))
    price_temp = (item.find_all('div', 'package-body-price fanum'))
    service_name.append(title)
    traffic.append(traffic_temp)
    price.append((price_temp))



dataframe = pd.DataFrame({
    'service name' : service_name,
    'traffic' : traffic,
    'price' : price
 })

dataframe.to_csv('temp_csv/0000.csv', encoding='utf-8-sig', index=False)

data = pd.read_csv('temp_csv/0000.csv')
price = list(data['price'])
service_name = list(data['service name'])
traffic = list(data['traffic'])

price = [x[39:] for x in price]
price = [x[:-7] for x in price]
service_name = [x[28:] for x in service_name]
service_name = [x[:-7] for x in service_name]
# print(service_name)
# traffic = [(x.replace('\n','')) for x in traffic]

traffic = [x[47:] for x in traffic]
traffic = [x[:-73] for x in traffic]
traffic = [list((re.sub('^\s+|\s+$','',str(x)) for x in traffic))]
# print((traffic))
cleaned = pd.DataFrame({
    'service name' : service_name,
    'traffic' : traffic[0],
    'price': price
})
cleaned.to_csv('temp_csv/0001.csv', encoding='utf-8-sig', index=False)

columns = ['FCP', 'product type', 'traffic', 'bandwidth', 'duration', 'price', 'description', 'night_traffic', 'infra']
product_type, traffic, bandwidth, duration, FCP, price, description, night_traffic, infra = [], [], [], [], [], [], [], [], []

# dataset = pd.read_csv('0001.csv')
dataset = cleaned
ds_s_name = list(dataset['service name'])
ds_price = list(dataset['price'])
ds_traffic = list(dataset['traffic'])

for item in ds_s_name:
    separated = item.split(' ')
    if separated[0] != 'بسته':
        product_type.append(separated[0])
    else:
        product_type.append('ترافیک')

    try:
        index_band = separated.index('مگابیت')
        bandwidth.append(separated[index_band - 1])
    except:
        bandwidth.append('None')

    try:
        index_dur = separated.index('ماهه')
        duration.append(index_dur-1)
    except:
        duration.append('None')


for item in ds_traffic:
    try:
        separated = item.split(' ')
        traffic.append(separated[0])
    except:
        traffic.append('None')

for item in ds_price:
    try:
        separated = item.split(' ')
        price.append(separated[0])
    except:
        price.append('None')

for item in service_name:
    description.append(item)
    night_traffic.append(0)
    infra.append('ADSL')

fcp = ['Pars'] * len(product_type)
# [f(x) if condition else g(x) for x in sequence]
bandwidth = [int(x)*1024 if x != 'None' else x  for x in bandwidth]
duration = [int(x) if x!='None' else 0 for x in duration]


# print(len(product_type))
# print(len(traffic))
# print(len(bandwidth))
# print(len(duration))
# print(len(night_traffic))
# print(len(infra))
# print(len(price))
# print(len(description))


bandwidth = [int(x) if x!='None' else 0 for x in bandwidth]
traffic = [x.replace(',','') if x!='' else 0 for x in traffic]
traffic = [int(x) if x!='' else 0 for x in traffic]
price = [x.replace(',','') if x!='' else 0 for x in price]
price = [int(x) for x in price]
# print(price)

new_dataset = pd.DataFrame({'FCP':fcp,'product type':product_type, 'traffic':traffic,'bandwidth':bandwidth, \
                                                 'duration':duration, 'night traffic': night_traffic, 'infra': infra, \
                                                 'price':price, 'description': description})



date = datetime.today().strftime('%Y-%m-%d')
time = int(time.time())


the_latest_pars_addresss = os.listdir('D:\hiweb\exports\Clean_Codes\login_required\exported_data\pars')[-1]
the_latest_pars = pd.read_csv(f'D:\hiweb\exports\Clean_Codes\login_required\exported_data\pars\{the_latest_pars_addresss}')



if ((list(new_dataset['price']) != list(the_latest_pars['price'])) or \
        (list(new_dataset['bandwidth']) != list(the_latest_pars['bandwidth'])) or \
    (list(new_dataset['duration']) != list(the_latest_pars['duration'])) or \
    (list(new_dataset['description']) != list(the_latest_pars['description'])) or \
        (list(new_dataset['traffic']) != list(the_latest_pars['traffic']))):
    new_dataset.to_csv(f'exported_data/pars/Pars_{date}_{time}.csv', encoding='utf-8-sig', index=False)
    print('the newest version of Pars is saved')
else:
    print('everything is same for Pars')







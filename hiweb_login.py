import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unidecode import unidecode


URL = 'https://p.hiweb.ir/'
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
soup = BeautifulSoup(s.get(URL + 'order').text, 'html.parser')
services = soup.find('div', id='packages-view')

headers = ['service name', 'traffic', 'price']
service_name, traffic, price = [], [], []

hiweb_services = pd.DataFrame(columns=headers)

for item in services.find_all('div','package type2'):
    title = (item.find_all('div', 'package-title'))
    # title = [re.sub('<div class="package-title">', '', x) for x in title]
    # title = [re.sub('< / div >', '', x) for x in title]
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

dataframe.to_csv('DataFrame.csv', encoding='utf-8-sig')
# print(services.find_all('div','package type2')[0])
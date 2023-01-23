import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unidecode import unidecode


url_hiweb = 'https://www.hiweb.ir/home-services/adsl-pricelist'
url_pars = 'https://www.parsonline.com/adsl/sale/compare-services'

page_hiweb = requests.get(url_hiweb)
soup_hiweb = BeautifulSoup(page_hiweb.text, 'lxml')

# table_hiweb = soup_hiweb.find('table', "table-striped text-center")#, '//*[@id="nonVolumetric"]/div/div[3]/table')
table_hiweb1 = soup_hiweb.select('#nonVolumetric > div > div:nth-child(14) > table')

headers = []
for item in table_hiweb1:
    for i in item.find_all('th'):
        title = i.text
        title = re.sub(r"\s+$", "", title)
        title = re.sub(r"^\s+", "", title)
        headers.append(title)

hiweb_table_1 = pd.DataFrame(columns=headers)

for item in table_hiweb1:
    for j in item.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        row = [(re.sub('\.', ',', x)) for x in row]
        row = [unidecode(x) for x in row]
        length = len(hiweb_table_1)
        hiweb_table_1.loc[length] = row
hiweb_table_1.to_csv('hiweb_table_1.csv', encoding='utf-8-sig')


table_hiweb2 = soup_hiweb.select('#nonVolumetric > div > div:nth-child(21) > table')

headers = []
for item in table_hiweb2:
    for i in item.find_all('th'):
        title = i.text
        title = re.sub(r"\s+$", "", title)
        title = re.sub(r"^\s+", "", title)
        headers.append(title)

hiweb_table_2 = pd.DataFrame(columns=headers)

for item in table_hiweb2:
    for j in item.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        row = [(re.sub('\.',',',x)) for x in row]
        row = [unidecode(x) for x in row]
        length = len(hiweb_table_2)
        hiweb_table_2.loc[length] = row
hiweb_table_2.to_csv('hiweb_table_2.csv', encoding='utf-8-sig')


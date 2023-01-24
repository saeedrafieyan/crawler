import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unidecode import unidecode


url_saba = 'http://www.sabanet.ir/adsl'

page_saba = requests.get(url_saba)
soup_saba = BeautifulSoup(page_saba.text, 'lxml')

# table_saba = soup_saba.find('table', "table-striped text-center")#, '//*[@id="nonVolumetric"]/div/div[3]/table')
table_saba1 = soup_saba.select('#ADSLPriceList > div > div > div > div:nth-child(2) > table')

headers = []
for item in table_saba1:
    for i in item.find_all('th'):
        title = i.text
        title = re.sub(r"\s+$", "", title)
        title = re.sub(r"^\s+", "", title)
        headers.append(title)

saba_table_1 = pd.DataFrame(columns=headers)

for item in table_saba1:
    for j in item.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        row = [(re.sub('\.', ',', x)) for x in row]
        row = [unidecode(x) for x in row]
        length = len(saba_table_1)
        saba_table_1.loc[length] = row
saba_table_1.to_csv('saba_table_1.csv', encoding='utf-8-sig')

#
# table_saba2 = soup_saba.select('#nonVolumetric > div > div:nth-child(21) > table')
#
# headers = []
# for item in table_saba2:
#     for i in item.find_all('th'):
#         title = i.text
#         title = re.sub(r"\s+$", "", title)
#         title = re.sub(r"^\s+", "", title)
#         headers.append(title)
#
# saba_table_2 = pd.DataFrame(columns=headers)
#
# for item in table_saba2:
#     for j in item.find_all('tr')[1:]:
#         row_data = j.find_all('td')
#         row = [i.text for i in row_data]
#         row = [(re.sub('\.',',',x)) for x in row]
#         row = [unidecode(x) for x in row]
#         length = len(saba_table_2)
#         saba_table_2.loc[length] = row
# saba_table_2.to_csv('saba_table_2.csv', encoding='utf-8-sig')


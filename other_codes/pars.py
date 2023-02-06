import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


url_pars = 'https://www.parsonline.com/adsl/sale/compare-services'

page_pars = requests.get(url_pars)
soup_pars = BeautifulSoup(page_pars.text, 'lxml')

# table_pars = soup_pars.find('table', "table-striped text-center")#, '//*[@id="nonVolumetric"]/div/div[3]/table')
table_pars1 = soup_pars.select('body > div.wrap > div.core > section > div > div.table-responsive.packages_container > table:nth-child(3)')


for item in table_pars1:
    i = item.find_all('tr')[0]
    title = i.text
    title = re.sub(r"\s+$", "", title)
    title = re.sub(r"^\s+", "", title)
    headers = title.split('\n')

pars_table_1 = pd.DataFrame(columns=headers)

for item in table_pars1:
    for j in item.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(pars_table_1)
        pars_table_1.loc[length] = row
pars_table_1.to_csv('pars_table_1.csv', encoding='utf-8-sig')


table_pars2 = soup_pars.select('body > div.wrap > div.core > section > div > div.table-responsive.packages_container > table:nth-child(7)')

for item in table_pars2:
    i = item.find_all('tr')[0]
    title = i.text
    title = re.sub(r"\s+$", "", title)
    title = re.sub(r"^\s+", "", title)
    headers = title.split('\n')

pars_table_2 = pd.DataFrame(columns=headers)

for item in table_pars2:
    for j in item.find_all('tr')[1:]:
        row_data = j.find_all('td')
        row = [i.text for i in row_data]
        length = len(pars_table_2)
        pars_table_2.loc[length] = row
pars_table_2.to_csv('pars_table_2.csv', encoding='utf-8-sig')




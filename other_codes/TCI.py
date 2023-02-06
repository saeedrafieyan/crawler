import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unidecode import unidecode


url_tci = 'https://www.tci.ir/page-adsl/fa/0'

page_tci = requests.get(url_tci)
soup_tci = BeautifulSoup(page_tci.text, 'lxml')

table_tci1 = soup_tci.select('#mainbody > div > div > div.phonedetail > div:nth-child(5) > div:nth-child(1) > table > tbody')

headers = []
for item in table_tci1:
    for i in item.find_next_sibling('td'):
        title = i.text
        title = re.sub(r"\s+$", "", title)
        title = re.sub(r"^\s+", "", title)
        headers.append(title)
print(headers)
tci_table_1 = pd.DataFrame(columns=headers)

for item in table_tci1:
    for j in item.find_all('td')[1:]:
        row_data = j.find_all('span')
        row = [i.text for i in row_data]
        row = [(re.sub('\.', ',', x)) for x in row]
        row = [unidecode(x) for x in row]
        length = len(tci_table_1)
        tci_table_1.loc[length] = row
tci_table_1.to_csv('00tci_table_1.csv', encoding='utf-8-sig')


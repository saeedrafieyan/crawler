import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unidecode import unidecode


def table_crawler(website, table_tag, header_tag, row_tag, values_tag, dataset_name):
    url = website

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    table = soup.select(table_tag)

    headers = []
    for item in table:
        for i in item.find_all(header_tag):
            title = i.text
            title = re.sub(r"\s+$", "", title)
            title = re.sub(r"^\s+", "", title)
            headers.append(title)

    dataset = pd.DataFrame(columns=headers)

    for item in table:
        for j in item.find_all(row_tag)[1:]:
            row_data = j.find_all(values_tag)
            row = [i.text for i in row_data]
            row = [(re.sub('\.', ',', x)) for x in row]
            row = [unidecode(x) for x in row]
            length = len(dataset)
            dataset.loc[length] = row
    dataset.to_csv(f'{dataset_name}.csv', encoding='utf-8-sig')

    return print("done")


table_crawler('https://www.tci.ir/page-adsl/fa/0', '#mainbody > div > div > div.phonedetail > div:nth-child(5) > div:nth-child(1) > table > tbody','td','tr','span','TCI_public_services_tabel_1')

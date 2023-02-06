import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from unidecode import unidecode
from datetime import datetime
import time
import os


def hiweb_public_services(url, table_tag):
    url = url
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    # descrip = soup.select('//*[@id="nonVolumetric"]/div/h3[2]')
    table = soup.select(table_tag)
    headers = []

    for item in table:
        for i in item.find_all('th'):
            title = i.text
            title = re.sub(r"\s+$", "", title)
            title = re.sub(r"^\s+", "", title)
            headers.append(title)

    dataset = pd.DataFrame(columns=headers)

    for item in table:
        for j in item.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            row = [(re.sub('\.', ',', x)) for x in row]
            row = [unidecode(x) for x in row]
            length = len(dataset)
            dataset.loc[length] = row
    return dataset


def pars_public_services(url, table_tag):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.select(table_tag)

    for item in table:
        i = item.find_all('tr')[0]
        title = i.text
        title = re.sub(r"\s+$", "", title)
        title = re.sub(r"^\s+", "", title)
        headers = title.split('\n')

    dataset = pd.DataFrame(columns=headers)

    for item in table:
        for j in item.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            length = len(dataset)
            dataset.loc[length] = row

    return dataset


def unifier_pars(dataset):
    product_type, traffic, bandwidth, duration, FCP, price, description, night_traffic, infra = [], [], [], [], [], [], [], [], []
    fcp = 'pars'
    pt = 'سرویس'
    dr = 1
    tr = list(dataset['ترافیک معادل بین الملل (GB)'])
    bw = list(dataset['سرعت سرویس (Kbps)'])
    pr = list(dataset['قیمت سرویس (ریال)'])
    for i in range(len(pr)):
        product_type.append(pt)
        traffic.append(tr[i])
        bandwidth.append(bw[i])
        duration.append(dr)
        FCP.append(fcp)
        price.append(pr[i])
        description.append('Empty')
        night_traffic.append(0)
        infra.append('ADSL')
    bandwidth = [int(x) for x in bandwidth]
    traffic = [int(x) for x in traffic]
    price = [int(x.replace(',','')) for x in price]
    unified_dataset = pd.DataFrame(pd.DataFrame({'FCP':fcp,'product type':product_type, 'traffic':traffic,'bandwidth':bandwidth, \
                                                 'duration':duration, 'night traffic': night_traffic, 'infra': infra, \
                                                 'price':price, 'description': description}))
    return unified_dataset

def unifier_hiweb(dataset):
    product_type, traffic, bandwidth, duration, FCP, price, description, night_traffic, infra = [], [], [], [], [], [], [], [], []
    fcp = 'hiweb'
    pt = 'سرویس'
    dr = 1
    tr = list(dataset['ترافیک بین الملل (GB)'])
    bw = list(dataset['سرعت سرویس (Kbps)'])
    pr = list(dataset['قیمت سرویس (ریال)'])
    for i in range(len(pr)):
        product_type.append(pt)
        traffic.append(tr[i])
        bandwidth.append(bw[i])
        duration.append(dr)
        FCP.append(fcp)
        price.append(pr[i])
        description.append("None")
        night_traffic.append(0)
        infra.append('ADSL')
    bandwidth = [int(x) for x in bandwidth]
    traffic = [int(x) for x in traffic]
    price = [int(x.replace(',', '')) for x in price]
    unified_dataset = pd.DataFrame(pd.DataFrame({'FCP':fcp,'product type':product_type, 'traffic':traffic,'bandwidth':bandwidth, \
                                                 'duration':duration, 'night traffic': night_traffic, 'infra': infra, \
                                                 'price':price, 'description': description}))
    return unified_dataset


date = datetime.today().strftime('%Y-%m-%d')
time = int(time.time())

hiweb_table1 = hiweb_public_services('https://www.hiweb.ir/home-services/adsl-pricelist','#nonVolumetric > div > div:nth-child(14) > table')
hiweb_table2 = hiweb_public_services('https://www.hiweb.ir/home-services/adsl-pricelist', '#nonVolumetric > div > div:nth-child(21) > table')
hiweb = pd.concat([hiweb_table1, hiweb_table2], ignore_index=True)
hiweb_unified = unifier_hiweb(hiweb)
the_latest_hiweb_address = os.listdir('D:\hiweb\exports\Clean_Codes\public_informations\exported_data\hiweb')[-1]
the_latest_hiweb = pd.read_csv(f'D:\hiweb\exports\Clean_Codes\public_informations\exported_data\hiweb\{the_latest_hiweb_address}')




if ((list(hiweb_unified['price']) != list(the_latest_hiweb['price'])) or \
        (list(hiweb_unified['bandwidth']) != list(the_latest_hiweb['bandwidth'])) or \
        (list(hiweb_unified['duration']) != list(the_latest_hiweb['duration'])) or \
        (list(hiweb_unified['description']) != list(the_latest_hiweb['description'])) or \
        (list(hiweb_unified['traffic']) != list(the_latest_hiweb['traffic']))):
    hiweb_unified.to_csv(f'exported_data/hiweb/Hiweb_unified_{date}_{time}.csv', encoding='utf-8-sig', index=False)
    print('the newest version of HiWEB is saved')
else:
    print('everything is same for HiWEB')





pars_table1 = pars_public_services('https://www.parsonline.com/adsl/sale/compare-services','body > div.wrap > div.core > section > div > div.table-responsive.packages_container > table:nth-child(3)')
pars_table2 = pars_public_services('https://www.parsonline.com/adsl/sale/compare-services','body > div.wrap > div.core > section > div > div.table-responsive.packages_container > table:nth-child(7)')
pars = pd.concat([pars_table1, pars_table2], ignore_index=True)
pars_unified = unifier_pars(pars)
the_latest_pars_address = os.listdir('D:\hiweb\exports\Clean_Codes\public_informations\exported_data\pars')[-1]
the_latest_pars = pd.read_csv(f'D:\hiweb\exports\Clean_Codes\public_informations\exported_data\pars\{the_latest_pars_address}')



if ((list(pars_unified['price']) != list(the_latest_pars['price'])) or \
        (list(pars_unified['bandwidth']) != list(the_latest_pars['bandwidth'])) or \
    (list(pars_unified['duration']) != list(the_latest_pars['duration'])) or \
    (list(pars_unified['description']) != list(the_latest_pars['description'])) or \
        (list(pars_unified['traffic']) != list(the_latest_pars['traffic']))):
    pars_unified.to_csv(f'exported_data/pars/Pars_unified_{date}_{time}.csv', encoding='utf-8-sig', index=False)
    print('the newest version of PARS is saved')
else:
    print('everything is same for Pars')




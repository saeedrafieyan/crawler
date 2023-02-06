import re

import pandas as pd

columns = ['product type', 'deal type', 'traffic', 'bandwidth', 'duration', 'FCP', 'price']
product_type, deal_type, traffic, bandwidth, duration, FCP, price = [], [], [], [], [], [], []

dataset = pd.read_csv('0001.csv')

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
        bandwidth.append('NaN')

    try:
        index_dur = separated.index('ماهه')
        duration.append(index_dur-1)
    except:
        duration.append('NaN')


for item in ds_traffic:
    try:
        separated = item.split(' ')
        traffic.append(separated[0])
    except:
        traffic.append('NaN')

for item in ds_price:
    try:
        separated = item.split(' ')
        price.append(separated[0])
    except:
        price.append('NaN')

fcp = ['Hiweb'] * len(product_type)

print(len(traffic) == len(product_type))
new_dataset = pd.DataFrame({'FCP':fcp,'product type':product_type, 'traffic':traffic,'bandwidth':bandwidth, 'duration':duration, 'price':price})

print(len(product_type))
# print(len(deal_type))
print(len(traffic))
print(len(bandwidth))  # 280
print(len(duration))  # 280
print(len(price))
new_dataset.to_csv('0002.csv', encoding='utf-8-sig', index=False)

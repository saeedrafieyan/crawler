import re

import pandas as pd

columns = ['product type', 'deal type', 'traffic', 'bandwidth', 'duration', 'FCP', 'price']
product_type, deal_type, traffic, bandwidth, duration, FCP, price = [],[],[],[],[],[],[]

dataset = pd.read_csv('pars_cleaned_dataset.csv')

ds_s_name = list(dataset['service name'])
ds_price = list(dataset['price'])
ds_traffic = list(dataset['traffic'])


for item in ds_s_name:
    separated = item.split(' ')
    if separated[0] != 'بسته':
        product_type.append(separated[0])
    else:
        product_type.append('ترافیک')

    for i in range(len(separated)):
        if separated[i] == 'مگابیت':
            bandwidth.append(separated[i-1])
        else:
            bandwidth.append('NaN')

    for i in range(len(separated)):
        if separated[i] == 'ماهه':
            duration.append(separated[i-1])
        else:
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

print(len(traffic) == len(product_type))
# new_dataset = pd.DataFrame({'product type':product_type, 'deal type':deal_type, 'traffic':traffic,'bandwidth':bandwidth, 'duration':duration, 'price':price})

print(len(product_type))
print(len(deal_type))
print(len(traffic))
print(len(bandwidth))
print(len(duration))
print(len(price))
new_dataset.to_csv('HiwebReformed.csv', encoding='utf-8-sig', index=False)
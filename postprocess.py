import re

import pandas as pd

data = pd.read_csv('DataFrame.csv')
price = list(data['price'])
service_name = list(data['service name'])
traffic = list(data['traffic'])

price = [x[39:] for x in price]
price = [x[:-7] for x in price]
service_name = [x[28:] for x in service_name]
service_name = [x[:-7] for x in service_name]
# traffic = [(x.replace('\n','')) for x in traffic]

traffic = [x[47:] for x in traffic]
traffic = [x[:-73] for x in traffic]

cleaned = pd.DataFrame({
    'service name' : service_name,
    'traffic' : traffic,
    'price': price
})
cleaned.to_csv('cleaned_dataset.csv', encoding='utf-8-sig', index=False)
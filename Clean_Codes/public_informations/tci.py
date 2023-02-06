import pandas as pd
import re
import time
from datetime import datetime
import os



dfs = pd.read_html('https://www.tci.ir/page-adsl/fa/0')

table1 = dfs[0]
table2 = dfs[1]
table3 = dfs[2]
table4 = dfs[3]

table1.drop([0], axis=0, inplace=True)
table2.drop([0], axis=0, inplace=True)
table3.drop([0], axis=0, inplace=True)

columns = ['FCP', 'product type', 'traffic', 'bandwidth', 'duration', 'price', 'description', 'night_traffic', 'infra']
product_type, traffic, bandwidth, duration, FCP, price, description, night_traffic, infra = [], [], [], [], [], [], [], [], []

dataset_1 = table1
fcp = 'TCI'
pt_t1 = 'سرویس'
tr_t1 = list(dataset_1[2])[1:]
bw_t1 = list(dataset_1[1])[1:]
# [f(x) if condition else g(x) for x in sequence]
bw_t1 = [int(re.split(r'\D+',x)[0])*1024 if x.endswith('Mb') else int(re.split(r'\D+',x)[0]) for x in bw_t1]
p1m_t1 = list(dataset_1[5])[1:]
p1m_t1 = [x+'0' if x.isnumeric() else x for x in p1m_t1]

p3m_t1 = list(dataset_1[6])[1:]
p3m_t1 = [x+'0' if x.isnumeric() else x for x in p3m_t1]

p6m_t1 = list(dataset_1[7])[1:]
p6m_t1 = [x+'0' if x.isnumeric() else x for x in p6m_t1]

p12m_t1 = list(dataset_1[8])[1:]
p12m_t1 = [x+'0' if x.isnumeric() else x for x in p12m_t1]


for i in range(len(p1m_t1)):
    FCP.append(fcp)
    product_type.append(pt_t1)
    traffic.append(tr_t1[i])
    bandwidth.append(bw_t1[i])
    duration.append(1)
    price.append(p1m_t1[i])
    description.append('')
    night_traffic.append(0)
    infra.append('ADSL')

for i in range(len(p3m_t1)):
    FCP.append(fcp)
    product_type.append(pt_t1)
    traffic.append(tr_t1[i])
    bandwidth.append(bw_t1[i])
    duration.append(3)
    price.append(p3m_t1[i])
    description.append('')
    night_traffic.append(0)
    infra.append('ADSL')

for i in range(len(p6m_t1)):
    FCP.append(fcp)
    product_type.append(pt_t1)
    traffic.append(tr_t1[i])
    bandwidth.append(bw_t1[i])
    duration.append(6)
    price.append(p6m_t1[i])
    description.append('')
    night_traffic.append(0)
    infra.append('ADSL')

for i in range(len(p12m_t1)):
    FCP.append(fcp)
    product_type.append(pt_t1)
    traffic.append(tr_t1[i])
    bandwidth.append(bw_t1[i])
    duration.append(12)
    price.append(p12m_t1[i])
    description.append('')
    night_traffic.append(0)
    infra.append('ADSL')

#######################

dataset_2 = table2

pt_t2 = 'گیگ پلاس'
tr_t2 = list(dataset_2[5])[1:]
bw_t2 = list(dataset_2[0])[1:]
# [f(x) if condition else g(x) for x in sequence]
bw_t2 = [int(re.split(r'\D+',x)[0])*1024 if x.endswith('Mb') else int(re.split(r'\D+',x)[0]) for x in bw_t2]
p1m_t2 = list(dataset_2[8])[1:]
p1m_t2 = [x+'0' if x.isnumeric() else x for x in p1m_t2]

p3m_t2 = list(dataset_2[6])[1:]
p3m_t2 = [x+'0' if x.isnumeric() else x for x in p3m_t2]

p6m_t2 = list(dataset_2[7])[1:]
p6m_t2 = [x+'0' if x.isnumeric() else x for x in p6m_t2]

p12m_t2 = list(dataset_2[8])[1:]
p12m_t2 = [x+'0' if x.isnumeric() else x for x in p12m_t2]

for i in range(len(p1m_t2)):
    FCP.append(fcp)
    product_type.append(pt_t2)
    traffic.append(tr_t2[i])
    bandwidth.append(bw_t2[i])
    duration.append(1)
    price.append(p1m_t2[i])
    description.append('')
    night_traffic.append(0)
    infra.append('ADSL')

for i in range(len(p3m_t2)):
    FCP.append(fcp)
    product_type.append(pt_t2)
    traffic.append(tr_t2[i])
    bandwidth.append(bw_t2[i])
    duration.append(3)
    price.append(p3m_t2[i])
    description.append('')
    night_traffic.append(0)
    infra.append('ADSL')

for i in range(len(p6m_t2)):
    FCP.append(fcp)
    product_type.append(pt_t2)
    traffic.append(tr_t2[i])
    bandwidth.append(bw_t2[i])
    duration.append(6)
    price.append(p6m_t2[i])
    description.append('')
    night_traffic.append(0)
    infra.append('ADSL')

for i in range(len(p12m_t2)):
    FCP.append(fcp)
    product_type.append(pt_t2)
    traffic.append(tr_t2[i])
    bandwidth.append(bw_t2[i])
    duration.append(12)
    price.append(p12m_t2[i])
    description.append('')
    night_traffic.append(0)
    infra.append('ADSL')

##########################
dataset_3 = table3
pt_t3 = 'ترافیک'
tr_t3 = list(dataset_3[1])[2:]
tr_t3 = [(x.split(' ')[0]) for x in tr_t3]
bw_t3 = 'NaN'
dr_t3 = 'NaN'
pr = list(dataset_3[2])[2:]
# print(pr)
pr = [(int(float(x)) * 10000 ) for x in pr]

for i in range(len(pr)):
    FCP.append(fcp)
    product_type.append(pt_t3)
    traffic.append(tr_t3[i])
    bandwidth.append(bw_t3)
    duration.append(dr_t3)
    price.append(pr[i])
    description.append('')
    night_traffic.append(0)
    infra.append('ADSL')

####################
dataset_4 = table4
# print(dataset_4)
pt_t4 = 'ترافیک زمان دار'
tr_t4_temp = list(dataset_4[1])
tr_t4 = []
for item in tr_t4_temp:
    token = item.split(' ')
    for i in range(len(token)):
        if token[i] == 'گیگابایت':
            tr_t4.append(int(token[i-1]))
bw_t3 = 'NaN'
dr_t4 = list(dataset_4[2])[1:]
dr_t4 = [int(x[:2]) for x in dr_t4]
pr_t4 = list(dataset_4[3])[1:]
pr_t4 = [(int(float(x)) * 10000 ) for x in pr_t4]
des_t4 = list(dataset_4[1][1:])
print(len(des_t4))

for i in range(len(pr_t4)):
    FCP.append(fcp)
    product_type.append(pt_t3)
    traffic.append(tr_t3[i])
    bandwidth.append(bw_t3)
    duration.append(dr_t3)
    price.append(pr[i])
    description.append(des_t4[i])
    night_traffic.append(0)
    infra.append('ADSL')




date = datetime.today().strftime('%Y-%m-%d')
time = int(time.time())




# print(len(product_type))
# print(len(traffic))
# print(len(bandwidth))
# print(len(duration))
# print(len(night_traffic))
# print(len(infra))
# print(len(price))
# print(len(description))

# [int(x)*1024 if x != 'NaN' else x  for x in bandwidth]


bandwidth = [int(x) if x!='NaN' else 0 for x in bandwidth]
traffic = [int(x) for x in traffic]
price = [int(x) if x!= '-' else 0 for x in price]


tci_dataframe = pd.DataFrame(pd.DataFrame({'FCP':fcp,'product type':product_type, 'traffic':traffic,'bandwidth':bandwidth, \
                                                 'duration':duration, 'night traffic': night_traffic, 'infra': infra, \
                                                 'price':price, 'description': description}))

the_latest_tci_addresss = os.listdir('D:/hiweb/exports/Clean_Codes/public_informations/exported_data/tci')[-1]
the_latest_tci = pd.read_csv(f'D:/hiweb/exports/Clean_Codes/public_informations/exported_data/tci/{the_latest_tci_addresss}')


if ((list(tci_dataframe['price']) != list(the_latest_tci['price'])) or \
        (list(tci_dataframe['bandwidth']) != list(the_latest_tci['bandwidth'])) or \
        (list(tci_dataframe['traffic']) != list(the_latest_tci['traffic']))):
    tci_dataframe.to_csv(f'exported_data/tci/TCI_{date}_{time}.csv.csv',encoding='utf-8-sig', index=False)
    print('the newest version of TCI is saved')
else:
    print('everything is same for TCI')






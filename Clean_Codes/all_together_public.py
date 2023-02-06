import os
import pandas as pd

path = 'D:/hiweb/exports/Clean_Codes/public_informations/exported_data/'

pars_address = os.listdir('D:/hiweb/exports/Clean_Codes/public_informations/exported_data/pars/')[-1]
hiweb_address = os.listdir('D:/hiweb/exports/Clean_Codes/public_informations/exported_data/hiweb/')[-1]
tci_address = os.listdir('D:/hiweb/exports/Clean_Codes/public_informations/exported_data/tci/')[-1]

pars = pd.read_csv(f'{path}/pars/{pars_address}')
hiweb = pd.read_csv(f'{path}/hiweb/{hiweb_address}')
tci = pd.read_csv(f'{path}/tci/{tci_address}')

all_together = pd.concat([pars,hiweb, tci],ignore_index=True)
all_together.to_csv(f'D:/hiweb/exports/Clean_Codes/public_informations/all_together_public.csv', encoding='utf-8-sig', index=False)


import pandas as pd
import os

df1 = pd.read_csv('D:\hiweb\exports\Clean_Codes\public_informations\exported_data\hiweb\Hiweb_unified_2023-02-05_1675576038.csv')
df2 = pd.read_csv('D:\hiweb\exports\Clean_Codes\public_informations\exported_data\hiweb\Hiweb_unified_2023-02-05_1675575340.csv')
# compare = pd.DataFrame.compare(df1,df2)
# df_diff = pd.concat([df1,df2]).drop_duplicates(keep=False)


if list(df1['price']) != list(df2['price']):
    print('i found some changes')
else:
    print('everything is same')
# print(df1 != df2)

path = 'D:\hiweb\exports\Clean_Codes\public_informations\exported_data\hiweb'
print(os.listdir(path))
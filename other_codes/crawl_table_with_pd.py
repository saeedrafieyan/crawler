import pandas as pd

dfs = pd.read_html('https://www.tci.ir/page-adsl/fa/0')

table1 = dfs[0]
table2 = dfs[1]
table3 = dfs[2]

table1.drop([0], axis=0, inplace=True)
table2.drop([0], axis=0, inplace=True)
table3.drop([0], axis=0, inplace=True)

table1.to_csv('100tci.csv', encoding='utf-8-sig', index=False)
table2.to_csv('110tci.csv', encoding='utf-8-sig', index=False)
table3.to_csv('111tci.csv', encoding='utf-8-sig', index=False)


import pandas
import os

filepath = os.getcwd() + '\\data\\sdg_master_unique_cleaned.xlsx'
print(filepath)

df = pandas.read_excel(filepath)
print(df)

for row in df.index:
    code = str(df.at[row, 'sdg_codes'])
    if code == 'DNC':
        df.at[row, 'sdg_codes'] = code
    elif len(code) == 4:
        df.at[row, 'sdg_codes'] = code[:2]
    else:
        df.at[row, 'sdg_codes'] = code[:1]

df.to_csv('truncated_codes.csv')

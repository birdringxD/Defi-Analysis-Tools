import time
import requests
import json
import pandas as pd
import tg

df = pd.DataFrame(columns=[
    'srx',
    'swd', 
])

# transaction api
srx_url = 'https://apilist.tronscan.org/api/account?address=TJYxw5yvLLNzoC9VEogrrehGWsTidRHwcC'
text = requests.get(srx_url).text
data = json.loads(text)
srx_balance = data['balance']

swd_url = 'https://apilist.tronscan.org/api/account?address=TCoCR2oDhL3ghKsRgrKdGWPNt8rVRUwpiW'
text = requests.get(swd_url).text
data = json.loads(text)
swd_balance = data['balance']
 
srx_balance = (round((srx_balance) / 1000000, 2))
swd_balance = (round((swd_balance) / 1000000, 2))
print(srx_balance)
print(swd_balance)

old_df = pd.read_csv('./tmp.csv') 
srx = old_df.iloc[0].at['srx']
swd = old_df.iloc[0].at['swd']
print(srx)
print(swd)

if((srx - srx_balance) / srx >= 0.03) :
    text = "srx合约余额降低：" + str((srx - srx_balance) / srx) + " 从"+ str(srx) + "减少到" + str(srx_balance)
    tg.send_warning(text)
if((swd - swd_balance) / swd >= 0.03) :
    text = "swd合约余额降低：" + str((swd - swd_balance) / swd) + " 从"+ str(swd) + "减少到" + str(swd_balance)
    tg.send_warning(text)

df.loc[0] = [srx_balance, swd_balance]
df.to_csv('./tmp.csv', index = False)

import time
import requests
import json
import pandas as pd

def run():
    t = int(round(time.time() * 1000))
    time_start=time.time()

    # transaction api
    tokens_list = [
        "TSNWgunSeGUQqBKK4bM31iLw3bn9SBWWTG", 
    # "TKkeiboTkxXKJpbmVFbv4a8ov5rAfRDMf9",
    # "TN7zQd2oCCguSQykZ437tZzLEaGJ7EGyha",
    ]

    df = pd.DataFrame(columns=[
    'token_name',
    'rank', 
    'holder_address', 
    #'balance', 
    'holders_count', 
    #'total_supply_with_decimals'
    ])

    cnt = 0

    for tokens_list in tokens_list:
        url = "https://apilist.tronscan.io/api/token_trc20/holders?sort=-balance&start=0&limit=50&contract_address=%s" % (tokens_list)
        h_url = "https://apilist.tronscan.org/api/token_trc20?contract=%s&showAll=1" % (tokens_list)
        #c_url = "https://apilist.tronscan.org/api/contract?contract=%s" % (tokens_list)
        name_url = "https://apilist.tronscan.org/api/token_trc20?contract=%s" % (tokens_list)

        name_text = requests.get(name_url).text
        name_data = json.loads(name_text)
        tokens_name = name_data['trc20_tokens'][0]['name']

        text = requests.get(url).text
        data = json.loads(text)

        h_text = requests.get(h_url).text
        h_data = json.loads(h_text)

        print(tokens_name)

        #holders_count = h_data['trc20_tokens'][0]['holders_count']
        #total_supply_with_decimals = h_data['trc20_tokens'][0]['total_supply_with_decimals']
        total = 0
        for i in range(0, 50):
            holder_address = data["trc20_tokens"][i]["holder_address"]
            balance = data["trc20_tokens"][i]["balance"]
            df.loc[cnt] = [
                tokens_name, 
                i + 1,
                holder_address, 
               # holders_count,
                float(float(balance) / 1000000),
                #float(int(total_supply_with_decimals) / 1000000000000000000),
            ]
            #print(df)
            total = total + float(float(balance) / 1000000)
            cnt = cnt + 1

    old_df = pd.read_csv('./holders.csv') 
    old_total = old_df['holders_count'].sum() 
    #print(old_df.to_string(index = False))
    #print('time cost: ',time_end-time_start,'s')

    print("total tokens: " + str(total))
    print("old_total tokens: " + str(old_total))

    #print(df.to_string(index = False))



    for i in range(0, 50):
        old_num = old_df.iloc[i].at['holders_count']
        new_num = df.iloc[i].at['holders_count']
        if(new_num <= old_num * 0.8) : 
            print(df.iloc[i].at['holder_address'], old_num, new_num)



    df.to_csv('./holders.csv', index = False)

    time_end=time.time()
    print('time cost: ',time_end-time_start,'s')
    return df


if __name__=="__main__":
    run()


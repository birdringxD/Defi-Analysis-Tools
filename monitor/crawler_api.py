import time
import requests
import json
import pandas as pd
import datetime
import telebot
import main

def crawler():
    t = int(round(time.time() * 1000))
    today=datetime.date.today()
    onemonth=datetime.timedelta(days=30)
    lastmoth=int((today-onemonth).strftime("%Y%m%d"))
    today = int(today.strftime("%Y%m%d"))

    # transaction api
    tokens_list = [
        #"tether",
        #"sun",
        #"jfi",
        "blockcola",
        #"tether",
        #"juststablecoin",
    ]

    df = pd.DataFrame(columns=[
        '名称', 
        '市值',
        '发行总量', 
        '流通总量', 
        '当前币价', 
        '24小时交易量',
        '持币地址数量',
    # '实时涨跌幅',
        '一小时涨跌幅',
        '一天涨跌幅',
        '一周涨跌幅',
        '昨日最高',
        '昨日最低',
        '一周最高',
        '一周最低',
        '更新时间'
    ])

    i = 0
    for tokens_list in tokens_list: 
        #print (tokens_list)
        url = "https://fxhapi.feixiaohao.com/public/v1/ticker?code=%s" % (tokens_list)
        #print(url)
        text = requests.get(url).text
        data = json.loads(text)
        #print(data)
        h_url = 'https://dncapi.bqrank.net/api/v3/coin/history?coincode=%s&begintime=%s&endtime=%s&page=1&per_page=100&webp=1' %(tokens_list, lastmoth, today)
        h_text = requests.get(h_url).text
        h_data = json.loads(h_text)

        holder_url = 'https://dncapi.bqrank.net/api/v3/coin/holders?code=%s&webp=1' % (tokens_list)
        holder_text = requests.get(holder_url).text
        holder_data = json.loads(holder_text)
        # c_url = 'https://dncapi.bqrank.net/api/coin/coinchange?code=%s&webp=1' % (tokens_list)
        # c_text = requests.get(c_url).text
        # c_data = json.loads(c_text)

        #price_cny = data['data']['price_cny']
        market_cap_usd = data[0]['market_cap_usd']
        max_supply = data[0]['max_supply']
        available_supply = data[0]['available_supply']  
        price_usd = data[0]['price_usd']
        volume_24h_usd = data[0]['volume_24h_usd']
        addrcount = holder_data['data']['top']['addrcount']
        # change_percent = data['data']['change_percent']
        percent_change_1h = data[0]['percent_change_1h']
        percent_change_24h = data[0]['percent_change_24h']
        percent_change_7d = data[0]['percent_change_7d']
        # change_hour = c_data['data']['change_hour']
        # change_day = c_data['data']['change_day']
        # change_week = c_data['data']['change_week']
        # changerate = h_data['data']['data']['changerate']
        high = h_data['data']['data']['high']
        low = h_data['data']['data']['low']
        high_week = h_data['data']['data']['high_week']
        low_week = h_data['data']['data']['low_week']

        last_updated = data[0]["last_updated"]
        last_updated = time.localtime(int(last_updated)) 
        last_updated = time.strftime("%Y-%m-%d %H:%M:%S", last_updated) 

        text = "当前" + (tokens_list) + "的价格为： $" + str(price_usd)
        main.text_all = main.text_all + text + "\n ------\n"
        print(price_usd)

        df.loc[i] = [
            tokens_list, 
            int(market_cap_usd),
            int(max_supply), 
            int(available_supply),
            price_usd, 
            int(volume_24h_usd),
            addrcount,
            #change_percent,
            percent_change_1h,
            percent_change_24h,
            percent_change_7d,
            high,
            low,
            high_week,
            low_week,
            last_updated
        ]

        i += 1

    #print(df.to_string(index = False))
    #df.to_csv('./coins_list.csv', index = False)
    return main.text_all


if __name__=="__main__":
    crawler()
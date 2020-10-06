#-*-coding:utf8-*-

import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import datetime
import pandas as pd
import re
import telebot
from pyvirtualdisplay import Display

bot = telebot.TeleBot("1392579799:AAGzEhVwQMrPbBEd2BfUFz_bI4M-ODgzNhg")
text_all = " ------ \n"

def crawler():
    global text_all
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
        text_all = text_all + text + "\n ------\n"
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

    print(df.to_string(index = False))
    #df.to_csv('./coins_list.csv', index = False)
    return df


def dex():
    global text_all
    df = pd.DataFrame(columns=[
            '名称', 
            '币价',
            '更新时间', 
            '池子',
        ])
    i = 0

    
    display = Display(visible=0, size=(800, 600))
    display.start()
    options = webdriver.ChromeOptions()
    #options.add_argument("--enable-javascript")
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path='../driver/chromedriver', chrome_options=options)

    list = ["0xdd77c93199064a53e1db19ee0930bcdf7c9999f4",
            "0x00c70e8b3c9d0e0adb85993382abaae2a11c5d96",
            "0xd11684e2ea44128c26877376cb75b9c36e8381dd",
    ]

    for list in list :
        url = "https://sushiswap.vision/pair/%s" % (list)
        driver.get(url)
        time.sleep(15)

        ac = driver.find_element_by_xpath('//button[@class="sc-ifAKCX hWioQc sc-jbKcbu sc-gGBfsJ cqJbMq"]')
        ActionChains(driver).move_to_element(ac).click(ac).perform()

        t = datetime.datetime.now()
        tt = t.strftime('%Y.%m.%d-%H:%M:%S')
        print(tt)

        name = driver.find_element_by_xpath('//span[@class="sc-hXRMBi glnILI"]').text
        print(name)

        price = driver.find_element_by_xpath('//div[@class="sc-bdVaJa jofVNV css-flugrv"]').text
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        price_num = re.findall(p1, price)
        print(price_num[0][1:])
       # print(price)

        top = driver.find_element_by_xpath('//div[@class="sc-VigVT cBSjqC"]')
        pool = top.find_element_by_xpath('//div[@class="sc-kgoBCf bkBlZq"]').text
        #print(pool)
        pool_num = pool.split("\n")
        print(pool_num)
        #print(pool_num[0].replace(',', ''))

        df.loc[i] = [
                name,
                price,
                tt,
                pool_num,
                ]
        i = i + 1
        text = (price) + "  当前池子里有：" + (pool_num[0].replace(',', '')) + " " +  (pool_num[1])
        text_all = text_all + text + "\n ------\n"

    print(df.to_string(index = False))
    #df.to_csv('./dex.csv', index = False)

def run():
    global text_all
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
        if(new_num <= old_num * 0.75) : 
            print(df.iloc[i].at['holder_address'], old_num, new_num)
            text = "可乐有大户出货了： 排名第" + str(i+1) + "的大户持仓减少超过25%， 从" + old_num + "到" + new_num

    text_all = text_all + text + "\n ------\n"

    df.to_csv('./holders.csv', index = False)
    time_end=time.time()
    print('time cost: ',time_end-time_start,'s')
    return df


if __name__=="__main__":
    crawler()
    dex()
    bot.send_message("-472312939", text_all)


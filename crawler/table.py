from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import numpy as np
import requests
import json

text = ''

def run():
    global text 
    text = '预警价格TOP5: | '
    url = 'https://bscscan.com/tokenholdings?a=0xc1db7f59d783e2d0f795b66f175b23d3834c36ee&ps=100&sort=symbol&order=asc'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument("no-sandbox")
    driver = webdriver.Chrome(executable_path='../../driver/chromedriver', chrome_options=options)
    driver.get(url)
    time.sleep(1)

    html = driver.page_source

    soup = BeautifulSoup(html,'html5lib')
    tbody = soup.find('tbody', id = "tb1")
    tr_tags = tbody.find_all('tr')
    unknown = [1388.89, 277.78, 416.67, 277.78, 277.78, 694.44, 416.67, 277.78, 277.78, 694.44, 416.67, 277.78, np.nan, 416.67, 416.67, 416.67]
    symbols = []
    quantities = []
    price = []
    value = []
    speed = []
    early_price = [30.64, 0.1091, 5.577, np.nan, 12866, np.nan, 4.39, 2.6332, 26.54, np.nan, np.nan, 58.97, np.nan, np.nan, 0.256, 2.23]
    warning = []
    liquidation = []
    percentage = []
    early_price2 = [30.86, 0.1087, 5.317, np.nan, 12866, np.nan, 4.33, np.nan, 21.97, np.nan, np.nan, 55.35, np.nan, np.nan, 0.2545, 2.22]
    warning2 = []
    liquidation2 = []
    percentage2 = []
    early_price3 = [np.nan, np.nan, 5.333, np.nan, np.nan, np.nan, np.nan, np.nan, 22.28, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
    warning3 = []
    liquidation3 = []
    percentage3 = []

    for tr in tr_tags:
        td_tags = tr.find_all('td')
        symbols.append(td_tags[2].text)
        num = float(td_tags[3].text.replace(',',''))
        quantities.append(num)

        if (td_tags[4].text == '-') : 
            p = np.nan
        else :
            p = float(td_tags[4].text.split('(', 1 )[0].replace('$', '').replace(',', ''))

        price.append(p)

        if (td_tags[7].text == '-') : 
            value.append(np.nan)
        else :
            num = float(td_tags[7].text.replace('$', '').replace(',', ''))
            value.append(num)


    driver.close()

    df = pd.DataFrame((symbols, quantities, price, value, unknown, speed, 
    early_price, warning, liquidation, percentage,
    early_price2, warning2, liquidation2, percentage2,
    early_price3, warning3, liquidation3, percentage3,
    ))

    df = df.T
    df.columns = ['Symbol','Quantity', 'Price', 'Value', 'Unknown', 'Speed', 
    'Early_price', 'Warning', 'Liquidation', 'Percentage',
    'Early_price2', 'Warning2', 'Liquidation2', 'Percentage2',
    'Early_price3', 'Warning3', 'Liquidation3', 'Percentage3',
    ]

### Atom source change
    url = "https://www.binance.com/api/v3/ticker/price?symbol=ATOMUSDT"
    html = requests.get(url).text
    data = json.loads(html)
    price = float(data['price'])
    df.iloc[2].at['Price'] = price
### 

    df['Speed'] =  10000 / (10000 + df['Value']) * df['Unknown']
    df['Early_price'] = df['Early_price']
    df['Warning'] = (df['Early_price'] * 13 / 15)
    df['Liquidation'] = (df['Early_price'] * 115 / 150)

    df.iloc[2].at['Warning'] = df.iloc[2].at['Early_price'] * 14 / 18
    #print(df.iloc[2].at['Early_price'])
    #print(df.iloc[2].at['Early_price'] * 14 / 18)
    df.iloc[8].at['Warning'] = df.iloc[8].at['Early_price'] * 14 / 18
    df.iloc[2].at['Liquidation'] = df.iloc[2].at['Early_price'] * 12 / 18
    df.iloc[8].at['Liquidation'] = df.iloc[8].at['Early_price'] * 12 / 18
    df['Percentage'] = (df['Price'] - df['Warning']) / df['Warning']

    df['Warning2'] = df['Early_price2'] * 13 / 15
    df['Liquidation2'] = df['Early_price2'] * 115 / 150
    df.iloc[2].at['Warning2'] = df.iloc[2].at['Early_price'] * 14 / 18
    df.iloc[8].at['Warning2'] = df.iloc[8].at['Early_price'] * 14 / 18
    df.iloc[2].at['Liquidation2'] = df.iloc[2].at['Early_price'] * 12 / 18
    df.iloc[8].at['Liquidation2'] = df.iloc[8].at['Early_price'] * 12 / 18
    df['Percentage2'] = (df['Price'] - df['Warning2']) / df['Warning2']

    df['Warning3'] = df['Early_price3'] * 13 / 15
    df['Liquidation3'] = df['Early_price3'] * 115 / 150
    df.iloc[2].at['Warning3'] = df.iloc[2].at['Early_price'] * 14 / 18
    df.iloc[8].at['Warning3'] = df.iloc[8].at['Early_price'] * 14 / 18
    df.iloc[2].at['Liquidation3'] = df.iloc[2].at['Early_price'] * 12 / 18
    df.iloc[8].at['Liquidation3'] = df.iloc[8].at['Early_price'] * 12 / 18
    df['Percentage3'] = (df['Price'] - df['Warning3']) / df['Warning3']

    #df.sort_values('Speed', inplace=True, ascending=False)

    pd.set_option('display.float_format',lambda x : '%.2f' % x)

    df['Speed'] = df['Speed'].map(lambda x: '%.2f' % x)
    df['Warning'] = df['Warning'].map(lambda x: '%.2f' % x)
    df['Liquidation'] = df['Liquidation'].map(lambda x: '%.2f' % x)
    df['Percentage'] = df['Percentage'].map(lambda x: '%.2f' % x)
    df['Warning2'] = df['Warning2'].map(lambda x: '%.2f' % x)
    df['Liquidation2'] = df['Liquidation2'].map(lambda x: '%.2f' % x)
    df['Percentage2'] = df['Percentage2'].map(lambda x: '%.2f' % x)
    df['Warning3'] = df['Warning3'].map(lambda x: '%.2f' % x)
    df['Liquidation3'] = df['Liquidation3'].map(lambda x: '%.2f' % x)
    df['Percentage3'] = df['Percentage3'].map(lambda x: '%.2f' % x)
    df.to_csv('./table.csv')
    per = df['Percentage'].astype(float)
    per = per.sort_values()
    cnt = 5
    for i in per.index:
        if(cnt > 0):
            text += df.iloc[i].at['Symbol'] + ': ' + str(per[i]) + ' | '
            cnt -= 1
    return df

def gettext():
    return text

if __name__=="__main__":
    run()
    t = gettext()
    print(t)




#-*-coding:utf8-*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import datetime
import pandas as pd
import re
import telebot
from pyvirtualdisplay import Display
import main
import json
import requests

def dex():
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
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument("no-sandbox")
    driver = webdriver.Chrome(executable_path='../../driver/chromedriver', chrome_options=options)
    #driver = webdriver.Chrome(chrome_options=options)


### KUN
    url = 'https://mainnet.infura.io/v3/744334c01a994553b8a51c67c931c8d6'
    s = json.dumps({"jsonrpc":"2.0","id":2,"method":"eth_call","params":[{"data":"0x15e84af900000000000000000000000059d4ccc94a9c4c3d3b4ba2aa343a9bdf95145dd100000000000000000000000065d9bc970aa9b2413027fa339f7f179b3f3f2604","to":"0x461e474e594b211d41bb2ff855aa43e455d93888"},"latest"]})
    #d = {"jsonrpc":"2.0","id":2,"method":"eth_call","params":[{"data":"0x15e84af900000000000000000000000059d4ccc94a9c4c3d3b4ba2aa343a9bdf95145dd100000000000000000000000065d9bc970aa9b2413027fa339f7f179b3f3f2604","to":"0x461e474e594b211d41bb2ff855aa43e455d93888"},"latest"]}
    html = requests.post(url, data=s)
    data = json.loads(html.text)
    num = int(data['result'], 16)
    kun = round(num/1000000000000000000, 2)
    text = '1 KUN = ' + str(kun) + ' QUSD' 
    main.text_all = main.text_all + text + "\n ------\n"
### 

### Zeus
    url = "http://info.zeusswap.finance/#/pair/0xa9790d715e5bae2ef66932723d68d1bd8d0d6ae4"
    driver.get(url)
    time.sleep(10)
    ac = driver.find_element_by_xpath('//button[@class="sc-ifAKCX hWioQc sc-dNLxif sc-jnlKLf infGov"]')
    ActionChains(driver).move_to_element(ac).click(ac).perform()
    text = driver.find_element_by_xpath('//div[@class="sc-bdVaJa KpMoH css-flugrv"]').text
    main.text_all = main.text_all + text + "\n ------\n"

### Zeus END

### COLA
    url = "https://justswap.io/#/scan/detail/trx/TSNWgunSeGUQqBKK4bM31iLw3bn9SBWWTG"
    driver.get(url)
    time.sleep(10)
    price = driver.find_elements_by_xpath('//div[@class="pr-price top10 flex"]')[0].text
    pattern = re.compile('.*?\)', re.S)
    price = re.findall(pattern, price)
    text = (price[0])
    main.text_all = main.text_all + text + "\n ------\n"

### COLA END

### SAVE
    url = "https://justswap.io/#/scan/detail/trx/TKeMUmuAiqyKpTKT1Z9TMtzA84bdm4hCyh"
    driver.get(url)
    time.sleep(10)
   # price = driver.find_element_by_xpath('//div[@class="pr-l"]').find_element_by_xpath('//span[@class="left10"]').text
    price = driver.find_elements_by_xpath('//div[@class="pr-price top10 flex"]')[0].text
    pattern = re.compile('.*?\)', re.S)
    price = re.findall(pattern, price)
    text = (price[0])
    main.text_all = main.text_all + text + "\n ------\n"
### SAVE END

### TGAL
#     url = "https://justswap.io/#/scan/detail/trx/TGq2YxmUStqSpaVrg5Lqc3y1yrcbP4VYgU"
#     driver.get(url)
#     time.sleep(10)
#     #print(driver.page_source)

#    # price = driver.find_element_by_xpath('//div[@class="pr-l"]').find_element_by_xpath('//span[@class="left10"]').text
#     price = driver.find_elements_by_xpath('//div[@class="pr-price top10 flex"]')[0].text
#     pattern = re.compile('.*?\)', re.S)
#     price = re.findall(pattern, price)
#     #print(price)
#     #print(price[0])
#     text = (price[0])
#     main.text_all = main.text_all + text + "\n ------\n"
### TGAL END


    list = ["0xdd77c93199064a53e1db19ee0930bcdf7c9999f4",
            #"0x00c70e8b3c9d0e0adb85993382abaae2a11c5d96", LIGHT-ETH
            #"0xd11684e2ea44128c26877376cb75b9c36e8381dd", LIGHT-USDT
    ]

    for list in list :
        url = "https://sushiswap.vision/pair/%s" % (list)
        driver.get(url)
        time.sleep(10)

        ac = driver.find_element_by_xpath('//button[@class="sc-ifAKCX hWioQc sc-jbKcbu sc-gGBfsJ cqJbMq"]')
        ActionChains(driver).move_to_element(ac).click(ac).perform()

        t = datetime.datetime.now()
        tt = t.strftime('%Y.%m.%d-%H:%M:%S')
       # print(tt)

        name = driver.find_element_by_xpath('//span[@class="sc-hXRMBi glnILI"]').text
       # print(name)

        price = driver.find_element_by_xpath('//div[@class="sc-bdVaJa jofVNV css-flugrv"]').text
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        price_num = re.findall(p1, price)
        #print(price_num[0][1:])
        #print(price)

        top = driver.find_element_by_xpath('//div[@class="sc-VigVT cBSjqC"]')
        pool = top.find_element_by_xpath('//div[@class="sc-kgoBCf bkBlZq"]').text
        #print(pool)
        pool_num = pool.split("\n")
        #print(pool_num[0].replace(',', ''))

        df.loc[i] = [
                name,
                price,
                tt,
                pool_num,
                ]
        i = i + 1
        text = (price) + " In Pool: " + (pool_num[0].replace(',', '')) + " " +  (pool_num[1])
        main.text_all = main.text_all + text + "\n ------\n"

    #print(df.to_string(index = False))
    #df.to_csv('./dex.csv', index = False)
    driver.quit()
    return main.text_all




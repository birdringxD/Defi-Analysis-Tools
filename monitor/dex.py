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

def dex():
    df = pd.DataFrame(columns=[
            '名称', 
            '币价',
            '更新时间', 
            '池子',
        ])
    i = 0

    
    #display = Display(visible=0, size=(800, 600))
    #display.start()

    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")

    #driver = webdriver.Chrome(executable_path='../driver/chromedriver', chrome_options=options)
    driver = webdriver.Chrome(chrome_options=options)

    list = ["0xdd77c93199064a53e1db19ee0930bcdf7c9999f4",
            "0x00c70e8b3c9d0e0adb85993382abaae2a11c5d96",
            "0xd11684e2ea44128c26877376cb75b9c36e8381dd",
    ]

    for list in list :
        url = "https://sushiswap.vision/pair/%s" % (list)
        driver.get(url)
        time.sleep(12)

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
        #print(price_num[0][1:])
       # print(price)

        top = driver.find_element_by_xpath('//div[@class="sc-VigVT cBSjqC"]')
        pool = top.find_element_by_xpath('//div[@class="sc-kgoBCf bkBlZq"]').text
        #print(pool)
        pool_num = pool.split("\n")
        #print(pool_num)
        #print(pool_num[0].replace(',', ''))

        df.loc[i] = [
                name,
                price,
                tt,
                pool_num,
                ]
        i = i + 1
        text = (price) + " 池子里有：" + (pool_num[0].replace(',', '')) + " " +  (pool_num[1])
        main.text_all = main.text_all + text + "\n ------\n"

    #print(df.to_string(index = False))
    #df.to_csv('./dex.csv', index = False)
    return main.text_all


#df.to_csv('./dex.csv', index = False)
#driver.find_element_by_css_selector('sc-ifAKCX hWioQc sc-jbKcbu sc-gGBfsJ cqJbMq').click()

#print(driver.save_screenshot)
#print(driver.page_source)
#print(price)
#writer = re.findall('<h1>Paste from (.*?) at', html.text, re.S)




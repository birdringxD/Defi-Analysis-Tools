import requests
import json
import re
import pandas as pd
import main

def eth_holder():
    df = pd.DataFrame(columns=[
        'rank', 
        'holder_address', 
        'holders_count', 
    ])


    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-language': 'zh-CN,zh;q=0.9'}
    response=requests.get('https://cn.etherscan.com/token/tokenholderchart/0x0dbb4b96a23ea7943bb72a8f16cc2c248f372935',headers=headers)
    response.encoding='utf-8'
    html = response.text

    #pattern = re.compile('<script type="text/javascript">.*?</script>', re.S)
    pattern = re.compile('data:.*?</script>', re.S)
    items = re.findall(pattern, html)

    #print(items)
    items = str(items).split(',')

    for i in range(0, len(items)):
        items[i] = items[i].lstrip("\"data: [ ['")
        items[i] = items[i].lstrip(" ")
        items[i] = items[i].lstrip("[")
        items[i] = items[i].rstrip("]")
        items[i] = items[i].lstrip("'")
        items[i] = items[i].rstrip("'")
        #print(i, items[i])

    total = 0
    for i in range(0, 50):
        df.loc[i] = [
            i + 1,
            items[i * 2],
            items[i * 2 + 1]
        ]
        if (items[i * 2] != '0x00c70e8b3c9d0e0adb85993382abaae2a11c5d96' and items[i * 2] != '0xebca2f0306c62cbe7da2808dacc147ec447936af' and items[i * 2] != '0xd11684e2ea44128c26877376cb75b9c36e8381dd') :
            total = total + float(items[i * 2 + 1])


    old_df = pd.read_csv('./eth_holders.csv')
    old_total = 0
    for i in range(0, 50):
        if (old_df.iloc[i].at['holder_address'] != '0x00c70e8b3c9d0e0adb85993382abaae2a11c5d96' and old_df.iloc[i].at['holder_address'] != '0xebca2f0306c62cbe7da2808dacc147ec447936af' and old_df.iloc[i].at['holder_address'] != '0xd11684e2ea44128c26877376cb75b9c36e8381dd') :
            old_total = old_total + float(old_df.iloc[i].at['holders_count'])


    print("total tokens: " + str(total))
    print("old_total tokens: " + str(old_total))

    if(total <= old_total * 0.98):
        text = "! Light top50真实用户持有总量降低超过2%：从" + str(old_total) + "减少到" + str(total)
        text_all = text_all + text + "\n ------\n"

    for i in range(0, 50):
        old_num = float(old_df.iloc[i].at['holders_count'])
        new_num = float(df.iloc[i].at['holders_count'])
        if(new_num <= old_num * 0.85):
            print(df.iloc[i].at['holder_address'], old_num, new_num)
            text = "Light持币排名变动： 排名第" + str(i+1) + "的用户持仓减少超过15%， 从" + str(old_num) + "减少到" + str(new_num)
            main.text_all = main.text_all + text + "\n ------\n"

    #print(df.to_string(index = False))
    df.to_csv('./eth_holders.csv', index = False)
    return main.text_all

if __name__=="__main__":
    eth_holder()


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
import tg
import dex
import crawler_api
import holders
import eth_holders

bot = tg.bot
text_all = ""

if __name__=="__main__":

    crawler_api.crawler()
    dex.dex()
    holders.holder()
    message = eth_holders.eth_holder()
    print(message)
    #tg.send(message)
    #bot.send_message("-472312939", text_all)


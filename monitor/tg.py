import telebot
from telebot import types

TOKEN = '1392579799:AAGzEhVwQMrPbBEd2BfUFz_bI4M-ODgzNhg'
bot = telebot.TeleBot(TOKEN)

def send(text):
    bot.send_message("-472312939", text)

def send_warning(text) :
    bot.send_message("-497234371", text)

if __name__=="__main__":
    #init()
    send_warning("测试")    
import telebot
from telebot import types

TOKEN = '1392579799:AAGzEhVwQMrPbBEd2BfUFz_bI4M-ODgzNhg'
bot = telebot.TeleBot(TOKEN)

def send(text):
    bot.send_message("-472312939", text)


if __name__=="__main__":
    #init()
    send("测试")    
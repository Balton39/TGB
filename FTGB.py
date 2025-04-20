import telebot
import threading
from flask import Flask
from threading import Thread

TOKEN = '8057642755:AAGWAf1TMxEtYNeB3CkCx_vPyqS7eHisuDo'
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я работаю 24/7!")

keep_alive()  # запускаем веб-сервер
bot.infinity_polling()

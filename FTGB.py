import telebot
from telebot import types
from flask import Flask, request

TOKEN = "8057642755:AAGWAf1TMxEtYNeB3CkCx_vPyqS7eHisuDo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Главное меню
@bot.message_handler(commands=['start'])
def send_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Начать")
    bot.send_message(message.chat.id, "Ассаламу алейкум, Алмаз! Я бот Алихан. Могу помочь тебе в твоих вопросах.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Начать")
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Поиск КХыргызов", "Поиск должников в Калининграде")
    markup.add("Продвижение на WB", "Обучение Ozon", "Реклама Авито")
    bot.send_message(message.chat.id, "Выбери одну из опций:", reply_markup=markup)

# Кнопки
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "Поиск КХыргызов" or message.text == "Поиск должников в Калининграде":
        bot.send_message(message.chat.id, "Введите имя:")
        bot.register_next_step_handler(message, lambda m: ask_age(m, message.text))
    elif message.text == "Продвижение на WB":
        send_wb_tips(message)
    elif message.text == "Обучение Ozon":
        send_ozon_tips(message)
    elif message.text == "Реклама Авито":
        send_avito_tips(message)
    elif message.text == "В главное меню":
        send_welcome(message)

# Последовательность вопросов
user_data = {}

def ask_age(message, context):
    user_data[message.chat.id] = {"name": message.text}
    bot.send_message(message.chat.id, "Примерный возраст:")
    bot.register_next_step_handler(message, lambda m: ask_marks(m, context))

def ask_marks(message, context):
    user_data[message.chat.id]["age"] = message.text
    bot.send_message(message.chat.id, "Особые приметы:")
    bot.register_next_step_handler(message, lambda m: ask_debt(m, context))

def ask_debt(message, context):
    user_data[message.chat.id]["marks"] = message.text
    bot.send_message(message.chat.id, "Сумма долга:")
    bot.register_next_step_handler(message, lambda m: show_search(m, context))

def show_search(message, context):
    user_data[message.chat.id]["debt"] = message.text
    bot.send_message(message.chat.id, "Начинаю поиск по всемирной Базе данных... ⏳")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("В главное меню")
    bot.send_message(message.chat.id, "Результаты будут позже", reply_markup=markup)

# Советы
def send_wb_tips(message):
    tips = "Советы для WB:\n- Используйте SEO ключи\n- Актуальные фото\n- Участвуйте в акциях"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("В главное меню")
    bot.send_message(message.chat.id, tips, reply_markup=markup)

def send_ozon_tips(message):
    tips = "Советы для Ozon:\n- Следите за отзывами\n- Заполняйте описание товара полностью"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("В главное меню")
    bot.send_message(message.chat.id, tips, reply_markup=markup)

def send_avito_tips(message):
    tips = "Советы для Авито:\n- Используйте местные теги\n- Делайте понятные заголовки"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("В главное меню")
    bot.send_message(message.chat.id, tips, reply_markup=markup)

# Webhook часть
@app.route(f"/{TOKEN}", methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@app.route("/", methods=['GET'])
def index():
    return "Бот работает!", 200

# Установка webhook при запуске
if __name__ == "__main__":
    import os
    bot.remove_webhook()
    bot.set_webhook(url=f"https://https://tgb-mv9m.onrender.com/{TOKEN}")  # <-- твой Render URL
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

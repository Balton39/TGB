import telebot
from telebot import types

bot = telebot.TeleBot("8057642755:AAGWAf1TMxEtYNeB3CkCx_vPyqS7eHisuDo")

# Стартовое сообщение с кнопкой "Начать"
@bot.message_handler(commands=['start'])
def send_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Начать")
    bot.send_message(
        message.chat.id,
        "Ассаламу алейкум Алмаз! Я бот Алихан. Могу помочь тебе в твоих вопросах.",
        reply_markup=markup
    )

# Главное меню
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Поиск КХыргызов", "Поиск должников в Калининграде")
    markup.add("Продвижение на WB", "Обучение Ozon", "Реклама Авито")
    bot.send_message(message.chat.id, "Выбери одну из опций:", reply_markup=markup)

# Обработка кнопок
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "Начать":
        show_main_menu(message)
    elif message.text == "Поиск КХыргызов" or message.text == "Поиск должников в Калининграде":
        bot.send_message(message.chat.id, "Введите имя:")
        bot.register_next_step_handler(message, lambda m: ask_age(m, message.text))
    elif message.text == "Продвижение на WB":
        send_wb_tips(message)
    elif message.text == "Обучение Ozon":
        send_ozon_tips(message)
    elif message.text == "Реклама Авито":
        send_avito_tips(message)
    elif message.text == "В главное меню":
        show_main_menu(message)

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

# Запуск
bot.polling()

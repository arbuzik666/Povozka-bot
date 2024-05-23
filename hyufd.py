import telebot
from telebot import types
import random
import os

token = '7175201286:AAGaMMdng_3QUr8HBRL9g0XvhSxL-IvI11o'
bot = telebot.TeleBot(token)

# Калькулятор
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    calc_button = types.KeyboardButton('/Калькулятор')
    note_button = types.KeyboardButton('/Заметка')
    remind_button = types.KeyboardButton('/Напоминалка')
    image_button = types.KeyboardButton('/Картинка')
    markup.add(calc_button, note_button, remind_button, image_button)
    bot.send_message(message.chat.id, "Приветствую в обители Ивана!", reply_markup=markup)

@bot.message_handler(commands=['Калькулятор'])
def calc_message(message):
    bot.send_message(message.chat.id, 'Введите математическое выражение:')
    bot.register_next_step_handler(message, calc_handler)

def calc_handler(message):
    try:
        result = eval(message.text)
        bot.send_message(message.chat.id, f'Результат: {result}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

# Заметки с напоминанием
notes = {}

@bot.message_handler(commands=['Заметка'])
def note_message(message):
    bot.send_message(message.chat.id, 'Введите текст заметки:')
    bot.register_next_step_handler(message, note_handler)

def note_handler(message):
    notes[message.chat.id] = message.text
    bot.send_message(message.chat.id, 'Заметка сохранена!')

@bot.message_handler(commands=['Напоминалка'])
def remind_message(message):
    if message.chat.id in notes:
        bot.send_message(message.chat.id, notes[message.chat.id])
    else:
        bot.send_message(message.chat.id, 'У вас нет заметок!')

# Отправление случайной картинки из папки
image_folder = 'C:\\Users\\user\\Desktop\\papochka'

@bot.message_handler(commands=['Картинка'])
def image_message(message):
    images = os.listdir(image_folder)
    image_path = os.path.join(image_folder, random.choice(images))
    bot.send_photo(message.chat.id, open(image_path, 'rb'))


@bot.message_handler(content_types=['text']) 
def unknown_message(message): 
    bot.send_message(message.chat.id, 'Я слишком глупый для таких команд.')
bot.infinity_polling()
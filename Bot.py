import telebot
import sqlite3
import difflib
from my_token import tg_token

Category = {'Разные': 1, 'Афоризмы': 2, 'Цитаты': 3, 'Семейные': 4, 'Армия': 5, 'Интимные': 6,
            'Про студентов': 7, 'Медицинские': 8, 'Про мужчин': 9, 'Народные': 10, 'Наркоманы': 11,
            'Новые Русские': 12,
            'Вовочка': 13, 'Компьютеры': 14, 'Спорт': 15, 'Советские': 16, 'Иностранцы': 17, 'Дорожные': 18,
            'Животные': 19,
            'Черный юмор': 20, 'Сказочные': 21, 'Про евреев': 22, 'Криминал': 23, 'Поручик Ржевский': 24,
            'Про женщин': 25,
            'Штирлиц': 26, 'WOW': 27, 'Киногерои': 28, 'Алкоголики': 29, 'Чукча': 30, 'Реклама': 31, 'Бородатые': 32,
            'Про детей': 33, 'Про программистов': 34, 'Про Путина': 35, 'Полиция': 36, 'Судебные': 37,
            'Про сисадмина': 38,
            'Политика': 39, 'Друзья': 40, 'Про Билла Гейтса': 41, 'Про тещу': 42, 'Про деньги': 43, 'Шоу-бизнес': 44,
            'Школьные': 45}


def get_joke(category):
    conn = sqlite3.connect('jokes.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM anek WHERE category = {category} ORDER BY RANDOM() LIMIT 1 ")
    return cur.fetchone()[2].replace("\\n", "\n")


def get_random_joke():
    conn = sqlite3.connect('jokes.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM anek ORDER BY RANDOM() LIMIT 1 ")
    return cur.fetchone()[2].replace("\\n", "\n")


bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=["start"])
def start_message(message, res=False):
    bot.send_message(message.chat.id,
                     'Привет, ' + message.from_user.first_name + '!\nЯ умею рассказывать анекдоты...')


@bot.message_handler(content_types=["text"])
def other_message(message):
    if message.text in {"анек", "Анек", "Анекдот", "анекдот"}:
        bot.send_message(message.chat.id, get_random_joke())
    elif difflib.get_close_matches(message.text, Category.keys()):
        bot.send_message(message.chat.id,
                         get_joke(Category[difflib.get_close_matches(message.text, Category.keys())[0]]))
    else:
        bot.send_message(message.chat.id,
                         "Извините, " + message.from_user.first_name + ", я не знаю такой команды...\nНапиши нужную категорию или \"aнекдот\"")


bot.polling(none_stop=True, interval=0)

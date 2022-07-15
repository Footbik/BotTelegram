import telebot
from telebot import types
import sqlite3
import sqlite3 as sql
import difflib
from my_token import tg_token
import requests
from time import time
from bs4 import BeautifulSoup as bs

counter_pages = -1
URL = "http://bashorg.org/"

r = requests.get(URL)
soup = bs(r.text, "html.parser")

counter_pages = 0


def get_jokes_from_internet():
    r = requests.get(URL)
    soup = bs(r.text, "html.parser")
    sentence = str(soup.find('td', align='center'))
    s = ''
    for x in sentence[5:-5]:
        if x.isdigit():
            s += x
    s = int(s)
    res: int
    if (res != s):
        res = s
        vacancies_name = soup.find_all('div', class_='quote')
        return vacancies_name


AdminId = frozenset({694690916})

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

CategoryKeys = list(Category.keys())
CategoryKeys.remove('Интимные')
CategoryKeys.remove('Наркоманы')
CategoryKeys.remove('Алкоголики')

d = {
    5: ['майор', "прапорщик", "сержант", "cтаршина", "cержант", "танк"],
    7: ['студент', 'универ', 'колледж', "экзамена", "училище", "экзамен", "профессор"],
    8: ['вpач', "доктор", "аптека", "лекарство", "клиника"],
    4: ['муж', 'жена', 'молодожены'],
    9: ['мужик', 'мужчина'],
    10: ['француз', 'народов', 'хохол', 'кавказец'],
    11: ['менты', 'наркотик'],
    12: ['новый русский', 'новых русских'],
    13: ['Вовочка', 'Вовочке', ' (В)овочку'],
    14: ['антивирусные', 'файлы', 'компьютер', 'Фотошоп', 'курсор'],
    15: ['комментатор', 'футбольная', 'плывет', 'кубок', 'бьют'],
    16: ['Меншиков', 'граф', 'Пушкина', 'князь'],
    17: ['иностранец', 'кризиса', 'стране'],
    18: ['автомобиль', 'скорость', 'водила', 'машина', 'дальнобойщик', 'гаишники'],
    19: ['собаку', 'зоопарка', 'животные', 'грызуны', 'котики'],
    20: ['негр', 'сдох', 'Гитлер', 'феминистки'],
    21: ['сказочные герои', 'Иван-Царевич', 'Царь-батюшка', 'золотую рыбку'],
    22: ['Абрам', 'Еврейская', 'Моня', 'еврей'],
    23: ['коррупции', 'свидетель', 'грабитель', 'уголовная статья'],
    24: ['Поручику Ржевскому', 'Поручик Ржевский', 'Поручик', 'Ржевский'],
    25: ['женщины', 'женщина'],
    26: ['Штирлиц'],
    27: ['ВОВ', 'Ооо', ''],
    28: ['Василий Иваныч', 'Петька', 'Шерлоку Холмсу', 'Холмс'],
    29: ['алкаша', 'пьете', 'пьяный'],
    30: ['чукча', 'чукчу', 'чукчи'],
    31: ['Обявление', 'о б я в л е н и е'],
    33: ['дочка', 'портфель', 'школы', 'сын'],
    34: ['программист', 'баги', 'Из жизни программистов'],
    35: ['Володя Путин', 'Путин', 'Президента Путина', 'Путина'],
    36: ['тюрьма', 'заключённый'],  # ?
    37: ['судом', 'Судья', 'подсудимый', 'судья'],
    38: ['сисадмин'],
    39: ['Кремль', 'Госдума', 'Янукович', 'Верховной Радой'],
    40: ['товарищ', 'друзья', 'друг', 'подруга'],
    41: ['Windows', 'Билла Гейтса', 'Билл Гейтс'],
    42: ['теща', 'тещу', 'теще', 'зять'],
    43: ['деньги', 'рубль', 'зарабатывать'],
    44: ['режиссер', 'артистов', 'актер', 'Филипп Киркоров'],
    45: ['учитель', 'урок', 'теорема', 'теорему']
}


def category(text):
    for cat in d:
        keywords = d[cat]
        for keyword in keywords:
            if keyword in text:
                connection = sqlite3.connect("jokes.db")
                cursor = connection.cursor()
                text_insert = f'''INSERT INTO anek
                                (id,category, anekdot)
                                VALUES
                                (15.07,{cat} , "{text}");'''
                cursor.execute(text_insert)
                connection.commit()
                cursor.close()
                return cat


def get_joke(category):
    conn = sqlite3.connect('jokes.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM anek WHERE category = {category} ORDER BY RANDOM() LIMIT 1 ")
    return cur.fetchone()[2].replace("\\n", "\n")


def is_joke_in_table(new_anekdot):
    con = sqlite3.connect('jokes.db')
    cur = con.cursor()
    cur.execute("select id from POSTS where id=?", (new_anekdot,))
    data = cur.fetchall()
    if data is None:
        new_anekdot.get_category()
    con.close()


def put_joke_in_table(new_anekdot, category):
    con = sql.connect('jokes.db')
    cur = con.cursor()
    sqlite_insert_query = """INSERT INTO jokes.db (category, anekdot)
                          VALUES ({}, {});""".format(category, new_anekdot)
    count = cur.execute(sqlite_insert_query)
    con.commit()
    cur.close()


def get_random_joke():
    conn = sqlite3.connect('jokes.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM anek ORDER BY RANDOM() LIMIT 1 ")
    return cur.fetchone()[2].replace("\\n", "\n")


bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, я умею в шутки...")


def change_markup(message):
    global markup
    global counter_pages
    for i in CategoryKeys[counter_pages * 5: (counter_pages + 1) * 5]:
        markup.add(types.KeyboardButton(i))
    markup.add(types.KeyboardButton('Далее >>'))
    markup.add(types.KeyboardButton('Выйти в меню'))
    show_buttons(message)


def show_buttons(message):
    bot.send_message(message.chat.id, 'Выбери категорию' if counter_pages != -1 else 'Чего желаете?',
                     reply_markup=markup)


@bot.message_handler(commands=["menu"])
def button_message(message):
    global markup
    global counter_pages
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in ['Помощь', 'Анекдоты по категориям', 'Случайный анекдот']:
        markup.add(types.KeyboardButton(i))
    counter_pages = -1
    bot.send_message(message.chat.id, "Меню в кнопках", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def other_message(message):
    global markup
    global counter_pages
    if message.text in {"Анекдоты по категориям"}:
        counter_pages = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        change_markup(message)
    elif message.text in {"анек", "Анек", "Анекдот", "анекдот", "Случайный анекдот"}:
        bot.send_message(message.chat.id, get_random_joke())
    elif message.text in {"Найди новые шутки", "Найди новые анекдоты"}:
        if message.chat.id in AdminId:
            bot.send_message(message.chat.id, f"Делаю запрос на сайт {URL}")
            # put_joke_in_table(get_category(is_joke_in_table(get_jokes_from_internet())))
        else:
            bot.send_message(message.chat.id, "У вас недостаточно прав для данной команды:(")
    elif difflib.get_close_matches(message.text, Category.keys()):
        bot.send_message(message.chat.id,
                         get_joke(Category[difflib.get_close_matches(message.text, Category.keys())[0]]))
    elif message.text == 'Далее >>':
        if not counter_pages == 4:
            counter_pages += 1
        else:
            counter_pages = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        change_markup(message)
    elif message.text == 'Выйти в меню':
        counter_pages = 0
        button_message(message)
    elif message.text == 'Помощь':
        bot.send_message(message.chat.id,
                         """Что? Тебе нужна помощь?
Боже, ну, я анекдотер, посылаю анекдоты, чтобы ты их прочитал...
В чем смысл жизни?
Посмеялись?
Нет?
ъуъ!
Тоже не смешно?
Тогда привыкайте, лучше шуток не будет.""")


bot.polling(none_stop=True, interval=0)

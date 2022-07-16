import telebot
from telebot import types
import sqlite3
import sqlite3 as sql
import difflib
import requests
from bs4 import BeautifulSoup as bs

counter_pages = -1
URL = "http://bashorg.org/"

counter_pages = 0

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


def get_jokes_from_internet():
    r = requests.get(URL)
    soup = bs(r.text, "html.parser")
    sentence = str(soup.find('td', align='center'))
    # Мы узнаем кол-во анекдотов в данный момент
    # Забираем информацию в виде строки и теперь нам нужно извлечь из этой строки число - кол-во анекдотов
    s = ''
    for x in sentence[5:-5]:
        if x.isdigit():
            s += x
    s = int(s)
    # Мы получили искомое число
    with open("previous_jokes_count.txt", "r") as file:
        res = file.read()
        res = int(res)
    # Сравниваем кол-во анекдлотов в данный момент с прошлым кол-вом анекдотов
    if res < s:
        with open("previous_jokes_count.txt", "w") as file:
            res = s
            file.write(str(res))
        # Переменной с старым значением присваивается новое число
        jokes = soup.find_all('div', class_='quote')
        output = []
        for joke in jokes:
            output.append(str(joke)[19:-6])
            output[-1] = "\n".join(output[-1].split("<br/>"))
        return output
    else:
        return False


def get_category(text):
    for cat in d:
        keywords = d[cat]
        for keyword in keywords:
            if keyword in text:
                connection = sqlite3.connect("jokess.db")
                cursor = connection.cursor()
                text_insert = f'''INSERT INTO anek
                                (id,category, anekdot)
                                VALUES
                                (15.07,{cat} , "{text}");'''
                cursor.execute(text_insert)
                connection.commit()
                cursor.close()
                return cat
        return 1


def get_joke(category):
    conn = sqlite3.connect('jokess.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM anek WHERE category = {category} ORDER BY RANDOM() LIMIT 1 ")
    return cur.fetchone()[2].replace("\\n", "\n").replace("&quot;", '"')


def is_joke_in_table(new_anekdot):
    con = sqlite3.connect('jokess.db')
    cur = con.cursor()
    cur.execute("select id from anek where id=?", (new_anekdot,))
    data = cur.fetchall()
    con.close()
    if data is None:
        return True
    else:
        return False


con = sql.connect('jokes.db')
cur = con.cursor()
cur.execute("""DELETE FROM anek WHERE _rowid_ >= 130367""")


def put_joke_in_table(new_anekdot, category):
    con = sql.connect('jokess.db')
    cur = con.cursor()
    cur.execute('''SELECT id FROM anek ORDER BY id DESC''')
    print(cur.fetchone())
    # n = int(cur.fetchone()[0]) + 1
    # print(n)
    sqlite_insert_query = """INSERT INTO anek (id, category, anekdot)
                          VALUES ({}, {}, '{}');""".format(n, category, new_anekdot)
    cur.execute(sqlite_insert_query)
    con.commit()
    cur.close()
    print([new_anekdot])


def find_and_save_new_jokes():
    a = get_jokes_from_internet()
    for i in a:
        if not is_joke_in_table(i):
            put_joke_in_table(i, get_category(i))
        else:
            print("Bruh")


def get_random_joke():
    conn = sqlite3.connect('jokess.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM anek ORDER BY RANDOM() LIMIT 1 ")
    return cur.fetchone()[2].replace("\\n", "\n").replace("&quot;", '"')


bot = telebot.TeleBot("5501718145:AAGzjQtia3a12rM7YOQPf-ctKlkt8nfeIgc")


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Привет, я бот-агрегатор, мама всегда мне говорила, что я клоун, так что буду делать то, что умею - шутить")
    button_message(message)


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
    bot.send_message(message.chat.id, "Там в меню появились кнопочки, так что можешь выбрать, что душе угодно",
                     reply_markup=markup)


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
            find_and_save_new_jokes()
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
    else:
        bot.send_message(message.chat.id, f"Извините, {message.from_user.first_name}, я не знаю такой команды:(")


bot.polling(none_stop=True, interval=0)

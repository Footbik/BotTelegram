import telebot
from my_token import tg_token

bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=["start"])
def start_message(message, res=False):
    bot.send_message(message.chat.id,
                     'Привет, ' + message.from_user.first_name + '!\nЯ умею рассказывать анекдоты...')


@bot.message_handler(content_types=["text"])
def other_message(message):
    if message.text in {"Анекдот", "Шутка", "Анек", "анек", "анекдот"}:
        bot.send_message(message.chat.id, "Тут должен был быть анекдот")
    else:
        bot.send_message(message.chat.id,
                         "Извините, " + message.from_user.first_name + ", я не знаю такой команды...\nНапиши нужную категорию или \"aнекдот\"")


bot.polling(none_stop=True, interval=0)

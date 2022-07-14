import requests
from discord.ext import commands
from bs4 import BeautifulSoup as bs

client = commands.Bot(command_prefix="/") #Создаём префикс для команд
URL_TEMPLATE = "http://bashorg.org/byrating" #Создаём ссылку, из которой будем брать текст
r = requests.get(URL_TEMPLATE)
soup = bs(r.text, "html.parser")
vacancies_names = soup.find_all('div', class_='quote') #Ищем текст по заданным критериям
@client.command()
async def anek(ctx): #Создаём функцию вывода текста
    for name in vacancies_names:
        output = str(name)[19:-6]
        await ctx.send("\n".join(output.split("<br/>")))
        break
client.run("Токен") #Вставляем токен дискорд-бота
bot.polling(none_stop=True, interval=0) #Ставим дискорд-бота на повтор

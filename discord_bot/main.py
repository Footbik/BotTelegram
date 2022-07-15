import sqlite3
from discord.ext import commands
from config import settings, Category
import difflib
TOKEN = settings.get('token')
bot = commands.Bot(command_prefix='/')

# commands.Context.fetch_message()

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


@bot.event
async def on_message(ctx):
    msg = ctx.content
    print(ctx.content)
    if ctx.author != bot.user and msg[0] == '!' and msg[1:] != 'categories':
        if msg[1:].lower() in {"анек", "анекдот", 'шутка', "anek", 'anekdot', "фтул", "фтулвще", "fytr", " fytrljn"}:
            await ctx.reply(get_random_joke())
        elif difflib.get_close_matches(msg[1:], Category.keys()):
            await ctx.reply(get_joke(Category[difflib.get_close_matches(msg[1:], Category.keys())[0]]))
        else:
            await ctx.reply("Извините, " + str(ctx.author.name) + ", я не смог подобрать для вас анекдот. Попробуйте другую категорию")


    elif msg[1:] == "categories":
        local = 'Категории Анекдотов:\n'
        for i in Category.keys():
            local += '- ' + i + '\n'
        await ctx.reply(local)





bot.run(TOKEN)

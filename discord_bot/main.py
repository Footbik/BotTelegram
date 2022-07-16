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
    return cur.fetchone()[2].replace("\\n", "\n").replace("&quot;", '"')


def get_random_joke():
    conn = sqlite3.connect('jokes.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM anek ORDER BY RANDOM() LIMIT 1 ")
    return cur.fetchone()[2].replace("\\n", "\n").replace("&quot;", '"')


@bot.event
async def on_message(ctx):
    msg = ctx.content
    if msg[0] == '!' and msg[1:] not in ("categories", "help"):
        if ctx.author != bot.user:
            if msg[1:].lower() in {"анек", "анекдот", 'шутка', "anek", 'anekdot', "фтул", "фтулвще", "fytr",
                                   " fytrljn"}:
                await ctx.reply(get_random_joke())
            elif difflib.get_close_matches(msg[1:], Category.keys()):
                await ctx.reply(get_joke(Category[difflib.get_close_matches(msg[1:], Category.keys())[0]]))
            else:
                await ctx.reply("Извините, " + str(
                    ctx.author.name) + ", я не смог подобрать для вас анекдот. Попробуйте другую категорию")


    elif msg[1:] == "categories" and msg[0] == '!':
        local = 'Категории Анекдотов:\n- Анекдот(Cлучайный)\n'
        for i in Category.keys():
            local += '- ' + i + '\n'
        await ctx.reply(local)
    elif msg[1:] == "help" and msg[0] == "!":
        await ctx.reply("""
        Привет! Я бот шутник! Ты можешь писать мне категории(в формате !категория), а я буду присылать тебе анекдоты на эту тему.\nКатегории можно узнать командой !categories.""")


@bot.event
async def on_guild_join(guild):
    msg = """Тук, тук, тук! Я вхожу! Напиши !help для информации"""
    try:
        joinchannel = guild.system_channel
        # The system channel is where Discord’s join messages are sent
        await joinchannel.send(msg)
    except:
        # if no system channel is found send to the first channel in guild
        await guild.text_channels[0].send(msg)


bot.run(TOKEN)

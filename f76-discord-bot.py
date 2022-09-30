from os import getenv
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import discord
import requests

load_dotenv()

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="!help")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    # Если пишет сам бот, то ничего не делаем
    if message.author == client.user:
        return

    desc = f"На сервере у {message.author}"

    # справка
    if message.content == '!h' or message.content == '!help':
        emb = discord.Embed(title='СПРАВКА', color=discord.Colour.dark_orange())
        emb.set_thumbnail(url="https://bestuzheff.github.io/images/f76_nuca_cola.webp")        
        emb.add_field(name='Команды бота:', value="""
        **!h** - справка по боту 
        **!к** - коды запуска ракет 
        **!м** - событие Горелая земля
        **!э** - событие Колоссальная проблема
        **!б** - событие Криптидография\n""", inline=False)
        emb.set_footer(text='По вопросам работы бота писать @bestuzheff#3788')
        await message.channel.send(embed=emb)

    # Вывод кодов запуска ракет
    if message.content == '!к' or message.content == '!k':
        # Получим коды запуска ракет
        codes = get_nuka_codes()
        if len(codes) == 3:
            emb = discord.Embed(title='КОДЫ ЗАПУСКА РАКЕТ', color=discord.Colour.dark_orange())
            emb.set_thumbnail(url="https://bestuzheff.github.io/images/f76_bomb.webp")
            emb.add_field(name='Альфа', value=codes[0], inline=True)
            emb.add_field(name='Браво', value=codes[1], inline=True)
            emb.add_field(name='Чарли', value=codes[2], inline=True)
        else:
            emb = discord.Embed(title="Получить коды запуска ракет не удалось!")
        await message.channel.send(embed=emb)

    # События
    # Матка
    if message.content.startswith('!м'):
        emb = discord.Embed(title='СОБЫТИЕ ГОРЕЛАЯ ЗЕМЛЯ', description=desc, color=0x7289da)
        emb.set_thumbnail(url="https://bestuzheff.github.io/images/f76_Scorched_quest.webp")
        note = get_note(message.content)
        if note != '':
            emb.add_field(name='Примечание', value=note, inline=False)
        await message.channel.send(embed=emb)

    # Эрл
    if message.content.startswith('!э'):
        emb = discord.Embed(title='СОБЫТИЕ КОЛОССАЛЬНАЯ ПРОБЛЕМА', description=desc, color=0x7289da)
        emb.set_thumbnail(url="https://bestuzheff.github.io/images/f76_wst_colossus.webp")
        note = get_note(message.content)
        if note != '':
            emb.add_field(name='Примечание', value=note, inline=False)
        await message.channel.send(embed=emb)

    # Баран
    if message.content.startswith('!б'):
        emb = discord.Embed(title='СОБЫТИЕ КРИПТИДОГРАФИЯ', description=desc, color=0x7289da)
        emb.set_thumbnail(url="https://bestuzheff.github.io/images/f76_cryptide.png")
        note = get_note(message.content)
        if note != '':
            emb.add_field(name='Примечание', value=note, inline=False)
        await message.channel.send(embed=emb)


def get_nuka_codes():
    codes = []

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0', }
    response = requests.get("https://nukacrypt.com", timeout=15, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        nuclearcodess = soup.find("div", {"id": "nuclearcodess"})
        quotes = nuclearcodess.find_all("td")
        for nuca_code in quotes:
            nuca_code_text = nuca_code.text
            if nuca_code_text.isdigit():
                codes.append(nuca_code_text)
    return codes


def get_note(message):
    note = message[2:].strip()
    return note


client.run(bot_token)

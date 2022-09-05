import discord
import requests
from os import getenv
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

bot_token = getenv("BOT_TOKEN")



intents = discord.Intents.default()
# intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # Если пишет сам бот, то ничего не делаем
    if message.author == client.user:
        return

    # Вывод справки
    if message.content == '!к' or message.content == '!k':
        # Получим коды запуска ракет
        codes = get_nuka_codes()
        if len(codes) == 3:
            emb = discord.Embed(title='☢ Коды запуска ракет ☢', color=discord.Colour.dark_orange())
            emb.add_field(name='Альфа:', value=codes[0], inline=True)
            emb.add_field(name='Браво:', value=codes[1], inline=True)
            emb.add_field(name='Чарли:', value=codes[2], inline=True)
            emb.set_footer(text='По вопросам работы бота писать @bestuzheff#3788')
        else:
            emb = discord.Embed(title="Получить коды запуска ракет не удалось!")
        await message.channel.send(embed=emb)


def get_nuka_codes():
    codes = []
    response = requests.get("https://nukacrypt.com/", timeout=15)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        nuclearcodess = soup.find("div", {"id": "nuclearcodess"})
        quotes = nuclearcodess.find_all("td")
        for nucaCode in quotes:
            nucaCodeText = nucaCode.text
            if nucaCodeText.isdigit():
                codes.append(nucaCodeText)
    return codes
    

client.run(bot_token)

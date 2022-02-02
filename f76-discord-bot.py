import os
import discord

bot_token = os.getenv("TOKEN")
if not bot_token:
    exit("Error: no token provided")

# bot_id = os.getenv("BOT_ID")
# if not bot_id:
#     exit("Error: no bot id provided")

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # Если пишет сам бот, то ничего не делаем
    if message.author == client.user:
        return

    # Вывод справки
    if message.content == '!h' or message.content == '!help':
        emb = discord.Embed(title="🪧 СПРАВКА ПО КОМАНДАМ")
        # Карма
        emb.add_field(name=">> КАРМА", value="Рейтинг пользователей", inline=False)
        emb.add_field(name="Увеличение кармы:", value="+karma @пользователь", inline=True)
        emb.add_field(name='Уменьшение кармы:', value="-karma @пользователь", inline=True)
        emb.add_field(name="Узнать карму:", value="!karma @пользователь", inline=True)

        # Коды запуска
        # emb.add_field(name=">> КОДЫ", value="Коды запуска ядерных ракет", inline=False)
        # emb.add_field(name="!k", value="Вывести коды запуска на эту неделю", inline=False)

        emb.set_footer(text="☢ Fallout 76 | Our Future Begins ☢")
        await message.channel.send(embed=emb)

    if message.content.startswith("+karma"):
        await message.channel.send('Увеличение кармы!')
        # user_id_string = message.content.removeprefix("+karma ")
        # user_id = get_user_id_from_string(user_id_string)
        # user = await client.fetch_user(user_id)
        # await message.channel.send(user)

    if message.content.startswith("-karma"):
        await message.channel.send('Уменьшение кармы!')

    if message.content.startswith("!karma"):
        await message.channel.send('Проверка кармы!')

client.run(bot_token)


# Функция убирает из строки пользователя лишние символы и преобразует в число
def get_user_id_from_string(users_string):
    users_string = users_string.removeprefix("<@")
    users_string = users_string.removesuffix(">")
    if users_string.isdigit():
        return int(users_string)
    else:
        return 0

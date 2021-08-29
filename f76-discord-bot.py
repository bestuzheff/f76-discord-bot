import os
import discord

bot_token = os.getenv("TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot_id = os.getenv("BOT_ID")
if not bot_id:
    exit("Error: no bot id provided")


# Функция убирает из строки пользователя лишние символы и преобразует в число
def get_user_id_from_string(users_string):
    users_string = users_string.removeprefix("<@")
    users_string = users_string.removesuffix(">")
    if users_string.isdigit():
        return int(users_string)
    else:
        return 0


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):

        # Если пишет сам бот, то ничего не делаем
        if message.author == self.user:
            return

        # Вывод справки
        if (bot_id in message.content) or message.content == '!h' or message.content == '!help':
            emb = discord.Embed(title="🪧 СПРАВКА ПО КОМАНДАМ")
            # Карма
            emb.add_field(name=">> КАРМА", value="Рейтинг пользователей", inline=False)
            emb.add_field(name="Увеличение кармы:", value="+karma @пользователь", inline=True)
            emb.add_field(name="Уменьшение кармы:", value="-karma @пользователь", inline=True)
            emb.add_field(name="Узнать карму:", value="!karma @пользователь", inline=True)

            # Коды запуска
            # emb.add_field(name=">> КОДЫ", value="Коды запуска ядерных ракет", inline=False)
            # emb.add_field(name="!k", value="Вывести коды запуска на эту неделю", inline=False)

            emb.set_footer(text="☢ Fallout 76 | Our Future Begins ☢ <@548652307521339413>")
            await message.channel.send(embed=emb)

        if message.content.startswith("+karma"):
            user_id_string = message.content.removeprefix("+karma ")
            user_id = get_user_id_from_string(user_id_string)
            user = await client.fetch_user(user_id)
            await message.channel.send(user)

        if message.content.startswith("-karma"):
            await message.channel.send('Уменьшение кармы!')

        if message.content.startswith("!karma"):
            await message.channel.send('Проверка кармы!')


client = MyClient()
client.run(bot_token)

# @client.command()
# async def name(ctx):
#     user = await client.fetch_user('<user id>')
#     await user.send('hey')

FROM python:3.10-slim

WORKDIR /app

COPY ./images /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY f76-discord-bot.py f76-discord-bot.py
COPY .env .env


CMD [ "python3", "f76-discord-bot.py"]
import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота от BotFather
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# API ключ OpenWeatherMap
OWM_API_KEY = os.getenv("OWM_API_KEY")

# Город для прогноза
CITY = "Krasnodar"

# ID чатов для рассылки (необязательно для простого бота)
MY_CHAT_ID = os.getenv("MY_CHAT_ID")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")

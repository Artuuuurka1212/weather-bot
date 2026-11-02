import os

# GitHub Actions сам подставит эти значения из "Secrets"
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWM_API_KEY = os.getenv("OWM_API_KEY")
MY_CHAT_ID = os.getenv("MY_CHAT_ID")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
CITY = "Krasnodar"
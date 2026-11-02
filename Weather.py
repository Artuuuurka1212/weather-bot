import asyncio
from aiogram import Bot
from config import BOT_TOKEN, MY_CHAT_ID, GROUP_CHAT_ID
from weather_api import get_weather


async def main():
    bot = Bot(token=BOT_TOKEN)
    weather_text = await get_weather()

    print("Отправляю погоду...")

    # Отправка лично
    if MY_CHAT_ID:
        await bot.send_message(MY_CHAT_ID, weather_text, parse_mode="HTML")
        print(f"✅ Отправлено лично (ID: {MY_CHAT_ID})")

    # Отправка в группу
    if GROUP_CHAT_ID:
        await bot.send_message(GROUP_CHAT_ID, weather_text, parse_mode="HTML")
        print(f"✅ Отправлено в группу (ID: {GROUP_CHAT_ID})")

    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
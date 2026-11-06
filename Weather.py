import asyncio
from aiogram import Bot
from aiogram.types import FSInputFile  # <-- ВАЖНО: добавлен этот импорт
from config import BOT_TOKEN, MY_CHAT_ID, GROUP_CHAT_ID
from weather_api import get_daily_forecast_with_data
from weather_card import create_weather_card


async def main():
    bot = Bot(token=BOT_TOKEN)

    # 1. Получаем данные погоды
    weather_data = await get_daily_forecast_with_data()

    if "error" in weather_data:
        print(f"❌ Ошибка: {weather_data['error']}")
        return

    # 2. Генерируем карточку
    print("🎨 Генерирую карточку погоды...")
    card_path = create_weather_card(
        city=weather_data["city"],
        date=weather_data["date"],
        weekday=weather_data["weekday"],
        min_temp=weather_data["min_temp"],
        max_temp=weather_data["max_temp"],
        avg_temp=weather_data["avg_temp"],
        description=weather_data["description"],
        rain_chance=weather_data["rain_chance"]
    )

    # 3. Формируем текстовое сообщение
    text = (
        f"🌍 <b>Прогноз на сегодня ({weather_data['city']})</b>\n"
        f"📅 {weather_data['date']}, {weather_data['weekday']}\n\n"
        f"🌡 <b>Температура:</b> от {weather_data['min_temp']}° до {weather_data['max_temp']}°C\n"
        f"🌡 <b>Средняя:</b> {weather_data['avg_temp']}°C\n"
        f"🌥 <b>Погода:</b> {weather_data['description']}\n"
        f"🌧 <b>Шанс дождя:</b> {weather_data['rain_chance']}%\n"
    )

    if weather_data["rain_chance"] >= 80:
        text += "\n⚠️ <i>Скорее всего, будет дождь. Возьми зонт!</i>\n"
    elif weather_data["rain_chance"] >= 50:
        text += "\n🌂 <i>Возможен дождь. Зонт не помешает.</i>\n"
    elif weather_data["rain_chance"] >= 20:
        text += "\n☁️ <i>Небольшая вероятность дождя.</i>\n"
    else:
        text += "\n☀️ <i>Дождя не ожидается.</i>\n"

    text += "\n✨ <b>Хорошего дня!</b>"

    # 4. Отправляем сообщение с картинкой (ИСПРАВЛЕННЫЙ БЛОК)
    print("📤 Отправляю прогноз...")

    # Создаем специальный объект файла для aiogram 3.x
    photo_file = FSInputFile(card_path)

    if MY_CHAT_ID:
        await bot.send_photo(
            MY_CHAT_ID,
            photo=photo_file,  # <-- Передаем объект FSInputFile, а не open()
            caption=text,
            parse_mode="HTML"
        )
        print(f"✅ Отправлено лично (ID: {MY_CHAT_ID})")

    if GROUP_CHAT_ID:
        await bot.send_photo(
            GROUP_CHAT_ID,
            photo=photo_file,
            caption=text,
            parse_mode="HTML"
        )
        print(f"✅ Отправлено в группу (ID: {GROUP_CHAT_ID})")

    await bot.session.close()
    print("✅ Готово!")


if __name__ == "__main__":
    asyncio.run(main())

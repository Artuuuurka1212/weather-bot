import aiohttp
from config import OWM_API_KEY, CITY


# Маппинг кодов погоды OWM на эмодзи
WEATHER_EMOJIS = {
    "01d": "☀️", "01n": "🌙",
    "02d": "🌤", "02n": "🌙",
    "03d": "☁️", "03n": "☁️",
    "04d": "☁️", "04n": "☁️",
    "09d": "🌧", "09n": "🌧",
    "10d": "🌦", "10n": "🌧",
    "11d": "⛈", "11n": "⛈",
    "13d": "🌨", "13n": "🌨",
    "50d": "🌫", "50n": "🌫",
}


async def get_weather() -> str:
    """Получает текущую погоду в Краснодаре с OpenWeatherMap."""
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={OWM_API_KEY}&units=metric&lang=ru"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return "❌ Не удалось получить погоду. Попробуйте позже."

                data = await response.json()

        # Достаем нужные данные
        temp = round(data["main"]["temp"])
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        icon_code = data["weather"][0]["icon"]
        emoji = WEATHER_EMOJIS.get(icon_code, "🌡")
        
        # Шанс дождя (вероятность осадков от 0 до 1)
        rain_probability = data.get("rain", {}).get("1h", 0)
        pop = data.get("pop", 0)  # Probability of precipitation
        rain_chance = round(pop * 100)

        # Формируем красивое сообщение
        text = (
            f"🌍 <b>Погода в Краснодаре</b>\n\n"
            f"{emoji} <b>Температура:</b> {temp}°C\n"
            f"🌥 <b>Состояние:</b> {description.capitalize()}\n"
            f"💨 <b>Ветер:</b> {wind_speed} м/с\n"
            f"🌧 <b>Шанс дождя:</b> {rain_chance}%\n\n"
            f"✨ <b>Хорошего дня!</b>"
        )
        return text

    except Exception as e:
        print(f"Ошибка при запросе погоды: {e}")
        return "❌ Произошла ошибка. Попробуйте позже."

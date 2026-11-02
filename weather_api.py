import aiohttp
from config import OWM_API_KEY, CITY


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

        temp = round(data["main"]["temp"])
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        icon_code = data["weather"][0]["icon"]
        emoji = WEATHER_EMOJIS.get(icon_code, "🌡")

        text = (
            f"🌍 <b>Погода в Краснодаре</b>\n\n"
            f"{emoji} <b>Температура:</b> {temp}°C\n"
            f"🌥 <b>Состояние:</b> {description.capitalize()}\n"
            f"💨 <b>Ветер:</b> {wind_speed} м/с"
        )
        return text

    except Exception as e:
        print(f"Ошибка при запросе погоды: {e}")
        return "❌ Произошла ошибка. Попробуйте позже."
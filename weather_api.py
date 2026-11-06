import aiohttp
from config import OWM_API_KEY, CITY
from datetime import datetime, timedelta, timezone

# Словарь для перевода названий городов
CITY_NAMES_RU = {
    "Krasnodar": "Краснодар",
    "Moscow": "Москва",
    "Saint Petersburg": "Санкт-Петербург",
    "Novosibirsk": "Новосибирск",
    "Yekaterinburg": "Екатеринбург",
    "Kazan": "Казань",
    "Nizhny Novgorod": "Нижний Новгород",
    "Chelyabinsk": "Челябинск",
    "Samara": "Самара",
    "Rostov-on-Don": "Ростов-на-Дону",
    "Ufa": "Уфа",
    "Krasnoyarsk": "Красноярск",
    "Voronezh": "Воронеж",
    "Perm": "Пермь",
    "Volgograd": "Волгоград",
}

# Словарь для перевода дней недели
WEEKDAYS_RU = {
    "Monday": "понедельник",
    "Tuesday": "вторник",
    "Wednesday": "среда",
    "Thursday": "четверг",
    "Friday": "пятница",
    "Saturday": "суббота",
    "Sunday": "воскресенье"
}


async def get_daily_forecast() -> str:
    """Возвращает текстовый прогноз погоды на сегодня."""

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={CITY}&appid={OWM_API_KEY}&units=metric&lang=ru"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return "❌ Не удалось получить прогноз. Попробуйте позже."

                data = await response.json()

        msk_tz = timezone(timedelta(hours=3))
        today_msk = datetime.now(msk_tz)
        today_str = today_msk.strftime("%Y-%m-%d")

        weekday_en = today_msk.strftime("%A")
        weekday_ru = WEEKDAYS_RU.get(weekday_en, weekday_en)
        city_ru = CITY_NAMES_RU.get(CITY, CITY)

        today_forecast = [
            item for item in data["list"]
            if item["dt_txt"].startswith(today_str)
        ]

        if not today_forecast:
            return f"❌ Прогноз на сегодня ({today_str}) недоступен."

        temps = [item["main"]["temp"] for item in today_forecast]
        avg_temp = round(sum(temps) / len(temps))
        min_temp = round(min(temps))
        max_temp = round(max(temps))

        max_rain_chance = 0
        for item in today_forecast:
            pop = item.get("pop", 0)
            rain_chance = round(pop * 100)
            if rain_chance > max_rain_chance:
                max_rain_chance = rain_chance

        descriptions = [item["weather"][0]["description"] for item in today_forecast]
        most_common_description = max(set(descriptions), key=descriptions.count)

        # Формируем текст построчно (чтобы избежать ошибок с f-строками)
        lines = []
        lines.append(f"🌍 <b>Прогноз на сегодня ({city_ru})</b>")
        lines.append(f"📅 {today_msk.strftime('%d.%m.%Y')}, {weekday_ru}")
        lines.append("")
        lines.append(f"🌡 <b>Температура:</b> от {min_temp}° до {max_temp}°C")
        lines.append(f"🌡 <b>Средняя:</b> {avg_temp}°C")
        lines.append(f"🌥 <b>Погода:</b> {most_common_description.capitalize()}")
        lines.append(f"🌧 <b>Шанс дождя:</b> {max_rain_chance}%")
        lines.append("")

        if max_rain_chance >= 80:
            lines.append("⚠️ <i>Скорее всего, будет дождь. Возьми зонт!</i>")
        elif max_rain_chance >= 50:
            lines.append("🌂 <i>Возможен дождь. Зонт не помешает.</i>")
        elif max_rain_chance >= 20:
            lines.append("☁️ <i>Небольшая вероятность дождя.</i>")
        else:
            lines.append("☀️ <i>Дождя не ожидается.</i>")

        lines.append("")
        lines.append("✨ <b>Хорошего дня!</b>")

        text = "\n".join(lines)

        return text

    except Exception as e:
        print(f"Ошибка при запросе прогноза: {e}")
        return "❌ Произошла ошибка. Попробуйте позже."


async def get_daily_forecast_with_data() -> dict:
    """Возвращает данные погоды в виде словаря для генерации карточки."""

    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={CITY}&appid={OWM_API_KEY}&units=metric&lang=ru"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return {"error": "Не удалось получить прогноз"}

                data = await response.json()

        msk_tz = timezone(timedelta(hours=3))
        today_msk = datetime.now(msk_tz)
        today_str = today_msk.strftime("%Y-%m-%d")

        today_forecast = [
            item for item in data["list"]
            if item["dt_txt"].startswith(today_str)
        ]

        if not today_forecast:
            return {"error": "Прогноз недоступен"}

        temps = [item["main"]["temp"] for item in today_forecast]
        avg_temp = round(sum(temps) / len(temps))
        min_temp = round(min(temps))
        max_temp = round(max(temps))

        max_rain_chance = 0
        for item in today_forecast:
            pop = item.get("pop", 0)
            rain_chance = round(pop * 100)
            if rain_chance > max_rain_chance:
                max_rain_chance = rain_chance

        descriptions = [item["weather"][0]["description"] for item in today_forecast]
        most_common_description = max(set(descriptions), key=descriptions.count)

        return {
            "city": CITY_NAMES_RU.get(CITY, CITY),
            "date": today_msk.strftime("%d.%m.%Y"),
            "weekday": WEEKDAYS_RU.get(today_msk.strftime("%A"), today_msk.strftime("%A")),
            "min_temp": min_temp,
            "max_temp": max_temp,
            "avg_temp": avg_temp,
            "description": most_common_description.capitalize(),
            "rain_chance": max_rain_chance
        }

    except Exception as e:
        print(f"Ошибка: {e}")
        return {"error": str(e)}

from PIL import Image, ImageDraw, ImageFont
import os
import platform
import random
import math


def get_font(size: int) -> ImageFont.FreeTypeFont:
    """Возвращает шрифт для текста (кириллица)."""
    system = platform.system()

    font_paths = []
    if system == "Windows":
        font_paths = [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
        ]
    elif system == "Linux":
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    elif system == "Darwin":
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",
        ]

    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue

    return ImageFont.load_default()


def get_emoji_font(size: int) -> ImageFont.FreeTypeFont:
    """Возвращает шрифт для эмодзи."""
    emoji_paths = [
        "C:/Windows/Fonts/seguiemj.ttf",
        "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
    ]
    for path in emoji_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()


def get_weather_info(description: str):
    """Возвращает тип погоды и эмодзи."""
    desc_lower = description.lower()

    if "ясно" in desc_lower or "clear" in desc_lower:
        return "sun", "☀️"
    elif "облачн" in desc_lower or "cloud" in desc_lower:
        if "перемен" in desc_lower:
            return "partly_cloudy", "⛅"
        return "cloudy", "☁️"
    elif "дожд" in desc_lower or "rain" in desc_lower or "морось" in desc_lower or "drizzle" in desc_lower:
        return "rain", "🌧"
    elif "снег" in desc_lower or "snow" in desc_lower:
        return "snow", "❄️"
    elif "гром" in desc_lower or "thunder" in desc_lower or "гроза" in desc_lower:
        return "thunder", "⛈"
    elif "туман" in desc_lower or "fog" in desc_lower:
        return "fog", "🌫"
    else:
        return "default", "🌡"


def draw_rain_drops(draw, width, height):
    """Рисует капли дождя на фоне."""
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        length = random.randint(10, 20)
        draw.line([(x, y), (x - 3, y + length)], fill='#4A7BA8', width=2)


def draw_sun_rays(draw, width, height):
    """Рисует солнце с лучами."""
    cx, cy = width // 2, height // 3
    radius = 60

    draw.ellipse([(cx - radius, cy - radius), (cx + radius, cy + radius)], fill='#FFD54F', outline='#FFB300', width=3)

    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x1 = cx + int((radius + 10) * math.cos(rad))
        y1 = cy + int((radius + 10) * math.sin(rad))
        x2 = cx + int((radius + 25) * math.cos(rad))
        y2 = cy + int((radius + 25) * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill='#FFD54F', width=3)


def draw_clouds(draw, width, height):
    """Рисует облака на фоне."""
    for _ in range(3):
        x = random.randint(50, width - 150)
        y = random.randint(50, height // 2)
        draw.ellipse([(x, y), (x + 80, y + 40)], fill='#3A5A7A')
        draw.ellipse([(x + 30, y - 20), (x + 100, y + 30)], fill='#3A5A7A')
        draw.ellipse([(x + 60, y), (x + 140, y + 40)], fill='#3A5A7A')


def draw_snowflakes(draw, width, height):
    """Рисует снежинки."""
    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(3, 6)
        draw.ellipse([(x - size, y - size), (x + size, y + size)], fill='#B0BEC5')


def draw_centered_emoji_text(draw, y, emoji, text, text_font, emoji_font, fill, width):
    """Рисует эмодзи + текст по центру, измеряя ширину."""
    # Измеряем ширину текста
    text_bbox = draw.textbbox((0, 0), text, font=text_font)
    text_width = text_bbox[2] - text_bbox[0]

    # Примерная ширина эмодзи (размер шрифта + небольшой отступ)
    emoji_width = emoji_font.size + 5

    # Отступ между эмодзи и текстом
    gap = 15

    # Общая ширина композиции
    total_width = emoji_width + gap + text_width

    # Начальная позиция X (чтобы всё было по центру)
    start_x = (width - total_width) // 2

    # Рисуем эмодзи
    draw.text((start_x, y), emoji, fill=fill, font=emoji_font)

    # Рисуем текст справа от эмодзи
    draw.text((start_x + emoji_width + gap, y), text, fill=fill, font=text_font)


def create_weather_card(
        city: str,
        date: str,
        weekday: str,
        min_temp: int,
        max_temp: int,
        avg_temp: int,
        description: str,
        rain_chance: int,
        output_path: str = "weather_card.png"
) -> str:
    """Создаёт карточку погоды с динамичным фоном."""

    width = 600
    height = 950

    # === ЦВЕТОВАЯ ПАЛИТРА ===
    bg_color = '#1E3A5F'
    text_main = '#FFFFFF'
    text_sub = '#B0BEC5'
    temp_color = '#81D4FA'
    rain_color = '#FFB74D'
    box_bg = '#264A73'
    box_border = '#3A6B9F'

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Определяем тип погоды
    weather_type, emoji = get_weather_info(description)

    # === РИСУЕМ ДИНАМИЧНЫЙ ФОН ===
    if weather_type == "rain":
        draw_rain_drops(draw, width, height)
    elif weather_type == "sun":
        draw_sun_rays(draw, width, height)
    elif weather_type in ["cloudy", "partly_cloudy"]:
        draw_clouds(draw, width, height)
    elif weather_type == "snow":
        draw_snowflakes(draw, width, height)

    # Загружаем шрифты
    font_city = get_font(56)
    font_date = get_font(32)
    font_temp = get_font(64)
    font_temp_label = get_font(30)
    font_weather = get_font(36)
    font_emoji = get_emoji_font(40)
    font_rain = get_font(34)
    font_warning = get_font(28)
    font_warning_emoji = get_emoji_font(28)

    # === ГОРОД ===
    y = 100
    draw.text((width // 2, y), city, fill=text_main, font=font_city, anchor='mm')

    # === ДАТА ===
    y += 70
    weekday_capitalized = weekday.capitalize()
    date_text = f"{date}, {weekday_capitalized}"
    draw.text((width // 2, y), date_text, fill=text_sub, font=font_date, anchor='mm')

    # === ТЕМПЕРАТУРА ===
    y += 140
    temp_text = f"от {min_temp}° до {max_temp}°C"
    draw.text((width // 2, y), temp_text, fill=temp_color, font=font_temp, anchor='mm')

    # === СРЕДНЯЯ ТЕМПЕРАТУРА ===
    y += 90
    avg_text = f"Средняя: {avg_temp}°C"
    draw.text((width // 2, y), avg_text, fill=text_sub, font=font_temp_label, anchor='mm')

    # === БЛОК С ОПИСАНИЕМ ПОГОДЫ ===
    y += 120
    box_top = y
    box_height = 140
    box_left = 50
    box_right = width - 50

    draw.rounded_rectangle(
        [(box_left, box_top), (box_right, box_top + box_height)],
        radius=20,
        fill=box_bg
    )

    # Рисуем эмодзи + текст по центру (с измерением ширины!)
    desc_y = box_top + box_height // 2 - 20
    draw_centered_emoji_text(
        draw, desc_y, emoji, description.capitalize(),
        font_weather, font_emoji, text_main, width
    )

    # === ШАНС ДОЖДЯ ===
    y = box_top + box_height + 60
    rain_text = f"Шанс дождя: {rain_chance}%"
    draw.text((width // 2, y), rain_text, fill=rain_color, font=font_rain, anchor='mm')

    # === ПРЕДУПРЕЖДЕНИЕ С ЭМОДЗИ ===
    y += 50

    if rain_chance >= 80:
        warning_emoji = "☂️"
        warning_lines = ["Скорее всего, будет дождь.", "Возьми зонт!"]
    elif rain_chance >= 50:
        warning_emoji = "☂️"
        warning_lines = ["Возможен дождь.", "Зонт не помешает."]
    elif rain_chance >= 20:
        warning_emoji = "☁️"
        warning_lines = ["Небольшая вероятность дождя."]
    else:
        warning_emoji = "☀️"
        warning_lines = ["Дождя не ожидается."]

    # Рисуем эмодзи по центру
    draw.text((width // 2, y), warning_emoji, fill=text_sub, font=font_warning_emoji, anchor='mm')

    # Рисуем текст предупреждения по центру
    y += 35
    for line in warning_lines:
        draw.text((width // 2, y), line, fill=text_sub, font=font_warning, anchor='mm')
        y += 35

    # === ДЕКОРАТИВНАЯ ЛИНИЯ ===
    line_y = height - 80
    draw.line(
        [(width // 4, line_y), (3 * width // 4, line_y)],
        fill=box_border,
        width=2
    )

    img.save(output_path, 'PNG', quality=95)
    print(f"✅ Карточка сохранена: {output_path}")
    return output_path

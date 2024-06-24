from database import add_user_city
import requests

OPENCAGE_API_KEY = '56caf74ae9114f5387cbc690d7dd81c0'


import aiohttp

async def determine_city_from_coordinates(latitude, longitude):
    try:
        url = f'https://api.opencagedata.com/geocode/v1/json?key={OPENCAGE_API_KEY}&q={latitude}+{longitude}&pretty=1&language=ru'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                json_data = await response.json()
                city = json_data.get('results', [{}])[0].get('components', {}).get('city', 'неизвестно')
                return city
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе данных: {e}")
        return "неизвестно"


from telegram import Update
from telegram.ext import ContextTypes


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    location = update.message.location
    latitude, longitude = location.latitude, location.longitude
    city = await determine_city_from_coordinates(latitude, longitude)
    city_added = await add_user_city(user_id, city)

    if city_added:
        await update.message.reply_text(f"Ваш город определен как {city}")
    else:
        await update.message.reply_text(f"Город {city} не найден в списке допустимых городов.")

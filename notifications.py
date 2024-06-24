import requests
from database import get_user_cities, get_northern_lights_data, get_user_threshold
import requests
from datetime import datetime, timedelta


async def send_notification(context):
    user_cities = get_user_cities()
    data = get_northern_lights_data()
    forecast_time = get_forecast_time()

    for user_id, city in user_cities:
        threshold = get_user_threshold(user_id)
        probability = get_probability_for_city(data, city)
        if probability is not None and probability >= threshold:
            message = f"В городе {city} ожидается наблюдение северного сияния с вероятностью {probability}%\n" \
                      f"время возможного наблюдения: {forecast_time}"
            await context.bot.send_message(chat_id=user_id, text=message)
    print("send_notification completed")

"""
async def send_mess(context):
    user_id = 828359541
    message = "Привет, Денис, как дела?"
    await context.bot.send_message(chat_id=user_id, text=message)
"""

def get_forecast_time():
    json_url = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
    try:
        response = requests.get(json_url)
        response.raise_for_status()
        json_data = response.json()
        forecast_time = json_data.get("Forecast Time", "неизвестно")

        if forecast_time != "неизвестно":
            # Преобразуем время в нужный формат
            dt = datetime.strptime(forecast_time, "%Y-%m-%dT%H:%M:%SZ")
            dt = dt + timedelta(hours=5)
            formatted_time = dt.strftime("%d.%m.%Y %H:%M")
            return formatted_time
        else:
            return "неизвестно"
    except requests.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
        return "неизвестно"



def get_probability_for_city(data, city):
    for city_name, probability in data:
        if city_name == city:
            return probability
    return None

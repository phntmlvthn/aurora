import operator

import aiosqlite
import telegram.ext as tg
from database import add_user_city, delete_user_cities, get_user_cities_for_user, get_northern_lights_data, \
    set_user_threshold
from notifications import get_forecast_time


async def start(update, context):
    bot_description = (
        "Привет! Я бот, который оповещает о вероятном северном сиянии в вашем городе.\n\n"
        "Доступные команды:\n"
        "/add *название города* - добавить город для наблюдения\n"
        "/mycities - отобразить все города, которые я добавил\n"
        "/deletecities - удалить все мои добавленные города\n"
        "/showcities - отобразить города России, в которых ожидается северное сияние в ближайшее время\n"
        "/threshold - установить минимальный порог вероятности наблюдения сияния\n\n"
        "Также вы можете прислать мне вашу геолокацию, и я сам определю и запишу ваш город\n"
    )
    await update.message.reply_text(bot_description)
    await update.message.reply_text(
        'Все данные о вероятностях наблюдения получены с данного [сервиса](https://services.swpc.noaa.gov/json/ovation_aurora_latest.json)\n'
        f'Ближайшее северное сияние спрогнозированно на {get_forecast_time()}',
        parse_mode='Markdown', disable_web_page_preview=True)


async def add_city(update, context):
    if len(context.args) == 0:
        await update.message.reply_text("Чтобы добавить город, используйте команду /add вместе с названием города.")
    else:
        city = ' '.join(context.args).capitalize()
        city_added = await add_user_city(update.message.chat_id, city)

        if city_added:
            await update.message.reply_text(f"Город {city} добавлен!")
        else:
            await update.message.reply_text(f"Город {city} не найден в списке допустимых городов.")


async def delete_cities(update, context):
    user_id = update.message.chat_id
    delete_user_cities(user_id)
    await update.message.reply_text("Все добавленные вами города были удалены.")


async def my_cities(update, context):
    user_id = update.message.chat_id
    user_cities = get_user_cities_for_user(user_id)
    if user_cities:
        message = "Ваши сохраненные города:\n" + "\n".join(user_cities)
    else:
        message = "Вы еще не добавили ни одного города."
    await update.message.reply_text(message)



async def my_cities(update, context):
    user_id = update.message.chat_id
    user_cities = get_user_cities_for_user(user_id)
    if user_cities:
        message = "Ваши сохраненные города:\n" + "\n".join(user_cities)
    else:
        message = "Вы еще не добавили ни одного города."
    await update.message.reply_text(message)

async def show_cities(update, context):
    data = get_northern_lights_data()
    message = "Города в которых ожидается северное сияние в ближайшее время с некоторой вероятностью:\n"
    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)

    for city, probability in sorted_data:
        if probability is not None and probability >= 1:
            message += f"{city}: {probability}%\n"

    await update.message.reply_text(message)

async def handle_text(update, context):
    text = update.message.text
    await update.message.reply_text(f"Вы отправили текст: {text}")


async def set_threshold(update, context):
    user_id = update.message.chat_id
    if len(context.args) == 0:
        await update.message.reply_text("Укажите порог в процентах после команды /threshold")
    else:
        try:
            threshold = int(context.args[0])
            if threshold < 1 or threshold > 100:
                raise ValueError
            await set_user_threshold(user_id, threshold)
            await update.message.reply_text(f"Порог вероятности наблюдения сияния установлен на {threshold}%")
        except ValueError:
            await update.message.reply_text("Порог должен быть целым числом от 1 до 100")



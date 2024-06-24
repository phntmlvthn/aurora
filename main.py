import telegram.ext as tg
from commands import add_city, delete_cities, handle_text, my_cities, show_cities, start, set_threshold
from database import initialize_database
from location import handle_location
from notifications import send_notification
from parsing import async_process_aurora_data
#from notifications import  send_mess


def main():
    application = tg.ApplicationBuilder().token("6008867290:AAHKv1-SQ9TLkHwe6LjzmIH9c_MqyZbgpAQ").build()
    initialize_database()
    start_handler = tg.CommandHandler("start", start)
    add_city_handler = tg.CommandHandler("add", add_city)
    show_cities_handler = tg.CommandHandler("showcities", show_cities)
    my_cities_handler = tg.CommandHandler("mycities", my_cities)
    delete_cities_handler = tg.CommandHandler("deletecities", delete_cities)

    text_handler = tg.MessageHandler(tg.filters.TEXT & ~tg.filters.COMMAND, handle_text)
    location_handler = tg.MessageHandler(tg.filters.LOCATION, handle_location)

    threshold_handler = tg.CommandHandler('threshold', set_threshold)
    application.add_handler(threshold_handler)

    application.add_handler(start_handler)
    application.add_handler(add_city_handler)
    application.add_handler(show_cities_handler)
    application.add_handler(my_cities_handler)
    application.add_handler(delete_cities_handler)
    application.add_handler(text_handler)
    application.add_handler(location_handler)

    job_queue = application.job_queue
    #job_queue.run_once(send_mess, 0)


    job_queue.run_once(async_process_aurora_data, 0)
    job_queue.run_repeating(async_process_aurora_data, interval=300)

    job_queue.run_once(send_notification, 10)
    job_queue.run_repeating(send_notification, interval=300)

    application.run_polling()


if __name__ == '__main__':
    main()

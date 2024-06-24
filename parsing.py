import requests
import json
import sqlite3
from collections import defaultdict
import asyncio


def sync_process_aurora_data(context):
    process_aurora_data()


async def async_process_aurora_data(context):
    await asyncio.to_thread(sync_process_aurora_data, context)


def process_aurora_data(context=None):
    with open('сities.json', 'r', encoding='utf-8') as f:
        cities = defaultdict(list)
        for city, coords in json.load(f).items():
            cities[tuple(coords)].append(city)

    def get_aurora_data():
        url = "https://services.swpc.noaa.gov/json/ovation_aurora_latest.json"
        response = requests.get(url)
        data = json.loads(response.text)
        return data["coordinates"]

    conn = sqlite3.connect('mydatabase.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS aurora_data
                 (longitude INTEGER, latitude INTEGER, probability INTEGER, city TEXT, UNIQUE(longitude, latitude, city))''')

    c.execute("DELETE FROM aurora_data")

    aurora_data = get_aurora_data()

    for lon, lat, prob in aurora_data:
        if prob > 0:
            city_names = cities.get((lon, lat), [])
            for city_name in city_names:
                try:
                    c.execute("INSERT INTO aurora_data VALUES (?, ?, ?, ?)", (lon, lat, prob, city_name))
                except sqlite3.IntegrityError:
                    pass
    print("parsing completed")
    conn.commit()
    conn.close()

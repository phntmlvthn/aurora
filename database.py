import sqlite3
import json
import aiofiles
import aiosqlite

def initialize_database():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_cities (
            user_id INTEGER,
            city TEXT,
            PRIMARY KEY (user_id, city)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_threshold (
            user_id INTEGER PRIMARY KEY,
            threshold INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

async def set_user_threshold(user_id, threshold):
    async with aiosqlite.connect('mydatabase.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''
                INSERT OR REPLACE INTO user_threshold (user_id, threshold)
                VALUES (?, ?)
            ''', (user_id, threshold))
            await conn.commit()

def get_user_threshold(user_id):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT threshold FROM user_threshold WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 1

async def load_city_data():
    async with aiofiles.open('сities.json', 'r', encoding='utf-8') as f:
        data = await f.read()
    return json.loads(data)
async def add_user_city(user_id, city):
    city_data = await load_city_data()
    if city not in city_data:
        return False
    async with aiosqlite.connect('mydatabase.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('INSERT OR IGNORE INTO user_cities (user_id, city) VALUES (?, ?)', (user_id, city))
            await conn.commit()
    return True


def delete_user_cities(user_id):
    conn = sqlite3.connect('mydatabase.db')
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_cities WHERE user_id = ?', (user_id,))
        conn.commit()
    finally:
        conn.close()


def get_user_cities():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, city FROM user_cities')
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_user_cities_for_user(user_id):
    conn = sqlite3.connect('mydatabase.db')
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT city FROM user_cities WHERE user_id = ?', (user_id,))
        user_cities = [row[0] for row in cursor.fetchall()]
        return user_cities
    finally:
        conn.close()


def get_northern_lights_data():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute('SELECT city, probability FROM aurora_data')
    rows = cursor.fetchall()
    conn.close()
    return rows

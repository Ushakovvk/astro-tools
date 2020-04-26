from instabot import Bot
import time
import sqlite3
import json
import os
from tqdm import tqdm

# Загружаем список подписчиков астрологов
with open('astro_followers.txt', 'r') as f:
    astro_followers = json.load(f)

#list_astro_followers = []
#for astro, foll in astro_followers.items():
#    list_astro_followers.extend(foll)
#list_astro_followers = list(set(list_astro_followers))
list_astro_followers = astro_followers['690988666'][1500:]

bd_path = 'followers_info.bd'
conn = sqlite3.connect(bd_path)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE if not exists follower_info ( 
                username TEXT PRIMARY KEY,
                full_name TEXT,
                is_private INT,
                media_count INT,
                follower_count INT,
                following_count INT,
                biography TEXT,
                category TEXT,
                is_business INT
                )""")
cursor.execute("""CREATE TABLE if not exists following (user_id INT PRIMARY KEY, count INT DEFAULT 1)""")

bot = Bot()
bot.login(username='', password='')

for user_id in tqdm(list_astro_followers):
        username = bot.get_username_from_user_id(user_id)
        # Проверка на наличие в базе
        cursor.execute("SELECT * FROM follower_info WHERE username=?", (username,))
        if not cursor.fetchall():
            with conn:
                user_info = bot.get_user_info(username, use_cache=False)
                print(username)
                if user_info:

                    full_name = user_info['full_name']
                    is_private = user_info['is_private']
                    media_count = user_info['media_count']
                    follower_count = user_info['follower_count']
                    following_count = user_info['following_count']
                    biography = user_info['biography']
                    is_business = user_info['is_business']
                    if is_business:
                        category = user_info['category']
                    else:
                        category = ''
                    cursor.execute('INSERT INTO follower_info VALUES (?,?,?,?,?,?,?,?,?)',(username, full_name, is_private, 
                                                                media_count, follower_count, following_count, biography, category, is_business))
                    if (following_count <= 2000) and (not is_private):
                        following = bot.get_user_following(username)
                        cursor.executemany('INSERT INTO following(user_id) VALUES (?) ON CONFLICT(user_id) DO UPDATE SET count=count+1', 
                                        [(f,) for f in following])
            #time.sleep(3)
            os.system('cls')
conn.close()

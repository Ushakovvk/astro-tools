from instabot import Bot
import time
import sqlite3
import json
import os

def collect(bd_path, astrologes, period):
    time_now = time.strftime('%Y-%m-%d %H:%M')
    conn = sqlite3.connect(bd_path)
    cursor = conn.cursor()
    sql = "INSERT INTO stats VALUES (?,?,?,?,?,?,?)"
    bot = Bot()
    bot.login(username='', password='')
    for username in astrologes:
        count_followers = bot.get_user_info(username, use_cache=False)['follower_count']
        user_id = bot.get_user_id_from_username(username)
        medias = bot.get_user_medias(user_id, filtration=False)
        if not medias:
            print(f'{time_now}-{username}-False')
            conn.close()
            return False
        for media_id in medias:
            media_id = int(media_id.split('_')[0])
            media_link = bot.get_link_from_media_id(media_id)
            media_info = bot.get_media_info(media_id)[0]
            like_count = media_info['like_count']
            taken_at = time.strftime('%Y-%m-%d %H:%M', time.localtime(media_info['taken_at']))
            cursor.execute(sql, (time_now, media_id, media_link, taken_at,
                                    like_count, username, count_followers))
            conn.commit()
            time.sleep(3)  # 3 Секунды между постами
        time.sleep(10)  # 10 секунд между пользователями
    conn.close()
    return True

bd_path = 'astro_history.bd'
conn = sqlite3.connect(bd_path)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE if not exists stats (time TEXT, 
                media_id INTEGER,
                media_link TEXT,
                taken_at TEXT, 
                like_count INTEGER, 
                owner TEXT, 
                count_followers INTEGER)""")
conn.close()

astrologes = ['Astrolog_anisimova', 'Mylablife', 'Astrokoza', 'Chukreeva_zvezda', 'Katrin.dia',
'Innashakti', 'Lubimova.astrolog', 'Alexandrova_astro', 'elena_blinovskaya']
period = 30  # Минуты
print('Start...')
try:
    while True:
        t1 = time.time()
        collect(bd_path, astrologes, period)
        dt = period * 60 - (time.time() - t1)
        time.sleep(dt)
except KeyboardInterrupt:
    print('Exit...')
    conn.close()


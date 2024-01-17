import json

import psycopg
import datetime


class Database:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        self.conn = psycopg.connect(
            dbname='default_db',
            user='gen_user',
            password='Alisa220!',
            host='109.172.90.131',
            port=5432
        )

    def execute(self, query, *args, commit=True):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            if commit:
                self.conn.commit()

    def fetch_all(self, query, *args):
        with self.conn.cursor() as cursor:
            cursor.execute(query, args)
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def fetch_one(self, query, *args):
        with self.conn.cursor() as cursor:
            cursor.execute(query, args)
            columns = [desc[0] for desc in cursor.description]
            result = cursor.fetchone()
            return dict(zip(columns, result)) if result else None


def check_and_insert_user(telegram_id, user_info):
    db = Database()
    # Проверяем, существует ли пользователь с указанным telegram_id
    try:
        user_query = "SELECT * FROM vpn_bot.users WHERE telegram_id = %s;"
        existing_user = db.fetch_one(user_query, telegram_id)
    except Exception as e:
        print(e)
        return

    if existing_user:
        return True

    # Если пользователь не существует, добавляем его
    insert_user_query = f"""
        INSERT INTO vpn_bot.users (telegram_id, user_info, reg_time)
        VALUES ('{telegram_id}', '{json.dumps(user_info)}', '{datetime.datetime.now()}');
    """
    try:
        db.execute(insert_user_query)
        return False
    except Exception as e:
        print(e)


def get_user_info(telegram_id):
    db = Database()
    try:
        user_query = "SELECT * FROM vpn_bot.us_keys WHERE telegram_id = %s;"
        data = db.fetch_one(user_query, telegram_id)
        return data
    except Exception as e:
        print(e)
        return None


def get_all_user_info():
    db = Database()
    try:
        user_query = '''
        SELECT 
            telegram_id,  
            key_id,
            used_bytes,
            data_limit
        FROM vpn_bot.us_keys;
        '''
        data = db.fetch_all(user_query)
        return data
    except Exception as e:
        print(e)
        return None

import requests
import sqlite3
import random
import string
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


class MessageSender:
    API_URL = 'https://api.exolve.ru/messaging/v1/SendSMS'
    CODE_EXPIRY_MINUTES = 2 # Время жизни кода в минутах
    # Создаем планировщик
    scheduler = BackgroundScheduler()
    scheduler.start()

    def __init__(self, api_key, from_number, path2database):
        self.api_key = api_key
        self.from_number = from_number
        self.path2database = path2database

    def _generate_unique_code(self):
        """Генерация уникального 4-значного кода."""
        conn = sqlite3.connect(self.path2database)
        cursor = conn.cursor()
        
        while True:
            code = ''.join(random.choices(string.digits, k=4))
            cursor.execute('SELECT 1 FROM temp_auth_codes WHERE code = ?', (code,))
            if cursor.fetchone() is None:
                break

        conn.close()
        return code
    
    def _create_table(self):
        """Создание таблицы для хранения временных кодов."""
        conn = sqlite3.connect(self.path2database)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temp_auth_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                destination TEXT,
                expiry_time DATETIME
            )
        ''')
        conn.commit()
        conn.close()


    def _store_code_in_db(self, code, destination):
        """Сохранение кода в базе данных."""
        expiry_time = datetime.now() + timedelta(minutes=self.CODE_EXPIRY_MINUTES)
        conn = sqlite3.connect(self.path2database)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO temp_auth_codes (code, destination, expiry_time)
            VALUES (?, ?, ?)
        ''', (code, destination, expiry_time))
        conn.commit()
        conn.close()


    def _send_sms_via_api(self, destination, text):
        """Отправка SMS через API."""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'number': self.from_number,
            'destination': destination,
            'text': text
        }

        response = requests.post(self.API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            print(f'SMS sent successfully to {destination}')
        else:
            print(f'Failed to send SMS to {destination}: {response.status_code}, {response.text}')



    def _remove_code_from_db(self, code):
        """Удаление определенного кода из базы данных."""
        conn = sqlite3.connect(self.path2database)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM temp_auth_codes WHERE code = ?', (code,))
        conn.commit()
        conn.close()
        print(f'Removed code {code} from database')


    def _schedule_code_removal(self, code):
        """Запланировать удаление кода через определенное время."""
        self.scheduler.add_job(
            func=self._remove_code_from_db,
            trigger='date',
            run_date=datetime.now() + timedelta(minutes=self.CODE_EXPIRY_MINUTES),
            args=[code]
        )


    def send_auth_code(self, destination):
        """Отправка уникального кода для регистрации пользователя."""
        self._create_table()
        code = self._generate_unique_code()
        self._store_code_in_db(code, destination)
        self._send_sms_via_api(destination, text=f'Your verification code is {code}')
        self._schedule_code_removal(code)
    
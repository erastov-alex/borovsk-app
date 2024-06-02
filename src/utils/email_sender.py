import sqlite3
import random
import string
from datetime import datetime, timedelta

from config import REAL_DB_PATH

from flask_mail import Message, Mail


class EmailSender:
    CODE_EXPIRY_MINUTES = 2 # Время жизни кода в минутах

    # scheduler = BackgroundScheduler()
    # scheduler.start()

    def __init__(self,mail, path2database):
        self.mail = mail
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


    def _remove_code_from_db(self, code):
        """Удаление определенного кода из базы данных."""
        conn = sqlite3.connect(self.path2database)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM temp_auth_codes WHERE code = ?', (code,))
        conn.commit()
        conn.close()
        print(f'Removed code {code} from database')


    def _send_email_via_stmp(self, to_mail, verification_code):
        # Формирование письма
        msg = Message("Подтверждение Регистрации", recipients=[to_mail])
        # Текстовое содержимое
        msg.body  = f"""\
        Привет!
        Спасибо за регистрацию.
        Ваш проверочный код: {verification_code}
        Пожалуйста, используйте его для завершения регистрации.
        """

        # HTML-содержимое
        msg.html = f"""\
        <html>
        <head>
            <style>
                .container {{
                    width: 90%;
                    margin: auto;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    background-color: #f9f9f9;
                    border: 1px solid #ececec;
                    padding: 20px;
                    border-radius: 8px;
                }}
                h1 {{
                    color: #333;
                }}
                p {{
                    color: #666;
                    font-size: 14px;
                }}
                .code {{
                    font-size: 24px;
                    color: #2a7ae2;
                    font-weight: bold;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Подтверждение Регистрации</h1>
                <p>Спасибо за регистрацию. Ваш проверочный код:</p>
                <div class="code">{verification_code}</div>
                <p>Пожалуйста, используйте его для завершения регистрации.</p>
            </div>
        </body>
        </html>
        """
        
        try:
            self.mail.send(msg)
            print("Success!")
            return "200"
        except Exception as e:
            print(f"Error - {e}")
            return f"Error - {e}"
            

    def send_auth_code_email(self, destination):
        self._create_table()
        code = self._generate_unique_code()
        self._store_code_in_db(code, destination)
        sended = self._send_email_via_stmp(destination, code)
        # self._schedule_code_removal(code)
        return sended


def init_mail(app):
    mail = Mail(app)
    return mail

def init_sender(mail):
    sender = EmailSender(mail, REAL_DB_PATH)
    return sender
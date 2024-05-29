import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sqlite3
import random
import string
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from config import MAIL, MAIL_PASSWORD, REAL_DB_PATH

class EmailSender:
    CODE_EXPIRY_MINUTES = 2 # Время жизни кода в минутах

    scheduler = BackgroundScheduler()
    scheduler.start()

    def __init__(self, from_mail, mail_password, path2database):
        self.from_mail = from_mail
        self.mail_password = mail_password
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


    def _schedule_code_removal(self, code):
        """Запланировать удаление кода через определенное время."""
        self.scheduler.add_job(
            func=self._remove_code_from_db,
            trigger='date',
            run_date=datetime.now() + timedelta(minutes=self.CODE_EXPIRY_MINUTES),
            args=[code]
        )


    def _send_email_via_stmp(self, to_mail, verification_code):
        # Настройка почтового сервера и учетных данных
        smtp_server = 'smtp.yandex.ru'
        smtp_port = 465
        
        # Формирование письма
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Подтверждение Регистрации'
        msg['From'] = self.from_mail
        msg['To'] = to_mail

        # Текстовое содержимое
        text_content = f"""\
        Привет!
        Спасибо за регистрацию.
        Ваш проверочный код: {verification_code}
        Пожалуйста, используйте его для завершения регистрации.
        """

        # HTML-содержимое
        html_content = f"""\
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

        # Присоединение текстового и HTML-содержимого к сообщению
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Отправка письма
        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(self.from_mail, self.mail_password)
                server.sendmail(self.from_mail, to_mail, msg.as_string())
            print("Письмо отправлено успешно!")
        except Exception as e:
            print(f"Ошибка при отправке письма: {e}")


    def send_auth_code_email(self, destination):
        self._create_table()
        code = self._generate_unique_code()
        self._store_code_in_db(code, destination)
        self._send_email_via_stmp(destination, code)
        self._schedule_code_removal(code)


sender = EmailSender(MAIL, MAIL_PASSWORD, REAL_DB_PATH)

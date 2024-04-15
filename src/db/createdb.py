import sqlite3

# Создание или подключение к базе данных
conn = sqlite3.connect('database.db')

# Создание курсора
c = conn.cursor()

# Создание таблицы Users
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT,
             password TEXT,
             email TEXT)''')

# Создание таблицы bookings
c.execute('''CREATE TABLE IF NOT EXISTS bookings
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              start_date TEXT,
              end_date TEXT,
              house_id INTEGER,
              FOREIGN KEY(user_id) REFERENCES users(id))''')

# Закрытие соединения с базой данных
conn.close()
import sqlite3
import os

database_path = os.path.join("instance", "database2.db")

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Получение названий колонок
cursor.execute("PRAGMA table_info(users)")
columns = [info[1] for info in cursor.fetchall()]

# Получение данных из таблицы users
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
conn.close()

# Форматированный вывод
for row in rows:
    for col_name, value in zip(columns, row):
        print(f"{col_name} - {value}")
    print()  # Пустая строка между записями

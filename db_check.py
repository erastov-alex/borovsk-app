import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM users')  
rows = cursor.fetchall()
conn.close()

for row in rows:
    print(row)
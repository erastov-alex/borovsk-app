import sqlite3

conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT * FROM bookings')  
rows = cursor.fetchall()
conn.close()

for row in rows:
    print(row)
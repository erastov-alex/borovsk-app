import sqlite3

conn = sqlite3.connect('db_bookings.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT * FROM bookings')  
rows = cursor.fetchall()
conn.close()

for row in rows:
    print(row)
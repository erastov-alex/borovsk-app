import sqlite3
import os

database_path = os.path.join('instance', 'database2.db')

conn = sqlite3.connect(database_path)
cursor = conn.cursor()
cursor.execute('SELECT * FROM houses')  
rows = cursor.fetchall()
conn.close()

for row in rows:
    print(row)
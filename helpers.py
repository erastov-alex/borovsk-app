import sqlite3
from flask import g, session

# Функция для получения соединения с базой данных
def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# Функция для закрытия соединения с базой данных
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Функция для получения текущего пользователя
def get_current_user():
    user_id = session.get('user_id')
    if user_id is None:
        return None
    db = get_db_connection()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    return user

# Проверяем наличие бронирований для текущего пользователя
def has_bookings():
    user = get_current_user()
    if user is None:
        return False
    db = get_db_connection()
    bookings = db.execute('SELECT * FROM bookings WHERE user_id = ?', (user['id'],)).fetchall()
    return len(bookings) > 0

def get_users_bookings():
    user = get_current_user()
    if user is None:
        return False
    db = get_db_connection()
    bookings = db.execute('SELECT * FROM bookings WHERE user_id = ?', (user['id'],)).fetchall()
    return bookings

def get_booking_by_id(booking_id):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
    booking = c.fetchone()

    conn.close()

    if booking:
        return {
            'id': booking[0],
            'user_id': booking[1],
            'start_date': booking[2],
            'end_date': booking[3],
            'house_id': booking[4]
        }
    else:
        return None
    
def update_booking(booking_id, start_date, end_date, house_id):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("UPDATE bookings SET start_date = ?, end_date = ?, house_id = ? WHERE id = ?", (start_date, end_date, house_id, booking_id))

    conn.commit()
    conn.close()
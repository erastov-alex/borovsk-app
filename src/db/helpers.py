import sqlite3
from flask import g, session

def get_db_connection():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect('database.db')
        db.row_factory = sqlite3.Row
    return db

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
    with get_db_connection() as db:
        user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    return user

# Проверяем наличие бронирований для текущего пользователя
def has_bookings():
    user = get_current_user()
    if user is None:
        return False
    with get_db_connection() as db:
        bookings = db.execute('SELECT * FROM bookings WHERE user_id = ?', (user['id'],)).fetchall()
    return len(bookings) > 0

def get_users_bookings():
    user = get_current_user()
    if user is None:
        return False
    with get_db_connection() as db:
        bookings = db.execute('SELECT * FROM bookings WHERE user_id = ?', (user['id'],)).fetchall()
    return bookings


def get_booking_by_id(booking_id):
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
        booking = c.fetchone()

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
    query = "UPDATE bookings SET start_date = ?, end_date = ?, house_id = ? WHERE id = ?"
    values = (start_date, end_date, house_id, booking_id) 
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute(query, values)
        conn.commit()


def cancel_booking_by_id(booking_id):
    query = "DELETE FROM bookings WHERE id = ?"
    values = (booking_id,)  # Кортеж с одним значением
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute(query, values)
        conn.commit()

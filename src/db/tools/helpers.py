from flask import session as s
from db.models.database import sql_session 
from db.models.users import User
from db.models.bookings import Booking 
import hashlib

def create_user(username, email, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    new_user = User(username=username, email=email, password=hashed_password)
    session = sql_session()
    session.add(new_user)
    session.commit()
    session.close()


def get_current_user():
    user_id = s.get('user_id')
    if user_id is None:
        return None
    session = sql_session()
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    return user

def has_bookings():
    user = get_current_user()
    if user is None:
        return False
    return bool(user.bookings)

def get_users_bookings():
    user = get_current_user()
    if user is None:
        return None
    return user.bookings

def get_booking_by_id(booking_id):
    session = sql_session()
    booking = sql_session.query(Booking).filter_by(id=booking_id).first()
    session.close()
    return booking

def update_booking(booking_id, start_date, end_date, house_id):
    booking = get_booking_by_id(booking_id)
    if booking:
        session = sql_session()
        booking.start_date = start_date
        booking.end_date = end_date
        booking.house_id = house_id
        sql_session.commit()
        session.close()

def cancel_booking_by_id(booking_id):
    booking = get_booking_by_id(booking_id)
    if booking:
        session = sql_session()
        session.delete(booking)
        session.commit()
        session.close()
        
def close_db(exception=None):
    session = sql_session()
    session.close()
        
from flask import session as s
from db.models.database import Session 
from db.models.users import User
from db.models.bookings import Booking 
from sqlalchemy.orm import joinedload
import hashlib

def create_user(username, email, password):
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    new_user = User(username=username, email=email, password=hashed_password)
    with Session() as session:
        session.add(new_user)
        session.commit()

def add_booking(user_id, start_date, end_date, house_id):
    with Session() as session:
        booking = Booking(user_id=user_id, start_date=start_date, end_date=end_date, house_id=house_id)
        session.add(booking)
        session.commit()

def get_current_user():
    user_id = s.get('user_id')
    if user_id is None:
        return None
    with Session() as session:
        user = session.query(User).filter_by(id=user_id).first()
    return user

def get_user_by_username(username):
    with Session() as session:
        user = session.query(User).filter_by(username=username).first()
    return user


def has_bookings():
    user = get_current_user()
    if user is None:
        return False
    return bool(get_users_bookings())


def get_users_bookings():
    user = get_current_user()
    if user is None:
        return None
    with Session() as session: 
        user_with_bookings = session.query(User).options(joinedload(User.bookings)).filter_by(id=user.id).first()
        bookings = user_with_bookings.bookings
    return bookings


def get_booking_by_id(booking_id):
    with Session() as session: 
        booking = session.query(Booking).filter_by(id=booking_id).first()
    return booking


def update_booking(booking_id, start_date, end_date, house_id):
    with Session() as session:
        try:
            booking = session.query(Booking).filter_by(id=booking_id).first()
            if booking:
                booking.start_date = start_date
                booking.end_date = end_date
                booking.house_id = house_id
                session.commit()
        except Exception:
            print("ERROR")


def cancel_booking_by_id(booking_id):
    booking = get_booking_by_id(booking_id)
    if booking:
        with Session() as session: 
            session.delete(booking)
            session.commit()
        
def close_db(exception=None):
    session = Session()
    session.close()
        
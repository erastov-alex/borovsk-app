import os

from models.users import User
from models.bookings import Booking 
from models.houses import House
from flask import session as s
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from models import db

from datetime import datetime, timedelta


def create_user(username, email, password):
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()


def add_booking(user_id, start_date, end_date, house_id):
    booking = Booking(user_id=user_id, start_date=start_date, end_date=end_date, house_id=house_id)
    db.session.add(booking)
    db.session.commit()


def get_current_user():
    user_id = s.get('user_id')
    if user_id is None:
        return None
    user = User.query.filter_by(id=user_id).first()
    return user


def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user


def get_all_bookings():
    try:
        bookings = Booking.query.all()
        return bookings
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def has_bookings(current_user):
    return bool(get_users_bookings(current_user))


def get_users_bookings(current_user):
    user_with_bookings = User.query.options(joinedload(User.bookings)).filter_by(id=current_user.id).first()
    bookings = user_with_bookings.bookings
    return bookings


def get_booking_by_id(booking_id):
    booking = Booking.query.filter_by(id=booking_id).first()
    return booking


def update_booking(booking_id, start_date, end_date, house_id):
    try:
        booking = Booking.query.filter_by(id=booking_id).first()
        if booking:
            booking.start_date = start_date
            booking.end_date = end_date
            booking.house_id = house_id
            db.session.commit()
        return True
    except Exception:
        print("ERROR")
        return None


def cancel_booking_by_id(booking_id):
    booking = get_booking_by_id(booking_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()


def close_db(exception=None):
    db.session.close()


def get_all_photos(path):
    return os.listdir(path)

# in cache
# def get_all_houses():
#     try:
#         houses = House.query.all()
#         return houses
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
    
    
def get_all_users():
    try:
        users = User.query.all()
        return users
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def get_unavailable_dates(house_id):
    unavailable_dates = []
    bookings = Booking.query.filter_by(house_id=house_id).all()
    for booking in bookings:
        start_date = datetime.strptime(booking.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(booking.end_date, '%Y-%m-%d')
        while start_date <= end_date:
            unavailable_dates.append(start_date.strftime('%Y-%m-%d'))
            start_date += timedelta(days=1)
    return unavailable_dates

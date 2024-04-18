# import sys
# import os

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# from db.model import db_check


from models.database import create_db
from models.users import User
from models.bookings import Booking


def create_database(load_fake_data: bool = True):
    create_db()
    
create_database()
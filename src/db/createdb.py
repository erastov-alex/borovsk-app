from models.users import User
from models.bookings import Booking
from models.database import Base, engine
import os
DATABASE_NAME = 'database.sqlite'

def create_db():
    Base.metadata.create_all(engine)
    
    
def create_database(load_fake_data: bool = True):
    if not os.path.exists(DATABASE_NAME):
        create_db()

create_database()

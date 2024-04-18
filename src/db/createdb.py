from models.users import User
from models.bookings import Booking
from models.database import Base, engine


def create_db():
    Base.metadata.create_all(engine)
    
    
def create_database(load_fake_data: bool = True):
    create_db()
    
create_database()
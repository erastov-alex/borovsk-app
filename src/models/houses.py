from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from . import db

class House(db.Model):
    __tablename__ = 'houses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    floors = Column(String, nullable=False)
    persons = Column(Integer, nullable=False)
    beds = Column(Integer, nullable=False)
    rooms = Column(Integer, nullable=False)
    bbq = Column(Boolean, nullable=False)
    water = Column(Boolean, nullable=False)
    photos_dir = Column(String, nullable=False)
    small_disc = Column(String, nullable=False)
    big_disc = Column(String, nullable=False)
    bookings = relationship("Booking", back_populates="house")
    
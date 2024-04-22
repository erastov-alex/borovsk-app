from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from . import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    house_id = Column(Integer, ForeignKey('houses.id'))  # Внешний ключ к таблице House
    house = relationship("House", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
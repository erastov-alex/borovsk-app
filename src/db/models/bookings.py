from sqlalchemy import Column, Integer, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from .database import Base

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    house_id = Column(Integer, nullable=False)
    user = relationship("User", back_populates="bookings")
    
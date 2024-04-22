from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import hashlib
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    bookings = relationship("Booking", back_populates="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
import hashlib
from . import db

from flask_login import UserMixin


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    bookings = relationship("Booking", back_populates="user")
    name = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    second_name = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    total_bonuses = Column(String(50), nullable=True)
    interested = Column(Boolean, nullable=True)

    def __init__(self, username, email, password, name, interested):
        self.username = username
        self.email = email
        self.password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        self.name = name
        self.interested = interested

    def get_id(self):
        return self.id

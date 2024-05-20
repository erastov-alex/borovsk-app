from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
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
        self.set_password(password)  # Хешируем пароль при создании пользователя
        self.name = name
        self.interested = interested

    def set_password(self, password):
        """Хешируем пароль с использованием werkzeug.security."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверяем пароль с использованием werkzeug.security."""
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id
    
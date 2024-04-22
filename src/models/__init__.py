from flask_sqlalchemy import SQLAlchemy
# Импорт моделей, чтобы они были доступны в других частях приложения

db = SQLAlchemy()

from .houses import House
from .bookings import Booking
from .users import User

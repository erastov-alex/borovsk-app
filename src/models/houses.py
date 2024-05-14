from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from . import db


class House(db.Model):
    __tablename__ = 'houses'
    
    """
    id: уникальный идентификатор дома (первичный ключ).
    name: название дома.
    floors: количество этажей в доме.
    persons: количество персон, которые могут разместиться в доме.
    beds: количество кроватей в доме.
    rooms: количество комнат в доме.
    bbq: флаг, указывающий на наличие барбекю (True/False).
    water: флаг, указывающий на наличие воды (True/False).
    photos_dir: директория с фотографиями дома.
    small_disc: описание дома (короткое).
    big_disc: описание дома (подробное).
    bookings: отношение с бронированиями (один ко многим).
    """

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    floors = Column(String, nullable=False)
    persons = Column(Integer, nullable=False)
    beds = Column(Integer, nullable=False)
    rooms = Column(Integer, nullable=False)
    bbq = Column(Boolean, nullable=False)
    water = Column(Boolean, nullable=False)
    main_photo = Column(String, nullable=False)
    photos_dir = Column(String, nullable=False)
    small_disc = Column(String, nullable=False)
    big_disc = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    bookings = relationship("Booking", back_populates="house")
    
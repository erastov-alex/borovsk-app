import os

from models.users import User
from models.bookings import Booking
from models.houses import House
from flask import session as s
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from models import db


def add_house(
    id, name, floors, persons, beds, rooms, bbq, water, photos_dir, small_disc, big_disc
):
    new_house = House(
        id=id,
        name=name,
        floors=floors,
        persons=persons,
        beds=beds,
        rooms=rooms,
        bbq=bbq,
        water=water,
        photos_dir=photos_dir,
        small_disc=small_disc,
        big_disc=big_disc,
    )
    db.session.add(new_house)
    db.session.commit()


name = "Уютный"
floors = "Одноэтажный"
persons = 2
beds = 1
rooms = 2
bbq = False
water = True
photos_dir = "static/img/houses/house1"
small_disc = "Прекрасно подходит для романтического отдыха вдвоем. Уютная атмосфера и комфорт обеспечат незабываемый отдых."
big_disc = "Этот уютный одноэтажный домик под названием Уютный идеально подходит для романтического отдыха вдвоем. Он расположен в живописном уголке Подмосковья в Боровске и предлагает всё необходимое для комфортного и незабываемого пребывания. Дом оснащен двумя комнатами, в которых найдется место для отдыха и развлечений. Свежий воздух, удивительная природа и тишина сделают ваш отдых неповторимым. Приходите и наслаждайтесь временем в этом уникальном уголке природы!"

add_house(
    id, name, floors, persons, beds, rooms, bbq, water, photos_dir, small_disc, big_disc
)

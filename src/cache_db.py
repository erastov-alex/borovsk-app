from flask_caching import Cache
from models.database import Session 
from models.houses import House 

cache = Cache()
# cache.init_app(app)

@cache.memoize(timeout=3600)  # Кэшировать результаты на 1 час
def get_disc_from_database(house_id):
    with Session() as session: 
        house = session.query(House).filter_by(id=house_id).first()
        small_disc = house.small_disc
        big_disc = house.big_disc
    return big_disc, small_disc 

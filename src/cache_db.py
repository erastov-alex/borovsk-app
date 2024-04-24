from app import app
from models.houses import House
from flask_caching import Cache


cache = Cache()
cache.init_app(app)

@cache.memoize(timeout=3600)
def get_cache_house(house_id):
    house = House.query.filter_by(id=house_id).first()
    return house

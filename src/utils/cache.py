from models.houses import House

from flask_caching import Cache

from flask import flash

cache = Cache()


def init_cache(app):
    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})


def get_house_info(house_id):
    cache_key = f'product_info:{house_id}'
    house = cache.get(cache_key)
    if house is None:
        house = House.query.filter_by(id=house_id).first()
        cache.set(cache_key, house, timeout=300)
    return house


def get_all_houses():
    cache_key = 'all_houses'
    houses = cache.get(cache_key)
    if houses is None:
        houses = House.query.all()
        cache.set(cache_key, houses, timeout=300)
    return houses

def delete_cache():
    cache.clear()
    flash("Кэш удален", "success")
        
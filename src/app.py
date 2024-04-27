from flask import Flask
from models import db  # Импорт объекта базы данных
from config import *

from utils.cache import init_cache

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY  # подствавьте свой секретный ключ
# секретный ключ для хеширования данных сессии при авторизации

# Конфигурация базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

init_cache(app)
app.config['CACHE_TYPE'] = CACHE_TYPE


# Инициализация базы данных
db.init_app(app)

from login import login_manager
login_manager.init_app(app)


from routes.main_routes import main_bp
from routes.users_routes import users_bp
from routes.booking_routes import bookings_bp
from routes.admin_routes import admin_bp

app.register_blueprint(main_bp)
app.register_blueprint(users_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(admin_bp)

# Создание таблиц в базе данных
with app.app_context():
    db.create_all()
     
# Ваши маршруты и другие настройки Flask
if __name__ == '__main__':
    app.run(debug=True)
    
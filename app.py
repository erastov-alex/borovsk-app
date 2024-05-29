from flask import Flask
from flask_migrate import Migrate

from src.models import db  # Импорт объекта базы данных
from config import *
from src.api.api import Api
from src.api.routes import api

from src.utils.cache import init_cache

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

init_cache(app)
app.config["CACHE_TYPE"] = CACHE_TYPE

from flask_wtf import CSRFProtect

csrf = CSRFProtect(app)

# Инициализация базы данных
db.init_app(app)

from src.models.users import User
from src.models.bookings import Booking
from src.models.houses import House

migrate = Migrate(app, db)

jwt = Api(app, os.getenv("JWT_SECRET_KEY"))

from src.login import login_manager

login_manager.init_app(app)

from src.routes.main_routes import main_bp
from src.routes.users_routes import users_bp
from src.routes.booking_routes import bookings_bp
from src.routes.admin_routes import admin_bp

app.register_blueprint(main_bp)
app.register_blueprint(users_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api)

# Создание таблиц в базе данных
# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

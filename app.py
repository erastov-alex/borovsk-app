from flask import Flask
from flask_migrate import Migrate

from src.models import db  # Импорт объекта базы данных
from config import *
from src.api.api import Api
from src.api.routes import api

from src.utils.cache import init_cache

from flask_mail import Mail
from src.utils.email_sender import EmailSender

application = Flask(__name__, template_folder="src/templates", static_folder="src/static")

application.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

application.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

init_cache(application)
application.config["CACHE_TYPE"] = CACHE_TYPE

from flask_wtf import CSRFProtect

csrf = CSRFProtect(application)

# Инициализация базы данных
db.init_app(application)

from src.models.users import User
from src.models.bookings import Booking
from src.models.houses import House

migrate = Migrate(application, db)

jwt = Api(application, os.getenv("JWT_SECRET_KEY"))

from src.login import login_manager

login_manager.init_app(application)

from src.routes.main_routes import main_bp
from src.routes.users_routes import users_bp
from src.routes.booking_routes import bookings_bp
from src.routes.admin_routes import admin_bp


mail = Mail(application)
# Create an instance of EmailSender
application.config['MAIL_SERVER'] = SMTP_SERVER
application.config['MAIL_PORT'] = SMTP_PORT
application.config['MAIL_USE_SSL'] = True
application.config['MAIL_USERNAME'] = os.getenv("MAIL")  # введите свой адрес электронной почты здесь
application.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL")  # и здесь
application.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")  # введите пароль


application.register_blueprint(main_bp)
application.register_blueprint(users_bp, mail=mail)
application.register_blueprint(bookings_bp)
application.register_blueprint(admin_bp)
application.register_blueprint(api)


# Создание таблиц в базе данных
# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    application.run(debug=True)

from flask import Flask
from models import db  # Импорт объекта базы данных
from config import SECRET_KEY, DATABASE_PATH
from flask_login import LoginManager

from models.users import User

from main_routes import main_bp
from user_routes import users_bp
from booking_routes import bookings_bp
from admin_routes import admin_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY  # подствавьте свой секретный ключ
# секретный ключ для хеширования данных сессии при авторизации

# Конфигурация базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'simple'

app.register_blueprint(main_bp)
app.register_blueprint(users_bp)
app.register_blueprint(bookings_bp)
app.register_blueprint(admin_bp)

# Инициализация базы данных
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

# Устанавливаем пользовательское сообщение о входе
login_manager.login_message = "Мы почти на месте, осталось только войти в аккаунт!"

@login_manager.user_loader
def load_user(user_id):
# Закрытие соединения с базой данных после запроса
    return User.query.get(user_id)


# Создание таблиц в базе данных
with app.app_context():
    db.create_all()
    
# Ваши маршруты и другие настройки Flask
if __name__ == '__main__':
    app.run(debug=True)
    
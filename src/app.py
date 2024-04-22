from flask import Flask
from models import db  # Импорт объекта базы данных
from config import SECRET_KEY, DATABASE_PATH
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY  # подствавьте свой секретный ключ
# секретный ключ для хеширования данных сессии при авторизации

# Конфигурация базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'simple'

# Инициализация базы данных
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Создание таблиц в базе данных
with app.app_context():
    db.create_all()
    
# Ваши маршруты и другие настройки Flask
if __name__ == '__main__':
    from routes import *  # Импорт маршрутов
    app.run(debug=True)
    
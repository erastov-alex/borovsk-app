from flask_login import LoginManager

from models.users import User

login_manager = LoginManager()
login_manager.login_view = 'users.login'

# Устанавливаем пользовательское сообщение о входе
login_manager.login_message = "Мы почти на месте, осталось только войти в аккаунт!"

@login_manager.user_loader
def load_user(user_id):
# Закрытие соединения с базой данных после запроса
    return User.query.get(user_id)
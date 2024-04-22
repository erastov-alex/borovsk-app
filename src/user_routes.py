from flask import Blueprint, flash, render_template, redirect, url_for, request
from models.users import *  # Импорт моделей
from tools.helpers import *
import hashlib

from flask_login import login_user, logout_user, login_required

users_bp = Blueprint('users', __name__)


@users_bp.route('/logout')
@login_required
def logout():
    logout_user()  # Выход пользователя из сеанса с помощью Flask-Login
    return redirect(url_for('main.index'))


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        user = get_user_by_username(username)

        if user and user.password == hashed_password:
            login_user(user)  # Вход пользователя с помощью Flask-Login
            if username == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('main.index'))
        else:
            error = 'Неправильное имя пользователя или пароль'
    return render_template('login.html', error=error)


@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        intersted = request.form.get('intersted')
        form = RegistrationForm(username=username, email=email, password=password, confirm_password=confirm_password)
        if form.validate_on_submit():
            user = User(name=name, username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Registration successful!', 'success')  # Оповещение об успешной регистрации
            return redirect(url_for('main.index'))
        else:
            # Если форма не прошла валидацию, получаем ошибки для каждого поля
            errors = {field.name: field.errors for field in form if field.errors}
            flash('Registration failed. Please check the following fields:', 'danger')
            print(errors, 'danger')  # Передаем ошибки всплывающему уведомлению
    return render_template('register.html', form = form)

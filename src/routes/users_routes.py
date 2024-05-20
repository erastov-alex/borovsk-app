from flask import Blueprint, flash, render_template, redirect, url_for, request
from src.models.users import * 
from src.utils.helpers import *
from src.models.forms import *
import hashlib

from sqlalchemy.exc import IntegrityError

from flask_login import login_user, logout_user, login_required, current_user

users_bp = Blueprint("users", __name__)


@users_bp.route("/logout")
@login_required
def logout():
    logout_user()  # Выход пользователя из сеанса с помощью Flask-Login
    flash("Вы успешно вышли")
    return redirect(url_for("main.index"))


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        form = LoginForm(username=username, password=hashed_password)
        if form.validate_on_submit():
            user = get_user_by_username(username)
            if user and user.check_password(form.password.data):
                login_user(user)  # Вход пользователя с помощью Flask-Login
                flash("Вы успешно вошли")
                if username == "admin":
                    return redirect(url_for("admin.admin_dashboard"))
                return redirect(url_for("main.index"))
            else:
                flash("Неправильное имя пользователя или пароль", "danger")
    return render_template("users/login.html", error=error, form=form)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        interested = True if request.form.get("interested") else False
        form = RegistrationForm(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password,
        )
        if form.validate_on_submit():
            try:
                user = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    name=name,
                    interested=interested,
                )
                db.session.add(user)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()  # Откатываем транзакцию
                if "UNIQUE constraint failed: users.email" in str(e):
                    flash(
                        "Этот адрес электронной почты уже используется. Пожалуйста, выберите другой адрес.",
                        "danger",
                    )
                elif "UNIQUE constraint failed: users.username" in str(e):
                    flash(
                        "Этот логин уже занят. Пожалуйста, выберите другой логин.",
                        "danger",
                    )
                else:
                    flash(
                        "Произошла ошибка при регистрации. Пожалуйста, попробуйте еще раз.",
                        "danger",
                    )
                return render_template("users/register.html", form=form)
            login_user(user)
            flash(
                "Успешная регистрация!", "success"
            )  # Оповещение об успешной регистрации
            return redirect(url_for("users.user_panel"))
        else:
            # Если форма не прошла валидацию, получаем ошибки для каждого поля
            errors = {field.name: field.errors for field in form if field.errors}
            flash(
                "Регистрация не удалась. Пожалуйста, проверьте следующие поля:",
                "danger",
            )
            print(errors, "danger")  # Передаем ошибки всплывающему уведомлению
    return render_template("users/register.html", form=form)


@users_bp.route("/user_panel")
@login_required
def user_panel():
    # Если текущий пользователь администратор, перенаправляем на административную панель
    if current_user.username == "admin":
        return redirect(url_for("admin.admin_dashboard"))

    # Проверяем наличие бронирований для текущего пользователя
    has_bookings_var = has_bookings(current_user)
    user_bookings = False

    if has_bookings_var:
        user_bookings = get_users_bookings(current_user)

    return render_template(
        "users/user_panel.html",
        has_bookings=has_bookings_var,
        user_bookings=user_bookings,
        active_page="user_panel",
    )


@users_bp.route("/user_info", methods=["GET", "POST"])
@login_required
def user_info():
    form = InfoForm(
        username=current_user.username,
        email= current_user.email
        )
    if request.method == "POST":
        first_name = request.form.get("first_name")
        second_name = request.form.get("second_name")
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        phone = request.form.get("phone")
        form = InfoForm(
            username=username
            )
        if form.validate_on_submit():
            user = current_user
            user.first_name = first_name
            user.second_name = second_name
            user.name = name
            user.username = username
            user.email = email
            user.phone = phone
            db.session.commit() 
            flash("Изменения Сохранены!")
            return redirect(url_for("users.user_info")) 
        else:
            flash('Oops!')
    return render_template("users/user_info.html", active_page="user_info", form=form)


@users_bp.route("/user_settings")
@login_required
def user_settings():
    return render_template("users/user_settings.html", active_page="user_settings")

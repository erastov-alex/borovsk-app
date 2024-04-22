from app import app, login_manager
from flask import flash, render_template, redirect, url_for, request, session, jsonify
from models.users import *  # Импорт моделей
from tools.helpers import *
from cache_db import get_disc_from_database
import hashlib

from flask_login import login_user, logout_user, current_user, login_required


@login_manager.user_loader
def load_user(user_id):
# Закрытие соединения с базой данных после запроса
    return User.query.get(user_id)


@app.teardown_appcontext
def teardown_db(exception=None):
    close_db()


@app.route('/')
def index():
    show_toast = False
    if 'toast_shown' not in session:
        show_toast = True
        session['toast_shown'] = True
    else:
        show_toast = False

    return render_template('index.html', show_toast=show_toast, current_user=current_user)    


@app.route('/logout')
@login_required
def logout():
    logout_user()  # Выход пользователя из сеанса с помощью Flask-Login
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('index'))
        else:
            error = 'Неправильное имя пользователя или пароль'
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('index'))
        else:
            # Если форма не прошла валидацию, получаем ошибки для каждого поля
            errors = {field.name: field.errors for field in form if field.errors}
            flash('Registration failed. Please check the following fields:', 'danger')
            print(errors, 'danger')  # Передаем ошибки всплывающему уведомлению
    return render_template('register.html', form = form)


@app.route('/house_selection', methods=['GET', 'POST'])
@login_required
def house_selection():
    # Извлекаем house_id, start_date и end_date из параметров GET-запроса, если они есть
    house_id = request.args.get('house_id')

    return render_template('house_selection.html', house_id=house_id)


@app.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    house_id = request.args.get('house_id')
    return render_template('calendar.html', house_id=house_id, username=current_user.username)


@app.route('/booking_confirmation', methods=['GET', 'POST'])
@login_required
def booking_confirmation():
    if request.method == 'GET':
        # Если это GET запрос, просто отображаем страницу подтверждения бронирования
        username = session.get('username')
        house_id = request.args.get('house_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        return render_template('booking_confirmation.html', username=username, house_id=house_id, start_date=start_date, end_date=end_date)
    
    elif request.method == 'POST':
        # Если это POST запрос, обрабатываем данные бронирования
        user_id = current_user.id
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            house_id = request.form['house_id']
            add_booking(user_id=user_id, start_date=start_date, end_date=end_date, house_id=house_id)
            return jsonify({'message': 'Booking confirmed'}), 200
        else:
            return jsonify({'error': 'User not logged in'}), 401


@app.route('/user_panel')
@login_required
def user_panel():
    # Если текущий пользователь администратор, перенаправляем на административную панель
    if current_user.username == 'admin':
        return redirect(url_for('admin_dashboard'))

    # Проверяем наличие бронирований для текущего пользователя
    has_bookings_var = has_bookings(current_user)
    user_bookings = False
    
    if has_bookings_var:
        user_bookings = get_users_bookings(current_user)

    return render_template('user_panel.html', has_bookings=has_bookings_var, user_bookings = user_bookings, active_page = 'user_panel')


@app.route('/edit_start_date/<int:booking_id>/<int:house_id>/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
@login_required
def edit_start_date(booking_id, house_id, start_date, end_date):
    # Инициализируем переменную booking
    booking = get_booking_by_id(booking_id)
    
    if request.method == 'POST':
        # Обработка формы редактирования бронирования
        # Получаем данные из формы и обновляем бронирование в базе данных
        start_date_new = request.form.get('start_date_new')

        # Обновляем бронирование в базе данных
        update_booking(booking_id, start_date_new, end_date, house_id)

        # Получаем обновленные данные бронирования из базы данных
        booking = get_booking_by_id(booking_id)

        # Возвращаем шаблон модального окна с обновленными данными
        return render_template(
            'edit_booking.html', 
            booking=booking, 
            active_page = 'user_panel'
            )
    
    
@app.route('/edit_end_date/<int:booking_id>/<int:house_id>/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
@login_required
def edit_end_date(booking_id, house_id, start_date, end_date):
    # Инициализируем переменную booking
    booking = get_booking_by_id(booking_id)
    
    if request.method == 'POST':
        # Обработка формы редактирования бронирования
        # Получаем данные из формы и обновляем бронирование в базе данных
        end_date_new = request.form.get('end_date_new')

        # Обновляем бронирование в базе данных
        update_booking(booking_id, start_date, end_date_new, house_id)

        # Получаем обновленные данные бронирования из базы данных
        booking = get_booking_by_id(booking_id)

        # Возвращаем шаблон модального окна с обновленными данными
        return render_template('edit_booking.html', booking=booking, active_page = 'user_panel')


@app.route('/edit_booking/<int:booking_id>/<int:house_id>/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
@login_required
def edit_booking(booking_id, house_id, start_date, end_date):

    # Инициализируем переменную booking
    booking = get_booking_by_id(booking_id)
    
    # Если метод запроса GET, просто возвращаем шаблон модального окна
    return render_template(
        'edit_booking.html', 
        booking=booking,  
        active_page = 'user_panel'
        )


@app.route('/user_info')
@login_required
def user_info():
    return render_template('user_info.html', active_page='user_info')


@app.route('/user_settings')
@login_required
def user_settings():
    return render_template('user_settings.html', active_page='user_settings')


@app.route('/cancel_booking/<int:booking_id>')
@login_required
def cancel_booking(booking_id):
    # Обновляем бронирование в базе данных
    cancel_booking_by_id(booking_id)

    return redirect(url_for('user_panel'))


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.username != 'admin':
        return redirect(url_for('user_panel')) 
    
    bookings = get_all_bookings()
    
    return render_template('admin_dashboard.html', bookings=bookings)


@app.route('/house/<int:house_id>')
def house_details(house_id):
    # Получаем путь к папке с фотографиями для данного house_id
    photo_dir = f"static/img/houses/house{house_id}/"
    
    # Получаем список файлов в этой папке
    photos = get_all_photos(photo_dir)
    
    # Определяем количество фотографий
    num_of_photos = len(photos)
    
    big_disc, small_disc = get_disc_from_database(house_id)
        
    # Рендерим шаблон, передавая количество фотографий в контексте
    return render_template(
        'house_details.html', 
        house_id=house_id, 
        num_of_photos=num_of_photos, 
        big_disc=big_disc, 
        small_disc=small_disc
        )

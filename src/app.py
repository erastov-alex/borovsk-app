from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from db.models.database import Session
from db.models.users import User
from db.models.bookings import Booking 
from db.tools.helpers import *
from config import SECRET_KEY, DATABASE_NAME
import hashlib # библиотека для хеширования

app = Flask(__name__, template_folder='templates')
app.secret_key = SECRET_KEY  # подствавьте свой секретный ключ
# секретный ключ для хеширования данных сессии при авторизации

# Конфигурация базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Закрытие соединения с базой данных после запроса
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db()


@app.route('/')
def index():
    username = None
    show_toast = False
    if 'username' in session:
        username = session['username']
    # Проверяем, было ли уже показано сообщение в текущей сессии
        if 'toast_shown' not in session:
            show_toast = True
            session['toast_shown'] = True
        else:
            show_toast = False

    return render_template('index.html', username=username, show_toast=show_toast)    


@app.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    session.clear()
    # Перенаправление на главную страницу или страницу входа
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
            session['user_id'] = user.id
            session['username'] = username
            
            if username == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_panel'))

        else:
            error = 'Неправильное имя пользователя или пароль'
    return render_template('login_reg.html', error=error)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['regUsername']
        email = request.form['email']
        password = request.form['regPassword']
        confirm_password = request.form['confirmPassword']

        # Проверка, что пароли совпадают
        if password != confirm_password:
            return render_template('login_reg.html', error="Пароли не совпадают")

        # Создание пользователя
        create_user(username, email, password)
        # в случае успеха создаем сессию в которую записываем id пользователя
        user = get_user_by_username(username)
        session['user_id'] = user.id
        session['username'] = username
        # и делаем переадресацию пользователя на новую страницу -> в нашу адимнку
        return redirect(url_for('user_panel'))
        # return render_template('user_panel.html', username=username)

    return render_template('login_reg.html')



@app.route('/house_selection', methods=['GET', 'POST'])
def house_selection():
    username = None
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for('login'))

    # Извлекаем house_id, start_date и end_date из параметров GET-запроса, если они есть
    house_id = request.args.get('house_id')

    return render_template('house_selection.html', username=username, house_id=house_id)

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    username = None
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for('login'))
    house_id = request.args.get('house_id')
    return render_template('calendar.html', house_id=house_id, username=username)


@app.route('/booking_confirmation', methods=['GET', 'POST'])
def booking_confirmation():
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for('login'))
    if request.method == 'GET':
        # Если это GET запрос, просто отображаем страницу подтверждения бронирования
        username = session.get('username')
        house_id = request.args.get('house_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        return render_template('booking_confirmation.html', username=username, house_id=house_id, start_date=start_date, end_date=end_date)
    
    elif request.method == 'POST':
        # Если это POST запрос, обрабатываем данные бронирования
        user_id = session.get('user_id')
        if user_id:
            user = Session().query(User).filter_by(id=user_id).first()
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
def user_panel():
    # Проверяем, авторизован ли пользователь
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа
    if session['username'] == 'admin':
        return redirect(url_for('admin_dashboard'))

    # Получаем имя пользователя из сеанса
    username = session['username']

    # Проверяем наличие бронирований для текущего пользователя
    has_bookings_var = has_bookings()
    user_bookings = False
    
    if has_bookings_var:
        user_bookings = get_users_bookings()

    return render_template('user_panel.html', username=username, has_bookings=has_bookings_var, user_bookings = user_bookings, active_page = 'user_panel')

@app.route('/edit_start_date/<int:booking_id>/<int:house_id>/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
def edit_start_date(booking_id, house_id, start_date, end_date):
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа
    
    # Получаем имя пользователя из сеанса
    username = session['username']
    
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
        return render_template('edit_booking.html', booking=booking, username=username, active_page = 'user_panel')
    
@app.route('/edit_end_date/<int:booking_id>/<int:house_id>/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
def edit_end_date(booking_id, house_id, start_date, end_date):
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа
    
    # Получаем имя пользователя из сеанса
    username = session['username']
    
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
        return render_template('edit_booking.html', booking=booking, username=username, active_page = 'user_panel')


@app.route('/edit_booking/<int:booking_id>/<int:house_id>/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
def edit_booking(booking_id, house_id, start_date, end_date):
    # Проверяем, авторизован ли пользователь
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа
    
    # Получаем имя пользователя из сеанса
    username = session['username']
    
    # Инициализируем переменную booking
    booking = get_booking_by_id(booking_id)
    
    # Если метод запроса GET, просто возвращаем шаблон модального окна
    return render_template('edit_booking.html', booking=booking, username=username, active_page = 'user_panel')


@app.route('/user_info')
def user_info():
    # Проверяем, авторизован ли пользователь
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа

    # Получаем имя пользователя из сеанса
    username = session['username']
    return render_template('user_info.html', username=username, active_page='user_info')


@app.route('/user_settings')
def user_settings():
    # Проверяем, авторизован ли пользователь
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа

    # Получаем имя пользователя из сеанса
    username = session['username']
    return render_template('user_settings.html', username=username, active_page='user_settings')

@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    # Проверяем, авторизован ли пользователь
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа
    
    # # Получаем имя пользователя из сеанса
    # username = session['username']

    # Обновляем бронирование в базе данных
    cancel_booking_by_id(booking_id)

    return redirect(url_for('user_panel'))


@app.route('/admin_dashboard')
def admin_dashboard():
    # Проверяем, авторизован ли пользователь
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа
    
    if session['username'] != 'admin':
        return redirect(url_for('user_panel')) 
    
    bookings = get_all_bookings()
    

    return render_template('admin_dashboard.html', bookings=bookings)



if __name__ == '__main__':
    app.run(debug=True)
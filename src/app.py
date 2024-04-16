from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import sqlite3 # подключаем Sqlite в наш проект 
import hashlib # библиотека для хеширования 
from db.createuser import create_user
from db.helpers import *

app = Flask(__name__, template_folder='templates')
app.secret_key = 'admin1234'  # подствавьте свой секретный ключ
# секретный ключ для хеширования данных сессии при авторизации

# Закрытие соединения с базой данных после запроса
@app.teardown_appcontext
def teardown_db(exception):
    close_db()

@app.route('/')
def index():
    username = None
    if 'username' in session:
        username = session['username']
    return render_template('index.html', username=username)

@app.route('/adm_login', methods=['GET', 'POST'])
def admin_login():
    error = None # обнуляем переменную ошибок 
    if request.method == 'POST':
        username = request.form['username'] # обрабатываем запрос с нашей формы который имеет атрибут name="username"
        password = request.form['password'] # обрабатываем запрос с нашей формы который имеет атрибут name="password"
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest() # шифруем пароль в sha-256

        with get_db_connection() as conn:
            # создаем запрос для поиска пользователя по username,
            # если такой пользователь существует, то получаем все данные id, password
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            # Ваши операции с базой данных здесь
        
        # теперь проверяем если данные сходятся формы с данными БД
        if user and user['password'] == hashed_password:
            # в случае успеха создаем сессию в которую записываем id пользователя
            session['user_id'] = user['id']
            # и делаем переадресацию пользователя на новую страницу -> в нашу адимнку
            return redirect(url_for('admin_panel'))

        else:
            error = 'Неправильное имя пользователя или пароль'

    return render_template('login_adm.html', error=error)

@app.route('/admin_panel')
def admin_panel():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))
    with get_db_connection() as conn:
        # создаем запрос для поиска пользователя по username,
        # если такой пользователь существует, то получаем все данные id, password
        blocks = conn.execute('SELECT * FROM bookings').fetchall()  # Получаем все
        # Ваши операции с базой данных здесь
   

    # Преобразование данных из БД в список словарей
    blocks_list = [dict(ix) for ix in blocks]
    # print(blocks_list) [{строка 1 из бд},{строка 2 из бд},{строка 3 из бд}, строка 4 из бд]

     # Теперь нужно сделать группировку списка в один словарь json
    # Группировка данных в словарь JSON
    json_data = {}
    for raw in blocks_list:
        # Создание новой записи, если ключ еще не существует
        if raw['idblock'] not in json_data:
            json_data[raw['idblock']] = []

        # Добавление данных в существующий ключ
        json_data[raw['idblock']].append({
            'id': raw['id'],
            'user_id': raw['user_id'],
            'start_date': raw['start_date'],
            'end_date': raw['end_date'],
            'house_id': raw['title']
        })

    # print(json_data)
    # передаем на json на фронт - далее нужно смотреть admin_panel.html и обрабатывать там
    return render_template('admin_panel.html', json_data=json_data)


@app.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    session.clear()
    # Перенаправление на главную страницу или страницу входа
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None # обнуляем переменную ошибок 
    if request.method == 'POST':
        username = request.form['username'] # обрабатываем запрос с нашей формы который имеет атрибут name="username"
        password = request.form['password'] # обрабатываем запрос с нашей формы который имеет атрибут name="password"
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest() # шифруем пароль в sha-256

        with get_db_connection() as conn:
            # создаем запрос для поиска пользователя по username,
            # если такой пользователь существует, то получаем все данные id, password
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            # Ваши операции с базой данных здесь
        
        # теперь проверяем если данные сходятся формы с данными БД
        if user and user['password'] == hashed_password:
            # в случае успеха создаем сессию в которую записываем id пользователя
            session['user_id'] = user['id']
            session['username'] = request.form['username']
            # и делаем переадресацию пользователя на новую страницу -> в нашу адимнку
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
        return render_template('user_panel.html', username=username)

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
    house_id = request.args.get('house_id')
    return render_template('calendar.html', house_id=house_id)


@app.route('/booking_confirmation', methods=['GET', 'POST'])
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
        username = session.get('username')

        start_date = request.form['start_date']
        end_date = request.form['end_date']
        house_id = request.form['house_id']
        user_id = session['user_id']

        if user_id:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO bookings (user_id, start_date, end_date, house_id) VALUES (?, ?, ?, ?)', (user_id, start_date, end_date, house_id))
            conn.commit()
            conn.close()
            return jsonify({'message': 'Booking confirmed'}), 200
        else:
            return jsonify({'error': 'User not logged in'}), 401

@app.route('/user_panel')
def user_panel():
    # Проверяем, авторизован ли пользователь
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа

    # Получаем имя пользователя из сеанса
    username = session['username']

    # Проверяем наличие бронирований для текущего пользователя
    has_bookings_var = has_bookings()
    user_bookings = False
    
    if has_bookings_var:
        user_bookings = get_users_bookings()

    return render_template('user_panel.html', username=username, has_bookings=has_bookings_var, user_bookings = user_bookings)

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
        return render_template('edit_booking.html', booking=booking, username=username)
    
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
        return render_template('edit_booking.html', booking=booking, username=username)


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
    return render_template('edit_booking.html', booking=booking, username=username)

@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    # Проверяем, авторизован ли пользователь
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа
    
    # Получаем имя пользователя из сеанса
    username = session['username']

    # Обновляем бронирование в базе данных
    cancel_booking_by_id(booking_id)

    return redirect(url_for('user_panel'))



if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3 # подключаем Sqlite в наш проект 
import hashlib # библиотека для хеширования 
from createuser import create_user

app = Flask(__name__)
app.secret_key = 'admin1234'  # подствавьте свой секретный ключ
# секретный ключ для хеширования данных сессии при авторизации

# Устанавливаем соединение с Базой Данных
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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

        # устанавливаем соединение с БД
        conn = get_db_connection() 
        # создаем запрос для поиска пользователя по username,
        # если такой пользователь существует, то получаем все данные id, password
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        # закрываем подключение БД
        conn.close() 
        
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

    conn = get_db_connection()
    blocks = conn.execute('SELECT * FROM bookings').fetchall()  # Получаем все записи из таблицы content
    conn.close()

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

@app.route('/user_panel')
def user_panel():
    # Проверяем, авторизован ли пользователь
    if 'username' not in session:
        return redirect(url_for('login'))  # Если не авторизован, перенаправляем на страницу входа

    # Получаем имя пользователя из сеанса
    username = session['username']

    conn = get_db_connection()
    blocks = conn.execute('SELECT * FROM bookings').fetchall()  # Получаем все записи из таблицы content
    conn.close()

    # Преобразование данных из БД в список словарей
    blocks_list = [dict(ix) for ix in blocks]
    # print(blocks_list) [{строка 1 из бд},{строка 2 из бд},{строка 3 из бд}, строка 4 из бд]

     # Теперь нужно сделать группировку списка в один словарь json
    # Группировка данных в словарь JSON
    # json_data = {}
    # for raw in blocks_list:
    #     # Создание новой записи, если ключ еще не существует
    #     if raw['idblock'] not in json_data:
    #         json_data[raw['idblock']] = []

    #     # Добавление данных в существующий ключ
    #     json_data[raw['idblock']].append({
    #         'id': raw['id'],
    #         'user_id': raw['user_id'],
    #         'start_date': raw['start_date'],
    #         'end_date': raw['end_date'],
    #         'house_id': raw['title']
    #     })

    # print(json_data)
    # передаем на json на фронт - далее нужно смотреть admin_panel.html и обрабатывать там
    return render_template('user_panel.html', username=username)

@app.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    session.clear()
    # Перенаправление на главную страницу или страницу входа
    return redirect(url_for('index'))

@app.route('/update_content', methods=['POST'])
def update_content():

    booking_id = request.form['id']
    user_id = request.form['user_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    house_id = request.form['house_id']

    # Обработка загруженного файла
    # file = request.files['img']

    # if file and allowed_file(file.filename):
    #     filename = secure_filename(file.filename)
    #     save_path = os.path.join(path_to_save_images, filename)
    #     imgpath = "/static/imgs/"+filename
    #     file.save(save_path)
    #     # Обновите путь изображения в вашей базе данных

    # Обновление данных в базе
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # if file:
    #     cursor.execute('UPDATE content SET short_title=?, img=?, altimg=?, title=?, contenttext=? WHERE id=?',
    #                (short_title, imgpath, altimg, title, contenttext, content_id))
    # else:
    #     cursor.execute('UPDATE content SET short_title=?, altimg=?, title=?, contenttext=? WHERE id=?',
    #                    (short_title, altimg, title, contenttext, content_id))
    # conn.commit()
    conn.close()

    return redirect(url_for('admin_panel'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None # обнуляем переменную ошибок 
    if request.method == 'POST':
        username = request.form['username'] # обрабатываем запрос с нашей формы который имеет атрибут name="username"
        password = request.form['password'] # обрабатываем запрос с нашей формы который имеет атрибут name="password"
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest() # шифруем пароль в sha-256

        # устанавливаем соединение с БД
        conn = get_db_connection() 
        # создаем запрос для поиска пользователя по username,
        # если такой пользователь существует, то получаем все данные id, password
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        # закрываем подключение БД
        conn.close() 
        
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

        return redirect(url_for('user_panel')) # Перенаправление на главную страницу после успешной регистрации

    return render_template('login_reg.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    username = None
    if 'username' in session:
        username = session['username']
    else:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        house_id = request.form['house_id']
        user_id = session['user_id']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bookings (user_id, start_date, end_date, house_id) VALUES (?, ?, ?, ?)', (user_id, start_date, end_date, house_id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    
    # Извлекаем house_id, start_date и end_date из параметров GET-запроса, если они есть
    house_id = request.args.get('house_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    return render_template('booking.html', username=username, house_id=house_id, start_date=start_date, end_date=end_date)

if __name__ == '__main__':
    app.run(debug=True)
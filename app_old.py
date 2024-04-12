import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
app = Flask(__name__)
app.secret_key = 'admin1234'


# Создание или подключение к базе данных
conn = sqlite3.connect('database.db')

# Создание курсора
c = conn.cursor()

# Создание таблицы Content
c.execute('''CREATE TABLE IF NOT EXISTS content (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             idblock TEXT,
             short_title TEXT,
             img TEXT,
             altimg TEXT,
             title TEXT,
             contenttext TEXT,
             author TEXT,
             timestampdata DATETIME)''')

# Создание таблицы Users
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT,
             password TEXT)''')

# Закрытие соединения с базой данных
conn.close()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Проверка, что пользователь с таким именем не существует
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Пользователь с таким именем уже существует', 'error')
            return redirect(url_for('register'))

        # Добавление нового пользователя в базу данных
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        flash('Вы успешно зарегистрировались', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['username'] = username
            flash('Вы успешно вошли', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT start_date, end_date FROM bookings WHERE user_id = ?', (session['user_id'],))
    bookings = cursor.fetchall()
    conn.close()

    if not bookings:
        bookings_message = "Нет доступных бронирований"
    else:
        bookings_message = None

    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']

        conn = sqlite3.connect('db_users.sqlite')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET username = ?, password = ? WHERE id = ?', (new_username, new_password, session['user_id']))
        conn.commit()
        conn.close()

        session['username'] = new_username
        flash('Данные успешно изменены', 'success')
        return redirect(url_for('index'))

    return render_template('account.html', bookings=bookings, bookings_message=bookings_message)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Вы успешно вышли', 'success')
    return redirect(url_for('index'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        house_id = request.form['house_id']
        user_id = session['user_id']

        conn = sqlite3.connect('db_bookings.sqlite')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bookings (user_id, start_date, end_date, house_id) VALUES (?, ?, ?, ?)', (user_id, start_date, end_date, house_id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('book.html')


if __name__ == '__main__':
    app.run(debug=True)
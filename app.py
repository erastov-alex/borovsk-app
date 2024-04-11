import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
app = Flask(__name__)
app.secret_key = 'admin1234'

# Создание базы данных и таблицы для бронирований
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS bookings
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              start_date TEXT,
              end_date TEXT,
              name TEXT,
              surname TEXT)''')
conn.commit()
conn.close()

# Создание базы данных и таблицы для пользователей
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE,
              password TEXT)''')
conn.commit()
conn.close()

conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS bookings
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              start_date TEXT,
              end_date TEXT,
              house_id INTEGER,
              FOREIGN KEY(user_id) REFERENCES users(id),
              FOREIGN KEY(house_id) REFERENCES houses(id))''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/book', methods=['GET', 'POST'])
# def book():
#     if request.method == 'POST':
#         start_date = request.form['start_date']
#         end_date = request.form['end_date']
#         name = request.form['name']
#         surname = request.form['surname']

#         conn = sqlite3.connect('db.sqlite')
#         cursor = conn.cursor()
#         cursor.execute('INSERT INTO bookings (start_date, end_date, name, surname) VALUES (?, ?, ?, ?)', (start_date, end_date, name, surname))
#         conn.commit()
#         conn.close()

#         return redirect(url_for('index'))
#     return render_template('book.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Проверка, что пользователь с таким именем не существует
        conn = sqlite3.connect('db.sqlite')
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
        
        conn = sqlite3.connect('db.sqlite')
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

    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']

        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET username = ?, password = ? WHERE id = ?', (new_username, new_password, session['user_id']))
        conn.commit()
        conn.close()

        session['username'] = new_username
        flash('Данные успешно изменены', 'success')
        return redirect(url_for('index'))

    return render_template('account.html')

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

        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO bookings (user_id, start_date, end_date, house_id) VALUES (?, ?, ?, ?)', (user_id, start_date, end_date, house_id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('book.html')


if __name__ == '__main__':
    app.run(debug=True)
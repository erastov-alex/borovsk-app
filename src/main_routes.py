from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from models.users import *  # Импорт моделей
from tools.helpers import *
from cache_db import get_disc_from_database
import hashlib

from flask_login import login_user, logout_user, current_user, login_required

main_bp = Blueprint('main', __name__)

@main_bp.record
def record_teardown(state):
    app = state.app
    app.teardown_appcontext(close_db)


@main_bp.route('/')
def index():
    show_toast = False
    if 'toast_shown' not in session:
        show_toast = True
        session['toast_shown'] = True
    else:
        show_toast = False

    return render_template('index.html', show_toast=show_toast, current_user=current_user)    


@main_bp.route('/house_selection', methods=['GET', 'POST'])
@login_required
def house_selection():
    # Извлекаем house_id, start_date и end_date из параметров GET-запроса, если они есть
    house_id = request.args.get('house_id')

    return render_template('house_selection.html', house_id=house_id)


@main_bp.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    house_id = request.args.get('house_id')
    return render_template('calendar.html', house_id=house_id, username=current_user.username)


@main_bp.route('/booking_confirmation', methods=['GET', 'POST'])
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


@main_bp.route('/user_panel')
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


@main_bp.route('/user_info')
@login_required
def user_info():
    return render_template('user_info.html', active_page='user_info')


@main_bp.route('/user_settings')
@login_required
def user_settings():
    return render_template('user_settings.html', active_page='user_settings')


@main_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.username != 'admin':
        return redirect(url_for('user_panel')) 
    
    bookings = get_all_bookings()
    
    return render_template('admin_dashboard.html', bookings=bookings)


@main_bp.route('/house/<int:house_id>')
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

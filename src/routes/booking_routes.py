from flask import Blueprint, render_template, request, redirect, url_for
from models.users import *  # Импорт моделей
from utils.helpers import *

from flask_login import login_required


bookings_bp = Blueprint('bookings', __name__)


@bookings_bp.route('/edit_start_date/<int:booking_id>/<int:house_id>/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
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
    
    
@bookings_bp.route('/edit_end_date/<int:booking_id>/<int:house_id>/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
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


@bookings_bp.route('/edit_booking/<int:booking_id>/<int:house_id>/<string:start_date>/<string:end_date>', methods=['GET', 'POST'])
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


@bookings_bp.route('/cancel_booking/<int:booking_id>')
@login_required
def cancel_booking(booking_id):
    # Обновляем бронирование в базе данных
    cancel_booking_by_id(booking_id)

    return redirect(url_for('main.user_panel'))

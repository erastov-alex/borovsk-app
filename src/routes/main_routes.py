from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify, flash
from utils.helpers import *
from utils.cache import get_house_info
from utils.cache import get_all_houses

from flask_login import current_user, login_required

main_bp = Blueprint('main', __name__)

@main_bp.record
def record_teardown(state):
    app = state.app
    app.teardown_appcontext(close_db)


@main_bp.route('/')
def index():
    houses = get_all_houses()

    return render_template('main/index.html', current_user=current_user, houses=houses)    


@main_bp.route('/house_selection', methods=['GET', 'POST'])
@login_required
def house_selection():
    houses = get_all_houses()
    # Извлекаем house_id, start_date и end_date из параметров GET-запроса, если они есть
    if request.method == "POST":
        house_id = request.form.get('house_id')
        session['house_id'] = house_id
        return redirect(url_for('main.calendar'))

    return render_template('main/house_selection.html', houses=houses)


@main_bp.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    house_id = session.get('house_id')  # Retrieve house_id from session
    if not house_id:
        return redirect(url_for('main.house_selection'))
    '''
    Return list of unavailable dates for house_id in YYYY-MM-DD format
    '''
    unavailable_dates = get_unavailable_dates(house_id)
    
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        if not start_date and not end_date:
            flash("Пожалуйста, выберите даты")
        elif start_date in unavailable_dates or end_date in unavailable_dates:
            flash("К сожалению, выбранные даты заняты")
        else:
            session['start_date'] = start_date
            session['end_date'] = end_date
            return redirect(url_for('main.booking_confirmation')) 
    
    return render_template(
        'main/calendar.html', 
        house_id=house_id, 
        username=current_user.username, 
        unavailable_dates=unavailable_dates
        )


@main_bp.route('/booking_confirmation', methods=['GET', 'POST'])
@login_required
def booking_confirmation():
    house_id = session.get('house_id')
    start_date = session.get('start_date')
    end_date = session.get('end_date')
    if not house_id and not start_date and not end_date:
        return redirect(url_for('main.calendar')) 
    
    if request.method == 'GET':
        # Если это GET запрос, просто отображаем страницу подтверждения бронирования
        return render_template('main/booking_confirmation.html', house_id=house_id, start_date=start_date, end_date=end_date)
    
    elif request.method == 'POST':
        # Если это POST запрос, обрабатываем данные бронирования
        user_id = current_user.id
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                return jsonify({'error': 'User not found'}), 404
            add_booking(user_id=user_id, start_date=start_date, end_date=end_date, house_id=house_id)
            session.pop('house_id')
            session.pop('start_date')
            session.pop('end_date')
            return render_template('main/booking_confirmation.html', house_id=house_id, start_date=start_date, end_date=end_date, confirmed=True)
            
        else:
            return jsonify({'error': 'User not logged in'}), 401


@main_bp.route('/house_details/<int:house_id>')
def house_details(house_id):
    # Получаем путь к папке с фотографиями для данного house_id
    house = get_house_info(house_id)
    num_of_photos = len(os.listdir(house.photos_dir))
    stickers = [house.name, house.floors+' Этажа', 'Скидка', 'Мангал', 'Парковка']

        
    # Рендерим шаблон, передавая количество фотографий в контексте
    return render_template(
        'main/house_details.html', 
        house=house,
        num_of_photos=num_of_photos,
        stickers=stickers
        )

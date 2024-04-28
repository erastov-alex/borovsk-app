from flask import Blueprint, jsonify, request

from models.users import *  # Импорт моделей
from models.bookings import *
from models.houses import *

from utils.helpers import *

from flask_jwt_extended import jwt_required


api = Blueprint('api', __name__)


@api.route('/api/all_bookings', methods=['GET'])
@jwt_required()
def all_bookings():
    bookings = get_all_bookings()
    return jsonify(bookings)


@api.route('/api/all_users', methods=['GET'])
@jwt_required()
def all_users():
    users = get_all_users()
    return jsonify(users)


@api.route('/api/edit_booking', methods=['POST'])
@jwt_required()
def edit_booking():
    # Получаем данные редактирования из тела POST запроса
    data = request.json

    # Проверяем, присутствуют ли необходимые данные в запросе
    if 'booking_id' not in data or 'start_date' not in data or 'end_date' not in data or 'house_id' not in data:
        return jsonify({'error': 'Missing data in request'}), 400

    # Получаем booking_id и новые даты из запроса
    booking_id = data['booking_id']
    start_date = data['start_date']
    end_date = data['end_date']
    house_id = data['house_id']

    # Выполняем изменение бронирования в базе данных
    success = update_booking(booking_id, start_date, end_date, house_id=house_id)

    # Проверяем, успешно ли прошло изменение
    if success:
        return jsonify({'message': 'Booking edited successfully'}), 200
    else:
        return jsonify({'error': 'Failed to edit booking'}), 500
    
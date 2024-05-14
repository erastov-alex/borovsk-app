from flask import Blueprint, flash, render_template, redirect, url_for, request, jsonify
from models.users import *
from models.houses import *# Импорт моделей
from utils.helpers import *

from flask_login import current_user, login_required
from flask_jwt_extended import create_access_token


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.username != 'admin':
        return redirect(url_for('user.user_panel')) 
    users = get_all_users()
    bookings = get_all_bookings()

    return render_template('admin/admin_dashboard.html', users=users, bookings=bookings)


@admin_bp.route('/add_house', methods=['GET', 'POST'])
@login_required
def add_house():
    if request.method == 'POST':
        name = request.form.get('name')
        floors = request.form.get('floors')
        persons = request.form.get('persons')
        beds = request.form.get('beds')
        rooms = request.form.get('rooms')
        bbq = True if request.form.get('bbq') else False
        water = True if request.form.get('water') else False
        main_photo = request.form.get('main_photo')
        photos_dir = request.form.get('photos_dir')
        small_disc = request.form.get('small_disc')
        big_disc = request.form.get('big_disc')
        price = request.form.get('price')

        # Создаем новый объект дома
        new_house = House(name=name, floors=floors, persons=persons, beds=beds, rooms=rooms,
                          bbq=bbq, water=water,main_photo=main_photo, photos_dir=photos_dir, small_disc=small_disc, big_disc=big_disc, price=price)
        
        # Добавляем его в базу данных
        db.session.add(new_house)
        db.session.commit()
        
        # Редиректим пользователя на страницу с информацией о добавленном доме
        flash('Дом успешно добавлен!', 'success')
        return redirect(url_for('admin.admin_house'))
    
    # Если метод GET, просто отображаем форму для добавления дома
    return render_template('admin/add_house.html')



 
@admin_bp.route('/admin_bookings')
@login_required
def admin_bookings():
    bookings = get_all_bookings()
    return render_template('admin/admin_bookings.html', bookings=bookings) 

 
@admin_bp.route('/admin_house')
@login_required
def admin_house():
    all_houses = get_all_houses()
    return render_template('admin/admin_house.html', houses=all_houses) 

 
@admin_bp.route('/admin_users')
@login_required
def admin_users():
    all_users = get_all_users()
    return render_template('admin/admin_users.html', users=all_users) 

@admin_bp.route('/api', methods=['GET', 'POST'])
@login_required
def api():
    token = None
    if request.method == 'POST':
        token = create_access_token(identity=current_user.username)
        return jsonify({'token': token})  # Вернуть токен в формате JSON
    return render_template('admin/api.html', token=token) 

@admin_bp.route('/edit_house/<house_id>', methods=['GET', 'POST'])
@login_required
def edit_house(house_id):
    house = House.query.get(house_id)

    if request.method == 'POST':
        # Update house attributes
        house.name = request.form.get('name')
        house.floors = request.form.get('floors')
        house.persons = request.form.get('persons')
        house.beds = request.form.get('beds')
        house.rooms = request.form.get('rooms')
        house.bbq = True if request.form.get('bbq') else False
        house.water = True if request.form.get('water') else False
        house.main_photo = request.form.get('main_photo')
        house.photos_dir = request.form.get('photos_dir')
        house.small_disc = request.form.get('small_disc')
        house.big_disc = request.form.get('big_disc')
        house.price = request.form.get('price')
        db.session.commit()  # Commit the changes
        flash('Изменения Сохранены!')
        return redirect(url_for('admin.admin_house'))  # Redirect to houses list

    return render_template('admin/add_house.html', edit=True, house=house)

@admin_bp.route('/del_house/<house_id>', methods=['POST'])
@login_required
def del_house(house_id):
    if request.method == 'POST':
        house = House.query.get(house_id)
        db.session.delete(house)  # Remove the house object from the session
        db.session.commit()  # Commit the changes
        flash('Дом Удален!')
        return redirect(url_for('admin.admin_house'))  # Redirect to houses list

    return render_template('admin/add_house.html', edit=True, house=house)
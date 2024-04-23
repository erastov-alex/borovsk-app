from flask import Blueprint, flash, render_template, redirect, url_for, request
from models.users import *
from models.houses import *# Импорт моделей
from tools.helpers import *

from flask_login import current_user, login_required


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.username != 'admin':
        return redirect(url_for('user.user_panel')) 
    
    bookings = get_all_bookings()
    
    return render_template('admin_dashboard.html', bookings=bookings)


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
        photos_dir = request.form.get('photos_dir')
        small_disc = request.form.get('small_disc')
        big_disc = request.form.get('big_disc')

        # Создаем новый объект дома
        new_house = House(name=name, floors=floors, persons=persons, beds=beds, rooms=rooms,
                          bbq=bbq, water=water, photos_dir=photos_dir, small_disc=small_disc, big_disc=big_disc)
        
        # Добавляем его в базу данных
        db.session.add(new_house)
        db.session.commit()
        
        # Редиректим пользователя на страницу с информацией о добавленном доме
        flash('Дом успешно добавлен!', 'success')
        return redirect(url_for('main.house_details', house_id=new_house.id))
    
    # Если метод GET, просто отображаем форму для добавления дома
    return render_template('add_house.html')

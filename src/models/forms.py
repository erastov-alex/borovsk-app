from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

class InfoForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Save")
    
class HouseForm(FlaskForm):
    name = StringField('Название дома', validators=[DataRequired(message="Обязательное поле!")])
    floors = IntegerField('Количество этажей', validators=[DataRequired(message="Обязательное поле!"), NumberRange(min=1, message="Количество этажей должно быть больше 0")])
    persons = IntegerField('Количество персон', validators=[DataRequired(message="Обязательное поле!"), NumberRange(min=1, message="Количество персон должно быть больше 0")])
    beds = IntegerField('Количество кроватей', validators=[DataRequired(message="Обязательное поле!"), NumberRange(min=0, message="Количество кроватей не может быть отрицательным")])
    rooms = IntegerField('Количество комнат', validators=[DataRequired(message="Обязательное поле!"), NumberRange(min=0, message="Количество комнат не может быть отрицательным")])
    bbq = BooleanField('Наличие барбекю')
    water = BooleanField('Наличие воды')
    main_photo = StringField('Главная фотография (путь до файла)', validators=[DataRequired(message="Обязательное поле!")])
    photos_dir = StringField('Директория с фотографиями', validators=[DataRequired(message="Обязательное поле!")])
    small_disc = TextAreaField('Короткое описание', validators=[DataRequired(message="Обязательное поле!")])
    big_disc = TextAreaField('Подробное описание', validators=[DataRequired(message="Обязательное поле!")])
    price = TextAreaField('Цена', validators=[DataRequired(message="Обязательное поле!")])
    submit = SubmitField('Сохранить')
    delete = SubmitField('Удалить дом')
    
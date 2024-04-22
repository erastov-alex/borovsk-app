from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
import hashlib
from . import db

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import UserMixin

class User(UserMixin, db.Model):
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    bookings = relationship("Booking", back_populates="user")
    name = Column(String(50), nullable=True)
    intersted = Column(Boolean,nullable=True)

    def __init__(self, username, email, password, name, interested=False):
        self.username = username
        self.email = email
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.name = name
        self.intersted = interested
        
    def get_id(self):
        return self.id
    
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

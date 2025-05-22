from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date
from . import db

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Например, Main, Dessert, Drink

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    dish = db.relationship('Dish', backref=db.backref('menus', lazy=True))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
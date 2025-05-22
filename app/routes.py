from flask import Blueprint, render_template
from datetime import date
from .models import Menu, Dish
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    today = date.today()
    daily_menu = Menu.query.filter_by(date=today).join(Dish).all()
    return render_template('index.html', menu=daily_menu)
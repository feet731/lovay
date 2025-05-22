from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Dish, Menu, User
from . import db, login_manager
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, FloatField, DateField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from datetime import date

admin = Blueprint('admin', __name__)

# Форма для добавления/редактирования блюд
class DishForm(FlaskForm):
    name = StringField('Название блюда', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextField('Описание')
    price = FloatField('Цена', validators=[DataRequired()])
    category = StringField('Категория', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Добавить блюдо')

# Форма для назначения блюд в меню
class MenuForm(FlaskForm):
    date = DateField('Дата', validators=[DataRequired(message='Пожалуйста, выберите дату.')], format='%Y-%m-%d')
    dish_id = SelectField('Блюдо', coerce=int, validators=[DataRequired(message='Пожалуйста, выберите блюдо.')])
    submit = SubmitField('Добавить в меню')

# Форма для входа в админ-панель
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=80)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        return render_template('admin/login.html', form=form, message={'type': 'error', 'text': 'Неверное имя пользователя или пароль'})
    return render_template('admin/login.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@admin.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    dish_form = DishForm()
    menu_form = MenuForm()
    dishes = Dish.query.all()
    menu_form.dish_id.choices = [(dish.id, dish.name) for dish in dishes]
    menus = Menu.query.join(Dish).all()
    return render_template('admin/dashboard.html', dish_form=dish_form, menu_form=menu_form, dishes=dishes, menus=menus)

@admin.route('/dashboard/add_dish', methods=['POST'])
@login_required
def add_dish():
    dish_form = DishForm()
    if dish_form.validate_on_submit():
        try:
            dish = Dish(
                name=dish_form.name.data,
                description=dish_form.description.data,
                price=dish_form.price.data,
                category=dish_form.category.data
            )
            db.session.add(dish)
            db.session.commit()
            return redirect(url_for('admin.dashboard', message={'type': 'success', 'text': 'Блюдо успешно добавлено!'}))
        except Exception as e:
            db.session.rollback()
            return redirect(url_for('admin.dashboard', message={'type': 'error', 'text': f'Ошибка при добавлении блюда: {str(e)}'}))
    errors = '; '.join([f'{field}: {", ".join(messages)}' for field, messages in dish_form.errors.items()])
    return redirect(url_for('admin.dashboard', message={'type': 'error', 'text': f'Ошибка валидации формы: {errors}'}))

@admin.route('/dashboard/add_to_menu', methods=['POST'])
@login_required
def add_to_menu():
    menu_form = MenuForm()
    dishes = Dish.query.all()
    menu_form.dish_id.choices = [(dish.id, dish.name) for dish in dishes]
    if not dishes:
        return redirect(url_for('admin.dashboard', message={'type': 'error', 'text': 'Нет доступных блюд для добавления в меню. Сначала добавьте блюдо.'}))
    if menu_form.validate_on_submit():
        try:
            menu = Menu(
                date=menu_form.date.data,
                dish_id=menu_form.dish_id.data
            )
            db.session.add(menu)
            db.session.commit()
            return redirect(url_for('admin.dashboard', message={'type': 'success', 'text': 'Блюдо успешно добавлено в меню!'}))
        except Exception as e:
            db.session.rollback()
            return redirect(url_for('admin.dashboard', message={'type': 'error', 'text': f'Ошибка при обновлении меню: {str(e)}'}))
    errors = '; '.join([f'{field}: {", ".join(messages)}' for field, messages in menu_form.errors.items()])
    return redirect(url_for('admin.dashboard', message={'type': 'error', 'text': f'Ошибка валидации формы: {errors}'}))

@admin.route('/delete_dish/<int:dish_id>', methods=['POST'])
@login_required
def delete_dish(dish_id):
    try:
        dish = Dish.query.get_or_404(dish_id)
        if Menu.query.filter_by(dish_id=dish_id).first():
            return redirect(url_for('admin.dashboard', message={'type': 'error', 'text': 'Нельзя удалить блюдо, так как оно используется в меню.'}))
        db.session.delete(dish)
        db.session.commit()
        return redirect(url_for('admin.dashboard', message={'type': 'success', 'text': 'Блюдо успешно удалено!'}))
    except Exception as e:
        db.session.rollback()
        return redirect(url_for('admin.dashboard', message={'type': 'error', 'text': f'Ошибка при удалении блюда: {str(e)}'}))

@admin.route('/delete_menu/<int:menu_id>', methods=['POST'])
@login_required
def delete_menu(menu_id):
    try:
        menu = Menu.query.get_or_404(menu_id)
        db.session.delete(menu)
        db.session.commit()
        return redirect(url_for('admin.dashboard', message={'type': 'success', 'text': 'Пункт меню успешно удален!'}))
    except Exception as e:
        db.session.rollback()
        return redirect(url_for('admin.dashboard', message={'type': 'error', 'text': f'Ошибка при удалении пункта меню: {str(e)}'}))
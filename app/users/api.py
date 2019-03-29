from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user
import os
from app.models import User, db, bcrypt
from app import login_manager
from app.users.forms import RegistrationForm, LoginForm


users = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@users.route("/user")
def home():
    return render_template('admin/index.html')

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.home'))
            flash('You have been logged in!', 'success')
        else:
            flash('login Unsuccessful. Please check your email and password', 'danger')
    return render_template('user/login.html', form=form)

@users.route("/create-user", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        print('fuck')
        flash('Data user has been created', 'success')

    return render_template('user/register.html', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))

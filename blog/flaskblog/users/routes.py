""" Module contains user related routes """
from flask import render_template, url_for, flash, redirect, request
from flaskblog.users.forms import (
    RegistrationForm, LoginForm, UpdateAccountForm)
from flask import Blueprint
from flaskblog import db, bcrypt
from flaskblog.models import User
from flask_login import (login_user, current_user, logout_user, login_required)
from flaskblog.users.utils import save_picture


user = Blueprint('user', __name__)


@user.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        encrypt_pwd = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=encrypt_pwd)
        db.session.add(user)  # Adding user to db.
        db.session.commit()  # commiting changes to db.
        flash("Your account is now created, please log in.", 'success')
        return redirect(url_for('login'))  # Return login page
    return render_template('register.html', title='Register', form=form)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # verify that the user list is not empty and compare the passwords
        # from the database to the password enter by the user in the
        # login form.
        if user and bcrypt.check_password_hash(
                user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                redirect(url_for('main.home'))
        else:
            flash("Login unsucessful. Please check username and password",
                  'danger')
    return render_template('login.html', title='Login', form=form)


@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@user.route('/account', methods=['GET', 'POST'])
@login_required  # User needs to log in before accessing this route.
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename=f'profile-pics/{current_user.image_file}')
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

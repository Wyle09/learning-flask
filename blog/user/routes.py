from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask import Blueprint


user = Blueprint('user', __name__)


@user.route('/register', method=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@user.route('/login', method=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # If loop is needed to check that the password and email is valid.
        flash("You have been logged in!", 'success')
        return redirect(url_for('home'))
        # else:
        flash("Login unsucessful. Please check username and password", 'danger')
    return render_template('login.html', title='Login', form=form)

from flask import render_template, url_for, flash, redirect
from flask import Blueprint


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')


@main.route('/about')
def about():
    return render_template('about.html')

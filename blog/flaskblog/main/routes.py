from flask import render_template, url_for, flash, redirect
from flask import Blueprint
from flaskblog.models import Post


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html')

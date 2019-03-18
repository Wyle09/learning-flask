""" Module contains posts related routes """
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.posts.forms import PostForm
from flask import Blueprint
from flaskblog import db
from flaskblog.models import Post
from flask_login import current_user, login_required


post = Blueprint('posts', __name__)


@post.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('main.home'))
    return render_template('create-post.html', title='New Post', form=form)


@post.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@post.route('/post/<int:post_id>/update')
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    return render_template('create-post.html', title='Update', form=form)

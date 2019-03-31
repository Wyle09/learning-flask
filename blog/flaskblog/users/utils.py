import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f'{random_hex}{f_ext}'
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)

    # Resize the picture file before saving it to the file system.
    output_size = (125, 125)
    resize_img = Image.open(form_picture)
    resize_img.thumbmail(output_size)
    resize_img.save(picture_path)

    return picture_fn


def send_reset_email(user):
    """ Sends an email to the user containing a reset token link """
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender='noreply@gmail.com',
                  recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request please ignore this email.
'''
    mail.send(msg)

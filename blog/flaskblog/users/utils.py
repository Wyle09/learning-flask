import os
import secrets
from PIL import Image
from flaskblog import app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = f'{random_hex}{f_ext}'
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    # Resize the picture file before saving it to the file system.
    output_size = (125, 125)
    resize_img = Image.open(form_picture)
    resize_img.thumbmail(output_size)
    resize_img.save(picture_path)

    return picture_fn

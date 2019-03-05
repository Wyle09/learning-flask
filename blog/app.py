from flask import Flask, render_template, session, request, redirect, flash
from flask_bootstrap import Bootstrap
from database import query
from database.Database import Database
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/blogs/<int:id>')
def blogs(id):
    return render_template('blogs.html', blog_id=id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        # Get values from the user registration form.
        user_registration = request.form

        if user_registration['password'] != user_registration['confirm_password']:
            flash("Password does not match! Try again", 'danger')
            return render_template('register.html')

        register_query = query.register(user_registration['first_name'],
                                        user_registration['last_name'],
                                        user_registration['username'],
                                        user_registration['email'],
                                        generate_password_hash(
                                                user_registration['password']))
        db = Database(register_query)
        execute = db.execute_query()
        flash("Registration successful! Please login", 'success')
        conn = execute[0]  # Get connection object.
        conn.commit()
        conn.close()
        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_login = request.form
        login_query = query.login(user_login['username'])
        db = Database(login_query)
        execute = db.execute_query()
        conn, cur = execute  # get connection & cursor objects.
        user = cur.fetchone()  # User in DB.

        if user:  # Check if user exist.
            # compare password between db and login form.
            if check_password_hash(user.Password, user_login['password']):
                session['_login'] = True
                session['_firstName'] = user.First_Name
                session['_lastName'] = user.Last_Name
                success_message = "Welcome {0} ! You have been successfully" \
                    " logged in".format(user_login['username'])
                flash(success_message, 'success')
            else:
                conn.close()
                flash("Password does not match", 'danger')
                return render_template('login.html')
        else:
            conn.close()
            flash("User not found", 'danger')
            return render_template('login.html')

    return render_template('login.html')


@app.route('/write-blog', methods=['GET', 'POST'])
def write_blog():
    return render_template('write-blog.html')


@app.route('/my-blogs')
def my_blogs():
    return render_template('my-blogs.html')


@app.route('/edit-blog/<int:id>', methods=['GET', 'POST'])
def edit_blog():
    return render_template('edit-blog.html')


@app.route('/delete-blog/<int:id>', methods=['POST'])
def delete_blog():
    return 'Success'


@app.route('/logout')
def logout():
    # Close connection after user logs out.
    return render_template('logout.html')


def main():
    if __name__ == '__main__':
        app.run(debug=True)


main()

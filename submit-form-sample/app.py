from flask import Flask, render_template, request, session, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc
import yaml
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
bootstrap = Bootstrap(app)


def sql_server_connection():
    db_config = yaml.load(open('db.yaml'))
    conn = pyodbc.connect(driver=db_config['driver'], host=db_config['server'],
                          database=db_config['db'], user_id=db_config['uid'],
                          password=db_config['pwd'])
    return conn


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sql_server_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            form = request.form
            name = form['name']
            age = form['age']
            password = form['password']
            # encrypt the password before storing the data in the db
            password = generate_password_hash(password)
            insert_query = "INSERT INTO employee(name, age, pwd) VALUES" \
                "('{0}',{1},'{2}')".format(name, age, password)
            cur.execute(insert_query)
            flash('Successfully inserted data', 'success')
            conn.commit()
        except Exception as e:  # ImportError:
            flash("Failed to insert data", 'danger')
            flash(e, 'danger')

    return render_template('index.html')


@app.route('/employees')
def employee():
    conn = sql_server_connection()
    cur = conn.cursor()
    select_query = "SELECT * FROM employee"
    cur.execute(select_query)
    employees_data = cur.fetchall()

    if len(employees_data) > 0:
        # can optain the user information without accessing the db again.
        session['username'] = employees_data[0].name
        # check that passwords match.
        # return str(check_password_hash(employees_data[0].pwd, 'Password_1'))
        return render_template('employees.html', employees=employees_data)


def main():
    if __name__ == '__main__':
        app.run(debug=True)


main()

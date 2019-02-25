from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import pyodbc
import yaml


app = Flask(__name__)
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
        form = request.form
        name = form['name']
        age = form['age']
        insert_query = "INSERT INTO employee(name, age) VALUES('{0}', {1})" \
            .format(name, age)
        cur.execute(insert_query)
        conn.commit()

    return render_template('index.html')


@app.route('/employees')
def employee():
    conn = sql_server_connection()
    cur = conn.cursor()
    select_query = "SELECT * FROM employee"
    cur.execute(select_query)
    employees_data = cur.fetchall()

    if len(employees_data) > 0:
        return render_template('employees.html', employees=employees_data)


def main():
    if __name__ == '__main__':
        app.run(debug=True)


main()

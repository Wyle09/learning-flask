from flask import Flask, render_template
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


def execute_query(query):
    conn = sql_server_connection()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()


@app.route('/')
def index():
    query = "INSERT INTO [User] VALUES({0})".format(" 'Mike' ")
    execute_query(query)
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/css')
def css():
    return render_template('css.html')


def main():
    if __name__ == '__main__':
        app.run(debug=True)


main()

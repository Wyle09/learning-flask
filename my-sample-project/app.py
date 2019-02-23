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


@app.route('/')
def index():
    conn = sql_server_connection()
    cur = conn.cursor()
    #    query = "INSERT INTO [User] VALUES({0})".format(" 'Mike' ")
    query = "SELECT * FROM [User]"
    cur.execute(query)
    results = cur.fetchall()

    if len(results) > 0:
        # Convert list of pyodb rows to list
        user_list = [row[0] for row in results]
        return user_list[0]

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

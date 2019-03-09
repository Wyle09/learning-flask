from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
    blogs_query = query.select_blog()
    db = Database(blogs_query)
    execute = db.execute_query()
    conn, cur = execute
    blogs = cur.fetchall()

    if blogs:
        conn.close()
        return render_template('index.html', blogs=blogs)
    return render_template('index.html', blogs=None)


@main.route('/about')
def about():
    return render_template('about.html')

from flask import Blueprint

blog_post = Blueprint('blog_post', __name__)


@blog_post.route('/blogs/<int:id>')
def blogs(id):
    blogs_query = query.select_blog_id(id)
    db = Database(blogs_query)
    execute = db.execute_query()
    conn, cur = execute
    blog = cur.fetchone()

    if blog:
        conn.close()
        return render_template('blogs.html', blog=blog)

    return "Blog not found"


@blog_post.route('/write-blog', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        blog_post = request.form
        author = "{0} {1}".format(session['firstName'], session['lastName'])
        write_query = query.write_blog_query(blog_post['title'],
                                             author,
                                             blog_post['body'])
        db = Database(write_query)
        execute = db.execute_query()
        conn, cur = execute
        conn.commit()
        conn.close()
        flash("Successfully posted new blog", 'sucess')
        return redirect('/')

    return render_template('write-blog.html')


@blog_post.route('/my-blogs')
def my_blogs():
    return render_template('my-blogs.html')


@blog_post.route('/edit-blog/<int:id>', methods=['GET', 'POST'])
def edit_blog():
    return render_template('edit-blog.html')


@blog_post.route('/delete-blog/<int:id>', methods=['POST'])
def delete_blog():
    return 'Success'

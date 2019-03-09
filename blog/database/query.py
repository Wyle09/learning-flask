def register(first_name, last_name, user_name, email, password):
    query = """
    SET NOCOUNT ON;
    INSERT INTO [User](
        [First_Name],
        [Last_Name],
        [Username],
        [Email],
        [Password])
       VALUES('{0}','{1}','{2}','{3}','{4}');
    """.format(first_name, last_name, user_name, email, password)
    return query


def username_exist(username):
    query = """
    SET NOCOUNT ON; SELECT * FROM [User] WHERE [Username] = '{0}';
    """.format(username)
    return query


def write_blog_query(title, body, author):
    query = """
    SETNOCOUNT ON;
    INSERT INTO [Blog](
    [Title],
    [Author],
    [Body])
    VALUES('{0}','{1}','{2}');
    """.format(title, body, author)
    return query


def select_blog():
    query = "SET NOCOUNT ON; SELECT * FROM BLOG;"
    return query


def select_blog_id(id):
    query = """
    SET NOCOUNT ON;
    SELECT * FROM Blog WHERE Blog_Id = {0};
    """.format(id)
    return query

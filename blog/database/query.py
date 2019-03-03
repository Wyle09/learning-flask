def register(first_name, last_name, user_name, email, password):
    query = """
    INSERT INTO [User](
        [First_Name],
        [Last_Name],
        [Username],
        [Email],
        [Password])
       VALUES('{0}','{1}','{2}','{3}','{4}')
    """.format(first_name, last_name, user_name, email, password)
    return query


def login(username):
    query = "SELECT * FROM [User] WHERE [Username] = '{0}'".format(username)
    return query

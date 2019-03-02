import pyodbc
import yaml


class Database:
    def __init__(self, query):
        self.query = query

    def sql_server_connection(self):
        db_config = yaml.load(open('database/db.yaml'))
        conn = pyodbc.connect(driver=db_config['driver'],
                              host=db_config['server'],
                              database=db_config['db'],
                              user_id=db_config['uid'],
                              password=db_config['pwd'])
        return conn

    def execute_query(self):
        conn = self.sql_server_connection()
        cur = conn.cursor()
        cur.execute(self.query)
        conn.commit()
        return conn, cur

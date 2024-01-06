import mysql.connector

class DatabaseConnection:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "1234$",
            "database": "weblaptop"
        }
        self.conn = mysql.connector.connect(**self.db_config)

    def get_connection(self):
        return self.conn

    def close_connection(self):
        self.conn.close()
        
    def cursor(self):
        return self.conn.cursor()
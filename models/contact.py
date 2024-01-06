import mysql.connector

class ContactModel:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "1234$",
            "database": "weblaptop"
        }
        self.conn = mysql.connector.connect(**self.db_config)

    def get_contact(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM contact")
        data = cursor.fetchall()
        data = [dict(zip(cursor.column_names, row)) for row in data]
        cursor.close()
        return data
    
    def close_connection(self):
        self.conn.close()
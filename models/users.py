import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "1234$",
            "database": "weblaptop"
        }
        self.conn = mysql.connector.connect(**self.db_config)

    def get_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        data = [dict(zip(cursor.column_names, row)) for row in data]
        cursor.close()
        return data
    
    def get_user_detail(self, user_id):
        cursor = self.conn.cursor()
        query = "SELECT * FROM users WHERE ID = %s"
        cursor.execute(query, (user_id,))
        data = cursor.fetchone()
        cursor.close()
        if data:
            return dict(zip(cursor.column_names, data))
        return None

    def login(self, username, password):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE TK = %s AND MK = %s", (username,password))
        user = cursor.fetchone()
        cursor.close()
        return user

    def register(self, hoten, username, password, email, sdt, diachi):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (Hoten, TK, MK, Email, SDT, Diachi, PQ) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (hoten, username, password, email, sdt, diachi, 0))
        self.conn.commit()
        cursor.close()

    def check_tk(self, username):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE TK = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        return user

    def create_user(self, hoten, username, password, email, sdt, diachi, pq):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (Hoten, TK, MK, Email, SDT, Diachi, PQ) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (hoten, username, password, email, sdt, diachi, pq))
        self.conn.commit()
        cursor.close()

    def update_user(self, user_id, ht,tk,mk,e,sdt,dc,pq):
        cursor = self.conn.cursor()
        update_query = "UPDATE users SET Hoten = %s, TK = %s, MK = %s, Email = %s, SDT = %s, Diachi = %s, PQ = %s WHERE ID = %s;"
        cursor.execute(update_query, (ht, tk, mk, e, sdt, dc, pq, user_id))
        self.conn.commit()
        cursor.close()
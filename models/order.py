import mysql.connector

class OrderModel:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "1234$",
            "database": "weblaptop"
        }
        self.conn = mysql.connector.connect(**self.db_config)

    def get_orders(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT orders.*,users.Hoten FROM orders,users where orders.userID = users.ID")
        data = cursor.fetchall()
        data = [dict(zip(cursor.column_names, row)) for row in data]
        cursor.close()
        return data
    
    def get_orders_detail(self, order_id):
        cursor = self.conn.cursor()
        query = "SELECT orderdetail.*,orders.trangthai FROM orderdetail,orders WHERE orderdetail.orderID=orders.ID and orderID = %s"
        cursor.execute(query, (order_id,))
        data = cursor.fetchall()
        data = [dict(zip(cursor.column_names, row)) for row in data]
        cursor.close()
        return data
    
    def update_order(self, order_id, tt):
        cursor = self.conn.cursor()
        update_query = "UPDATE orders SET trangthai = %s WHERE ID = %s"
        cursor.execute(update_query, (tt, order_id))
        self.conn.commit()
        cursor.close()
    
    def create_order(self, user_id, total_amount, address):
        cursor = self.conn.cursor()
        insert_query = "INSERT INTO orders (userID, ngaydat, diachi, tongtien, trangthai) VALUES (%s, NOW(), %s, %s, 0)"
        cursor.execute(insert_query, (user_id, address, total_amount))
        self.conn.commit()
        order_id = cursor.lastrowid
        cursor.close()
        return order_id

    def create_order_detail(self, order_id, product_id, quantity, price):
        cursor = self.conn.cursor()
        insert_query = "INSERT INTO orderdetail (orderID, masp, sl, gia) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (order_id, product_id, quantity, price))
        self.conn.commit()
        cursor.close()

    def close_connection(self):
        self.conn.close()
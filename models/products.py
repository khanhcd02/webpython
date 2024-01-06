import mysql.connector

class ProductModel:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "1234$",
            "database": "weblaptop"
        }
        self.conn = mysql.connector.connect(**self.db_config)

    def get_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT products.*,brands.hangsx FROM products,brands WHERE products.Loaisp = brands.ID")
        data = cursor.fetchall()
        data = [dict(zip(cursor.column_names, row)) for row in data]
        cursor.close()
        return data
    
    def get_product_by_id(self, product_id):
        cursor = self.conn.cursor()
        query = "SELECT * FROM products WHERE ID = %s"
        cursor.execute(query, (product_id,))
        data = cursor.fetchone()
        cursor.close()
        if data:
            return dict(zip(cursor.column_names, data))
        return None

    def create_product(self, name, price, description, img, loaisp):
        cursor = self.conn.cursor()
        insert_query = "INSERT INTO products (Tensp, Gia, Mota, Img, Loaisp) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (name, price, description, img, loaisp))
        self.conn.commit()
        cursor.close()

    def update_product(self, product_id, name, price, description, img, loaisp):
        cursor = self.conn.cursor()
        update_query = "UPDATE products SET Tensp = %s, Gia = %s, Mota = %s, Img = %s, Loaisp = %s WHERE ID = %s"
        cursor.execute(update_query, (name, price, description, img, loaisp, product_id))
        self.conn.commit()
        cursor.close()

    def delete_product(self, product_id):
        cursor = self.conn.cursor()
        delete_query = "DELETE FROM products WHERE ID = %s"
        cursor.execute(delete_query, (product_id,))
        self.conn.commit()
        cursor.close()

    def close_connection(self):
        self.conn.close()

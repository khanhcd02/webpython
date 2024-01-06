import mysql.connector

class BrandModel:
    def __init__(self, db_connection):
        self.conn = db_connection

    def get_brands(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM brands")
        data = cursor.fetchall()
        data = [dict(zip(cursor.column_names, row)) for row in data]
        cursor.close()
        return data

    def create_brand(self, hangsx):
        cursor = self.conn.cursor()
        insert_query = "INSERT INTO brands (hangsx) VALUES (%s)"
        cursor.execute(insert_query, (hangsx,))
        self.conn.commit()
        cursor.close()

    def update_brand(self, brand_id, hangsx):
        cursor = self.conn.cursor()
        update_query = "UPDATE brands SET hangsx = %s WHERE ID = %s"
        cursor.execute(update_query, (hangsx, brand_id))
        self.conn.commit()
        cursor.close()

    def delete_brand(self, brand_id):
        cursor = self.conn.cursor()
        delete_query = "DELETE FROM brands WHERE ID = %s"
        cursor.execute(delete_query, (brand_id,))
        self.conn.commit()
        cursor.close()

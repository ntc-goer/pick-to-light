import os

import psycopg2

db = None


def init_db():
    global db
    if db is None:
        db_host = os.getenv("DATABASE_HOST", "localhost")
        db_name = os.getenv("DATABASE_NAME", "server_db")
        db_port = os.getenv("DATABASE_PORT", 5433)
        db_user = os.getenv("DATABASE_USER", "user")
        db_password = os.getenv("DATABASE_PASSWORD", "12345")
        return DatabaseManager(db_host, db_port, db_user, db_password, db_name)
    return db


def get_db():
    global db
    if db is None:
        return init_db()
    return db


class DatabaseManager:
    def __init__(self, host, port, user, password, dbname):
        self.conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        self.cursor = self.conn.cursor()

    def insert_product(self, name, price):
        self.cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
        self.conn.commit()

    def get_products_by_category(self, category_id):
        query = """SELECT id, product_name, product_image, price, stock 
                   FROM products
                   WHERE category_id = %s"""
        with self.conn.cursor() as cur:
            cur.execute(query, (category_id,))
            rows = cur.fetchall()
            print(rows)
            # convert to list of dict
            result = [
                {"id": r[0], "product_name": r[1], "product_image": r[2], "price": r[3], "stock": r[4]}
                for r in rows
            ]
        return result

    def close(self):
        self.cursor.close()
        self.conn.close()

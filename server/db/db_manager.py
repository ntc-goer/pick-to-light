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

    def create_order_item(self, order_id, product_id, quantity, price):
        query = """
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (order_id, product_id, quantity, price))
            self.conn.commit()

    def delete_cart(self, cart_id):
        query = """
                DELETE \
                FROM carts
                WHERE id = %s RETURNING id \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (cart_id,))
            self.conn.commit()

    def create_order(self, user_id):
        query = """
                INSERT INTO orders (user_id)
                VALUES (%s) RETURNING id, user_id, created_at \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (user_id,))
            row = cur.fetchone()
            self.conn.commit()

            if row:
                return {
                    "id": row[0],
                    "user_id": row[1],
                    "created_at": row[2],
                }
            return None

    def create_cart_item(self, cart_id, product_id, quantity):
        query = """
                INSERT INTO cart_items (cart_id, product_id, quantity)
                VALUES (%s, %s, %s) RETURNING id, cart_id, product_id, quantity \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (cart_id, product_id, quantity))
            self.conn.commit()

    def get_order_items_by_order_id(self, order_id):
        query = """
                SELECT oi.id, \
                       oi.order_id, \
                       oi.product_id, \
                       oi.quantity, \
                       oi.price, \
                       p.product_name, \
                       p.product_image
                FROM order_items oi
                         JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = %s
                ORDER BY oi.id DESC \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (order_id,))
            rows = cur.fetchall()
            if not rows:
                return []

            # convert to list of dicts
            result = [
                {
                    "id": r[0],
                    "order_id": r[1],
                    "product_id": r[2],
                    "quantity": r[3],
                    "price": r[4],
                    "product_name": r[5],
                    "product_image": r[6],
                }
                for r in rows
            ]
            return result

    def get_cart_items(self, cart_id):
        query = """
                SELECT 
                    ci.id,
                    ci.product_id,
                    p.product_name,
                    p.product_image,
                    p.price,
                    ci.quantity
                FROM cart_items ci
                JOIN products p ON ci.product_id = p.id
                WHERE ci.cart_id = %s
                ORDER BY ci.created_at DESC
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (cart_id,))
            rows = cur.fetchall()
            if not rows:
                return []
            result = [
                {
                    "id": r[0],
                    "product_id": r[1],
                    "product_name": r[2],
                    "product_image": r[3],
                    "price": r[4],
                    "quantity": r[5],
                }
                for r in rows
            ]
        return result

    def update_cart_item_quantity(self, cart_item_id, quantity):
        if quantity <= 0:
            query = """
                    DELETE \
                    FROM cart_items
                    WHERE id = %s
                    """
            with self.conn.cursor() as cur:
                cur.execute(query, cart_item_id)
                self.conn.commit()

        query = """
                UPDATE cart_items
                SET quantity = %s
                WHERE id = %s
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (quantity, cart_item_id))
            self.conn.commit()

    def get_cart_item(self, cart_id, product_id):
        query = """SELECT id, cart_id, product_id, quantity
                   FROM cart_items
                   WHERE cart_id = %s AND product_id = %s"""
        with self.conn.cursor() as cur:
            cur.execute(query, (cart_id,product_id))
            row = cur.fetchone()
            if row is None:
                return None
            # convert to list of dict
            result = {"id": row[0], "cart_id": row[1], "product_id": row[2], "quantity": row[3],}

            return result

    def get_products_by_category(self, category_id):
        query = """SELECT id, product_name, product_image, price, stock 
                   FROM products
                   WHERE category_id = %s"""
        with self.conn.cursor() as cur:
            cur.execute(query, (category_id,))
            rows = cur.fetchall()
            # convert to list of dict
            result = [
                {"id": r[0], "product_name": r[1], "product_image": r[2], "price": r[3], "stock": r[4]}
                for r in rows
            ]
            return result

    def get_orders(self):
        query = """
                SELECT id, user_id, created_at
                FROM orders
                ORDER BY created_at DESC \
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            orders = []
            for row in rows:
                orders.append({
                    "id": row[0],
                    "user_id": row[1],
                    "created_at": row[2],
                })
            return orders

    def close(self):
        self.cursor.close()
        self.conn.close()

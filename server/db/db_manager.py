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

    def drop_all_table(self):
        self.cursor.execute("""
                            SELECT tablename
                            FROM pg_tables
                            WHERE schemaname = 'public';
                            """)

        tables = self.cursor.fetchall()
        print("tables: ", tables)
        for table in tables:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE;")
            print(f"Dropped table: {table[0]}")

    def run_script(self, filename):
        try:
            print(f"Running script {filename}")
            with open(filename, "r", encoding="utf-8") as f:
                sql_code = f.read()
                for statement in sql_code.split(";"):
                    stmt = statement.strip()
                    if stmt:
                        self.cursor.execute(stmt)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def insert_product(self, product_name, product_image, price, stock):
        self.cursor.execute("INSERT INTO products (product_name, product_image, price, stock) VALUES ("
                            "%s, %s, %s, %s)", (product_name, product_image, price, stock))
        self.conn.commit()

    def get_product_by_id(self, product_id):
        query = """
                SELECT id, product_name, product_image, stock, price
                FROM products
                WHERE id = %s \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (product_id,))
            row = cur.fetchone()
            if row is None:
                return None
            return {
                "id": row[0],
                "product_name": row[1],
                "product_image": row[2],
                "stock": row[3],
                "price": row[4],
            }

    def update_product_by_id(self, product_id, product_name, product_image, stock, price):
        query = """
                UPDATE products
                SET product_name  = %s,
                    product_image = %s,
                    stock         = %s,
                    price         = %s
                WHERE id = %s
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (product_name, product_image, stock, price, product_id))
            self.conn.commit()
            return cur.rowcount > 0  # True if at least one row was updated

    def get_product_location(self, shelve, row_location, column_location):
        query = """
                SELECT pl.id,
                       pl.product_id,
                       pl.shelve,
                       pl.row_location,
                       pl.column_location,
                       pl.module_id,
                       pl.quantity,
                       p.product_name
                FROM product_locations pl
                         JOIN products p ON pl.product_id = p.id
                WHERE pl.shelve = %s
                  AND pl.row_location = %s
                  AND pl.column_location = %s LIMIT 1; \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (shelve, row_location, column_location))
            row = cur.fetchone()
            if row is None:
                return None
            return {
                "id": row[0],
                "product_id": row[1],
                "shelve": row[2],
                "row_location": row[3],
                "column_location": row[4],
                "module_id": row[5],
                "quantity": row[6],
                "product_name": row[7],
            }

    def get_product_location_by_product_id(self, product_id):
        query = """
                SELECT id, product_id, shelve, row_location, column_location, module_id
                FROM product_locations
                WHERE product_id = %s
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (product_id,))
            rows = cur.fetchall()

            locations = []
            for row in rows:
                locations.append({
                    "id": row[0],
                    "product_id": row[1],
                    "shelve": row[2],
                    "row_location": row[3],
                    "column_location": row[4],
                    "module_id": row[5]
                })
            return locations

    def upsert_product_location(self, product_id, shelve, row_location, column_location, module_id, quantity):
        query = """
                INSERT INTO product_locations (product_id, shelve, row_location, column_location, module_id, quantity)
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (shelve, row_location, column_location)
               DO
                UPDATE SET
                    product_id = EXCLUDED.product_id,
                    quantity = EXCLUDED.quantity,
                    module_id = EXCLUDED.module_id;
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (product_id, shelve, row_location, column_location, module_id, int(quantity)))
        self.conn.commit()

    def upsert_shelve_module_mapping(self, location_id, module_id):
        query = """
                INSERT INTO shelve_module_mappings (module_id, product_location_id)
                VALUES (%s, %s) ON CONFLICT (module_id, product_location_id)
                       DO \
                UPDATE SET module_id = EXCLUDED.module_id; \
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (module_id, location_id))
        self.conn.commit()

    def get_products(self):
        query = """
                SELECT id, \
                       product_name, \
                       product_image, \
                       price, \
                       stock
                FROM products
                ORDER BY product_name ASC
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                return []
            result = [
                {
                    "id": r[0],
                    "product_name": r[1],
                    "product_image": r[2],
                    "price": r[3],
                    "stock": r[4],
                }
                for r in rows
            ]
        return result

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
                SELECT oi.id,
                       oi.order_id,
                       oi.product_id,
                       oi.quantity,
                       oi.price,
                       p.product_name,
                       p.product_image
                FROM orders o
                         JOIN order_items oi ON o.id = oi.order_id
                         JOIN products p ON oi.product_id = p.id
                WHERE o.id = %s
                ORDER BY oi.id DESC;
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
                SELECT ci.id,
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
                   WHERE cart_id = %s
                     AND product_id = %s"""
        with self.conn.cursor() as cur:
            cur.execute(query, (cart_id, product_id))
            row = cur.fetchone()
            if row is None:
                return None
            # convert to list of dict
            result = {"id": row[0], "cart_id": row[1], "product_id": row[2], "quantity": row[3], }

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

    def get_order_by_id(self, order_id):
        query = """
                SELECT id, user_id, created_at
                FROM orders
                WHERE id = %s
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (order_id,))
            row = cur.fetchone()

            if row:
                return {
                    "id": row[0],
                    "user_id": row[1],
                    "created_at": row[2],
                }
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()

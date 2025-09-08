import psycopg2

class DatabaseManager:
    def __init__(self, host="localhost", dbname="warehouse", user="postgres", password="your_password", port=5432):
        self.conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            price NUMERIC
        )
        """)
        self.conn.commit()

    def insert_product(self, name, price):
        self.cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
        self.conn.commit()

    def get_products(self):
        self.cursor.execute("SELECT id, name, price FROM products")
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

import os

from dotenv import load_dotenv

from db.db_manager import DatabaseManager

load_dotenv()

def init_db():
    db_host = os.getenv("DATABASE_HOST", "localhost")
    db_name = os.getenv("DATABASE_NAME", "server_db")
    db_port = os.getenv("DATABASE_PORT", 5433)
    db_user = os.getenv("DATABASE_USER", "user")
    db_password = os.getenv("DATABASE_PASSWORD", "12345")
    return DatabaseManager(db_host, db_port, db_user, db_password, db_name)

db = init_db()

print("Start setup.....")
db.drop_all_table()
db.run_script("db/schema.sql")
db.run_script("db/data.sql")
print("Setting up finished.....")

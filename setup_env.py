from Data.connect_to_db import get_connection
import secrets

if True:
    conn = get_connection()
    conn.close()

    SECRET_KEY = secrets.token_hex(16)

    DATABASE_URL = "postgresql:///" + input("Enter the address of your database: postgresql:/// ")
    with open(".env", "w") as f:
        f.write(f"DATABASE_URL={DATABASE_URL}\n")
        f.write(f"SECRET_KEY={SECRET_KEY}")
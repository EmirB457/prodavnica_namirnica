import sqlite3
import pandas as pd

DB_NAME = "store.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            expiry_date TEXT,
            supplier TEXT,
            min_stock INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_product(name, category, price, quantity, expiry_date, supplier, min_stock):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products (name, category, price, quantity, expiry_date, supplier, min_stock)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, category, price, quantity, expiry_date, supplier, min_stock))

    conn.commit()
    conn.close()


def get_products():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM products ORDER BY id DESC", conn)
    conn.close()
    return df


def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

    conn.commit()
    conn.close()


def get_low_stock():
    conn = get_connection()
    query = """
        SELECT * FROM products
        WHERE quantity <= min_stock
        ORDER BY quantity ASC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
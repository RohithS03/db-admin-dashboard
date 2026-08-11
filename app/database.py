import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample.db"))

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall() if not row[0].startswith('sqlite_')]
    conn.close()
    return tables

def get_table_schema(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info('{table_name}');")
    columns = cursor.fetchall()
    conn.close()
    return columns

def get_table_data(table_name, limit=50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM '{table_name}' LIMIT {limit};")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description] if cursor.description else []
    conn.close()
    return columns, rows

def execute_raw_sql(sql_query):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        if sql_query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []
            conn.close()
            return columns, rows, None
        else:
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            return ["Affected Rows"], [[affected]], None
    except Exception as e:
        conn.close()
        return [], [], str(e)

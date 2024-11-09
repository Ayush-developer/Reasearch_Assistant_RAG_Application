# config/db_config.py
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="ingestion",  # Adjust your DB name
        user="postgres",  # Your DB username
        password="password"  # Your DB password
    )


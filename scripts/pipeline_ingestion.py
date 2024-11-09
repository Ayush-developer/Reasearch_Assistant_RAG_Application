import psycopg2
# Connect to the PostgreSQL database running in the Docker container
try:
    conn = psycopg2.connect(
        host="localhost",      # Host is localhost since PostgreSQL is mapped to this port
        port=5432,             # Port exposed by Docker
        database="postgres",  # Your database name
        user="postgres",       # PostgreSQL user
        password="password"  # Your PostgreSQL password
    )
    cursor = conn.cursor()
    print("Connection successful!")
except Exception as e:
    print(f"Error: {e}")


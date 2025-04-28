import mysql.connector

def connection():
    # Configuration dictionary for MySQL connection
    db_config = {
        'host': 'localhost',         # MySQL server is hosted locally
        'user': 'root',              # Default user in XAMPP MySQL
        'password': '',              # Default empty password for XAMPP MySQL
        'database': 'studenttracker' # Your database name
    }

    try:
        # Establishing connection to the MySQL database
        conn = mysql.connector.connect(**db_config)
        print("Successfully connected to the database.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

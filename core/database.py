"""
Database Module for Chatbot SI
-------------------------------
Handles MySQL database connections and data loading.
"""

import mysql.connector
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_db_connection():
    """
    Initialize database connection with auto-reconnect and timeout settings.
    Supports both Railway DATABASE_URL and local .env configuration.
    
    Returns:
        MySQL connection object or None if failed
    """
    try:
        # Check if Railway DATABASE_URL is available
        database_url = os.getenv('DATABASE_URL')
        
        if database_url:
            # Parse Railway DATABASE_URL format: mysql://user:password@host:port/database
            import re
            match = re.match(r'mysql://(.+):(.+)@(.+):(\d+)/(.+)', database_url)
            if match:
                user, password, host, port, database = match.groups()
                print(f"[DB] Connecting to Railway MySQL...")
                print(f"[DB] Host: {host}, Port: {port}, Database: {database}, User: {user}")
                db_connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    port=int(port),
                    consume_results=True,
                    autocommit=True,  # Enable autocommit to prevent connection issues
                    pool_name="chatbot_pool",  # Connection pooling
                    pool_size=5,  # Pool size
                    connection_timeout=30,  # 30 seconds timeout
                    pool_reset_session=True  # Reset session on pool get
                )
                print("[OK] Railway Database Connected Successfully")
                return db_connection
            else:
                print(f"[ERROR] Invalid DATABASE_URL format")
                return None
        
        # Fallback to local/manual environment variables
        host = os.getenv('MYSQL_HOST', 'localhost')
        user = os.getenv('MYSQL_USER', 'root')
        password = os.getenv('MYSQL_PASSWORD', '')
        database = os.getenv('MYSQL_DATABASE', 'chatbot_si')
        
        print("[DB] Using local database configuration...")
        print(f"[DB] Host: {host}, Database: {database}, User: {user}")
        print(f"[DB] Password: {'*' * len(password) if password else '(empty)'}")
        
        db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            consume_results=True,
            autocommit=True,  # Enable autocommit
            connection_timeout=30,  # Increase timeout to 30 seconds
            # Additional settings to prevent connection loss
            use_pure=True,  # Use pure Python implementation (more stable)
        )
        
        # Set additional session variables to prevent timeout
        cursor = db_connection.cursor()
        cursor.execute("SET SESSION wait_timeout=28800")  # 8 hours
        cursor.execute("SET SESSION interactive_timeout=28800")  # 8 hours
        cursor.close()
        
        print("[OK] Local Database Connected Successfully")
        print("[DB] Connection timeout: 30s, Session timeout: 8h")
        return db_connection
        
    except mysql.connector.Error as err:
        print(f"[ERROR] MySQL Connection Error: {err}")
        print(f"[ERROR] Error Code: {err.errno if hasattr(err, 'errno') else 'N/A'}")
        print(f"[HINT] Check your database credentials in .env file")
        print(f"[HINT] Verify database server is running and accessible")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error during database connection: {e}")
        import traceback
        traceback.print_exc()
        return None

def load_chat_data_from_json(file_path):
    """
    Load chat data from JSON file.
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        dict: Parsed JSON data or None if failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            chat_data = json.load(file)
        return chat_data
    except FileNotFoundError:
        print(f"[ERROR] Error: File '{file_path}' tidak ditemukan.")
        return None
    except json.JSONDecodeError:
        print(f"[ERROR] Error: Format JSON di '{file_path}' salah.")
        return None

def save_chat_to_database(cursor, db_connection, user_input, bot_response, source="local"):
    """
    Save chat interaction to database.
    
    Args:
        cursor: MySQL cursor
        db_connection: MySQL connection
        user_input: User's message
        bot_response: Bot's response
        source: Source of response (local, groq, etc.)
    """
    try:
        # Use column names matching migration schema
        sql = "INSERT INTO chat_logs (user_message, bot_response) VALUES (%s, %s)"
        value = (user_input, f"[{source}] {bot_response}")
        cursor.execute(sql, value)
        db_connection.commit()
    except mysql.connector.Error as err:
        print(f"[ERROR] Database Error: {err}")
    except Exception as e:
        print(f"[ERROR] Error: {e}")


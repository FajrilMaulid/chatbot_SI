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
    Initialize database connection.
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
                print(f"[...] Connecting to Railway MySQL: {host}")
                db_connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database,
                    port=int(port),
                    consume_results=True  # Automatically consume unread results
                )
                print("[OK] Railway Database Connected")
                return db_connection
        
        # Fallback to local/manual environment variables
        print("[...] Using local database configuration")
        db_connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'chatbot_si'),
            consume_results=True  # Automatically consume unread results
        )
        print("[OK] Local Database Connected")
        return db_connection
        
    except mysql.connector.Error as err:
        print(f"[ERROR] Database Error: {err}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
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


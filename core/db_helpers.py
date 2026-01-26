"""
Database Helper Functions
--------------------------
Helper functions for database connection validation and reconnection.
"""

import mysql.connector
from mysql.connector import Error

def ensure_connection(db_connection, cursor):
    """
    Ensure database connection is alive, reconnect if needed.
    
    Args:
        db_connection: MySQL connection object
        cursor: MySQL cursor object
    
    Returns:
        tuple: (connection, cursor, is_alive)
    """
    if db_connection is None or cursor is None:
        return db_connection, cursor, False
    
    try:
        # Ping to check if connection is alive
        db_connection.ping(reconnect=True, attempts=3, delay=1)
        return db_connection, cursor, True
    except Error as err:
        print(f"[WARNING] Connection lost: {err}")
        print("[INFO] Attempting to reconnect...")
        return db_connection, cursor, False

def safe_execute(cursor, db_connection, query, params=None):
    """
    Execute SQL query with connection validation.
    Auto-reconnects if connection is lost.
    
    Args:
        cursor: MySQL cursor
        db_connection: MySQL connection
        query: SQL query string
        params: Query parameters (tuple or dict)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate connection first
        db_connection.ping(reconnect=True, attempts=3, delay=1)
        
        # Execute query
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        return True
        
    except mysql.connector.errors.OperationalError as err:
        # Error 2013: Lost connection during query
        # Error 2006: MySQL server has gone away
        if err.errno in (2013, 2006):
            print(f"[ERROR] Connection lost during query (Error {err.errno})")
            print("[HINT] Try reconnecting to database")
            print("[HINT] Consider increasing wait_timeout in MySQL config")
        raise
        
    except Error as err:
        print(f"[ERROR] Database query failed: {err}")
        raise

def validate_connection_before_query(func):
    """
    Decorator to validate connection before executing database operations.
    
    Usage:
        @validate_connection_before_query
        def my_db_function(cursor, ...):
            cursor.execute(...)
    """
    def wrapper(*args, **kwargs):
        # Assume first arg after self (if exists) is cursor
        cursor = None
        db_connection = None
        
        for arg in args:
            if hasattr(arg, 'execute'):  # It's a cursor
                cursor = arg
                if hasattr(cursor, '_connection'):
                    db_connection = cursor._connection
                break
        
        if cursor and db_connection:
            try:
                db_connection.ping(reconnect=True, attempts=3, delay=1)
            except Error as err:
                print(f"[ERROR] Connection validation failed: {err}")
                raise
        
        return func(*args, **kwargs)
    
    return wrapper

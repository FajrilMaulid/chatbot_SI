"""
Admin API Module for Chatbot SI
---------------------------------
Handles all admin-related database operations and business logic.

Functions:
- verify_admin_login: Verify admin credentials
- get_all_chat_logs: Retrieve chat history with pagination
- get_all_intents_with_data: Get intents with patterns and responses
- create_intent, update_intent, delete_intent: Intent CRUD operations
- add_pattern, delete_pattern: Pattern management
- add_response, delete_response: Response management
"""

from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

def verify_admin_login(username, password, cursor):
    """
    Verify admin login credentials
    
    Args:
        username: Admin username
        password: Plain text password
        cursor: MySQL cursor
    
    Returns:
        dict: Admin user data if valid, None otherwise
    """
    try:
        # CRITICAL: Validate connection before query
        if hasattr(cursor, '_connection'):
            cursor._connection.ping(reconnect=True, attempts=3, delay=1)
            print("[DB] Connection validated before admin login query")
        
        cursor.execute(
            "SELECT id, username, password_hash FROM admin_users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], password):
            return {
                'id': user[0],
                'username': user[1]
            }
        return None
        
    except Exception as e:
        print(f"[ERROR] Error in verify_admin_login: {e}")
        import traceback
        traceback.print_exc()
        raise  # Re-raise to be caught by admin_routes error handler

def update_last_login(user_id, cursor, db_connection):
    """Update last login timestamp for admin user"""
    cursor.execute(
        "UPDATE admin_users SET last_login = NOW() WHERE id = %s",
        (user_id,)
    )
    db_connection.commit()

def get_all_chat_logs(cursor, limit=50, offset=0, search=None):
    """
    Get all chat logs with pagination
    
    Args:
        cursor: MySQL cursor
        limit: Number of records per page
        offset: Offset for pagination
        search: Optional search term for filtering
    
    Returns:
        dict: {'logs': [...], 'total': int}
    """
    # Build query
    if search:
        query = """
            SELECT id, session_id, user_message, bot_response, detected_intent, 
                   confidence, created_at 
            FROM chat_logs 
            WHERE user_message LIKE %s OR bot_response LIKE %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        search_term = f"%{search}%"
        cursor.execute(query, (search_term, search_term, limit, offset))
        
        # IMPORTANT: Fetch results BEFORE executing COUNT query
        rows = cursor.fetchall()
        
        # Get total count
        cursor.execute(
            "SELECT COUNT(*) FROM chat_logs WHERE user_message LIKE %s OR bot_response LIKE %s",
            (search_term, search_term)
        )
    else:
        query = """
            SELECT id, session_id, user_message, bot_response, detected_intent, 
                   confidence, created_at 
            FROM chat_logs 
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, offset))
        
        # IMPORTANT: Fetch results BEFORE executing COUNT query
        rows = cursor.fetchall()
        
        # Get total count
        cursor.execute("SELECT COUNT(*) FROM chat_logs")
    
    total = cursor.fetchone()[0]
    
    # Format results
    logs = []
    for row in rows:
        logs.append({
            'id': row[0],
            'session_id': row[1],
            'user_message': row[2],
            'bot_response': row[3],
            'detected_intent': row[4],
            'confidence': row[5],
            'created_at': row[6].strftime('%Y-%m-%d %H:%M:%S') if row[6] else None
        })
    
    return {'logs': logs, 'total': total}

def get_all_intents_with_data(cursor):
    """
    Get all intents with their patterns and responses
    
    Returns:
        list: List of intents with nested patterns and responses
    """
    # Get all intents
    cursor.execute("SELECT id, intent_name, tag FROM intents ORDER BY intent_name")
    intents = []
    
    for row in cursor.fetchall():
        intent_id = row[0]
        
        # Get patterns for this intent
        cursor.execute(
            "SELECT id, pattern_text FROM patterns WHERE intent_id = %s ORDER BY id",
            (intent_id,)
        )
        patterns = [{'id': p[0], 'text': p[1]} for p in cursor.fetchall()]
        
        # Get responses for this intent
        cursor.execute(
            "SELECT id, response_text FROM responses WHERE intent_id = %s ORDER BY id",
            (intent_id,)
        )
        responses = [{'id': r[0], 'text': r[1]} for r in cursor.fetchall()]
        
        intents.append({
            'id': intent_id,
            'intent_name': row[1],
            'tag': row[2],
            'patterns': patterns,
            'responses': responses
        })
    
    return intents

def create_intent(cursor, db_connection, intent_name, tag=None):
    """
    Create a new intent
    
    Args:
        cursor: MySQL cursor
        db_connection: MySQL connection
        intent_name: Name of the intent
        tag: Optional tag for categorization
    
    Returns:
        int: ID of created intent
    """
    if not tag:
        tag = intent_name
    
    cursor.execute(
        "INSERT INTO intents (intent_name, tag) VALUES (%s, %s)",
        (intent_name, tag)
    )
    db_connection.commit()
    return cursor.lastrowid

def update_intent(cursor, db_connection, intent_id, intent_name, tag):
    """
    Update an existing intent
    
    Args:
        cursor: MySQL cursor
        db_connection: MySQL connection
        intent_id: ID of intent to update
        intent_name: New intent name
        tag: New tag
    
    Returns:
        bool: True if successful
    """
    cursor.execute(
        "UPDATE intents SET intent_name = %s, tag = %s WHERE id = %s",
        (intent_name, tag, intent_id)
    )
    db_connection.commit()
    return cursor.rowcount > 0

def delete_intent(cursor, db_connection, intent_id):
    """
    Delete an intent (cascade deletes patterns and responses)
    
    Args:
        cursor: MySQL cursor
        db_connection: MySQL connection
        intent_id: ID of intent to delete
    
    Returns:
        bool: True if successful
    """
    cursor.execute("DELETE FROM intents WHERE id = %s", (intent_id,))
    db_connection.commit()
    return cursor.rowcount > 0

def add_pattern(cursor, db_connection, intent_id, pattern_text):
    """
    Add a pattern to an intent
    
    Args:
        cursor: MySQL cursor
        db_connection: MySQL connection
        intent_id: ID of intent
        pattern_text: Pattern text to add
    
    Returns:
        int: ID of created pattern
    """
    cursor.execute(
        "INSERT INTO patterns (intent_id, pattern_text) VALUES (%s, %s)",
        (intent_id, pattern_text)
    )
    db_connection.commit()
    return cursor.lastrowid

def delete_pattern(cursor, db_connection, pattern_id):
    """
    Delete a pattern
    
    Args:
        cursor: MySQL cursor
        db_connection: MySQL connection
        pattern_id: ID of pattern to delete
    
    Returns:
        bool: True if successful
    """
    cursor.execute("DELETE FROM patterns WHERE id = %s", (pattern_id,))
    db_connection.commit()
    return cursor.rowcount > 0

def add_response(cursor, db_connection, intent_id, response_text):
    """
    Add a response to an intent
    
    Args:
        cursor: MySQL cursor
        db_connection: MySQL connection
        intent_id: ID of intent
        response_text: Response text to add
    
    Returns:
        int: ID of created response
    """
    cursor.execute(
        "INSERT INTO responses (intent_id, response_text) VALUES (%s, %s)",
        (intent_id, response_text)
    )
    db_connection.commit()
    return cursor.lastrowid

def delete_response(cursor, db_connection, response_id):
    """
    Delete a response
    
    Args:
        cursor: MySQL cursor
        db_connection: MySQL connection
        response_id: ID of response to delete
    
    Returns:
        bool: True if successful
    """
    cursor.execute("DELETE FROM responses WHERE id = %s", (response_id,))
    db_connection.commit()
    return cursor.rowcount > 0

def get_stats(cursor):
    """
    Get dashboard statistics
    
    Returns:
        dict: Statistics data
    """
    stats = {}
    
    # Total conversations
    cursor.execute("SELECT COUNT(*) FROM chat_logs")
    stats['total_conversations'] = cursor.fetchone()[0]
    
    # Total intents
    cursor.execute("SELECT COUNT(*) FROM intents")
    stats['total_intents'] = cursor.fetchone()[0]
    
    # Total patterns
    cursor.execute("SELECT COUNT(*) FROM patterns")
    stats['total_patterns'] = cursor.fetchone()[0]
    
    # Total responses
    cursor.execute("SELECT COUNT(*) FROM responses")
    stats['total_responses'] = cursor.fetchone()[0]
    
    # Today's conversations
    cursor.execute("SELECT COUNT(*) FROM chat_logs WHERE DATE(created_at) = CURDATE()")
    stats['today_conversations'] = cursor.fetchone()[0]
    
    return stats

def log_chat(cursor, db_connection, session_id, user_message, bot_response, detected_intent=None, confidence=None):
    """
    Log a chat interaction
    
    Args:
        cursor: MySQL cursor
        db_connection: MySQL connection
        session_id: User session ID
        user_message: User's message
        bot_response: Bot's response
        detected_intent: Detected intent name
        confidence: Confidence score
    """
    cursor.execute(
        """INSERT INTO chat_logs 
           (session_id, user_message, bot_response, detected_intent, confidence) 
           VALUES (%s, %s, %s, %s, %s)""",
        (session_id, user_message, bot_response, detected_intent, confidence)
    )
    db_connection.commit()

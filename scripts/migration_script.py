"""
Database Migration Script for Chatbot SI Admin Panel
------------------------------------------------------
Creates necessary MySQL tables and migrates data from intents_ml.json to database.

Tables created:
- admin_users: Store admin credentials
- intents: Store intent information
- patterns: Store patterns for each intent
- responses: Store responses for each intent
- chat_logs: Store conversation history

Usage:
    python migration_script.py
"""

import mysql.connector
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
def get_db_config():
    """Get database configuration from environment variables"""
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Parse Railway DATABASE_URL format: mysql://user:password@host:port/database
        import re
        match = re.match(r'mysql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', database_url)
        if match:
            return {
                'user': match.group(1),
                'password': match.group(2),
                'host': match.group(3),
                'port': int(match.group(4)),
                'database': match.group(5)
            }
    
    # Fallback to individual environment variables
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'chatbot_si'),
        'port': int(os.getenv('DB_PORT', 3306))
    }

def create_tables(cursor):
    """Create all necessary tables"""
    
    print("Creating tables...")
    
    # Admin users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL,
            INDEX idx_username (username)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("[+] Table 'admin_users' created/verified")
    
    # Intents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            intent_name VARCHAR(100) UNIQUE NOT NULL,
            tag VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_intent_name (intent_name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("[+] Table 'intents' created/verified")
    
    # Patterns table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patterns (
            id INT AUTO_INCREMENT PRIMARY KEY,
            intent_id INT NOT NULL,
            pattern_text VARCHAR(500) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE,
            INDEX idx_intent_id (intent_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("[+] Table 'patterns' created/verified")
    
    # Responses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            intent_id INT NOT NULL,
            response_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE,
            INDEX idx_intent_id (intent_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("[+] Table 'responses' created/verified")
    
    # Chat logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            session_id VARCHAR(100),
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            detected_intent VARCHAR(100),
            confidence FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_session_id (session_id),
            INDEX idx_created_at (created_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("[+] Table 'chat_logs' created/verified")
    
    print("\n[OK] All tables created successfully!\n")

def create_default_admin(cursor, db_connection):
    """Create default admin user if not exists"""
    
    print("Creating default admin user...")
    
    # Check if admin already exists
    cursor.execute("SELECT id FROM admin_users WHERE username = 'admin'")
    if cursor.fetchone():
        print("[!] Admin user already exists, skipping...")
        return
    
    # Create admin with hashed password
    password_hash = generate_password_hash('admin123')
    cursor.execute(
        "INSERT INTO admin_users (username, password_hash) VALUES (%s, %s)",
        ('admin', password_hash)
    )
    db_connection.commit()
    
    print("[+] Default admin user created")
    print("  Username: admin")
    print("  Password: admin123")
    print("  [!] PLEASE CHANGE THIS PASSWORD AFTER FIRST LOGIN!\n")

def migrate_json_to_database(cursor, db_connection, json_file_path):
    """Migrate data from intents_ml.json to database"""
    
    print(f"Migrating data from {json_file_path}...")
    
    # Check if data already migrated
    cursor.execute("SELECT COUNT(*) FROM intents")
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"[!] Database already contains {count} intents, skipping migration...")
        return
    
    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    intents_data = data.get('intents', [])
    print(f"Found {len(intents_data)} intents to migrate...")
    
    migrated_count = 0
    for intent_data in intents_data:
        intent_name = intent_data.get('intent')
        patterns = intent_data.get('patterns', [])
        responses = intent_data.get('responses', [])
        
        if not intent_name:
            continue
        
        # Insert intent
        cursor.execute(
            "INSERT INTO intents (intent_name, tag) VALUES (%s, %s)",
            (intent_name, intent_name)
        )
        intent_id = cursor.lastrowid
        
        # Insert patterns
        for pattern in patterns:
            cursor.execute(
                "INSERT INTO patterns (intent_id, pattern_text) VALUES (%s, %s)",
                (intent_id, pattern)
            )
        
        # Insert responses
        for response in responses:
            cursor.execute(
                "INSERT INTO responses (intent_id, response_text) VALUES (%s, %s)",
                (intent_id, response)
            )
        
        migrated_count += 1
        print(f"  [+] Migrated intent '{intent_name}' with {len(patterns)} patterns and {len(responses)} responses")
    
    db_connection.commit()
    print(f"\n[OK] Successfully migrated {migrated_count} intents to database!\n")

def verify_migration(cursor):
    """Verify that migration was successful"""
    
    print("Verifying migration...")
    
    cursor.execute("SELECT COUNT(*) FROM intents")
    intent_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM patterns")
    pattern_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM responses")
    response_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM admin_users")
    admin_count = cursor.fetchone()[0]
    
    print(f"  [+] Intents: {intent_count}")
    print(f"  [+] Patterns: {pattern_count}")
    print(f"  [+] Responses: {response_count}")
    print(f"  [+] Admin users: {admin_count}")
    print("\n[OK] Migration verification complete!\n")

def main():
    """Main migration function"""
    
    print("\n" + "="*60)
    print("Chatbot SI - Database Migration Script")
    print("="*60 + "\n")
    
    try:
        # Get database configuration
        db_config = get_db_config()
        print(f"Connecting to database: {db_config['host']}:{db_config['port']}/{db_config['database']}")
        
        # Connect to database
        db_connection = mysql.connector.connect(**db_config)
        cursor = db_connection.cursor()
        print("[+] Database connection successful\n")
        
        # Create tables
        create_tables(cursor)
        
        # Create default admin user
        create_default_admin(cursor, db_connection)
        
        # Migrate JSON data
        json_file_path = os.path.join('data', 'intents_ml.json')
        if os.path.exists(json_file_path):
            migrate_json_to_database(cursor, db_connection, json_file_path)
        else:
            print(f"[!] JSON file not found at {json_file_path}, skipping data migration...")
        
        # Verify migration
        verify_migration(cursor)
        
        # Close connection
        cursor.close()
        db_connection.close()
        
        print("="*60)
        print("[OK] Migration completed successfully!")
        print("="*60 + "\n")
        print("Next steps:")
        print("1. Run the Flask app: python app.py")
        print("2. Login to admin panel at: http://localhost:5000/admin.html")
        print("3. Username: admin, Password: admin123")
        print("4. IMPORTANT: Change the default password immediately!\n")
        
    except mysql.connector.Error as e:
        print(f"\n[ERROR] Database error: {e}")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database credentials in .env file are correct")
        print("3. Database exists (create it if needed)")
        return 1
    
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

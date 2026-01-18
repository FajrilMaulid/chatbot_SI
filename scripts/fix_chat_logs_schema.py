"""
Fix Chat Logs Table Schema
---------------------------
Updates existing chat_logs table to match new schema
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    print("\n" + "="*60)
    print("Fixing chat_logs table schema...")
    print("="*60 + "\n")
    
    # Connect to database
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', 'chatbot_si')
    )
    cursor = conn.cursor()
    
    print("Checking current table structure...")
    cursor.execute("DESCRIBE chat_logs")
    columns = [row[0] for row in cursor.fetchall()]
    print(f"Current columns: {', '.join(columns)}\n")
    
    # Check if old column exists
    if 'user_input' in columns and 'user_message' not in columns:
        print("[!] Found old schema with 'user_input' column")
        print("[...] Renaming 'user_input' to 'user_message'...")
        
        cursor.execute("ALTER TABLE chat_logs CHANGE COLUMN user_input user_message TEXT NOT NULL")
        conn.commit()
        print("[OK] Column renamed successfully!\n")
        
    elif 'user_message' in columns:
        print("[OK] Table already has correct schema (user_message column exists)\n")
    
    # Also add missing columns if needed
    cursor.execute("DESCRIBE chat_logs")
    columns_dict = {row[0]: row[1] for row in cursor.fetchall()}
    
    updates_needed = []
    
    if 'session_id' not in columns_dict:
        updates_needed.append("ADD COLUMN session_id VARCHAR(100) AFTER id")
    
    if 'detected_intent' not in columns_dict:
        updates_needed.append("ADD COLUMN detected_intent VARCHAR(100) AFTER bot_response")
    
    if 'confidence' not in columns_dict:
        updates_needed.append("ADD COLUMN confidence FLOAT AFTER detected_intent")
    
    if updates_needed:
        print("[...] Adding missing columns...")
        for update in updates_needed:
            cursor.execute(f"ALTER TABLE chat_logs {update}")
            print(f"  [+] {update}")
        conn.commit()
        print("[OK] Missing columns added!\n")
    
    # Verify final structure
    print("Verifying final table structure...")
    cursor.execute("DESCRIBE chat_logs")
    print("\nFinal table structure:")
    print("-" * 60)
    for row in cursor.fetchall():
        print(f"  {row[0]:<20} {row[1]:<15} {row[2]}")
    print("-" * 60)
    
    cursor.close()
    conn.close()
    
    print("\n" + "="*60)
    print("[OK] Schema fix completed successfully!")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"\n[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()

"""
Add Sample Chat Logs
---------------------
Script untuk menambahkan sample chat logs ke database untuk testing admin panel
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    # Connect to database
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', 'chatbot_si')
    )
    cursor = conn.cursor()
    
    # Sample chat data
    sample_chats = [
        ("Apa itu sistem informasi?", "[data-grounded] Sistem Informasi adalah program studi yang mempelajari tentang teknologi informasi dan manajemen bisnis.", "test-session-1"),
        ("Berapa biaya kuliah SI?", "[data-grounded] Biaya kuliah SI berkisar antara Rp 10-15 juta per semester.", "test-session-1"),
        ("Siapa kaprodi SI?", "[data-grounded] Kaprodi SI adalah Dr. John Doe, M.Kom", "test-session-2"),
        ("Prospek kerja lulusan SI?", "[data-grounded] Lulusan SI dapat bekerja sebagai: Data Analyst, System Analyst, IT Consultant, Software Engineer, dll.", "test-session-2"),
        ("Mata kuliah apa saja yang dipelajari?", "[data-grounded] Mata kuliah SI antara lain: Database, Pemrograman, Analisis Sistem, dll.", "test-session-3"),
    ]
    
    # Insert sample data
    print("Adding sample chat logs...")
    for user_msg, bot_msg, session in sample_chats:
        cursor.execute(
            "INSERT INTO chat_logs (user_message, bot_response, session_id) VALUES (%s, %s, %s)",
            (user_msg, bot_msg, session)
        )
        print(f"  [+] Added: {user_msg[:50]}...")
    
    conn.commit()
    
    # Check total logs
    cursor.execute('SELECT COUNT(*) FROM chat_logs')
    total = cursor.fetchone()[0]
    print(f"\n[OK] Total chat logs in database: {total}")
    
    cursor.close()
    conn.close()
    print("\n[OK] Sample data berhasil ditambahkan!")
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()

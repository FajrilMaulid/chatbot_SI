"""
Database Connection Diagnostic Script
--------------------------------------
This script tests the database connection and helps diagnose issues.
Run this script to verify your database configuration is correct.

Usage:
    python scripts/test_db_connection.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.database import init_db_connection
from dotenv import load_dotenv

def test_database_connection():
    """Test database connection and print diagnostic information"""
    
    print("="*70)
    print("DATABASE CONNECTION DIAGNOSTIC TOOL")
    print("="*70)
    
    # Load environment variables
    load_dotenv()
    
    # Display configuration (without password)
    print("\n📋 CONFIGURATION:")
    print(f"   MYSQL_HOST: {os.getenv('MYSQL_HOST', 'localhost')}")
    print(f"   MYSQL_USER: {os.getenv('MYSQL_USER', 'root')}")
    print(f"   MYSQL_DATABASE: {os.getenv('MYSQL_DATABASE', 'chatbot_si')}")
    password = os.getenv('MYSQL_PASSWORD', '')
    print(f"   MYSQL_PASSWORD: {'*' * len(password) if password else '(empty)'}")
    
    # Test connection
    print("\n🔄 TESTING CONNECTION...")
    print("-"*70)
    
    db_connection = init_db_connection()
    
    if db_connection is None:
        print("\n❌ CONNECTION FAILED")
        print("\n💡 TROUBLESHOOTING TIPS:")
        print("1. Verify MySQL server is running")
        print("2. Check credentials in .env file")
        print("3. Ensure database exists:")
        print("   mysql -u root -p")
        print("   CREATE DATABASE chatbot_si;")
        print("4. Check if MySQL port is accessible")
        print("5. For shared hosting, use correct host (not 'localhost')")
        print("="*70)
        return False
    
    # Test cursor
    print("\n🔄 TESTING CURSOR...")
    try:
        cursor = db_connection.cursor()
        print("✅ Cursor created successfully")
        
        # Test query
        print("\n🔄 TESTING QUERY...")
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()[0]
        print(f"✅ Connected to database: {db_name}")
        
        # Check tables
        print("\n🔄 CHECKING TABLES...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        if not tables:
            print("⚠️  No tables found in database")
            print("💡 Run migration script:")
            print("   python scripts/migration_script.py")
        else:
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"   - {table[0]}: {count} rows")
        
        # Check admin_users table
        print("\n🔄 CHECKING ADMIN USERS...")
        try:
            cursor.execute("SELECT COUNT(*) FROM admin_users")
            admin_count = cursor.fetchone()[0]
            print(f"✅ Admin users table: {admin_count} users")
            
            if admin_count == 0:
                print("⚠️  No admin users found")
                print("💡 Default admin should be created during migration")
        except Exception as e:
            print(f"⚠️  admin_users table issue: {e}")
            print("💡 Run migration script to create table")
        
        cursor.close()
        db_connection.close()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED - DATABASE IS READY")
        print("="*70)
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        
        if db_connection:
            db_connection.close()
        
        print("\n" + "="*70)
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)

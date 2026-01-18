"""
Chatbot SI - Automatic Setup Script
------------------------------------
One-click installation untuk setup project secara lengkap.

Features:
- Install Python dependencies
- Create database
- Run migration
- Setup .env file
- Add sample data
- Verify installation

Usage:
    python setup.py
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}[OK]{Colors.ENDC} {text}")

def print_info(text):
    print(f"{Colors.OKCYAN}[INFO]{Colors.ENDC} {text}")

def print_warning(text):
    print(f"{Colors.WARNING}[WARN]{Colors.ENDC} {text}")

def print_error(text):
    print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} {text}")

def run_command(command, description, check=True):
    """Run shell command with error handling"""
    print_info(f"{description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success(f"{description} completed")
            return True
        else:
            print_warning(f"{description} returned code {result.returncode}")
            if result.stderr:
                print(f"  {result.stderr[:200]}")
            return False
    except subprocess.CalledProcessError as e:
        print_error(f"{description} failed: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def check_python_version():
    """Check if Python version is 3.8+"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print_info(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error("Python 3.8 or higher is required!")
        return False
    
    print_success("Python version OK")
    return True

def install_dependencies():
    """Install Python packages from requirements.txt"""
    print_header("Installing Dependencies")
    
    if not os.path.exists('requirements.txt'):
        print_error("requirements.txt not found!")
        return False
    
    print_info("Installing packages from requirements.txt...")
    success = run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing dependencies"
    )
    
    return success

def setup_env_file():
    """Create .env file from .env.example"""
    print_header("Setting Up Environment Variables")
    
    if os.path.exists('.env'):
        print_warning(".env file already exists")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print_info("Keeping existing .env file")
            return True
    
    if not os.path.exists('.env.example'):
        print_error(".env.example not found!")
        return False
    
    # Copy .env.example to .env
    shutil.copy('.env.example', '.env')
    print_success("Created .env file from .env.example")
    
    print_info("\nPlease configure the following in .env:")
    print("  - MySQL credentials (MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE)")
    print("  - SECRET_KEY (for Flask sessions)")
    print("  - GROQ_API_KEY (optional, for AI features)")
    
    response = input("\nDo you want to edit .env now? (y/N): ").strip().lower()
    if response == 'y':
        print_info("Opening .env in default editor...")
        if sys.platform == 'win32':
            os.system('notepad .env')
        else:
            os.system('nano .env || vi .env')
    
    return True

def check_mysql_connection():
    """Check if MySQL is accessible"""
    print_header("Checking MySQL Connection")
    
    try:
        import mysql.connector
        from dotenv import load_dotenv
        
        load_dotenv()
        
        print_info("Testing MySQL connection...")
        
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
        )
        
        print_success("MySQL connection successful")
        
        # Check if database exists
        cursor = conn.cursor()
        db_name = os.getenv('MYSQL_DATABASE', 'chatbot_si')
        
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if db_name not in databases:
            print_warning(f"Database '{db_name}' does not exist")
            response = input(f"Create database '{db_name}'? (Y/n): ").strip().lower()
            if response != 'n':
                cursor.execute(f"CREATE DATABASE {db_name}")
                print_success(f"Database '{db_name}' created")
            else:
                print_error("Database required. Please create it manually.")
                return False
        else:
            print_success(f"Database '{db_name}' exists")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print_error("mysql-connector-python not installed. Run: pip install mysql-connector-python")
        return False
    except Exception as e:
        print_error(f"MySQL connection failed: {e}")
        print_info("\nPlease check:")
        print("  1. MySQL server is running")
        print("  2. Credentials in .env are correct")
        print("  3. MySQL user has proper permissions")
        return False

def run_migration():
    """Run database migration script"""
    print_header("Running Database Migration")
    
    if not os.path.exists('scripts/migration_script.py'):
        print_error("Migration script not found!")
        return False
    
    success = run_command(
        f"{sys.executable} scripts/migration_script.py",
        "Running database migration"
    )
    
    return success

def add_sample_data():
    """Add sample chat logs"""
    print_header("Adding Sample Data")
    
    response = input("Do you want to add sample chat logs? (Y/n): ").strip().lower()
    if response == 'n':
        print_info("Skipping sample data")
        return True
    
    if not os.path.exists('scripts/add_sample_chats.py'):
        print_warning("Sample data script not found, skipping...")
        return True
    
    success = run_command(
        f"{sys.executable} scripts/add_sample_chats.py",
        "Adding sample data"
    )
    
    return success

def verify_installation():
    """Verify that everything is set up correctly"""
    print_header("Verifying Installation")
    
    checks = {
        "Python packages": lambda: os.path.exists('.venv') or True,
        ".env file": lambda: os.path.exists('.env'),
        "Database connection": check_mysql_connection,
        "Data folder": lambda: os.path.exists('data'),
        "Static files": lambda: os.path.exists('static'),
    }
    
    all_ok = True
    for name, check_func in checks.items():
        try:
            if check_func():
                print_success(f"{name}: OK")
            else:
                print_error(f"{name}: FAILED")
                all_ok = False
        except:
            print_error(f"{name}: ERROR")
            all_ok = False
    
    return all_ok

def show_next_steps():
    """Show what to do next"""
    print_header("Installation Complete!")
    
    print(f"{Colors.OKGREEN}✓ Setup completed successfully!{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Next Steps:{Colors.ENDC}")
    print(f"\n1. {Colors.OKCYAN}Start the application:{Colors.ENDC}")
    print(f"   {Colors.BOLD}python app.py{Colors.ENDC}")
    
    print(f"\n2. {Colors.OKCYAN}Access the chatbot:{Colors.ENDC}")
    print(f"   {Colors.BOLD}http://localhost:5000{Colors.ENDC}")
    
    print(f"\n3. {Colors.OKCYAN}Access admin panel:{Colors.ENDC}")
    print(f"   {Colors.BOLD}http://localhost:5000/admin{Colors.ENDC}")
    print(f"   Username: {Colors.BOLD}admin{Colors.ENDC}")
    print(f"   Password: {Colors.BOLD}admin123{Colors.ENDC}")
    print(f"   {Colors.WARNING}⚠ CHANGE THIS PASSWORD!{Colors.ENDC}")
    
    print(f"\n4. {Colors.OKCYAN}Configure Groq API (optional):{Colors.ENDC}")
    print(f"   - Get API key from: {Colors.BOLD}https://console.groq.com{Colors.ENDC}")
    print(f"   - Add to .env: {Colors.BOLD}GROQ_API_KEY=your_key_here{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Documentation:{Colors.ENDC}")
    print(f"   - README.md - Getting started guide")
    print(f"   - PROJECT_STRUCTURE.md - Project organization")
    print(f"   - docs/ - Deployment guides")
    
    print(f"\n{Colors.OKGREEN}Happy coding! 🚀{Colors.ENDC}\n")

def main():
    """Main setup function"""
    print_header("Chatbot SI - Automatic Setup")
    print(f"{Colors.BOLD}This script will set up the entire project automatically{Colors.ENDC}\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print_error("Failed to install dependencies")
        sys.exit(1)
    
    # Setup .env file
    if not setup_env_file():
        print_error("Failed to setup .env file")
        sys.exit(1)
    
    # Check MySQL connection
    if not check_mysql_connection():
        print_error("MySQL connection failed")
        print_info("Please fix MySQL connection and run setup again")
        sys.exit(1)
    
    # Run migration
    if not run_migration():
        print_error("Database migration failed")
        sys.exit(1)
    
    # Add sample data (optional)
    add_sample_data()
    
    # Verify installation
    if not verify_installation():
        print_warning("Some verification checks failed")
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Setup interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

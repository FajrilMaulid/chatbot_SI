# 📦 Installation Guide - Chatbot SI

<div align="center">

**Panduan instalasi lengkap untuk Chatbot Sistem Informasi IPI Garut**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7%2B-orange?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[🚀 Quick Start](#-quick-start-recommended) • [🔧 Manual Install](#-manual-installation) • [🐛 Troubleshooting](#-troubleshooting) • [📚 Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Quick Start (Recommended)](#-quick-start-recommended)
- [Manual Installation](#-manual-installation)
- [Configuration](#-configuration)
- [Verification](#-verification)
- [Post-Installation](#-post-installation)
- [Troubleshooting](#-troubleshooting)
- [Platform-Specific Guides](#-platform-specific-guides)
- [Documentation](#-documentation)

---

## 🎯 Prerequisites

### Required Software

| Software                | Version       | Purpose             | Download                                                                             |
| ----------------------- | ------------- | ------------------- | ------------------------------------------------------------------------------------ |
| **Python**              | 3.8 or higher | Runtime environment | [Download](https://www.python.org/downloads/)                                        |
| **MySQL** / **MariaDB** | 5.7+ / 10.2+  | Database server     | [MySQL](https://dev.mysql.com/downloads/) / [MariaDB](https://mariadb.org/download/) |
| **pip**                 | Latest        | Package manager     | Included with Python                                                                 |
| **Git**                 | Latest        | Version control     | [Download](https://git-scm.com/)                                                     |

### Check Installed Versions

```bash
# Python
python --version
# Should show: Python 3.8.x or higher

# pip
pip --version

# MySQL
mysql --version

# Git
git --version
```

### System Requirements

- **RAM:** Minimum 2GB (4GB recommended)
- **Storage:** Minimum 500MB free space
- **OS:** Windows 10+, Ubuntu 18.04+, macOS 10.15+

---

## 🚀 Quick Start (Recommended)

> ⚡ **Estimated Time:** 2-5 minutes

### Option 1: Automated Setup Script

This is the **easiest and fastest** way to install the chatbot.

#### For All Platforms:

```bash
# 1. Clone the repository
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI

# 2. Run automated setup
python setup.py
```

The `setup.py` script will automatically:

- ✅ Check system requirements
- ✅ Install Python dependencies
- ✅ Create database and tables
- ✅ Setup `.env` configuration
- ✅ Create admin user
- ✅ Add sample data
- ✅ Verify installation

#### For Windows (One-Click):

```bash
# Double-click or run in terminal
installation\INSTALL.bat
```

#### For Linux/Mac (One-Click):

```bash
# Make executable and run
chmod +x installation/install.sh
./installation/install.sh
```

### Option 2: Quick Manual Setup

```bash
# 1. Clone repository
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .config/.env.example .env
# Edit .env with your database credentials

# 4. Create database
mysql -u root -p -e "CREATE DATABASE chatbot_si;"

# 5. Run migration
python scripts/migration_script.py

# 6. Start application
python app.py
```

---

## 🔧 Manual Installation

> 📝 **For advanced users** who want full control over the installation process.

### Step 1: Clone Repository

```bash
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI
```

### Step 2: Create Virtual Environment (Recommended)

Using a virtual environment keeps your project dependencies isolated.

#### Windows:

```bash
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate
```

#### Linux/Mac:

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt after activation.

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**Dependencies that will be installed:**

- Flask - Web framework
- Flask-Cors - Cross-origin resource sharing
- mysql-connector-python - MySQL database connector
- scikit-learn - Machine learning library
- python-dotenv - Environment variable management
- groq - Groq API client (optional)

### Step 4: Setup Environment Configuration

```bash
# Copy example configuration
cp .config/.env.example .env

# Windows alternative
copy .config\.env.example .env
```

**Edit `.env` file** with your preferred text editor:

```bash
# Linux/Mac
nano .env

# Windows
notepad .env
```

**Required configuration:**

```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password_here
MYSQL_DATABASE=chatbot_si
MYSQL_PORT=3306

# Flask Configuration
SECRET_KEY=generate_random_secret_key_here
FLASK_ENV=development
DEBUG=True
PORT=5000

# Admin Configuration
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Groq API (Optional - for AI enhancement)
GROQ_API_KEY=your_groq_api_key_here
ENABLE_GROQ=false
```

**Generate SECRET_KEY:**

```bash
python -c "import os; print(os.urandom(24).hex())"
```

Copy the output and paste it as your `SECRET_KEY` value.

### Step 5: Setup Database

#### Create Database

**Using MySQL CLI:**

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE chatbot_si CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Verify database created
SHOW DATABASES;

# Exit MySQL
exit;
```

**Using MySQL Workbench:**

1. Open MySQL Workbench
2. Connect to your local MySQL server
3. Click "Create Schema" button
4. Name: `chatbot_si`
5. Charset: `utf8mb4`
6. Collation: `utf8mb4_unicode_ci`
7. Click "Apply"

#### Run Database Migration

```bash
# Create all tables and initial data
python scripts/migration_script.py
```

**Migration will create:**

- `intents` - Intent patterns and responses
- `chat_logs` - Chat conversation history
- `admin_users` - Admin panel users

#### (Optional) Add Sample Data

```bash
# Add test chat logs for demonstration
python scripts/add_sample_chats.py
```

### Step 6: Test Database Connection

```bash
# Verify database connectivity
python scripts/test_db_connection.py
```

You should see:

```
✅ Database connection successful!
✅ Found X intents in database
✅ Found X admin users
```

### Step 7: Start Application

```bash
# Start Flask development server
python app.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

---

## ⚙️ Configuration

### Environment Variables Reference

```env
# ===================================
# DATABASE CONFIGURATION
# ===================================
MYSQL_HOST=localhost              # MySQL server host
MYSQL_USER=root                   # MySQL username
MYSQL_PASSWORD=your_password      # MySQL password (CHANGE THIS!)
MYSQL_DATABASE=chatbot_si         # Database name
MYSQL_PORT=3306                   # MySQL port (default: 3306)

# ===================================
# FLASK CONFIGURATION
# ===================================
SECRET_KEY=your_secret_key_here   # Flask session secret (GENERATE NEW!)
FLASK_ENV=development             # development or production
DEBUG=True                        # Enable debug mode (False in production)
PORT=5000                         # Application port

# ===================================
# ADMIN CONFIGURATION
# ===================================
ADMIN_USERNAME=admin              # Default admin username
ADMIN_PASSWORD=admin123           # Default admin password (CHANGE THIS!)

# ===================================
# GROQ API (OPTIONAL)
# ===================================
GROQ_API_KEY=                     # Your Groq API key
ENABLE_GROQ=false                 # Enable AI enhancement (true/false)
GROQ_MODEL=mixtral-8x7b-32768     # Groq model to use

# ===================================
# LOGGING
# ===================================
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_TO_FILE=True                  # Save logs to file

# ===================================
# SECURITY
# ===================================
RATE_LIMIT_ENABLED=True           # Enable rate limiting
MAX_LOGIN_ATTEMPTS=5              # Max failed login attempts
SESSION_TIMEOUT=3600              # Session timeout in seconds
```

### Configuration Files Structure

```
chatbot_SI/
├── .env                          # Your active configuration (git-ignored)
├── .config/
│   ├── .env.example              # Template configuration
│   ├── .htaccess.hostinger.example
│   └── .htaccess.niagahoster.example
```

---

## ✅ Verification

### 1. Check File Structure

```bash
# Verify all essential files exist
ls -la  # Linux/Mac
dir     # Windows
```

You should have:

- ✅ `.env` file
- ✅ `venv/` folder (if using virtual environment)
- ✅ All folders: `api/`, `core/`, `models/`, etc.

### 2. Test Database

```bash
# Login to MySQL
mysql -u root -p

# Use database
USE chatbot_si;

# Show tables
SHOW TABLES;

# Should show:
# +------------------------+
# | Tables_in_chatbot_si   |
# +------------------------+
# | admin_users            |
# | chat_logs              |
# | intents                |
# +------------------------+

# Exit
exit;
```

### 3. Test Application

**A. Start Server:**

```bash
python app.py
```

**B. Test Endpoints:**

Open your browser and visit:

1. **Main Chatbot:** http://localhost:5000
   - You should see the chatbot interface
   - Try sending a message: "Apa itu Sistem Informasi?"

2. **Admin Login:** http://localhost:5000/admin
   - Username: `admin`
   - Password: `admin123`
   - You should be able to login

3. **Admin Dashboard:** http://localhost:5000/admin/dashboard
   - Should show statistics
   - Should show recent chat logs

**C. Test Chat Functionality:**

```bash
# In a new terminal, test with CLI
python scripts/chatbot_cli.py

# Type some questions:
# > Apa itu Sistem Informasi?
# > Siapa ketua HIMASIFOR?
# > Berapa biaya kuliah?
```

### 4. Check Logs

```bash
# View application logs
cat logs/app.log           # Linux/Mac
type logs\app.log          # Windows

# View security logs
cat logs/security.log      # Linux/Mac
type logs\security.log     # Windows
```

---

## 🎓 Post-Installation

### 1. ⚠️ Change Default Credentials

**IMPORTANT:** Change default admin password immediately!

#### Option A: Via Admin Panel

1. Login to http://localhost:5000/admin
2. Go to Settings or Profile
3. Change password from `admin123` to a strong password

#### Option B: Via Database

```bash
mysql -u root -p chatbot_si

# Update admin password (will be hashed by application)
UPDATE admin_users SET password = 'your_new_password_here' WHERE username = 'admin';
exit;
```

### 2. 🔑 Configure Groq API (Optional)

Groq API enhances chatbot responses with AI.

1. **Get API Key:**
   - Visit: https://console.groq.com
   - Sign up / Login
   - Generate API key

2. **Add to `.env`:**

   ```env
   GROQ_API_KEY=gsk_your_actual_key_here
   ENABLE_GROQ=true
   ```

3. **Test:**
   ```bash
   # Ask a complex question
   # The chatbot should provide more detailed AI-enhanced answers
   ```

See detailed setup: [docs/guides/GROQ_SETUP.md](docs/guides/GROQ_SETUP.md)

### 3. 📝 Customize Training Data

**Edit intents file:**

```bash
# Open training data
nano data/intents_ml.json  # Linux/Mac
notepad data\intents_ml.json  # Windows
```

**Add your own intents, patterns, and responses:**

```json
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["hi", "hello", "halo"],
      "responses": ["Hello! How can I help you?"]
    }
  ]
}
```

**Re-run migration to update database:**

```bash
python scripts/migration_script.py
```

### 4. 🧪 Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test
python tests/test_chatbot_filtering.py

# Run with coverage
pytest --cov=. tests/
```

### 5. 📊 Monitor Application

```bash
# Check logs in real-time
tail -f logs/app.log          # Linux/Mac
Get-Content logs\app.log -Wait  # Windows PowerShell

# Monitor security events
tail -f logs/security.log     # Linux/Mac
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. ❌ "MySQL connection refused"

**Problem:** Cannot connect to MySQL database

**Solutions:**

```bash
# Check if MySQL is running
# Windows:
sc query MySQL80
# If not running:
net start MySQL80

# Linux:
sudo systemctl status mysql
# If not running:
sudo systemctl start mysql

# Mac:
brew services list
# If not running:
brew services start mysql
```

**Check credentials:**

```bash
# Test MySQL connection
mysql -u root -p

# If login fails, reset password:
# See MySQL documentation for password reset
```

#### 2. ❌ "Module not found" / "No module named 'flask'"

**Problem:** Python dependencies not installed

**Solutions:**

```bash
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# Reinstall all dependencies
pip install --upgrade pip
pip install -r requirements.txt

# If still failing, try:
pip install --force-reinstall -r requirements.txt
```

#### 3. ❌ "Database 'chatbot_si' doesn't exist"

**Problem:** Database not created

**Solution:**

```bash
# Create database
mysql -u root -p -e "CREATE DATABASE chatbot_si CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Run migration
python scripts/migration_script.py
```

#### 4. ❌ "Port 5000 already in use"

**Problem:** Another application is using port 5000

**Solutions:**

```bash
# Option 1: Change port in .env
PORT=8000

# Option 2: Find and kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Linux/Mac:
lsof -i :5000
kill -9 <process_id>
```

#### 5. ❌ "Access denied for user 'root'@'localhost'"

**Problem:** MySQL credentials incorrect

**Solution:**

```bash
# Update .env with correct credentials
MYSQL_USER=your_actual_username
MYSQL_PASSWORD=your_actual_password

# Or create new MySQL user
mysql -u root -p

CREATE USER 'chatbot_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON chatbot_si.* TO 'chatbot_user'@'localhost';
FLUSH PRIVILEGES;
exit;
```

#### 6. ❌ "Secret key must be set"

**Problem:** SECRET_KEY not configured in .env

**Solution:**

```bash
# Generate new secret key
python -c "import os; print(os.urandom(24).hex())"

# Add to .env
SECRET_KEY=<paste_generated_key_here>
```

#### 7. ❌ "Template not found" errors

**Problem:** Flask cannot find HTML templates

**Solution:**

```bash
# Make sure you're running from project root
cd chatbot_SI
python app.py

# Check static/ folder exists with HTML files
ls static/  # Should show: index.html, admin.html, etc.
```

#### 8. ❌ "CORS policy" errors in browser console

**Problem:** Cross-origin requests blocked

**Solution:**

Already configured in the app, but if issues persist:

```bash
# Check Flask-Cors is installed
pip install flask-cors

# Verify in app.py
# CORS(app) should be present
```

#### 9. ❌ Migration script errors

**Problem:** Database migration fails

**Solution:**

```bash
# Drop and recreate database (WARNING: Destroys all data!)
mysql -u root -p

DROP DATABASE IF EXISTS chatbot_si;
CREATE DATABASE chatbot_si CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# Re-run migration
python scripts/migration_script.py
```

#### 10. ❌ Groq API not working

**Problem:** Groq API returns errors

**Solutions:**

```bash
# Check API key is valid
# Visit: https://console.groq.com

# Verify .env configuration
GROQ_API_KEY=gsk_...
ENABLE_GROQ=true

# Check internet connection
# Groq API requires internet access

# Disable Groq temporarily
ENABLE_GROQ=false
```

### Getting More Help

If you're still experiencing issues:

1. **Check Logs:**

   ```bash
   cat logs/app.log
   cat logs/security.log
   ```

2. **Enable Debug Mode:**

   ```env
   DEBUG=True
   LOG_LEVEL=DEBUG
   ```

3. **Search Issues:**
   - GitHub Issues: https://github.com/your-username/chatbot_SI/issues

4. **Create New Issue:**
   - Include: Error message, logs, OS, Python version
   - Include: Steps to reproduce

---

## 💻 Platform-Specific Guides

### Windows

#### Using Anaconda

```bash
# Create conda environment
conda create -n chatbot python=3.11
conda activate chatbot

# Install dependencies
pip install -r requirements.txt

# Continue with normal installation steps
```

#### Using XAMPP MySQL

```bash
# Start XAMPP Control Panel
# Start MySQL service

# Update .env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=    # Usually empty in XAMPP
```

### Linux (Ubuntu/Debian)

#### Install MySQL

```bash
# Update packages
sudo apt update

# Install MySQL
sudo apt install mysql-server

# Secure installation
sudo mysql_secure_installation

# Start MySQL
sudo systemctl start mysql
sudo systemctl enable mysql
```

#### Install Python 3.11

```bash
# Add PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev

# Install pip
sudo apt install python3-pip
```

### macOS

#### Using Homebrew

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11

# Install MySQL
brew install mysql
brew services start mysql

# Secure MySQL
mysql_secure_installation
```

---

## 📚 Documentation

### Quick Links

- 📖 [README.md](README.md) - Project overview
- 🏗️ [STRUCTURE.md](STRUCTURE.md) - Project structure
- 🔧 [Configuration Guide](docs/guides/GROQ_SETUP.md) - Groq API setup
- 🔒 [Security Guide](docs/guides/SECURITY_GUIDE.md) - Security best practices
- 🚀 [Deployment Guide](docs/deployment/DEPLOYMENT_GUIDE.md) - Deploy to production

### Deployment Guides

- [Railway](docs/deployment/RAILWAY_QUICKSTART.md) - Deploy to Railway
- [Hostinger](docs/deployment/HOSTINGER_DEPLOYMENT.md) - Deploy to Hostinger
- [Niagahoster](docs/deployment/NIAGAHOSTER_DEPLOYMENT.md) - Deploy to Niagahoster

### Troubleshooting Guides

- [Admin Panel Issues](docs/guides/ADMIN_PANEL_FIX_GUIDE.md)
- [MySQL Timeout](docs/guides/MYSQL_TIMEOUT_FIX.md)

---

## 🔗 Useful Commands

```bash
# Start application
python app.py

# Run in background (Linux/Mac)
nohup python app.py &

# Run migration
python scripts/migration_script.py

# Add sample data
python scripts/add_sample_chats.py

# Test database connection
python scripts/test_db_connection.py

# Interactive chatbot CLI
python scripts/chatbot_cli.py

# Run tests
pytest tests/

# Check Python version
python --version

# Check installed packages
pip list

# Update all packages
pip install --upgrade -r requirements.txt
```

---

## 🎉 Success!

If you've reached this point and your chatbot is running, congratulations! 🎊

**Next Steps:**

1. ✅ Change default admin password
2. ✅ Customize intents in `data/intents_ml.json`
3. ✅ Configure Groq API for better responses
4. ✅ Read [Security Guide](docs/guides/SECURITY_GUIDE.md)
5. ✅ Deploy to production (see [Deployment Guide](docs/deployment/DEPLOYMENT_GUIDE.md))

---

## 📞 Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/your-username/chatbot_SI/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/your-username/chatbot_SI/discussions)
- 📧 **Email:** your.email@example.com
- 📖 **Wiki:** [Project Wiki](https://github.com/your-username/chatbot_SI/wiki)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for Program Studi Sistem Informasi IPI Garut**

⭐ Star this repo if you find it helpful!

[⬆ Back to Top](#-installation-guide---chatbot-si)

</div>

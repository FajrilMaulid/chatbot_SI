# 🚀 Quick Installation Guide

## One-Click Install (Recommended)

### Windows

```bash
# Double-click atau run di terminal:
INSTALL.bat
```

### Linux/Mac

```bash
chmod +x install.sh
./install.sh
```

---

## Manual Installation

### Prerequisites

- ✅ Python 3.8+
- ✅ MySQL 5.7+ / MariaDB 10.2+
- ✅ pip

### Steps

```bash
# 1. Clone repository
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI

# 2. Setup Python
python setup.py
# Script will handle everything automatically!

# 3. Start application
python app.py
```

---

## Quick Verification

After installation, check:

1. ✅ `.env` file exists
2. ✅ Database `chatbot_si` created
3. ✅ Tables migrated
4. ✅ Admin user exists

Test:

```bash
# Visit
http://localhost:5000

# Admin panel
http://localhost:5000/admin
Username: admin
Password: admin123
```

---

## Troubleshooting

### "MySQL connection failed"

```bash
# Check MySQL is running
# Windows:
sc query MySQL

# Linux:
sudo systemctl status mysql

# Start if not running:
sudo systemctl start mysql
```

### "Module not found"

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### "Database already exists"

```bash
# Drop and recreate (WARNING: destroys data)
mysql -u root -p
DROP DATABASE chatbot_si;
CREATE DATABASE chatbot_si;
exit;

# Re-run migration
python scripts/migration_script.py
```

### Port 5000 already in use

```bash
# Change PORT in .env
PORT=8000

# Or stop other process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Linux:
lsof -i :5000
kill -9 <process_id>
```

---

## Configuration Files

### `.env` - Main configuration

```bash
# Database
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=chatbot_si

# Flask
SECRET_KEY=generate-with-python-os-urandom
FLASK_ENV=development

# Groq (optional)
GROQ_API_KEY=your_groq_key
```

### Generate SECRET_KEY

```bash
python -c "import os; print(os.urandom(24).hex())"
```

---

## Next Steps After Install

1. **Change admin password**
   - Login to `/admin`
   - Change default password `admin123`

2. **Configure Groq API** (optional)
   - Get key: https://console.groq.com
   - Add to `.env`

3. **Customize data**
   - Edit `data/intents_ml.json`
   - Run migration: `python scripts/migration_script.py`

4. **Deploy** (optional)
   - See `docs/DEPLOYMENT_GUIDE.md`

---

## Scripts Reference

| Script                            | Purpose                       |
| --------------------------------- | ----------------------------- |
| `setup.py`                        | Automated full setup          |
| `INSTALL.bat`                     | Windows one-click installer   |
| `install.sh`                      | Linux/Mac one-click installer |
| `scripts/migration_script.py`     | Database migration            |
| `scripts/fix_chat_logs_schema.py` | Fix schema issues             |
| `scripts/add_sample_chats.py`     | Add test data                 |

---

## Support

- 📖 Full guide: [README.md](README.md)
- 🏗️ Structure: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- 🚀 Deploy: [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/chatbot_SI/issues)

---

**Installation time: ~2-5 minutes** ⚡

# 🤖 Chatbot SI - Sistem Informasi IPI Garut

<div align="center">

Chatbot cerdas untuk menjawab pertanyaan seputar Program Studi Sistem Informasi dengan AI-powered responses dan admin panel lengkap.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7%2B-orange?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[🚀 Quick Start](#-quick-start-automated) • [📦 Full Installation Guide](INSTALLATION.md) • [📚 Documentation](#-documentation) • [🚀 Deploy](#-deployment)

</div>

---

## ✨ Features

- 🤖 **AI-Powered Chatbot** dengan Groq API integration
- 🎯 **Multi-Intent Detection** - Jawab pertanyaan majemuk sekaligus
- 🔍 **Topic Filtering** - Fokus pada pertanyaan akademik SI
- 📊 **Admin Panel** - Manage intents, patterns, responses
- 📈 **Chat Logs** - Track semua percakapan
- 🔒 **Security Features** - Rate limiting, input validation, logging
- 🎨 **Modern UI** - Glassmorphism design dengan dark mode

## 🚀 Quick Start (Automated)

> 📖 **For detailed installation instructions with troubleshooting and platform-specific guides, see [INSTALLATION.md](INSTALLATION.md)**

### Option 1: One-Click Setup (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI

# 2. Run automated setup
python setup.py
```

Setup script akan:

- ✅ Install semua dependencies
- ✅ Create database
- ✅ Run migration
- ✅ Setup .env file
- ✅ Add sample data
- ✅ Verify installation

### Option 2: Manual Setup

```bash
# 1. Clone repository
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI

# 2. Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
copy .config\.env.example .env  # Windows
# atau
cp .config/.env.example .env  # Linux/Mac

# Edit .env dengan database credentials Anda

# 5. Create database
mysql -u root -p
CREATE DATABASE chatbot_si;
exit;

# 6. Run migration
python scripts/migration_script.py

# 7. (Optional) Add sample data
python scripts/add_sample_chats.py
```

## ▶️ Run Application

```bash
python app.py
```

**Access:**

- Chatbot: http://localhost:5000
- Admin Panel: http://localhost:5000/admin
  - Username: `admin`
  - Password: `admin123` ⚠️ **CHANGE THIS!**

## 📋 Requirements

- Python 3.8+
- MySQL 5.7+ atau MariaDB 10.2+
- pip (Python package manager)

## 🔧 Configuration

### Database Setup

Edit `.env` file:

```bash
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=chatbot_si
```

### Groq API (Optional)

Untuk fitur AI enhancement, daftar di [Groq Console](https://console.groq.com):

```bash
GROQ_API_KEY=your_api_key_here
ENABLE_GROQ=true
```

### Secret Key

Generate secret key untuk Flask sessions:

```bash
python -c "import os; print(os.urandom(24).hex())"
```

Tambahkan ke `.env`:

```bash
SECRET_KEY=your_generated_secret_key
```

## 📁 Project Structure

```
chatbot_SI/
├── .config/          # Template konfigurasi (.env.example, .htaccess)
├── api/              # Flask blueprints (routes)
├── backup/           # File backup (code/)
├── config/           # Configuration management
├── core/             # Chatbot core logic (6 modules)
├── data/             # Training data
├── deployment/       # File deployment (Procfile, passenger_wsgi.py)
├── docs/             # Dokumentasi (deployment/, guides/, project/)
├── installation/     # Script instalasi (INSTALL.bat, install.sh)
├── logs/             # Application logs
├── models/           # Database operations
├── scripts/          # Standalone scripts
├── static/           # Frontend files
├── tests/            # Test files
├── utils/            # Security utilities
├── setup.py          # Automated setup script
└── app.py            # Main application
```

See [PROJECT_STRUCTURE.md](docs/project/PROJECT_STRUCTURE.md) for details.

## 🛠️ Useful Scripts

```bash
# Run migration
python scripts/migration_script.py

# Fix database schema
python scripts/fix_chat_logs_schema.py

# Add sample data
python scripts/add_sample_chats.py

# Run tests
pytest tests/
```

## 📚 Documentation

**Installation:**

- [📦 INSTALLATION.md](INSTALLATION.md) - **Complete installation guide** (Recommended)
- [docs/guides/INSTALL.md](docs/guides/INSTALL.md) - Quick installation reference

**Project & Setup:**

- [docs/project/PROJECT_STRUCTURE.md](docs/project/PROJECT_STRUCTURE.md) - Detailed project organization
- [docs/guides/GROQ_SETUP.md](docs/guides/GROQ_SETUP.md) - Groq API setup guide
- [docs/guides/SECURITY_GUIDE.md](docs/guides/SECURITY_GUIDE.md) - Security best practices

**Deployment:**

- [docs/deployment/DEPLOYMENT_GUIDE.md](docs/deployment/DEPLOYMENT_GUIDE.md) - General deployment instructions
- [docs/deployment/RAILWAY_QUICKSTART.md](docs/deployment/RAILWAY_QUICKSTART.md) - Deploy to Railway
- [docs/deployment/HOSTINGER_DEPLOYMENT.md](docs/deployment/HOSTINGER_DEPLOYMENT.md) - Deploy to Hostinger
- [docs/deployment/NIAGAHOSTER_DEPLOYMENT.md](docs/deployment/NIAGAHOSTER_DEPLOYMENT.md) - Deploy to Niagahoster

**Troubleshooting:**

- [docs/guides/ADMIN_PANEL_FIX_GUIDE.md](docs/guides/ADMIN_PANEL_FIX_GUIDE.md) - Fix admin panel issues
- [docs/guides/MYSQL_TIMEOUT_FIX.md](docs/guides/MYSQL_TIMEOUT_FIX.md) - Fix MySQL timeout issues

## 🔒 Security Features

- **Rate Limiting** - Proteksi brute force
- **Input Validation** - Sanitasi input user
- **Security Headers** - XSS, CSRF protection
- **Password Hashing** - Bcrypt untuk admin password
- **Session Security** - HTTPOnly cookies
- **Comprehensive Logging** - Track security events

## 🎯 Default Admin Credentials

⚠️ **IMPORTANT**: Change after first login!

- Username: `admin`
- Password: `admin123`

Change via admin panel or update database directly.

## 🌐 Deployment

### Railway.app (Recommended)

1. Push to GitHub
2. Connect to Railway
3. Add MySQL database addon
4. Set environment variables
5. Deploy!

See [docs/deployment/RAILWAY_QUICKSTART.md](docs/deployment/RAILWAY_QUICKSTART.md)

### Other Platforms

- **Render.com** - See [docs/deployment/DEPLOYMENT_GUIDE.md](docs/deployment/DEPLOYMENT_GUIDE.md)
- **Heroku** - Use MySQL ClearDB addon
- **VPS** - Nginx + Gunicorn setup

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test
python tests/test_chatbot_filtering.py

# Run with coverage
pytest --cov=. tests/
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

**Quick Start:**

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

For detailed guidelines, coding standards, and development setup, read [CONTRIBUTING.md](CONTRIBUTING.md).

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Fajril Maulid - Initial work

## 🙏 Acknowledgments

- Groq API for AI enhancement
- Flask framework
- scikit-learn for ML model
- Institut Pendidikan Indonesia (IPI) Garut

## 📞 Support

- GitHub Issues: [Report bugs](https://github.com/your-username/chatbot_SI/issues)
- Email: your.email@example.com
- Documentation: [Wiki](https://github.com/your-username/chatbot_SI/wiki)

---

**Made with ❤️ for Program Studi Sistem Informasi IPI Garut**

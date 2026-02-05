# 🤖 Chatbot SI - Sistem Informasi IPI Garut

<div align="center">

Chatbot cerdas untuk menjawab pertanyaan seputar Program Studi Sistem Informasi dengan respons bertenaga AI dan panel admin lengkap.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7%2B-orange?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[🚀 Mulai Cepat](#-mulai-cepat-otomatis) • [📦 Panduan Instalasi Lengkap](INSTALLATION.md) • [📚 Dokumentasi](#-dokumentasi) • [🚀 Deploy](#-deployment)

</div>

---

## ✨ Fitur

- 🤖 **Chatbot Bertenaga AI** dengan integrasi Groq API
- 🎯 **Deteksi Multi-Intent** - Jawab pertanyaan majemuk sekaligus
- 🔍 **Filter Topik** - Fokus pada pertanyaan akademik SI
- 📊 **Panel Admin** - Kelola intents, pola, dan respons
- 📈 **Log Percakapan** - Lacak semua percakapan
- 🔒 **Fitur Keamanan** - Pembatasan rate, validasi input, logging
- 🎨 **UI Modern** - Desain glassmorphism dengan mode gelap

## 🚀 Mulai Cepat (Otomatis)

> 📖 **Untuk instruksi instalasi lengkap dengan troubleshooting dan panduan khusus platform, lihat [INSTALLATION.md](INSTALLATION.md)**

### Opsi 1: Setup Satu Klik (Rekomendasi)

```bash
# 1. Clone repository
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI

# 2. Jalankan setup otomatis
python setup.py
```

Script setup akan:

- ✅ Install semua dependencies
- ✅ Buat database
- ✅ Jalankan migration
- ✅ Setup file .env
- ✅ Tambah data contoh
- ✅ Verifikasi instalasi

### Opsi 2: Setup Manual

```bash
# 1. Clone repository
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI

# 2. Buat virtual environment (opsional)
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

# Edit .env dengan kredensial database Anda

# 5. Buat database
mysql -u root -p
CREATE DATABASE chatbot_si;
exit;

# 6. Jalankan migration
python scripts/migration_script.py

# 7. (Opsional) Tambah data contoh
python scripts/add_sample_chats.py
```

## ▶️ Jalankan Aplikasi

```bash
python app.py
```

**Akses:**

- Chatbot: http://localhost:5000
- Panel Admin: http://localhost:5000/admin
  - Username: `admin`
  - Password: `admin123` ⚠️ **UBAH INI!**

## 📋 Persyaratan

- Python 3.8+
- MySQL 5.7+ atau MariaDB 10.2+
- pip (Python package manager)

## 🔧 Konfigurasi

### Setup Database

Edit file `.env`:

```bash
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password_anda
MYSQL_DATABASE=chatbot_si
```

### Groq API (Opsional)

Untuk fitur peningkatan AI, daftar di [Groq Console](https://console.groq.com):

```bash
GROQ_API_KEY=api_key_anda_disini
ENABLE_GROQ=true
```

### Secret Key

Generate secret key untuk Flask sessions:

```bash
python -c "import os; print(os.urandom(24).hex())"
```

Tambahkan ke `.env`:

```bash
SECRET_KEY=secret_key_yang_di_generate
```

## 📁 Struktur Proyek

```
chatbot_SI/
├── .config/          # Template konfigurasi (.env.example, .htaccess)
├── api/              # Flask blueprints (routes)
├── backup/           # File backup (code/)
├── config/           # Manajemen konfigurasi
├── core/             # Logika inti chatbot (6 modul)
├── data/             # Data training
├── deployment/       # File deployment (Procfile, passenger_wsgi.py)
├── docs/             # Dokumentasi (deployment/, guides/, project/)
├── installation/     # Script instalasi (INSTALL.bat, install.sh)
├── logs/             # Log aplikasi
├── models/           # Operasi database
├── scripts/          # Script standalone
├── static/           # File frontend
├── tests/            # File tes
├── utils/            # Utilitas keamanan
├── setup.py          # Script setup otomatis
└── app.py            # Aplikasi utama
```

Lihat [PROJECT_STRUCTURE.md](docs/project/PROJECT_STRUCTURE.md) untuk detail.

## 🛠️ Script Berguna

```bash
# Jalankan migration
python scripts/migration_script.py

# Perbaiki skema database
python scripts/fix_chat_logs_schema.py

# Tambah data contoh
python scripts/add_sample_chats.py

# Jalankan tes
pytest tests/
```

## 📚 Dokumentasi

**Instalasi:**

- [📦 INSTALLATION.md](INSTALLATION.md) - **Panduan instalasi lengkap** (Rekomendasi)
- [docs/guides/INSTALL.md](docs/guides/INSTALL.md) - Referensi instalasi cepat

**Proyek & Setup:**

- [docs/project/PROJECT_STRUCTURE.md](docs/project/PROJECT_STRUCTURE.md) - Organisasi proyek detail
- [docs/guides/GROQ_SETUP.md](docs/guides/GROQ_SETUP.md) - Panduan setup Groq API
- [docs/guides/SECURITY_GUIDE.md](docs/guides/SECURITY_GUIDE.md) - Praktik terbaik keamanan

**Deployment:**

- [docs/deployment/DEPLOYMENT_GUIDE.md](docs/deployment/DEPLOYMENT_GUIDE.md) - Instruksi deployment umum
- [docs/deployment/RAILWAY_QUICKSTART.md](docs/deployment/RAILWAY_QUICKSTART.md) - Deploy ke Railway
- [docs/deployment/HOSTINGER_DEPLOYMENT.md](docs/deployment/HOSTINGER_DEPLOYMENT.md) - Deploy ke Hostinger
- [docs/deployment/NIAGAHOSTER_DEPLOYMENT.md](docs/deployment/NIAGAHOSTER_DEPLOYMENT.md) - Deploy ke Niagahoster

**Troubleshooting:**

- [docs/guides/ADMIN_PANEL_FIX_GUIDE.md](docs/guides/ADMIN_PANEL_FIX_GUIDE.md) - Perbaiki masalah panel admin
- [docs/guides/MYSQL_TIMEOUT_FIX.md](docs/guides/MYSQL_TIMEOUT_FIX.md) - Perbaiki masalah timeout MySQL

## 🔒 Fitur Keamanan

- **Pembatasan Rate** - Proteksi brute force
- **Validasi Input** - Sanitasi input pengguna
- **Header Keamanan** - Proteksi XSS, CSRF
- **Password Hashing** - Bcrypt untuk password admin
- **Keamanan Session** - Cookie HTTPOnly
- **Logging Komprehensif** - Lacak peristiwa keamanan

## 🎯 Kredensial Admin Default

⚠️ **PENTING**: Ubah setelah login pertama kali!

- Username: `admin`
- Password: `admin123`

Ubah melalui panel admin atau update database secara langsung.

## 🌐 Deployment

### Railway.app (Rekomendasi)

1. Push ke GitHub
2. Hubungkan ke Railway
3. Tambah addon database MySQL
4. Set environment variables
5. Deploy!

Lihat [docs/deployment/RAILWAY_QUICKSTART.md](docs/deployment/RAILWAY_QUICKSTART.md)

### Platform Lain

- **Render.com** - Lihat [docs/deployment/DEPLOYMENT_GUIDE.md](docs/deployment/DEPLOYMENT_GUIDE.md)
- **Heroku** - Gunakan addon MySQL ClearDB
- **VPS** - Setup Nginx + Gunicorn

## 🧪 Testing

```bash
# Jalankan semua tes
pytest tests/

# Jalankan tes tertentu
python tests/test_chatbot_filtering.py

# Jalankan dengan coverage
pytest --cov=. tests/
```

## 🤝 Kontribusi

Kami menerima kontribusi! Silakan lihat [Panduan Kontribusi](CONTRIBUTING.md) kami untuk detail.

**Mulai Cepat:**

1. Fork repository
2. Buat feature branch (`git checkout -b feature/FiturKeren`)
3. Commit perubahan (`git commit -m 'Tambah FiturKeren'`)
4. Push ke branch (`git push origin feature/FiturKeren`)
5. Buka Pull Request

Untuk panduan detail, standar coding, dan setup pengembangan, baca [CONTRIBUTING.md](CONTRIBUTING.md).

## 📝 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT.

## 👥 Pembuat

- Fajril Maulid - Karya awal

## 🙏 Penghargaan

- Groq API untuk peningkatan AI
- Framework Flask
- scikit-learn untuk model ML
- Institut Pendidikan Indonesia (IPI) Garut

## 📞 Dukungan

- GitHub Issues: [Laporkan bug](https://github.com/your-username/chatbot_SI/issues)
- Email: your.email@example.com
- Dokumentasi: [Wiki](https://github.com/your-username/chatbot_SI/wiki)

---

**Dibuat dengan ❤️ untuk Program Studi Sistem Informasi IPI Garut**

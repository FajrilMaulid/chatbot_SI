# 📦 Panduan Instalasi - Chatbot SI

<div align="center">

**Panduan instalasi lengkap untuk Chatbot Sistem Informasi IPI Garut**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7%2B-orange?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[🚀 Mulai Cepat](#-mulai-cepat-recommended) • [🔧 Instalasi Manual](#-instalasi-manual) • [🐛 Troubleshooting](#-troubleshooting) • [📚 Dokumentasi](#-dokumentasi)

</div>

---

## 📋 Daftar Isi

- [Persyaratan Sistem](#-persyaratan-sistem)
- [Mulai Cepat (Recommended)](#-mulai-cepat-recommended)
- [Instalasi Manual](#-instalasi-manual)
- [Konfigurasi](#-konfigurasi)
- [Verifikasi](#-verifikasi)
- [Pasca Instalasi](#-pasca-instalasi)
- [Troubleshooting](#-troubleshooting)
- [Panduan Platform Spesifik](#-panduan-platform-spesifik)
- [Dokumentasi](#-dokumentasi)

---

## 🎯 Persyaratan Sistem

### Software yang Dibutuhkan

| Software                | Versi                 | Kegunaan           | Download                                                                             |
| ----------------------- | --------------------- | ------------------ | ------------------------------------------------------------------------------------ |
| **Python**              | 3.8 atau lebih tinggi | Lingkungan runtime | [Download](https://www.python.org/downloads/)                                        |
| **MySQL** / **MariaDB** | 5.7+ / 10.2+          | Server database    | [MySQL](https://dev.mysql.com/downloads/) / [MariaDB](https://mariadb.org/download/) |
| **pip**                 | Terbaru               | Package manager    | Sudah termasuk dengan Python                                                         |
| **Git**                 | Terbaru               | Version control    | [Download](https://git-scm.com/)                                                     |

### Cek Versi yang Terinstal

```bash
# Python
python --version
# Harus menampilkan: Python 3.8.x atau lebih tinggi

# pip
pip --version

# MySQL
mysql --version

# Git
git --version
```

### Spesifikasi Sistem

- **RAM:** Minimum 2GB (Direkomendasikan 4GB)
- **Storage:** Minimum 500MB ruang kosong
- **OS:** Windows 10+, Ubuntu 18.04+, macOS 10.15+

---

## 🚀 Mulai Cepat (Recommended)

> ⚡ **Estimasi Waktu:** 2-5 menit

### Opsi 1: Setup Otomatis

Ini adalah cara **termudah dan tercepat** untuk menginstal chatbot.

#### Untuk Semua Platform:

```bash
# 1. Clone repository
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI

# 2. Jalankan setup otomatis
python setup.py
```

Script `setup.py` akan otomatis:

- ✅ Mengecek persyaratan sistem
- ✅ Menginstal dependencies Python
- ✅ Membuat database dan tabel
- ✅ Setup konfigurasi `.env`
- ✅ Membuat user admin
- ✅ Menambahkan data contoh
- ✅ Verifikasi instalasi

#### Untuk Windows (One-Click):

```bash
# Double-click atau jalankan di terminal
installation\INSTALL.bat
```

#### Untuk Linux/Mac (One-Click):

```bash
# Buat executable dan jalankan
chmod +x installation/install.sh
./installation/install.sh
```

### Opsi 2: Setup Manual Cepat

```bash
# 1. Clone repository
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .config/.env.example .env
# Edit .env dengan kredensial database Anda

# 4. Buat database
mysql -u root -p -e "CREATE DATABASE chatbot_si;"

# 5. Jalankan migration
python scripts/migration_script.py

# 6. Mulai aplikasi
python app.py
```

---

## 🔧 Instalasi Manual

> 📝 **Untuk pengguna advanced** yang ingin kontrol penuh atas proses instalasi.

### Langkah 1: Clone Repository

```bash
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI
```

### Langkah 2: Buat Virtual Environment (Direkomendasikan)

Menggunakan virtual environment menjaga dependencies project tetap terisolasi.

#### Windows:

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan
venv\Scripts\activate
```

#### Linux/Mac:

```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan
source venv/bin/activate
```

Anda akan melihat `(venv)` di prompt terminal setelah aktivasi.

### Langkah 3: Install Dependencies

```bash
# Upgrade pip terlebih dahulu
pip install --upgrade pip

# Install semua requirements
pip install -r requirements.txt
```

**Dependencies yang akan diinstal:**

- Flask - Web framework
- Flask-Cors - Cross-origin resource sharing
- mysql-connector-python - MySQL database connector
- scikit-learn - Machine learning library
- python-dotenv - Environment variable management
- groq - Groq API client (opsional)

### Langkah 4: Setup Konfigurasi Environment

```bash
# Copy konfigurasi contoh
cp .config/.env.example .env

# Alternatif Windows
copy .config\.env.example .env
```

**Edit file `.env`** dengan text editor pilihan Anda:

```bash
# Linux/Mac
nano .env

# Windows
notepad .env
```

**Konfigurasi yang diperlukan:**

```env
# Konfigurasi Database
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password_mysql_anda_disini
MYSQL_DATABASE=chatbot_si
MYSQL_PORT=3306

# Konfigurasi Flask
SECRET_KEY=generate_random_secret_key_disini
FLASK_ENV=development
DEBUG=True
PORT=5000

# Konfigurasi Admin
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Groq API (Opsional - untuk peningkatan AI)
GROQ_API_KEY=groq_api_key_anda_disini
ENABLE_GROQ=false
```

**Generate SECRET_KEY:**

```bash
python -c "import os; print(os.urandom(24).hex())"
```

Copy output dan paste sebagai value `SECRET_KEY` Anda.

### Langkah 5: Setup Database

#### Buat Database

**Menggunakan MySQL CLI:**

```bash
# Login ke MySQL
mysql -u root -p

# Buat database
CREATE DATABASE chatbot_si CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Verifikasi database dibuat
SHOW DATABASES;

# Keluar dari MySQL
exit;
```

**Menggunakan MySQL Workbench:**

1. Buka MySQL Workbench
2. Koneksi ke MySQL server lokal Anda
3. Klik tombol "Create Schema"
4. Nama: `chatbot_si`
5. Charset: `utf8mb4`
6. Collation: `utf8mb4_unicode_ci`
7. Klik "Apply"

#### Jalankan Database Migration

```bash
# Buat semua tabel dan data awal
python scripts/migration_script.py
```

**Migration akan membuat:**

- `intents` - Pattern intent dan responses
- `chat_logs` - Histori percakapan chat
- `admin_users` - User admin panel

#### (Opsional) Tambahkan Data Contoh

```bash
# Tambah log chat untuk demonstrasi
python scripts/add_sample_chats.py
```

### Langkah 6: Test Koneksi Database

```bash
# Verifikasi konektivitas database
python scripts/test_db_connection.py
```

Anda akan melihat:

```
✅ Koneksi database berhasil!
✅ Ditemukan X intents di database
✅ Ditemukan X admin users
```

### Langkah 7: Mulai Aplikasi

```bash
# Mulai Flask development server
python app.py
```

Anda akan melihat:

```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

---

## ⚙️ Konfigurasi

### Referensi Environment Variables

```env
# ===================================
# KONFIGURASI DATABASE
# ===================================
MYSQL_HOST=localhost              # Host server MySQL
MYSQL_USER=root                   # Username MySQL
MYSQL_PASSWORD=password_anda      # Password MySQL (GANTI INI!)
MYSQL_DATABASE=chatbot_si         # Nama database
MYSQL_PORT=3306                   # Port MySQL (default: 3306)

# ===================================
# KONFIGURASI FLASK
# ===================================
SECRET_KEY=secret_key_anda_disini # Flask session secret (GENERATE BARU!)
FLASK_ENV=development             # development atau production
DEBUG=True                        # Enable debug mode (False di production)
PORT=5000                         # Port aplikasi

# ===================================
# KONFIGURASI ADMIN
# ===================================
ADMIN_USERNAME=admin              # Username admin default
ADMIN_PASSWORD=admin123           # Password admin default (GANTI INI!)

# ===================================
# GROQ API (OPSIONAL)
# ===================================
GROQ_API_KEY=                     # API key Groq Anda
ENABLE_GROQ=false                 # Enable peningkatan AI (true/false)
GROQ_MODEL=mixtral-8x7b-32768     # Model Groq yang digunakan

# ===================================
# LOGGING
# ===================================
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_TO_FILE=True                  # Simpan logs ke file

# ===================================
# KEAMANAN
# ===================================
RATE_LIMIT_ENABLED=True           # Enable rate limiting
MAX_LOGIN_ATTEMPTS=5              # Maksimal percobaan login gagal
SESSION_TIMEOUT=3600              # Timeout session dalam detik
```

### Struktur File Konfigurasi

```
chatbot_SI/
├── .env                          # Konfigurasi aktif Anda (git-ignored)
├── .config/
│   ├── .env.example              # Template konfigurasi
│   ├── .htaccess.hostinger.example
│   └── .htaccess.niagahoster.example
```

---

## ✅ Verifikasi

### 1. Cek Struktur File

```bash
# Verifikasi semua file essential ada
ls -la  # Linux/Mac
dir     # Windows
```

Anda harus memiliki:

- ✅ File `.env`
- ✅ Folder `venv/` (jika menggunakan virtual environment)
- ✅ Semua folder: `api/`, `core/`, `models/`, dll.

### 2. Test Database

```bash
# Login ke MySQL
mysql -u root -p

# Gunakan database
USE chatbot_si;

# Tampilkan tabel
SHOW TABLES;

# Harus menampilkan:
# +------------------------+
# | Tables_in_chatbot_si   |
# +------------------------+
# | admin_users            |
# | chat_logs              |
# | intents                |
# +------------------------+

# Keluar
exit;
```

### 3. Test Aplikasi

**A. Mulai Server:**

```bash
python app.py
```

**B. Test Endpoints:**

Buka browser Anda dan kunjungi:

1. **Chatbot Utama:** http://localhost:5000
   - Anda akan melihat interface chatbot
   - Coba kirim pesan: "Apa itu Sistem Informasi?"

2. **Login Admin:** http://localhost:5000/admin
   - Username: `admin`
   - Password: `admin123`
   - Anda harus bisa login

3. **Dashboard Admin:** http://localhost:5000/admin/dashboard
   - Harus menampilkan statistik
   - Harus menampilkan log chat terbaru

**C. Test Fungsi Chat:**

```bash
# Di terminal baru, test dengan CLI
python scripts/chatbot_cli.py

# Ketik beberapa pertanyaan:
# > Apa itu Sistem Informasi?
# > Siapa ketua HIMASIFOR?
# > Berapa biaya kuliah?
```

### 4. Cek Logs

```bash
# Lihat application logs
cat logs/app.log           # Linux/Mac
type logs\app.log          # Windows

# Lihat security logs
cat logs/security.log      # Linux/Mac
type logs\security.log     # Windows
```

---

## 🎓 Pasca Instalasi

### 1. ⚠️ Ganti Kredensial Default

**PENTING:** Ganti password admin default segera!

#### Opsi A: Via Admin Panel

1. Login ke http://localhost:5000/admin
2. Pergi ke Settings atau Profile
3. Ganti password dari `admin123` ke password yang kuat

#### Opsi B: Via Database

```bash
mysql -u root -p chatbot_si

# Update password admin (akan di-hash oleh aplikasi)
UPDATE admin_users SET password = 'password_baru_anda' WHERE username = 'admin';
exit;
```

### 2. 🔑 Konfigurasi Groq API (Opsional)

Groq API meningkatkan response chatbot dengan AI.

1. **Dapatkan API Key:**
   - Kunjungi: https://console.groq.com
   - Sign up / Login
   - Generate API key

2. **Tambahkan ke `.env`:**

   ```env
   GROQ_API_KEY=gsk_key_asli_anda_disini
   ENABLE_GROQ=true
   ```

3. **Test:**
   ```bash
   # Tanyakan pertanyaan kompleks
   # Chatbot harus memberikan jawaban yang lebih detail dengan AI
   ```

Lihat setup detail: [docs/guides/GROQ_SETUP.md](docs/guides/GROQ_SETUP.md)

### 3. 📝 Kustomisasi Training Data

**Edit file intents:**

```bash
# Buka training data
nano data/intents_ml.json  # Linux/Mac
notepad data\intents_ml.json  # Windows
```

**Tambahkan intents, patterns, dan responses Anda sendiri:**

```json
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["hi", "hello", "halo"],
      "responses": ["Halo! Apa yang bisa saya bantu?"]
    }
  ]
}
```

**Jalankan ulang migration untuk update database:**

```bash
python scripts/migration_script.py
```

### 4. 🧪 Jalankan Tests

```bash
# Jalankan semua tests
pytest tests/

# Jalankan test spesifik
python tests/test_chatbot_filtering.py

# Jalankan dengan coverage
pytest --cov=. tests/
```

### 5. 📊 Monitor Aplikasi

```bash
# Cek logs secara real-time
tail -f logs/app.log          # Linux/Mac
Get-Content logs\app.log -Wait  # Windows PowerShell

# Monitor security events
tail -f logs/security.log     # Linux/Mac
```

---

## 🐛 Troubleshooting

### Masalah Umum dan Solusi

#### 1. ❌ "MySQL connection refused"

**Masalah:** Tidak bisa koneksi ke MySQL database

**Solusi:**

```bash
# Cek apakah MySQL berjalan
# Windows:
sc query MySQL80
# Jika tidak berjalan:
net start MySQL80

# Linux:
sudo systemctl status mysql
# Jika tidak berjalan:
sudo systemctl start mysql

# Mac:
brew services list
# Jika tidak berjalan:
brew services start mysql
```

**Cek kredensial:**

```bash
# Test koneksi MySQL
mysql -u root -p

# Jika login gagal, reset password:
# Lihat dokumentasi MySQL untuk reset password
```

#### 2. ❌ "Module not found" / "No module named 'flask'"

**Masalah:** Dependencies Python tidak terinstal

**Solusi:**

```bash
# Pastikan virtual environment sudah diaktifkan
# Anda harus melihat (venv) di prompt

# Install ulang semua dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Jika masih gagal, coba:
pip install --force-reinstall -r requirements.txt
```

#### 3. ❌ "Database 'chatbot_si' doesn't exist"

**Masalah:** Database belum dibuat

**Solusi:**

```bash
# Buat database
mysql -u root -p -e "CREATE DATABASE chatbot_si CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Jalankan migration
python scripts/migration_script.py
```

#### 4. ❌ "Port 5000 already in use"

**Masalah:** Aplikasi lain menggunakan port 5000

**Solusi:**

```bash
# Opsi 1: Ganti port di .env
PORT=8000

# Opsi 2: Cari dan matikan proses yang menggunakan port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Linux/Mac:
lsof -i :5000
kill -9 <process_id>
```

#### 5. ❌ "Access denied for user 'root'@'localhost'"

**Masalah:** Kredensial MySQL salah

**Solusi:**

```bash
# Update .env dengan kredensial yang benar
MYSQL_USER=username_asli_anda
MYSQL_PASSWORD=password_asli_anda

# Atau buat user MySQL baru
mysql -u root -p

CREATE USER 'chatbot_user'@'localhost' IDENTIFIED BY 'password_kuat';
GRANT ALL PRIVILEGES ON chatbot_si.* TO 'chatbot_user'@'localhost';
FLUSH PRIVILEGES;
exit;
```

#### 6. ❌ "Secret key must be set"

**Masalah:** SECRET_KEY tidak dikonfigurasi di .env

**Solusi:**

```bash
# Generate secret key baru
python -c "import os; print(os.urandom(24).hex())"

# Tambahkan ke .env
SECRET_KEY=<paste_generated_key_disini>
```

#### 7. ❌ Error "Template not found"

**Masalah:** Flask tidak menemukan template HTML

**Solusi:**

```bash
# Pastikan Anda menjalankan dari project root
cd chatbot_SI
python app.py

# Cek folder static/ ada dengan file HTML
ls static/  # Harus menampilkan: index.html, admin.html, dll.
```

#### 8. ❌ Error "CORS policy" di browser console

**Masalah:** Cross-origin requests diblokir

**Solusi:**

Sudah dikonfigurasi di app, tapi jika masih ada masalah:

```bash
# Cek Flask-Cors terinstal
pip install flask-cors

# Verifikasi di app.py
# CORS(app) harus ada
```

#### 9. ❌ Error pada migration script

**Masalah:** Database migration gagal

**Solusi:**

```bash
# Drop dan buat ulang database (WARNING: Menghapus semua data!)
mysql -u root -p

DROP DATABASE IF EXISTS chatbot_si;
CREATE DATABASE chatbot_si CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit;

# Jalankan ulang migration
python scripts/migration_script.py
```

#### 10. ❌ Groq API tidak bekerja

**Masalah:** Groq API mengembalikan error

**Solusi:**

```bash
# Cek API key valid
# Kunjungi: https://console.groq.com

# Verifikasi konfigurasi .env
GROQ_API_KEY=gsk_...
ENABLE_GROQ=true

# Cek koneksi internet
# Groq API membutuhkan akses internet

# Nonaktifkan Groq sementara
ENABLE_GROQ=false
```

### Mendapatkan Bantuan Lebih Lanjut

Jika Anda masih mengalami masalah:

1. **Cek Logs:**

   ```bash
   cat logs/app.log
   cat logs/security.log
   ```

2. **Enable Debug Mode:**

   ```env
   DEBUG=True
   LOG_LEVEL=DEBUG
   ```

3. **Cari Issues:**
   - GitHub Issues: https://github.com/your-username/chatbot_SI/issues

4. **Buat Issue Baru:**
   - Sertakan: Pesan error, logs, OS, versi Python
   - Sertakan: Langkah-langkah untuk mereproduksi

---

## 💻 Panduan Platform Spesifik

### Windows

#### Menggunakan Anaconda

```bash
# Buat conda environment
conda create -n chatbot python=3.11
conda activate chatbot

# Install dependencies
pip install -r requirements.txt

# Lanjutkan dengan langkah instalasi normal
```

#### Menggunakan XAMPP MySQL

```bash
# Mulai XAMPP Control Panel
# Start service MySQL

# Update .env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=    # Biasanya kosong di XAMPP
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

# Mulai MySQL
sudo systemctl start mysql
sudo systemctl enable mysql
```

#### Install Python 3.11

```bash
# Tambah PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev

# Install pip
sudo apt install python3-pip
```

### macOS

#### Menggunakan Homebrew

```bash
# Install Homebrew (jika belum terinstal)
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

## 📚 Dokumentasi

### Link Cepat

- 📖 [README.md](README.md) - Overview project
- 🏗️ [STRUCTURE.md](STRUCTURE.md) - Struktur project
- 🔧 [Panduan Konfigurasi](docs/guides/GROQ_SETUP.md) - Setup Groq API
- 🔒 [Panduan Keamanan](docs/guides/SECURITY_GUIDE.md) - Best practices keamanan
- 🚀 [Panduan Deployment](docs/deployment/DEPLOYMENT_GUIDE.md) - Deploy ke production

### Panduan Deployment

- [Railway](docs/deployment/RAILWAY_QUICKSTART.md) - Deploy ke Railway
- [Hostinger](docs/deployment/HOSTINGER_DEPLOYMENT.md) - Deploy ke Hostinger
- [Niagahoster](docs/deployment/NIAGAHOSTER_DEPLOYMENT.md) - Deploy ke Niagahoster

### Panduan Troubleshooting

- [Masalah Admin Panel](docs/guides/ADMIN_PANEL_FIX_GUIDE.md)
- [MySQL Timeout](docs/guides/MYSQL_TIMEOUT_FIX.md)

---

## 🔗 Command Berguna

```bash
# Mulai aplikasi
python app.py

# Jalankan di background (Linux/Mac)
nohup python app.py &

# Jalankan migration
python scripts/migration_script.py

# Tambah data contoh
python scripts/add_sample_chats.py

# Test koneksi database
python scripts/test_db_connection.py

# Chatbot CLI interaktif
python scripts/chatbot_cli.py

# Jalankan tests
pytest tests/

# Cek versi Python
python --version

# Cek package terinstal
pip list

# Update semua packages
pip install --upgrade -r requirements.txt
```

---

## 🎉 Berhasil!

Jika Anda sudah sampai di sini dan chatbot Anda berjalan, selamat! 🎊

**Langkah Selanjutnya:**

1. ✅ Ganti password admin default
2. ✅ Kustomisasi intents di `data/intents_ml.json`
3. ✅ Konfigurasi Groq API untuk response yang lebih baik
4. ✅ Baca [Panduan Keamanan](docs/guides/SECURITY_GUIDE.md)
5. ✅ Deploy ke production (lihat [Panduan Deployment](docs/deployment/DEPLOYMENT_GUIDE.md))

---

## 📞 Dukungan

- 🐛 **Issues:** [GitHub Issues](https://github.com/your-username/chatbot_SI/issues)
- 💬 **Diskusi:** [GitHub Discussions](https://github.com/your-username/chatbot_SI/discussions)
- 📧 **Email:** your.email@example.com
- 📖 **Wiki:** [Project Wiki](https://github.com/your-username/chatbot_SI/wiki)

---

## 📄 Lisensi

Project ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

---

<div align="center">

**Dibuat dengan ❤️ untuk Program Studi Sistem Informasi IPI Garut**

⭐ Star repo ini jika Anda merasa terbantu!

[⬆ Kembali ke Atas](#-panduan-instalasi---chatbot-si)

</div>

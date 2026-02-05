# 🚀 Panduan Instalasi Cepat

## Instalasi One-Click (Direkomendasikan)

### Windows

```bash
# Double-click atau jalankan di terminal:
installation\INSTALL.bat
```

### Linux/Mac

```bash
chmod +x installation/install.sh
./installation/install.sh
```

---

## Instalasi Manual

### Persyaratan

- ✅ Python 3.8+
- ✅ MySQL 5.7+ / MariaDB 10.2+
- ✅ pip

### Langkah-langkah

```bash
# 1. Clone repository
git clone https://github.com/your-username/chatbot_SI.git
cd chatbot_SI

# 2. Setup Python
python setup.py
# Script akan menghandle semuanya secara otomatis!

# 3. Mulai aplikasi
python app.py
```

---

## Verifikasi Cepat

Setelah instalasi, cek:

1. ✅ File `.env` ada
2. ✅ Database `chatbot_si` dibuat
3. ✅ Tabel sudah dimigrate
4. ✅ User admin sudah ada

Test:

```bash
# Kunjungi
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
# Cek MySQL berjalan
# Windows:
sc query MySQL

# Linux:
sudo systemctl status mysql

# Mulai jika belum berjalan:
sudo systemctl start mysql
```

### "Module not found"

```bash
# Install ulang dependencies
pip install -r requirements.txt
```

### "Database already exists"

```bash
# Drop dan buat ulang (WARNING: menghapus data)
mysql -u root -p
DROP DATABASE chatbot_si;
CREATE DATABASE chatbot_si;
exit;

# Jalankan ulang migration
python scripts/migration_script.py
```

### Port 5000 sudah digunakan

```bash
# Ganti PORT di .env
PORT=8000

# Atau matikan proses lain yang menggunakan port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Linux:
lsof -i :5000
kill -9 <process_id>
```

---

## File Konfigurasi

### `.env` - Konfigurasi utama

```bash
# Database
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password_anda
MYSQL_DATABASE=chatbot_si

# Flask
SECRET_KEY=generate-dengan-python-os-urandom
FLASK_ENV=development

# Groq (opsional)
GROQ_API_KEY=groq_key_anda
```

### Generate SECRET_KEY

```bash
python -c "import os; print(os.urandom(24).hex())"
```

---

## Langkah Setelah Install

1. **Ganti password admin**
   - Login ke `/admin`
   - Ganti password default `admin123`

2. **Konfigurasi Groq API** (opsional)
   - Dapatkan key: https://console.groq.com
   - Tambahkan ke `.env`

3. **Kustomisasi data**
   - Edit `data/intents_ml.json`
   - Jalankan migration: `python scripts/migration_script.py`

4. **Deploy** (opsional)
   - Lihat `docs/deployment/DEPLOYMENT_GUIDE.md`

---

## Referensi Scripts

| Script                            | Kegunaan                      |
| --------------------------------- | ----------------------------- |
| `setup.py`                        | Setup otomatis lengkap        |
| `installation/INSTALL.bat`        | Windows one-click installer   |
| `installation/install.sh`         | Linux/Mac one-click installer |
| `scripts/migration_script.py`     | Database migration            |
| `scripts/fix_chat_logs_schema.py` | Perbaiki masalah schema       |
| `scripts/add_sample_chats.py`     | Tambah data test              |

---

## Dukungan

- 📖 Panduan lengkap: [INSTALLATION.md](../../INSTALLATION.md)
- 🏗️ Struktur: [PROJECT_STRUCTURE.md](../project/PROJECT_STRUCTURE.md)
- 🚀 Deploy: [DEPLOYMENT_GUIDE.md](../deployment/DEPLOYMENT_GUIDE.md)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/chatbot_SI/issues)

---

**Waktu instalasi: ~2-5 menit** ⚡

> 💡 **Untuk panduan instalasi lengkap dengan troubleshooting detail dan panduan platform-spesifik, lihat [INSTALLATION.md](../../INSTALLATION.md)**

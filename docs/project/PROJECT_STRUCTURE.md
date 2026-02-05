# 📁 Panduan Struktur Project

## Organisasi Folder

```
chatbot_SI/
│
├── 📂 api/                     # Flask Blueprints (Route API)
│   ├── __init__.py
│   ├── chat_routes.py          # Endpoint API chat
│   └── admin_routes.py         # Endpoint API admin panel
│
├── 📂 core/                    # Logika Inti Chatbot
│   ├── __init__.py             # Inisialisasi chatbot, exports
│   ├── database.py             # Koneksi DB & inisialisasi
│   ├── ml_model.py             # Training & prediksi ML
│   ├── groq_client.py          # Integrasi Groq API
│   ├── filters.py              # Filtering topik & multi-intent
│   └── response_handler.py     # Pipeline generasi response utama
│
├── 📂 config/                  # Konfigurasi
│   ├── __init__.py
│   └── app_config.py           # Konfigurasi aplikasi terpusat
│
├── 📂 models/                  # Model & Operasi Database
│   ├── __init__.py
│   └── admin_api.py            # Operasi CRUD admin
│
├── 📂 utils/                   # Fungsi Utility & Helpers
│   ├── __init__.py
│   ├── validators.py           # Validasi & sanitasi input
│   ├── security.py             # Kekuatan password, hashing, deteksi IP
│   └── logger.py               # Logging keamanan & admin
│
├── 📂 scripts/                 # Script Standalone
│   ├── migration_script.py     # Migrasi database
│   ├── chatbot_cli.py          # CLI chatbot (standalone)
│   ├── add_sample_chats.py     # Tambah data contoh
│   ├── fix_chat_logs_schema.py # Perbaiki schema
│   └── test_db_connection.py   # Test koneksi database
│
├── 📂 tests/                   # File Test
│   ├── __init__.py
│   ├── test_chatbot_filtering.py
│   ├── test_ipi_data.py
│   └── test_multi_intent.py
│
├── 📂 data/                    # File Data
│   └── intents_ml.json         # Data training chatbot
│
├── 📂 static/                  # File Statis (Frontend)
│   ├── admin.html              # Halaman login admin
│   ├── admin-dashboard.html    # Dashboard admin
│   ├── index.html              # Halaman chatbot utama
│   ├── css/
│   │   ├── styles.css
│   │   └── admin-styles.css
│   ├── js/
│   │   ├── app.js
│   │   ├── admin-app.js
│   │   └── particles.js
│   └── images/
│
├── 📂 logs/                    # Log Aplikasi
│   ├── security.log            # Percobaan login, akses tidak sah
│   ├── admin_actions.log       # Operasi CRUD admin
│   └── app.log                 # Log aplikasi umum
│
├── 📂 docs/                    # Dokumentasi
│   ├── deployment/             # Panduan deployment
│   ├── guides/                 # Panduan & troubleshooting
│   └── project/                # Dokumentasi project
│
├── 📂 .config/                 # Template konfigurasi
│   ├── .env.example
│   ├── .htaccess.hostinger.example
│   └── .htaccess.niagahoster.example
│
├── 📂 deployment/              # File deployment
│   ├── Procfile
│   ├── passenger_wsgi.py
│   └── runtime.txt
│
├── 📂 installation/            # Script instalasi
│   ├── INSTALL.bat
│   └── install.sh
│
├── 📂 backup/                  # File backup
│   ├── README.md
│   └── code/
│       ├── app.py.backup
│       └── chatbot_core.py.old
│
├── 📄 app.py                   # Aplikasi Flask Utama
├── 📄 setup.py                 # Script setup otomatis
├── 📄 requirements.txt         # Dependencies Python
├── 📄 .env                     # Environment variables (tidak di git)
├── 📄 .gitignore               # Pattern git ignore
├── 📄 README.md                # Dokumentasi project
├── 📄 INSTALLATION.md          # Panduan instalasi lengkap
├── 📄 CONTRIBUTING.md          # Panduan kontribusi
└── 📄 STRUCTURE.md             # File ini
```

## 📝 Deskripsi File

### Aplikasi Inti

- **app.py** - Aplikasi Flask utama dengan struktur tersederhanakan
- **setup.py** - Script setup otomatis untuk instalasi
- **requirements.txt** - Dependencies Python yang dibutuhkan

### API Blueprints (`api/`)

- **chat_routes.py** - Endpoint chat (`/api/chat`, `/api/clear-history`, `/api/health`)
- **admin_routes.py** - Route admin panel (`/admin`, `/api/admin/*`)

### Modul Inti (`core/`)

- **database.py** - Koneksi database (Railway & lokal), loading JSON, logging chat
- **ml_model.py** - Training model ML, prediksi intent, scoring confidence
- **groq_client.py** - Client Groq API, rephrasing response natural, kombinasi multi-intent
- **filters.py** - Filtering relevansi topik, deteksi multi-intent
- **response_handler.py** - Pipeline response utama, caching, proses multi-stage
- ****init**.py** - Inisialisasi package, fungsi `initialize_chatbot()`

### Konfigurasi (`config/`)

- **app_config.py** - Class konfigurasi terpusat (Flask, keamanan, pengaturan chatbot)

### Models (`models/`)

- **admin_api.py** - Autentikasi admin, operasi CRUD untuk intents/patterns/responses, logging chat

### Utilities (`utils/`)

- **validators.py** - Validasi input (username, password, nama intent, sanitasi)
- **security.py** - Pengecekan kekuatan password, hashing, deteksi IP
- **logger.py** - Logging keamanan, logging aksi admin

### Scripts (`scripts/`)

- **migration_script.py** - Migrasi database dari JSON ke MySQL
- **chatbot_cli.py** - Chatbot CLI standalone
- **add_sample_chats.py** - Tambah data contoh untuk testing
- **fix_chat_logs_schema.py** - Perbaiki schema chat logs
- **test_db_connection.py** - Test koneksi database

### Tests (`tests/`)

- **test_chatbot_filtering.py** - Test filtering topik
- **test_ipi_data.py** - Test data IPI
- **test_multi_intent.py** - Test deteksi multi-intent

## 🚀 Mulai Cepat

### 1. Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Setup database:

```bash
python scripts/migration_script.py
```

### 3. Jalankan aplikasi:

```bash
python app.py
```

### 4. Akses:

- **Chatbot**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin

## 📦 Pattern Import

### Import dari core:

```python
from core import initialize_chatbot, get_bot_response, groq_client
```

### Import dari api:

```python
from api import chat_bp, admin_bp, init_chat_routes, init_admin_routes
```

### Import dari config:

```python
from config import Config
```

### Import dari models:

```python
from models import admin_api
```

### Import dari utils:

```python
from utils.validators import validate_username, validate_password
from utils.security import check_password_strength, get_client_ip
from utils.logger import log_login_attempt, log_admin_action
```

## Menjalankan Scripts

### Jalankan migration:

```bash
python scripts/migration_script.py
```

### Jalankan CLI chatbot:

```bash
python scripts/chatbot_cli.py
```

### Tambah data contoh:

```bash
python scripts/add_sample_chats.py
```

### Jalankan tests:

```bash
# Test individual
python tests/test_chatbot_filtering.py

# Semua tests (jika pytest terinstal)
pytest tests/
```

## 🔒 Lokasi Fitur Keamanan

- **Rate Limiting**: app.py (Flask-Limiter)
- **Validasi Input**: utils/validators.py
- **Kekuatan Password**: utils/security.py
- **Logging**: utils/logger.py → logs/
- **Security Headers**: app.py (Flask-Talisman)

## 📊 Best Practices

### 1. **Models** - Operasi database saja

- Simpan logika database di `models/`
- Gunakan parameterized queries
- Handle error dengan graceful

### 2. **Utils** - Fungsi utility yang reusable

- Logika validasi umum
- Utility keamanan
- Fungsi logging

### 3. **API** - Request handling saja

- Controller tipis
- Delegasikan ke core/models
- Return HTTP codes yang proper

### 4. **Core** - Business logic

- Kecerdasan chatbot
- Proses ML
- Generasi response

### 5. **Tests** - Jaga test coverage tinggi

- Test setiap modul independently
- Integration tests untuk workflow
- Mock external dependencies

## 🔄 Menambah Fitur Baru

### Perlu tambah endpoint chat baru?

→ Tambahkan ke `api/chat_routes.py`

### Perlu modifikasi logika ML?

→ Edit `core/ml_model.py`

### Perlu ubah integrasi Groq?

→ Edit `core/groq_client.py`

### Perlu tambah fitur admin?

→ Tambahkan ke `api/admin_routes.py`

### Perlu update config?

→ Edit `config/app_config.py`

### Perlu tambah validasi?

→ Tambahkan ke `utils/validators.py`

### Perlu cek logs?

→ Lihat file di folder `logs/`

## 📈 Manfaat Arsitektur

- ✅ Modular & terorganisir
- ✅ Single responsibility per modul
- ✅ Mudah di-test independently
- ✅ Mudah di-maintain dan extend
- ✅ Arsitektur scalable
- ✅ Industry best practices
- ✅ Separation of concerns yang jelas

---

**Dibuat dengan ❤️ untuk Program Studi Sistem Informasi IPI Garut**

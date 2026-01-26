# Panduan Deploy Chatbot SI ke Niagahoster

Panduan lengkap step-by-step untuk deploy aplikasi Chatbot SI ke Niagahoster shared hosting dengan cPanel dan MySQL database.

---

## 📋 Prasyarat

Sebelum mulai, pastikan Anda punya:

- [ ] Akun Niagahoster aktif (paket Hosting minimal **Pelajar** atau **Bayi** dengan Python support)
- [ ] Akses cPanel dari Niagahoster
- [ ] File project chatbot sudah siap
- [ ] GROQ API Key (gratis dari https://console.groq.com)
- [ ] FTP Client (FileZilla) atau gunakan File Manager di cPanel

> [!IMPORTANT]
> **Niagahoster Python Support**: Tidak semua paket hosting Niagahoster support Python. Pastikan paket Anda memiliki Python App capability. Jika tidak tersedia, pertimbangkan upgrade atau gunakan VPS.

---

## 🎯 Ringkasan Deployment Strategy

Niagahoster menggunakan **Passenger WSGI** untuk menjalankan aplikasi Python/Flask. Berikut flow deployment:

1. Upload file aplikasi via FTP/File Manager
2. Setup MySQL database di cPanel
3. Install dependencies Python via SSH
4. Configure Passenger WSGI
5. Setup environment variables
6. Test dan monitoring

---

## 🚀 Tahapan Deployment

### **Step 1: Verifikasi File yang Diperlukan**

Pastikan file-file ini ada di root project Anda:

#### ✅ `requirements.txt`

```txt
flask
flask-cors
scikit-learn
mysql-connector-python
numpy
pandas
groq
python-dotenv
cachetools
gunicorn
Flask-Session
Werkzeug
Flask-Limiter
Flask-Talisman
```

#### ✅ `passenger_wsgi.py` (FILE BARU - PENTING!)

Buat file baru di root project:

```python
import sys
import os

# Add project directory to path
INTERP = os.path.expanduser("~/virtualenv/chatbot_si/3.9/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

# Import Flask app
from app import app as application
```

> [!NOTE]
> Path `/3.9/` di atas mungkin berbeda tergantung versi Python di server Niagahoster. Akan kita sesuaikan nanti di Step 6.

#### ✅ `.htaccess` (FILE BARU)

Buat file `.htaccess` di root project:

```apache
PassengerEnabled On
PassengerAppRoot /home/username/chatbot_si
PassengerStartupFile passenger_wsgi.py
PassengerPython /home/username/virtualenv/chatbot_si/3.9/bin/python3
```

Ganti `username` dengan actual username cPanel Anda.

---

### **Step 2: Upload File ke Hosting**

#### **Option A: Via cPanel File Manager (Recommended untuk pemula)**

1. **Login ke cPanel**
   - Buka email welcome dari Niagahoster
   - Atau login dari: https://panel.niagahoster.co.id
   - Klik **cPanel** pada layanan hosting Anda

2. **Buka File Manager**
   - Scroll ke section **Files**
   - Klik **File Manager**

3. **Navigasi ke public_html**
   - Jika ingin accessible di `https://yourdomain.com` → upload ke `public_html`
   - Jika ingin subdirectory `https://yourdomain.com/chatbot` → buat folder `chatbot` di `public_html`

4. **Upload Files**
   - Klik **Upload** di toolbar
   - Drag & drop atau select semua file project
   - Tunggu sampai complete

5. **Extract (jika upload ZIP)**
   - Jika upload dalam bentuk ZIP, klik kanan file → **Extract**

#### **Option B: Via FTP (Lebih cepat untuk file banyak)**

1. **Download FileZilla** dari https://filezilla-project.org

2. **Get FTP Credentials dari cPanel**
   - cPanel → **FTP Accounts**
   - Gunakan credentials atau buat FTP account baru

3. **Connect via FileZilla**

   ```
   Host: ftp.yourdomain.com
   Username: username@yourdomain.com
   Password: your_password
   Port: 21
   ```

4. **Upload Project**
   - Left panel: Local project folder
   - Right panel: `/public_html/`
   - Drag and drop semua file

---

### **Step 3: Setup MySQL Database**

1. **Buat Database**
   - cPanel → **MySQL Databases**
   - Di section **Create New Database**:
     - Database Name: `chatbot_db`
     - Click **Create Database**

   > [!NOTE]
   > Niagahoster akan menambahkan prefix username, mis: `username_chatbot_db`

2. **Buat MySQL User**
   - Scroll ke **MySQL Users** → **Add New User**
     - Username: `chatbot_user`
     - Password: Generate strong password (simpan!)
     - Click **Create User**

3. **Assign User ke Database**
   - Scroll ke **Add User To Database**
   - Select User: `chatbot_user`
   - Select Database: `chatbot_db`
   - Click **Add**
   - Di halaman **Privileges**, pilih **ALL PRIVILEGES**
   - Click **Make Changes**

4. **Catat Database Credentials**
   ```
   Database Name: username_chatbot_db
   Database User: username_chatbot_user
   Database Password: [password yang dibuat]
   Database Host: localhost
   Database Port: 3306
   ```

---

### **Step 4: Import Database Schema**

1. **Buka phpMyAdmin**
   - cPanel → **phpMyAdmin**
   - Select database `username_chatbot_db` di sidebar kiri

2. **Import SQL Schema**

   **Option A: Via phpMyAdmin (Recommended)**
   - Tab **SQL**
   - Copy-paste SQL berikut atau upload `migration_script.sql`:

   ```sql
   -- Create tables
   CREATE TABLE IF NOT EXISTS intents (
       id INT AUTO_INCREMENT PRIMARY KEY,
       intent_name VARCHAR(255) NOT NULL,
       tag VARCHAR(100),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TABLE IF NOT EXISTS patterns (
       id INT AUTO_INCREMENT PRIMARY KEY,
       intent_id INT NOT NULL,
       pattern_text TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE
   );

   CREATE TABLE IF NOT EXISTS responses (
       id INT AUTO_INCREMENT PRIMARY KEY,
       intent_id INT NOT NULL,
       response_text TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE
   );

   CREATE TABLE IF NOT EXISTS chat_logs (
       id INT AUTO_INCREMENT PRIMARY KEY,
       session_id VARCHAR(255) NOT NULL,
       user_message TEXT NOT NULL,
       bot_response TEXT NOT NULL,
       detected_intent VARCHAR(255),
       confidence FLOAT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       INDEX idx_session (session_id),
       INDEX idx_created (created_at)
   );

   CREATE TABLE IF NOT EXISTS admin_users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(100) UNIQUE NOT NULL,
       password_hash VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       last_login TIMESTAMP NULL
   );

   -- Create default admin user (password: admin123)
   INSERT INTO admin_users (username, password_hash) VALUES
   ('admin', 'scrypt:32768:8:1$lM8kN9pQ2rT4vW6z$8f5e4b3c2d1a0987654321fedcba9876543210abcdef1234567890abcdef123456789');
   ```

   - Click **Go** untuk execute

   **Option B: Via Migration Script**
   - Upload `scripts/migration_script.py` ke server
   - SSH ke server (Step 5)
   - Jalankan: `python scripts/migration_script.py`

3. **Verify Tables**

   ```sql
   SHOW TABLES;
   ```

   Harus ada: `intents`, `patterns`, `responses`, `chat_logs`, `admin_users`

---

### **Step 5: Setup Virtual Environment & Install Dependencies**

Niagahoster shared hosting umumnya tidak menyediakan SSH access untuk paket basic. Ada 2 opsi:

#### **Option A: Jika Punya SSH Access (VPS atau paket Premium)**

1. **Login via SSH**

   ```bash
   ssh username@yourdomain.com
   # atau SSH dari cPanel → Terminal
   ```

2. **Navigate ke Project Directory**

   ```bash
   cd ~/public_html/chatbot_si
   # atau cd ~/public_html/ jika itu root
   ```

3. **Create Virtual Environment**

   ```bash
   # Check Python version
   python3 --version

   # Create virtualenv
   virtualenv -p python3 ~/virtualenv/chatbot_si/3.9

   # Activate
   source ~/virtualenv/chatbot_si/3.9/bin/activate
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Test Installation**
   ```bash
   python -c "import flask; print('Flask OK')"
   python -c "import mysql.connector; print('MySQL OK')"
   python -c "import groq; print('Groq OK')"
   ```

#### **Option B: Jika TIDAK Ada SSH Access (Shared Hosting Basic)**

> [!WARNING]
> **Keterbatasan Shared Hosting**: Tanpa SSH, deployment Flask app ke shared hosting sangat terbatas. Niagahoster shared hosting basic **TIDAK RECOMMENDED** untuk Python apps production.
>
> **Alternatif yang Disarankan**:
>
> - Upgrade ke **VPS Niagahoster** (mulai Rp 50.000/bulan)
> - Atau gunakan platform PaaS seperti:
>   - **Render.com** (free tier available)
>   - **PythonAnywhere** (free tier dengan MySQL)
>   - **Heroku** (paid, tapi mudah)

Jika tetap ingin coba di shared hosting:

1. **Setup Python App via cPanel**
   - cPanel → **Setup Python App** (jika tersedia)
   - Python Version: 3.9 atau latest
   - Application Root: `/home/username/public_html/chatbot_si`
   - Application URL: `/` atau `/chatbot`
   - Click **Create**

2. **Add Dependencies**
   - Di Python App interface, ada field untuk install packages
   - Install satu per satu atau paste requirements.txt content

---

### **Step 6: Configure Environment Variables**

1. **Create `.env` File**

   Via File Manager:
   - Navigate ke root project folder
   - Click **+ File** → Create file `.env`
   - Edit file dan paste:

   ```bash
   # Flask Configuration
   SECRET_KEY=generate-your-own-key-here
   FLASK_ENV=production
   FLASK_DEBUG=False
   PORT=5000

   # Database MySQL
   MYSQL_HOST=localhost
   MYSQL_USER=username_chatbot_user
   MYSQL_PASSWORD=your_database_password
   MYSQL_DATABASE=username_chatbot_db
   MYSQL_PORT=3306

   # GROQ API
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=llama-3.3-70b-versatile
   GROQ_TEMPERATURE=0.7
   GROQ_MAX_TOKENS=1024

   # Chatbot Config
   CONFIDENCE_THRESHOLD=0.7
   ENABLE_GROQ=true
   ENABLE_CACHING=true
   CACHE_TTL=3600
   ENABLE_TOPIC_FILTERING=true
   FORCE_DATA_GROUNDED=true
   ENABLE_RESPONSE_REPHRASING=true
   ENABLE_MULTI_INTENT=true
   MULTI_INTENT_MAX_QUESTIONS=5

   # Security
   RATELIMIT_STORAGE_URL=memory://
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

2. **Generate SECRET_KEY**

   Di komputer lokal, jalankan:

   ```bash
   python -c "from utils.security import generate_secret_key; print(generate_secret_key())"
   ```

   Copy output dan paste ke `.env`

3. **Update Database Credentials**
   - Ganti `username_chatbot_user` dengan actual username
   - Ganti `your_database_password` dengan password MySQL
   - Ganti `username_chatbot_db` dengan actual database name

4. **Update GROQ_API_KEY**
   - Login ke https://console.groq.com
   - Generate API key
   - Paste ke `.env`

---

### **Step 7: Configure Passenger WSGI**

1. **Edit `passenger_wsgi.py`**

   Sesuaikan path dengan environment Anda:

   ```python
   import sys
   import os

   # Path ke Python interpreter di virtual environment
   INTERP = os.path.expanduser("~/virtualenv/chatbot_si/3.9/bin/python3")

   # Restart interpreter jika belum menggunakan virtualenv
   if sys.executable != INTERP:
       os.execl(INTERP, INTERP, *sys.argv)

   # Add project directory to Python path
   sys.path.insert(0, os.path.dirname(__file__))

   # Load environment variables
   from dotenv import load_dotenv
   load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

   # Import Flask app
   from app import app as application

   # Passenger compatibility
   if __name__ == '__main__':
       application.run()
   ```

2. **Update `.htaccess`**

   ```apache
   PassengerEnabled On
   PassengerAppRoot /home/username/public_html/chatbot_si
   PassengerStartupFile passenger_wsgi.py
   PassengerPython /home/username/virtualenv/chatbot_si/3.9/bin/python3

   # Redirect all requests to Passenger
   <IfModule mod_rewrite.c>
       RewriteEngine On
       RewriteBase /
       RewriteCond %{REQUEST_FILENAME} !-f
       RewriteCond %{REQUEST_FILENAME} !-d
       RewriteRule . passenger_wsgi.py [L]
   </IfModule>
   ```

   **Ganti:**
   - `username` dengan actual cPanel username
   - `/3.9/` dengan versi Python Anda

---

### **Step 8: Set File Permissions**

Via File Manager atau SSH:

```bash
# Set permissions
chmod 755 passenger_wsgi.py
chmod 644 .htaccess
chmod 600 .env
chmod -R 755 static/
chmod -R 755 templates/
```

Via File Manager:

- Klik kanan file → **Change Permissions**
- `passenger_wsgi.py`: 755
- `.htaccess`: 644
- `.env`: 600

---

### **Step 9: Restart Application**

1. **Via cPanel**
   - **Setup Python App** → Click **Restart**

2. **Via SSH (jika ada access)**

   ```bash
   touch ~/public_html/chatbot_si/tmp/restart.txt
   ```

3. **Via File Manager**
   - Create file `tmp/restart.txt` di root project
   - Passenger akan auto-detect dan restart

---

### **Step 10: Testing**

1. **Test Homepage**

   ```
   https://yourdomain.com
   # atau
   https://yourdomain.com/chatbot
   ```

   Harus muncul chatbot interface

2. **Test Chat API**

   ```bash
   curl -X POST https://yourdomain.com/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Halo"}'
   ```

3. **Test Admin Panel**

   ```
   https://yourdomain.com/admin
   ```

   - Login: `admin`
   - Password: `admin123` (GANTI SETELAH LOGIN!)

4. **Check Error Logs**
   - cPanel → **Errors** (jika ada)
   - Atau create `error_log` file di root project

---

## 🔧 Troubleshooting

### **Error: "Application failed to start"**

**Check:**

1. **Passenger Error Log**
   - File Manager → cek file `error_log` di root project
   - Atau cPanel → **Errors**

2. **Common Issues:**

   ```
   ModuleNotFoundError: No module named 'flask'
   → Solution: Install dependencies via pip (Step 5)

   Can't connect to MySQL server
   → Solution: Check .env database credentials

   Permission denied
   → Solution: Fix file permissions (Step 8)
   ```

3. **Python Path Issues**

   Edit `passenger_wsgi.py`:

   ```python
   # Debug: print Python path
   import sys
   print("Python:", sys.executable)
   print("Path:", sys.path)
   ```

### **Error: "Database connection failed"**

**Check:**

1. **Database credentials di `.env`**
2. **Database user privileges** (harus ALL PRIVILEGES)
3. **Database host** (gunakan `localhost`, bukan `127.0.0.1`)

**Test connection manual:**

Via SSH atau Python Shell di cPanel:

```python
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='username_chatbot_user',
    password='your_password',
    database='username_chatbot_db'
)
print("Connected:", conn.is_connected())
conn.close()
```

### **Error: "Static files not loading"**

**Check:**

1. **Static folder permissions**: 755
2. **CORS configuration** di `config.py`
3. **Browser console** untuk error details

**Solution:**

Update `.htaccess`:

```apache
# Allow static files
<FilesMatch "\.(css|js|png|jpg|jpeg|gif|ico|woff|woff2|ttf)$">
  Header set Access-Control-Allow-Origin "*"
</FilesMatch>
```

### **Error: "500 Internal Server Error"**

**Debug Steps:**

1. **Enable Flask Debug (temporarily)**

   Edit `.env`:

   ```bash
   FLASK_DEBUG=True
   ```

   > [!CAUTION]
   > **DISABLE** after debugging!

2. **Check Application Log**

   ```python
   # Add to passenger_wsgi.py
   import logging
   logging.basicConfig(filename='app.log', level=logging.DEBUG)
   ```

3. **Check Server Error Log**
   - cPanel → Errors

### **Chat tidak tersimpan ke database**

**Check:**

1. **Table `chat_logs` exists**

   ```sql
   SHOW TABLES LIKE 'chat_logs';
   ```

2. **Database user has INSERT privilege**
3. **Application logs** untuk database errors

---

## 💰 Niagahoster Pricing (2026)

### **Rekomendasi Paket untuk Python App:**

| Paket           | Harga/Bulan | Python Support | MySQL | Recommended?              |
| --------------- | ----------- | -------------- | ----- | ------------------------- |
| **Bayi**        | Rp 10.000   | ❌ Limited     | ✅    | ❌ Tidak untuk production |
| **Pelajar**     | Rp 15.000   | ❌ Limited     | ✅    | ❌ Tidak untuk production |
| **Personal**    | Rp 20.000   | ⚠️ Basic       | ✅    | ⚠️ Mungkin untuk testing  |
| **Bisnis**      | Rp 40.000   | ⚠️ Basic       | ✅    | ⚠️ Untuk low traffic      |
| **VPS Starter** | Rp 50.000   | ✅ Full SSH    | ✅    | ✅ **RECOMMENDED**        |

> [!IMPORTANT]
> **Untuk Production**: Sangat disarankan menggunakan **VPS** atau alternatif PaaS:
>
> - **VPS Niagahoster**: Rp 50.000/bulan (full control, SSH, Python)
> - **Render.com**: Free tier available (lebih mudah deployment)
> - **PythonAnywhere**: Free tier dengan MySQL included

---

## 🔄 Update Aplikasi

Untuk update setelah deploy:

1. **Edit code di lokal**
2. **Test di lokal**
3. **Upload file yang berubah** via FTP/File Manager
4. **Restart aplikasi**:
   ```bash
   touch tmp/restart.txt
   ```

---

## 📊 Monitoring & Maintenance

### **Check Logs**

1. **Application Log**
   - File: `chatbot_si/error_log`
   - Via File Manager atau download via FTP

2. **Server Error Log**
   - cPanel → **Errors**

3. **Custom Logging**

   Add to `app.py`:

   ```python
   import logging

   logging.basicConfig(
       filename='app.log',
       level=logging.INFO,
       format='%(asctime)s - %(levelname)s: %(message)s'
   )
   ```

### **Database Backup**

**Manual Backup via phpMyAdmin:**

1. phpMyAdmin → Select database
2. Tab **Export**
3. Format: SQL
4. Click **Go**
5. Save file

**Automated Backup via cPanel:**

- cPanel → **Backup**
- Setup daily/weekly backup
- Download backup files regularly

### **Monitor Traffic**

- cPanel → **Metrics** → **Visitors**
- Check bandwidth usage
- Monitor CPU usage

---

## 🆘 Alternative: Deploy ke VPS

Jika shared hosting tidak mencukupi, pertimbangkan **VPS Niagahoster**:

### **Kelebihan VPS:**

✅ Full SSH access
✅ Install packages bebas
✅ Python version control
✅ Better performance
✅ Custom configurations
✅ Process management (systemd)

### **Quick Start VPS:**

```bash
# 1. Order VPS dari Niagahoster
# 2. SSH ke VPS
ssh root@your-vps-ip

# 3. Install requirements
apt update
apt install python3 python3-pip mysql-server nginx

# 4. Clone/upload project
git clone https://github.com/yourusername/chatbot-si.git
cd chatbot-si

# 5. Install dependencies
pip3 install -r requirements.txt

# 6. Setup database
mysql -u root -p < scripts/migration_script.sql

# 7. Setup gunicorn + nginx
# ... (similar to Railway but with nginx reverse proxy)
```

---

## 📚 Resource Tambahan

- **Niagahoster Knowledge Base**: https://www.niagahoster.co.id/kb
- **cPanel Documentation**: https://docs.cpanel.net
- **Passenger Documentation**: https://www.phusionpassenger.com/docs
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/

---

## ✅ Post-Deployment Checklist

- [ ] Application accessible via domain
- [ ] Database connected dan tables created
- [ ] Admin panel working (`/admin`)
- [ ] Chat functionality working
- [ ] Static files loading (CSS, JS)
- [ ] No errors in error_log
- [ ] HTTPS enabled (SSL certificate)
- [ ] Admin password changed from default
- [ ] Environment variables configured
- [ ] CORS configured correctly
- [ ] Database backup strategy in place
- [ ] Monitoring setup

---

## ⚠️ Kesimpulan & Rekomendasi

### **Niagahoster Shared Hosting:**

**Pros:**

- ✅ Murah (mulai Rp 10.000/bulan)
- ✅ Support Indonesia
- ✅ cPanel user-friendly
- ✅ MySQL included

**Cons:**

- ❌ Limited Python support di paket basic
- ❌ Tidak ada SSH di paket murah
- ❌ Performance terbatas untuk Python apps
- ❌ Setup lebih rumit dibanding PaaS

### **Rekomendasi Final:**

1. **Untuk Production & Kemudahan**:
   - ✅ **Render.com** (deployment mudah, free tier)
   - ✅ **PythonAnywhere** (Python-focused, free tier)

2. **Untuk Budget & Control**:
   - ✅ **VPS Niagahoster** (Rp 50k/bulan, full control)

3. **Niagahoster Shared Hosting**:
   - ⚠️ Hanya untuk testing atau **sangat low traffic**
   - ⚠️ Butuh upgrade ke paket Bisnis minimal

---

**Jika ada kesulitan deployment ke Niagahoster shared hosting, saya sarankan coba Render.com atau PythonAnywhere sebagai alternatif yang lebih mudah dan reliable untuk Flask applications!** 🚀

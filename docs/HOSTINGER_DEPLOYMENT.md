# Panduan Deploy Chatbot SI ke Hostinger

Panduan lengkap step-by-step untuk deploy aplikasi Chatbot SI ke Hostinger shared hosting atau VPS dengan hPanel/cPanel dan MySQL database.

---

## 📋 Prasyarat

Sebelum mulai, pastikan Anda punya:

- [ ] Akun Hostinger aktif (minimal paket **Premium** atau **Business** dengan Python support)
- [ ] Akses hPanel dari Hostinger
- [ ] File project chatbot sudah siap
- [ ] GROQ API Key (gratis dari https://console.groq.com)
- [ ] FTP Client (FileZilla) atau gunakan File Manager di hPanel

> [!IMPORTANT]
> **Hostinger Python Support**: Tidak semua paket Hostinger mendukung Python applications. Paket **Premium Web Hosting** ke atas mendukung Python. Untuk production, **VPS Cloud** sangat disarankan.

---

## 🎯 Ringkasan Deployment Strategy

Hostinger menggunakan **hPanel** (proprietary control panel) atau **cPanel** (untuk VPS). Untuk Python apps, deployment menggunakan **Passenger WSGI** atau **custom setup** di VPS.

**Flow Deployment:**

1. Upload file aplikasi via FTP/File Manager
2. Setup MySQL database di hPanel
3. Install Python dependencies (via SSH)
4. Configure Passenger WSGI atau setup manual
5. Setup environment variables
6. Test dan monitoring

---

## 🚀 Tahapan Deployment

### **Step 1: Pilih Paket Hostinger yang Tepat**

#### **Shared Hosting Plans (untuk testing/low traffic)**

| Paket        | Harga/Bulan | Python Support | MySQL | Recommended?            |
| ------------ | ----------- | -------------- | ----- | ----------------------- |
| **Single**   | $2.99       | ❌ No          | ✅    | ❌ Tidak support Python |
| **Premium**  | $3.99       | ⚠️ Limited     | ✅    | ⚠️ Untuk testing only   |
| **Business** | $4.99       | ⚠️ Limited     | ✅    | ⚠️ Untuk low traffic    |

#### **VPS Cloud Plans (RECOMMENDED untuk production)**

| Paket     | Harga/Bulan | RAM  | CPU     | Storage | Recommended?      |
| --------- | ----------- | ---- | ------- | ------- | ----------------- |
| **KVM 1** | $5.99       | 4GB  | 1 core  | 50GB    | ✅ **BEST VALUE** |
| **KVM 2** | $8.99       | 8GB  | 2 cores | 100GB   | ✅ For scaling    |
| **KVM 4** | $14.99      | 16GB | 4 cores | 200GB   | ✅ High traffic   |

> [!TIP]
> **Rekomendasi**: Untuk chatbot production dengan MySQL, gunakan **VPS Cloud KVM 1** ($5.99/bulan). Lebih murah dari Railway dan full control dengan SSH.

---

### **Step 2: Verifikasi File yang Diperlukan**

Pastikan file-file ini ada di root project Anda:

#### ✅ `requirements.txt`

```txt
flask==3.0.0
flask-cors==4.0.0
scikit-learn==1.3.2
mysql-connector-python==8.2.0
numpy==1.26.2
pandas==2.1.4
groq==0.4.1
python-dotenv==1.0.0
cachetools==5.3.2
gunicorn==21.2.0
Flask-Session==0.5.0
Werkzeug==3.0.1
Flask-Limiter==3.5.0
Flask-Talisman==1.1.0
```

#### ✅ `passenger_wsgi.py` (Untuk Shared Hosting dengan Passenger)

```python
import sys
import os

# Add project directory to path
INTERP = os.path.expanduser("~/virtualenv/chatbot_si/3.9/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Import Flask app
from app import app as application

if __name__ == '__main__':
    application.run()
```

#### ✅ `.htaccess` (Untuk Shared Hosting)

```apache
PassengerEnabled On
PassengerAppRoot /home/username/public_html/chatbot_si
PassengerStartupFile passenger_wsgi.py
PassengerPython /home/username/virtualenv/chatbot_si/3.9/bin/python3

<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . passenger_wsgi.py [L]
</IfModule>
```

#### ✅ `wsgi.py` (Untuk VPS dengan Gunicorn)

```python
from app import app

if __name__ == '__main__':
    app.run()
```

---

### **Step 3: Upload File ke Hostinger**

#### **Option A: Via hPanel File Manager (Recommended untuk shared hosting)**

1. **Login ke hPanel**
   - Buka https://hpanel.hostinger.com
   - Login dengan email dan password Anda

2. **Pilih Hosting**
   - Dashboard → Pilih hosting yang ingin digunakan
   - Click **Manage**

3. **Buka File Manager**
   - Sidebar → **Files** → **File Manager**
   - Atau langsung ke **Public_html**

4. **Upload Files**
   - Navigate ke folder target (biasanya `public_html`)
   - Click **Upload Files**
   - Drag & drop atau select semua file project
   - Tunggu sampai complete

5. **Extract (jika upload ZIP)**
   - Klik kanan file ZIP → **Extract**

#### **Option B: Via FTP (Lebih cepat)**

1. **Get FTP Credentials**
   - hPanel → **Files** → **FTP Accounts**
   - Atau create new FTP account

2. **FTP Details:**

   ```
   Host: ftp.yourdomain.com
   Username: u123456789 (dari hPanel)
   Password: your_password
   Port: 21
   ```

3. **Connect via FileZilla**
   - Download FileZilla: https://filezilla-project.org
   - Connect dengan credentials di atas
   - Upload semua file ke `/public_html/chatbot_si/`

---

### **Step 4: Setup MySQL Database**

#### **Via hPanel (Shared Hosting)**

1. **Create Database**
   - hPanel → **Databases** → **MySQL Databases**
   - Click **+ Create New Database**
   - Database Name: `chatbot_db`
   - Click **Create**

2. **Note Credentials**

   Hostinger akan show:

   ```
   Database Name: u123456789_chatbot_db
   Username: u123456789
   Password: [auto-generated atau set sendiri]
   Hostname: localhost
   Port: 3306
   ```

   **SAVE** credentials ini!

3. **Access phpMyAdmin**
   - Click **Manage** pada database yang baru dibuat
   - Atau hPanel → **phpMyAdmin**

#### **Via VPS (jika pakai VPS Cloud)**

SSH ke VPS dan run:

```bash
# Install MySQL (jika belum ada)
sudo apt update
sudo apt install mysql-server -y

# Secure installation
sudo mysql_secure_installation

# Login ke MySQL
sudo mysql -u root -p

# Create database
CREATE DATABASE chatbot_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create user
CREATE USER 'chatbot_user'@'localhost' IDENTIFIED BY 'strong_password_here';

# Grant privileges
GRANT ALL PRIVILEGES ON chatbot_db.* TO 'chatbot_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

### **Step 5: Import Database Schema**

#### **Via phpMyAdmin**

1. **Open phpMyAdmin**
   - hPanel → **Databases** → Click database → **phpMyAdmin**

2. **Select Database**
   - Pada sidebar kiri, click database `u123456789_chatbot_db`

3. **Import Schema**
   - Tab **SQL**
   - Copy-paste SQL berikut:

```sql
-- Create intents table
CREATE TABLE IF NOT EXISTS intents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    intent_name VARCHAR(255) NOT NULL,
    tag VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tag (tag)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create patterns table
CREATE TABLE IF NOT EXISTS patterns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    intent_id INT NOT NULL,
    pattern_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE,
    INDEX idx_intent (intent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create responses table
CREATE TABLE IF NOT EXISTS responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    intent_id INT NOT NULL,
    response_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intent_id) REFERENCES intents(id) ON DELETE CASCADE,
    INDEX idx_intent (intent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create chat_logs table
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create admin_users table
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default admin user (username: admin, password: admin123)
-- IMPORTANT: Change this password after first login!
INSERT INTO admin_users (username, password_hash) VALUES
('admin', 'scrypt:32768:8:1$lM8kN9pQ2rT4vW6z$8f5e4b3c2d1a0987654321fedcba9876543210abcdef1234567890abcdef123456789')
ON DUPLICATE KEY UPDATE username=username;
```

4. **Execute**
   - Click **Go**
   - Verify tables created: `SHOW TABLES;`

---

### **Step 6: Setup Python Environment & Dependencies**

#### **Shared Hosting dengan SSH Access**

1. **Enable SSH**
   - hPanel → **Advanced** → **SSH Access**
   - Enable SSH dan note credentials

2. **SSH ke Server**

   ```bash
   ssh u123456789@yourdomain.com
   # Enter password dari hPanel
   ```

3. **Navigate to Project**

   ```bash
   cd ~/public_html/chatbot_si
   ls -la
   ```

4. **Check Python Version**

   ```bash
   python3 --version
   # atau
   python --version
   ```

5. **Create Virtual Environment**

   ```bash
   # Hostinger biasanya sudah punya virtualenv
   python3 -m venv ~/virtualenv/chatbot_si/3.9

   # Activate
   source ~/virtualenv/chatbot_si/3.9/bin/activate
   ```

6. **Install Dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt

   # Verify installations
   pip list
   ```

7. **Test Imports**
   ```bash
   python3 -c "import flask; print('Flask OK')"
   python3 -c "import mysql.connector; print('MySQL OK')"
   python3 -c "import groq; print('Groq OK')"
   ```

#### **VPS Cloud (Full Control)**

```bash
# 1. SSH ke VPS
ssh root@your-vps-ip

# 2. Update system
sudo apt update && sudo apt upgrade -y

# 3. Install Python dan dependencies
sudo apt install python3 python3-pip python3-venv -y

# 4. Navigate dan setup project
cd /var/www/chatbot_si

# 5. Create venv
python3 -m venv venv
source venv/bin/activate

# 6. Install requirements
pip install -r requirements.txt

# 7. Test app locally
python app.py
# Should run on port 5000
```

---

### **Step 7: Configure Environment Variables**

#### **Create `.env` File**

Via File Manager atau SSH:

```bash
# Via SSH
cd ~/public_html/chatbot_si
nano .env
```

Paste configuration berikut:

```bash
# Flask Configuration
SECRET_KEY=generate-your-own-secure-key-here
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000

# MySQL Database (update dengan credentials dari Step 4)
MYSQL_HOST=localhost
MYSQL_USER=u123456789
MYSQL_PASSWORD=your_database_password
MYSQL_DATABASE=u123456789_chatbot_db
MYSQL_PORT=3306

# GROQ API (get from https://console.groq.com)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=1024

# Chatbot Configuration
CONFIDENCE_THRESHOLD=0.7
ENABLE_GROQ=true
ENABLE_CACHING=true
CACHE_TTL=3600
ENABLE_TOPIC_FILTERING=true
FORCE_DATA_GROUNDED=true
ENABLE_RESPONSE_REPHRASING=true
ENABLE_MULTI_INTENT=true
MULTI_INTENT_MAX_QUESTIONS=5

# Security & Rate Limiting
RATELIMIT_STORAGE_URL=memory://
ALLOWED_ORIGINS=https://yourdomain.com
CORS_ORIGINS=https://yourdomain.com

# Session Configuration
SESSION_TYPE=filesystem
SESSION_PERMANENT=true
PERMANENT_SESSION_LIFETIME=3600
```

#### **Generate SECRET_KEY**

Di komputer lokal:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy output dan paste ke .env
```

#### **Set File Permissions**

```bash
chmod 600 .env
# Agar hanya owner yang bisa read/write
```

---

### **Step 8: Deploy Application**

#### **Option A: Shared Hosting dengan Passenger WSGI**

1. **Verify passenger_wsgi.py**

   Update path sesuai environment:

   ```python
   INTERP = os.path.expanduser("~/virtualenv/chatbot_si/3.9/bin/python3")
   ```

2. **Update .htaccess**

   Ganti `username` dengan actual username:

   ```apache
   PassengerAppRoot /home/u123456789/public_html/chatbot_si
   PassengerPython /home/u123456789/virtualenv/chatbot_si/3.9/bin/python3
   ```

3. **Set Permissions**

   ```bash
   chmod 755 passenger_wsgi.py
   chmod 644 .htaccess
   chmod -R 755 static/
   ```

4. **Restart Passenger**
   ```bash
   mkdir -p tmp
   touch tmp/restart.txt
   ```

#### **Option B: VPS dengan Systemd + Nginx**

Untuk VPS Cloud, setup production-grade deployment:

1. **Create Gunicorn Service**

```bash
sudo nano /etc/systemd/system/chatbot.service
```

```ini
[Unit]
Description=Chatbot SI Flask Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/chatbot_si
Environment="PATH=/var/www/chatbot_si/venv/bin"
ExecStart=/var/www/chatbot_si/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

2. **Start Service**

```bash
sudo systemctl daemon-reload
sudo systemctl start chatbot
sudo systemctl enable chatbot
sudo systemctl status chatbot
```

3. **Configure Nginx**

```bash
sudo nano /etc/nginx/sites-available/chatbot
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/chatbot_si/static;
        expires 30d;
    }
}
```

4. **Enable Site & Restart Nginx**

```bash
sudo ln -s /etc/nginx/sites-available/chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

5. **Setup SSL (Free dengan Let's Encrypt)**

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

### **Step 9: Testing**

#### **1. Test Homepage**

```
https://yourdomain.com
```

Harus muncul chatbot interface

#### **2. Test Chat API**

```bash
curl -X POST https://yourdomain.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Halo, apa itu sistem informasi?"}'
```

Expected response:

```json
{
  "response": "...",
  "intent": "greeting",
  "confidence": 0.95
}
```

#### **3. Test Admin Panel**

```
https://yourdomain.com/admin
```

- Username: `admin`
- Password: `admin123`

> [!CAUTION]
> **WAJIB ganti password default** setelah login pertama kali!

#### **4. Check Logs**

**Shared Hosting:**

```bash
cat ~/public_html/chatbot_si/error.log
```

**VPS:**

```bash
sudo journalctl -u chatbot -f
sudo tail -f /var/log/nginx/error.log
```

---

## 🔧 Troubleshooting

### **Error: "Application failed to start"**

**Check:**

1. **Error Logs**

   ```bash
   # Shared hosting
   cat ~/public_html/chatbot_si/error.log

   # VPS
   sudo journalctl -u chatbot -n 50
   ```

2. **Common Issues:**

   **ModuleNotFoundError: No module named 'flask'**

   ```bash
   Solution: Reinstall dependencies
   source ~/virtualenv/chatbot_si/3.9/bin/activate
   pip install -r requirements.txt
   ```

   **Can't connect to MySQL server**

   ```bash
   Solution: Check database credentials in .env
   Test: mysql -u u123456789 -p u123456789_chatbot_db
   ```

   **Permission denied**

   ```bash
   Solution: Fix permissions
   chmod 755 passenger_wsgi.py
   chmod -R 755 static/
   ```

### **Error: "500 Internal Server Error"**

**Debug Steps:**

1. **Enable Debug Temporarily**

   Edit `.env`:

   ```bash
   FLASK_DEBUG=True
   ```

   > **DISABLE** after debugging!

2. **Check Application Logs**

   ```python
   # Add to passenger_wsgi.py for debugging
   import logging
   logging.basicConfig(filename='app_debug.log', level=logging.DEBUG)
   ```

3. **Test Manually**
   ```bash
   cd ~/public_html/chatbot_si
   source ~/virtualenv/chatbot_si/3.9/bin/activate
   python app.py
   # Check error output
   ```

### **Error: "Database connection failed"**

**Solution:**

1. **Test Connection**

   ```bash
   mysql -h localhost -u u123456789 -p
   # Enter password
   USE u123456789_chatbot_db;
   SHOW TABLES;
   ```

2. **Check .env Variables**

   ```bash
   cat .env | grep MYSQL
   # Verify all values correct
   ```

3. **Test from Python**
   ```python
   python3 << EOF
   import mysql.connector
   conn = mysql.connector.connect(
       host='localhost',
       user='u123456789',
       password='your_password',
       database='u123456789_chatbot_db'
   )
   print("Connected:", conn.is_connected())
   conn.close()
   EOF
   ```

### **Static Files Not Loading**

**Check:**

1. **File Permissions**

   ```bash
   chmod -R 755 static/
   ```

2. **CORS Headers**

   Update `.htaccess`:

   ```apache
   <FilesMatch "\.(css|js|png|jpg|jpeg|gif|ico|woff|woff2|ttf)$">
       Header set Access-Control-Allow-Origin "*"
   </FilesMatch>
   ```

3. **Browser Cache**
   - Hard refresh: Ctrl+Shift+R
   - Clear cache

### **Chat Logs Not Saving**

**Check:**

1. **Table exists**

   ```sql
   SHOW TABLES LIKE 'chat_logs';
   DESC chat_logs;
   ```

2. **Database user permissions**

   ```sql
   SHOW GRANTS FOR 'u123456789'@'localhost';
   ```

3. **Application logs for DB errors**
   ```bash
   grep -i "database\|mysql" error.log
   ```

---

## 💰 Hostinger Pricing & Recommendations (2026)

### **Shared Hosting**

| Paket        | Harga/Bulan (Promo) | Normal | Storage | Bandwidth | Python?    |
| ------------ | ------------------- | ------ | ------- | --------- | ---------- |
| **Single**   | $2.99               | $9.99  | 50GB    | 100GB     | ❌         |
| **Premium**  | $3.99               | $11.99 | 100GB   | Unlimited | ⚠️ Limited |
| **Business** | $4.99               | $14.99 | 200GB   | Unlimited | ⚠️ Limited |

### **VPS Cloud (RECOMMENDED)**

| Paket     | Harga/Bulan | RAM  | CPU     | Storage   | Bandwidth |
| --------- | ----------- | ---- | ------- | --------- | --------- |
| **KVM 1** | **$5.99**   | 4GB  | 1 core  | 50GB SSD  | 1TB       |
| **KVM 2** | $8.99       | 8GB  | 2 cores | 100GB SSD | 2TB       |
| **KVM 4** | $14.99      | 16GB | 4 cores | 200GB SSD | 4TB       |
| **KVM 8** | $29.99      | 32GB | 8 cores | 400GB SSD | 8TB       |

### **Rekomendasi untuk Chatbot SI**

✅ **Best Choice: VPS Cloud KVM 1** ($5.99/bulan)

- 4GB RAM cukup untuk Flask + MySQL
- Full SSH access
- Complete control
- Scalable
- Better performance vs shared hosting

⚠️ **Alternative: Business Shared** ($4.99/bulan)

- Hanya untuk testing atau very low traffic
- Limited Python support
- Tidak recommended untuk production

---

## 🔄 Update Aplikasi

### **Shared Hosting**

```bash
# 1. SSH ke server
ssh u123456789@yourdomain.com

# 2. Navigate to project
cd ~/public_html/chatbot_si

# 3. Backup current version
tar -czf backup_$(date +%Y%m%d).tar.gz .

# 4. Upload new files via FTP or git pull
git pull origin main

# 5. Install new dependencies if any
source ~/virtualenv/chatbot_si/3.9/bin/activate
pip install -r requirements.txt

# 6. Restart application
touch tmp/restart.txt
```

### **VPS**

```bash
# 1. SSH ke VPS
ssh root@your-vps-ip

# 2. Navigate and pull
cd /var/www/chatbot_si
git pull origin main

# 3. Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# 4. Restart service
sudo systemctl restart chatbot
sudo systemctl status chatbot
```

---

## 📊 Monitoring & Maintenance

### **Monitor Application**

**Shared Hosting:**

```bash
# Check error logs
tail -f ~/public_html/chatbot_si/error.log

# Check access logs
tail -f ~/logs/access.log
```

**VPS:**

```bash
# Application logs
sudo journalctl -u chatbot -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# System resources
htop
```

### **Database Backup**

**Manual Backup:**

```bash
# Via SSH
mysqldump -u u123456789 -p u123456789_chatbot_db > backup_$(date +%Y%m%d).sql

# Download via FTP or SCP
scp u123456789@yourdomain.com:~/backup_*.sql ./
```

**Automated Backup Script:**

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=~/backups
DB_USER="u123456789"
DB_PASS="your_password"
DB_NAME="u123456789_chatbot_db"

mkdir -p $BACKUP_DIR

mysqldump -u $DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Keep only last 7 backups
ls -t $BACKUP_DIR/db_backup_*.sql.gz | tail -n +8 | xargs rm -f

echo "Backup completed: db_backup_$DATE.sql.gz"
```

Setup cron job:

```bash
crontab -e

# Daily backup at 3 AM
0 3 * * * /home/u123456789/backup.sh
```

### **Performance Monitoring**

**For VPS:**

1. **Install monitoring tools**

   ```bash
   sudo apt install htop iotop nethogs -y
   ```

2. **Monitor resources**

   ```bash
   # CPU & Memory
   htop

   # Disk I/O
   sudo iotop

   # Network
   sudo nethogs
   ```

3. **Application metrics**

   Consider using:
   - **Prometheus** + **Grafana** for metrics
   - **Uptime Robot** for uptime monitoring
   - **New Relic** for APM

---

## 🔐 Security Best Practices

### **1. Change Default Credentials**

```bash
# Login to admin panel
# /admin → Change password from 'admin123'
```

### **2. SSL Certificate (HTTPS)**

**Shared Hosting:**

- hPanel → **Security** → **SSL**
- Enable free SSL (Let's Encrypt)

**VPS:**

```bash
sudo certbot --nginx -d yourdomain.com
```

### **3. Firewall (VPS only)**

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### **4. Secure MySQL**

```bash
# Remove test database and anonymous users
sudo mysql_secure_installation

# Use strong passwords
# Disable remote access if not needed
```

### **5. Protect Sensitive Files**

Update `.htaccess`:

```apache
<FilesMatch "^\.env$">
    Order allow,deny
    Deny from all
</FilesMatch>

<FilesMatch "\.(py|pyc|pyo)$">
    Order allow,deny
    Deny from all
</FilesMatch>
```

### **6. Regular Updates**

```bash
# VPS: Update system regularly
sudo apt update && sudo apt upgrade -y

# Update Python packages
pip install --upgrade -r requirements.txt
```

---

## ✅ Post-Deployment Checklist

- [ ] Application accessible via domain
- [ ] HTTPS/SSL enabled
- [ ] Database connected dan tables created
- [ ] Admin panel working (`/admin`)
- [ ] Chat functionality working
- [ ] Static files loading (CSS, JS, images)
- [ ] No errors in logs
- [ ] Admin password changed from default
- [ ] Environment variables configured correctly
- [ ] CORS configured
- [ ] Backup strategy in place
- [ ] Monitoring setup
- [ ] Error logging configured
- [ ] Performance optimized

---

## 🆘 Getting Help

### **Hostinger Support**

- **24/7 Live Chat**: Available in hPanel
- **Knowledge Base**: https://support.hostinger.com
- **Community Forum**: https://community.hostinger.com

### **Technical Documentation**

- **Hostinger Tutorials**: https://www.hostinger.com/tutorials
- **Flask Documentation**: https://flask.palletsprojects.com
- **MySQL Documentation**: https://dev.mysql.com/doc/

---

## 🎉 Kesimpulan

Anda sekarang memiliki chatbot yang fully deployed di Hostinger!

**Untuk Production:**

- ✅ Gunakan **VPS Cloud KVM 1** untuk performa optimal
- ✅ Setup monitoring dan backup
- ✅ Enable SSL/HTTPS
- ✅ Regular maintenance dan updates

**Untuk Testing:**

- ⚠️ Business Shared bisa digunakan untuk POC
- ⚠️ Tapi bersiap untuk limitasi dan troubleshooting

**Cost-effective & Reliable:**

- Hostinger VPS ($5.99) vs Railway ($5-7) → **Similar price**
- Hostinger = **Full control** + **Better for Southeast Asia latency**
- Railway = **Easier deployment** (but need int'l payment)

---

**Selamat! Chatbot Anda sudah live di Hostinger!** 🚀

Jika ada pertanyaan atau masalah, check logs atau hubungi Hostinger support.

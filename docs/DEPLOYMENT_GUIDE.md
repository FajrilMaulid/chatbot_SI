# 🚀 Panduan Deployment Chatbot SI

Panduan lengkap untuk men-deploy Chatbot SI ke berbagai platform hosting.

---

## 📋 Pre-Deployment Checklist

Sebelum deploy, pastikan:

- ✅ Semua kode sudah terupdate dan berfungsi lokal
- ✅ File `.env` sudah dikonfigurasi dengan benar
- ✅ Database MySQL sudah ditest lokal
- ✅ Groq API key sudah didapatkan
- ✅ Git repository sudah siap (GitHub/GitLab)

---

## 🎯 Pilihan Platform Hosting

| Platform           | Kesulitan       | Harga Mulai | Rekomendasi             |
| ------------------ | --------------- | ----------- | ----------------------- |
| **Railway**        | ⭐ Mudah        | $5/bulan    | ⭐⭐⭐⭐⭐ Production   |
| **Render**         | ⭐ Mudah        | FREE        | ⭐⭐⭐⭐ Testing/Budget |
| **PythonAnywhere** | ⭐ Sangat Mudah | FREE        | ⭐⭐⭐ Pemula           |

---

## 🚂 Railway.app (RECOMMENDED)

### Kelebihan:

- Auto-deploy dari GitHub
- MySQL built-in
- SSL gratis
- Setup cepat

### Langkah-langkah:

#### 1. **Persiapan Repository**

```bash
# Inisialisasi git (jika belum)
git init

# Add semua file
git add .

# Commit
git commit -m "Initial commit for deployment"

# Push ke GitHub
git remote add origin https://github.com/username/chatbot-si.git
git branch -M main
git push -u origin main
```

#### 2. **Setup Railway**

1. Buka [railway.app](https://railway.app)
2. Klik **"Start a New Project"**
3. Login dengan GitHub
4. Klik **"Deploy from GitHub repo"**
5. Pilih repository `chatbot-si`

#### 3. **Tambah MySQL Database**

1. Di Railway dashboard, klik **"+ New"**
2. Pilih **"Database" → "Add MySQL"**
3. MySQL akan otomatis dibuat
4. Copy connection details

#### 4. **Setup Environment Variables**

Di Railway project settings → **Variables**, tambahkan:

```env
# Groq API
GROQ_API_KEY=gsk_your_actual_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=1024

# Chatbot
CONFIDENCE_THRESHOLD=0.7
ENABLE_GROQ=true
ENABLE_CACHING=true
CACHE_TTL=3600

# Flask
FLASK_ENV=production
FLASK_DEBUG=false

# MySQL (akan otomatis terisi dari Railway MySQL)
# Atau manual jika pakai external DB:
MYSQL_HOST=containers-us-west-xxx.railway.app
MYSQL_USER=root
MYSQL_PASSWORD=xxxxx
MYSQL_DATABASE=chatbot_si
MYSQL_PORT=3306
```

> **💡 Tips:** Railway akan auto-inject `DATABASE_URL` dari MySQL service. Anda mungkin perlu update `chatbot_core.py` untuk membaca ini.

#### 5. **Update Database Connection**

Edit `chatbot_core.py` untuk support Railway MySQL:

```python
import os

def get_db_connection():
    """Connect to database with Railway support"""
    # Railway provides DATABASE_URL
    database_url = os.getenv('DATABASE_URL')

    if database_url:
        # Parse Railway DATABASE_URL
        # Format: mysql://user:password@host:port/database
        import re
        match = re.match(r'mysql://(.+):(.+)@(.+):(\d+)/(.+)', database_url)
        if match:
            user, password, host, port, database = match.groups()
            return mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=int(port)
            )

    # Fallback to .env variables
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', 'chatbot_si')
    )
```

#### 6. **Deploy!**

Railway akan otomatis:

1. Detect Python project
2. Install dependencies dari `requirements.txt`
3. Run command dari `Procfile`
4. Generate public URL

**URL akan seperti:** `https://chatbot-si-production-xxxx.up.railway.app`

#### 7. **Setup Database Tables**

Setelah deploy, akses Railway MySQL:

1. Klik MySQL service → **"Data"** tab
2. Atau gunakan MySQL client dengan connection details
3. Run SQL untuk membuat tables:

```sql
CREATE DATABASE IF NOT EXISTS chatbot_si;
USE chatbot_si;

CREATE TABLE IF NOT EXISTS chat_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_message TEXT,
    bot_response TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confidence_score FLOAT,
    response_type VARCHAR(50)
);
```

#### 8. **Test Deployment**

Buka URL Railway dan test chatbot:

- Test basic questions
- Test Groq API responses
- Check conversation history

---

## 🎨 Render.com (FREE Alternative)

### Kelebihan:

- Free tier 750 hours/bulan
- Auto-deploy dari Git
- Custom domain gratis

### Langkah-langkah:

#### 1. **Push Code ke GitHub** (sama seperti Railway)

#### 2. **Setup Render**

1. Buka [render.com](https://render.com)
2. Sign up/Login dengan GitHub
3. Klik **"New +"** → **"Web Service"**
4. Connect repository `chatbot-si`

#### 3. **Configure Service**

- **Name:** chatbot-si
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Instance Type:** Free (atau Starter $7/month)

#### 4. **Add MySQL Database**

> ⚠️ **Catatan:** Render Free tier TIDAK include database. Pilihan:

**Opsi A: Pakai External Database (Gratis)**

- [FreeSQLDatabase.com](https://www.freesqldatabase.com/) (100MB gratis)
- [db4free.net](https://www.db4free.net/) (200MB gratis)

**Opsi B: Render PostgreSQL** ($7/month)

1. Klik **"New +"** → **"PostgreSQL"**
2. Connect ke web service

**Opsi C: Pakai Railway MySQL** (recommend)

- Deploy app di Render
- Database di Railway (lebih murah)

#### 5. **Environment Variables**

Di Render dashboard → **Environment**, tambahkan semua env vars seperti Railway.

#### 6. **Deploy**

Render akan auto-deploy. URL: `https://chatbot-si.onrender.com`

> ⚠️ **Free Tier:** Service akan "sleep" setelah 15 menit tidak ada traffic. First request setelah sleep butuh ~30 detik.

---

## 🐍 PythonAnywhere (TERMUDAH)

### Kelebihan:

- Khusus Python
- Setup sangat mudah
- MySQL included di Free tier
- Tidak perlu Docker/Git

### Langkah-langkah:

#### 1. **Sign Up**

1. Buka [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up untuk **Beginner** (Free) account

#### 2. **Upload Code**

**Opsi A: Upload ZIP**

1. Zip folder chatbot_si
2. Dashboard → **Files** → Upload ZIP
3. Extract di `/home/username/chatbot_si`

**Opsi B: Git Clone**

```bash
# Di PythonAnywhere Bash console
git clone https://github.com/username/chatbot-si.git
cd chatbot-si
```

#### 3. **Install Dependencies**

Di PythonAnywhere Bash console:

```bash
# Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 chatbot-env

# Install dependencies
pip install -r requirements.txt
```

#### 4. **Setup MySQL Database**

1. Dashboard → **Databases**
2. Buat database: `username$chatbot_si`
3. Set password
4. Klik **"Open MySQL console"**
5. Run SQL untuk create tables (sama seperti Railway)

#### 5. **Create .env File**

Di PythonAnywhere Files editor:

1. Buka `/home/username/chatbot_si/.env`
2. Tambahkan environment variables:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

CONFIDENCE_THRESHOLD=0.7
ENABLE_GROQ=true

MYSQL_HOST=username.mysql.pythonanywhere-services.com
MYSQL_USER=username
MYSQL_PASSWORD=your_db_password
MYSQL_DATABASE=username$chatbot_si
```

#### 6. **Configure Web App**

1. Dashboard → **Web** → **"Add a new web app"**
2. Pilih **"Manual configuration"**
3. Python version: **3.10**

#### 7. **Setup WSGI File**

Edit `/var/www/username_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

# Add project directory
project_home = '/home/username/chatbot_si'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from app import app as application
```

#### 8. **Set Virtual Environment**

Di Web app configuration:

- **Virtualenv:** `/home/username/.virtualenvs/chatbot-env`

#### 9. **Set Static Files**

Di "Static files" section:

- **URL:** `/static/`
- **Directory:** `/home/username/chatbot_si/static`

#### 10. **Reload & Test**

1. Klik **"Reload"** (green button)
2. Akses: `https://username.pythonanywhere.com`

---

## 🔧 Troubleshooting

### Railway

**Error: "Application failed to respond"**

```bash
# Check logs
railway logs

# Common fix: pastikan PORT dari environment
# Update app.py:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

**Database connection error**

```python
# Pastikan DATABASE_URL di-parse dengan benar
# Check Railway logs untuk connection string
```

### Render

**Service sleeping**

- Upgrade ke Starter ($7/month)
- Atau pakai external uptime monitor (UptimeRobot)

**Database not found**

- Pastikan external database accessible
- Check firewall rules

### PythonAnywhere

**ImportError**

```bash
# Pastikan virtual environment active
workon chatbot-env
pip install -r requirements.txt
```

**MySQL connection refused**

```env
# Pastikan host benar
MYSQL_HOST=username.mysql.pythonanywhere-services.com
# Bukan: localhost
```

**Static files 404**

- Cek path static files di Web config
- Reload web app

---

## ✅ Post-Deployment Verification

Setelah deploy, test:

1. **Basic Functionality**

   - [ ] Halaman utama terbuka
   - [ ] Chat interface muncul
   - [ ] Bisa kirim pesan

2. **ML Features**

   - [ ] Local ML predictions berfungsi
   - [ ] Confidence threshold kerja

3. **Groq API**

   - [ ] Complex questions dijawab API
   - [ ] Response natural dan bervariasi

4. **Database**

   - [ ] Chat logs tersimpan
   - [ ] Conversation history berfungsi

5. **Performance**
   - [ ] Response time < 3 detik
   - [ ] No errors di console

---

## 📊 Monitoring & Maintenance

### Logs

**Railway:**

```bash
railway logs --tail
```

**Render:**

- Dashboard → Logs tab

**PythonAnywhere:**

- Dashboard → Files → `/var/log/`
- Error log: `username.pythonanywhere.com.error.log`
- Server log: `username.pythonanywhere.com.server.log`

### Updates

**Auto-deploy (Railway/Render):**

```bash
git add .
git commit -m "Update chatbot"
git push origin main
# Auto-deploy triggered!
```

**Manual (PythonAnywhere):**

1. Update files via Files/Git
2. Reload web app

---

## 💰 Cost Optimization

### Free Tier Tricks:

1. **Groq API:**

   - FREE tier: 30 requests/minute
   - Cukup untuk usage ringan-medium
   - Set rate limiting jika perlu

2. **Database:**

   - Railway MySQL: $5/month (500MB)
   - Free alternatives: db4free.net
   - Optimize queries untuk save resources

3. **Hosting:**
   - Render Free: 750 hours = ~31 hari
   - Combine: App di Render (free) + DB di Railway ($5)
   - Total: $5/bulan

### Recommended Setup (Budget):

```
App: Render.com Free tier (Web Service)
Database: Railway.app $5/month (MySQL)
Total: $5/month = ~Rp 80.000/bulan
```

---

## 🎓 Tips untuk Mahasiswa

1. **GitHub Student Pack:**

   - Gratis $200 DigitalOcean credit
   - Gratis domain .me
   - Apply: [education.github.com](https://education.github.com/pack)

2. **Free Domain:**

   - Freenom (.tk, .ml, .ga) - gratis
   - Cloudflare Pages - gratis hosting + domain

3. **Development:**
   - Development: Local
   - Staging: Render Free
   - Production: Railway $5

---

## 📞 Support

Jika ada masalah:

1. Check logs terlebih dahulu
2. Verify environment variables
3. Test database connection
4. Check Groq API quota

**Platform Support:**

- Railway: [docs.railway.app](https://docs.railway.app)
- Render: [render.com/docs](https://render.com/docs)
- PythonAnywhere: [help.pythonanywhere.com](https://help.pythonanywhere.com)

---

## 🎉 Selamat!

Chatbot SI Anda sekarang sudah LIVE dan bisa diakses dari mana saja! 🚀

**Langkah selanjutnya:**

- Share URL dengan teman/dosen
- Monitor usage dan performance
- Tambah fitur baru
- Scale jika perlu

---

**Made with ❤️ for Sistem Informasi Students**

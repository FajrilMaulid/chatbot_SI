# Panduan Deploy Chatbot SI ke Railway

Panduan lengkap step-by-step untuk deploy aplikasi Chatbot SI ke Railway.app dengan MySQL database.

---

## 📋 Prasyarat

Sebelum mulai, pastikan Anda punya:

- [ ] Akun GitHub (untuk connect repository)
- [ ] Akun Railway.app (gratis - sign up di https://railway.app)
- [ ] Code sudah di-push ke GitHub repository
- [ ] File `.env` TIDAK di-commit ke Git (pastikan di `.gitignore`)

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

#### ✅ `runtime.txt`

```txt
python-3.13.1
```

#### ✅ `Procfile`

```
web: gunicorn app:app
```

#### ✅ `.gitignore`

Pastikan berisi:

```
.env
.env.local
__pycache__/
*.py[cod]
venv/
*.log
*.db
```

---

### **Step 2: Push Code ke GitHub**

```bash
# Pastikan .env tidak ter-track
git status

# Jika .env muncul, tambahkan ke .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"

# Push semua perubahan
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

---

### **Step 3: Setup Railway Project**

1. **Login ke Railway**
   - Buka https://railway.app
   - Click **"Login"** atau **"Start a New Project"**
   - Login dengan GitHub account

2. **Create New Project**
   - Click **"New Project"**
   - Pilih **"Deploy from GitHub repo"**
   - Pilih repository chatbot Anda
   - Railway akan auto-detect sebagai Python app

3. **Configure Build**
   - Railway otomatis detect `requirements.txt`
   - Build akan dimulai otomatis

---

### **Step 4: Setup MySQL Database**

1. **Add MySQL Service**
   - Di Railway dashboard project Anda
   - Click **"+ New"** → **"Database"** → **"Add MySQL"**
   - Railway akan provision MySQL database

2. **Get Database Credentials**
   - Click pada MySQL service
   - Tab **"Variables"**
   - Copy connection string `DATABASE_URL`

   Format:

   ```
   mysql://username:password@host:port/database
   ```

---

### **Step 5: Configure Environment Variables**

Di Railway dashboard, pada **Web Service** Anda:

1. **Click "Variables" tab**

2. **Add Raw Editor** dan paste:

```bash
# Flask Configuration
SECRET_KEY=generate-new-one-see-below
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5000

# Database (dari MySQL service Railway)
DATABASE_URL=mysql://root:password@containers-us-west-xxx.railway.app:1234/railway

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
ALLOWED_ORIGINS=https://your-app-name.up.railway.app

# MySQL Details (optional, DATABASE_URL override these)
MYSQL_HOST=containers-us-west-xxx.railway.app
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_DATABASE=railway
```

3. **Generate SECRET_KEY:**

   **Di komputer lokal**, jalankan:

   ```bash
   python -c "from utils.security import generate_secret_key; print(generate_secret_key())"
   ```

   Copy output dan paste ke `SECRET_KEY` di Railway variables.

4. **Update ALLOWED_ORIGINS:**
   - Setelah deploy, Railway akan kasih URL seperti `https://chatbot-si-production.up.railway.app`
   - Update `ALLOWED_ORIGINS` dengan URL tersebut

---

### **Step 6: Setup Database Schema**

Setelah MySQL service ready:

1. **Connect ke Database Railway**

   Ada 2 cara:

   **Cara 1: Dari Railway Dashboard**
   - Click MySQL service → Tab "Data"
   - Bisa run SQL query langsung di sini

   **Cara 2: Dari Lokal (MySQL Workbench/CLI)**

   ```bash
   mysql -h containers-us-west-xxx.railway.app -P 1234 -u root -p
   # Masukkan password dari Railway
   ```

2. **Run Migration Script**

   Upload `scripts/migration_script.py` dan jalankan:

   **Option A: Via Railway CLI** (recommended)

   ```bash
   # Install Railway CLI
   npm i -g @railway/cli

   # Login
   railway login

   # Link project
   railway link

   # Run migration
   railway run python scripts/migration_script.py
   ```

   **Option B: Manual SQL**
   - Copy SQL dari migration script
   - Paste dan run di Railway MySQL Data tab

3. **Verify Tables Created**
   ```sql
   SHOW TABLES;
   -- Expected: intents, patterns, responses, chat_logs, admin_users
   ```

---

### **Step 7: Deploy Application**

1. **Trigger Deployment**
   - Railway akan auto-deploy saat ada perubahan
   - Atau click **"Deploy"** di dashboard

2. **Monitor Build Logs**
   - Tab **"Deployments"** → Click latest deployment
   - Lihat build logs untuk error

   Expected output:

   ```
   -----> Installing dependencies from requirements.txt
   -----> Discovering process types
          Procfile declares types -> web
   -----> Launching...
   ```

3. **Check Application Logs**
   - Tab **"Logs"** di service
   - Pastikan tidak ada error

   Expected:

   ```
   [OK] Groq API initialized successfully
   [OK] Local Database Connected
   [OK] Chatbot initialization complete!
   * Running on http://0.0.0.0:5000
   ```

---

### **Step 8: Dapatkan URL Aplikasi**

1. **Generate Public URL**
   - Tab **"Settings"** → **"Networking"**
   - Click **"Generate Domain"**
   - Railway akan beri URL: `https://your-app.up.railway.app`

2. **Custom Domain (Optional)**
   - Jika punya domain sendiri
   - Settings → Networking → Custom Domain
   - Add domain dan configure DNS

---

### **Step 9: Testing**

1. **Test Homepage**

   ```
   https://your-app.up.railway.app
   ```

   - Harus muncul chatbot interface

2. **Test Chat API**

   ```bash
   curl -X POST https://your-app.up.railway.app/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Halo"}'
   ```

3. **Test Admin Panel**

   ```
   https://your-app.up.railway.app/admin
   ```

   - Login dengan credentials dari migration script
   - Default: `admin` / `admin123`

4. **Test Database**
   - Send beberapa chat messages
   - Check di Admin Panel → Chat Logs
   - Harus tersimpan di database

---

### **Step 10: Security Checklist**

Setelah deploy, verifikasi:

- [ ] `FLASK_DEBUG=false` di Railway variables
- [ ] `SECRET_KEY` bukan default value
- [ ] `ALLOWED_ORIGINS` sudah di-set ke Railway URL
- [ ] File `.env` tidak di-commit ke Git
- [ ] Admin password sudah diganti (default: `admin123`)
- [ ] HTTPS aktif (Railway auto-provide SSL)
- [ ] Database credentials aman
- [ ] Logs tidak expose sensitive data

---

## 🔧 Troubleshooting

### **Error: "Application failed to start"**

**Check Logs:**

```bash
railway logs
```

**Common Issues:**

1. **Missing dependencies**

   ```
   Solution: Verify requirements.txt is complete
   ```

2. **Database connection failed**

   ```
   Solution: Check DATABASE_URL is correct
   ```

3. **Port binding error**
   ```
   Solution: Make sure app.py uses PORT from env:
   port = int(os.getenv('PORT', 5000))
   app.run(host='0.0.0.0', port=port)
   ```

### **Error: "Database tables not found"**

**Solution:**

```bash
# Run migration script via Railway CLI
railway run python scripts/migration_script.py
```

### **Error: "Static files not loading"**

**Check:**

- `static` folder ada di repository
- CORS headers configured correctly
- Check browser console for errors

### **Chat logs tidak tersimpan**

**Check:**

1. Database schema correct (`chat_logs` table exists)
2. Database credentials valid
3. Application logs for database errors

---

## 💰 Railway Pricing (2026)

### **Free Tier:**

- $5 credit per month
- Enough untuk:
  - Small Flask app
  - MySQL database (basic)
  - Low traffic (~1000 requests/month)

### **Hobby Plan ($5/month):**

- $5 base + usage
- Recommended untuk production
- Better uptime
- More resources

### **Estimasi Biaya:**

- **App (512MB RAM):** ~$2-3/month
- **MySQL (512MB):** ~$2-3/month
- **Total:** ~$5-7/month

---

## 🔄 Update Aplikasi

Untuk update setelah deploy:

```bash
# 1. Edit code di lokal
# 2. Test di lokal
# 3. Commit dan push
git add .
git commit -m "Update feature XYZ"
git push origin main

# Railway akan auto-deploy!
```

**Monitoring:**

- Railway dashboard → Deployments
- Check logs untuk error

---

## 📊 Monitoring & Maintenance

### **Check Logs**

```bash
# Via Railway CLI
railway logs

# Or di Railway Dashboard → Logs tab
```

### **Database Backup**

**Manual Backup:**

```bash
# Connect dan export
mysqldump -h host -P port -u user -p database > backup.sql
```

**Railway Auto-backup:**

- Upgrade ke Pro plan untuk auto-backups

### **Monitor Usage**

- Dashboard → Metrics
- Track CPU, Memory, Network usage
- Set alerts untuk high usage

---

## 🆘 Rollback Deployment

Jika ada masalah setelah deploy:

1. **Via Railway Dashboard:**
   - Deployments tab
   - Click deployment sebelumnya yang stable
   - Click "Redeploy"

2. **Via Git:**
   ```bash
   # Revert ke commit sebelumnya
   git revert HEAD
   git push origin main
   ```

---

## 📚 Resource Tambahan

- **Railway Docs:** https://docs.railway.app
- **Railway Community:** https://discord.gg/railway
- **Flask Deployment Guide:** https://flask.palletsprojects.com/en/latest/deploying/

---

## ✅ Post-Deployment Checklist

- [ ] Application accessible via Railway URL
- [ ] Database connected dan tables created
- [ ] Admin panel working
- [ ] Chat functionality working
- [ ] Logs showing no errors
- [ ] HTTPS enabled (auto Railway)
- [ ] Admin password changed from default
- [ ] Environment variables configured
- [ ] CORS configured correctly
- [ ] Monitoring setup
- [ ] Backup strategy in place

---

**Selamat! Chatbot Anda sudah live di Railway!** 🎉

Jika ada pertanyaan atau masalah, check Railway logs atau community Discord.

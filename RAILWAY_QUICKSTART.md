# 🚀 Quick Start Deployment - Railway.app

Panduan singkat deploy Chatbot SI ke Railway (paling recommended).

---

## ⚡ Prerequisites

- [ ] Git installed
- [ ] GitHub account
- [ ] Groq API Key ([console.groq.com](https://console.groq.com))
- [ ] Code chatbot sudah berfungsi lokal

---

## 📝 Step-by-Step

### 1. Push ke GitHub

```bash
# Inisialisasi git (jika belum)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create repository di GitHub, lalu:
git remote add origin https://github.com/YOUR_USERNAME/chatbot-si.git
git branch -M main
git push -u origin main
```

### 2. Deploy ke Railway

1. **Sign Up Railway:**

   - Buka [railway.app](https://railway.app)
   - Login dengan GitHub

2. **Create New Project:**

   - Klik **"Start a New Project"**
   - Pilih **"Deploy from GitHub repo"**
   - Select `chatbot-si` repository
   - Klik **"Deploy Now"**

3. **Add MySQL Database:**
   - Di project dashboard, klik **"+ New"**
   - Pilih **"Database"** → **"Add MySQL"**
   - MySQL service akan auto-create

### 3. Configure Environment Variables

Di Railway project → Select your web service → **"Variables"** tab:

```env
GROQ_API_KEY=gsk_your_actual_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=1024
CONFIDENCE_THRESHOLD=0.7
ENABLE_GROQ=true
ENABLE_CACHING=true
CACHE_TTL=3600
FLASK_ENV=production
FLASK_DEBUG=false
```

> **💡 Pro tip:** Railway akan auto-inject `DATABASE_URL` dari MySQL service.

### 4. Update Database Connection Code

Edit `chatbot_core.py`, ubah database connection function:

```python
import os
import re
import mysql.connector

def get_db_connection():
    """Connect to database with Railway support"""
    # Railway provides DATABASE_URL automatically
    database_url = os.getenv('DATABASE_URL')

    if database_url:
        # Parse Railway DATABASE_URL format: mysql://user:password@host:port/database
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

    # Fallback to manual env vars (for local development)
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', 'chatbot_si')
    )
```

Update di function `initialize_chatbot()` juga:

```python
def initialize_chatbot():
    """Initialize chatbot components"""
    try:
        # Connect to database
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # ... rest of code
```

**Commit & push changes:**

```bash
git add chatbot_core.py
git commit -m "Add Railway database support"
git push origin main
```

Railway akan auto-redeploy!

### 5. Setup Database Tables

Setelah deploy selesai:

1. **Access Railway MySQL:**

   - Di Railway dashboard → Klik **MySQL service**
   - Tab **"Data"** → **"Query"**

2. **Run SQL:**

```sql
-- Create table for chat logs
CREATE TABLE IF NOT EXISTS chat_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_message TEXT,
    bot_response TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confidence_score FLOAT,
    response_type VARCHAR(50)
);

-- Verify table created
SHOW TABLES;
```

### 6. Get Your URL

1. Di Railway project → Select web service
2. Tab **"Settings"** → section **"Domains"**
3. Klik **"Generate Domain"**
4. URL akan seperti: `https://chatbot-si-production-xxxx.up.railway.app`

### 7. Test Live Chatbot! 🎉

Buka URL dan test:

- ✅ Basic questions
- ✅ Groq API responses
- ✅ Conversation history
- ✅ Database logging

---

## 🔧 Common Issues

### 1. "Application failed to respond"

**Fix:** Update `app.py` untuk baca PORT dari environment:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
```

### 2. "Database connection error"

**Fix:**

- Pastikan MySQL service running
- Check `DATABASE_URL` di environment variables
- Verify database connection code updated

### 3. "ModuleNotFoundError"

**Fix:**

- Pastikan `requirements.txt` lengkap
- Includes `gunicorn`
- Railway akan auto-install

---

## 📊 View Logs

```bash
# Install Railway CLI (optional)
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# View logs
railway logs
```

Atau di web: Project → Service → **"Deployments"** tab → Click deployment → **"View Logs"**

---

## 💰 Pricing

- **Starter Plan:** $5/month

  - 500 execution hours
  - $0.000231/GB-hour
  - Cukup untuk chatbot medium traffic

- **Tips:**
  - Start dengan $5 credit (gratis trial)
  - Monitor usage di dashboard
  - Optimize jika perlu

---

## 🎓 Updates & Maintenance

**Untuk update chatbot:**

```bash
# Make changes locally
git add .
git commit -m "Update feature X"
git push origin main

# Railway auto-deploys! ✨
```

**Monitor:**

- Metrics di Railway dashboard
- Check logs regularly
- Set up Slack/Discord notifications (optional)

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] MySQL database added
- [ ] Environment variables configured
- [ ] Database connection updated
- [ ] Tables created in MySQL
- [ ] Domain generated
- [ ] Live chatbot tested
- [ ] Logs checked for errors

---

## 🆘 Need Help?

- **Railway Docs:** [docs.railway.app](https://docs.railway.app)
- **Railway Discord:** [discord.gg/railway](https://discord.gg/railway)
- **Full Guide:** See `DEPLOYMENT_GUIDE.md`

---

**Selamat! Chatbot Anda sudah LIVE! 🚀**

Share URL dengan teman-teman dan dosen! 🎉

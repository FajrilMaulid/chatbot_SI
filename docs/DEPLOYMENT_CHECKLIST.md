# 📋 Pre-Deployment Checklist

Gunakan checklist ini sebelum deploy chatbot ke production.

---

## ✅ Code Preparation

- [ ] **Semua kode berfungsi lokal**  
      Test chatbot di local environment terlebih dahulu

- [ ] **Requirements lengkap**  
      Verify `requirements.txt` includes semua dependencies:

  - flask
  - flask-cors
  - scikit-learn
  - mysql-connector-python
  - numpy
  - pandas
  - groq
  - python-dotenv
  - cachetools
  - gunicorn

- [ ] **Procfile exists**  
      File `Procfile` dengan content: `web: gunicorn app:app`

- [ ] **Runtime specified**  
      File `runtime.txt` dengan Python version (e.g., `python-3.11.0`)

- [ ] **.gitignore configured**  
      Jangan commit:
  - `.env`
  - `__pycache__/`
  - `*.pyc`
  - `.venv/`

---

## 🔑 Environment Variables

Prepare environment variables yang diperlukan:

### Required:

- [ ] `GROQ_API_KEY` - API key dari console.groq.com
- [ ] `GROQ_MODEL` - Default: `llama-3.3-70b-versatile`
- [ ] `CONFIDENCE_THRESHOLD` - Default: `0.7`

### Optional (with defaults):

- [ ] `GROQ_TEMPERATURE` - Default: `0.7`
- [ ] `GROQ_MAX_TOKENS` - Default: `1024`
- [ ] `ENABLE_GROQ` - Default: `true`
- [ ] `ENABLE_CACHING` - Default: `true`
- [ ] `CACHE_TTL` - Default: `3600`
- [ ] `FLASK_ENV` - Set to `production` for deployment
- [ ] `FLASK_DEBUG` - Set to `false` for deployment

### Database (Platform-specific):

- [ ] **Railway**: `DATABASE_URL` (auto-injected)
- [ ] **Other**: Manual config
  - `MYSQL_HOST`
  - `MYSQL_USER`
  - `MYSQL_PASSWORD`
  - `MYSQL_DATABASE`
  - `MYSQL_PORT` (optional, default: 3306)

---

## 🗄️ Database Setup

- [ ] **Database created**  
      MySQL database dengan nama `chatbot_si` (atau custom name)

- [ ] **Tables created**

  ```sql
  CREATE TABLE IF NOT EXISTS chat_logs (
      id INT AUTO_INCREMENT PRIMARY KEY,
      user_message TEXT,
      bot_response TEXT,
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      confidence_score FLOAT,
      response_type VARCHAR(50)
  );
  ```

- [ ] **Connection tested**  
      Verify database accessible from hosting environment

---

## 📦 Git Repository

- [ ] **Repository initialized**

  ```bash
  git init
  ```

- [ ] **All files committed**

  ```bash
  git add .
  git commit -m "Initial commit for deployment"
  ```

- [ ] **Pushed to GitHub/GitLab**

  ```bash
  git remote add origin <repo-url>
  git push -u origin main
  ```

- [ ] **Sensitive files ignored**  
      Ensure `.env` is in `.gitignore`

---

## 🚀 Platform-Specific

### For Railway:

- [ ] Railway account created
- [ ] GitHub connected to Railway
- [ ] MySQL service added to project
- [ ] Environment variables configured
- [ ] Domain generated

### For Render:

- [ ] Render account created
- [ ] Repository connected
- [ ] Build command set: `pip install -r requirements.txt`
- [ ] Start command set: `gunicorn app:app`
- [ ] Database configured (external or Render PostgreSQL)

### For PythonAnywhere:

- [ ] PythonAnywhere account created
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] WSGI file configured
- [ ] Static files mapped

---

## 🧪 Testing

### Local Testing:

- [ ] **Start server locally**

  ```bash
  python app.py
  ```

- [ ] **Test basic questions**  
      "apa itu sistem informasi?"

- [ ] **Test Groq API**  
      Complex questions to trigger API

- [ ] **Test database logging**  
      Verify chat logs saved

### Post-Deployment Testing:

- [ ] **Health check**  
      Visit `/api/health` endpoint

- [ ] **Frontend loads**  
      Check if index.html renders properly

- [ ] **Chat works**  
      Send test messages

- [ ] **Database logs**  
      Verify chat logs being saved

- [ ] **Error handling**  
      Test with invalid inputs

---

## 🔒 Security

- [ ] **Debug mode OFF**  
      `FLASK_DEBUG=false` in production

- [ ] **Secret key secure**  
      Use strong random secret key

- [ ] **API keys protected**  
      Never expose in client-side code

- [ ] **CORS configured**  
      Set appropriate CORS policies

- [ ] **HTTPS enabled**  
      Most platforms provide free SSL

---

## 📊 Monitoring

- [ ] **Logs configured**  
      Know where to find application logs

- [ ] **Error tracking**  
      Set up error notifications (optional)

- [ ] **Usage monitoring**  
      Track Groq API usage

- [ ] **Database monitoring**  
      Monitor database size and performance

---

## 💰 Cost Check

- [ ] **Pricing plan confirmed**  
      Understand hosting costs

- [ ] **Groq API quota**  
      Be aware of API rate limits

- [ ] **Database size**  
      Monitor storage usage

- [ ] **Bandwidth**  
      Track traffic (if applicable)

---

## 📚 Documentation

- [ ] **README updated**  
      Include deployment instructions

- [ ] **Environment variables documented**  
      List all required env vars

- [ ] **Database schema documented**  
      SQL scripts for table creation

- [ ] **API endpoints documented**  
      List all available endpoints

---

## 🆘 Rollback Plan

- [ ] **Backup plan ready**  
      Know how to revert if deployment fails

- [ ] **Local version working**  
      Keep local version as backup

- [ ] **Database backup**  
      Export database before major changes

---

## ✅ Final Check

Before going live:

1. **Test thoroughly** - All features work as expected
2. **Monitor closely** - Watch logs for first few hours
3. **Share URL** - Distribute to users only after verification
4. **Document issues** - Note any problems for improvement

---

## 🎉 Ready to Deploy!

If all items are checked, you're ready to deploy your chatbot! 🚀

Choose your platform and follow the respective guide:

- **Railway**: See `RAILWAY_QUICKSTART.md`
- **Full Guide**: See `DEPLOYMENT_GUIDE.md`

Good luck!

---

**Last updated:** January 2026

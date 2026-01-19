# Security Guide - Chatbot SI

## 🔐 Security Best Practices

Panduan lengkap untuk mengamankan deployment chatbot SI Anda.

---

## 1. SECRET_KEY Management

### ⚠️ Mengapa SECRET_KEY Penting?

`SECRET_KEY` digunakan Flask untuk:

- **Enkripsi session cookies** - Melindungi data session user
- **CSRF Protection** - Mencegah serangan Cross-Site Request Forgery
- **Secure data signing** - Memvalidasi integritas data

Jika SECRET_KEY bocor, attacker bisa:

- Membajak session admin
- Membuat session palsu
- Bypass CSRF protection

### ✅ Cara Generate SECRET_KEY yang Aman

**Method 1: Menggunakan Utility Function (Recommended)**

```bash
python -c "from utils.security import generate_secret_key; print(generate_secret_key())"
```

**Method 2: Menggunakan Python Secrets Module**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Method 3: Menggunakan OpenSSL**

```bash
openssl rand -hex 32
```

### 🚫 Jangan Lakukan Ini:

- ❌ Menggunakan string sederhana: `SECRET_KEY=mypassword123`
- ❌ Menggunakan API key sebagai SECRET_KEY
- ❌ Commit file `.env` ke Git repository
- ❌ Share SECRET_KEY via email/chat

### ✅ Best Practices:

- ✅ Generate SECRET_KEY baru untuk setiap environment (dev, staging, prod)
- ✅ Minimal 64 karakter (32 bytes hex)
- ✅ Simpan di environment variables, bukan di code
- ✅ Rotate SECRET_KEY secara berkala (akan invalidate semua session)

---

## 2. Environment Variables Security

### File `.env` Protection

File `.env` berisi data sensitif seperti:

- SECRET_KEY
- Database credentials
- API keys (GROQ_API_KEY)

**Checklist:**

- [ ] File `.env` ada di `.gitignore`
- [ ] File `.env` TIDAK pernah di-commit ke Git
- [ ] Gunakan `.env.example` sebagai template (tanpa nilai sensitif)
- [ ] Setiap developer generate `.env` sendiri dari `.env.example`

### Membersihkan Git History (jika `.env` sudah pernah di-commit)

```bash
# WARNING: Ini akan rewrite Git history. Koordinasi dengan tim!

# Remove .env from all commits
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (DANGER!)
git push origin --force --all
```

**Alternatif yang lebih aman:**

- Rotate semua secrets (SECRET_KEY, database password, API keys)
- Anggap semua secrets lama sudah compromised

---

## 3. CORS (Cross-Origin Resource Sharing) Configuration

### Development vs Production

**Development:**

```python
CORS_ORIGINS = '*'  # Allow semua origins
```

**Production:**

```python
CORS_ORIGINS = ['https://yourdomain.com', 'https://www.yourdomain.com']
```

### Konfigurasi Production

Di file `.env` production, tambahkan:

```bash
ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
```

Atau set environment variable di hosting platform:

- **Railway**: Dashboard → Variables → Add `ALLOWED_ORIGINS`
- **PythonAnywhere**: Web tab → Environment variables

---

## 4. Debug Mode Security

### ⚠️ Bahaya Debug Mode di Production

Ketika `FLASK_DEBUG=true`:

- Stack traces ditampilkan ke user
- Environment variables bisa ter-expose
- Code paths bisa dilihat attacker
- Automatic reloader aktif (performance impact)

### ✅ Konfigurasi yang Benar

**Development (`.env`):**

```bash
FLASK_ENV=development
FLASK_DEBUG=true  # OK untuk development
```

**Production (environment variables):**

```bash
FLASK_ENV=production
FLASK_DEBUG=false  # WAJIB false!
```

---

## 5. Database Security

### Connection Security

**Development:**

```bash
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DATABASE=chatbot_si
```

**Production (Railway/Cloud):**

```bash
DATABASE_URL=mysql://user:password@host:port/database
```

### Best Practices:

- ✅ Gunakan user database dengan minimal privileges
- ✅ Password minimal 16 karakter random
- ✅ Enable MySQL SSL/TLS untuk production
- ✅ Restrict database access by IP (firewall)
- ✅ Regular backup database

---

## 6. Rate Limiting

### Development vs Production

**Development (`.env`):**

```bash
RATELIMIT_STORAGE_URL=memory://
```

**Production (dengan Redis):**

```bash
RATELIMIT_STORAGE_URL=redis://username:password@host:port
```

### Mengapa Redis untuk Production?

- Memory storage di-reset setiap app restart
- Tidak cocok untuk production dengan multiple instances
- Redis persistent dan shared across instances

### Setup Redis (Railway)

1. Add Redis service di Railway dashboard
2. Copy connection URL
3. Set `RATELIMIT_STORAGE_URL` environment variable

---

## 7. Security Headers (Talisman)

Aplikasi ini sudah menggunakan Flask-Talisman untuk security headers di production:

- **HTTPS Enforcement** - Force HTTPS redirect
- **HSTS** - HTTP Strict Transport Security
- **CSP** - Content Security Policy
- **X-Frame-Options** - Clickjacking protection

Headers ini otomatis aktif ketika `FLASK_ENV=production`.

---

## 8. Session Security

### Current Configuration

```python
SESSION_COOKIE_HTTPONLY = True      # Prevent JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'     # CSRF protection
SESSION_COOKIE_SECURE = True        # HTTPS only (production)
PERMANENT_SESSION_LIFETIME = 2 hours
```

### Recommendations:

- ✅ Session timeout setelah 2 jam inactivity
- ✅ HttpOnly cookie (prevent XSS)
- ✅ SameSite=Lax (prevent CSRF)
- ✅ Secure flag di production (HTTPS only)

---

## 9. Deployment Security Checklist

### Pre-Deployment

- [ ] Generate SECRET_KEY baru untuk production
- [ ] Set `FLASK_DEBUG=false`
- [ ] Configure `ALLOWED_ORIGINS` untuk CORS
- [ ] Setup Redis untuk rate limiting
- [ ] Review `.gitignore` contains `.env`
- [ ] Database credentials aman & unique
- [ ] Backup database production

### Hosting Platform Configuration

#### Railway

1. **Environment Variables:**

   ```
   SECRET_KEY=<generated-secure-key>
   FLASK_ENV=production
   FLASK_DEBUG=false
   DATABASE_URL=<railway-mysql-url>
   GROQ_API_KEY=<your-groq-key>
   ALLOWED_ORIGINS=https://yourdomain.com
   RATELIMIT_STORAGE_URL=redis://<railway-redis-url>
   ```

2. **SSL/TLS:** Otomatis provided oleh Railway

#### PythonAnywhere

1. **Environment Variables:** Set di Web tab
2. **HTTPS:** Requires paid plan atau custom domain
3. **MySQL:** Already included, update credentials

### Post-Deployment

- [ ] Test HTTPS redirect
- [ ] Verify CORS restrictions
- [ ] Test rate limiting
- [ ] Check error pages (no stack trace leak)
- [ ] Monitor logs untuk unauthorized access
- [ ] Setup uptime monitoring

---

## 10. Password Security

### Admin Password Requirements

Fungsi `check_password_strength()` di `utils/security.py` memeriksa:

- ✅ Minimal 8 karakter (recommended 12+)
- ✅ Uppercase letters
- ✅ Lowercase letters
- ✅ Numbers
- ✅ Special characters
- ✅ No common patterns

### Password Hashing

Aplikasi menggunakan **PBKDF2-SHA256** untuk hash password:

```python
from utils.security import hash_password, verify_password

hashed = hash_password("SecurePassword123!")
is_valid = verify_password("SecurePassword123!", hashed)
```

---

## 11. API Key Security (GROQ)

### Best Practices:

- ✅ Store di environment variable
- ✅ Jangan hardcode di code
- ✅ Jangan commit ke Git
- ✅ Rotate jika ter-expose
- ✅ Monitor usage di Groq dashboard

### Jika API Key Ter-Expose:

1. **Immediately revoke** di Groq dashboard
2. **Generate new** API key
3. **Update** environment variables di production
4. **Review logs** untuk suspicious activity
5. **Change** semua credentials yang mungkin related

---

## 12. Logging & Monitoring

### Security Events yang Di-log:

- ✅ Login attempts (success & failure)
- ✅ Logout events
- ✅ Rate limit exceeded
- ✅ Unauthorized access attempts
- ✅ Admin actions (CRUD operations)

### Log Files Location:

```
logs/
  ├── app.log          # General application logs
  ├── security.log     # Security-related events
  └── error.log        # Error logs
```

### Monitoring Recommendations:

- Monitor failed login attempts (brute force detection)
- Alert on repeated rate limit violations
- Track unusual admin activity patterns
- Regular security audit dari logs

---

## 13. Input Validation & Sanitization

### Sudah Diimplementasi:

- ✅ SQL Injection protection (parameterized queries)
- ✅ Username validation
- ✅ XSS protection (Flask auto-escaping)
- ✅ Filename sanitization
- ✅ URL validation (open redirect prevention)

### Functions Available:

```python
from utils.security import sanitize_filename, is_safe_redirect_url
from utils.validators import validate_username

# Sanitize filename
safe_name = sanitize_filename("../../etc/passwd")  # Returns "passwd"

# Validate redirect URL
is_safe = is_safe_redirect_url("/dashboard", allowed_hosts=['yourdomain.com'])

# Validate username
is_valid, msg = validate_username("admin123")
```

---

## 14. Backup & Disaster Recovery

### Regular Backups:

1. **Database:**

   ```bash
   mysqldump -u user -p chatbot_si > backup_$(date +%Y%m%d).sql
   ```

2. **Environment Config:**
   - Backup `.env` securely (encrypted)
   - Document all environment variables

3. **Application Code:**
   - Git repository (tanpa `.env`)
   - Tagged releases

### Recovery Plan:

1. Setup new instance di hosting platform
2. Restore database dari backup
3. Configure environment variables
4. Deploy latest stable release
5. Verify functionality

---

## 15. Security Testing

### Manual Tests:

```bash
# Test security module
python -c "from utils.security import generate_secret_key; print(len(generate_secret_key()))"

# Test application startup
python app.py

# Test import fixes
python -c "from utils.security import sanitize_filename; print(sanitize_filename('test/../file.txt'))"
```

### Checklist:

- [ ] SECRET_KEY properly configured
- [ ] Debug mode disabled in production
- [ ] CORS restrictions working
- [ ] Rate limiting functional
- [ ] Session security (HttpOnly, SameSite, Secure)
- [ ] HTTPS redirect working
- [ ] Error pages don't leak info
- [ ] Admin authentication required
- [ ] SQL injection protection
- [ ] XSS protection

---

## 16. Vulnerability Scanning

### Dependencies Security:

```bash
# Check for vulnerable packages
pip list --outdated

# Update dependencies
pip install --upgrade -r requirements.txt
```

### Regular Updates:

- [ ] Flask & extensions
- [ ] Database drivers
- [ ] Security libraries (Werkzeug, etc)
- [ ] Python version

---

## 17. Incident Response

### If Security Breach Suspected:

1. **Immediate Actions:**
   - Take application offline if critical
   - Revoke all API keys
   - Reset all passwords
   - Rotate SECRET_KEY

2. **Investigation:**
   - Review security logs
   - Identify breach vector
   - Assess data impact

3. **Remediation:**
   - Patch vulnerability
   - Update security measures
   - Restore from clean backup if needed

4. **Communication:**
   - Notify affected users
   - Document incident
   - Update security procedures

---

## 🆘 Need Help?

Jika menemukan security issue:

1. **JANGAN** publicly disclose di GitHub issues
2. **Contact** maintainer privately
3. **Provide** detailed information
4. **Wait** for patch before disclosure

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Guide](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Railway Security Docs](https://docs.railway.app/deploy/deployments)

---

**Last Updated:** 2026-01-20  
**Version:** 1.0

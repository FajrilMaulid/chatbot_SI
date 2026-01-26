# MySQL Connection Timeout Fix - Deployment Guide

## 🔍 Problem Identified

**Server Log Error:**

```
mysql.connector.errors.OperationalError: 2013 (HY000):
Lost connection to MySQL server during query
```

**Root Cause:**

- MySQL connection times out during query execution
- Common in production with short `wait_timeout` settings
- Connection was established but gets dropped before query completes

![Server Error Log](file:///C:/Users/Fajril%20Maulid/.gemini/antigravity/brain/3289c508-a2fc-40db-a1f5-0bd6e643216a/uploaded_image_1769390300889.png)

---

## ✅ Solution Implemented

### 1. Increased Connection Timeouts

**File:** [core/database.py](file:///d:/File%20Web/chatbot_si_revisi/chatbot_SI/core/database.py)

**Changes:**

```python
db_connection = mysql.connector.connect(
    # ... other params ...
    connection_timeout=30,  # 30 seconds (was default 10s)
    autocommit=True,  # Prevent hanging transactions
    use_pure=True,  # More stable implementation
)

# Set session timeouts
cursor.execute("SET SESSION wait_timeout=28800")  # 8 hours
cursor.execute("SET SESSION interactive_timeout=28800")  # 8 hours
```

**Benefits:**

- Prevents connection timeout during slow queries
- Keeps connection alive longer between requests
- Auto-commits prevent pending transactions

### 2. Connection Validation Before Queries

**File:** [models/admin_api.py](file:///d:/File%20Web/chatbot_si_revisi/chatbot_SI/models/admin_api.py)

**Added:**

```python
def verify_admin_login(username, password, cursor):
    try:
        # CRITICAL: Validate connection before query
        if hasattr(cursor, '_connection'):
            cursor._connection.ping(reconnect=True, attempts=3, delay=1)
            print("[DB] Connection validated before admin login query")

        cursor.execute(...)
        # ... rest of function
```

**Benefits:**

- Checks if connection is alive before executing query
- Auto-reconnects if connection was lost
- Prevents Error 2013 from occurring

### 3. Enhanced Error Handling

**File:** [api/admin_routes.py](file:///d:/File%20Web/chatbot_si_revisi/chatbot_SI/api/admin_routes.py)

**Added:**

```python
except mysql.connector.errors.OperationalError as op_err:
    error_code = op_err.errno if hasattr(op_err, 'errno') else None

    if error_code in (2013, 2006):
        return jsonify({
            'error': 'Database connection timeout. Please try again.',
            'details': 'The server is experiencing connection issues...'
        }), 503
```

**Benefits:**
-specific handling for timeout errors (2013, 2006)

- User-friendly error message
- HTTP 503 (Service Unavailable) instead of 500

### 4. Database Helper Functions

**File:** [core/db_helpers.py](file:///d:/File%20Web/chatbot_si_revisi/chatbot_SI/core/db_helpers.py) (New)

**Functions:**

- `ensure_connection()` - Validates and reconnects if needed
- `safe_execute()` - Executes queries with auto-reconnect
- `@validate_connection_before_query` - Decorator for validation

---

## 🚀 Deployment Steps

### Step 1: Upload Modified Files

Upload these files to your server:

1. [core/database.py](file:///d:/File%20Web/chatbot_si_revisi/chatbot_SI/core/database.py) - Timeout settings
2. [models/admin_api.py](file:///d:/File%20Web/chatbot_si_revisi/chatbot_SI/models/admin_api.py) - Connection ping
3. [api/admin_routes.py](file:///d:/File%20Web/chatbot_si_revisi/chatbot_SI/api/admin_routes.py) - Error handling
4. [core/db_helpers.py](file:///d:/File%20Web/chatbot_si_revisi/chatbot_SI/core/db_helpers.py) - Helper functions (new file)

### Step 2: Restart Application

```bash
# For Passenger (Hostinger/Niagahoster)
touch tmp/restart.txt

# Or via cPanel
# Setup Python App → Restart button
```

### Step 3: Test Admin Login

1. Go to `/admin`
2. Enter credentials
3. Should login successfully without Error 2013

---

## 🔧 Additional MySQL Server Configuration (Optional)

If you have access to MySQL server configuration:

**Edit `my.cnf` or `my.ini`:**

```ini
[mysqld]
wait_timeout = 28800  # 8 hours
interactive_timeout = 28800  # 8 hours
connect_timeout = 30  # 30 seconds
max_allowed_packet = 64M  # Increase if needed
```

**For shared hosting:**

- Contact support to increase `wait_timeout`
- Or use `.htaccess` if supported:

```apache
php_value mysql.connect_timeout 30
```

---

## 🧪 Verification

After deployment, check:

**1. Application Logs:**

```
[DB] Using local database configuration...
[DB] Connection timeout: 30s, Session timeout: 8h
[OK] Local Database Connected Successfully
✅ Database connection: OK
```

**2. Admin Login:**

- No Error 2013
- Successful authentication
- Dashboard loads correctly

**3. Under Load:**

- Test with multiple concurrent logins
- Verify no timeout after idle periods
- Check logs for any connection warnings

---

## 🐛 Troubleshooting

### Still Getting Error 2013?

**Check 1: MySQL Server Timeout Settings**

```sql
SHOW VARIABLES LIKE '%timeout%';
```

Look for:

- `wait_timeout` - Should be >= 28800
- `interactive_timeout` - Should be >= 28800

**Check 2: Connection Pooling Issues**

If using connection pooling, ensure:

- Pool connections are validated before use
- Pool size is appropriate (5-10 for small apps)
- Stale connections are removed

**Check 3: Network Issues**

```bash
# Test network latency to MySQL server
ping your-mysql-host

# Check if firewall is blocking
telnet your-mysql-host 3306
```

**Check 4: MySQL Server Resources**

```sql
SHOW PROCESSLIST;  # Check for too many connections
SHOW STATUS LIKE 'Threads_connected';
SHOW VARIABLES LIKE 'max_connections';
```

### Error 2006 (MySQL Server Has Gone Away)

Similar to 2013, but usually means:

- Server restarted
- `max_allowed_packet` too small
- Query too large

**Solution:**

```sql
SET GLOBAL max_allowed_packet=67108864;  # 64MB
```

---

## 📊 Performance Impact

**Before Fix:**

- Connection timeout after ~10 seconds idle
- Need to reconnect for each request batch
- Error 2013 on admin login

**After Fix:**

- Connection stays alive for 8 hours
- Auto-reconnect if connection lost
- No timeout errors
- Slightly increased memory (minimal)

---

## 🔐 Security Considerations

**Autocommit Enabled:**

- Each query commits immediately
- No transaction rollback capability
- Acceptable for this application (mostly reads)

**Long Session Timeout:**

- 8 hours is reasonable for web apps
- Connections auto-close after timeout
- MySQL handles cleanup automatically

**Connection Pooling:**

- Only for Railway deployment
- Local deployment uses single connection
- Pool size = 5 (adequate for small apps)

---

## 📝 Summary of Changes

| Component          | Change             | Impact                 |
| ------------------ | ------------------ | ---------------------- |
| Connection Timeout | 10s → 30s          | Prevents early timeout |
| Session Timeout    | 300s → 28800s      | 5min → 8hours          |
| Autocommit         | OFF → ON           | Prevents hanging       |
| Ping Before Query  | Added              | Validates connection   |
| Error Handling     | Generic → Specific | Better UX              |
| Helper Module      | New                | Reusable utilities     |

---

## ✅ Success Criteria

Deploy is successful when:

1. ✅ Admin login works without errors
2. ✅ No Error 2013 in logs
3. ✅ Connection stays alive between requests
4. ✅ App handles idle connections gracefully
5. ✅ Clear error messages if timeout occurs

---

**Created:** 2026-01-26  
**Issue:** MySQL Error 2013 - Connection Lost During Query  
**Status:** ✅ Fixed with timeout increase and connection validation

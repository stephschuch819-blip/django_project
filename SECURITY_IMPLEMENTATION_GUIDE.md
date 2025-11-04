# Security Implementation Guide

## 🎯 Overview

This guide covers all security improvements implemented in the DGLegacy Portal application.

---

## ✅ Implemented Security Features

### 1. **IDOR Protection** ✓
- Secure case retrieval with validation
- Authorization checks on all protected views
- Session validation and cleanup
- Security logging for suspicious access

### 2. **Password Hashing** ✓
- Django's PBKDF2-SHA256 password hashing
- Automatic hashing on model save
- Secure password verification
- Migration command for existing passwords

### 3. **Rate Limiting** ✓
- Login endpoint: 5 attempts per minute per IP
- Automatic blocking of excessive requests
- Prevents brute force attacks

### 4. **Security Headers** ✓
- Content Security Policy (CSP)
- HTTP Strict Transport Security (HSTS)
- Referrer Policy
- Permissions Policy
- X-Content-Type-Options
- X-Frame-Options
- Cross-Origin policies

### 5. **Enhanced Session Management** ✓
- 1-hour session timeout
- Session regeneration on login
- HTTP-only cookies
- Secure cookies (production)
- SameSite cookie protection
- Session expiry on browser close

### 6. **Security Logging** ✓
- Separate security log file
- IP address tracking
- Suspicious access logging
- Log rotation (10MB, 5 backups)

---

## 🚀 Deployment Steps

### Step 1: Hash Existing Passwords

**CRITICAL:** Run this before deploying to production.

```bash
# Dry run to see what will be changed
python manage.py hash_passwords --dry-run

# Actually hash the passwords
python manage.py hash_passwords
```

**Output:**
```
✓ Case DG-ABC123 already has hashed password
✓ Hashed password for case DG-XYZ789
============================================================
Total cases: 10
Already hashed: 3
Newly hashed: 7

Password hashing complete!
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**New dependency added:**
- `django-ratelimit==4.1.0` - Rate limiting

### Step 3: Update Environment Variables

Create/update `.env` file:

```env
# Required
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=your-database-url

# Cloudinary (for file uploads)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### Step 4: Verify Settings

Check `delegacy_portal/settings.py`:

```python
# In production, these should be:
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Step 5: Create Logs Directory

```bash
python setup_logs.py
```

### Step 6: Run Security Tests

```bash
python test_idor_protection.py
```

All tests should show `[PASS]`.

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 8: Run Migrations

```bash
python manage.py migrate
```

### Step 9: Deploy

Deploy to your hosting platform (Render, Heroku, etc.)

---

## 🔒 Security Features Details

### Password Hashing

**Implementation:**
```python
# In models.py
from django.contrib.auth.hashers import make_password

def save(self, *args, **kwargs):
    if self.password and not self.password.startswith('pbkdf2_sha256$'):
        self.password = make_password(self.password)
    super().save(*args, **kwargs)
```

**Usage in views:**
```python
from django.contrib.auth.hashers import check_password

if check_password(password, case.password):
    # Password is correct
```

**Algorithm:** PBKDF2-SHA256 with 600,000 iterations

### Rate Limiting

**Configuration:**
```python
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def beneficiary_login(request):
    # Login logic
```

**Limits:**
- Login: 5 attempts per minute per IP
- Blocks further attempts automatically
- Returns 429 Too Many Requests

**To add rate limiting to other views:**
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='10/h', method='POST')
def my_view(request):
    # Your view logic
```

### Security Headers

**Headers automatically added to all responses:**

1. **Content-Security-Policy**
   - Prevents XSS attacks
   - Restricts resource loading
   - Blocks inline scripts (with exceptions for CDNs)

2. **Strict-Transport-Security** (Production only)
   - Forces HTTPS for 1 year
   - Includes subdomains
   - HSTS preload enabled

3. **Referrer-Policy: same-origin**
   - Prevents referrer leakage

4. **Permissions-Policy**
   - Disables: geolocation, camera, microphone, payment, USB

5. **X-Content-Type-Options: nosniff**
   - Prevents MIME sniffing

6. **X-Frame-Options: DENY**
   - Prevents clickjacking

### Session Security

**Configuration:**
```python
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True  # Refresh on activity
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # Production only
SESSION_COOKIE_SAMESITE = 'Lax'
```

**Features:**
- Sessions expire after 1 hour of inactivity
- Session regenerated on login (prevents fixation)
- Automatic cleanup of invalid sessions
- HTTP-only cookies (prevents XSS theft)

---

## 🧪 Testing

### Manual Security Tests

#### 1. Test IDOR Protection
```bash
python test_idor_protection.py
```

Expected: All tests pass

#### 2. Test Rate Limiting
```bash
# Try to login 6 times rapidly
# 6th attempt should be blocked with 429 error
```

#### 3. Test Session Timeout
```bash
# Login
# Wait 1 hour
# Try to access dashboard
# Should redirect to login
```

#### 4. Test Security Headers
```bash
# In browser DevTools > Network
# Check response headers for:
# - Content-Security-Policy
# - Strict-Transport-Security (production)
# - X-Frame-Options
# - etc.
```

### Automated Tests

Create `portal/tests/test_security.py`:

```python
from django.test import TestCase, Client
from portal.models import BeneficiaryCase

class SecurityTests(TestCase):
    def test_password_hashing(self):
        """Test that passwords are hashed"""
        case = BeneficiaryCase.objects.create(
            beneficiary_name="Test User",
            beneficiary_email="test@example.com",
            deceased_name="Deceased",
            password="plaintext123"
        )
        # Password should be hashed
        self.assertTrue(case.password.startswith('pbkdf2_sha256$'))
        self.assertNotEqual(case.password, "plaintext123")
    
    def test_rate_limiting(self):
        """Test login rate limiting"""
        client = Client()
        # Make 6 login attempts
        for i in range(6):
            response = client.post('/login/', {
                'case_number': 'INVALID',
                'password': 'wrong'
            })
        # 6th attempt should be rate limited
        self.assertEqual(response.status_code, 429)
    
    def test_security_headers(self):
        """Test security headers are present"""
        client = Client()
        response = client.get('/login/')
        self.assertIn('Content-Security-Policy', response)
        self.assertIn('X-Frame-Options', response)
        self.assertEqual(response['X-Frame-Options'], 'DENY')
```

Run tests:
```bash
python manage.py test portal.tests.test_security
```

---

## 📊 Security Monitoring

### Log Files

**Location:** `logs/`

1. **security.log** - Security events
   - Failed login attempts
   - IDOR violations
   - Session anomalies
   - IP addresses

2. **application.log** - General events
   - Successful logins
   - Application errors
   - User actions

### Monitoring Commands

```bash
# View recent security events
tail -f logs/security.log

# Count failed login attempts today
grep "Invalid case number" logs/security.log | grep $(date +%Y-%m-%d) | wc -l

# Find suspicious IPs
grep "Suspicious" logs/security.log | awk '{print $NF}' | sort | uniq -c | sort -rn

# Monitor rate limiting
grep "429" logs/application.log
```

### Alerts to Set Up

1. **Multiple failed logins** (>10 per hour from same IP)
2. **IDOR attempts** (any "Suspicious access" log)
3. **Rate limit violations** (>5 per hour)
4. **Session anomalies** (invalid case_id in session)

---

## 🔧 Configuration Reference

### Production Settings Checklist

```python
# settings.py - Production Configuration

# Security
DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']  # From environment
ALLOWED_HOSTS = ['yourdomain.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ['DATABASE_URL'])
}
```

### Rate Limiting Configuration

Adjust in `views.py`:

```python
# Stricter limits
@ratelimit(key='ip', rate='3/m', method='POST', block=True)

# More lenient
@ratelimit(key='ip', rate='10/m', method='POST', block=True)

# Different keys
@ratelimit(key='user', rate='10/h')  # Per user
@ratelimit(key='header:x-real-ip', rate='5/m')  # Behind proxy
```

### CSP Configuration

Adjust in `settings.py`:

```python
# Stricter CSP (no inline scripts)
CSP_SCRIPT_SRC = ("'self'", "cdn.jsdelivr.net")

# Allow specific domains
CSP_SCRIPT_SRC = ("'self'", "https://trusted-cdn.com")

# Report violations
CSP_REPORT_URI = '/csp-report/'
```

---

## 🚨 Incident Response

### If Security Breach Detected

1. **Immediate Actions**
   ```bash
   # Check security logs
   tail -100 logs/security.log
   
   # Identify affected cases
   grep "case_id" logs/security.log
   
   # Force logout all users
   python manage.py shell
   >>> from django.contrib.sessions.models import Session
   >>> Session.objects.all().delete()
   ```

2. **Deactivate Compromised Cases**
   ```python
   case = BeneficiaryCase.objects.get(case_number='DG-123456')
   case.is_active = False
   case.save()
   ```

3. **Reset Passwords**
   ```python
   case.set_password('new-secure-password')
   case.save()
   ```

4. **Review Logs**
   - Check all access from suspicious IPs
   - Identify data accessed
   - Document timeline

5. **Notify Affected Users**

6. **Update Security Measures**

---

## 📋 Maintenance Schedule

### Daily
- [ ] Review security.log for anomalies
- [ ] Check failed login attempts

### Weekly
- [ ] Review rate limiting logs
- [ ] Check session statistics
- [ ] Update dependencies (if needed)

### Monthly
- [ ] Security audit
- [ ] Penetration testing
- [ ] Review and update security policies
- [ ] Dependency vulnerability scan

### Quarterly
- [ ] External security audit
- [ ] Update security documentation
- [ ] Security training
- [ ] Disaster recovery test

---

## 🔗 Additional Resources

### Django Security
- [Django Security Docs](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

### Tools
- **safety** - Dependency vulnerability scanner
- **bandit** - Python security linter
- **django-defender** - Additional brute force protection
- **django-axes** - Advanced login attempt tracking

### Commands
```bash
# Check for vulnerabilities
pip install safety
safety check

# Security linting
pip install bandit
bandit -r portal/

# Django security check
python manage.py check --deploy
```

---

## ✅ Final Checklist

Before going to production:

- [ ] Run `python manage.py hash_passwords`
- [ ] Run `python manage.py check --deploy`
- [ ] Set `DEBUG = False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set all environment variables
- [ ] Run security tests
- [ ] Create logs directory
- [ ] Test rate limiting
- [ ] Verify HTTPS is working
- [ ] Test session timeout
- [ ] Review security headers
- [ ] Set up log monitoring
- [ ] Configure backup system
- [ ] Document incident response plan
- [ ] Train team on security procedures

---

**Last Updated:** November 4, 2025  
**Version:** 2.0  
**Status:** Production Ready

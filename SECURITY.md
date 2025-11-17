# 🔒 Security Guidelines for NLQ Assistant

## CRITICAL: Never Commit These Files to GitHub!

The following files contain sensitive information and **MUST NOT** be committed:

```
❌ .env                 - API keys and database credentials
❌ .env.local          - Local environment variables
❌ db.sqlite3          - Production database
❌ *.key               - SSL/TLS keys
❌ *.pem               - Certificate files
❌ secrets.json        - Secret configurations
```

All these are already in `.gitignore` for protection.

---

## 🛡️ Environment Variables (Critical!)

### What Goes in .env?
```env
# API Keys (NEVER in code!)
GEMINI_API_KEY=your_actual_key_here
SECRET_KEY=your_secret_key_here

# Database Credentials (if using external DB)
DATABASE_PASSWORD=your_password_here

# AWS Keys (if using S3)
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
```

### Never Include In Code
❌ Database passwords in `settings.py`
❌ API keys in templates
❌ Secret keys in views.py
❌ Credentials in comments
❌ Any hardcoded sensitive values

---

## ✅ Before Committing to GitHub

### 1. Check Your .gitignore
```bash
# Verify .gitignore is in place
cat .gitignore | grep -E "\.env|\.key|db\.sqlite3"
```

### 2. Check What Will Be Committed
```bash
# See files that will be committed
git status

# Preview changes
git diff --cached
```

### 3. Remove Accidental Commits
```bash
# If you accidentally committed .env
git rm --cached .env
git commit -m "Remove .env file"

# Force removal from history (DANGEROUS - ask before doing this)
git filter-branch --tree-filter 'rm -f .env' -- --all
```

### 4. Use git-secrets (Recommended)
```bash
# Install git-secrets
brew install git-secrets  # macOS
# or download from https://github.com/awslabs/git-secrets

# Scan for secrets
git secrets --scan

# Prevent commits with secrets
git secrets --install
git secrets --register-aws  # Or other patterns
```

---

## 🔑 API Key Management

### Getting Your Gemini API Key
1. Visit https://ai.google.dev
2. Click "Get API Key"
3. Create new project or select existing
4. Generate API key
5. Copy to `.env` file (NOT in code)

### Protecting Your API Key
✅ Store in `.env` file
✅ Never commit `.env` to GitHub
✅ Use `.env.example` as template
✅ Rotate keys regularly
✅ Use different keys for dev/prod
✅ Monitor API usage
❌ Never hardcode in Python files
❌ Never paste in commits
❌ Never share in issues/PRs

---

## 🚨 If You Accidentally Commit a Secret

### Immediate Action (URGENT!)
```bash
# 1. Regenerate all exposed keys IMMEDIATELY
# - Get new Gemini API key
# - Generate new SECRET_KEY
# - Update database password

# 2. Revoke old credentials
# - Disable old API key
# - Reset passwords
# - Check audit logs

# 3. Remove from Git history
git filter-branch --tree-filter 'rm -f .env' HEAD
git push origin --force
```

### For Security Breaches
1. **Immediately revoke exposed secrets**
2. **Rotate all credentials**
3. **Review access logs**
4. **Check for unauthorized access**
5. **Enable 2FA if available**
6. **Notify administrators**

---

## 📋 Security Checklist

### Before Every Commit
- [ ] `.env` file NOT included
- [ ] No API keys in code
- [ ] No database passwords visible
- [ ] No hardcoded credentials
- [ ] `git status` looks clean
- [ ] `.gitignore` is in place

### Before First Deployment
- [ ] Create `.env` file from `.env.example`
- [ ] Generate new `SECRET_KEY`
- [ ] Get production Gemini API key
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Setup HTTPS certificate
- [ ] Enable CSRF protection
- [ ] Configure database securely
- [ ] Review security headers

### Regular Maintenance
- [ ] Rotate API keys quarterly
- [ ] Update dependencies monthly
- [ ] Review access logs
- [ ] Check for exposed secrets
- [ ] Update Django to latest version
- [ ] Review .gitignore regularly

---

## 🔐 Django Security Settings

### Production Settings (settings.py)
```python
# NEVER leave these in development mode!
DEBUG = False

# Must be a unique, random string
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')

# Set your domain
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
X_FRAME_OPTIONS = 'DENY'
```

### Load Environment Variables
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

# Get sensitive values from environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
```

---

## 📝 Security Best Practices

### 1. Code Review
- Review all code before committing
- Never commit credentials
- Check third-party dependencies
- Use security linters

### 2. Dependency Security
```bash
# Check for vulnerable packages
pip install safety
safety check

# Keep dependencies updated
pip list --outdated
pip install --upgrade -r requirements.txt
```

### 3. Database Security
- Use strong passwords
- Never commit `db.sqlite3`
- Use PostgreSQL in production
- Enable encryption at rest
- Regular backups with encryption

### 4. Authentication
- Enforce HTTPS in production
- Enable 2FA for GitHub account
- Use SSH keys for Git (no passwords)
- Limit API key scope
- Rotate keys regularly

### 5. Secrets Management
- Use environment variables
- Use `.gitignore` for sensitive files
- Use `.env.example` as template
- Different secrets per environment
- Never log sensitive values

---

## 🔍 How to Check if Secrets Are Exposed

### GitHub API
```bash
# Check public repositories
curl https://api.github.com/user/repos?type=public
```

### Git Log
```bash
# Check commit history
git log --all --oneline | grep -i secret
git log -p | grep -i "api_key\|password\|secret"
```

### GitHub Security Tab
1. Go to your repository
2. Click "Security"
3. Check "Secret scanning"
4. Review any alerts

---

## 📚 Additional Resources

### Security Tools
- [git-secrets](https://github.com/awslabs/git-secrets) - Prevent secrets in Git
- [safety](https://pyup.io/safety/) - Check vulnerable dependencies
- [bandit](https://github.com/PyCQA/bandit) - Find security issues in Python

### Django Security
- [Django Security Guide](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Django Security](https://owasp.org/www-project-django/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

### General Security
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Cybersecurity](https://www.nist.gov/cyberframework)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)

---

## ⚠️ Common Mistakes to Avoid

```python
# ❌ DON'T DO THIS
GEMINI_API_KEY = "sk-xyz123"  # Hardcoded!
SECRET_KEY = "my-secret-key"  # In code!
DATABASE_PASSWORD = "password123"  # Visible!

# ✅ DO THIS INSTEAD
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
```

```python
# ❌ DON'T commit these files
.env
db.sqlite3
*.pem
*.key
secrets.json

# ✅ Use .gitignore to prevent them
# All already configured in this project
```

---

## 🆘 Security Incident Response

### If You Find Exposed Secrets
1. **Stop all activity** - Don't use the exposed credentials
2. **Revoke immediately** - Cancel API keys, reset passwords
3. **Check logs** - Look for unauthorized access
4. **Clean history** - Remove from Git history
5. **Force push** - Update remote repository
6. **Notify users** - If applicable
7. **Review process** - Prevent future incidents

### Contact Security Team
- GitHub Security: security@github.com
- Google Cloud: cloud-security@google.com
- Your organization's security team

---

## 📞 Support

For security concerns:
1. Check [SECURITY.md](./SECURITY.md) (this file)
2. Review `.gitignore` configuration
3. Check `.env.example` template
4. Consult Django security docs
5. Contact your security team

---

## ✅ Summary

**REMEMBER:**
- ✅ Use `.env` for secrets
- ✅ Use `.gitignore` for protection
- ✅ Never commit sensitive files
- ✅ Use `.env.example` as template
- ✅ Rotate keys regularly
- ✅ Check before every commit
- ✅ Store credentials securely

**Questions?** See this file or consult `.env.example`

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Status**: Production Guidelines ✅

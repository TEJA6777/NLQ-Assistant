# ⚡ QUICK START - Run in 5 Minutes

## 🔴 IMPORTANT: Security Fix Applied!

The exposed API key in `.env.example` has been removed and replaced with a placeholder.
**NEVER commit real API keys to GitHub!**

---

## 🚀 Run These Commands (Copy & Paste)

### Windows (PowerShell)
```powershell
# 1. Create .env file
cp .env.example .env

# 2. Setup virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python manage.py migrate

# 5. Start server
python manage.py runserver
```

### Mac/Linux
```bash
# 1. Create .env file
cp .env.example .env

# 2. Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python manage.py migrate

# 5. Start server
python manage.py runserver
```

---

## ✏️ Edit `.env` File

Open `.env` in your editor and replace:
```
GEMINI_API_KEY=your_actual_api_key_here_do_not_commit_real_key
```

With your actual key from: **https://ai.google.dev**

---

## 🌐 Open in Browser

```
http://localhost:8000
```

---

## ✅ You're Done!

- Upload CSV files
- Ask questions in natural language
- See results instantly

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **HOW_TO_RUN.md** | Detailed setup guide (READ THIS!) |
| **README.md** | Project overview |
| **GUIDE.md** | Complete documentation |
| **SECURITY.md** | Security guidelines |

---

**Start querying! 🎉**

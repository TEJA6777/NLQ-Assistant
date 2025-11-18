# 🚀 How to Run NLQ Assistant

## ⚠️ IMPORTANT SECURITY NOTE
Your `.env.example` contains an exposed API key! Follow these steps immediately:

---

## Step 1: Fix Security (CRITICAL!)

### Replace the exposed API key in `.env.example`:
```bash
<<<<<<< HEAD
=======

>>>>>>> 2a8f426 (uploading into rendering)
# To this:
GEMINI_API_KEY=your_actual_api_key_here_get_from_google_ai_dev
```

**Why?** If someone finds this in your GitHub, they can use your API and incur charges!

---

## Step 2: Setup Your Environment

### 1. Create `.env` file from template
```bash
cp .env.example .env
```

### 2. Get your own API key
- Go to: https://ai.google.dev
- Click "Get API Key"
- Create new project or select existing
- Copy your API key

### 3. Add your API key to `.env`
Edit the `.env` file (NOT `.env.example`):
```
GEMINI_API_KEY=your_actual_api_key_here
```

---

## Step 3: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

---

## Step 4: Initialize Database

```bash
python manage.py migrate
```

---

## Step 5: Run the Server

```bash
python manage.py runserver
```

**Output:**
```
Starting development server at http://127.0.0.1:8000/
```

---

## Step 6: Open in Browser

Visit: **http://localhost:8000**

---

## ✅ You're Ready!

1. **Upload CSV file** - Click "Upload Dataset" button
2. **Ask questions** - Type natural language queries
3. **View results** - See formatted results in chat

---

## 📁 Project Files

| File | What it is |
|------|-----------|
| `README.md` | Project overview |
| `GUIDE.md` | Full documentation |
| `SETUP.md` | Quick setup guide |
| `SECURITY.md` | Security best practices |
| `.env.example` | Configuration template |
| `.env` | Your actual config (NOT in git) |

---

## 🐛 Troubleshooting

### Styles not loading?
- Clear browser cache (Ctrl+F5)
- Check internet (needs Tailwind CSS CDN)

### API key errors?
- Verify `.env` has GEMINI_API_KEY
- Ensure key is valid from Google

### Port already in use?
```bash
python manage.py runserver 8001  # Use different port
```

### Database errors?
```bash
python manage.py migrate
```

### Reset everything?
```bash
rm db.sqlite3
python manage.py migrate
python manage.py runserver
```

---

## 📚 Documentation

- **README.md** - Quick start & overview
- **GUIDE.md** - Comprehensive guide with all details
- **SECURITY.md** - Security guidelines
- **SETUP.md** - 2-minute setup

---

**Now you're all set! Start querying! 🎉**

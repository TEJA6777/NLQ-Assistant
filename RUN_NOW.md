# 🚀 Copy & Paste Commands - Get Running in 5 Minutes

## ✅ Everything is already configured!

All you need to do is:
1. Add your API key to `.env`
2. Run these commands

---

## 🔑 Step 1: Get Your API Key

1. Go to: **https://ai.google.dev**
2. Click "**Get API Key**"
3. Create a new project (or use existing)
4. **Copy the API key**
5. Open `.env` file in any text editor
6. Find this line:
   ```
   GEMINI_API_KEY=your_actual_api_key_here_do_not_commit_real_key
   ```
7. Replace with your actual key:
   ```
   GEMINI_API_KEY=AIza...yourkeyherexxxxxxxx
   ```
8. **Save the file**

---

## 💻 Step 2: Copy & Paste These Commands

### For Windows (PowerShell):

```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install packages
pip install -r requirements.txt

# Create database
python manage.py migrate

# Run the server
python manage.py runserver
```

### For Mac/Linux:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Create database
python manage.py migrate

# Run the server
python manage.py runserver
```

---

## 🌐 Step 3: Open in Browser

```
http://localhost:8000
```

---

## ✅ You're Done!

Now you can:
1. **Upload CSV/Excel files**
2. **Ask questions in natural language**
3. **See results instantly**

---

## 📚 If You Need Help

| Question | File to Read |
|----------|-------------|
| "How do I get started?" | START_HERE.md |
| "What's the full setup?" | HOW_TO_RUN.md |
| "What's already done?" | PROJECT_STATUS.md |
| "Tell me everything" | GUIDE.md |
| "Security questions?" | SECURITY.md |

---

## 🔴 Common Issues & Fixes

### Virtual environment not activating?
```powershell
# Try this instead
& ".\venv\Scripts\Activate.ps1"
```

### "Port 8000 already in use"?
```bash
python manage.py runserver 8001
```

### "Module not found"?
```bash
# Make sure venv is activated
venv\Scripts\activate
pip install -r requirements.txt
```

### "No such table"?
```bash
python manage.py migrate
```

### API key not working?
- Check `.env` file
- Make sure you saved it
- Verify key is from Google (https://ai.google.dev)
- Key should have no extra spaces

---

## 🎉 That's It!

Your app is running and ready to use! 🚀

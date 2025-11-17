# 🚀 NLQ Assistant - Natural Language Query Engine

A powerful Django web application that converts natural language queries into SQL and executes them on uploaded datasets. Powered by Google Gemini AI.

**Author**: Kodati Sai Teja  
**Email**: saitejakodati6777@gmail.com  
**GitHub**: https://github.com/TEJA6777/NLQ-Assistant  

---

## ✨ Features

### Core Functionality
- **🗣️ Natural Language Queries** - Ask in English, no SQL needed
- **🤖 AI-Powered** - Google Gemini AI converts queries to SQL automatically
- **📊 Multi-Dataset Support** - Upload and manage multiple CSV/Excel files
- **💾 Chat History** - Persistent conversation per dataset
- **📈 Data Operations** - SELECT, INSERT, UPDATE, DELETE via natural language

### User Interface
- **🎨 Modern Design** - Professional, responsive Tailwind CSS interface
- **📱 Fully Responsive** - Mobile, tablet, and desktop compatible
- **💬 Chat Interface** - Intuitive conversational UI
- **📂 Database Sidebar** - Quick access to tables and columns
- **⚡ Zero Dependencies** - CDN-based styling (no npm needed)

---

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.8+
- Django 3.2+
- Google Gemini API key

### Installation Steps

1. **Clone repository**
   ```bash
   git clone https://github.com/TEJA6777/NLQ-Assistant.git
   cd NLQ-Assistant
   ```

2. **Create & activate virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment (⚠️ IMPORTANT)**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

5. **Initialize database**
   ```bash
   python manage.py migrate
   ```

6. **Run server**
   ```bash
   python manage.py runserver
   # Visit http://localhost:8000
   ```

---

## 📱 Pages Overview

| Page | URL | Purpose |
|------|-----|---------|
| **Home** | `/` | Landing page, feature showcase |
| **Query Interface** | `/query/` | Main chat interface (sidebar + chat) |
| **Upload** | `/upload/` | Drag-and-drop file upload |
| **Results** | `/results/` | Query results with SQL display |

---

## 🔐 Security

### Environment Variables
- **NEVER** commit `.env` file (contains API keys)
- Use `.env.example` as template only
- `.gitignore` automatically protects `.env`
- Regenerate API keys if accidentally exposed

### API Key Protection
1. Create `.env` from `.env.example`
2. Add your actual GEMINI_API_KEY
3. Never share or commit `.env`
4. Rotate keys regularly if needed

See **SECURITY.md** for complete security guide.

---

## 📁 Project Structure

```
nlq_project/
├── README.md                    # This file
├── GUIDE.md                     # Comprehensive guide
├── SECURITY.md                  # Security guidelines
├── requirements.txt             # Python dependencies
├── .env.example                 # Configuration template
├── .gitignore                   # Git protection
├── manage.py                    # Django CLI
├── db.sqlite3                   # Database
│
├── templates/                   # 7 HTML templates
│   ├── base.html               # Base with Tailwind CSS
│   ├── home.html               # Landing page
│   ├── query.html              # Main chat interface ⭐
│   ├── upload.html             # File upload
│   ├── error.html              # Error handling
│   ├── results.html            # Results display
│   └── index.html              # Welcome page
│
├── query_app/                   # Django app
│   ├── views.py                # Page logic
│   ├── models.py               # Database models
│   ├── forms.py                # HTML forms
│   └── urls.py                 # URL routing
│
└── nlq_project/                 # Django config
    ├── settings.py             # Settings
    ├── urls.py                 # Main URLs
    └── wsgi.py                 # Production
```

---

## 🛠️ Technology Stack

- **Backend**: Django 3.2+, Python 3.8+
- **AI**: Google Gemini API
- **Frontend**: Tailwind CSS (CDN), Font Awesome icons
- **Database**: SQLite3 (default), PostgreSQL (optional)
- **Data**: pandas, sqlparse

---

## 📊 Usage Examples

### Upload a CSV File
1. Click **"Upload Dataset"** button
2. Drag file or select from computer
3. Choose CSV or Excel format
4. System auto-creates table and detects columns

### Ask a Query
1. Select dataset from left sidebar
2. Type in chat box: *"Show me all records where status is pending"*
3. AI converts to SQL automatically
4. View results in formatted table
5. Results stored in chat history

### Clear History
- Click **"Clear Chat"** button
- Deletes conversation history only
- Dataset remains unchanged

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Styles not loading | Clear browser cache, hard refresh (Ctrl+F5) |
| Icons not showing | Verify internet connection (needs CDN) |
| API key errors | Check `.env` file has GEMINI_API_KEY |
| Database errors | Run `python manage.py migrate` |
| File upload fails | Check file size < 10MB |

---

## 🚀 Deployment

### Development
```bash
python manage.py runserver
# http://localhost:8000
```

### Production
1. Set `DEBUG = False` in settings.py
2. Collect static files: `python manage.py collectstatic`
3. Configure `ALLOWED_HOSTS`
4. Use PostgreSQL database
5. Enable HTTPS

---

## 👤 Author & Contact

**Name**: Kodati Sai Teja  
**Email**: saitejakodati6777@gmail.com  
**GitHub**: https://github.com/TEJA6777  
**Repository**: https://github.com/TEJA6777/NLQ-Assistant  

---

## 📄 License

[Your License Here]

---

## 📚 More Information

See **GUIDE.md** for comprehensive documentation including:
- Detailed feature explanations
- Customization guide
- Design specifications
- Deployment options
- And more!

---

**Ready to query with natural language? Get started now! 🎉**

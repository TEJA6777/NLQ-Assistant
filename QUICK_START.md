# 🚀 NLQ Assistant - Quick Start Guide

## Installation & Setup (5 minutes)

### 1. Activate Virtual Environment
```powershell
cd d:\Google Hackathon\nlq_project
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies (if not already done)
```powershell
pip install -r requirements.txt
```

### 3. Create `.env` File
Create a file named `.env` in the project root with:
```
GEMINI_API_KEY=your_api_key_here
DEBUG=True
SECRET_KEY=django-insecure-test-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

**Get your free API key:**
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key to your `.env` file

### 4. Run Migrations
```powershell
python manage.py migrate
```

### 5. Start the Server
```powershell
python manage.py runserver
```

### 6. Open in Browser
```
http://localhost:8000
```

---

## 🎯 Website Structure

Your website now has:

### **Left Sidebar**
- NLQ logo and title
- List of all uploaded databases
- Upload Dataset button
- Clear Chat button

### **Top Navigation**
- Home - Landing page
- About - About the project
- Features - Feature overview
- Contact - Contact form

### **Main Pages**

#### 📍 Home Page (`/`)
- Hero section with overview
- Quick statistics
- Call-to-action buttons

#### 💬 Chat Page (`/query/`)
- Beautiful chat interface
- Natural language input
- Real-time results
- Conversation history
- Database selector

#### 📤 Upload Page
- Drag-and-drop file upload
- CSV/Excel support
- Automatic table creation

#### ℹ️ About Page (`/about/`)
- Project mission
- Key features
- Technology stack

#### ✨ Features Page (`/features/`)
- Detailed feature breakdown
- How it works
- Supported queries
- Example queries

#### 📧 Contact Page (`/contact/`)
- Contact form
- Support information
- FAQ section

---

## 📊 Upload Data

### Supported Formats
- CSV files (.csv)
- Excel files (.xls, .xlsx)

### How to Upload
1. Click "Upload Dataset" in sidebar or on Home page
2. Select your file (drag-and-drop supported)
3. Click "Upload & Process"
4. Your database appears in the sidebar

### Example CSV Format
```
ID,Name,Age,City
1,John,28,New York
2,Jane,32,Los Angeles
3,Bob,45,Chicago
```

---

## 💬 Ask Questions

### Natural Language Examples
- "Show me all records"
- "Count records by city"
- "Find records where age > 30"
- "Group by city and count"
- "Show top 10 entries"
- "Update status to active"
- "Delete records older than 2020"

### Supported Query Types
- **SELECT**: View and filter data
- **COUNT**: Count records
- **GROUP BY**: Group and aggregate
- **ORDER BY**: Sort results
- **WHERE**: Apply conditions
- **INSERT**: Add new records
- **UPDATE**: Modify records
- **DELETE**: Remove records
- **ALTER**: Modify table structure

---

## 🔧 Troubleshooting

### Problem: Server won't start
**Solution**: 
- Check that virtual environment is activated
- Verify Python 3.8+ is installed
- Run `pip install -r requirements.txt`

### Problem: API key error
**Solution**:
- Create `.env` file with GEMINI_API_KEY
- Get key from https://makersuite.google.com/app/apikey
- Restart the server after adding key

### Problem: Can't upload files
**Solution**:
- Check `media/datasets/` folder exists
- Verify file format is CSV or Excel
- Check file size < 50MB

### Problem: Chat not working
**Solution**:
- Select a database first
- Verify database was uploaded successfully
- Check GEMINI_API_KEY is valid

---

## 📁 Project Layout

```
nlq_project/
├── 📄 WEBSITE_GUIDE.md        (Comprehensive guide)
├── 📄 QUICK_START.md          (This file)
├── 📄 manage.py
├── 📄 requirements.txt
├── 📄 db.sqlite3              (Database)
├── 📄 .env                    (Your API key - keep secret!)
│
├── 📁 templates/              (HTML pages)
│   ├── base.html             (Main layout)
│   ├── home.html             (Home page)
│   ├── query.html            (Chat page)
│   ├── about.html            (About page)
│   ├── features.html         (Features page)
│   ├── contact.html          (Contact page)
│   └── upload.html           (Upload page)
│
├── 📁 query_app/              (Django app)
│   ├── views.py              (Page logic)
│   ├── urls.py               (URL routing)
│   ├── models.py             (Database models)
│   ├── forms.py              (Django forms)
│   └── migrations/           (Database migrations)
│
├── 📁 nlq_project/            (Django config)
│   ├── settings.py           (Settings)
│   ├── urls.py               (Main URLs)
│   └── wsgi.py
│
└── 📁 media/                  (Uploaded files)
    └── datasets/             (Your CSV/Excel files)
```

---

## 🎨 UI Features

### Beautiful Design
- Modern gradient backgrounds
- Smooth animations
- Responsive layout
- Professional color scheme

### User-Friendly
- Sidebar for easy navigation
- One-click database switching
- Clear visual hierarchy
- Helpful icons

### Interactive
- Real-time chat interface
- Auto-scrolling messages
- Loading indicators
- Error messages

---

## 🔐 Security

**Your data is safe:**
- Data stored locally on your server
- No data sent to external databases
- Only queries sent to Gemini AI
- All processing is server-side

**Keep secure:**
- Don't share your `.env` file
- Keep API key confidential
- Use HTTPS in production

---

## 📱 Responsive Design

Works perfectly on:
- ✅ Desktop computers
- ✅ Tablets
- ✅ Mobile phones

The sidebar collapses on smaller screens for better mobile experience.

---

## 🎓 Next Steps

1. **Upload your first dataset**
   - Go to Home page
   - Click "Upload Dataset"
   - Select your CSV/Excel file

2. **Ask a question**
   - Go to Chat page
   - Select your database
   - Type a natural language question

3. **Explore the AI**
   - Try different query types
   - See how it handles complex requests
   - Discover the capabilities

4. **Read the documentation**
   - Check WEBSITE_GUIDE.md for detailed info
   - Visit Features page for examples
   - Check Contact page for FAQ

---

## 🆘 Need Help?

1. **Check the Contact page** - Has FAQ section
2. **Review WEBSITE_GUIDE.md** - Comprehensive documentation
3. **Check logs** - Django prints helpful error messages
4. **Test the API key** - Ensure GEMINI_API_KEY is valid

---

## 🚀 Ready to Go!

Your NLQ Assistant website is now fully functional and ready to use!

**Start with:**
```powershell
python manage.py runserver
```

Then visit: **http://localhost:8000**

Happy querying! 🎉

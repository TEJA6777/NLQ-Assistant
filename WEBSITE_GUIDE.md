# NLQ Assistant - Fully Functional Website Guide

## 🎉 Your Website is Now Complete!

Your Natural Language Query Assistant website has been completely redesigned with a professional, fully functional interface. Here's what you've got:

---

## ✨ What's New

### 1. **Professional Layout**
- **Left Sidebar**: Displays all your uploaded databases and tables in an organized list
  - Click on any database to select it and start chatting
  - Shows database name and table name for easy identification
  - "Upload Dataset" button for quick file uploads
  - "Clear Chat" button to reset conversation

- **Top Navigation Bar**: Professional header with navigation links
  - Home - Main page with overview
  - About - Learn about the NLQ Assistant
  - Features - Detailed feature descriptions
  - Contact - Contact form and support information

- **Main Content Area**: Responsive and clean interface for all pages

### 2. **Home Page**
- Eye-catching hero section with project overview
- Quick statistics showing value proposition
- Call-to-action buttons to start using the app

### 3. **Chat Interface** (Query Page)
- Beautiful chat-like interface for natural language queries
- User messages appear in blue bubbles on the right
- Bot responses appear in gray bubbles on the left
- Shows SQL queries that were generated (educational)
- Auto-scrolls to latest messages
- Formatted data tables for displaying results

### 4. **Upload Functionality**
- New upload page with drag-and-drop support
- File selection with visual feedback
- Automatic table creation from CSV/Excel files
- Supported formats: CSV, XLS, XLSX

### 5. **Additional Pages**
- **About Page**: Information about the project and features
- **Features Page**: Detailed breakdown of all capabilities with examples
- **Contact Page**: Contact form with FAQ section

---

## 🚀 How to Use

### Step 1: Start the Server
```powershell
cd d:\Google Hackathon\nlq_project
python manage.py runserver
```

### Step 2: Configure Your API Key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

Get your free Gemini API key from: https://makersuite.google.com/app/apikey

### Step 3: Upload Your Data
1. Go to the chat page or click "Upload Dataset" in the sidebar
2. Select a CSV or Excel file
3. The system will automatically create a table

### Step 4: Ask Questions
1. Select your database from the left sidebar
2. Type a natural language query in the chat input
3. Get instant results with formatted tables

### Step 5: Multiple Databases
- Upload as many datasets as you want
- Switch between them using the left sidebar
- Each database maintains its own conversation history

---

## 📁 File Structure

```
nlq_project/
├── templates/
│   ├── base.html          ← Main layout with sidebar and navbar
│   ├── home.html          ← Home page
│   ├── query.html         ← Chat interface (FULLY FUNCTIONAL)
│   ├── about.html         ← About page
│   ├── features.html      ← Features page
│   ├── contact.html       ← Contact page
│   ├── upload.html        ← Upload interface
│   ├── index.html         ← Legacy (still works)
│   ├── results.html       ← Results page
│   └── error.html         ← Error page
├── query_app/
│   ├── views.py           ← Updated with new view functions
│   ├── urls.py            ← Updated with all routes
│   ├── models.py          ← Database models
│   ├── forms.py           ← Django forms
│   └── migrations/
├── nlq_project/
│   ├── settings.py        ← Django settings
│   ├── urls.py            ← Main URL routing
│   └── wsgi.py
├── media/
│   └── datasets/          ← Uploaded files stored here
├── db.sqlite3             ← SQLite database
├── manage.py              ← Django management
└── requirements.txt       ← Python dependencies
```

---

## 🔗 URL Routes

| Route | Page | Feature |
|-------|------|---------|
| `/` | Home | Landing page |
| `/about/` | About | About the project |
| `/features/` | Features | Feature details |
| `/contact/` | Contact | Contact form |
| `/query/` | Chat | Main chat interface |
| `/process_query/` | Backend | Process natural language queries |
| `/clear_conversation/` | Backend | Clear chat history |

---

## 🎯 Key Features Now Working

### ✅ Database Management
- [x] Upload CSV/Excel files
- [x] Automatic table creation
- [x] Display database list in sidebar
- [x] Select database to chat with
- [x] Multiple database support

### ✅ Chat Interface
- [x] Beautiful chat UI with messages
- [x] Natural language to SQL conversion
- [x] Direct Gemini AI integration
- [x] Formatted result tables
- [x] Conversation history
- [x] Auto-scrolling chat

### ✅ Navigation
- [x] Top navigation bar
- [x] Sidebar database list
- [x] Page routing working
- [x] Active page highlighting
- [x] Upload button integration

### ✅ Data Operations
- [x] SELECT queries
- [x] Data filtering
- [x] Aggregations (COUNT, SUM, etc.)
- [x] Sorting and grouping
- [x] INSERT/UPDATE/DELETE support

---

## 🛠️ Technical Details

### Backend
- **Framework**: Django 3.2.20
- **Database**: SQLite
- **AI**: Google Gemini 2.0 Flash
- **Data Processing**: Pandas, SQLParse

### Frontend
- **Framework**: Tailwind CSS
- **Icons**: Font Awesome 6.4.0
- **Styling**: Custom CSS with gradients and animations

### Features
- Responsive design
- Mobile-friendly
- Real-time chat interface
- Automatic SQL generation
- Result formatting

---

## 🔒 Security Notes

1. **Data Security**: Your data stays on your server
2. **API Key**: Keep your Gemini API key in `.env` file
3. **Database**: SQLite database is local
4. **No External Data Transfer**: Only queries are sent to Gemini AI

---

## 📝 Example Queries

Try asking:
- "Show me all records"
- "Count records by city"
- "Find the top 10 entries"
- "What's the average value?"
- "Filter records where status is active"
- "Group by department and count"

---

## 🐛 Troubleshooting

### Issue: Upload button not working
- Make sure `media/datasets/` folder exists
- Check that `MEDIA_ROOT` is configured in settings.py

### Issue: Chat not responding
- Verify GEMINI_API_KEY is set in `.env`
- Check that the API key is valid
- Ensure your database is selected

### Issue: Database not showing in sidebar
- Verify the upload was successful
- Check that the file was saved to `media/datasets/`
- Refresh the page

### Issue: Tables not displaying
- Ensure your CSV/Excel file has proper headers
- Check that file format is supported (CSV, XLS, XLSX)
- Verify the data isn't corrupted

---

## 📚 Django Management Commands

```powershell
# Run migrations
python manage.py migrate

# Create superuser (for admin panel)
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Run development server
python manage.py runserver 0.0.0.0:8000

# Access admin panel
# http://localhost:8000/admin/
```

---

## 🚀 Production Deployment

For production, consider:

1. **Update Settings**:
   - Set `DEBUG = False`
   - Update `SECRET_KEY`
   - Set proper `ALLOWED_HOSTS`

2. **Use Production Server**:
   - Gunicorn: `gunicorn nlq_project.wsgi`
   - Waitress: `waitress-serve --port 8000 nlq_project.wsgi:application`

3. **Database**:
   - Use PostgreSQL instead of SQLite
   - Implement proper backups

4. **Security**:
   - Use HTTPS
   - Set CSRF protections
   - Implement rate limiting

---

## 📞 Support

For issues or questions:
- Check the FAQ on the Contact page
- Review the Features page for examples
- Check Django logs for errors

---

## 🎓 Learning Resources

- Django Docs: https://docs.djangoproject.com/
- Tailwind CSS: https://tailwindcss.com/
- Google Gemini API: https://makersuite.google.com/
- SQLParse: https://sqlparse.readthedocs.io/

---

**Your NLQ Assistant is ready to use! Start uploading your data and asking questions in natural language.** 🎉

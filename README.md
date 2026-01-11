# 🚀 NLQ Assistant - Natural Language Query Engine

A powerful Django web application that converts natural language queries into SQL and executes them on uploaded datasets. Powered by Google Gemini AI.

**Author**: Kodati Sai Teja  
**Email**: saitejakodati6777@gmail.com  
**GitHub**: https://github.com/TEJA6777/NLQ-Assistant

---

## ✨ Features

### Core Functionality
- **🗣️ Natural Language Queries** - Ask questions in plain English, no SQL knowledge required
- **🤖 AI-Powered** - Google Gemini AI automatically converts queries to SQL
- **📊 Multi-Dataset Support** - Upload and manage multiple CSV/Excel files
- **💾 Chat History** - Persistent conversation history per dataset
- **📈 Data Operations** - Supports SELECT, INSERT, UPDATE, DELETE operations
- **🔍 Advanced Queries** - Aggregations, filtering, sorting, grouping, and complex queries

### User Interface
- **🎨 Modern Design** - Professional, responsive Tailwind CSS interface
- **📱 Fully Responsive** - Works seamlessly on mobile, tablet, and desktop
- **💬 Chat Interface** - Intuitive conversational UI with message bubbles
- **📂 Database Sidebar** - Quick access to tables and columns
- **⚡ Zero Dependencies** - CDN-based styling (no npm/build process needed)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Django 3.2 or higher
- Google Gemini API key ([Get one here](https://ai.google.dev))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/TEJA6777/NLQ-Assistant.git
   cd NLQ-Assistant
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables** ⚠️ IMPORTANT
   ```bash
   # Create .env file from template
   cp .env.example .env
   
   # Edit .env and add your API key
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   
   **Get your API key:**
   - Visit https://ai.google.dev
   - Click "Get API Key"
   - Create a new project or select existing
   - Copy your API key to `.env` file

5. **Initialize database**
   ```bash
   python manage.py migrate
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   
   Visit **http://localhost:8000** in your browser

---

## 📖 Usage Guide

### Uploading Data

1. Click **"Upload Dataset"** button in the sidebar or on the home page
2. Drag and drop your CSV/Excel file or click to browse
3. Select your file (supports `.csv`, `.xls`, `.xlsx`)
4. Click **"Upload & Process"**
5. Your dataset will appear in the sidebar and be ready to query

**Supported formats:**
- CSV files (`.csv`)
- Excel files (`.xls`, `.xlsx`)
- Maximum file size: 10MB

### Asking Questions

1. **Select a dataset** from the left sidebar (click on it)
2. **Type your question** in natural language in the chat input box
   - Example: *"Show me all records where age is greater than 30"*
   - Example: *"Count the number of records by city"*
   - Example: *"Find the top 10 entries sorted by salary"*
3. **Press Enter** or click **Send**
4. **View results** - The AI converts your question to SQL and displays results in a formatted table
5. **Chat history** - All queries and responses are saved for context

### Example Queries

- *"Show me all records"*
- *"Count records by city"*
- *"Find records where age > 30"*
- *"Group by department and show average salary"*
- *"Show top 10 entries sorted by date"*
- *"Update status to active where id is 5"*
- *"Delete records older than 2020"*

### Clearing Chat History

- Click **"Clear Chat"** button to delete conversation history for the current dataset
- Dataset data remains unchanged (no data loss)

---

## 📁 Project Structure

```
nlq_project/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
│
├── nlq_project/              # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── query_app/                # Main Django application
│   ├── __init__.py
│   ├── models.py             # Database models (Dataset, Conversation)
│   ├── views.py              # View functions
│   ├── urls.py               # App URL routing
│   ├── forms.py              # Django forms
│   ├── admin.py              # Django admin configuration
│   └── migrations/           # Database migrations
│
├── templates/                # HTML templates
│   ├── base.html             # Base template with Tailwind CSS
│   ├── home.html             # Landing page
│   ├── query.html            # Main chat interface ⭐
│   ├── upload.html           # File upload page
│   ├── results.html          # Results display page
│   ├── error.html            # Error handling page
│   └── about.html, features.html, contact.html  # Additional pages
│
├── static/                   # Static files (CSS, JS, images)
├── media/                    # Uploaded files
│   └── datasets/             # CSV/Excel files stored here
│
└── scripts/                  # Helper scripts (optional)
    ├── diagnose.py           # System diagnostic tool
    └── cleanup_db.py         # Database cleanup utility
```

---

## 🛠️ Technology Stack

- **Backend**: Django 4.2.6, Python 3.8+
- **AI/ML**: Google Gemini API (gemini-2.0-flash)
- **Frontend**: Tailwind CSS (CDN), Font Awesome icons
- **Database**: SQLite3 (default), PostgreSQL (production)
- **Data Processing**: pandas, sqlparse
- **Environment**: python-dotenv

---

## 📱 Pages Overview

| Page | URL | Description |
|------|-----|-------------|
| **Home** | `/` | Landing page with feature showcase |
| **Query Interface** | `/query/` | Main chat interface (sidebar + chat) |
| **Upload** | `/upload/` | Drag-and-drop file upload page |
| **Results** | `/results/` | Query results with SQL display |
| **About** | `/about/` | Project information and overview |
| **Features** | `/features/` | Detailed feature descriptions |
| **Contact** | `/contact/` | Contact form and support information |

---

## 🔐 Security

### Environment Variables

**⚠️ NEVER commit the `.env` file to version control!**

The `.env` file contains sensitive information:
- `GEMINI_API_KEY` - Your Google Gemini API key
- `SECRET_KEY` - Django secret key (for production)
- `DEBUG` - Debug mode setting
- `ALLOWED_HOSTS` - Allowed hostnames

### Best Practices

1. ✅ Always use `.env.example` as a template
2. ✅ Keep `.env` in `.gitignore` (already configured)
3. ✅ Never share or commit API keys
4. ✅ Use different keys for development and production
5. ✅ Rotate keys regularly if needed
6. ✅ Set `DEBUG=False` in production

### Production Deployment

Before deploying to production:
1. Set `DEBUG = False` in `settings.py`
2. Generate a new `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` with your domain
4. Use PostgreSQL or another production database
5. Enable HTTPS
6. Set up proper static file serving
7. Configure environment variables on your hosting platform

---

## 🚀 Deployment

### Development

```bash
python manage.py runserver
# Server runs at http://localhost:8000
```

### Production (Render.com)

1. **Connect Repository**
   - Connect your GitHub repository to Render

2. **Create Web Service**
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --no-input`
   - Start Command: `gunicorn nlq_project.wsgi:application`

3. **Environment Variables**
   - `DEBUG=False`
   - `SECRET_KEY=your-secure-random-key`
   - `GEMINI_API_KEY=your-gemini-api-key`
   - `ALLOWED_HOSTS=your-service-name.onrender.com`

4. **Deploy**
   - Render will automatically build and deploy your application

### Production (Other Platforms)

For Heroku, AWS, DigitalOcean, etc.:
1. Install dependencies from `requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Collect static files: `python manage.py collectstatic`
4. Set environment variables
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Configure static files serving
7. Use a production database (PostgreSQL recommended)

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Styles not loading** | Clear browser cache (Ctrl+F5 or Cmd+Shift+R), check internet connection (needs Tailwind CDN) |
| **Icons not showing** | Verify internet connection (Font Awesome via CDN) |
| **API key errors** | Check `.env` file exists and contains `GEMINI_API_KEY`, verify key is valid |
| **Database errors** | Run `python manage.py migrate` to apply migrations |
| **File upload fails** | Check file size (< 10MB), verify file format (CSV/Excel), check `media/datasets/` folder exists |
| **Port already in use** | Use different port: `python manage.py runserver 8001` |
| **Import errors** | Activate virtual environment, install dependencies: `pip install -r requirements.txt` |

### Reset Everything

If you need to start fresh:
```bash
# Delete database
rm db.sqlite3  # Linux/Mac
del db.sqlite3  # Windows

# Recreate database
python manage.py migrate

# Start server
python manage.py runserver
```

### Diagnostic Tools

Use the diagnostic script to check system status:
```bash
python scripts/diagnose.py
```

This will check:
- API key configuration
- API connectivity
- Database status
- Uploaded datasets
- System health

---

## 📊 Usage Examples

### Upload a CSV File
1. Navigate to the upload page or click "Upload Dataset"
2. Select your CSV file
3. Click "Upload & Process"
4. File is processed and table is created automatically

### Ask a Query
1. Select dataset from sidebar
2. Type: *"Show me all customers from New York"*
3. AI converts to: `SELECT * FROM customers WHERE city='New York'`
4. Results displayed in formatted table
5. Query saved in chat history

### Complex Queries
- *"Group by department and calculate average salary"*
- *"Show top 5 products by sales volume"*
- *"Find records where date is between 2023-01-01 and 2023-12-31"*
- *"Count distinct values in category column"*

---

## 🧪 Testing

### Test API Key
```bash
python scripts/test_your_key.py
```

### Test API Connection
```bash
python scripts/test_api.py
```

---

## 📝 Development

### Running Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

### Django Admin
Access admin panel at: `http://localhost:8000/admin/`

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 👤 Author & Contact

**Name**: Kodati Sai Teja  
**Email**: saitejakodati6777@gmail.com  
**GitHub**: https://github.com/TEJA6777  
**Repository**: https://github.com/TEJA6777/NLQ-Assistant

---

## 📄 License

This project is open source and available for personal and educational use.

---

## 🙏 Acknowledgments

- Google Gemini AI for natural language processing
- Django team for the excellent framework
- Tailwind CSS for beautiful styling
- Font Awesome for icons

---

**Ready to query with natural language? Get started now! 🎉**

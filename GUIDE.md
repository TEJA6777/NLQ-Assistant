# 📖 NLQ Assistant - Comprehensive Guide

Complete documentation for the NLQ Assistant project.

**Table of Contents**
1. [Getting Started](#getting-started)
2. [Features in Detail](#features-in-detail)
3. [User Guide](#user-guide)
4. [Developer Guide](#developer-guide)
5. [Customization](#customization)
6. [Deployment](#deployment)
7. [FAQ & Troubleshooting](#faq--troubleshooting)

---

## Getting Started

### Installation (Full Steps)

1. **Clone repository**
   ```bash
   git clone https://github.com/TEJA6777/NLQ-Assistant.git
   cd NLQ-Assistant
   ```

2. **Setup Python environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (Mac/Linux)
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key** ⚠️ IMPORTANT
   ```bash
   # Copy template
   cp .env.example .env
   
   # Edit .env file and add:
   GEMINI_API_KEY=your_actual_api_key_from_google
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   # Server runs at http://localhost:8000
   ```

---

## Features in Detail

### 1. Natural Language to SQL Conversion

**What it does**: Converts natural language questions to SQL queries automatically.

**How to use**:
- Type: *"Show all customers from New York"*
- System converts to: `SELECT * FROM customers WHERE city='New York'`
- Results displayed in formatted table

**Supported queries**:
- SELECT queries (filtering, sorting)
- COUNT and aggregations
- INSERT operations
- UPDATE operations
- DELETE operations (with caution)

### 2. Multi-Dataset Management

**Upload Files**:
- Click "Upload Dataset" button
- Drag and drop CSV or Excel file
- Auto-creates database table
- Auto-detects column types

**Switch Between Datasets**:
- Left sidebar shows all datasets
- Click dataset name to switch
- Each dataset has separate chat history

**View Columns**:
- Click dataset to expand column list
- Shows column names and types
- First 5 columns visible, "+N more" for additional

### 3. Chat Interface

**User Messages** (Blue bubbles, right-aligned)
- Natural language questions
- Multiple queries in conversation
- Easily reference previous messages

**Bot Responses** (Gray bubbles, left-aligned)
- AI-generated SQL query
- Results in formatted table
- Error messages if query fails

**Clear History**:
- Click "Clear Chat" button
- Deletes all messages for current dataset
- Dataset data remains unchanged

### 4. Modern UI/UX

**Responsive Design**:
- Mobile phones (< 768px)
- Tablets (768-1024px)
- Desktop screens (> 1024px)

**Design Elements**:
- Gradient buttons with hover effects
- Professional color scheme (blue & indigo)
- Smooth animations
- Font Awesome icons throughout

**Zero Dependencies**:
- Tailwind CSS via CDN (no npm install)
- Font Awesome icons via CDN
- No build process needed
- Instant styling

---

## User Guide

### Uploading Data

1. **Supported Formats**:
   - CSV (.csv)
   - Excel (.xls, .xlsx)
   - Maximum size: 10MB

2. **Upload Steps**:
   - Click "Upload Dataset" in left sidebar
   - Drag file onto upload zone OR click to browse
   - Select file from computer
   - Click "Upload & Process"
   - System redirects to chat with new dataset

3. **What Happens**:
   - File is parsed
   - Table created in database
   - Columns auto-detected
   - Dataset available immediately

### Querying Data

1. **Select Dataset**:
   - Click dataset in left sidebar
   - Dataset becomes active (highlighted blue)
   - Chat history for that dataset loads

2. **Write Query**:
   - Click in message input box
   - Type natural language question
   - Example: "Show me top 10 records"

3. **Send Query**:
   - Press Enter or click Send button
   - AI processes query
   - Converts to SQL
   - Results display in table
   - Added to chat history

4. **View Results**:
   - Results appear in formatted table
   - Blue gradient header
   - Click row for more details
   - Horizontal scroll on mobile

### Managing Conversations

**Clear Chat**:
- Click "Clear Chat" button
- Deletes all messages for current dataset
- Dataset data intact (no data lost)
- Chat history deleted

**Save Important Queries**:
- Copy SQL from response
- Save to notes
- Results can be exported manually

---

## Developer Guide

### Project Structure

**App Directory**: `query_app/`
- `views.py` - Page logic and data processing
- `models.py` - Database models (Dataset, Conversation)
- `forms.py` - Django forms for input
- `urls.py` - URL routing
- `admin.py` - Django admin interface

**Templates**: `templates/`
- `base.html` - Base template with Tailwind CSS
- `query.html` - Main chat interface
- `home.html` - Landing page
- `upload.html` - File upload page
- `results.html` - Results display
- `error.html` - Error handling
- `index.html` - Welcome page

**Configuration**: `nlq_project/`
- `settings.py` - Django settings
- `urls.py` - Main URL configuration
- `wsgi.py` - Production deployment

### Key Models

**Dataset**:
```python
class Dataset(models.Model):
    name = CharField()  # Dataset name
    table_name = CharField()  # SQL table name
    columns = JSONField()  # Column information
    created_at = DateTimeField()
```

**Conversation**:
```python
class Conversation(models.Model):
    dataset = ForeignKey(Dataset)
    user_query = TextField()  # Natural language query
    sql_query = TextField()  # Generated SQL
    response = TextField()  # Query results
    timestamp = DateTimeField()
```

### API Key Integration

The app uses Google Gemini API for NLP:

```python
# In views.py
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
```

### Adding Features

**Add New Template**:
1. Create file in `templates/`
2. Extend `base.html`
3. Use Tailwind CSS classes
4. Add Font Awesome icons

**Add New View**:
1. Create function in `views.py`
2. Add route in `urls.py`
3. Create template in `templates/`

**Modify Styling**:
1. Edit `templates/base.html`
2. Change Tailwind classes
3. Or add custom CSS in `<style>` tag

---

## Customization

### Change Colors

Edit `templates/base.html` style section:

```html
<!-- Find these and change -->
<style>
  /* Primary color */
  .btn-primary {
    @apply bg-gradient-to-r from-blue-600 to-blue-700;
  }
  
  /* Change from-blue-600 to your color */
  /* from-red-600, from-green-600, from-purple-600, etc. */
</style>
```

Color options: red, blue, green, purple, pink, yellow, indigo

### Change Layout Width

In `templates/query.html`:
```html
<!-- Left sidebar width -->
<div class="w-72">  <!-- Change 72 to 80, 96, etc. -->

<!-- Corresponds to: -->
<!-- w-72 = 18rem = 288px -->
<!-- w-80 = 20rem = 320px -->
<!-- w-96 = 24rem = 384px -->
```

### Change Icons

All icons use Font Awesome. Find and replace:
```html
<!-- Current -->
<i class="fas fa-database"></i>

<!-- Change to any Font Awesome icon -->
<i class="fas fa-[icon-name]"></i>

<!-- Examples: fa-home, fa-user, fa-cog, fa-trash, etc. -->
```

### Add Custom Fonts

In `templates/base.html`:
```html
<!-- Add to <head> -->
<link href="https://fonts.googleapis.com/css2?family=YourFont&display=swap" rel="stylesheet">

<!-- Update CSS -->
body {
  font-family: 'YourFont', sans-serif;
}
```

---

## Deployment

### Development Server
```bash
python manage.py runserver
# http://localhost:8000
```

### Production Deployment

**1. Update Settings**
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'your-secret-key-here'  # Or use environment variable
```

**2. Collect Static Files**
```bash
python manage.py collectstatic
```

**3. Database Setup**
- Change from SQLite to PostgreSQL (recommended)
- Create database and migrations

**4. Web Server**
Options: Gunicorn, uWSGI, Apache, Nginx

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn nlq_project.wsgi:application
```

**5. Security**
- Enable HTTPS (SSL certificate)
- Set CSRF protection
- Configure CORS if needed
- Regular backups

**6. Hosting Options**
- Heroku (easiest for beginners)
- AWS (most flexible)
- DigitalOcean (good balance)
- Google Cloud
- Azure

---

## FAQ & Troubleshooting

### Q: API key errors?
**A**: Check `.env` file exists and has GEMINI_API_KEY set correctly.

### Q: Styles not loading?
**A**: 
- Clear browser cache
- Hard refresh (Ctrl+F5 or Cmd+Shift+R)
- Check internet connection (needs CDN)

### Q: Icons not displaying?
**A**:
- Verify Font Awesome CDN working
- Check browser console for errors
- Try different browser

### Q: File upload fails?
**A**:
- File size < 10MB
- Supported format (CSV or Excel)
- Check browser console for errors

### Q: SQL errors in results?
**A**:
- Check column names match file
- Query might need adjustment
- Try simpler query first

### Q: Database errors?
**A**:
```bash
# Reset database (deletes all data!)
python manage.py migrate --fake-initial
python manage.py migrate

# Or use Django admin to manage
python manage.py createsuperuser
# Visit /admin/
```

### Q: How to reset everything?
**A**:
```bash
# Delete database
rm db.sqlite3

# Create new database
python manage.py migrate

# Restart server
python manage.py runserver
```

### Q: How to backup data?
**A**:
```bash
# Export data to JSON
python manage.py dumpdata > backup.json

# Import from JSON
python manage.py loaddata backup.json
```

---

## Security Best Practices

1. **API Keys**
   - Never commit `.env` file
   - Use `.env.example` as template
   - Regenerate if exposed

2. **Database**
   - Don't expose credentials
   - Use strong passwords
   - Regular backups

3. **File Upload**
   - Validate file types
   - Limit file size
   - Scan for malware

4. **SQL Injection**
   - App uses parameterized queries
   - Additional validation recommended for production

5. **HTTPS**
   - Enable in production
   - Use SSL certificate
   - Redirect HTTP to HTTPS

See **SECURITY.md** for complete security guide.

---

## Support & Contact

**Author**: Kodati Sai Teja  
**Email**: saitejakodati6777@gmail.com  
**GitHub**: https://github.com/TEJA6777/NLQ-Assistant  

---

**Version**: 1.0  
**Status**: Production Ready ✅  
**Last Updated**: November 2025  

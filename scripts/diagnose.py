#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nlq_project.settings')
django.setup()

from query_app.models import Dataset, Conversation
from django.db import connection
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*60)
print("NLQ ASSISTANT - SYSTEM DIAGNOSTIC")
print("="*60 + "\n")

# 1. Check API Key
api_key = os.getenv('GEMINI_API_KEY')
print("1. API KEY STATUS:")
if api_key:
    print(f"   ✓ API Key found: {api_key[:15]}...{api_key[-5:]}")
else:
    print(f"   ✗ API Key NOT found in .env")

# 2. Test API
print("\n2. API CONNECTIVITY:")
try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Test")
    print(f"   ✓ Gemini API is working")
except Exception as e:
    print(f"   ✗ API Error: {str(e)}")

# 3. Check Databases
print("\n3. UPLOADED DATASETS:")
datasets = Dataset.objects.all()
if datasets.count() > 0:
    for ds in datasets:
        print(f"   ✓ {ds.name} (Table: {ds.table_name})")
else:
    print(f"   ⚠ No datasets uploaded yet")

# 4. Check Conversations
print("\n4. CONVERSATIONS:")
conversations = Conversation.objects.all()
print(f"   Total conversations: {conversations.count()}")
if conversations.count() > 0:
    latest = conversations.latest('created_at')
    print(f"   Latest: {latest.user_query[:50]}...")

# 5. Check Database Tables
print("\n5. DATABASE TABLES:")
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
django_tables = [t[0] for t in tables if t[0].startswith('django') or t[0].startswith('auth') or t[0].startswith('query')]
user_tables = [t[0] for t in tables if not t[0].startswith('django') and not t[0].startswith('auth') and not t[0].startswith('query')]

print(f"   Django tables: {len(django_tables)}")
if user_tables:
    print(f"   User tables ({len(user_tables)}):")
    for table in user_tables:
        print(f"     - {table}")
else:
    print(f"   User tables: None")

print("\n" + "="*60 + "\n")

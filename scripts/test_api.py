#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nlq_project.settings')
django.setup()

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
print(f"Testing API Key: {api_key[:15] if api_key else 'NOT FOUND'}...")

if not api_key:
    print("✗ ERROR: API key not found in .env file")
    sys.exit(1)

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Say 'Hello' only")
    print(f"✓ API is working!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ API Error: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

#!/usr/bin/env python
import google.generativeai as genai

api_key = "AIzaSyDXv9DWK0Z6UHQsnuMS4e0HSFF3XJgY8Mc"
print(f"Testing API Key: {api_key[:15]}...")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Say 'API Key is valid and working!' in one sentence")
    print(f"\n✓ SUCCESS! API Key is VALID and WORKING!")
    print(f"\nAPI Response: {response.text}")
except Exception as e:
    print(f"\n✗ ERROR! API Key is NOT working")
    print(f"Error: {str(e)}")

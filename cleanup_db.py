#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nlq_project.settings')
django.setup()

from query_app.models import Dataset, Conversation
from django.db import connection

# Delete all conversations
Conversation.objects.all().delete()
print("✓ Deleted all conversations")

# Drop all existing tables
cursor = connection.cursor()
datasets = Dataset.objects.all()
for dataset in datasets:
    try:
        cursor.execute(f'DROP TABLE IF EXISTS "{dataset.table_name}"')
        print(f"✓ Dropped table: {dataset.table_name}")
    except Exception as e:
        print(f"✗ Could not drop table {dataset.table_name}: {e}")

# Delete all datasets
count = Dataset.objects.count()
Dataset.objects.all().delete()
print(f"✓ Deleted {count} datasets")

print("\n✓ Database cleaned successfully! Now only upload new data.")

from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow per-user datasets
    name = models.CharField(max_length=255)
    table_name = models.CharField(max_length=255)
    columns = models.JSONField()
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    user_query = models.TextField()
    sql_query = models.TextField(blank=True, null=True)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

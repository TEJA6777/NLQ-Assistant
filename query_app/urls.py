from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process_query/', views.process_query, name='process_query'),  # Renamed for clarity
    path('query/', views.query_interface, name='query_interface'),
    path('clear_conversation/', views.clear_conversation, name='clear_conversation'),  # Added clear chat
    path('results/', views.query_results, name='query_results'),
]

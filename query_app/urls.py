from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('contact/', views.contact, name='contact'),
    path('process_query/', views.process_query, name='process_query'),
    path('query/', views.query_interface, name='query_interface'),
    path('clear_conversation/', views.clear_conversation, name='clear_conversation'),
    path('results/', views.query_results, name='query_results'),
]

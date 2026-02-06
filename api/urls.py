"""
API URLs
"""
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # ML Endpoints
    path('recommendations/', views.crop_recommendation_api, name='crop_recommendation'),
    path('yield-prediction/', views.yield_prediction_api, name='yield_prediction'),
    path('disease-risk/', views.disease_prediction_api, name='disease_risk'),
    
    # Chatbot - TEMPORAIREMENT DÉSACTIVÉ
    # path('chatbot/', views.chatbot_api, name='chatbot'),
    
    # Data Endpoints
    path('crops/', views.crops_list_api, name='crops_list'),
    path('market-prices/', views.market_prices_api, name='market_prices'),
    
    # User Endpoints
    path('user-stats/', views.user_stats_api, name='user_stats'),
    
    # Health Check
    path('health/', views.health_check, name='health_check'),
]

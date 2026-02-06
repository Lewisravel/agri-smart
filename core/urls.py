"""
Core URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('recommend/', views.crop_recommendation, name='crop_recommendation'),
    path('yield-prediction/', views.yield_prediction, name='yield_prediction'),
    path('farm/<int:farm_id>/', views.farm_detail, name='farm_detail'),
    path('market-prices/', views.market_prices_view, name='market_prices'),
    path('visualizations/', views.visualization_view, name='visualizations'),
    path('preferences/update/', views.update_preferences, name='update_preferences'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('chatbot/', views.chatbot_view, name='chatbot'), 
]

"""
Core Views - Main application views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Sum, Count
from datetime import datetime, timedelta
import json

from .models import Farm, Crop, CropSeason, WeatherData, Prediction, MarketPrice, UserPreference
from ml_models.predictor import CropRecommender, YieldPredictor
from ml_models.visualizer import DataVisualizer


def index(request):
    """Page d'accueil"""
    context = {
        'total_crops': Crop.objects.count(),
        'total_users': Farm.objects.values('user').distinct().count(),
        'total_predictions': Prediction.objects.count(),
    }
    return render(request, 'core/index.html', context)


@login_required
def dashboard(request):
    """Tableau de bord utilisateur"""
    user_farms = Farm.objects.filter(user=request.user)
    
    # Statistiques
    total_area = user_farms.aggregate(Sum('area_hectares'))['area_hectares__sum'] or 0
    active_seasons = CropSeason.objects.filter(
        farm__user=request.user,
        actual_harvest_date__isnull=True
    ).count()
    
    # Dernières saisons
    recent_seasons = CropSeason.objects.filter(
        farm__user=request.user
    ).select_related('farm', 'crop')[:5]
    
    # Prédictions récentes
    recent_predictions = Prediction.objects.filter(
        user=request.user
    )[:5]
    
    context = {
        'farms': user_farms,
        'total_area': total_area,
        'active_seasons': active_seasons,
        'recent_seasons': recent_seasons,
        'recent_predictions': recent_predictions,
    }
    
    return render(request, 'core/dashboard.html', context)


def crop_recommendation(request):
    """Vue pour recommandation de cultures"""
    if request.method == 'POST':
        # Récupérer les données du formulaire
        data = {
            'temperature': float(request.POST.get('temperature')),
            'humidity': float(request.POST.get('humidity')),
            'rainfall': float(request.POST.get('rainfall')),
            'soil_ph': float(request.POST.get('soil_ph')),
            'soil_type': request.POST.get('soil_type'),
            'region': request.POST.get('region'),
        }
        
        # Faire la prédiction
        recommender = CropRecommender()
        recommendations = recommender.recommend(data)
        
        # Sauvegarder la prédiction seulement si l'utilisateur est connecté
        if request.user.is_authenticated:
            farm_id = request.POST.get('farm_id')
            farm = None
            if farm_id:
                farm = get_object_or_404(Farm, id=farm_id, user=request.user)
            
            Prediction.objects.create(
                user=request.user,
                farm=farm,
                prediction_type='CROP_RECOMMENDATION',
                input_data=data,
                output_data=recommendations,
                confidence_score=recommendations[0].get('confidence', 0) if recommendations else 0
            )
        
        context = {
            'recommendations': recommendations,
            'input_data': data,
        }
        return render(request, 'core/recommendation_results.html', context)
    
    # GET request
    farms = []
    if request.user.is_authenticated:
        farms = Farm.objects.filter(user=request.user)
    
    crops = Crop.objects.all()
    
    context = {
        'farms': farms,
        'crops': crops,
    }
    return render(request, 'core/crop_recommendation.html', context)

def yield_prediction(request):
    """Vue pour prédiction de rendement"""
    if request.method == 'POST':
        # Récupérer les données du formulaire
        data = {
            'crop': request.POST.get('crop'),
            'area_hectares': float(request.POST.get('area_hectares')),
            'temperature': float(request.POST.get('temperature')),
            'rainfall': float(request.POST.get('rainfall')),
            'soil_ph': float(request.POST.get('soil_ph')),
            'fertilizer_npk': float(request.POST.get('fertilizer_npk', 0)),
            'irrigation': request.POST.get('irrigation') == 'true',
        }
        
        # Faire la prédiction
        predictor = YieldPredictor()
        prediction = predictor.predict(data)
        
        # Sauvegarder la prédiction si l'utilisateur est connecté
        if request.user.is_authenticated:
            farm_id = request.POST.get('farm_id')
            farm = None
            if farm_id:
                farm = get_object_or_404(Farm, id=farm_id, user=request.user)
            
            Prediction.objects.create(
                user=request.user,
                farm=farm,
                prediction_type='YIELD_PREDICTION',
                input_data=data,
                output_data=prediction,
                confidence_score=prediction.get('confidence', 0)
            )
        
        context = {
            'prediction': prediction,
            'input_data': data,
        }
        return render(request, 'core/yield_results.html', context)
    
    # GET request
    farms = []
    if request.user.is_authenticated:
        farms = Farm.objects.filter(user=request.user)
    
    crops = Crop.objects.all()
    
    context = {
        'farms': farms,
        'crops': crops,
    }
    return render(request, 'core/yield_prediction.html', context)

def farm_detail(request, farm_id):
    """Détails d'une ferme"""
    farm = get_object_or_404(Farm, id=farm_id, user=request.user)
    
    # Saisons de culture
    seasons = CropSeason.objects.filter(farm=farm).select_related('crop')
    
    # Données météo récentes
    weather_data = WeatherData.objects.filter(
        farm=farm,
        date__gte=datetime.now() - timedelta(days=30)
    ).order_by('-date')
    
    # Statistiques
    avg_yield = seasons.filter(yield_kg_per_ha__isnull=False).aggregate(
        Avg('yield_kg_per_ha')
    )['yield_kg_per_ha__avg'] or 0
    
    total_production = seasons.aggregate(Sum('total_production_kg'))['total_production_kg__sum'] or 0
    
    context = {
        'farm': farm,
        'seasons': seasons,
        'weather_data': weather_data,
        'avg_yield': avg_yield,
        'total_production': total_production,
    }
    
    return render(request, 'core/farm_detail.html', context)


def market_prices_view(request):
    """Vue des prix de marché"""
    # Prix récents par culture
    crops = Crop.objects.all()
    
    price_data = {}
    for crop in crops:
        latest_prices = MarketPrice.objects.filter(
            crop=crop
        ).order_by('-date')[:10]
        
        if latest_prices:
            price_data[crop.name_fr] = {
                'prices': [float(p.price_per_kg) for p in latest_prices],
                'dates': [p.date.strftime('%Y-%m-%d') for p in latest_prices],
            }
    
    context = {
        'crops': crops,
        'price_data': json.dumps(price_data),
    }
    
    return render(request, 'core/market_prices.html', context)


@login_required
@require_http_methods(["POST"])
def update_preferences(request):
    """Mettre à jour les préférences utilisateur"""
    preferences, created = UserPreference.objects.get_or_create(user=request.user)
    
    preferences.language = request.POST.get('language', 'fr')
    preferences.theme = request.POST.get('theme', 'light')
    preferences.notification_email = request.POST.get('notification_email') == 'true'
    preferences.save()
    
    messages.success(request, _('Préférences mises à jour avec succès'))
    return redirect('dashboard')


def visualization_view(request):
    """Vue pour visualisations avancées"""
    visualizer = DataVisualizer()
    
    # Graphiques pour l'utilisateur
    user_seasons = CropSeason.objects.filter(farm__user=request.user)
    
    charts = {
        'yield_trends': visualizer.create_yield_trend_chart(user_seasons),
        'crop_distribution': visualizer.create_crop_distribution_chart(user_seasons),
        'revenue_analysis': visualizer.create_revenue_chart(user_seasons),
    }
    
    context = {
        'charts': charts,
    }
    
    return render(request, 'core/visualizations.html', context)


def about(request):
    """Page À propos"""
    return render(request, 'core/about.html')


def contact(request):
    """Page Contact"""
    if request.method == 'POST':
        # Traiter le formulaire de contact
        messages.success(request, _('Votre message a été envoyé avec succès'))
        return redirect('index')
    
    return render(request, 'core/contact.html')
def chatbot_view(request):
    """Vue pour la page du chatbot"""
    return render(request, 'core/chatbot.html')

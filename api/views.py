"""
API Views - REST API endpoints
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.utils.translation import gettext as _

from ml_models.predictor import CropRecommender, YieldPredictor, DiseasePredictor
# from chatbot.chatbot import get_chatbot  # Temporairement désactivé
from core.models import Crop, MarketPrice, Farm, CropSeason
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def crop_recommendation_api(request):
    """
    API endpoint pour recommandation de cultures
    
    POST /api/recommendations/
    {
        "temperature": 28.5,
        "humidity": 75.0,
        "rainfall": 1200,
        "soil_ph": 6.5,
        "soil_type": "LOAM",
        "region": "CENTER"
    }
    """
    try:
        # Valider les données
        required_fields = ['temperature', 'humidity', 'rainfall', 'soil_ph']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'Le champ {field} est requis'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Faire la prédiction
        recommender = CropRecommender()
        recommendations = recommender.recommend(request.data)
        
        return Response({
            'success': True,
            'recommendations': recommendations,
            'input': request.data
        })
        
    except Exception as e:
        logger.error(f"Erreur API recommandation: {e}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def yield_prediction_api(request):
    """
    API endpoint pour prédiction de rendement
    
    POST /api/yield-prediction/
    {
        "crop": "Maïs",
        "area_hectares": 2.5,
        "temperature": 27.0,
        "rainfall": 900,
        "soil_ph": 6.2,
        "fertilizer_npk": 250,
        "irrigation": true
    }
    """
    try:
        # Valider les données
        required_fields = ['crop', 'area_hectares', 'temperature', 'rainfall', 'soil_ph']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'Le champ {field} est requis'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Faire la prédiction
        predictor = YieldPredictor()
        prediction = predictor.predict(request.data)
        
        return Response({
            'success': True,
            'prediction': prediction,
            'input': request.data
        })
        
    except Exception as e:
        logger.error(f"Erreur API prédiction: {e}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def disease_prediction_api(request):
    """
    API endpoint pour prédiction de risque de maladie
    
    POST /api/disease-risk/
    {
        "crop": "Tomate",
        "temperature": 28.0,
        "humidity": 85.0,
        "rainfall": 150
    }
    """
    try:
        required_fields = ['crop', 'temperature', 'humidity']
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'Le champ {field} est requis'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        predictor = DiseasePredictor()
        risk = predictor.predict_risk(request.data)
        
        return Response({
            'success': True,
            'risk': risk,
            'input': request.data
        })
        
    except Exception as e:
        logger.error(f"Erreur API risque maladie: {e}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def chatbot_api(request):
    """
    API endpoint pour le chatbot - TEMPORAIREMENT DÉSACTIVÉ
    """
    return Response({
        'success': False,
        'response': 'Le chatbot sera bientôt disponible! 🤖',
        'message': 'Fonctionnalité en cours de développement.'
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def crops_list_api(request):
    """
    Liste toutes les cultures disponibles
    
    GET /api/crops/
    """
    try:
        crops = Crop.objects.all()
        
        data = []
        for crop in crops:
            data.append({
                'id': crop.id,
                'name_fr': crop.name_fr,
                'name_en': crop.name_en,
                'scientific_name': crop.scientific_name,
                'category': crop.category,
                'growing_season_days': crop.growing_season_days,
                'water_requirement': crop.water_requirement,
                'temperature_min': crop.temperature_min,
                'temperature_max': crop.temperature_max,
                'optimal_ph_min': crop.optimal_ph_min,
                'optimal_ph_max': crop.optimal_ph_max
            })
        
        return Response({
            'success': True,
            'count': len(data),
            'crops': data
        })
        
    except Exception as e:
        logger.error(f"Erreur API liste cultures: {e}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def market_prices_api(request):
    """
    Récupère les prix de marché
    
    GET /api/market-prices/?crop=Maïs&region=CENTER
    """
    try:
        crop_name = request.GET.get('crop')
        region = request.GET.get('region')
        
        prices = MarketPrice.objects.all()
        
        if crop_name:
            prices = prices.filter(crop__name_fr=crop_name)
        if region:
            prices = prices.filter(region=region)
        
        prices = prices.order_by('-date')[:30]
        
        data = []
        for price in prices:
            data.append({
                'date': price.date.isoformat(),
                'crop': price.crop.name_fr,
                'region': price.region,
                'price_per_kg': float(price.price_per_kg),
                'supply_level': price.supply_level,
                'demand_level': price.demand_level
            })
        
        return Response({
            'success': True,
            'count': len(data),
            'prices': data
        })
        
    except Exception as e:
        logger.error(f"Erreur API prix marché: {e}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats_api(request):
    """
    Statistiques utilisateur
    
    GET /api/user-stats/
    """
    try:
        user = request.user
        
        farms = Farm.objects.filter(user=user)
        seasons = CropSeason.objects.filter(farm__user=user)
        
        stats = {
            'total_farms': farms.count(),
            'total_area': sum(farm.area_hectares for farm in farms),
            'active_seasons': seasons.filter(actual_harvest_date__isnull=True).count(),
            'completed_seasons': seasons.filter(actual_harvest_date__isnull=False).count(),
            'total_production': sum(
                season.total_production_kg or 0 
                for season in seasons
            ),
            'average_yield': seasons.filter(
                yield_kg_per_ha__isnull=False
            ).aggregate(
                avg=models.Avg('yield_kg_per_ha')
            )['avg'] or 0
        }
        
        return Response({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        logger.error(f"Erreur API stats utilisateur: {e}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint
    
    GET /api/health/
    """
    return Response({
        'status': 'healthy',
        'version': '1.0.0',
        'service': 'Agri Smart API'
    })

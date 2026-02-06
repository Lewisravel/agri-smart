"""
API Views - REST API endpoints
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.utils.translation import gettext as _
from django.db import models

from ml_models.predictor import CropRecommender, YieldPredictor, DiseasePredictor
from chatbot.chatbot import get_chatbot
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
    API endpoint pour le chatbot
    
    POST /api/chatbot/
    {
        "message": "Comment cultiver le maïs?",
        "language": "fr",
        "user_id": "optional"
    }
    """
    try:
        if 'message' not in request.data:
            return Response(
                {'error': 'Le champ message est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message = request.data['message']
        language = request.data.get('language', 'fr')
        user_id = request.data.get('user_id', 'anonymous')
        
        # Obtenir la réponse du chatbot
        bot = get_chatbot()
        response = bot.get_response(message, user_id=user_id, language=language)
        
        return Response({
            'success': True,
            'response': response['response'],
            'intent': response.get('intent'),
            'confidence': response.get('confidence'),
            'sources': response.get('sources', [])
        })
        
    except Exception as e:
        logger.error(f"Erreur API chatbot: {e}")
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def chat_message(request):
    """
    Endpoint pour les messages du chatbot (mode HTTP fallback)
    
    POST /api/chat/
    {
        "message": "Comment cultiver le maïs?"
    }
    """
    try:
        message = request.data.get('message', '')
        
        if not message:
            return Response({
                'error': 'Message vide'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Utiliser le chatbot
        try:
            bot = get_chatbot()
            response_data = bot.get_response(message, user_id='anonymous', language='fr')
            response_text = response_data.get('response', '')
        except Exception as e:
            logger.error(f"Erreur chatbot: {e}")
            # Réponse simple si le chatbot échoue
            response_text = generate_simple_response(message)
        
        return Response({
            'message': response_text,
            'response': response_text,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Erreur dans chat_message: {e}")
        return Response({
            'error': 'Erreur serveur',
            'message': 'Désolé, je rencontre un problème. Veuillez réessayer.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_simple_response(message):
    """Génère une réponse simple basée sur des mots-clés"""
    message_lower = message.lower()
    
    # Réponses simples basées sur des mots-clés
    if any(word in message_lower for word in ['maïs', 'mais', 'corn']):
        return """Le maïs se cultive ainsi:
        
🌱 **Plantation:** Planter en début de saison des pluies (mars-avril)
🌡️ **Température:** 20-30°C idéal
💧 **Eau:** Besoin régulier, surtout pendant la floraison
🌾 **Sol:** Sol bien drainé, pH 5.5-7.0
⏰ **Récolte:** 90-120 jours après plantation

**Conseils:**
- Espacement: 75cm entre rangs, 25cm entre plants
- Engrais NPK: 200-300 kg/ha
- Désherbage régulier nécessaire
        """
    
    elif any(word in message_lower for word in ['riz', 'rice']):
        return """Culture du riz:
        
🌱 **Plantation:** Repiquage après 25-30 jours en pépinière
💧 **Eau:** Besoin d'eau abondante (rizière inondée)
🌡️ **Température:** 25-35°C
🌾 **Sol:** Sol argileux, pH 5.5-6.5
⏰ **Récolte:** 120-150 jours

**Techniques:**
- Repiquage à 20x20 cm
- Gestion de l'eau cruciale
- Fertilisation NPK: 100-150 kg/ha
        """
    
    elif any(word in message_lower for word in ['tomate', 'tomato']):
        return """Culture de tomate:
        
🌱 **Plantation:** En pépinière puis repiquage après 4-6 semaines
🌡️ **Température:** 18-27°C
💧 **Arrosage:** Régulier mais éviter l'excès d'eau
🌾 **Sol:** Sol riche, bien drainé, pH 6.0-7.0
🐛 **Maladies:** Mildiou, nématodes - traiter préventivement
⏰ **Récolte:** 70-90 jours après repiquage

**Conseils:**
- Tuteurage obligatoire
- Paillage recommandé
- Taille des gourmands
        """
    
    elif any(word in message_lower for word in ['manioc', 'cassava']):
        return """Culture du manioc:
        
🌱 **Plantation:** Boutures de 20-25 cm
🌡️ **Température:** 25-29°C
💧 **Eau:** Résistant à la sécheresse
🌾 **Sol:** Sol sablonneux à limoneux, pH 5.5-7.0
⏰ **Récolte:** 9-12 mois

**Techniques:**
- Espacement: 1m x 1m
- Buttage après 3 mois
- Résistant aux maladies
        """
    
    elif any(word in message_lower for word in ['maladie', 'disease', 'traiter', 'parasite']):
        return """Pour les maladies des plantes:
        
🔍 **Prévention:**
- Rotation des cultures
- Bon drainage du sol
- Espacement adéquat entre plants
- Semences saines
- Désherbage régulier

💊 **Traitement:**
- Produits biologiques en priorité
- Fongicides si nécessaire
- Insecticides ciblés
- Consulter un agronome pour diagnostic précis

🌿 **Solutions naturelles:**
- Purin d'ortie
- Décoction d'ail
- Savon noir
        """
    
    elif any(word in message_lower for word in ['engrais', 'fertilizer', 'npk', 'fumier']):
        return """Sur les engrais:
        
🌾 **Types d'engrais:**
- **NPK:** Azote (N), Phosphore (P), Potassium (K)
- **Engrais organique:** Compost, fumier, déchets verts
- **Engrais minéral:** NPK 15-15-15, Urée 46%

📊 **Dosage:**
- Dépend de la culture et du type de sol
- Analyse de sol recommandée
- Application fractionnée souvent meilleure

⏰ **Application:**
- Engrais de fond avant semis
- Engrais de couverture en cours de culture
- NPK: 200-400 kg/ha selon culture
        """
    
    elif any(word in message_lower for word in ['irrigation', 'arrosage', 'eau']):
        return """Sur l'irrigation:
        
💧 **Besoins en eau par culture:**
- Riz: 1000-2000 mm
- Maïs: 500-800 mm
- Tomate: 400-600 mm
- Manioc: 500-1000 mm

🚿 **Méthodes d'irrigation:**
- Goutte-à-goutte (économe)
- Aspersion
- Gravitaire (rizières)

📅 **Périodes critiques:**
- Germination
- Floraison
- Formation des fruits/grains
        """
    
    elif any(word in message_lower for word in ['quand', 'période', 'moment', 'planter']):
        return """Calendrier de plantation au Cameroun:

**Saison des pluies (Mars-Juin):**
🌱 Maïs: Mars-Avril
🌱 Riz: Avril-Mai
🌱 Arachide: Avril-Mai
🌱 Soja: Avril-Mai

**Saison sèche (cultures irriguées):**
🌱 Tomate: Novembre-Janvier
🌱 Oignon: Octobre-Décembre
🌱 Maraîchage: Toute l'année avec irrigation

**Note:** Les dates varient selon les régions
        """
    
    elif any(word in message_lower for word in ['prix', 'vendre', 'marché', 'vente']):
        return """Sur la commercialisation:

💰 **Prix indicatifs (FCFA/kg):**
- Maïs: 400-600
- Riz: 600-800
- Tomate: 300-500
- Manioc: 200-300
- Arachide: 500-700

📊 **Conseils:**
- Groupement de producteurs pour meilleur prix
- Stockage adéquat pour vendre hors saison
- Diversification des débouchés
- Transformation pour valoriser la production

🏪 **Marchés:**
- Marchés locaux
- Grossistes
- Coopératives agricoles
        """
    
    elif any(word in message_lower for word in ['sol', 'terre', 'ph']):
        return """Sur le sol et le pH:

🌾 **Types de sol:**
- **Sableux:** Drainant, pauvre en nutriments
- **Argileux:** Lourd, retient l'eau
- **Limoneux:** Équilibré, très fertile
- **Humifère:** Riche en matière organique

📊 **pH du sol:**
- Acide: pH < 6.5 (ajouter de la chaux)
- Neutre: pH 6.5-7.5 (idéal pour la plupart des cultures)
- Alcalin: pH > 7.5 (ajouter du soufre ou compost)

🔬 **Amélioration:**
- Analyse de sol tous les 2-3 ans
- Apport de matière organique
- Rotation des cultures
- Correction du pH si nécessaire
        """
    
    elif any(word in message_lower for word in ['bonjour', 'salut', 'hello', 'hi', 'hey']):
        return """Bonjour! 👋 Bienvenue sur Agri Smart!

Je suis votre assistant agricole IA. Je peux vous aider avec:

🌱 **Techniques de culture:** Maïs, Riz, Tomate, Manioc, etc.
📅 **Calendrier agricole:** Quand planter chaque culture
🐛 **Gestion des maladies et parasites**
💧 **Irrigation et besoins en eau**
🌾 **Choix et dosage d'engrais**
💰 **Prix de marché et commercialisation**
🌡️ **Conditions optimales** (température, pH, etc.)

**Posez-moi vos questions!** Par exemple:
- "Comment cultiver le maïs?"
- "Quelle est la meilleure période pour planter?"
- "Comment traiter les maladies des tomates?"
        """
    
    elif any(word in message_lower for word in ['merci', 'thanks', 'thank you']):
        return """De rien! 😊 Je suis là pour vous aider.

N'hésitez pas à me poser d'autres questions sur:
- Culture des différentes plantes
- Gestion des maladies
- Techniques d'irrigation
- Fertilisation
- Calendrier agricole
- Prix de marché

Bonne culture! 🌱
        """
    
    else:
        return """Je suis votre assistant agricole IA. Je peux vous aider avec:

🌱 **Cultures:** Maïs, Riz, Tomate, Manioc, Arachide, Soja, Oignon, Coton
🐛 **Gestion:** Maladies, parasites, mauvaises herbes
💧 **Irrigation:** Besoins en eau, méthodes d'arrosage
🌾 **Fertilisation:** Types d'engrais, dosages
📅 **Calendrier:** Périodes de plantation, récolte
💰 **Marché:** Prix, commercialisation
🌡️ **Conditions:** Température, pH, humidité

**Exemples de questions:**
- "Comment cultiver le maïs?"
- "Quels engrais pour la tomate?"
- "Comment traiter le mildiou?"
- "Quand planter le riz?"

Posez-moi une question plus spécifique! 😊
        """


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
"""
Agricultural Chatbot using Hugging Face Models
Provides intelligent responses to agricultural questions
"""
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from django.conf import settings
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class AgriculturalChatbot:
    """
    Chatbot agricole intelligent utilisant des modèles Hugging Face
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Chatbot utilisant device: {self.device}")
        
        # Modèle de génération de texte (phi-2 pour texte, léger et efficace)
        self.model_name = settings.HUGGINGFACE_MODELS.get('text_generation', 'microsoft/phi-2')
        
        # Base de connaissances agricoles
        self.knowledge_base = self._load_knowledge_base()
        
        # Question-answering pipeline pour recherche dans la base
        try:
            self.qa_pipeline = pipeline(
                "question-answering",
                model=settings.HUGGINGFACE_MODELS.get('question_answering', 'deepset/roberta-base-squad2'),
                device=0 if self.device == "cuda" else -1
            )
            logger.info("Pipeline QA chargé avec succès")
        except Exception as e:
            logger.error(f"Erreur chargement pipeline QA: {e}")
            self.qa_pipeline = None
        
        # Historique des conversations
        self.conversation_history = {}
    
    def _load_knowledge_base(self) -> dict:
        """
        Charge la base de connaissances agricoles
        En production, charger depuis fichiers ou base de données
        """
        return {
            'crops': {
                'Maïs': {
                    'description': "Le maïs est une céréale cultivée pour ses grains riches en amidon. Il nécessite un climat chaud et humide avec une température optimale de 20-30°C. Le cycle cultural dure 90-120 jours selon les variétés.",
                    'cultivation': "Semis direct à 75cm entre lignes et 25cm sur ligne. Fertilisation NPK 15-15-15 à 200-300 kg/ha. Besoin en eau: 500-800mm sur le cycle.",
                    'diseases': "Principales maladies: Chenille légionnaire, Helminthosporiose, Striure. Traitement préventif recommandé.",
                    'harvest': "Récolte quand les grains atteignent 25-30% d'humidité. Rendement moyen: 2-6 tonnes/ha."
                },
                'Riz': {
                    'description': "Le riz est la céréale la plus consommée au monde. Culture en zone humide nécessitant beaucoup d'eau. Température optimale: 20-35°C. Cycle: 120-150 jours.",
                    'cultivation': "Repiquage à 20cm x 20cm. Maintenir 5-10cm d'eau permanente. NPK 20-10-10 + urée en couverture. Désherbage crucial.",
                    'diseases': "Pyriculariose, pourriture des racines, adventices aquatiques. Gestion de l'eau essentielle pour prévention.",
                    'harvest': "Récolte à maturité complète (grains dorés). Rendement: 3-7 tonnes/ha selon irrigation."
                },
                'Tomate': {
                    'description': "La tomate est un fruit-légume cultivé en saison fraîche. Température optimale: 18-27°C. Cycle court: 90-120 jours. Culture exigeante en eau et nutriments.",
                    'cultivation': "Plantation sur billons à 60cm x 40cm. Tuteurage nécessaire. NPK 10-20-20 + calcium. Irrigation goutte-à-goutte recommandée.",
                    'diseases': "Mildiou, alternariose, nématodes. Traitement fongicide préventif obligatoire. Rotation des cultures importante.",
                    'harvest': "Récolte échelonnée selon maturité. Rendement: 20-60 tonnes/ha selon système."
                },
                'Manioc': {
                    'description': "Le manioc est un tubercule de base en Afrique. Très résistant à la sécheresse. Cycle long: 8-24 mois. Pousse sur sols pauvres.",
                    'cultivation': "Plantation de boutures à 1m x 1m. Peu d'engrais nécessaire. Buttage à 3-4 mois. Très peu d'entretien.",
                    'diseases': "Mosaïque du manioc, bactériose, cochenilles. Utiliser boutures saines.",
                    'harvest': "Récolte à 10-12 mois minimum. Rendement: 10-30 tonnes/ha de tubercules frais."
                },
                'Oignon': {
                    'description': "L'oignon est un bulbe cultivé pour son goût. Préfère climat frais. Température: 13-24°C. Cycle: 90-120 jours.",
                    'cultivation': "Semis en pépinière puis repiquage à 10cm x 20cm. NPK équilibré. Irrigation régulière mais modérée.",
                    'diseases': "Mildiou, pourriture blanche, thrips. Drainage important.",
                    'harvest': "Récolte quand feuilles tombent. Séchage 2 semaines. Rendement: 15-40 tonnes/ha."
                }
            },
            'soil_management': {
                'ph_correction': "Pour sol acide (pH < 5.5): appliquer chaux à 1-3 tonnes/ha. Pour sol alcalin (pH > 7.5): apporter soufre ou gypse.",
                'fertilization': "Analyse de sol recommandée avant fertilisation. NPK selon culture. Matière organique 20 tonnes/ha tous les 2 ans.",
                'conservation': "Pratiques de conservation: paillage, culture de couverture, rotation, agroforesterie. Limite érosion et améliore fertilité."
            },
            'irrigation': {
                'types': "Goutte-à-goutte (90% efficacité), aspersion (75%), gravitaire (50%). Choisir selon culture et disponibilité eau.",
                'scheduling': "Irrigation selon stade: critique à floraison et formation fruits. Eviter sur-irrigation (maladies).",
                'water_saving': "Paillage, irrigation localisée, choix variétés résistantes, calendrier cultural optimisé."
            },
            'pest_management': {
                'integrated': "Lutte intégrée: rotation, plantes pièges, auxiliaires naturels, traitements ciblés si nécessaire.",
                'organic': "Méthodes bio: neem, purins de plantes, pièges à phéromones, prédateurs naturels.",
                'chemical': "Pesticides en dernier recours. Respecter doses, délais avant récolte, équipement protection."
            },
            'climate_adaptation': {
                'drought': "Variétés tolérantes sécheresse, paillage, irrigation localisée, semis précoces, cultures intercalaires.",
                'excess_rain': "Drainage, billonnage, variétés tolérantes, protection fongicide, retard semis si nécessaire.",
                'heat': "Ombrage léger, irrigation fréquente, variétés adaptées, horaires travaux adaptés."
            },
            'market': {
                'prices': "Prix varient selon saison, qualité, marché. Stockage post-récolte pour meilleurs prix. Organisations de producteurs recommandées.",
                'value_addition': "Transformation (séchage, farine, conserves) augmente valeur. Certification bio/commerce équitable = prix premium.",
                'access': "Coopératives agricoles facilitent accès marché, intrants, crédit, formation. Association recommandée."
            }
        }
    
    def get_response(self, user_message: str, user_id: str = None, language: str = 'fr') -> dict:
        """
        Génère une réponse au message utilisateur
        
        Args:
            user_message: Question de l'utilisateur
            user_id: ID utilisateur pour historique
            language: 'fr' ou 'en'
        
        Returns:
            dict avec réponse et métadonnées
        """
        try:
            # Détecter l'intention
            intent = self._detect_intent(user_message)
            
            # Chercher dans la base de connaissances
            relevant_context = self._search_knowledge_base(user_message, intent)
            
            # Générer réponse
            response = self._generate_response(
                user_message,
                relevant_context,
                intent,
                language
            )
            
            # Sauvegarder dans l'historique
            if user_id:
                self._update_conversation_history(user_id, user_message, response)
            
            return {
                'response': response,
                'intent': intent,
                'confidence': 0.85,
                'timestamp': datetime.now().isoformat(),
                'sources': relevant_context.get('sources', [])
            }
            
        except Exception as e:
            logger.error(f"Erreur génération réponse: {e}")
            return {
                'response': self._get_fallback_response(language),
                'intent': 'unknown',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _detect_intent(self, message: str) -> str:
        """Détecte l'intention de l'utilisateur"""
        message_lower = message.lower()
        
        # Intentions basées sur mots-clés
        if any(word in message_lower for word in ['culture', 'cultiver', 'planter', 'semis']):
            return 'cultivation'
        elif any(word in message_lower for word in ['maladie', 'ravageur', 'traiter', 'pest']):
            return 'disease'
        elif any(word in message_lower for word in ['engrais', 'fertiliser', 'npk', 'fumure']):
            return 'fertilization'
        elif any(word in message_lower for word in ['irrigation', 'arroser', 'eau']):
            return 'irrigation'
        elif any(word in message_lower for word in ['prix', 'marché', 'vendre', 'acheter']):
            return 'market'
        elif any(word in message_lower for word in ['sol', 'terre', 'ph']):
            return 'soil'
        elif any(word in message_lower for word in ['climat', 'température', 'pluie', 'sécheresse']):
            return 'climate'
        elif any(word in message_lower for word in ['rendement', 'production', 'récolte']):
            return 'yield'
        elif any(word in message_lower for word in ['recommande', 'conseille', 'quelle culture']):
            return 'recommendation'
        else:
            return 'general'
    
    def _search_knowledge_base(self, query: str, intent: str) -> dict:
        """Recherche dans la base de connaissances"""
        relevant_info = {
            'text': '',
            'sources': []
        }
        
        # Construire le contexte selon l'intention
        if intent == 'cultivation':
            for crop, info in self.knowledge_base['crops'].items():
                if crop.lower() in query.lower():
                    relevant_info['text'] += f"\n{crop}: {info['cultivation']}"
                    relevant_info['sources'].append(f"Guide de culture - {crop}")
        
        elif intent == 'disease':
            for crop, info in self.knowledge_base['crops'].items():
                if crop.lower() in query.lower():
                    relevant_info['text'] += f"\n{crop}: {info['diseases']}"
                    relevant_info['sources'].append(f"Maladies - {crop}")
        
        elif intent == 'soil':
            relevant_info['text'] = json.dumps(self.knowledge_base['soil_management'], ensure_ascii=False)
            relevant_info['sources'].append("Guide de gestion du sol")
        
        elif intent == 'irrigation':
            relevant_info['text'] = json.dumps(self.knowledge_base['irrigation'], ensure_ascii=False)
            relevant_info['sources'].append("Guide d'irrigation")
        
        elif intent == 'market':
            relevant_info['text'] = json.dumps(self.knowledge_base['market'], ensure_ascii=False)
            relevant_info['sources'].append("Informations de marché")
        
        else:
            # Recherche générale
            for category, content in self.knowledge_base.items():
                if isinstance(content, dict):
                    relevant_info['text'] += f"\n{json.dumps(content, ensure_ascii=False)}"
        
        # Si aucun contexte trouvé, donner info générale
        if not relevant_info['text']:
            relevant_info['text'] = "Informations agricoles générales disponibles."
            relevant_info['sources'].append("Base de connaissances")
        
        return relevant_info
    
    def _generate_response(self, query: str, context: dict, intent: str, language: str) -> str:
        """
        Génère une réponse basée sur le contexte
        Pour l'instant utilise des templates, mais peut être amélioré avec GPT
        """
        
        # Réponses selon l'intention
        if intent == 'cultivation':
            crops_mentioned = []
            for crop in self.knowledge_base['crops'].keys():
                if crop.lower() in query.lower():
                    crops_mentioned.append(crop)
            
            if crops_mentioned:
                crop = crops_mentioned[0]
                info = self.knowledge_base['crops'][crop]
                
                if language == 'fr':
                    response = f"**Culture du {crop}**\n\n"
                    response += f"{info['description']}\n\n"
                    response += f"**Pratiques culturales:**\n{info['cultivation']}\n\n"
                    response += f"**Récolte:**\n{info['harvest']}"
                else:
                    response = f"**Growing {crop}**\n\n"
                    response += f"{info['description']}\n\n"
                    response += f"**Cultivation practices:**\n{info['cultivation']}\n\n"
                    response += f"**Harvest:**\n{info['harvest']}"
                
                return response
        
        elif intent == 'disease':
            crops_mentioned = []
            for crop in self.knowledge_base['crops'].keys():
                if crop.lower() in query.lower():
                    crops_mentioned.append(crop)
            
            if crops_mentioned:
                crop = crops_mentioned[0]
                info = self.knowledge_base['crops'][crop]
                
                if language == 'fr':
                    response = f"**Maladies et ravageurs du {crop}**\n\n"
                    response += info['diseases'] + "\n\n"
                    response += "**Lutte intégrée:**\n"
                    response += self.knowledge_base['pest_management']['integrated']
                else:
                    response = f"**{crop} Diseases and Pests**\n\n"
                    response += info['diseases'] + "\n\n"
                    response += "**Integrated Management:**\n"
                    response += self.knowledge_base['pest_management']['integrated']
                
                return response
        
        elif intent == 'soil':
            if language == 'fr':
                response = "**Gestion du Sol**\n\n"
                response += f"**Correction du pH:**\n{self.knowledge_base['soil_management']['ph_correction']}\n\n"
                response += f"**Fertilisation:**\n{self.knowledge_base['soil_management']['fertilization']}\n\n"
                response += f"**Conservation:**\n{self.knowledge_base['soil_management']['conservation']}"
            else:
                response = "**Soil Management**\n\n"
                response += f"**pH Correction:**\n{self.knowledge_base['soil_management']['ph_correction']}\n\n"
                response += f"**Fertilization:**\n{self.knowledge_base['soil_management']['fertilization']}\n\n"
                response += f"**Conservation:**\n{self.knowledge_base['soil_management']['conservation']}"
            
            return response
        
        elif intent == 'irrigation':
            if language == 'fr':
                response = "**Irrigation Agricole**\n\n"
                response += f"**Types d'irrigation:**\n{self.knowledge_base['irrigation']['types']}\n\n"
                response += f"**Calendrier:**\n{self.knowledge_base['irrigation']['scheduling']}\n\n"
                response += f"**Économie d'eau:**\n{self.knowledge_base['irrigation']['water_saving']}"
            else:
                response = "**Agricultural Irrigation**\n\n"
                response += f"**Irrigation types:**\n{self.knowledge_base['irrigation']['types']}\n\n"
                response += f"**Scheduling:**\n{self.knowledge_base['irrigation']['scheduling']}\n\n"
                response += f"**Water saving:**\n{self.knowledge_base['irrigation']['water_saving']}"
            
            return response
        
        elif intent == 'recommendation':
            if language == 'fr':
                response = "**Recommandations de cultures**\n\n"
                response += "Pour une recommandation personnalisée, utilisez notre outil de recommandation dans l'application. "
                response += "Vous pourrez entrer vos données de sol, climat et localisation pour obtenir les meilleures cultures adaptées.\n\n"
                response += "**Cultures populaires au Cameroun:**\n"
                response += "- Maïs: Adapté à presque toutes les régions\n"
                response += "- Manioc: Résistant, faible entretien\n"
                response += "- Riz: Zones humides, bon rendement\n"
                response += "- Tomate: Rentable, demande élevée\n"
                response += "- Arachide: Sol léger, rotation bénéfique"
            else:
                response = "**Crop Recommendations**\n\n"
                response += "For personalized recommendations, use our recommendation tool in the application. "
                response += "You can enter your soil, climate and location data to get the best adapted crops.\n\n"
                response += "**Popular crops in Cameroon:**\n"
                response += "- Maize: Adapted to almost all regions\n"
                response += "- Cassava: Resistant, low maintenance\n"
                response += "- Rice: Humid zones, good yield\n"
                response += "- Tomato: Profitable, high demand\n"
                response += "- Peanut: Light soil, beneficial rotation"
            
            return response
        
        # Réponse générale
        if language == 'fr':
            return ("Je suis votre assistant agricole intelligent. Je peux vous aider avec:\n\n"
                   "🌱 Recommandations de cultures\n"
                   "💧 Irrigation et gestion de l'eau\n"
                   "🌿 Fertilisation et gestion du sol\n"
                   "🐛 Maladies et ravageurs\n"
                   "📊 Prévisions de rendement\n"
                   "💰 Prix de marché\n\n"
                   "Posez-moi vos questions agricoles!")
        else:
            return ("I'm your intelligent agricultural assistant. I can help you with:\n\n"
                   "🌱 Crop recommendations\n"
                   "💧 Irrigation and water management\n"
                   "🌿 Fertilization and soil management\n"
                   "🐛 Diseases and pests\n"
                   "📊 Yield forecasts\n"
                   "💰 Market prices\n\n"
                   "Ask me your agricultural questions!")
    
    def _get_fallback_response(self, language: str) -> str:
        """Réponse de secours en cas d'erreur"""
        if language == 'fr':
            return ("Désolé, je n'ai pas pu traiter votre demande. "
                   "Pourriez-vous reformuler votre question différemment?")
        else:
            return ("Sorry, I couldn't process your request. "
                   "Could you rephrase your question differently?")
    
    def _update_conversation_history(self, user_id: str, message: str, response: str):
        """Met à jour l'historique des conversations"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'timestamp': datetime.now().isoformat(),
            'user_message': message,
            'bot_response': response
        })
        
        # Garder seulement les 20 derniers messages
        if len(self.conversation_history[user_id]) > 20:
            self.conversation_history[user_id] = self.conversation_history[user_id][-20:]


# Instance globale du chatbot
chatbot_instance = None

"""
Chatbot simple basé sur des mots-clés
"""

def get_chatbot():
    """Retourne une instance simple du chatbot"""
    return SimpleChatbot()


class SimpleChatbot:
    """Chatbot simple sans dépendances lourdes"""
    
    def get_response(self, message, user_id='anonymous', language='fr'):
        """Génère une réponse basée sur des mots-clés"""
        message_lower = message.lower()
        
        # Réponses simples basées sur des mots-clés
        if any(word in message_lower for word in ['maïs', 'mais', 'corn']):
            response = """Le maïs se cultive ainsi:
            
🌱 **Plantation:** Mars-avril (début saison des pluies)
🌡️ **Température:** 20-30°C idéal
💧 **Eau:** Besoin régulier
🌾 **Sol:** pH 5.5-7.0
⏰ **Récolte:** 90-120 jours
            """
        
        elif any(word in message_lower for word in ['riz', 'rice']):
            response = """Culture du riz:
            
🌱 **Plantation:** Repiquage après 25-30 jours
💧 **Eau:** Besoin abondant
🌡️ **Température:** 25-35°C
⏰ **Récolte:** 120-150 jours
            """
        
        elif any(word in message_lower for word in ['tomate', 'tomato']):
            response = """Culture de tomate:
            
🌱 **Plantation:** Pépinière puis repiquage
🌡️ **Température:** 18-27°C
💧 **Arrosage:** Régulier
⏰ **Récolte:** 70-90 jours
            """
        
        elif any(word in message_lower for word in ['maladie', 'disease', 'traiter']):
            response = """Gestion des maladies:
            
🔍 **Prévention:**
- Rotation des cultures
- Bon drainage
- Espacement adéquat

💊 **Traitement:**
- Produits biologiques
- Fongicides si nécessaire
            """
        
        elif any(word in message_lower for word in ['engrais', 'fertilizer', 'npk']):
            response = """Sur les engrais:
            
🌾 **Types:** NPK, organiques
📊 **Dosage:** Selon culture et sol
⏰ **Application:** Fractionnée
            """
        
        elif any(word in message_lower for word in ['bonjour', 'salut', 'hello']):
            response = """Bonjour! 👋

Je suis votre assistant agricole. Je peux vous aider avec:
🌱 Techniques de culture
📅 Calendrier agricole
🐛 Gestion des maladies
💧 Irrigation
🌾 Engrais

Posez-moi vos questions!
            """
        
        else:
            response = """Je suis votre assistant agricole.

Posez-moi des questions sur:
🌱 Culture (maïs, riz, tomate, manioc)
🐛 Maladies et parasites
💧 Irrigation
🌾 Engrais
📅 Calendrier agricole
            """
        
        return {
            'response': response,
            'intent': 'general',
            'confidence': 0.8,
            'sources': []
        }
"""
WebSocket Consumer for Chatbot
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .chatbot import get_chatbot
import logging

logger = logging.getLogger(__name__)


class ChatbotConsumer(AsyncWebsocketConsumer):
    """
    Consumer WebSocket pour le chatbot en temps réel
    """
    
    async def connect(self):
        """Connexion WebSocket établie"""
        await self.accept()
        logger.info("Chatbot WebSocket connecté")
        
        # Envoyer message de bienvenue
        await self.send(text_data=json.dumps({
            'type': 'welcome',
            'message': 'Bienvenue! Je suis votre assistant agricole. Comment puis-je vous aider?'
        }))
    
    async def disconnect(self, close_code):
        """Déconnexion WebSocket"""
        logger.info(f"Chatbot WebSocket déconnecté: {close_code}")
    
    async def receive(self, text_data):
        """
        Recevoir un message du client
        """
        try:
            data = json.loads(text_data)
            user_message = data.get('message', '')
            language = data.get('language', 'fr')
            user_id = data.get('user_id', 'anonymous')
            
            if not user_message:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Message vide'
                }))
                return
            
            # Obtenir la réponse du chatbot
            bot = get_chatbot()
            response = bot.get_response(user_message, user_id=user_id, language=language)
            
            # Envoyer la réponse
            await self.send(text_data=json.dumps({
                'type': 'response',
                'message': response['response'],
                'intent': response.get('intent'),
                'confidence': response.get('confidence'),
                'sources': response.get('sources', [])
            }))
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Format de message invalide'
            }))
        except Exception as e:
            logger.error(f"Erreur WebSocket chatbot: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Une erreur est survenue'
            }))

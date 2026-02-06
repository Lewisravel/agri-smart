#!/usr/bin/env python
"""
Script d'entraînement de tous les modèles ML
"""
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agri_smart_project.settings')
django.setup()

from ml_models.predictor import CropRecommender, YieldPredictor, DiseasePredictor
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def train_all_models():
    """Entraîner tous les modèles ML"""
    
    print("\n" + "="*60)
    print("🤖 ENTRAÎNEMENT DES MODÈLES ML - AGRI SMART")
    print("="*60 + "\n")
    
    # 1. CropRecommender
    print("📊 Entraînement du modèle de recommandation de cultures...")
    try:
        recommender = CropRecommender()
        print("✅ Modèle de recommandation créé et entraîné")
        print(f"   Sauvegardé dans: ml_models/trained_models/crop_recommender.pkl")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # 2. YieldPredictor
    print("📈 Entraînement du modèle de prédiction de rendement...")
    try:
        predictor = YieldPredictor()
        print("✅ Modèle de prédiction créé et entraîné")
        print(f"   Sauvegardé dans: ml_models/trained_models/yield_predictor.pkl")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # 3. DiseasePredictor
    print("🐛 Entraînement du modèle de risque de maladies...")
    try:
        disease_predictor = DiseasePredictor()
        print("✅ Modèle de risque de maladies créé")
        print(f"   Sauvegardé dans: ml_models/trained_models/disease_risk.pkl")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n" + "="*60)
    print("✅ ENTRAÎNEMENT TERMINÉ")
    print("="*60)
    print("\nLes modèles sont prêts à être utilisés!")
    print("Vous pouvez maintenant démarrer l'application.\n")


if __name__ == '__main__':
    train_all_models()

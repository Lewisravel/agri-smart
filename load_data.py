#!/usr/bin/env python
"""
Script de chargement des données scrapées dans la base Django
"""
import os
import sys
import django
import pandas as pd
from datetime import datetime

# Configuration Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agri_smart_project.settings')
django.setup()

from core.models import Crop, MarketPrice
from django.contrib.auth.models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_crops():
    """Charger les cultures de base"""
    print("\n📊 Chargement des cultures...")
    
    crops_data = [
        {
            'name_fr': 'Maïs',
            'name_en': 'Maize',
            'scientific_name': 'Zea mays',
            'category': 'Céréale',
            'growing_season_days': 120,
            'water_requirement': 'Moyen',
            'temperature_min': 20.0,
            'temperature_max': 30.0,
            'optimal_ph_min': 5.5,
            'optimal_ph_max': 7.5,
            'description_fr': 'Céréale cultivée pour ses grains riches en amidon',
            'description_en': 'Cereal grown for its starch-rich grains'
        },
        {
            'name_fr': 'Riz',
            'name_en': 'Rice',
            'scientific_name': 'Oryza sativa',
            'category': 'Céréale',
            'growing_season_days': 140,
            'water_requirement': 'Élevé',
            'temperature_min': 20.0,
            'temperature_max': 35.0,
            'optimal_ph_min': 5.0,
            'optimal_ph_max': 7.0,
            'description_fr': 'Céréale la plus consommée au monde',
            'description_en': 'Most consumed cereal in the world'
        },
        {
            'name_fr': 'Tomate',
            'name_en': 'Tomato',
            'scientific_name': 'Solanum lycopersicum',
            'category': 'Légume-fruit',
            'growing_season_days': 90,
            'water_requirement': 'Moyen',
            'temperature_min': 18.0,
            'temperature_max': 27.0,
            'optimal_ph_min': 6.0,
            'optimal_ph_max': 7.0,
            'description_fr': 'Fruit-légume cultivé pour sa consommation',
            'description_en': 'Fruit-vegetable grown for consumption'
        },
        {
            'name_fr': 'Manioc',
            'name_en': 'Cassava',
            'scientific_name': 'Manihot esculenta',
            'category': 'Tubercule',
            'growing_season_days': 300,
            'water_requirement': 'Faible',
            'temperature_min': 20.0,
            'temperature_max': 35.0,
            'optimal_ph_min': 5.0,
            'optimal_ph_max': 7.5,
            'description_fr': 'Tubercule de base en Afrique',
            'description_en': 'Staple tuber in Africa'
        },
        {
            'name_fr': 'Oignon',
            'name_en': 'Onion',
            'scientific_name': 'Allium cepa',
            'category': 'Légume-bulbe',
            'growing_season_days': 110,
            'water_requirement': 'Moyen',
            'temperature_min': 13.0,
            'temperature_max': 24.0,
            'optimal_ph_min': 6.0,
            'optimal_ph_max': 7.5,
            'description_fr': 'Bulbe cultivé pour son goût',
            'description_en': 'Bulb grown for its taste'
        },
        {
            'name_fr': 'Arachide',
            'name_en': 'Peanut',
            'scientific_name': 'Arachis hypogaea',
            'category': 'Légumineuse',
            'growing_season_days': 120,
            'water_requirement': 'Moyen',
            'temperature_min': 20.0,
            'temperature_max': 30.0,
            'optimal_ph_min': 5.5,
            'optimal_ph_max': 7.0,
            'description_fr': 'Légumineuse oléagineuse',
            'description_en': 'Oilseed legume'
        },
        {
            'name_fr': 'Coton',
            'name_en': 'Cotton',
            'scientific_name': 'Gossypium',
            'category': 'Culture industrielle',
            'growing_season_days': 180,
            'water_requirement': 'Moyen',
            'temperature_min': 20.0,
            'temperature_max': 35.0,
            'optimal_ph_min': 5.5,
            'optimal_ph_max': 8.0,
            'description_fr': 'Plante cultivée pour ses fibres',
            'description_en': 'Plant grown for its fibers'
        },
        {
            'name_fr': 'Soja',
            'name_en': 'Soybean',
            'scientific_name': 'Glycine max',
            'category': 'Légumineuse',
            'growing_season_days': 110,
            'water_requirement': 'Moyen',
            'temperature_min': 20.0,
            'temperature_max': 30.0,
            'optimal_ph_min': 6.0,
            'optimal_ph_max': 7.5,
            'description_fr': 'Légumineuse riche en protéines',
            'description_en': 'Protein-rich legume'
        },
    ]
    
    created_count = 0
    for crop_data in crops_data:
        crop, created = Crop.objects.get_or_create(
            name_fr=crop_data['name_fr'],
            defaults=crop_data
        )
        if created:
            created_count += 1
            print(f"  ✓ {crop.name_fr} créé")
        else:
            print(f"  → {crop.name_fr} existe déjà")
    
    print(f"\n✅ {created_count} nouvelles cultures créées")
    print(f"📊 Total cultures: {Crop.objects.count()}")


def load_market_prices():
    """Charger quelques prix de marché depuis les données scrapées"""
    print("\n💰 Chargement des prix de marché...")
    
    data_file = 'data_scraper/data/market_prices.csv'
    
    if not os.path.exists(data_file):
        print(f"⚠️  Fichier {data_file} non trouvé")
        print("   Exécutez d'abord le scraper: cd data_scraper && python scraper.py")
        return
    
    try:
        df = pd.read_csv(data_file)
        print(f"  Lecture de {len(df)} prix...")
        
        # Charger un échantillon (pour ne pas surcharger la DB)
        sample_size = min(1000, len(df))
        df_sample = df.sample(n=sample_size, random_state=42)
        
        regions = ['Centre', 'Littoral', 'Nord', 'Ouest', 'Sud']
        
        loaded_count = 0
        for _, row in df_sample.iterrows():
            try:
                # Trouver la culture correspondante
                crop = Crop.objects.filter(name_fr=row['crop']).first()
                
                if crop:
                    MarketPrice.objects.get_or_create(
                        crop=crop,
                        region=regions[hash(str(row['market'])) % len(regions)],
                        date=pd.to_datetime(row['date']).date(),
                        defaults={
                            'price_per_kg': row['price_per_kg'],
                            'supply_level': 'Normal',
                            'demand_level': 'Normal'
                        }
                    )
                    loaded_count += 1
                    
                    if loaded_count % 100 == 0:
                        print(f"  → {loaded_count} prix chargés...")
                        
            except Exception as e:
                continue
        
        print(f"\n✅ {loaded_count} prix de marché chargés")
        print(f"💰 Total prix: {MarketPrice.objects.count()}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")


def create_demo_user():
    """Créer un utilisateur de démonstration"""
    print("\n👤 Création utilisateur de démonstration...")
    
    try:
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@agrismart.cm',
                'first_name': 'Utilisateur',
                'last_name': 'Démo',
                'is_staff': False,
                'is_active': True
            }
        )
        
        if created:
            user.set_password('demo123')
            user.save()
            print("  ✓ Utilisateur 'demo' créé")
            print("     Username: demo")
            print("     Password: demo123")
        else:
            print("  → Utilisateur 'demo' existe déjà")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")


def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("📊 CHARGEMENT DES DONNÉES - AGRI SMART")
    print("="*60)
    
    load_crops()
    load_market_prices()
    create_demo_user()
    
    print("\n" + "="*60)
    print("✅ CHARGEMENT TERMINÉ")
    print("="*60)
    print("\nVous pouvez maintenant démarrer l'application!")
    print("python manage.py runserver\n")


if __name__ == '__main__':
    main()

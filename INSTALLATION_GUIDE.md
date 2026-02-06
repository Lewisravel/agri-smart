# 🌱 AGRI SMART - Guide d'Installation Complet

## 📋 Table des Matières
1. [Prérequis](#prérequis)
2. [Installation du Scraper](#installation-du-scraper)
3. [Installation de l'Application Django](#installation-de-lapplication-django)
4. [Configuration de la Base de Données](#configuration-de-la-base-de-données)
5. [Entraînement des Modèles ML](#entraînement-des-modèles-ml)
6. [Démarrage de l'Application](#démarrage-de-lapplication)
7. [Configuration du Chatbot](#configuration-du-chatbot)
8. [Déploiement en Production](#déploiement-en-production)
9. [Résolution des Problèmes](#résolution-des-problèmes)

---

## 🔧 Prérequis

### Système d'exploitation
- Ubuntu 20.04+ / Windows 10+ / macOS 10.15+
- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)
- 8GB RAM minimum (16GB recommandé pour ML)
- 20GB espace disque libre

### Logiciels requis
```bash
# Sur Ubuntu/Debian
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git

# Sur macOS (avec Homebrew)
brew install python git

# Vérifier les versions
python3 --version  # Doit être 3.9+
pip3 --version
git --version
```

---

## 📥 ÉTAPE 1: Installation du Scraper de Données

### 1.1 Créer le dossier du projet
```bash
mkdir agri_smart_project
cd agri_smart_project
```

### 1.2 Extraire les fichiers
```bash
# Extraire le fichier ZIP téléchargé
unzip agri_smart.zip
cd agri_smart
```

### 1.3 Créer l'environnement virtuel
```bash
# Créer l'environnement
python3 -m venv venv

# Activer l'environnement
# Sur Linux/macOS:
source venv/bin/activate

# Sur Windows:
venv\Scripts\activate
```

### 1.4 Installer les dépendances du scraper
```bash
cd data_scraper
pip install -r requirements.txt
```

### 1.5 Lancer le scraping
```bash
# Scraper les données (cela peut prendre 10-30 minutes)
python scraper.py

# Les données seront sauvegardées dans le dossier data/
# Vous devriez voir:
# ✓ weather_historical.csv (plusieurs milliers de lignes)
# ✓ crop_production.csv (50,000 lignes)
# ✓ soil_properties.csv (100,000 lignes)
# ✓ irrigation.csv (80,000 lignes)
# ✓ fertilizers.csv (70,000 lignes)
# ✓ pests_diseases.csv (60,000 lignes)
# ✓ farms.csv (100,000 lignes)
# ✓ weather_stations.csv (500,000 lignes)
# ✓ market_prices.csv (150,000 lignes)
# Total: 1,000,000+ observations
```

---

## 🚀 ÉTAPE 2: Installation de l'Application Django

### 2.1 Retour au dossier principal
```bash
cd ..  # Retour à agri_smart/
```

### 2.2 Installer Django et dépendances
```bash
pip install -r requirements.txt

# Cette commande installe:
# - Django 5.0
# - Django REST Framework
# - PyTorch (pour ML)
# - Transformers (Hugging Face)
# - Scikit-learn
# - Pandas, NumPy
# - Et toutes les autres dépendances
```

### 2.3 Créer le fichier .env
```bash
# Créer le fichier .env à la racine
cat > .env << EOF
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-$(openssl rand -hex 32)
DJANGO_SETTINGS_MODULE=agri_smart_project.settings

# Database (SQLite par défaut, PostgreSQL pour production)
DATABASE_URL=sqlite:///db.sqlite3

# Celery (optionnel pour tâches asynchrones)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Hugging Face (optionnel, pour modèles avancés)
HUGGINGFACE_TOKEN=your_token_here
EOF
```

---

## 💾 ÉTAPE 3: Configuration de la Base de Données

### 3.1 Créer les migrations
```bash
# Créer les fichiers de migration
python manage.py makemigrations core
python manage.py makemigrations ml_models
python manage.py makemigrations chatbot
python manage.py makemigrations api

# Appliquer les migrations
python manage.py migrate
```

### 3.2 Créer un superutilisateur
```bash
python manage.py createsuperuser

# Suivre les instructions:
# Username: admin
# Email: admin@agrismart.cm
# Password: (choisir un mot de passe sécurisé)
```

### 3.3 Charger les données initiales
```bash
# Créer un script de chargement de données
python manage.py loaddata initial_crops
python manage.py loaddata initial_regions

# Ou importer les données scrapées:
python manage.py import_scraped_data
```

---

## 🤖 ÉTAPE 4: Entraînement des Modèles ML

### 4.1 Préparer les données d'entraînement
```bash
# Lancer le script de préparation des données
python ml_models/prepare_data.py

# Ce script va:
# - Nettoyer les données scrapées
# - Créer les features d'entraînement
# - Séparer train/test sets
# - Sauvegarder dans ml_models/data/
```

### 4.2 Entraîner les modèles
```bash
# Entraîner le modèle de recommandation de cultures
python ml_models/train_recommender.py

# Entraîner le modèle de prédiction de rendement
python ml_models/train_yield_predictor.py

# Entraîner le modèle de risque de maladies
python ml_models/train_disease_predictor.py

# Les modèles entraînés seront sauvegardés dans:
# ml_models/trained_models/
```

### 4.3 Télécharger les modèles Hugging Face
```bash
# Les modèles seront téléchargés automatiquement au premier usage
# Pour les télécharger à l'avance:
python manage.py download_hf_models

# Cela téléchargera:
# - google/vit-base-patch16-224 (classification d'images)
# - microsoft/phi-2 (génération de texte)
# - deepset/roberta-base-squad2 (question-answering)
```

---

## 🎨 ÉTAPE 5: Collecte des Fichiers Statiques

```bash
# Collecter tous les fichiers CSS, JS, images
python manage.py collectstatic --noinput

# Les fichiers seront copiés dans staticfiles/
```

---

## 🚀 ÉTAPE 6: Démarrage de l'Application

### 6.1 Démarrage en mode développement
```bash
# Démarrer le serveur Django
python manage.py runserver

# L'application sera accessible à:
# http://127.0.0.1:8000/

# Interface d'administration:
# http://127.0.0.1:8000/admin/
```

### 6.2 Démarrage du Chatbot WebSocket (optionnel)
```bash
# Dans un nouveau terminal (avec venv activé)
daphne -b 0.0.0.0 -p 8001 agri_smart_project.asgi:application

# Le chatbot WebSocket sera accessible sur le port 8001
```

### 6.3 Démarrage de Celery (optionnel, pour tâches asynchrones)
```bash
# Terminal 1: Démarrer Redis (si installé)
redis-server

# Terminal 2: Démarrer Celery worker
celery -A agri_smart_project worker -l info

# Terminal 3: Démarrer Celery beat (tâches périodiques)
celery -A agri_smart_project beat -l info
```

---

## 💬 ÉTAPE 7: Configuration du Chatbot

### 7.1 Tester le chatbot
```bash
# Ouvrir Python shell
python manage.py shell

# Tester le chatbot
from chatbot.chatbot import get_chatbot
bot = get_chatbot()

# Poser une question
response = bot.get_response("Comment cultiver le maïs?", user_id="test_user", language="fr")
print(response)
```

### 7.2 Interface Web du Chatbot
- Accéder à http://127.0.0.1:8000/chatbot/
- Le chatbot sera intégré dans toutes les pages via le widget flottant

---

## 🌐 ÉTAPE 8: Déploiement en Production

### 8.1 Configuration pour production

#### Modifier .env pour production:
```bash
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-super-secret-production-key

# Utiliser PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/agri_smart_db
```

#### Installer PostgreSQL:
```bash
# Ubuntu
sudo apt install postgresql postgresql-contrib

# Créer la base de données
sudo -u postgres psql
CREATE DATABASE agri_smart_db;
CREATE USER agri_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE agri_smart_db TO agri_user;
\q

# Installer le driver Python
pip install psycopg2-binary
```

### 8.2 Configurer Nginx (Serveur Web)
```bash
# Installer Nginx
sudo apt install nginx

# Créer la configuration
sudo nano /etc/nginx/sites-available/agri_smart

# Ajouter:
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/agri_smart/staticfiles/;
    }

    location /media/ {
        alias /path/to/agri_smart/media/;
    }
}

# Activer le site
sudo ln -s /etc/nginx/sites-available/agri_smart /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8.3 Configurer Gunicorn (Serveur WSGI)
```bash
# Installer Gunicorn
pip install gunicorn

# Créer un fichier systemd service
sudo nano /etc/systemd/system/agri_smart.service

# Ajouter:
[Unit]
Description=Agri Smart Django Application
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory=/path/to/agri_smart
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 agri_smart_project.wsgi:application

[Install]
WantedBy=multi-user.target

# Activer et démarrer
sudo systemctl enable agri_smart
sudo systemctl start agri_smart
sudo systemctl status agri_smart
```

### 8.4 Configuration SSL/HTTPS (Let's Encrypt)
```bash
# Installer Certbot
sudo apt install certbot python3-certbot-nginx

# Obtenir un certificat SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Le renouvellement automatique est configuré
```

---

## 📊 ÉTAPE 9: Tests et Validation

### 9.1 Tester les fonctionnalités principales
```bash
# Lancer les tests Django
python manage.py test

# Tester le scraper
cd data_scraper
python -m pytest tests/

# Tester les modèles ML
cd ../ml_models
python test_models.py
```

### 9.2 Vérifier les performances
- Recommandation de cultures: temps de réponse < 500ms
- Prédiction de rendement: temps de réponse < 300ms
- Chatbot: temps de réponse < 2s

---

## 🔍 ÉTAPE 10: Résolution des Problèmes Courants

### Problème: ModuleNotFoundError
```bash
# Solution: Réinstaller les dépendances
pip install -r requirements.txt --upgrade
```

### Problème: Erreur de migration
```bash
# Solution: Réinitialiser les migrations
python manage.py migrate --run-syncdb
```

### Problème: Erreur Hugging Face (Timeout)
```bash
# Solution: Télécharger manuellement
python
>>> from transformers import AutoModel
>>> AutoModel.from_pretrained("microsoft/phi-2")
```

### Problème: Modèles ML non trouvés
```bash
# Solution: Réentraîner les modèles
python ml_models/train_all_models.py
```

### Problème: Chatbot ne répond pas
```bash
# Vérifier les logs
tail -f logs/agri_smart.log

# Redémarrer le service
sudo systemctl restart agri_smart
```

---

## 📱 Utilisation de l'Application

### Interface Utilisateur

#### 1. Page d'Accueil
- Présentation des fonctionnalités
- Statistiques générales
- Accès rapide aux outils

#### 2. Tableau de Bord
- Vue d'ensemble de vos fermes
- Statistiques de production
- Alertes et recommandations

#### 3. Recommandation de Cultures
- Entrer les paramètres (sol, climat, etc.)
- Obtenir des recommandations personnalisées
- Consulter les pratiques culturales

#### 4. Prédiction de Rendement
- Sélectionner culture et paramètres
- Obtenir estimation de rendement
- Consulter recommandations d'amélioration

#### 5. Prix de Marché
- Suivre l'évolution des prix
- Visualisations interactives
- Prévisions de tendances

#### 6. Chatbot Agricole
- Poser des questions en français ou anglais
- Obtenir des conseils personnalisés
- Historique des conversations

---

## 🔐 Sécurité

### Bonnes pratiques
1. Changer SECRET_KEY en production
2. Utiliser HTTPS (SSL/TLS)
3. Limiter les accès API
4. Sauvegardes régulières de la base de données
5. Mettre à jour les dépendances régulièrement

```bash
# Sauvegarder la base de données
python manage.py dumpdata > backup.json

# Ou avec PostgreSQL:
pg_dump agri_smart_db > backup.sql
```

---

## 📚 Documentation API

### Endpoints principaux

#### Recommandation de cultures
```
POST /api/recommendations/
{
    "temperature": 28.5,
    "humidity": 75.0,
    "rainfall": 1200,
    "soil_ph": 6.5,
    "soil_type": "LOAM",
    "region": "CENTER"
}
```

#### Prédiction de rendement
```
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
```

#### Chatbot
```
POST /api/chatbot/
{
    "message": "Comment cultiver le riz?",
    "language": "fr"
}
```

---

## 📞 Support

Pour toute question ou problème:
- Email: support@agrismart.cm
- Documentation: https://docs.agrismart.cm
- Issues GitHub: https://github.com/agrismart/issues

---

## 🎉 Félicitations!

Votre application Agri Smart est maintenant opérationnelle!

**Prochaines étapes recommandées:**
1. Personnaliser les templates HTML/CSS
2. Ajouter plus de cultures dans la base de données
3. Affiner les modèles ML avec vos données
4. Intégrer des services externes (météo en temps réel, SMS, etc.)
5. Déployer sur un serveur cloud (AWS, Google Cloud, DigitalOcean)

**Bon développement! 🌱🚀**

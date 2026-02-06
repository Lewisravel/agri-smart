# 🚀 GUIDE DE DÉMARRAGE RAPIDE - AGRI SMART

## 📥 Étape 1: Extraction

Extrayez le fichier `agri_smart_complete.zip` dans un dossier de votre choix.

```bash
unzip agri_smart_complete.zip
cd agri_smart
```

## 🔧 Étape 2: Installation Automatique

### Sur Linux/macOS:
```bash
chmod +x quick_start.sh
./quick_start.sh
```

Le script va:
- ✅ Créer l'environnement virtuel
- ✅ Installer les dépendances
- ✅ Configurer la base de données
- ✅ Proposer de scraper les données
- ✅ Créer un superutilisateur
- ✅ Démarrer le serveur

### Sur Windows:
```cmd
# 1. Ouvrir PowerShell ou CMD dans le dossier agri_smart

# 2. Créer environnement virtuel
python -m venv venv
venv\Scripts\activate

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Configuration base de données
python manage.py migrate

# 5. Créer admin
python manage.py createsuperuser

# 6. Démarrer serveur
python manage.py runserver
```

## 🌐 Étape 3: Accès à l'Application

Une fois le serveur démarré, ouvrez votre navigateur:

- **Application:** http://127.0.0.1:8000/
- **Administration:** http://127.0.0.1:8000/admin/
- **API:** http://127.0.0.1:8000/api/

## 🎮 Étape 4: Utilisation

### A. Page d'Accueil
- Découvrez les fonctionnalités
- Cliquez sur "Commencer" pour tester

### B. Recommandation de Cultures
1. Allez sur "Recommandations" dans le menu
2. Entrez vos données:
   - Température: 28°C
   - Humidité: 75%
   - Précipitations: 1200mm
   - pH du sol: 6.5
3. Cliquez sur "Obtenir Recommandations"

### C. Prédiction de Rendement
1. Allez sur "Prévisions"
2. Choisissez une culture (ex: Maïs)
3. Entrez les paramètres
4. Obtenez la prédiction

### D. Chatbot
1. Cliquez sur l'icône de chat en bas à droite
2. Posez vos questions:
   - "Comment cultiver le maïs?"
   - "Quel est le meilleur engrais pour le riz?"
   - "Quelles sont les maladies de la tomate?"

### E. Prix de Marché
- Consultez l'évolution des prix
- Graphiques interactifs

## 📊 Étape 5: Scraping de Données (Optionnel)

Pour scraper 1M+ observations de données agricoles:

```bash
cd data_scraper
python scraper.py
```

Cela prendra 10-30 minutes et créera un dossier `data/` avec:
- weather_historical.csv
- crop_production.csv
- soil_properties.csv
- farms.csv
- market_prices.csv
- etc. (9 fichiers au total)

## 🔐 Étape 6: Administration

Connectez-vous à http://127.0.0.1:8000/admin/ avec:
- Username: celui que vous avez créé
- Password: votre mot de passe

Vous pouvez:
- Ajouter des cultures
- Gérer les fermes
- Voir les prédictions
- Configurer les prix

## 🌍 Étape 7: Changement de Langue

1. Cliquez sur le sélecteur de langue en haut à droite
2. Choisissez entre Français 🇫🇷 ou English 🇬🇧

## 🌓 Étape 8: Mode Sombre

Activez le mode sombre avec le bouton toggle en haut à droite.

## 📡 Étape 9: Test de l'API

### Avec curl:
```bash
# Recommandation
curl -X POST http://localhost:8000/api/recommendations/ \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28.5,
    "humidity": 75.0,
    "rainfall": 1200,
    "soil_ph": 6.5,
    "soil_type": "LOAM",
    "region": "CENTER"
  }'

# Chatbot
curl -X POST http://localhost:8000/api/chatbot/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Comment cultiver le maïs?",
    "language": "fr"
  }'
```

### Avec Python:
```python
import requests

response = requests.post('http://localhost:8000/api/recommendations/', json={
    "temperature": 28.5,
    "humidity": 75.0,
    "rainfall": 1200,
    "soil_ph": 6.5,
    "soil_type": "LOAM",
    "region": "CENTER"
})
print(response.json())
```

## 🐛 Résolution de Problèmes

### Erreur: "Port already in use"
```bash
python manage.py runserver 8001
```

### Erreur: "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### Erreur: Migration
```bash
python manage.py migrate --run-syncdb
```

### Erreur: Permission denied (Linux/Mac)
```bash
chmod +x manage.py
chmod +x quick_start.sh
```

## 📚 Documentation Complète

Pour plus de détails, consultez:
- **INSTALLATION_GUIDE.md** - Guide complet étape par étape
- **API_DOCUMENTATION.md** - Documentation API REST
- **README.md** - Vue d'ensemble du projet
- **SUMMARY.md** - Récapitulatif

## 🎯 Fonctionnalités Principales

✅ Recommandation de cultures IA
✅ Prédiction de rendement
✅ Chatbot agricole intelligent
✅ Gestion des maladies
✅ Prix de marché
✅ Visualisations interactives
✅ Mode clair/sombre
✅ Multilingue (FR/EN)
✅ API REST complète

## 📞 Besoin d'Aide?

- Email: contact@agrismart.cm
- Documentation: Voir fichiers .md inclus
- GitHub: https://github.com/agrismart

## 🎉 C'est Tout!

Vous êtes maintenant prêt à utiliser Agri Smart!

**Astuce:** Commencez par tester le chatbot et la recommandation de cultures pour voir la puissance de l'IA.

---

**🌱 Bonne utilisation! 🚀**

#!/bin/bash

# ===============================================
# AGRI SMART - Script de Démarrage Rapide
# ===============================================

echo "🌱 ================================================"
echo "🌱  AGRI SMART - Agriculture Intelligente"
echo "🌱  Script de démarrage rapide"
echo "🌱 ================================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérifier Python
echo -e "${BLUE}🔍 Vérification de Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé!${NC}"
    echo "Veuillez installer Python 3.9+ avant de continuer."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✅ Python $PYTHON_VERSION détecté${NC}"
echo ""

# Créer l'environnement virtuel si nécessaire
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Création de l'environnement virtuel...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Environnement virtuel créé${NC}"
else
    echo -e "${GREEN}✅ Environnement virtuel existe déjà${NC}"
fi
echo ""

# Activer l'environnement virtuel
echo -e "${BLUE}🔌 Activation de l'environnement virtuel...${NC}"
source venv/bin/activate
echo -e "${GREEN}✅ Environnement activé${NC}"
echo ""

# Installer les dépendances
echo -e "${BLUE}📚 Installation des dépendances...${NC}"
echo "Cela peut prendre 5-10 minutes..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dépendances installées avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'installation des dépendances${NC}"
    exit 1
fi
echo ""

# Créer le fichier .env si nécessaire
if [ ! -f ".env" ]; then
    echo -e "${BLUE}⚙️  Création du fichier .env...${NC}"
    cat > .env << EOF
DEBUG=True
SECRET_KEY=django-insecure-$(openssl rand -hex 32)
DJANGO_SETTINGS_MODULE=agri_smart_project.settings
DATABASE_URL=sqlite:///db.sqlite3
EOF
    echo -e "${GREEN}✅ Fichier .env créé${NC}"
else
    echo -e "${GREEN}✅ Fichier .env existe déjà${NC}"
fi
echo ""

# Créer les dossiers nécessaires
echo -e "${BLUE}📁 Création des dossiers...${NC}"
mkdir -p data logs media staticfiles ml_models/trained_models
echo -e "${GREEN}✅ Dossiers créés${NC}"
echo ""

# Scraping des données (optionnel)
echo -e "${YELLOW}📊 Scraping des données agricoles${NC}"
echo "Cette étape peut prendre 10-30 minutes."
read -p "Voulez-vous scraper les données maintenant? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[OoYy]$ ]]; then
    echo -e "${BLUE}🕷️  Démarrage du scraping...${NC}"
    cd data_scraper
    pip install -r requirements.txt > /dev/null 2>&1
    python scraper.py
    cd ..
    echo -e "${GREEN}✅ Scraping terminé${NC}"
else
    echo -e "${YELLOW}⏭️  Scraping ignoré${NC}"
fi
echo ""

# Migrations de la base de données
echo -e "${BLUE}🗄️  Configuration de la base de données...${NC}"
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo -e "${GREEN}✅ Base de données configurée${NC}"
echo ""

# Créer un superutilisateur
echo -e "${YELLOW}👤 Création du superutilisateur${NC}"
echo "Ceci permettra d'accéder à l'interface d'administration."
read -p "Voulez-vous créer un superutilisateur maintenant? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[OoYy]$ ]]; then
    python manage.py createsuperuser
else
    echo -e "${YELLOW}⏭️  Création de superutilisateur ignorée${NC}"
    echo "Vous pouvez le créer plus tard avec: python manage.py createsuperuser"
fi
echo ""

# Collecter les fichiers statiques
echo -e "${BLUE}🎨 Collecte des fichiers statiques...${NC}"
python manage.py collectstatic --noinput > /dev/null 2>&1
echo -e "${GREEN}✅ Fichiers statiques collectés${NC}"
echo ""

# Charger les données initiales
echo -e "${BLUE}🌱 Chargement des données initiales...${NC}"
if [ -f "core/fixtures/initial_crops.json" ]; then
    python manage.py loaddata initial_crops
fi
echo -e "${GREEN}✅ Données initiales chargées${NC}"
echo ""

# Démarrer le serveur
echo -e "${GREEN}🎉 ================================================${NC}"
echo -e "${GREEN}    Installation terminée avec succès!${NC}"
echo -e "${GREEN}🎉 ================================================${NC}"
echo ""
echo -e "${BLUE}📌 Informations importantes:${NC}"
echo "   • Application: http://127.0.0.1:8000/"
echo "   • Administration: http://127.0.0.1:8000/admin/"
echo "   • API: http://127.0.0.1:8000/api/"
echo ""
echo -e "${YELLOW}🚀 Pour démarrer le serveur, exécutez:${NC}"
echo "   python manage.py runserver"
echo ""
echo -e "${YELLOW}📚 Documentation complète:${NC}"
echo "   Voir INSTALLATION_GUIDE.md"
echo ""

# Demander si on doit démarrer le serveur
read -p "Voulez-vous démarrer le serveur maintenant? (o/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[OoYy]$ ]]; then
    echo -e "${BLUE}🚀 Démarrage du serveur...${NC}"
    echo ""
    python manage.py runserver
else
    echo -e "${YELLOW}Pour démarrer le serveur plus tard:${NC}"
    echo "   source venv/bin/activate"
    echo "   python manage.py runserver"
fi

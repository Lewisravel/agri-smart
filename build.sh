#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Début du build..."

# Mise à jour de pip
echo "📦 Mise à jour de pip..."
pip install --upgrade pip

# Installation des dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements_prod.txt

# Collecte des fichiers statiques
echo "🎨 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

# Migrations de la base de données
echo "🗄️ Migrations de la base de données..."
python manage.py migrate --no-input

# Entraînement des modèles ML (optionnel, peut être commenté si trop long)
echo "🤖 Entraînement des modèles ML..."
python train_models.py || echo "⚠️ Entraînement des modèles échoué, continuons..."

# Chargement des données initiales
echo "📊 Chargement des données initiales..."
python load_data.py || echo "⚠️ Chargement des données échoué, continuons..."

echo "✅ Build terminé avec succès!"

# 🚀 GUIDE DE DÉPLOIEMENT - AGRI SMART

## 📋 FICHIERS NÉCESSAIRES

Tous ces fichiers doivent être à la racine du projet:

```
agri_smart/
├── requirements_prod.txt    ✅ Dépendances production
├── runtime.txt              ✅ Version Python
├── Procfile                 ✅ Commande de démarrage
├── build.sh                 ✅ Script de build
├── .env.example             ✅ Template variables d'environnement
├── .gitignore               ✅ Fichiers à ignorer
└── manage.py
```

---

## 🔧 ÉTAPE 1: PRÉPARER LE CODE

### 1. Modifier `settings.py`

Ouvrez `agri_smart_project/settings.py` et ajoutez **À LA FIN DU FICHIER**:

```python
# Copier tout le contenu de settings_production_addon.py ici
```

### 2. Ajouter WhiteNoise au middleware

Dans `settings.py`, trouvez `MIDDLEWARE` et ajoutez:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← AJOUTER ICI
    # ... reste du middleware
]
```

---

## 🌐 ÉTAPE 2: CRÉER UN REPOSITORY GITHUB

### 1. Initialiser Git

```cmd
cd C:\Users\HP\Desktop\MES_PROJETS\Final\agri_smart_complete\agri_smart

git init
git add .
git commit -m "Initial commit - Ready for deployment"
```

### 2. Créer repository sur GitHub

1. Allez sur https://github.com/new
2. Nom: `agri-smart`
3. Public ou Private: votre choix
4. Ne cochez rien d'autre
5. Cliquez "Create repository"

### 3. Pousser le code

```cmd
git remote add origin https://github.com/VOTRE_USERNAME/agri-smart.git
git branch -M main
git push -u origin main
```

---

## 🎯 ÉTAPE 3: DÉPLOYER SUR RENDER

### 1. Créer un compte

1. Allez sur https://render.com
2. "Get Started for Free"
3. Inscrivez-vous avec GitHub

### 2. Créer un Web Service

1. Dashboard → "New +" → "Web Service"
2. Connectez votre repo GitHub
3. Cliquez "Connect" sur `agri-smart`

### 3. Configuration

**Name:** `agri-smart`

**Region:** `Frankfurt (EU Central)`

**Branch:** `main`

**Runtime:** `Python 3`

**Build Command:**
```bash
chmod +x build.sh && ./build.sh
```

**Start Command:**
```bash
gunicorn agri_smart_project.wsgi:application
```

**Instance Type:** `Free`

### 4. Variables d'environnement

Cliquez "Advanced" → "Add Environment Variable"

```
RENDER=True
SECRET_KEY=[généré avec la commande ci-dessous]
PYTHON_VERSION=3.11.7
DEBUG=False
```

**Générer SECRET_KEY:**
```cmd
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Déployer

Cliquez "Create Web Service"

⏳ Attendre 5-10 minutes

✅ URL finale: `https://agri-smart.onrender.com`

---

## 🔑 ÉTAPE 4: CRÉER SUPERUSER EN PRODUCTION

1. Dans Render Dashboard → votre service
2. Cliquez "Shell" (menu gauche)
3. Tapez:

```bash
python manage.py createsuperuser
```

Username: `admin`
Email: `admin@agrismart.cm`
Password: (votre choix)

---

## 🔄 ÉTAPE 5: MISES À JOUR

Pour mettre à jour l'application:

```cmd
git add .
git commit -m "Description de vos modifications"
git push origin main
```

Render redéploie automatiquement! 🎉

---

## 🐛 RÉSOLUTION DE PROBLÈMES

### Erreur: "Failed to build"

**Solution:** Vérifiez les logs dans Render. Souvent:
- `requirements_prod.txt` mal formaté
- `build.sh` pas exécutable

**Fix:**
```cmd
git update-index --chmod=+x build.sh
git commit -m "Fix build.sh permissions"
git push
```

### Erreur: "Static files not found"

**Solution:** Vérifiez que WhiteNoise est installé et configuré

### Base de données vide

**Solution:** Dans Render Shell:
```bash
python load_data.py
```

### Erreur 502

**Solution:** Vérifiez que Gunicorn est dans requirements_prod.txt

---

## 📊 ALTERNATIVES GRATUITES

### Option B: Railway.app

1. https://railway.app
2. New Project → Deploy from GitHub
3. Sélectionner repo
4. Ajouter variables d'environnement
5. Déploiement automatique

### Option C: PythonAnywhere

1. https://www.pythonanywhere.com
2. Create account (Free)
3. Bash console:
```bash
git clone https://github.com/VOTRE_USERNAME/agri-smart.git
mkvirtualenv agri --python=/usr/bin/python3.10
pip install -r requirements_prod.txt
```
4. Web tab → Manual configuration
5. Configurer WSGI et static files

---

## ✅ CHECKLIST

Avant de déployer:

- [ ] `requirements_prod.txt` à la racine
- [ ] `runtime.txt` à la racine
- [ ] `Procfile` à la racine
- [ ] `build.sh` à la racine et exécutable
- [ ] `settings.py` modifié avec config production
- [ ] WhiteNoise ajouté au middleware
- [ ] Code pushé sur GitHub
- [ ] Compte Render créé
- [ ] Service configuré
- [ ] Variables d'environnement ajoutées
- [ ] Service déployé
- [ ] Superuser créé
- [ ] Application testée en ligne

---

## 🎉 SUCCÈS!

Votre application est en ligne à:

**https://votre-app.onrender.com**

Partagez cette URL avec vos utilisateurs! 🌍

---

## 📞 SUPPORT

Si vous rencontrez des problèmes:

1. Vérifiez les logs dans Render Dashboard
2. Testez localement d'abord
3. Consultez la documentation Render
4. Cherchez l'erreur sur Stack Overflow

---

**Bon déploiement! 🚀**

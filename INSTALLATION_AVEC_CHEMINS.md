# 📁 GUIDE D'INSTALLATION AVEC CHEMINS DÉTAILLÉS

## 🗂️ STRUCTURE COMPLÈTE DU PROJET

Voici où chaque fichier doit se trouver dans votre projet:

```
C:\Users\HP\Desktop\MES_PROJETS\agri_smart\
│
├── 📄 manage.py
├── 📄 requirements.txt
├── 📄 train_models.py
├── 📄 load_data.py
├── 📄 .env
├── 📄 README.md
├── 📄 INSTALLATION_GUIDE.md
├── 📄 .gitignore
│
├── 📁 agri_smart_project\
│   ├── __init__.py
│   ├── settings.py        ← MODIFIÉ (accounts ajouté)
│   ├── urls.py            ← MODIFIÉ (accounts/ ajouté)
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
│
├── 📁 accounts\              ← NOUVEAU DOSSIER
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py           ← Connexion/Inscription/Déconnexion
│   ├── urls.py
│   └── admin.py
│
├── 📁 core\
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py           ← MODIFIÉ (login_required retiré)
│   ├── urls.py
│   ├── admin.py
│   └── signals.py
│
├── 📁 ml_models\
│   ├── __init__.py
│   ├── predictor.py
│   ├── visualizer.py
│   └── trained_models\     ← Modèles ML (.pkl)
│
├── 📁 chatbot\
│   ├── __init__.py
│   ├── chatbot.py
│   ├── consumers.py
│   └── routing.py
│
├── 📁 api\
│   ├── __init__.py
│   ├── views.py
│   └── urls.py
│
├── 📁 templates\
│   ├── base.html          ← MODIFIÉ (liens login/register)
│   │
│   ├── 📁 accounts\        ← NOUVEAU DOSSIER
│   │   ├── login.html
│   │   └── register.html
│   │
│   └── 📁 core\
│       ├── index.html
│       ├── dashboard.html
│       ├── crop_recommendation.html
│       └── yield_prediction.html
│
├── 📁 static\
│   ├── 📁 css\
│   │   └── style.css
│   └── 📁 js\
│       └── app.js
│
├── 📁 data_scraper\
│   ├── scraper.py
│   ├── requirements.txt
│   └── 📁 data\           ← Données CSV (après scraping)
│
├── 📁 media\              ← Uploads utilisateurs
├── 📁 staticfiles\        ← Fichiers statiques collectés
└── 📁 logs\               ← Logs de l'application
```

---

## 📋 CHECKLIST DES FICHIERS MODIFIÉS/AJOUTÉS

### ✅ Fichiers NOUVEAUX à créer:

**1. Dossier accounts/** (créer ce dossier)
```
C:\Users\HP\Desktop\MES_PROJETS\agri_smart\accounts\
```

**2. Dans accounts/:**
- `__init__.py`
- `apps.py`
- `models.py`
- `views.py`
- `urls.py`
- `admin.py`

**3. Dossier templates/accounts/** (créer ce dossier)
```
C:\Users\HP\Desktop\MES_PROJETS\agri_smart\templates\accounts\
```

**4. Dans templates/accounts/:**
- `login.html`
- `register.html`

### ✏️ Fichiers MODIFIÉS:

**1. agri_smart_project/settings.py**
- Ajouter `'accounts'` dans `INSTALLED_APPS`
- Ajouter à la fin:
```python
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'index'
```

**2. agri_smart_project/urls.py**
- Ajouter: `path('accounts/', include('accounts.urls')),`

**3. templates/base.html**
- Remplacer la section navbar avec liens login/register/logout

**4. core/views.py**
- Retirer `@login_required` de:
  - `crop_recommendation`
  - `yield_prediction`
  - `market_prices_view`
  - `visualization_view`

---

## 🚀 ÉTAPES D'INSTALLATION APRÈS EXTRACTION DU ZIP

### ÉTAPE 1: Extraire et Vérifier

```cmd
# Aller dans le dossier
cd C:\Users\HP\Desktop\MES_PROJETS\agri_smart

# Vérifier que le dossier accounts existe
dir accounts

# Vérifier que templates\accounts existe
dir templates\accounts
```

### ÉTAPE 2: Environnement Virtuel

```cmd
# Si pas encore créé
python -m venv venv

# Activer
venv\Scripts\activate
```

### ÉTAPE 3: Installer Dépendances

```cmd
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer
pip install -r requirements.txt
```

### ÉTAPE 4: Configuration Base de Données

```cmd
# Créer .env si pas présent
echo DEBUG=True > .env
echo SECRET_KEY=django-insecure-change-this >> .env

# Migrations
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py migrate
```

### ÉTAPE 5: Créer Superutilisateur

```cmd
python manage.py createsuperuser
```

**Exemple:**
- Username: `admin`
- Email: `admin@agrismart.cm`
- Password: `admin123` (choisir un mot de passe sécurisé)

### ÉTAPE 6: Charger Données Initiales

```cmd
# Entraîner les modèles ML
python train_models.py

# Charger les données de base
python load_data.py
```

### ÉTAPE 7: Fichiers Statiques

```cmd
python manage.py collectstatic --noinput
```

### ÉTAPE 8: Lancer l'Application

```cmd
python manage.py runserver
```

**Accès:**
- Application: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Login: http://127.0.0.1:8000/accounts/login/
- Register: http://127.0.0.1:8000/accounts/register/

---

## 🧪 TESTER L'APPLICATION

### Test 1: Page d'Accueil
```
✅ http://127.0.0.1:8000/
✅ Devrait s'afficher sans erreur
✅ Menu avec "Connexion" et "Inscription" visible
```

### Test 2: Inscription
```
✅ Cliquer sur "Inscription"
✅ Créer un nouveau compte
✅ Redirection automatique vers le dashboard
```

### Test 3: Connexion avec Compte Démo
```
✅ Aller sur "Connexion"
✅ Username: demo
✅ Password: demo123
✅ Connexion réussie
```

### Test 4: Recommandations (sans login)
```
✅ http://127.0.0.1:8000/recommend/
✅ Devrait fonctionner sans être connecté
```

### Test 5: Dashboard (avec login requis)
```
✅ http://127.0.0.1:8000/dashboard/
✅ Si pas connecté → redirection vers login
✅ Si connecté → affichage du dashboard
```

---

## 🔍 VÉRIFICATION DES FICHIERS

### Commande PowerShell pour vérifier:

```powershell
# Vérifier la structure
Get-ChildItem -Recurse -Directory | Select-Object FullName

# Vérifier fichiers accounts
Get-ChildItem accounts\ -Name

# Vérifier templates accounts
Get-ChildItem templates\accounts\ -Name
```

**Résultat attendu pour accounts/:**
```
__init__.py
admin.py
apps.py
models.py
urls.py
views.py
```

**Résultat attendu pour templates/accounts/:**
```
login.html
register.html
```

---

## ❗ PROBLÈMES COURANTS ET SOLUTIONS

### Problème 1: "No module named 'accounts'"

**Solution:**
```cmd
# Vérifier que accounts est dans INSTALLED_APPS
python manage.py check

# Réinstaller
pip install -r requirements.txt
```

### Problème 2: "TemplateDoesNotExist at /accounts/login/"

**Solution:**
```cmd
# Vérifier que le dossier existe
dir templates\accounts

# Créer si manquant
mkdir templates\accounts

# Copier les fichiers login.html et register.html
```

### Problème 3: "Reverse for 'accounts:login' not found"

**Solution:**
```cmd
# Vérifier urls.py principal
# Doit contenir: path('accounts/', include('accounts.urls'))

# Vérifier accounts/urls.py existe
dir accounts\urls.py
```

### Problème 4: Erreur 404 sur /accounts/login/

**Solution:**
```cmd
# Lancer les migrations
python manage.py migrate

# Redémarrer le serveur
# CTRL+C puis
python manage.py runserver
```

---

## 📞 AIDE SUPPLÉMENTAIRE

Si vous rencontrez des erreurs:

1. **Vérifier les logs:**
```cmd
type logs\agri_smart.log
```

2. **Vérifier la console Django:**
Regarder les messages dans le terminal où `runserver` tourne

3. **Mode DEBUG:**
Dans `.env`, assurez-vous que `DEBUG=True`

4. **Tester les URLs:**
```cmd
python manage.py show_urls
```

---

## ✅ VALIDATION FINALE

Avant de considérer l'installation réussie, cochez:

- [ ] Dossier `accounts/` existe avec 6 fichiers
- [ ] Dossier `templates/accounts/` existe avec 2 fichiers
- [ ] `settings.py` contient `'accounts'` dans INSTALLED_APPS
- [ ] `urls.py` contient `path('accounts/', ...)`
- [ ] Migrations effectuées sans erreur
- [ ] Serveur démarre sans erreur
- [ ] Page login accessible: http://127.0.0.1:8000/accounts/login/
- [ ] Page register accessible: http://127.0.0.1:8000/accounts/register/
- [ ] Connexion avec compte démo fonctionne
- [ ] Déconnexion fonctionne
- [ ] Recommandations accessibles sans login

---

## 🎉 FÉLICITATIONS!

Si toutes les cases sont cochées, votre application est **100% fonctionnelle**!

**Comptes disponibles:**
- **Admin:** Username défini à l'étape 5
- **Démo:** Username `demo`, Password `demo123`

**Prochaines étapes:**
1. Scraper plus de données (optionnel)
2. Personnaliser les templates
3. Ajouter vos propres cultures
4. Déployer en production

---

**📧 Besoin d'aide? Référez-vous à INSTALLATION_GUIDE.md pour plus de détails.**

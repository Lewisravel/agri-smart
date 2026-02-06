# 🪟 GUIDE D'INSTALLATION WINDOWS - ÉTAPE PAR ÉTAPE

## 📥 ÉTAPE 1: EXTRACTION DU ZIP

1. **Téléchargez** `agri_smart_complete.zip`
2. **Clic droit** sur le fichier → **Extraire tout**
3. **Choisissez** le dossier de destination:
   ```
   C:\Users\HP\Desktop\MES_PROJETS\
   ```
4. **Résultat:** Un dossier `agri_smart` est créé

---

## 📂 ÉTAPE 2: VÉRIFICATION DE LA STRUCTURE

Ouvrez l'Explorateur Windows et naviguez vers:
```
C:\Users\HP\Desktop\MES_PROJETS\agri_smart\
```

### ✅ Vous DEVEZ voir ces dossiers:

```
📁 agri_smart\
    ├── 📁 accounts              ← NOUVEAU (système de connexion)
    ├── 📁 agri_smart_project
    ├── 📁 api
    ├── 📁 chatbot
    ├── 📁 core
    ├── 📁 data
    ├── 📁 data_scraper
    ├── 📁 logs
    ├── 📁 media
    ├── 📁 ml_models
    ├── 📁 static
    ├── 📁 templates
    └── 📄 manage.py
```

### ✅ Dans le dossier `accounts\`:

```
📁 accounts\
    ├── 📄 __init__.py
    ├── 📄 admin.py
    ├── 📄 apps.py
    ├── 📄 models.py
    ├── 📄 urls.py
    └── 📄 views.py          ← Gère connexion/inscription
```

### ✅ Dans le dossier `templates\accounts\`:

```
📁 templates\
    └── 📁 accounts\
        ├── 📄 login.html      ← Page de connexion
        └── 📄 register.html   ← Page d'inscription
```

---

## 💻 ÉTAPE 3: OUVRIR LE TERMINAL

1. **Ouvrez** l'Explorateur de fichiers
2. **Naviguez** vers `C:\Users\HP\Desktop\MES_PROJETS\agri_smart\`
3. Dans la barre d'adresse, **tapez** `cmd` et appuyez sur **Entrée**
4. Une fenêtre de **commande** s'ouvre dans le bon dossier

---

## 🐍 ÉTAPE 4: ENVIRONNEMENT VIRTUEL

Dans le terminal CMD qui vient de s'ouvrir:

```cmd
REM Créer l'environnement virtuel
python -m venv venv

REM Attendre que ça termine (peut prendre 1-2 minutes)

REM Activer l'environnement
venv\Scripts\activate
```

**✅ Résultat attendu:**
Vous devriez voir `(venv)` au début de la ligne:
```
(venv) C:\Users\HP\Desktop\MES_PROJETS\agri_smart>
```

---

## 📦 ÉTAPE 5: INSTALLATION DES DÉPENDANCES

```cmd
REM Mettre à jour pip
python -m pip install --upgrade pip

REM Installer toutes les dépendances (10-15 minutes)
pip install -r requirements.txt
```

**⏳ Cette étape prend du temps. Soyez patient!**

---

## 🗄️ ÉTAPE 6: CONFIGURATION DE LA BASE DE DONNÉES

```cmd
REM Créer le fichier .env
echo DEBUG=True > .env
echo SECRET_KEY=django-insecure-ma-cle-secrete >> .env

REM Créer les migrations
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py makemigrations

REM Appliquer les migrations
python manage.py migrate
```

**✅ Résultat attendu:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying accounts.0001_initial... OK
  Applying core.0001_initial... OK
  ...
```

---

## 👤 ÉTAPE 7: CRÉER UN COMPTE ADMINISTRATEUR

```cmd
python manage.py createsuperuser
```

**Suivez les instructions:**
```
Username: admin
Email address: admin@agrismart.cm
Password: ********
Password (again): ********
Superuser created successfully.
```

**💡 CONSEIL:** Notez ces identifiants quelque part!

---

## 🤖 ÉTAPE 8: ENTRAÎNER LES MODÈLES ML

```cmd
python train_models.py
```

**✅ Résultat attendu:**
```
============================================================
🤖 ENTRAÎNEMENT DES MODÈLES ML - AGRI SMART
============================================================

📊 Entraînement du modèle de recommandation de cultures...
✅ Modèle de recommandation créé et entraîné

📈 Entraînement du modèle de prédiction de rendement...
✅ Modèle de prédiction créé et entraîné

🐛 Entraînement du modèle de risque de maladies...
✅ Modèle de risque de maladies créé

============================================================
✅ ENTRAÎNEMENT TERMINÉ
============================================================
```

---

## 📊 ÉTAPE 9: CHARGER LES DONNÉES

```cmd
python load_data.py
```

**✅ Résultat attendu:**
```
============================================================
📊 CHARGEMENT DES DONNÉES - AGRI SMART
============================================================

📊 Chargement des cultures...
  ✓ Maïs créé
  ✓ Riz créé
  ✓ Tomate créé
  ...

✅ 8 nouvelles cultures créées
📊 Total cultures: 8

👤 Création utilisateur de démonstration...
  ✓ Utilisateur 'demo' créé
     Username: demo
     Password: demo123

============================================================
✅ CHARGEMENT TERMINÉ
============================================================
```

---

## 🎨 ÉTAPE 10: COLLECTER LES FICHIERS STATIQUES

```cmd
python manage.py collectstatic --noinput
```

---

## 🚀 ÉTAPE 11: DÉMARRER L'APPLICATION

```cmd
python manage.py runserver
```

**✅ Résultat attendu:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
February 05, 2024 - 12:00:00
Django version 5.0, using settings 'agri_smart_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 🌐 ÉTAPE 12: OUVRIR L'APPLICATION

1. **Ouvrez** votre navigateur (Chrome, Firefox, Edge)
2. **Tapez** dans la barre d'adresse:
   ```
   http://127.0.0.1:8000/
   ```
3. **Appuyez** sur Entrée

**🎉 Vous devriez voir la page d'accueil d'Agri Smart!**

---

## 🧪 ÉTAPE 13: TESTER LES FONCTIONNALITÉS

### Test 1: Connexion avec le compte démo

1. Cliquez sur **"Connexion"** dans le menu
2. Entrez:
   - Username: `demo`
   - Password: `demo123`
3. Cliquez sur **"Se connecter"**

**✅ Vous devriez être redirigé vers le tableau de bord**

### Test 2: Créer un nouveau compte

1. Cliquez sur **"Inscription"** dans le menu
2. Remplissez le formulaire
3. Cliquez sur **"S'inscrire"**

**✅ Votre compte est créé et vous êtes connecté automatiquement**

### Test 3: Recommandations de cultures

1. Allez sur **"Recommandations"** dans le menu
2. Entrez les données:
   - Température: `28`
   - Humidité: `75`
   - Précipitations: `1200`
   - pH: `6.5`
3. Cliquez sur **"Obtenir Recommandations"**

**✅ Vous devriez voir une liste de cultures recommandées**

### Test 4: Prédiction de rendement

1. Allez sur **"Prévisions"**
2. Sélectionnez une culture
3. Entrez les paramètres
4. Cliquez sur **"Prédire"**

**✅ Vous devriez voir le rendement estimé**

### Test 5: Chatbot

1. Cliquez sur l'**icône de chat** en bas à droite
2. Tapez: `Comment cultiver le maïs?`
3. Appuyez sur Entrée

**✅ Le chatbot devrait répondre avec des informations**

---

## 📍 EMPLACEMENTS IMPORTANTS

### Fichiers de configuration:

**1. Base de données:**
```
C:\Users\HP\Desktop\MES_PROJETS\agri_smart\db.sqlite3
```

**2. Configuration:**
```
C:\Users\HP\Desktop\MES_PROJETS\agri_smart\.env
```

**3. Modèles ML entraînés:**
```
C:\Users\HP\Desktop\MES_PROJETS\agri_smart\ml_models\trained_models\
```

**4. Templates modifiés:**
```
C:\Users\HP\Desktop\MES_PROJETS\agri_smart\templates\
    └── accounts\
        ├── login.html
        └── register.html
```

**5. Code d'authentification:**
```
C:\Users\HP\Desktop\MES_PROJETS\agri_smart\accounts\
    ├── views.py     ← Logique de connexion
    └── urls.py      ← Routes de connexion
```

---

## 🔧 COMMANDES UTILES

### Démarrer l'application (après la première fois):

```cmd
cd C:\Users\HP\Desktop\MES_PROJETS\agri_smart
venv\Scripts\activate
python manage.py runserver
```

### Arrêter le serveur:
```
Appuyez sur CTRL+C dans le terminal
```

### Créer un nouvel utilisateur admin:
```cmd
python manage.py createsuperuser
```

### Accéder à l'interface d'administration:
```
http://127.0.0.1:8000/admin/
```

---

## ❗ RÉSOLUTION DE PROBLÈMES

### Problème: "ModuleNotFoundError: No module named 'accounts'"

**Solution:**
```cmd
# Vérifier que le dossier existe
dir accounts

# Si le dossier manque, ré-extraire le ZIP
```

### Problème: "TemplateDoesNotExist at /accounts/login/"

**Solution:**
```cmd
# Vérifier que les templates existent
dir templates\accounts

# Devrait afficher: login.html et register.html
```

### Problème: Page 404 sur /accounts/login/

**Solution:**
```cmd
# Redémarrer le serveur
# CTRL+C puis
python manage.py runserver
```

### Problème: "Port 8000 is already in use"

**Solution:**
```cmd
# Utiliser un autre port
python manage.py runserver 8001

# Puis accéder à http://127.0.0.1:8001/
```

---

## ✅ CHECKLIST FINALE

Avant de considérer l'installation réussie:

- [ ] Environnement virtuel activé (voir `(venv)` dans le terminal)
- [ ] Dossier `accounts\` existe avec 6 fichiers
- [ ] Dossier `templates\accounts\` existe avec 2 fichiers
- [ ] `pip install -r requirements.txt` terminé sans erreur
- [ ] `python manage.py migrate` terminé sans erreur
- [ ] Superutilisateur créé
- [ ] `python train_models.py` terminé avec succès
- [ ] `python load_data.py` terminé avec succès
- [ ] Serveur démarre avec `python manage.py runserver`
- [ ] Page d'accueil accessible: http://127.0.0.1:8000/
- [ ] Page login accessible: http://127.0.0.1:8000/accounts/login/
- [ ] Page register accessible: http://127.0.0.1:8000/accounts/register/
- [ ] Connexion avec `demo`/`demo123` fonctionne
- [ ] Recommandations de cultures fonctionnent
- [ ] Pas d'erreur 404 dans le navigateur

---

## 🎓 COMPTES DISPONIBLES

**Compte Démo:**
- Username: `demo`
- Password: `demo123`
- Accès: Utilisateur standard

**Compte Admin:**
- Username: celui que vous avez créé à l'étape 7
- Password: celui que vous avez défini
- Accès: Administration complète

---

## 🎉 FÉLICITATIONS!

Si toutes les cases de la checklist sont cochées, votre application **Agri Smart** est **100% opérationnelle**!

**Prochaines étapes:**
1. Explorer toutes les fonctionnalités
2. Scraper plus de données (optionnel)
3. Personnaliser l'apparence
4. Ajouter vos propres cultures
5. Déployer en production

---

**📧 Besoin d'aide? Consultez INSTALLATION_AVEC_CHEMINS.md pour plus de détails.**

**🌱 Bon développement avec Agri Smart! 🚀**

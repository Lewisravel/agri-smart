# 📁 EMPLACEMENT DES FICHIERS - GUIDE VISUEL

## 🗂️ STRUCTURE COMPLÈTE DU PROJET

```
C:\Users\HP\Desktop\MES_PROJETS\Final\agri_smart_complete\agri_smart\
│
├── 📄 manage.py                      ← Existant (Django)
├── 📄 requirements.txt               ← Existant (développement)
├── 📄 requirements_prod.txt          ← ✨ NOUVEAU (téléchargé)
├── 📄 runtime.txt                    ← ✨ NOUVEAU (téléchargé)
├── 📄 Procfile                       ← ✨ NOUVEAU (téléchargé)
├── 📄 build.sh                       ← ✨ NOUVEAU (téléchargé)
├── 📄 .env                           ← Existant
├── 📄 .env.example                   ← ✨ NOUVEAU (téléchargé)
├── 📄 .gitignore                     ← Existant (à vérifier)
├── 📄 DEPLOY_GUIDE.md                ← ✨ NOUVEAU (téléchargé)
├── 📄 DEPLOYMENT_CHECKLIST.md        ← ✨ NOUVEAU (téléchargé)
├── 📄 EMPLACEMENT_FICHIERS.md        ← ✨ NOUVEAU (ce fichier)
├── 📄 settings_production_addon.py   ← ✨ NOUVEAU (téléchargé - à copier dans settings.py)
│
├── 📁 agri_smart_project\
│   ├── settings.py                   ← À MODIFIER (ajouter code production)
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── 📁 accounts\
├── 📁 api\
├── 📁 chatbot\
├── 📁 core\
├── 📁 data\
├── 📁 data_scraper\
├── 📁 logs\
├── 📁 media\
├── 📁 ml_models\
├── 📁 static\
├── 📁 staticfiles\              ← Sera créé automatiquement
└── 📁 templates\
```

---

## 📥 FICHIERS TÉLÉCHARGÉS - OÙ LES METTRE?

### ✅ Fichiers à la RACINE du projet

Tous ces fichiers doivent être placés **DIRECTEMENT** dans:
```
C:\Users\HP\Desktop\MES_PROJETS\Final\agri_smart_complete\agri_smart\
```

**Liste:**
1. `requirements_prod.txt` → À la racine
2. `runtime.txt` → À la racine
3. `Procfile` → À la racine
4. `build.sh` → À la racine
5. `.env.example` → À la racine
6. `DEPLOY_GUIDE.md` → À la racine
7. `DEPLOYMENT_CHECKLIST.md` → À la racine
8. `EMPLACEMENT_FICHIERS.md` → À la racine (ce fichier)

### ⚠️ Fichier spécial: settings_production_addon.py

Ce fichier contient le code à **AJOUTER** dans `settings.py`:

**Emplacement:**
```
C:\Users\HP\Desktop\MES_PROJETS\Final\agri_smart_complete\agri_smart\settings_production_addon.py
```

**Action à faire:**
1. Ouvrir `agri_smart_project\settings.py`
2. Aller **À LA FIN** du fichier
3. Copier tout le contenu de `settings_production_addon.py`
4. Coller à la fin de `settings.py`
5. Sauvegarder

---

## 🎯 VÉRIFICATION RAPIDE

### Dans l'Explorateur Windows:

1. Ouvrez:
```
C:\Users\HP\Desktop\MES_PROJETS\Final\agri_smart_complete\agri_smart\
```

2. Vous devriez voir **À LA RACINE**:
```
📄 requirements_prod.txt
📄 runtime.txt
📄 Procfile
📄 build.sh
📄 .env.example
📄 DEPLOY_GUIDE.md
📄 DEPLOYMENT_CHECKLIST.md
📄 settings_production_addon.py
```

### Dans la console CMD:

```cmd
cd C:\Users\HP\Desktop\MES_PROJETS\Final\agri_smart_complete\agri_smart

dir requirements_prod.txt
dir runtime.txt
dir Procfile
dir build.sh
```

Chaque commande devrait afficher le fichier.

---

## 🔧 MODIFICATIONS À FAIRE

### 1️⃣ Modifier `agri_smart_project\settings.py`

**Emplacement:**
```
C:\Users\HP\Desktop\MES_PROJETS\Final\agri_smart_complete\agri_smart\agri_smart_project\settings.py
```

**Action 1:** Ajouter WhiteNoise au MIDDLEWARE

Trouvez cette section:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # AJOUTER ICI ↓
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... reste du middleware
]
```

**Action 2:** Ajouter le code de production

Allez **à la fin** du fichier `settings.py` et collez tout le contenu de `settings_production_addon.py`.

### 2️⃣ Rendre build.sh exécutable (pour Git)

Plus tard, quand vous ferez:
```cmd
git add .
git commit -m "Initial commit"
```

Ajoutez cette commande:
```cmd
git update-index --chmod=+x build.sh
```

---

## 📋 CHECKLIST D'INSTALLATION

Cochez au fur et à mesure:

- [ ] Tous les fichiers téléchargés
- [ ] Fichiers placés à la racine du projet
- [ ] `settings.py` modifié (WhiteNoise ajouté)
- [ ] `settings.py` modifié (code production ajouté)
- [ ] Vérification avec `dir` (tous les fichiers présents)
- [ ] Prêt pour Git et déploiement

---

## 🚫 ERREURS COURANTES

### ❌ Erreur: "Fichier introuvable"

**Cause:** Fichier pas à la bonne place

**Solution:** Vérifiez que le fichier est **à la racine**, pas dans un sous-dossier

### ❌ Erreur: "build.sh: command not found"

**Cause:** Fichier pas exécutable

**Solution:**
```cmd
git update-index --chmod=+x build.sh
```

### ❌ Erreur: "No module named 'whitenoise'"

**Cause:** WhiteNoise pas installé

**Solution:**
```cmd
pip install whitenoise
```

---

## 📞 AIDE VISUELLE

### Avant (structure actuelle):
```
agri_smart\
├── manage.py
├── requirements.txt
└── agri_smart_project\
    └── settings.py
```

### Après (avec fichiers de déploiement):
```
agri_smart\
├── manage.py
├── requirements.txt
├── requirements_prod.txt    ← NOUVEAU
├── runtime.txt              ← NOUVEAU
├── Procfile                 ← NOUVEAU
├── build.sh                 ← NOUVEAU
├── .env.example             ← NOUVEAU
├── DEPLOY_GUIDE.md          ← NOUVEAU
└── agri_smart_project\
    └── settings.py          ← MODIFIÉ
```

---

## ✅ PRÊT POUR LE DÉPLOIEMENT

Si tous les fichiers sont au bon endroit et `settings.py` est modifié:

**🎉 Vous êtes prêt pour le déploiement!**

Suivez maintenant: `DEPLOY_GUIDE.md`

---

**Besoin d'aide? Référez-vous à DEPLOY_GUIDE.md** 📖

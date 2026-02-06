# ✅ CHECKLIST DE DÉPLOIEMENT - AGRI SMART

## 📦 FICHIERS À LA RACINE

Vérifiez que ces fichiers sont présents à la racine du projet:

- [ ] `requirements_prod.txt` - Dépendances pour production
- [ ] `runtime.txt` - Version Python (3.11.7)
- [ ] `Procfile` - Commande de démarrage Gunicorn
- [ ] `build.sh` - Script de build automatique
- [ ] `.env.example` - Template variables d'environnement
- [ ] `.gitignore` - Fichiers à ignorer par Git

---

## 🔧 MODIFICATIONS DU CODE

### settings.py

- [ ] Code production ajouté à la fin (voir `settings_production_addon.py`)
- [ ] WhiteNoise ajouté au MIDDLEWARE (après SecurityMiddleware)
- [ ] STATIC_ROOT défini
- [ ] ALLOWED_HOSTS configuré pour production

### Vérification

```python
# Dans settings.py, vérifier:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Présent?
    # ...
]
```

---

## 🌐 GIT ET GITHUB

- [ ] Git initialisé (`git init`)
- [ ] Compte GitHub créé
- [ ] Repository créé sur GitHub
- [ ] Code ajouté (`git add .`)
- [ ] Commit effectué (`git commit -m "Initial commit"`)
- [ ] Remote ajouté (`git remote add origin ...`)
- [ ] Code poussé (`git push -u origin main`)

---

## 🎯 RENDER.COM

### Compte et Service

- [ ] Compte Render créé (avec GitHub)
- [ ] Web Service créé
- [ ] Repository connecté
- [ ] Branche `main` sélectionnée

### Configuration

- [ ] **Name:** Défini (ex: agri-smart)
- [ ] **Region:** Frankfurt (EU Central)
- [ ] **Runtime:** Python 3
- [ ] **Build Command:** `chmod +x build.sh && ./build.sh`
- [ ] **Start Command:** `gunicorn agri_smart_project.wsgi:application`
- [ ] **Instance Type:** Free

### Variables d'environnement

- [ ] `RENDER=True`
- [ ] `SECRET_KEY=...` (généré avec django)
- [ ] `PYTHON_VERSION=3.11.7`
- [ ] `DEBUG=False`

### Commande pour générer SECRET_KEY:
```cmd
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🚀 DÉPLOIEMENT

- [ ] "Create Web Service" cliqué
- [ ] Build en cours (5-10 minutes)
- [ ] Build réussi ✅
- [ ] Application accessible en ligne

### URL de l'application:
```
https://votre-app-name.onrender.com
```

---

## 👤 CONFIGURATION POST-DÉPLOIEMENT

### Créer Superuser

Dans Render Shell:
- [ ] Accédé au Shell Render
- [ ] Commande exécutée: `python manage.py createsuperuser`
- [ ] Username créé: `admin`
- [ ] Email défini
- [ ] Password défini

### Vérifier données

- [ ] Données de base chargées (`load_data.py` exécuté)
- [ ] 8 cultures présentes
- [ ] Compte demo créé (demo/demo123)

---

## 🧪 TESTS EN PRODUCTION

### Pages publiques (sans login)

- [ ] Page d'accueil: `https://votre-app.onrender.com/`
- [ ] Connexion: `https://votre-app.onrender.com/accounts/login/`
- [ ] Inscription: `https://votre-app.onrender.com/accounts/register/`
- [ ] Recommandations: `https://votre-app.onrender.com/recommend/`
- [ ] Prévisions: `https://votre-app.onrender.com/yield-prediction/`
- [ ] Prix: `https://votre-app.onrender.com/market-prices/`
- [ ] Chatbot: `https://votre-app.onrender.com/chatbot/`
- [ ] À propos: `https://votre-app.onrender.com/about/`

### Pages protégées (avec login)

- [ ] Connexion avec demo/demo123 fonctionne
- [ ] Dashboard accessible: `https://votre-app.onrender.com/dashboard/`
- [ ] Admin accessible: `https://votre-app.onrender.com/admin/`

### Fonctionnalités

- [ ] Recommandations de cultures fonctionnent
- [ ] Prédictions de rendement fonctionnent
- [ ] Chatbot répond correctement
- [ ] Prix de marché s'affichent
- [ ] Graphiques s'affichent
- [ ] Mode sombre fonctionne
- [ ] Connexion/Déconnexion fonctionne

---

## 🎨 FICHIERS STATIQUES

- [ ] CSS chargés correctement
- [ ] JavaScript fonctionne
- [ ] Images s'affichent
- [ ] Icônes Font Awesome visibles
- [ ] Bootstrap appliqué

---

## 🔒 SÉCURITÉ

- [ ] DEBUG=False en production
- [ ] SECRET_KEY unique et sécurisée (pas celle par défaut)
- [ ] HTTPS activé (automatique sur Render)
- [ ] CSRF tokens configurés
- [ ] ALLOWED_HOSTS correctement défini

---

## 📊 MONITORING

- [ ] Logs Render consultés (pas d'erreurs)
- [ ] Utilisation des ressources vérifiée
- [ ] Temps de chargement acceptable (<3s)

---

## 🔄 MISES À JOUR FUTURES

### Workflow de mise à jour établi:

```cmd
# 1. Modifier le code localement
# 2. Tester localement
python manage.py runserver

# 3. Commiter et pousser
git add .
git commit -m "Description des modifications"
git push origin main

# 4. Render redéploie automatiquement
# 5. Vérifier en production
```

- [ ] Workflow compris et documenté

---

## 📝 DOCUMENTATION

- [ ] URL de production notée
- [ ] Identifiants admin notés (en sécurité)
- [ ] Variables d'environnement documentées
- [ ] Guide utilisateur créé (optionnel)

---

## 🎉 DÉPLOIEMENT RÉUSSI

Si toutes les cases sont cochées:

### ✅ FÉLICITATIONS!

Votre application **Agri Smart** est:
- ✅ En ligne
- ✅ Accessible mondialement
- ✅ Sécurisée
- ✅ Prête pour les utilisateurs

**URL finale:** `https://votre-app.onrender.com`

---

## 📞 EN CAS DE PROBLÈME

### Ressources:

1. **Logs Render:** Dashboard → Logs
2. **Documentation Render:** https://render.com/docs
3. **Guide de déploiement:** `DEPLOY_GUIDE.md`
4. **Community:** https://community.render.com

### Problèmes courants:

| Problème | Solution |
|----------|----------|
| Build échoue | Vérifier requirements_prod.txt |
| Static files manquants | Vérifier WhiteNoise configuration |
| 502 Error | Vérifier Gunicorn dans requirements |
| DB vide | Exécuter load_data.py dans Shell |

---

**Date de déploiement:** __________

**Déployé par:** __________

**Version:** 1.0.0

---

**Bon déploiement! 🚀**

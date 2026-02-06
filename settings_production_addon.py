# ========================================
# CONFIGURATION PRODUCTION
# À AJOUTER À LA FIN DE agri_smart_project/settings.py
# ========================================

import os
import dj_database_url

# Détection environnement production
IS_PRODUCTION = os.environ.get('RENDER') or os.environ.get('RAILWAY_ENVIRONMENT')

if IS_PRODUCTION:
    print("🚀 Mode PRODUCTION activé")
    
    # Debug
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    
    # Hosts autorisés
    ALLOWED_HOSTS = [
        '.onrender.com',
        '.railway.app',
        'localhost',
        '127.0.0.1',
    ]
    
    # Ajouter votre domaine personnalisé si vous en avez un
    custom_domain = os.environ.get('CUSTOM_DOMAIN')
    if custom_domain:
        ALLOWED_HOSTS.append(custom_domain)
    
    # Base de données PostgreSQL
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        DATABASES = {
            'default': dj_database_url.config(
                default=database_url,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    else:
        # Fallback sur SQLite si pas de DB externe
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    
    # Sécurité
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Static files avec WhiteNoise
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    
    # CORS
    CORS_ALLOWED_ORIGINS = [
        f"https://{host}" for host in ALLOWED_HOSTS if host not in ['localhost', '127.0.0.1']
    ]
    
    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
    
else:
    print("💻 Mode DÉVELOPPEMENT activé")
    DEBUG = True
    ALLOWED_HOSTS = ['*']

# Toujours autoriser le domaine de render/railway dans CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'https://*.railway.app',
]

# Ajouter domaine personnalisé si présent
custom_domain = os.environ.get('CUSTOM_DOMAIN')
if custom_domain:
    CSRF_TRUSTED_ORIGINS.append(f'https://{custom_domain}')

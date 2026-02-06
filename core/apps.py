"""
Core App Configuration
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = _('Core - Gestion agricole')
    
    def ready(self):
        """Initialisation de l'application"""
        import core.signals  # noqa

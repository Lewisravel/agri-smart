"""
Core Signals - Django signals for automated tasks
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserPreference, CropSeason
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_preference(sender, instance, created, **kwargs):
    """
    Créer automatiquement les préférences utilisateur
    quand un nouvel utilisateur est créé
    """
    if created:
        UserPreference.objects.create(user=instance)
        logger.info(f"Préférences créées pour l'utilisateur: {instance.username}")


@receiver(post_save, sender=CropSeason)
def calculate_season_metrics(sender, instance, created, **kwargs):
    """
    Calculer automatiquement les métriques après sauvegarde
    """
    if instance.yield_kg_per_ha and instance.area_planted:
        if not instance.total_production_kg:
            instance.total_production_kg = instance.yield_kg_per_ha * instance.area_planted
            instance.save(update_fields=['total_production_kg'])
    
    if instance.total_revenue and instance.production_cost:
        if not instance.profit_margin:
            revenue = float(instance.total_revenue)
            cost = float(instance.production_cost)
            if revenue > 0:
                instance.profit_margin = ((revenue - cost) / revenue * 100)
                instance.save(update_fields=['profit_margin'])

"""
Core Models - Agricultural Data Models
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import json


class Farm(models.Model):
    """Modèle de ferme"""
    SOIL_TYPES = [
        ('SANDY', _('Sableux')),
        ('CLAY', _('Argileux')),
        ('LOAM', _('Limoneux')),
        ('SILT_LOAM', _('Argilo-limoneux')),
        ('SANDY_LOAM', _('Sablo-limoneux')),
    ]
    
    REGIONS = [
        ('NORTH', _('Nord')),
        ('FAR_NORTH', _('Extrême-Nord')),
        ('ADAMAWA', _('Adamaoua')),
        ('CENTER', _('Centre')),
        ('SOUTH', _('Sud')),
        ('EAST', _('Est')),
        ('WEST', _('Ouest')),
        ('LITTORAL', _('Littoral')),
        ('NORTHWEST', _('Nord-Ouest')),
        ('SOUTHWEST', _('Sud-Ouest')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(_('Nom'), max_length=200)
    region = models.CharField(_('Région'), max_length=50, choices=REGIONS)
    latitude = models.FloatField(_('Latitude'))
    longitude = models.FloatField(_('Longitude'))
    area_hectares = models.FloatField(_('Superficie (hectares)'))
    soil_type = models.CharField(_('Type de sol'), max_length=50, choices=SOIL_TYPES)
    soil_ph = models.FloatField(_('pH du sol'), null=True, blank=True)
    organic_matter = models.FloatField(_('Matière organique %'), null=True, blank=True)
    irrigation_available = models.BooleanField(_('Irrigation disponible'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Ferme')
        verbose_name_plural = _('Fermes')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_region_display()}"


class Crop(models.Model):
    """Modèle de culture"""
    name_fr = models.CharField(_('Nom (Français)'), max_length=100)
    name_en = models.CharField(_('Nom (English)'), max_length=100)
    scientific_name = models.CharField(_('Nom scientifique'), max_length=150, blank=True)
    category = models.CharField(_('Catégorie'), max_length=50)
    growing_season_days = models.IntegerField(_('Durée de croissance (jours)'))
    water_requirement = models.CharField(_('Besoin en eau'), max_length=50)
    temperature_min = models.FloatField(_('Température min (°C)'))
    temperature_max = models.FloatField(_('Température max (°C)'))
    optimal_ph_min = models.FloatField(_('pH optimal min'))
    optimal_ph_max = models.FloatField(_('pH optimal max'))
    description_fr = models.TextField(_('Description (Français)'), blank=True)
    description_en = models.TextField(_('Description (English)'), blank=True)
    
    class Meta:
        verbose_name = _('Culture')
        verbose_name_plural = _('Cultures')
        ordering = ['name_fr']
    
    def __str__(self):
        return self.name_fr


class CropSeason(models.Model):
    """Saison de culture pour une ferme"""
    SEASONS = [
        ('DRY', _('Saison sèche')),
        ('RAINY', _('Saison des pluies')),
        ('TRANSITION', _('Transition')),
    ]
    
    YIELD_QUALITY = [
        ('EXCELLENT', _('Excellente')),
        ('GOOD', _('Bonne')),
        ('AVERAGE', _('Moyenne')),
        ('POOR', _('Faible')),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='seasons')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='seasons')
    season_type = models.CharField(_('Type de saison'), max_length=20, choices=SEASONS)
    planting_date = models.DateField(_('Date de plantation'))
    expected_harvest_date = models.DateField(_('Date de récolte prévue'))
    actual_harvest_date = models.DateField(_('Date de récolte réelle'), null=True, blank=True)
    area_planted = models.FloatField(_('Superficie plantée (ha)'))
    
    # Données agronomiques
    fertilizer_used = models.BooleanField(_('Engrais utilisé'), default=False)
    npk_amount = models.FloatField(_('Quantité NPK (kg/ha)'), null=True, blank=True)
    pesticide_applications = models.IntegerField(_('Applications pesticides'), default=0)
    irrigation_type = models.CharField(_('Type d\'irrigation'), max_length=50, blank=True)
    
    # Résultats
    yield_kg_per_ha = models.FloatField(_('Rendement (kg/ha)'), null=True, blank=True)
    yield_quality = models.CharField(_('Qualité'), max_length=20, choices=YIELD_QUALITY, blank=True)
    total_production_kg = models.FloatField(_('Production totale (kg)'), null=True, blank=True)
    
    # Économie
    production_cost = models.DecimalField(_('Coût de production'), max_digits=12, decimal_places=2, null=True, blank=True)
    market_price_per_kg = models.DecimalField(_('Prix de marché (FCFA/kg)'), max_digits=10, decimal_places=2, null=True, blank=True)
    total_revenue = models.DecimalField(_('Revenu total'), max_digits=12, decimal_places=2, null=True, blank=True)
    profit_margin = models.FloatField(_('Marge bénéficiaire %'), null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Saison de culture')
        verbose_name_plural = _('Saisons de culture')
        ordering = ['-planting_date']
    
    def __str__(self):
        return f"{self.crop.name_fr} - {self.farm.name} ({self.planting_date})"
    
    def save(self, *args, **kwargs):
        # Calculer production totale
        if self.yield_kg_per_ha and self.area_planted:
            self.total_production_kg = self.yield_kg_per_ha * self.area_planted
        
        # Calculer revenu total
        if self.total_production_kg and self.market_price_per_kg:
            self.total_revenue = float(self.total_production_kg) * float(self.market_price_per_kg)
        
        # Calculer marge
        if self.total_revenue and self.production_cost:
            self.profit_margin = ((float(self.total_revenue) - float(self.production_cost)) / float(self.total_revenue) * 100)
        
        super().save(*args, **kwargs)


class WeatherData(models.Model):
    """Données météorologiques"""
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='weather_data')
    date = models.DateField(_('Date'))
    temperature_max = models.FloatField(_('Température max (°C)'))
    temperature_min = models.FloatField(_('Température min (°C)'))
    temperature_avg = models.FloatField(_('Température moy (°C)'))
    rainfall_mm = models.FloatField(_('Précipitations (mm)'))
    humidity_percent = models.FloatField(_('Humidité (%)'))
    wind_speed_kmh = models.FloatField(_('Vitesse du vent (km/h)'), null=True, blank=True)
    solar_radiation = models.FloatField(_('Radiation solaire (W/m²)'), null=True, blank=True)
    evapotranspiration = models.FloatField(_('Évapotranspiration (mm)'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Données météo')
        verbose_name_plural = _('Données météo')
        ordering = ['-date']
        unique_together = ['farm', 'date']
    
    def __str__(self):
        return f"{self.farm.name} - {self.date}"


class Prediction(models.Model):
    """Prédictions ML pour l'utilisateur"""
    PREDICTION_TYPES = [
        ('CROP_RECOMMENDATION', _('Recommandation de culture')),
        ('YIELD_FORECAST', _('Prévision de rendement')),
        ('DISEASE_RISK', _('Risque de maladie')),
        ('MARKET_PRICE', _('Prix de marché')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    prediction_type = models.CharField(_('Type'), max_length=50, choices=PREDICTION_TYPES)
    input_data = models.JSONField(_('Données d\'entrée'))
    output_data = models.JSONField(_('Résultats'))
    confidence_score = models.FloatField(_('Score de confiance'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Prédiction')
        verbose_name_plural = _('Prédictions')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_prediction_type_display()} - {self.created_at.strftime('%Y-%m-%d')}"


class MarketPrice(models.Model):
    """Prix de marché des cultures"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='market_prices')
    region = models.CharField(_('Région'), max_length=50)
    date = models.DateField(_('Date'))
    price_per_kg = models.DecimalField(_('Prix (FCFA/kg)'), max_digits=10, decimal_places=2)
    supply_level = models.CharField(_('Niveau d\'offre'), max_length=20, blank=True)
    demand_level = models.CharField(_('Niveau de demande'), max_length=20, blank=True)
    
    class Meta:
        verbose_name = _('Prix de marché')
        verbose_name_plural = _('Prix de marché')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.crop.name_fr} - {self.region} ({self.date})"


class UserPreference(models.Model):
    """Préférences utilisateur"""
    THEMES = [
        ('light', _('Clair')),
        ('dark', _('Sombre')),
    ]
    
    LANGUAGES = [
        ('fr', _('Français')),
        ('en', _('English')),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    language = models.CharField(_('Langue'), max_length=5, choices=LANGUAGES, default='fr')
    theme = models.CharField(_('Thème'), max_length=10, choices=THEMES, default='light')
    notification_email = models.BooleanField(_('Notifications email'), default=True)
    notification_sms = models.BooleanField(_('Notifications SMS'), default=False)
    default_farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = _('Préférence utilisateur')
        verbose_name_plural = _('Préférences utilisateur')
    
    def __str__(self):
        return f"Préférences - {self.user.username}"

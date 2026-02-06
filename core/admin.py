"""
Core Admin Configuration
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Farm, Crop, CropSeason, WeatherData, Prediction, MarketPrice, UserPreference


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'region', 'area_hectares', 'soil_type', 'created_at']
    list_filter = ['region', 'soil_type', 'irrigation_available']
    search_fields = ['name', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('Informations générales'), {
            'fields': ('user', 'name', 'region')
        }),
        (_('Localisation'), {
            'fields': ('latitude', 'longitude', 'area_hectares')
        }),
        (_('Caractéristiques du sol'), {
            'fields': ('soil_type', 'soil_ph', 'organic_matter')
        }),
        (_('Infrastructure'), {
            'fields': ('irrigation_available',)
        }),
        (_('Métadonnées'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name_fr', 'name_en', 'category', 'growing_season_days', 'water_requirement']
    list_filter = ['category', 'water_requirement']
    search_fields = ['name_fr', 'name_en', 'scientific_name']
    
    fieldsets = (
        (_('Noms'), {
            'fields': ('name_fr', 'name_en', 'scientific_name', 'category')
        }),
        (_('Exigences de croissance'), {
            'fields': ('growing_season_days', 'water_requirement', 'temperature_min', 'temperature_max')
        }),
        (_('Sol'), {
            'fields': ('optimal_ph_min', 'optimal_ph_max')
        }),
        (_('Descriptions'), {
            'fields': ('description_fr', 'description_en'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CropSeason)
class CropSeasonAdmin(admin.ModelAdmin):
    list_display = ['crop', 'farm', 'planting_date', 'expected_harvest_date', 'yield_kg_per_ha', 'yield_quality']
    list_filter = ['season_type', 'yield_quality', 'fertilizer_used', 'planting_date']
    search_fields = ['farm__name', 'crop__name_fr']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'planting_date'
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('farm', 'crop', 'season_type', 'area_planted')
        }),
        (_('Dates'), {
            'fields': ('planting_date', 'expected_harvest_date', 'actual_harvest_date')
        }),
        (_('Pratiques agronomiques'), {
            'fields': ('fertilizer_used', 'npk_amount', 'pesticide_applications', 'irrigation_type')
        }),
        (_('Résultats'), {
            'fields': ('yield_kg_per_ha', 'yield_quality', 'total_production_kg')
        }),
        (_('Économie'), {
            'fields': ('production_cost', 'market_price_per_kg', 'total_revenue', 'profit_margin')
        }),
        (_('Métadonnées'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['farm', 'date', 'temperature_avg', 'rainfall_mm', 'humidity_percent']
    list_filter = ['date', 'farm']
    search_fields = ['farm__name']
    date_hierarchy = 'date'


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'prediction_type', 'confidence_score', 'created_at']
    list_filter = ['prediction_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'input_data', 'output_data']
    date_hierarchy = 'created_at'


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['crop', 'region', 'date', 'price_per_kg', 'supply_level', 'demand_level']
    list_filter = ['region', 'date', 'crop']
    search_fields = ['crop__name_fr', 'region']
    date_hierarchy = 'date'


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'language', 'theme', 'notification_email', 'notification_sms']
    list_filter = ['language', 'theme', 'notification_email']
    search_fields = ['user__username']

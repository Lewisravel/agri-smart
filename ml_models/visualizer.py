"""
Data Visualizer - Create interactive charts and visualizations
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from django.db.models import Avg, Sum, Count
import json


class DataVisualizer:
    """
    Créateur de visualisations interactives
    """
    
    def __init__(self):
        self.color_palette = [
            '#28a745', '#20c997', '#17a2b8', '#ffc107', 
            '#dc3545', '#6610f2', '#e83e8c', '#fd7e14'
        ]
    
    def create_yield_trend_chart(self, crop_seasons) -> str:
        """
        Graphique de tendance des rendements
        
        Args:
            crop_seasons: QuerySet de CropSeason
        
        Returns:
            JSON string pour Plotly
        """
        if not crop_seasons:
            return json.dumps({})
        
        # Préparer les données
        df = pd.DataFrame(list(crop_seasons.values(
            'planting_date', 'crop__name_fr', 'yield_kg_per_ha'
        )))
        
        if df.empty:
            return json.dumps({})
        
        df['planting_date'] = pd.to_datetime(df['planting_date'])
        df = df.sort_values('planting_date')
        
        # Créer le graphique
        fig = go.Figure()
        
        for crop in df['crop__name_fr'].unique():
            crop_data = df[df['crop__name_fr'] == crop]
            
            fig.add_trace(go.Scatter(
                x=crop_data['planting_date'],
                y=crop_data['yield_kg_per_ha'],
                mode='lines+markers',
                name=crop,
                line=dict(width=2),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title='Évolution des rendements par culture',
            xaxis_title='Date de plantation',
            yaxis_title='Rendement (kg/ha)',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig.to_json()
    
    def create_crop_distribution_chart(self, crop_seasons) -> str:
        """
        Graphique de distribution des cultures
        
        Args:
            crop_seasons: QuerySet de CropSeason
        
        Returns:
            JSON string pour Plotly
        """
        if not crop_seasons:
            return json.dumps({})
        
        # Agréger par culture
        crop_counts = crop_seasons.values('crop__name_fr').annotate(
            count=Count('id'),
            total_area=Sum('area_planted')
        )
        
        df = pd.DataFrame(list(crop_counts))
        
        if df.empty:
            return json.dumps({})
        
        # Graphique en camembert
        fig = go.Figure(data=[go.Pie(
            labels=df['crop__name_fr'],
            values=df['total_area'],
            hole=0.4,
            marker=dict(colors=self.color_palette)
        )])
        
        fig.update_layout(
            title='Distribution des cultures par superficie',
            template='plotly_white',
            height=400
        )
        
        return fig.to_json()
    
    def create_revenue_chart(self, crop_seasons) -> str:
        """
        Graphique d'analyse de revenus
        
        Args:
            crop_seasons: QuerySet de CropSeason
        
        Returns:
            JSON string pour Plotly
        """
        if not crop_seasons:
            return json.dumps({})
        
        # Filtrer les saisons avec revenus
        df = pd.DataFrame(list(crop_seasons.filter(
            total_revenue__isnull=False,
            production_cost__isnull=False
        ).values(
            'crop__name_fr', 'total_revenue', 'production_cost', 'profit_margin'
        )))
        
        if df.empty:
            return json.dumps({})
        
        # Convertir en numeric
        df['total_revenue'] = pd.to_numeric(df['total_revenue'])
        df['production_cost'] = pd.to_numeric(df['production_cost'])
        
        # Agréger par culture
        crop_revenue = df.groupby('crop__name_fr').agg({
            'total_revenue': 'mean',
            'production_cost': 'mean',
            'profit_margin': 'mean'
        }).reset_index()
        
        # Créer le graphique à barres groupées
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Revenu',
            x=crop_revenue['crop__name_fr'],
            y=crop_revenue['total_revenue'],
            marker_color='#28a745'
        ))
        
        fig.add_trace(go.Bar(
            name='Coût',
            x=crop_revenue['crop__name_fr'],
            y=crop_revenue['production_cost'],
            marker_color='#dc3545'
        ))
        
        fig.update_layout(
            title='Analyse Revenu vs Coût par culture',
            xaxis_title='Culture',
            yaxis_title='Montant (FCFA)',
            barmode='group',
            template='plotly_white',
            height=400
        )
        
        return fig.to_json()
    
    def create_weather_chart(self, weather_data) -> str:
        """
        Graphique des données météo
        
        Args:
            weather_data: QuerySet de WeatherData
        
        Returns:
            JSON string pour Plotly
        """
        if not weather_data:
            return json.dumps({})
        
        df = pd.DataFrame(list(weather_data.values(
            'date', 'temperature_max', 'temperature_min', 
            'rainfall_mm', 'humidity_percent'
        )))
        
        if df.empty:
            return json.dumps({})
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Créer un graphique à sous-plots
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Température', 'Précipitations et Humidité'),
            vertical_spacing=0.15
        )
        
        # Température
        fig.add_trace(
            go.Scatter(
                x=df['date'], y=df['temperature_max'],
                name='Temp Max', mode='lines',
                line=dict(color='#dc3545', width=2)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['date'], y=df['temperature_min'],
                name='Temp Min', mode='lines',
                line=dict(color='#17a2b8', width=2)
            ),
            row=1, col=1
        )
        
        # Précipitations et humidité
        fig.add_trace(
            go.Bar(
                x=df['date'], y=df['rainfall_mm'],
                name='Pluie (mm)',
                marker_color='#20c997'
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df['date'], y=df['humidity_percent'],
                name='Humidité (%)', mode='lines',
                line=dict(color='#ffc107', width=2),
                yaxis='y2'
            ),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Température (°C)", row=1, col=1)
        fig.update_yaxes(title_text="Pluie (mm)", row=2, col=1)
        
        fig.update_layout(
            height=600,
            template='plotly_white',
            showlegend=True
        )
        
        return fig.to_json()
    
    def create_market_price_chart(self, market_prices) -> str:
        """
        Graphique d'évolution des prix de marché
        
        Args:
            market_prices: QuerySet de MarketPrice
        
        Returns:
            JSON string pour Plotly
        """
        if not market_prices:
            return json.dumps({})
        
        df = pd.DataFrame(list(market_prices.values(
            'date', 'crop__name_fr', 'price_per_kg', 'region'
        )))
        
        if df.empty:
            return json.dumps({})
        
        df['date'] = pd.to_datetime(df['date'])
        df['price_per_kg'] = pd.to_numeric(df['price_per_kg'])
        df = df.sort_values('date')
        
        fig = go.Figure()
        
        for crop in df['crop__name_fr'].unique():
            crop_data = df[df['crop__name_fr'] == crop]
            
            # Moyenne mobile sur 7 jours
            crop_data_sorted = crop_data.sort_values('date')
            crop_data_sorted['price_ma'] = crop_data_sorted['price_per_kg'].rolling(window=7, min_periods=1).mean()
            
            fig.add_trace(go.Scatter(
                x=crop_data_sorted['date'],
                y=crop_data_sorted['price_ma'],
                mode='lines',
                name=crop,
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title='Évolution des prix de marché (moyenne mobile 7 jours)',
            xaxis_title='Date',
            yaxis_title='Prix (FCFA/kg)',
            hovermode='x unified',
            template='plotly_white',
            height=400
        )
        
        return fig.to_json()
    
    def create_performance_heatmap(self, crop_seasons) -> str:
        """
        Heatmap de performance des cultures par région
        
        Args:
            crop_seasons: QuerySet de CropSeason
        
        Returns:
            JSON string pour Plotly
        """
        if not crop_seasons:
            return json.dumps({})
        
        df = pd.DataFrame(list(crop_seasons.values(
            'crop__name_fr', 'farm__region', 'yield_kg_per_ha'
        )))
        
        if df.empty:
            return json.dumps({})
        
        # Créer une table pivot
        pivot = df.pivot_table(
            values='yield_kg_per_ha',
            index='crop__name_fr',
            columns='farm__region',
            aggfunc='mean'
        )
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='Greens',
            text=np.round(pivot.values, 0),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Rendement<br>(kg/ha)")
        ))
        
        fig.update_layout(
            title='Performance des cultures par région',
            xaxis_title='Région',
            yaxis_title='Culture',
            template='plotly_white',
            height=500
        )
        
        return fig.to_json()
    
    def create_profitability_chart(self, crop_seasons) -> str:
        """
        Graphique de rentabilité
        
        Args:
            crop_seasons: QuerySet de CropSeason
        
        Returns:
            JSON string pour Plotly
        """
        if not crop_seasons:
            return json.dumps({})
        
        df = pd.DataFrame(list(crop_seasons.filter(
            profit_margin__isnull=False
        ).values(
            'crop__name_fr', 'profit_margin', 'yield_kg_per_ha'
        )))
        
        if df.empty:
            return json.dumps({})
        
        # Scatter plot
        fig = px.scatter(
            df,
            x='yield_kg_per_ha',
            y='profit_margin',
            color='crop__name_fr',
            size='yield_kg_per_ha',
            hover_name='crop__name_fr',
            labels={
                'yield_kg_per_ha': 'Rendement (kg/ha)',
                'profit_margin': 'Marge bénéficiaire (%)',
                'crop__name_fr': 'Culture'
            },
            title='Rentabilité vs Rendement',
            template='plotly_white',
            height=400
        )
        
        return fig.to_json()
    
    def create_seasonal_analysis(self, crop_seasons) -> str:
        """
        Analyse saisonnière des cultures
        
        Args:
            crop_seasons: QuerySet de CropSeason
        
        Returns:
            JSON string pour Plotly
        """
        if not crop_seasons:
            return json.dumps({})
        
        df = pd.DataFrame(list(crop_seasons.values(
            'planting_date', 'crop__name_fr', 'yield_kg_per_ha'
        )))
        
        if df.empty:
            return json.dumps({})
        
        df['planting_date'] = pd.to_datetime(df['planting_date'])
        df['month'] = df['planting_date'].dt.month
        df['month_name'] = df['planting_date'].dt.strftime('%B')
        
        # Agréger par mois et culture
        monthly = df.groupby(['month', 'month_name', 'crop__name_fr'])['yield_kg_per_ha'].mean().reset_index()
        
        fig = px.line(
            monthly,
            x='month_name',
            y='yield_kg_per_ha',
            color='crop__name_fr',
            markers=True,
            labels={
                'month_name': 'Mois de plantation',
                'yield_kg_per_ha': 'Rendement moyen (kg/ha)',
                'crop__name_fr': 'Culture'
            },
            title='Rendement moyen par mois de plantation',
            template='plotly_white',
            height=400
        )
        
        return fig.to_json()

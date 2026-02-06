# 📡 Agri Smart - Documentation API REST

## Base URL
```
http://localhost:8000/api/
```

## Authentification
La plupart des endpoints publics ne nécessitent pas d'authentification. Les endpoints utilisateur nécessitent un token JWT (optionnel).

---

## 🌱 Endpoints ML & Prédictions

### 1. Recommandation de Cultures

**Endpoint:** `POST /api/recommendations/`

**Description:** Obtient des recommandations de cultures basées sur les conditions du sol et du climat.

**Request Body:**
```json
{
    "temperature": 28.5,
    "humidity": 75.0,
    "rainfall": 1200,
    "soil_ph": 6.5,
    "soil_type": "LOAM",
    "region": "CENTER"
}
```

**Response:**
```json
{
    "success": true,
    "recommendations": [
        {
            "crop": "Maïs",
            "confidence": 85.5,
            "reasons": [
                "Température optimale (28.5°C)",
                "Pluviométrie adéquate (1200mm)",
                "pH du sol adapté (6.5)"
            ],
            "best_practices": {
                "spacing": "75cm entre lignes, 25cm sur ligne",
                "fertilizer": "NPK 15-15-15 à 200-300 kg/ha",
                "irrigation": "Irrigation complémentaire recommandée",
                "pest_control": "Surveiller chenille légionnaire"
            }
        },
        {
            "crop": "Riz",
            "confidence": 72.3,
            "reasons": [...],
            "best_practices": {...}
        }
    ],
    "input": {...}
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:8000/api/recommendations/ \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 28.5,
    "humidity": 75.0,
    "rainfall": 1200,
    "soil_ph": 6.5,
    "soil_type": "LOAM",
    "region": "CENTER"
  }'
```

---

### 2. Prédiction de Rendement

**Endpoint:** `POST /api/yield-prediction/`

**Description:** Prédit le rendement d'une culture avec intervalle de confiance.

**Request Body:**
```json
{
    "crop": "Maïs",
    "area_hectares": 2.5,
    "temperature": 27.0,
    "rainfall": 900,
    "soil_ph": 6.2,
    "fertilizer_npk": 250,
    "irrigation": true
}
```

**Response:**
```json
{
    "success": true,
    "prediction": {
        "yield_per_ha": 3245.67,
        "total_production_kg": 8114.18,
        "confidence_interval": {
            "lower": 2853.67,
            "upper": 3637.67
        },
        "confidence": 0.85,
        "recommendations": [
            {
                "category": "Fertilisation",
                "recommendation": "Apport optimal NPK",
                "impact": "Maintenir le niveau actuel"
            },
            {
                "category": "Irrigation",
                "recommendation": "Système en place efficace",
                "impact": "Continuer l'irrigation"
            }
        ]
    },
    "input": {...}
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:8000/api/yield-prediction/ \
  -H "Content-Type: application/json" \
  -d '{
    "crop": "Maïs",
    "area_hectares": 2.5,
    "temperature": 27.0,
    "rainfall": 900,
    "soil_ph": 6.2,
    "fertilizer_npk": 250,
    "irrigation": true
  }'
```

---

### 3. Prédiction de Risque de Maladie

**Endpoint:** `POST /api/disease-risk/`

**Description:** Évalue le risque de maladies et ravageurs.

**Request Body:**
```json
{
    "crop": "Tomate",
    "temperature": 28.0,
    "humidity": 85.0,
    "rainfall": 150
}
```

**Response:**
```json
{
    "success": true,
    "risk": {
        "risk_level": "Élevé",
        "risk_score": 0.8,
        "main_threats": [
            "Mildiou - risque élevé",
            "Pourriture fongique",
            "Chenille légionnaire"
        ],
        "prevention_measures": [
            "Traitement fongicide préventif",
            "Surveillance quotidienne",
            "Améliorer la circulation d'air",
            "Réduire l'irrigation si possible"
        ]
    },
    "input": {...}
}
```

---

## 💬 Chatbot

### 4. Chat avec l'Assistant IA

**Endpoint:** `POST /api/chatbot/`

**Description:** Conversation avec l'assistant agricole intelligent.

**Request Body:**
```json
{
    "message": "Comment cultiver le maïs au Cameroun?",
    "language": "fr",
    "user_id": "user123"
}
```

**Response:**
```json
{
    "success": true,
    "response": "**Culture du Maïs**\n\nLe maïs est une céréale cultivée pour ses grains riches en amidon...",
    "intent": "cultivation",
    "confidence": 0.92,
    "sources": [
        "Guide de culture - Maïs"
    ]
}
```

**Supported Languages:** `fr`, `en`

**Intents détectés:**
- `cultivation` - Questions sur la culture
- `disease` - Maladies et ravageurs
- `fertilization` - Fertilisation
- `irrigation` - Irrigation
- `market` - Prix de marché
- `soil` - Gestion du sol
- `climate` - Adaptation climatique
- `yield` - Rendement
- `recommendation` - Recommandations générales

---

## 📊 Données Publiques

### 5. Liste des Cultures

**Endpoint:** `GET /api/crops/`

**Description:** Liste toutes les cultures disponibles dans la base de données.

**Response:**
```json
{
    "success": true,
    "count": 16,
    "crops": [
        {
            "id": 1,
            "name_fr": "Maïs",
            "name_en": "Maize",
            "scientific_name": "Zea mays",
            "category": "Céréale",
            "growing_season_days": 120,
            "water_requirement": "Moyen",
            "temperature_min": 20.0,
            "temperature_max": 30.0,
            "optimal_ph_min": 5.5,
            "optimal_ph_max": 7.5
        },
        ...
    ]
}
```

---

### 6. Prix de Marché

**Endpoint:** `GET /api/market-prices/`

**Description:** Récupère les prix de marché des cultures.

**Query Parameters:**
- `crop` (optional) - Nom de la culture
- `region` (optional) - Région

**Example:**
```
GET /api/market-prices/?crop=Maïs&region=CENTER
```

**Response:**
```json
{
    "success": true,
    "count": 30,
    "prices": [
        {
            "date": "2024-02-04",
            "crop": "Maïs",
            "region": "CENTER",
            "price_per_kg": 450,
            "supply_level": "Normal",
            "demand_level": "Élevé"
        },
        ...
    ]
}
```

---

## 👤 Endpoints Utilisateur (Auth Requise)

### 7. Statistiques Utilisateur

**Endpoint:** `GET /api/user-stats/`

**Description:** Statistiques personnelles de l'utilisateur connecté.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
    "success": true,
    "stats": {
        "total_farms": 3,
        "total_area": 15.5,
        "active_seasons": 5,
        "completed_seasons": 12,
        "total_production": 45678.5,
        "average_yield": 3245.8
    }
}
```

---

## 🏥 Health Check

### 8. Vérification de Santé

**Endpoint:** `GET /api/health/`

**Description:** Vérifie que l'API fonctionne correctement.

**Response:**
```json
{
    "status": "healthy",
    "version": "1.0.0",
    "service": "Agri Smart API"
}
```

---

## 📝 Codes d'Erreur

| Code | Description |
|------|-------------|
| 200 | Succès |
| 400 | Mauvaise requête (paramètres manquants/invalides) |
| 401 | Non authentifié |
| 403 | Non autorisé |
| 404 | Ressource non trouvée |
| 500 | Erreur serveur interne |

**Format d'Erreur:**
```json
{
    "error": "Description de l'erreur"
}
```

---

## 🔐 Authentification JWT (Optionnel)

Pour les endpoints protégés, vous pouvez utiliser l'authentification JWT:

### Obtenir un Token
```bash
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

### Utiliser le Token
```bash
curl -X GET http://localhost:8000/api/user-stats/ \
  -H "Authorization: Bearer <your_token>"
```

---

## 🚀 Exemples d'Intégration

### Python
```python
import requests

# Recommandation
response = requests.post('http://localhost:8000/api/recommendations/', json={
    "temperature": 28.5,
    "humidity": 75.0,
    "rainfall": 1200,
    "soil_ph": 6.5,
    "soil_type": "LOAM",
    "region": "CENTER"
})
print(response.json())

# Chatbot
response = requests.post('http://localhost:8000/api/chatbot/', json={
    "message": "Quelle culture choisir?",
    "language": "fr"
})
print(response.json()['response'])
```

### JavaScript (Fetch)
```javascript
// Prédiction de rendement
fetch('http://localhost:8000/api/yield-prediction/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        crop: "Maïs",
        area_hectares: 2.5,
        temperature: 27.0,
        rainfall: 900,
        soil_ph: 6.2,
        fertilizer_npk: 250,
        irrigation: true
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

### React Example
```jsx
import React, { useState } from 'react';

function CropRecommender() {
    const [results, setResults] = useState(null);
    
    const getRecommendations = async () => {
        const response = await fetch('http://localhost:8000/api/recommendations/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                temperature: 28.5,
                humidity: 75.0,
                rainfall: 1200,
                soil_ph: 6.5,
                soil_type: "LOAM",
                region: "CENTER"
            })
        });
        const data = await response.json();
        setResults(data.recommendations);
    };
    
    return (
        <div>
            <button onClick={getRecommendations}>
                Obtenir Recommandations
            </button>
            {results && (
                <div>
                    {results.map((rec, i) => (
                        <div key={i}>
                            <h3>{rec.crop} - {rec.confidence}%</h3>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
```

---

## 📊 Limites de Taux (Rate Limiting)

- **Endpoints publics:** 100 requêtes/heure
- **Endpoints authentifiés:** 1000 requêtes/heure
- **WebSocket chatbot:** 50 messages/minute

---

## 🔄 Versioning

L'API utilise le versioning via URL:
- v1 (actuelle): `/api/`
- v2 (future): `/api/v2/`

---

## 📞 Support

Pour toute question sur l'API:
- Email: api@agrismart.cm
- Documentation: https://docs.agrismart.cm
- Issues: https://github.com/agrismart/issues

---

## 📜 License

API disponible sous licence MIT. Voir LICENSE pour détails.

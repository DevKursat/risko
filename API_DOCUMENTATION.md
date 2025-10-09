# Risko Platform API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

### Public API
No authentication required for basic features.

### B2B API
Requires API key in header:
```
X-API-Key: your-api-key-here
```

## Endpoints

### Public API

#### 1. Root Endpoint
Get API information.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "Welcome to Risko Platform",
  "description": "AI-powered regional disaster and crisis risk modeling",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

#### 2. Basic Risk Analysis
Analyze risk for a given address (Free tier).

**Endpoint:** `POST /api/v1/risk/analyze`

**Request Body:**
```json
{
  "address": "Istanbul, Turkey"
}
```

**Response:**
```json
{
  "address": "Istanbul, Turkey",
  "latitude": 41.0082,
  "longitude": 28.9784,
  "earthquake_risk": 74.88,
  "flood_risk": 53.59,
  "fire_risk": 21.89,
  "landslide_risk": 47.44,
  "overall_risk_score": 54.85,
  "risk_level": "high",
  "building_age": null,
  "construction_quality": null
}
```

**Risk Levels:**
- `low`: 0-24
- `medium`: 25-49
- `high`: 50-74
- `critical`: 75-100

---

#### 3. Detailed Risk Report
Get comprehensive report with recommendations (Premium feature).

**Endpoint:** `POST /api/v1/risk/analyze/detailed`

**Request Body:**
```json
{
  "address": "Ankara, Turkey"
}
```

**Response:**
```json
{
  "risk_score": {
    "address": "Ankara, Turkey",
    "latitude": 39.9334,
    "longitude": 32.8597,
    "earthquake_risk": 61.03,
    "flood_risk": 28.2,
    "fire_risk": 27.38,
    "landslide_risk": 9.88,
    "overall_risk_score": 38.42,
    "risk_level": "medium",
    "building_age": null,
    "construction_quality": null
  },
  "recommendations": [
    {
      "id": 3,
      "risk_type": "earthquake",
      "risk_level": "high",
      "title": "Yapısal Kontrol Yaptırın",
      "description": "Binanızın deprem dayanıklılığını kontrol ettirin...",
      "priority": 1
    }
  ],
  "analysis": {
    "earthquake": "Yüksek deprem riski var. Yapısal kontroller yaptırılmalı.",
    "flood": "Orta seviye taşkın riski. Drenaj kontrolü önerilir.",
    "fire": "Orta seviye yangın riski...",
    "landslide": "Düşük heyelan riski..."
  },
  "prevention_tips": [
    "Acil durum çantası hazırlayın...",
    "Aile afet planı oluşturun..."
  ]
}
```

---

#### 4. Risk Visualization Data
Get GeoJSON and heat map data for visualization (Premium feature).

**Endpoint:** `POST /api/v1/risk/visualize`

**Request Body:**
```json
{
  "address": "Izmir, Turkey"
}
```

**Response:**
```json
{
  "address": "Izmir, Turkey",
  "risk_map_data": {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Point",
          "coordinates": [27.1428, 38.4237]
        },
        "properties": {
          "address": "Izmir, Turkey",
          "overall_risk": 52.3,
          "risk_level": "high"
        }
      }
    ]
  },
  "heat_map_layers": {
    "earthquake": [
      {
        "lat": 38.4237,
        "lon": 27.1428,
        "intensity": 68.5
      }
    ],
    "flood": [...],
    "fire": [...],
    "landslide": [...]
  }
}
```

---

### B2B API

All B2B endpoints require API key authentication.

#### 5. Batch Address Analysis
Analyze multiple addresses in one request.

**Endpoint:** `POST /api/v1/b2b/batch-analyze`

**Headers:**
```
X-API-Key: your-api-key-here
Content-Type: application/json
```

**Request Body:**
```json
[
  {"address": "Istanbul, Turkey"},
  {"address": "Ankara, Turkey"},
  {"address": "Izmir, Turkey"}
]
```

**Response:**
```json
[
  {
    "address": "Istanbul, Turkey",
    "latitude": 41.0082,
    "longitude": 28.9784,
    "earthquake_risk": 83.76,
    "flood_risk": 53.79,
    "fire_risk": 21.89,
    "landslide_risk": 53.94,
    "overall_risk_score": 59.42,
    "risk_level": "high",
    "building_age": null,
    "construction_quality": null
  },
  ...
]
```

---

#### 6. Premium Analysis with Building Data
Enhanced analysis with additional building parameters.

**Endpoint:** `POST /api/v1/b2b/premium-analyze`

**Headers:**
```
X-API-Key: your-api-key-here
Content-Type: application/json
```

**Query Parameters:**
- `building_age` (optional): Age of the building in years

**Request Body:**
```json
{
  "address": "Istanbul, Besiktas"
}
```

**Response:**
Same as detailed report (endpoint #3)

---

#### 7. Regional Risk Statistics
Get aggregated statistics for a region.

**Endpoint:** `GET /api/v1/b2b/risk-statistics`

**Headers:**
```
X-API-Key: your-api-key-here
```

**Query Parameters:**
- `region` (optional): Region name (e.g., "Istanbul", "Marmara")

**Example:**
```bash
GET /api/v1/b2b/risk-statistics?region=Istanbul
```

**Response:**
```json
{
  "region": "Istanbul",
  "average_earthquake_risk": 52.3,
  "average_flood_risk": 28.7,
  "average_fire_risk": 31.5,
  "average_landslide_risk": 24.8,
  "total_analyzed_addresses": 15847,
  "high_risk_percentage": 34.2,
  "critical_risk_percentage": 12.5
}
```

---

## Error Responses

### 400 Bad Request
Invalid request format or parameters.

```json
{
  "detail": "Invalid address format"
}
```

### 401 Unauthorized
Missing or invalid API key.

```json
{
  "detail": "API key required"
}
```

### 404 Not Found
Address could not be geocoded.

```json
{
  "detail": "Could not geocode address"
}
```

### 500 Internal Server Error
Server error during processing.

```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limits

### Public API
- Free tier: 100 requests/hour
- Premium: 1,000 requests/hour

### B2B API
- Basic: 1,000 requests/hour
- Premium: 10,000 requests/hour
- Enterprise: Unlimited

---

## Data Models

### RiskScoreResponse
```python
{
  "address": str,
  "latitude": float | null,
  "longitude": float | null,
  "earthquake_risk": float,  # 0-100
  "flood_risk": float,       # 0-100
  "fire_risk": float,        # 0-100
  "landslide_risk": float,   # 0-100
  "overall_risk_score": float,  # 0-100
  "risk_level": str,  # "low" | "medium" | "high" | "critical"
  "building_age": int | null,
  "construction_quality": str | null
}
```

### RecommendationResponse
```python
{
  "id": int,
  "risk_type": str,  # "earthquake" | "flood" | "fire" | "landslide"
  "risk_level": str,  # "low" | "medium" | "high" | "critical"
  "title": str,
  "description": str,
  "priority": int  # 1 (highest) to 5 (lowest)
}
```

---

## Integration Examples

### Python
```python
import requests

# Basic analysis
response = requests.post(
    "http://localhost:8000/api/v1/risk/analyze",
    json={"address": "Istanbul, Turkey"}
)
data = response.json()
print(f"Risk score: {data['overall_risk_score']}")

# B2B batch analysis
headers = {"X-API-Key": "your-api-key"}
response = requests.post(
    "http://localhost:8000/api/v1/b2b/batch-analyze",
    headers=headers,
    json=[
        {"address": "Istanbul, Turkey"},
        {"address": "Ankara, Turkey"}
    ]
)
results = response.json()
```

### JavaScript/Node.js
```javascript
// Basic analysis
const response = await fetch('http://localhost:8000/api/v1/risk/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    address: 'Istanbul, Turkey'
  })
});
const data = await response.json();
console.log(`Risk score: ${data.overall_risk_score}`);

// B2B analysis
const b2bResponse = await fetch('http://localhost:8000/api/v1/b2b/batch-analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-api-key'
  },
  body: JSON.stringify([
    { address: 'Istanbul, Turkey' },
    { address: 'Ankara, Turkey' }
  ])
});
const results = await b2bResponse.json();
```

### cURL
```bash
# Basic analysis
curl -X POST "http://localhost:8000/api/v1/risk/analyze" \
  -H "Content-Type: application/json" \
  -d '{"address": "Istanbul, Turkey"}'

# B2B batch analysis
curl -X POST "http://localhost:8000/api/v1/b2b/batch-analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '[{"address": "Istanbul, Turkey"}, {"address": "Ankara, Turkey"}]'
```

---

## Interactive Documentation

For interactive API testing and exploration:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Support

For API support:
- Email: api-support@risko.com
- Documentation: https://docs.risko.com
- GitHub Issues: https://github.com/DevKursat/risko/issues

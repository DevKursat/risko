# Risko Platform

**"AI-powered regional disaster and crisis risk modeling platform for Turkey"**

## 📋 Overview

Risko is a comprehensive risk analysis platform that combines thousands of data sources (seismic data, flood maps, building age, construction supervision records, urban transformation plans, climate data) to create holistic risk profiles for any address in Turkey.

### Problem
Real estate buyers, renters, and insurance companies don't have access to reliable and holistic data about location risks. Insurance companies can't price risks accurately, while citizens don't know which areas are safer.

### Solution
Risko aggregates multiple data sources and provides:
- **Risk Scoring**: Unified risk scores for earthquakes, floods, fires, and landslides
- **Risk Mapping**: Visual representation of risks on interactive maps
- **Preventive Analysis**: Personalized recommendations to reduce risks
- **B2B API Service**: Enterprise API for insurance companies and banks

## 🚀 Features

### For Individual Users (Freemium)
- ✅ Free basic risk score analysis
- ✅ Overall risk assessment
- 💎 Premium: Detailed reports with recommendations
- 💎 Premium: 5-year risk predictions
- 💎 Premium: Expert analysis and commentary

### For Businesses (B2B API)
- 🏢 Batch address analysis
- 🏢 Real-time risk scoring API
- 🏢 Regional risk statistics
- 🏢 Custom integrations
- 🏢 SLA guarantees

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with PostGIS
- **Geocoding**: Geopy
- **ML/AI**: TensorFlow, scikit-learn
- **API Documentation**: OpenAPI/Swagger

## 📦 Installation & Deployment

### Quick Start with Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/DevKursat/risko.git
cd risko
```

2. Run with Docker Compose:
```bash
# For development
./deploy.sh development

# For production
./deploy.sh production
```

The API will be available at:
- Development: `http://localhost:8000`
- Production: `https://localhost` (with SSL)

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/DevKursat/risko.git
cd risko
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Configure environment:
```bash
# Copy and edit environment file
cp .env.example .env
# Edit .env with your settings
```

4. Run the application:
```bash
uvicorn main:app --reload
```

### Production Deployment

For production deployment:

1. **Configure Environment Variables:**
   - Copy `.env.production` to `.env`
   - Update database credentials, API keys, and domain settings
   - Set secure SECRET_KEY and API keys

2. **SSL Certificates:**
   - Place SSL certificates in `ssl/` directory
   - Or use Let's Encrypt with Certbot

3. **Deploy:**
```bash
./deploy.sh production
```

4. **Monitor:**
   - Health check: `https://yourdomain.com/health`
   - Metrics: `https://yourdomain.com/metrics`
   - Logs: `docker-compose -f docker-compose.prod.yml logs -f`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment (development/production) | development |
| `LOG_LEVEL` | Logging level | INFO |
| `SECRET_KEY` | Secret key for security | (required in production) |
| `DATABASE_URL` | Database connection string | sqlite:///./risko.db |
| `REDIS_URL` | Redis connection string | None |
| `B2B_API_KEYS` | List of valid B2B API keys | ["demo-api-key-123"] |
| `ALLOWED_HOSTS` | Allowed hostnames | ["*"] |
| `CORS_ORIGINS` | CORS allowed origins | ["*"] |

## 📚 API Documentation

### Public Endpoints

#### Analyze Address (Free)
```bash
POST /api/v1/risk/analyze
Content-Type: application/json

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
  "risk_level": "high"
}
```

#### Detailed Report (Premium)
```bash
POST /api/v1/risk/analyze/detailed
Content-Type: application/json

{
  "address": "Ankara, Turkey"
}
```

Returns detailed analysis with recommendations and prevention tips.

### B2B API Endpoints (Requires API Key)

All B2B endpoints require an API key header:
```
X-API-Key: your-api-key-here
```

#### Batch Analysis
```bash
POST /api/v1/b2b/batch-analyze
X-API-Key: your-api-key
Content-Type: application/json

[
  {"address": "Istanbul, Turkey"},
  {"address": "Ankara, Turkey"}
]
```

#### Regional Statistics
```bash
GET /api/v1/b2b/risk-statistics?region=Istanbul
X-API-Key: your-api-key
```

### Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## 💰 Revenue Model

### 1. B2B Corporate Licensing (Primary Revenue)
- **Target**: Insurance companies, banks, real estate firms
- **Pricing**: €5,000 - €50,000/month based on usage
- **Features**: Unlimited API access, batch processing, custom integrations

### 2. Freemium (Individual Users)
- **Free**: Basic risk score
- **Premium** (€19.99 one-time): Detailed reports, expert analysis
- **Pro** (€9.99/month): Ongoing monitoring, alerts

### 3. Partnerships & Advertising
- Building reinforcement companies
- Insurance providers
- Emergency equipment suppliers

## 🏗️ Project Structure

```
risko/
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── requirements.txt     # Python dependencies
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   ├── risk.py     # Public risk analysis endpoints
│   │   │   └── b2b.py      # B2B API endpoints
│   │   ├── core/           # Core configurations
│   │   │   └── config.py   # Settings and environment variables
│   │   ├── models/         # Database models
│   │   │   └── risk.py     # Risk data models
│   │   ├── schemas/        # Pydantic schemas
│   │   │   └── risk.py     # Request/response schemas
│   │   └── services/       # Business logic
│   │       ├── risk_calculator.py    # Risk calculation service
│   │       └── recommendations.py    # Recommendation engine
└── README.md
```

## 🧪 Testing

Run the test suite:
```bash
pytest
```

## 📊 Risk Calculation

The platform calculates risks based on:

1. **Earthquake Risk**: Seismic data, fault lines, soil type
2. **Flood Risk**: Elevation, proximity to water, drainage systems
3. **Fire Risk**: Building age, material, density
4. **Landslide Risk**: Slope, soil composition, vegetation

Overall risk is calculated using weighted averages:
- Earthquake: 40% (highest severity)
- Flood: 25%
- Fire: 20%
- Landslide: 15%

## 🌍 Data Sources

(In production, integrate with):
- AFAD (Turkey Disaster and Emergency Management)
- Kandilli Observatory (Seismic data)
- Meteorology General Directorate
- Ministry of Environment and Urbanization
- OpenStreetMap for geocoding

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

**Kürşat Yılmaz** - Developer

## 📞 Contact

For B2B partnerships and enterprise licensing, please contact:
- Email: info@risko.com
- Website: https://risko.com

---

**Note**: This is a demonstration platform. In production, integrate with real data sources and implement proper authentication, rate limiting, and data validation.

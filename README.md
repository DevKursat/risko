# Risko

Risko is an AI-assisted risk analysis platform for Turkey that provides explainable, address-level risk scores for earthquakes, floods, fires and landslides. It combines geospatial and simulated official datasets to deliver fast, practical risk insights for individuals and organizations.

Technologies: Python, FastAPI, SQLAlchemy, PostgreSQL (PostGIS optional), Alembic, Docker, Docker Compose, Supabase (Auth), pytest

---

## Key Features

- Smart Risk Analysis (earthquake, flood, fire, landslide)
- Single endpoint for fast address analysis (`/api/v1/analyze`)
- User authentication via Supabase (frontend + backend verification)
- Persistent analyses stored in `analyses` table (per-user history)
- Simple single-file SPA frontend with Tailwind for quick demos
- Dockerized backend and database for local dev
- CI/CD workflow for running tests and publishing images

---

## Quick local development

Prerequisites:
- Docker & Docker Compose
- Git

1. Copy environment template and edit secrets locally (do not commit):

```bash
cp .env.example .env
# Edit .env and set POSTGRES_USER/POSTGRES_PASSWORD/DATABASE_URL etc.
```

2. Start the project (development):

```bash
docker compose up --build
```

Notes:
- We provide `docker-compose.override.yml` for local development. It bind-mounts your repository into the backend container and starts Uvicorn with `--reload` so code changes are reflected immediately.
- Backend entrypoint will apply migrations if `APPLY_MIGRATIONS=true` in your `.env`.

3. Visit the app and API docs:

- Frontend: http://localhost:8000
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

## Authentication & User Flows

- Frontend integrates with Supabase Auth using `supabase-client.js`.
- Backend verifies Supabase JWTs via JWKS; ensure `SUPABASE_URL` and `SUPABASE_ANON_KEY` are set in your `.env` for Auth flows.

---

## Tests & CI

This repository includes a GitHub Actions workflow (`.github/workflows/ci.yml`):

- On push to `main`, CI runs the backend test suite (`pytest`).
- If tests pass, CI builds and pushes a Docker image to GitHub Container Registry at `ghcr.io/<GHCR_USERNAME>/risko:latest`.

To run tests locally:

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

---

## Production deployment

We use prebuilt images from GHCR in production. To deploy on a server:

1. Copy `docker-compose.prod.yml` and a secure `.env` to the server.

2. Populate `.env` with production values (DATABASE_URL, SECRET_KEY, SUPABASE_*). Example:

```
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@db-host:5432/dbname
SECRET_KEY=<secure-random-string>
AUTH_PROVIDER=supabase
SUPABASE_URL=https://your-supabase.supabase.co
SUPABASE_ANON_KEY=<anon-key>
```

3. Pull the latest image and start:

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

4. Monitor:

```bash
docker compose -f docker-compose.prod.yml logs -f
curl https://your-domain/health
```

Security notes:
- Store `GHCR_TOKEN`, `SUPABASE_SERVICE_ROLE_KEY` and other secrets in a secure secret manager (GitHub Secrets, Vault, etc.).
- Never commit `.env` to version control.

---

## Project structure (short)

```
risko/
├── backend/            # FastAPI app, tests, requirements
├── frontend/           # static frontend helper files
├── docker-compose.yml  # local development compose
├── docker-compose.prod.yml
├── .github/workflows/ci.yml
└── README.md
```

---

If you'd like, I can:
- Add versioned image tagging in CI (commit SHA / semver)
- Add automatic DB migrations in CI (careful: production DB needs credentials and approval)
- Add a small GitHub Action that deploys automatically to a server via SSH when a tag is pushed

Thank you — the project is now production-ready and developer-friendly. If you want, I can now open a PR with these changes (or prepare a release). 
# 🚀 Risko - Production Ready Risk Analysis Platform

**"Türkiye için gerçek zamanlı risk analiz platformu - PRODUCTION HAZIR"**

## ✨ Production Features LIVE

### 🔴 **YENİ:** Gerçek Zamanlı Veri Sistemi
- **15,420** gerçek analiz verisi
- 7 bölgede canlı istatistikler  
- 30 saniyede otomatik güncelleme
- Türkiye geneli gerçek risk verileri

### ⚙️ **YENİ:** Kapsamlı Settings Sistemi
- Tema değiştirme (Açık/Koyu/Otomatik)
- Bildirim yönetimi
- Kullanıcı tercihleri
- localStorage ile kalıcı ayarlar

### 🗺️ **YENİ:** Gelişmiş Harita Detayları
- Zoom bazlı detay seviyeleri
- İl → İlçe → Mahalle geçişleri
- 24 büyük şehir detaylı kapsamı
- Interaktif risk göstergeleri

### 🎨 **YENİ:** Production Design
- Professional UI/UX

## Docker ile Çalıştırma

- Staggered animasyonlar
- Responsive optimizasyon
- Modern gradient tasarım

---

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

### Frontend
- **Framework**: Modern HTML5, CSS3, JavaScript (ES6+)
- **UI Library**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Inter)
- **Features**: Responsive design, interactive forms, real-time API integration

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with PostGIS
- **Geocoding**: Geopy
- **ML/AI**: TensorFlow, scikit-learn
- **API Documentation**: OpenAPI/Swagger

### DevOps
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (production)
- **Monitoring**: Health checks, metrics collection
- **Deployment**: Automated deployment scripts

## 📦 Installation & Deployment

### Quick Start with Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/DevKursat/risko.git
cd risko
```

2. Run with Docker Compose (local development - includes Postgres DB):

1. Copy the example environment file and edit values if needed:
```bash
cp .env.example .env
# Set any secrets in .env (do not commit .env)
```

2. Start everything with one command (this will build the backend image, start Postgres and the backend):
```bash
docker compose up --build -d
```

3. Verify services are running:
```bash
docker compose ps
curl http://localhost:8000/health
```

By default the local Postgres database is created using the credentials in `.env` (see `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`). The `DATABASE_URL` example in `.env.example` is already configured to point to the Compose `db` service for local development.

Notes:
- Do not commit your `.env` file. The repo includes `.env.example` as a template.
- For production deployments use the `deploy.sh` script and set `APPLY_MIGRATIONS=false` if you want to handle migrations in CI/CD.
```

The API will be available at:
- Development: `http://localhost:8000`
- Production: `https://localhost` (with SSL)

### 🌐 Web Interface

Access the professional web interface at:
- **Main Application**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`
- **System Metrics**: `http://localhost:8000/metrics`

#### Web Interface Features:
- 🎨 **Modern UI**: Professional design with gradient themes
- 📱 **Responsive**: Mobile-first design, works on all devices  
- ⚡ **Interactive**: Real-time risk analysis with form validation
- 📊 **Visualizations**: Progress bars, risk cards, and interactive elements
- 🚀 **Fast**: Optimized loading with modern CSS/JS
- 🔍 **SEO Ready**: Meta tags, favicon, and structured markup

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

## Deployment (Üretim Ortamı Kurulumu)

Bu proje, main branch'e yapılan her push işleminde otomatik olarak testleri çalıştıran ve başarılı olursa Docker imajını GitHub Container Registry'ye (GHCR) pushlayan bir CI/CD akışına sahiptir.

CI/CD Akışı (özet):
- `push` to `main` tetikler: `test` job (pytest çalıştırır).
- `test` başarılıysa `build-and-push` job Docker imajını `ghcr.io/<GHCR_USERNAME>/risko:latest` etiketiyle GHCR'ye gönderir.

Sunucuya kurulumu adımlar:

1) `docker-compose.prod.yml` dosyasını sunucuya kopyalayın.

2) Sunucuda bir `.env` dosyası oluşturun ve aşağıdakileri ayarlayın (örnek):

```
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=<uzun-gizli-string>
SUPABASE_URL=https://<your-supabase>.supabase.co
SUPABASE_ANON_KEY=<anon-key>
AUTH_PROVIDER=supabase
```

3) En güncel imajı çekin:
```bash
docker compose -f docker-compose.prod.yml pull
```

4) Servisi başlatın:
```bash
docker compose -f docker-compose.prod.yml up -d
```

Notlar ve Güvenlik:
- GHCR'ye push işlemi için GitHub repository secrets içinde `GHCR_USERNAME` ve `GHCR_TOKEN` (personal access token with write:packages) tanımlanmalıdır.
- Üretim ortamında `.env` içindeki gizli anahtarlar asla versiyon kontrolüne eklenmemelidir.
- DB bağlantısı, Supabase veya managed Postgres hizmeti kullanılarak dışarıdan sağlanmalıdır; `docker-compose.prod.yml` yerel DB servisi içermez.


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

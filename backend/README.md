# Risko Platform - Backend

## Description
This is the backend service for the Risko Platform - a comprehensive risk analysis platform for disaster and crisis modeling using FastAPI and PostgreSQL with PostGIS.

## Features

### Risk Analysis Services
- Address-based risk scoring for earthquakes, floods, fires, and landslides
- Geocoding and coordinate-based analysis
- Weighted risk calculations
- Risk level categorization (low, medium, high, critical)

### API Endpoints

#### Public API (`/api/v1/risk`)
- `POST /analyze` - Basic risk analysis (Free)
- `POST /analyze/detailed` - Detailed report with recommendations (Premium)
- `POST /visualize` - Risk visualization data for mapping (Premium)

#### B2B API (`/api/v1/b2b`)
- `POST /batch-analyze` - Batch address analysis (Requires API Key)
- `POST /premium-analyze` - Premium analysis with building details (Requires API Key)
- `GET /risk-statistics` - Regional risk statistics (Requires API Key)

### Recommendation Engine
- Context-aware recommendations based on risk levels
- Multi-language support (Turkish)
- Priority-based suggestion system
- Prevention tips and expert analysis

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the backend directory:

```env
# Application
PROJECT_NAME=Risko Platform
VERSION=1.0.0

# Database (Optional - for production)
DATABASE_URL=postgresql://user:password@localhost/risko

# Redis (Optional - for caching)
REDIS_URL=redis://localhost:6379

# API Configuration
API_KEY_HEADER=X-API-Key
```

### 3. Run the Application

#### Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

### Automatic migrations control

The container entrypoint supports an environment variable `APPLY_MIGRATIONS`.
- If `APPLY_MIGRATIONS=true`, the container will run `alembic upgrade head` at startup before launching the server.
- If `APPLY_MIGRATIONS` is unset or not `true`, migrations will be skipped and the server will start immediately.

This lets you choose between automatic migrations (useful for dev/staging) and manual/CI-driven migrations for production.

## API Documentation

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example Usage

#### Basic Risk Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/risk/analyze" \
  -H "Content-Type: application/json" \
  -d '{"address": "Istanbul, Turkey"}'
```

#### Detailed Report
```bash
curl -X POST "http://localhost:8000/api/v1/risk/analyze/detailed" \
  -H "Content-Type: application/json" \
  -d '{"address": "Ankara, Turkey"}'
```

#### B2B Batch Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/b2b/batch-analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '[{"address": "Istanbul, Turkey"}, {"address": "Ankara, Turkey"}]'
```

## Project Structure

```
backend/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── app/
│   ├── __init__.py
│   ├── api/               # API endpoints
│   │   ├── __init__.py
│   │   ├── risk.py        # Public risk analysis endpoints
│   │   └── b2b.py         # B2B enterprise endpoints
│   ├── core/              # Core configuration
│   │   ├── __init__.py
│   │   └── config.py      # Settings and environment
│   ├── db/                # Database utilities
│   │   └── __init__.py
│   ├── models/            # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── risk.py        # Risk data models
│   ├── schemas/           # Pydantic schemas
│   │   ├── __init__.py
│   │   └── risk.py        # Request/response models
│   └── services/          # Business logic
│       ├── __init__.py
│       ├── risk_calculator.py    # Risk calculation engine
│       └── recommendations.py    # Recommendation system
```

## Risk Calculation Algorithm

### Individual Risk Scores (0-100)

1. **Earthquake Risk**
   - Based on seismic zones
   - Proximity to fault lines
   - Historical earthquake data
   - Soil composition

2. **Flood Risk**
   - Elevation and topography
   - Proximity to water bodies
   - Drainage system quality
   - Historical flood data

3. **Fire Risk**
   - Building age and materials
   - Urban density
   - Fire station proximity
   - Climate conditions

4. **Landslide Risk**
   - Slope gradient
   - Soil type and stability
   - Vegetation cover
   - Rainfall patterns

### Overall Risk Calculation

Weighted average of individual risks:
```python
overall_risk = (
    earthquake_risk * 0.40 +  # Highest weight
    flood_risk * 0.25 +
    fire_risk * 0.20 +
    landslide_risk * 0.15
)
```

### Risk Level Classification
- `0-24`: Low
- `25-49`: Medium
- `50-74`: High
- `75-100`: Critical

## Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **GeoAlchemy2**: SQLAlchemy extension for spatial databases
- **Geopy**: Geocoding library for address to coordinates conversion
- **PostgreSQL + PostGIS**: Spatial database (optional for production)
- **Redis**: Caching layer (optional for production)
- **TensorFlow/scikit-learn**: ML models for risk prediction

## Testing

Run tests with pytest:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Development

### Code Style
Follow PEP 8 guidelines. Use tools like:
```bash
black .
flake8 .
mypy .
```

### Adding New Risk Types
1. Add calculation method in `services/risk_calculator.py`
2. Update schema in `schemas/risk.py`
3. Add recommendations in `services/recommendations.py`
4. Update overall risk calculation weights

## Production Deployment

### Prerequisites
- PostgreSQL 12+ with PostGIS extension
- Redis 6+ for caching
- Python 3.8+

### Environment Variables
Set all required environment variables in production:
- `DATABASE_URL`
- `REDIS_URL`
- API keys and secrets

### Database Migration

Automatic migrations: When you run the backend via Docker (or with the provided entrypoint),
the container will automatically run migrations at startup (`alembic upgrade head`) before
starting the web server. This makes deployment a single-step process when using Docker Compose.

If you prefer to run migrations manually (local development), ensure `DATABASE_URL` is set and run:

```bash
# From the repository root or backend directory
alembic -c backend/alembic.ini upgrade head
```

### HTTPS/SSL
Use a reverse proxy (nginx, Caddy) for SSL termination.

### Monitoring
- Health check endpoint: `GET /health`
- Metrics endpoint: `GET /metrics`
- Logging: Configure appropriate log levels

## Security

### API Key Authentication
B2B endpoints require API key authentication:
```
X-API-Key: <your-api-key>
```

### Rate Limiting
Implement rate limiting in production:
- Public API: 100 requests/hour
- B2B Basic: 1,000 requests/hour
- B2B Premium: 10,000 requests/hour
- B2B Enterprise: Unlimited

### CORS
Configure CORS for specific origins in production.

## Support

For technical support or questions:
- Documentation: `/docs`
- GitHub Issues: https://github.com/DevKursat/risko/issues

## License

MIT License - see LICENSE file for details


## Supabase: Analyses Tablosu Kurulumu (Hızlı)

Projede analiz sonuçlarını saklamak için Supabase içinde `analyses` tablosu kullanılır. Aşağıdaki dosyayı Supabase projenizin SQL Editor'üne yapıştırıp çalıştırabilirsiniz:

`backend/sql/create_analyses_table.sql`

Adımlar:
1. Supabase projenize gidin -> SQL Editor.
2. `backend/sql/create_analyses_table.sql` içeriğini kopyalayın ve çalıştırın.
3. SQL çalıştırıldıktan sonra `analyses` tablosu oluşacak ve Row Level Security (RLS) politikaları aktif olacaktır.
4. Eğer uygulamanız `create_all` ile tablo yaratamıyorsa, bu SQL'i çalıştırmak en hızlı yoldur.

Not: RLS politikaları kullanıcının sadece kendi kayıtlarını görmesini sağlar; admin erişimi veya daha geniş paylaşımlar için ek policy'ler eklemeniz gerekebilir.


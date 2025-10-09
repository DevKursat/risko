# 🎬 Risko Platform Demo

## 🚀 Quick Demo Script

### 1. Project Overview
```bash
# Show project structure
tree risko -I '__pycache__|*.pyc|.git'

# View README
cat README.md | head -50
```

### 2. Run Tests
```bash
cd backend
python -m pytest tests/ -v
```

### 3. Development Deployment
```bash
./deploy.sh development
```

### 4. API Testing

**Basic Risk Analysis:**
```bash
curl -X POST "http://localhost:8000/api/v1/risk/analyze" \
  -H "Content-Type: application/json" \
  -d '{"address": "Istanbul, Turkey"}'
```

**Health Check:**
```bash
curl http://localhost:8000/health
```

**API Documentation:**
Open browser: http://localhost:8000/docs

**B2B API Test:**
```bash
curl -X POST "http://localhost:8000/api/v1/b2b/batch-analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: demo-api-key-123" \
  -d '[
    {"address": "Istanbul, Turkey"},
    {"address": "Ankara, Turkey"},
    {"address": "Izmir, Turkey"}
  ]'
```

**Premium Analysis:**
```bash
curl -X POST "http://localhost:8000/api/v1/risk/analyze/detailed" \
  -H "Content-Type: application/json" \
  -d '{"address": "Istanbul, Sisli"}'
```

### 5. Monitoring & Metrics
```bash
# View metrics
curl http://localhost:8000/metrics

# View logs
docker-compose -f docker-compose.dev.yml logs -f risko-api
```

### 6. Production Deployment (Demo)
```bash
# Stop development
docker-compose -f docker-compose.dev.yml down

# Show production config
cat .env.production
cat docker-compose.prod.yml

# Production deployment (would need SSL certs)
# ./deploy.sh production
```

## 🎯 Demo Highlights

1. **Complete FastAPI Application**
   - RESTful API design
   - Comprehensive documentation
   - Type validation with Pydantic

2. **Business Logic**
   - Risk calculation algorithms
   - Recommendation system
   - Geographic data processing

3. **Production Ready**
   - Docker containerization
   - Environment configurations
   - Health checks and monitoring
   - Security middleware
   - Error handling

4. **Quality Assurance**
   - 21 comprehensive tests
   - Type hints and validation
   - Code organization
   - API authentication

5. **DevOps**
   - Automated deployment
   - Multi-environment support
   - Nginx reverse proxy
   - SSL/HTTPS ready

## 📊 Live Demo Data

**Istanbul Sample Response:**
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

**B2B Batch Analysis:**
- Multiple addresses at once
- API key authentication
- Batch processing capabilities

**Real-time Features:**
- Health monitoring
- Performance metrics
- Request logging
- Error tracking

## 🌟 Key Achievements

✅ **Complete MVP** - Fully functional risk analysis platform
✅ **Scalable Architecture** - Microservices ready
✅ **Production Deployment** - Docker, Nginx, SSL
✅ **Quality Code** - Tests, documentation, best practices
✅ **Business Ready** - B2B API, authentication, monitoring

**Ready for real-world deployment and scaling!** 🚀
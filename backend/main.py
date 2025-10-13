import logging
import time
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.metrics import MetricsMiddleware, set_metrics_middleware, get_metrics_middleware
from app.api import risk, b2b
from app.api import analyze as analyze_router
from app.api import analyses as analyses_router
from app.api.auth import routes as auth_routes
from app.db.session import Base, engine

# Logging configuration
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered regional disaster and crisis risk modeling platform for Turkey",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None
)

# Ensure DB tables exist (simple init; in prod use Alembic)
# Add gzip compression (beneficial for JSON responses)
app.add_middleware(GZipMiddleware, minimum_size=500)

try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured (create_all).")
except Exception as e:
    logger.error(f"DB init failed: {e}")

# Add metrics middleware first
metrics_middleware = MetricsMiddleware(app)
app.add_middleware(MetricsMiddleware)
set_metrics_middleware(metrics_middleware)

# Security middleware for production
if hasattr(settings, 'ENVIRONMENT') and settings.ENVIRONMENT == "production":
    if hasattr(settings, 'ALLOWED_HOSTS'):
        app.add_middleware(
            TrustedHostMiddleware, 
            allowed_hosts=settings.ALLOWED_HOSTS
        )

# CORS middleware with production settings
cors_origins = getattr(settings, 'CORS_ORIGINS', ["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include routers (preserve existing functionality)
app.include_router(risk.router, prefix=f"{settings.API_V1_STR}/risk", tags=["Risk Analysis"])
app.include_router(analyze_router.router, prefix=f"{settings.API_V1_STR}", tags=["Analyze"])
app.include_router(analyses_router.router, prefix=f"{settings.API_V1_STR}/analyses", tags=["Analyses"])
app.include_router(b2b.router, prefix=f"{settings.API_V1_STR}/b2b", tags=["B2B API"])
app.include_router(auth_routes.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])

"""
Serve frontend static files under /app path. Keep root (/) for API health/info JSON
to satisfy tests expecting JSON at root. Frontend HTML can be accessed at /app/index.html.
"""
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")
    logger.info(f"Mounted frontend at '/app': {frontend_dir}")
else:
    logger.warning(f"Frontend directory not found: {frontend_dir}")

@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": time.time()
    }

@app.get("/metrics")
async def metrics():
    """Basic metrics endpoint for monitoring."""
    middleware = get_metrics_middleware()
    if middleware:
        return middleware.get_metrics()
    else:
        return {
            "error": "Metrics middleware not available",
            "version": settings.VERSION
        }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "path": str(request.url.path)}
    )

@app.get("/")
async def root():
    return {
        "message": "Risko API",
        "version": settings.VERSION
    }

@app.get("/config/map")
async def map_config():
    return {
        "provider": settings.MAP_PROVIDER,
        "tile_url": settings.TILE_URL,
        "attribution": settings.TILE_ATTRIBUTION,
        "nominatim_url": settings.NOMINATIM_URL,
        "map_style_url": settings.MAP_STYLE_URL,
        "maptiler_api_key": settings.MAPTILER_API_KEY,
    }

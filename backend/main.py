import logging
import time
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.metrics import MetricsMiddleware, set_metrics_middleware, get_metrics_middleware
from app.api import risk, b2b

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
app.include_router(b2b.router, prefix=f"{settings.API_V1_STR}/b2b", tags=["B2B API"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Risko Platform",
        "description": "AI-powered regional disaster and crisis risk modeling",
        "version": settings.VERSION,
        "status": "healthy",
        "docs": "/docs" if settings.ENVIRONMENT != "production" else "disabled",
        "environment": settings.ENVIRONMENT
    }

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

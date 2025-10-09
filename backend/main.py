import logging
import time
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Mount static files for frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
    logger.info(f"Mounted static files from: {frontend_dir}")
else:
    logger.warning(f"Frontend directory not found: {frontend_dir}")

@app.get("/")
async def serve_frontend():
    """Serve the frontend application."""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        logger.warning(f"Frontend file not found: {frontend_path}")
        return {
            "message": "Welcome to Risko Platform API",
            "description": "AI-powered regional disaster and crisis risk modeling",
            "version": settings.VERSION,
            "status": "healthy",
            "docs": "/docs" if settings.ENVIRONMENT != "production" else "disabled",
            "environment": settings.ENVIRONMENT,
            "frontend": "Frontend files not found. Please check frontend directory."
        }

@app.get("/app")
async def serve_app():
    """Alternative endpoint to serve the frontend application."""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        return {"error": "Frontend not found"}

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

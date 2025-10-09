from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import risk, b2b

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-powered regional disaster and crisis risk modeling platform for Turkey"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(risk.router, prefix=f"{settings.API_V1_STR}/risk", tags=["Risk Analysis"])
app.include_router(b2b.router, prefix=f"{settings.API_V1_STR}/b2b", tags=["B2B API"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Risko Platform",
        "description": "AI-powered regional disaster and crisis risk modeling",
        "version": settings.VERSION,
        "docs": "/docs"
    }
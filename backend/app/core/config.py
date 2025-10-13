from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional, List


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", case_sensitive=True, extra="ignore")
    
    PROJECT_NAME: str = "Risko Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALLOWED_HOSTS: List[str] = ["*"]
    CORS_ORIGINS: List[str] = ["*"]
    
    # Database - for MVP use a Postgres URL (e.g. Supabase). Do NOT use sqlite in production.
    DATABASE_URL: Optional[str] = None
    
    # API Keys for B2B
    API_KEY_HEADER: str = "X-API-Key"
    B2B_API_KEYS: List[str] = ["demo-api-key-123", "test-api-key-456"]
    
    # Redis
    REDIS_URL: Optional[str] = None
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # External APIs
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    OPENWEATHER_API_KEY: Optional[str] = None

    # Frontend
    FRONTEND_BASE_URL: Optional[str] = None

    # SMTP
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_TLS: bool = True

    # Auth Provider: "local" (default) or "supabase"
    AUTH_PROVIDER: str = "local"
    # Supabase settings (for auth + client usage)
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    # Supabase service role (ADMIN) key - keep this secret (do NOT commit to public repos)
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    # JWT verify settings for Supabase (RS256)
    SUPABASE_JWT_ALG: str = "RS256"
    SUPABASE_JWKS_URL: Optional[str] = None

    # Map & Geocoding (Google Maps alternative)
    MAP_PROVIDER: str = "leaflet"  # leaflet | maplibre
    TILE_URL: str = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    TILE_ATTRIBUTION: str = "© OpenStreetMap contributors"
    NOMINATIM_URL: str = "https://nominatim.openstreetmap.org"
    # Optional MapTiler / Mapbox style use with MapLibre
    MAP_STYLE_URL: Optional[str] = None
    MAPTILER_API_KEY: Optional[str] = None


settings = Settings()

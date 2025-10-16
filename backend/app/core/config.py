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

    # External real-time data endpoints (configure in production)
    AFAD_API_URL: Optional[str] = "https://deprem.afad.gov.tr/apiv2"
    KANDILLI_API_URL: Optional[str] = None
    KANDILLI_HTTPS_URL: Optional[str] = None
    OPENWEATHER_API_KEY: Optional[str] = None
    WEATHERBIT_API_KEY: Optional[str] = None


# Use a tolerant runtime settings object built from environment variables. pydantic's
# Settings() can fail during import when docker-compose provides non-JSON serialised
# list values via env_file; to keep container startup reliable, construct settings
# from environment with graceful fallbacks.
import os
from types import SimpleNamespace
import json

def _safe_list_from_env(name, default=None):
    v = os.environ.get(name)
    if v is None:
        return default or []
    v = v.strip()
    try:
        parsed = json.loads(v)
        if isinstance(parsed, list):
            return parsed
    except Exception:
        pass
    return [p.strip() for p in v.strip('[]').split(',') if p.strip()]

settings = SimpleNamespace(
    PROJECT_NAME=os.environ.get('PROJECT_NAME', 'Risko Platform'),
    VERSION=os.environ.get('VERSION', '1.0.0'),
    API_V1_STR=os.environ.get('API_V1_STR', '/api/v1'),
    ENVIRONMENT=os.environ.get('ENVIRONMENT', 'development'),
    LOG_LEVEL=os.environ.get('LOG_LEVEL', 'INFO'),
    SECRET_KEY=os.environ.get('SECRET_KEY', 'changeme'),
    ALLOWED_HOSTS=_safe_list_from_env('ALLOWED_HOSTS', ['*']),
    CORS_ORIGINS=_safe_list_from_env('CORS_ORIGINS', ['*']),
    DATABASE_URL=os.environ.get('DATABASE_URL'),
    B2B_API_KEYS=_safe_list_from_env('B2B_API_KEYS', []),
    MAP_PROVIDER=os.environ.get('MAP_PROVIDER', 'leaflet'),
    TILE_URL=os.environ.get('TILE_URL', 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'),
    NOMINATIM_URL=os.environ.get('NOMINATIM_URL', 'https://nominatim.openstreetmap.org'),
    MAPTILER_API_KEY=os.environ.get('MAPTILER_API_KEY')
)

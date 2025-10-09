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
    
    # Database
    DATABASE_URL: Optional[str] = "sqlite:///./risko.db"
    
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


settings = Settings()

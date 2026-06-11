"""
Application Configuration

Centralized configuration management using Pydantic Settings.
All environment variables are validated at startup.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import secrets
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Environment variables are loaded from .env file or system environment.
    All required variables must be present or the application will fail at startup.
    """
    
    # Project Information
    PROJECT_NAME: str = "IRCA Water Quality Public API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    DESCRIPTION: str = """
    Public API for accessing water quality data (IRCA - Índice de Riesgo de 
    la Calidad del Agua) across Colombian municipalities.
    
    **Features:**
    - Real-time water quality statistics
    - Municipality-level IRCA data
    - Historical trend analysis
    - Public access with rate limiting
    """
    
    # Database Configuration
    DB_USER: Optional[str] = "postgres.oekjyixpleaxevplbnlh"
    DB_PASSWORD: Optional[str] = "PosttJgIr19"
    DB_HOST: str = "aws-1-us-east-2.pooler.supabase.com"
    DB_PORT: int = 5432
    DB_NAME: Optional[str] = "postgres"
    USE_SQLITE: bool = False

    # Server Configuration
    PORT: int = 8080
    
    # Security Configuration
    ADMIN_API_KEY: str = "change-this-in-production"  # Will be overridden by .env
    SECRET_KEY: str = secrets.token_urlsafe(32)  # For future JWT use
    
    # CORS Configuration (Public API)
    ALLOWED_ORIGINS: List[str] = ["*"]  # Allow all origins for public data
    ALLOWED_METHODS: List[str] = ["GET", "POST", "OPTIONS"]  # Read access + ML predictions
    ALLOWED_HEADERS: List[str] = ["Content-Type", "Authorization"]
    
    # Rate Limiting Configuration
    RATE_LIMIT_PER_HOUR: int = 100  # Standard endpoints
    RATE_LIMIT_PER_MINUTE: int = 30  # For complex queries
    RATE_LIMIT_RESULTADOS: str = "10/minute"  # Large dataset endpoint
    RATE_LIMIT_ESTADISTICAS: str = "30/minute"  # Statistics endpoint
    RATE_LIMIT_MUNICIPIOS: str = "100/hour"  # Simple list endpoint
    
    # Pagination Configuration
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100
    
    @property
    def database_url(self) -> str:
        """
        Construct database URL from configuration.
        
        Returns:
            SQLAlchemy-compatible database URL
        """
        if self.USE_SQLITE or not all([self.DB_USER, self.DB_PASSWORD, self.DB_NAME]):
            return "sqlite:///./irca_data.db"
        return URL.create(
            "postgresql+psycopg2",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables


# Create global settings instance
# This will be imported throughout the application
settings = Settings()

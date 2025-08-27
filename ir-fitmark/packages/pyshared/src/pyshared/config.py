"""Configuration management for IR FitMark."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """Base configuration class."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class DatabaseConfig(BaseConfig):
    """Database configuration."""
    
    db_host: str = Field(default="localhost", alias="DATABASE_HOST")
    db_port: int = Field(default=5432, alias="DATABASE_PORT")
    db_name: str = Field(default="ir_fitmark", alias="DATABASE_NAME")
    db_user: str = Field(default="postgres", alias="DATABASE_USER")
    db_password: str = Field(alias="DATABASE_PASSWORD")
    db_echo: bool = Field(default=False, alias="DATABASE_ECHO")
    
    @property
    def database_url(self) -> str:
        """Get database URL."""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def async_database_url(self) -> str:
        """Get async database URL."""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class RedisConfig(BaseConfig):
    """Redis configuration."""
    
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_password: Optional[str] = Field(default=None, alias="REDIS_PASSWORD")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    
    @property
    def redis_url(self) -> str:
        """Get Redis URL."""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


class S3Config(BaseConfig):
    """S3/MinIO configuration."""
    
    s3_endpoint: str = Field(alias="S3_ENDPOINT")
    s3_access_key: str = Field(alias="S3_ACCESS_KEY")
    s3_secret_key: str = Field(alias="S3_SECRET_KEY")
    s3_bucket: str = Field(default="ir-fitmark", alias="S3_BUCKET")
    s3_region: str = Field(default="us-east-1", alias="S3_REGION")
    s3_use_ssl: bool = Field(default=True, alias="S3_USE_SSL")


class AuthConfig(BaseConfig):
    """Authentication configuration."""
    
    secret_key: str = Field(alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # Keycloak configuration
    keycloak_url: str = Field(alias="KEYCLOAK_URL")
    keycloak_realm: str = Field(default="ir-fitmark", alias="KEYCLOAK_REALM")
    keycloak_client_id: str = Field(alias="KEYCLOAK_CLIENT_ID")
    keycloak_client_secret: str = Field(alias="KEYCLOAK_CLIENT_SECRET")
    
    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key length."""
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters long")
        return v


class AIConfig(BaseConfig):
    """AI/ML configuration."""
    
    ai_model_path: str = Field(default="/models", alias="AI_MODEL_PATH")
    ai_confidence_threshold: float = Field(default=0.8, alias="AI_CONFIDENCE_THRESHOLD")
    ai_batch_size: int = Field(default=32, alias="AI_BATCH_SIZE")
    ai_max_video_duration: int = Field(default=300, alias="AI_MAX_VIDEO_DURATION")  # seconds
    
    # OpenAI/External AI API configuration
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    ai_provider: str = Field(default="local", alias="AI_PROVIDER")  # local, openai, etc.


class AppConfig(BaseConfig):
    """Application configuration."""
    
    app_name: str = Field(default="IR FitMark", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=False, alias="DEBUG")
    
    # API configuration
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_workers: int = Field(default=1, alias="API_WORKERS")
    
    # CORS configuration
    cors_origins: List[str] = Field(default=["*"], alias="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, alias="CORS_ALLOW_CREDENTIALS")
    
    # Upload configuration
    max_upload_size: int = Field(default=50 * 1024 * 1024, alias="MAX_UPLOAD_SIZE")  # 50MB
    allowed_video_types: List[str] = Field(
        default=["video/mp4", "video/webm", "video/avi"],
        alias="ALLOWED_VIDEO_TYPES"
    )
    allowed_image_types: List[str] = Field(
        default=["image/jpeg", "image/png", "image/webp"],
        alias="ALLOWED_IMAGE_TYPES"
    )
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @field_validator("allowed_video_types", "allowed_image_types", mode="before")
    @classmethod
    def parse_allowed_types(cls, v) -> List[str]:
        """Parse allowed file types from string or list."""
        if isinstance(v, str):
            return [file_type.strip() for file_type in v.split(",")]
        return v


class Settings:
    """Global settings container."""
    
    def __init__(self):
        self.app = AppConfig()
        self.database = DatabaseConfig()
        self.redis = RedisConfig()
        self.s3 = S3Config()
        self.auth = AuthConfig()
        self.ai = AIConfig()
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.app.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.app.environment.lower() == "development"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing."""
        return self.app.environment.lower() == "testing"


# Global settings instance
settings = Settings()
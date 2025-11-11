"""Application configuration settings."""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # MongoDB Configuration
    # Support both old format (MONGODB_URI env var) and new format (individual components)
    mongodb_uri_override: Optional[str] = Field(default=None, alias="MONGODB_URI")
    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_username: str = ""
    mongodb_password: str = ""
    mongodb_auth_source: str = "admin"
    mongodb_db_name: str = "hna_catalog"
    
    @property
    def mongodb_uri(self) -> str:
        """Build MongoDB URI with optional authentication."""
        # If mongodb_uri_override is explicitly set (via MONGODB_URI env var), use it (backward compatibility)
        if self.mongodb_uri_override:
            return self.mongodb_uri_override
        
        # Otherwise, build from components
        if self.mongodb_username and self.mongodb_password:
            return f"mongodb://{self.mongodb_username}:{self.mongodb_password}@{self.mongodb_host}:{self.mongodb_port}/?authSource={self.mongodb_auth_source}"
        else:
            return f"mongodb://{self.mongodb_host}:{self.mongodb_port}/"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    admin_username: str = "admin"
    admin_password: str = "admin123"
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()


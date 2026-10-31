from functools import lru_cache

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SmartSpace AI API"
    environment: str = "local"
    api_v1_prefix: str = "/api/v1"
    backend_cors_origins: list[AnyHttpUrl] | list[str] = ["http://localhost:3000"]
    database_url: str = "postgresql+asyncpg://smartspace:smartspace@localhost:5432/smartspace_ai"
    sync_database_url: str = "postgresql://smartspace:smartspace@localhost:5432/smartspace_ai"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret_key: str = Field(min_length=32, default="change-this-secret-in-production-32")
    jwt_refresh_secret_key: str = Field(
        min_length=32, default="change-this-refresh-secret-in-production-32"
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14
    password_reset_token_expire_minutes: int = 30
    email_verification_token_expire_minutes: int = 1440
    rate_limit: str = "100/minute"
    upload_provider: str = "local"
    s3_bucket: str | None = None
    cloudinary_cloud_name: str | None = None
    cloudinary_api_key: str | None = None
    cloudinary_api_secret: str | None = None
    razorpay_key_id: str | None = None
    razorpay_key_secret: str | None = None
    stripe_secret_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


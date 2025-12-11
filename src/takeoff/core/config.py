from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    APP_NAME: str = Field(default="Takeoff", description="Name of the application")
    APP_ENV: str = Field(
        default="development", description="Environment (development, production)"
    )
    DEBUG: bool = Field(default=False, description="Enable debug mode")

    # Example external service config
    DATABASE_URL: str = Field(
        default="sqlite:///./takeoff.db", description="Database connection string"
    )
    OPENROUTER_API_KEY: str | None = Field(default=None, description="OpenRouter API Key")
    OPENROUTER_MODEL: str = Field(default="openai/gpt-3.5-turbo", description="Model ID")

settings = Settings()

"""Application settings with environment variable support."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    Configuration is loaded from:
    1. Environment variables
    2. .env file (if present)

    Attributes:
        google_cloud_project: GCP project ID for Vertex AI
        google_cloud_location: GCP region for Vertex AI (default: europe-west1)
        gemini_model_name: Gemini model to use (default: gemini-2.5-flash)
        imagen_model_name: Imagen model to use (default: imagen-4.0-generate-001)
        save_debug_images: Whether to save generated images locally for debugging
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Google Cloud Configuration
    google_cloud_project: str
    google_cloud_location: str = "europe-west1"

    # Model Configuration
    gemini_model_name: str = "gemini-2.5-flash"
    imagen_model_name: str = "imagen-4.0-generate-001"

    # Feature Flags
    save_debug_images: bool = False


# Singleton instance
settings = Settings()

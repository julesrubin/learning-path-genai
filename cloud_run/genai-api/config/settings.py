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
        rag_corpus_display_name: Display name used to look up the RAG Engine corpus.
        rag_embedding_model: Vertex AI embedding model used by the RAG corpus.
        rag_top_k: Number of chunks to retrieve per query.
        gemini_input_price_per_million: USD price per 1M input tokens for the active Gemini model.
        gemini_output_price_per_million: USD price per 1M output tokens for the active Gemini model.
        gemini_context_window: Maximum context window size in tokens for the active Gemini model.
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

    # RAG Engine Configuration
    rag_corpus_display_name: str = "styleco-knowledge-base"
    rag_embedding_model: str = "publishers/google/models/text-embedding-005"
    rag_top_k: int = 5

    # Gemini pricing & context window — see https://cloud.google.com/vertex-ai/generative-ai/pricing
    gemini_input_price_per_million: float = 0.30
    gemini_output_price_per_million: float = 2.50
    gemini_context_window: int = 1_000_000


# Singleton instance
settings = Settings()

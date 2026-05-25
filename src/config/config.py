from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        app_name: Public application name.
        app_env: Current application environment.
        database_url: PostgreSQL connection URL.
        gmail_credentials_file: Gmail credentials file path.
        gmail_token_file: Gmail OAuth token cache file path.
        google_calendar_credentials_file: Google Calendar credentials file path.
        telegram_bot_token: Telegram bot token.
        telegram_default_chat_id: Default Telegram chat ID.
        telegram_api_base_url: Telegram Bot API base URL.
        ai_provider: AI provider identifier.
        ai_model: AI model identifier.
        openai_api_key: OpenAI API key.
        followup_repository: Follow-up repository backend.
        vector_dimension: Embedding dimension for pgvector storage.
    """

    app_name: str = "Email AI Assistant"
    app_env: str = "local"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/email_ai_assistant"
    gmail_credentials_file: str = ""
    gmail_token_file: str = "credentials/gmail-token.json"
    google_calendar_credentials_file: str = ""
    telegram_bot_token: str = ""
    telegram_default_chat_id: str = ""
    telegram_api_base_url: str = "https://api.telegram.org"
    ai_provider: str = "openai"
    ai_model: str = "gpt-4o-mini"
    openai_api_key: str = ""
    followup_repository: str = "memory"
    vector_dimension: int = 1536

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

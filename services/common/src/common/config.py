from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global configuration for scraper services."""

    LOG_LEVEL: str = "ERROR"

    # Kafka / Redpanda
    REDPANDA_BROKERS: str = "redpanda:9092"
    EVENT_TOPIC: str = "events.raw"

    KAFKA_SOCKET_TIMEOUT_MS: int = 5000
    KAFKA_MAX_RETRIES: int = 2
    # KAFKA_RETRY_BACKOFF_MS: int = 1000
    KAFKA_RECONNECT_BACKOFF_MS: int = 1000
    KAFKA_MAX_QUEUE_MESSAGES: int = 10000
    KAFKA_DELIVERY_TIMEOUT_MS: int = 10000
    KAFKA_ACKS: str = "1"
    KAFKA_ENABLE_IDEMPOTENCE: bool = False
    KAFKA_CONNECT_TIMEOUT: int = 5  # seconds for non-blocking init

    # Other services
    MEILISEARCH_URL: str = "http://meilisearch:7700"
    MEILISEARCH_API_KEY: str = "MASTER_KEY"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

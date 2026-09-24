from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_version: str = "0.1.0"
    log_level: str = "INFO"

    database_url: str = "sqlite:///./detectlab.db"
    redis_url: str = "redis://localhost:6379/0"

    object_store_endpoint: str = "http://localhost:9000"
    object_store_bucket: str = "detectlab-evidence"
    object_store_access_key: str = "changeme"
    object_store_secret_key: str = "changeme"

    oidc_issuer: str = ""
    oidc_client_id: str = ""

    attack_catalog_path: str = "./fixtures/attack-catalog"
    attack_catalog_version: str = "vCurrent"

    validation_default_timeout_seconds: int = 120
    validation_allowed_modes: str = "synthetic,replay"
    max_fixture_mb: int = 10

    telemetry_freshness_minutes: int = 60
    target_capability_freshness_hours: int = 24


settings = Settings()
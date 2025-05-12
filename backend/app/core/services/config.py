from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Astronomy Comet Analysis API"
    log_level: str = "DEBUG"
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    db_path: str = "" #default: in-memory sqlite db
    model_config = SettingsConfigDict(env_file=".config")

settings = Settings()
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    db_path: str = ""
    model_config = SettingsConfigDict(env_file=".config")

settings = Settings()
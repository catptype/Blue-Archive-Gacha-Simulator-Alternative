from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CACHE_EXPIRE: int = 180 
    TOKEN_EXPIRE: int = 60
    APP_NAME: str = "Blue Archive Gacha Simulator (Backend)"
    LOG_LEVEL: str = "INFO"
    DEBUG_MODE: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- Auth Settings ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRE: int = 15 # Minutes
    
    CACHE_EXPIRE: int = 180 
    APP_NAME: str = "Blue Archive Gacha Simulator (Backend)"
    LOG_LEVEL: str = "INFO"
    DEBUG_MODE: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
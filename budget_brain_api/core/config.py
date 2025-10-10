from pydantic_settings import BaseSettings
import secrets
 
class Settings(BaseSettings):
    PROJECT_NAME: str = "BudgetBrain API"
    POSTGRES_USER: str = "administrator"
    POSTGRES_PASSWORD: str = "30026427"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5434"
    POSTGRES_DB: str = "budgetbrain_db"
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # Note: In Pydantic V2 (with pydantic-settings), 'Config' should ideally be 'model_config'
        # but BaseSettings keeps the Config inner class for backward compatibility.
        env_file = ".env"

settings = Settings()
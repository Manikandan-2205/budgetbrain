from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "BudgetBrain API"
    debug: bool = False
    version: str = "1.0.0"
    api_prefix: str = "/api"

    # Database - PostgreSQL connection
    database_url: str = "postgresql://administrator:2002@localhost:5432/bugetbrain?search_path=bb"

    # JWT
    secret_key: str = "DIsYG2ZJaHf-AidchOl9dDQXKLk1NH5KxNmyIRxWsrU"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # AI/ML
    openai_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()

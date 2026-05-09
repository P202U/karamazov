from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Karamazov"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://user:password@db:5432/interview_coach"

    # AI Keys
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()

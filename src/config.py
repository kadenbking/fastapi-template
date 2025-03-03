from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    APP_ENV: str = ""
    APP_VERSION: str = ""
    API_KEY: str = ""
    DB_HOST: str = ""
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_PORT: int = 0
    S3_BUCKET: str = ""

    VIEWED_TEAMS_LIMIT: int = 6

    model_config = SettingsConfigDict(env_file=".env")

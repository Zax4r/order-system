import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str = os.getenv('DATABASE_URL')

settings = Settings()

def get_db_url():
    return settings.DATABASE_URL